#!/usr/bin/env python3
"""
Minimal SNMPv2c client + OLT uplink bandwidth poller (pure Python stdlib).

Used by GponMonitorSystem to collect real uplink traffic from OLTs/switches
when running inside the VTVcab network. Falls back to mock data when SNMP
is unreachable or not configured.

Standard IF-MIB OIDs (work on ZTE / Huawei / Dasan / any SNMP device):
  ifDescr        1.3.6.1.2.1.2.2.1.2.<ifindex>
  ifHCInOctets   1.3.6.1.2.1.31.1.1.1.6.<ifindex>   (64-bit inbound octets)
  ifHCOutOctets  1.3.6.1.2.1.31.1.1.1.10.<ifindex>  (64-bit outbound octets)
"""

import socket
import time
import threading

IF_DESCR = "1.3.6.1.2.1.2.2.1.2"
IF_HC_IN = "1.3.6.1.2.1.31.1.1.1.6"
IF_HC_OUT = "1.3.6.1.2.1.31.1.1.1.10"

# ---------------------------------------------------------------- BER codec

def _enc_length(n):
    if n < 0x80:
        return bytes([n])
    b = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return bytes([0x80 | len(b)]) + b


def _tlv(tag, content):
    return bytes([tag]) + _enc_length(len(content)) + content


def _enc_uint(n):
    if n < 0:
        raise ValueError("only non-negative ints supported")
    b = n.to_bytes((n.bit_length() + 7) // 8 or 1, "big")
    if b[0] & 0x80:
        b = b"\x00" + b
    return _tlv(0x02, b)


def _enc_octets(s):
    if isinstance(s, str):
        s = s.encode("utf-8")
    return _tlv(0x04, s)


def _enc_null():
    return _tlv(0x05, b"")


def _enc_oid(oid):
    parts = [int(x) for x in oid.strip(".").split(".")]
    out = bytes([40 * parts[0] + parts[1]])
    for p in parts[2:]:
        stack = [p & 0x7F]
        p >>= 7
        while p:
            stack.append(0x80 | (p & 0x7F))
            p >>= 7
        out += bytes(reversed(stack))
    return _tlv(0x06, out)


def _enc_seq(children):
    return _tlv(0x30, b"".join(children))


def build_get(community, oids, request_id, pdu_tag=0xA0):
    """Build SNMPv2c GetRequest (0xA0) or GetNextRequest (0xA1)."""
    vbl = _enc_seq([_enc_seq([_enc_oid(o), _enc_null()]) for o in oids])
    pdu = _tlv(pdu_tag, _enc_uint(request_id) + _enc_uint(0) + _enc_uint(0) + vbl)
    return _enc_seq([_enc_uint(1), _enc_octets(community), pdu])


def _dec_tlv(buf, pos):
    tag = buf[pos]
    pos += 1
    lb = buf[pos]
    pos += 1
    if lb & 0x80:
        n = lb & 0x7F
        length = int.from_bytes(buf[pos:pos + n], "big")
        pos += n
    else:
        length = lb
    return tag, buf[pos:pos + length], pos + length


def _dec_oid(content):
    first = content[0]
    parts = [first // 40, first % 40]
    val = 0
    for b in content[1:]:
        val = (val << 7) | (b & 0x7F)
        if not (b & 0x80):
            parts.append(val)
            val = 0
    return ".".join(str(p) for p in parts)


def _dec_value(tag, content):
    if tag == 0x02:
        return int.from_bytes(content, "big", signed=True)
    if tag in (0x41, 0x42, 0x43, 0x46):  # Counter32/Gauge32/TimeTicks/Counter64
        return int.from_bytes(content, "big", signed=False)
    if tag == 0x04:
        try:
            return content.decode("utf-8", errors="replace")
        except Exception:
            return content
    if tag == 0x05:
        return None
    if tag == 0x06:
        return _dec_oid(content)
    if tag == 0x30 or 0xA0 <= tag <= 0xA3:
        vals = []
        p = 0
        while p < len(content):
            t, c, p = _dec_tlv(content, p)
            vals.append(_dec_value(t, c))
        return vals
    return content


def _parse_response(data, request_id):
    tag, content, _ = _dec_tlv(data, 0)
    if tag != 0x30:
        raise ValueError("not an SNMP message")
    msg = _dec_value(tag, content)  # [version, community, pdu[...]]
    pdu = msg[2]
    # pdu decoded as list: [request_id, error_status, error_index, [[oid, val], ...]]
    if not isinstance(pdu, list) or len(pdu) != 4:
        raise ValueError("malformed PDU")
    if pdu[0] != request_id:
        raise ValueError("request-id mismatch")
    if pdu[1] != 0:
        raise ValueError(f"SNMP error-status {pdu[1]} at index {pdu[2]}")
    return [(vb[0], vb[1]) for vb in pdu[3]]


def _exchange(ip, community, oids, pdu_tag, timeout, port):
    rid = int(time.time() * 1000) & 0x7FFFFFFF
    req = build_get(community, oids, rid, pdu_tag)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(timeout)
    try:
        s.sendto(req, (ip, port))
        data, _ = s.recvfrom(65535)
    finally:
        s.close()
    return _parse_response(data, rid)


def snmp_get(ip, community, oids, timeout=3, port=161):
    """GET one or more OIDs. Returns {oid: value}."""
    if isinstance(oids, str):
        oids = [oids]
    return dict(_exchange(ip, community, oids, 0xA0, timeout, port))


def snmp_getnext(ip, community, oids, timeout=3, port=161):
    """GETNEXT. Returns [(next_oid, value), ...]."""
    if isinstance(oids, str):
        oids = [oids]
    return _exchange(ip, community, oids, 0xA1, timeout, port)


def snmp_walk(ip, community, base_oid, timeout=3, port=161, max_rows=500):
    """Walk a subtree. Returns [(oid, value), ...]."""
    base = base_oid.strip(".") + "."
    rows = []
    cur = base_oid.strip(".")
    for _ in range(max_rows):
        nxt = snmp_getnext(ip, community, cur, timeout, port)[0]
        if not nxt[0].startswith(base):
            break
        rows.append(nxt)
        cur = nxt[0]
    return rows


# ------------------------------------------------------- bandwidth poller

def _fmt_bps(bps):
    if bps >= 1e9:
        return f"{bps / 1e9:.2f}G"
    if bps >= 1e6:
        return f"{bps / 1e6:.2f}M"
    if bps >= 1e3:
        return f"{bps / 1e3:.0f}K"
    return f"{bps:.0f}"


class BandwidthPoller(threading.Thread):
    """Polls uplink counters via SNMP and computes bps. Daemon thread."""

    def __init__(self, devices, community="public", interval=60, timeout=4,
                 port=161, history_len=120):
        super().__init__(daemon=True)
        self.devices = devices or []
        self.community = community
        self.interval = interval
        self.timeout = timeout
        self.port = port
        self.history_len = history_len
        self.lock = threading.Lock()
        self.state = {}   # oltid -> {"ip":..., "uplinks": {name: {...}}}
        self.errors = {}

    def _poll_device(self, dev):
        oltid = dev.get("oltid", dev.get("ip"))
        ip = dev["ip"]
        result = {}
        for up in dev.get("uplinks", []):
            name = up.get("name", f"if{up['ifindex']}")
            idx = up["ifindex"]
            try:
                vals = snmp_get(ip, self.community,
                                [f"{IF_HC_IN}.{idx}", f"{IF_HC_OUT}.{idx}"],
                                timeout=self.timeout, port=self.port)
                in_oct = vals.get(f"{IF_HC_IN}.{idx}")
                out_oct = vals.get(f"{IF_HC_OUT}.{idx}")
                if not isinstance(in_oct, int) or not isinstance(out_oct, int):
                    raise ValueError("bad counter values")
                now = time.time()
                prev = self.state.get(oltid, {}).get("uplinks", {}).get(name)
                in_bps = out_bps = 0.0
                if prev and prev.get("in_oct") is not None:
                    dt = now - prev["ts"]
                    if dt > 0:
                        d_in = in_oct - prev["in_oct"]
                        d_out = out_oct - prev["out_oct"]
                        # counter reset / wrap -> ignore this sample
                        if d_in >= 0:
                            in_bps = d_in * 8 / dt
                        if d_out >= 0:
                            out_bps = d_out * 8 / dt
                hist = (prev.get("history", []) if prev else [])[-self.history_len + 1:]
                hist.append({"t": int(now), "in": round(in_bps), "out": round(out_bps)})
                result[name] = {
                    "ifindex": idx, "in_bps": round(in_bps), "out_bps": round(out_bps),
                    "in_str": _fmt_bps(in_bps), "out_str": _fmt_bps(out_bps),
                    "total_str": _fmt_bps(in_bps + out_bps),
                    "in_oct": in_oct, "out_oct": out_oct, "ts": now,
                    "history": hist, "ok": True,
                }
                self.errors.pop(f"{oltid}/{name}", None)
            except Exception as e:
                self.errors[f"{oltid}/{name}"] = str(e)[:120]
                prev = self.state.get(oltid, {}).get("uplinks", {}).get(name, {})
                result[name] = dict(prev, ok=False) if prev else {"ok": False, "error": str(e)[:120]}
        with self.lock:
            self.state[oltid] = {"ip": ip, "uplinks": result}

    def poll_once(self):
        for dev in self.devices:
            try:
                self._poll_device(dev)
            except Exception as e:
                self.errors[dev.get("oltid", dev.get("ip"))] = str(e)[:120]

    def snapshot(self):
        with self.lock:
            out = {"mode": "live", "updated": time.strftime("%Y-%m-%d %H:%M:%S"),
                   "links": [], "errors": dict(self.errors)}
            for oltid, dev in self.state.items():
                for name, u in dev["uplinks"].items():
                    if not u.get("ok"):
                        continue
                    out["links"].append({
                        "oltid": oltid, "ip": dev["ip"], "name": name,
                        "in_bps": u["in_bps"], "out_bps": u["out_bps"],
                        "in_str": u["in_str"], "out_str": u["out_str"],
                        "total_str": u["total_str"],
                    })
            return out

    def run(self):
        while True:
            try:
                self.poll_once()
            except Exception:
                pass
            time.sleep(self.interval)
