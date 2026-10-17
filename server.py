#!/usr/bin/env python3
"""
NOC Unified Monitor, OLT Tools, ONU Management & PRTG 10G Sensor Telemetry Server
Full Port matching VTVcab NOC & PRTG Network Monitor (Paessler style):
- Cong cu OLT (views/quanlyolt.php)
- Cong cu ONU (views/quanlyonu.php)
- Giam sat OLT & Bang thong Admin (Weathermap & RRDtool)
- PRTG 10G Sensors:
  * (285279233) xgei-1/4/1 Traffic 10 GBit/s (BIH.OLT.27)
  * (900003) XE0/3 Link1 connect nx3000 Traffic 10 GBit/s (BIH.OLT.05)
  * (900004) XE0/4 Link2 connect nx3000 Traffic 10 GBit/s (BIH.OLT.05)
  * (900002) XE0/2 [Downlink][Xe0/1][BIH.OLT.19] Traffic 10 GBit/s
  * Device BIH.OLT.019 (Long Bình Tân) - Alarms Ping & XE0/1 Down
Runs on 0.0.0.0:8765
"""

import http.server
import socketserver
import json
import time
import math
import random
import hashlib
import os
import sys
from urllib.parse import parse_qs, urlparse

PORT = 8765
HOST = "0.0.0.0"

# Provinces & OLTs
PROVINCES = [
    {"PROVINCE": "Đồng Nai"},
    {"PROVINCE": "Hồ Chí Minh"},
    {"PROVINCE": "Bình Dương"},
    {"PROVINCE": "Hà Nội"}
]

OLTS_BY_PROVINCE = {
    "Đồng Nai": [
        {"OLTID": "BIH.OLT.01", "NAME": "OLT 01 - Biên Hòa", "TYPE": "ZTE", "MODEL": "ZXA10 C620", "IP": "172.19.117.31"},
        {"OLTID": "BIH.OLT.02", "NAME": "OLT 02 - Hố Nai", "TYPE": "ZTE", "MODEL": "ZXA10 C620", "IP": "172.19.117.32"},
        {"OLTID": "BIH.OLT.03", "NAME": "OLT 03 - Trảng Dài", "TYPE": "HUAWEI", "MODEL": "MA5800-X7", "IP": "172.19.117.33"},
        {"OLTID": "BIH.OLT.04", "NAME": "OLT 04 - Thống Nhất", "TYPE": "ZTE", "MODEL": "ZXA10 C620", "IP": "172.19.117.34"},
        {"OLTID": "BIH.OLT.05", "NAME": "OLT 05 - Long Thành", "TYPE": "ZTE", "MODEL": "ZXA10 C600", "IP": "172.19.117.35"},
        {"OLTID": "BIH.OLT.06", "NAME": "OLT 06 - Long Khánh", "TYPE": "ZTE", "MODEL": "ZXA10 C620", "IP": "172.19.117.36"},
        {"OLTID": "BIH.OLT.019", "NAME": "OLT 19 - Long Bình Tân", "TYPE": "ZTE", "MODEL": "ZXA10 C620", "IP": "172.20.160.21"},
        {"OLTID": "BIH.OLT.27", "NAME": "OLT 27 - Hóa An", "TYPE": "ZTE", "MODEL": "ZXA10 C620", "IP": "172.20.160.27"}
    ]
}

# ALL PRTG 10G SENSORS (From All 6 User Screenshots)
PRTG_SENSORS = [
    {
        "id": "285279233",
        "name": "xgei-1/4/1 Traffic 10 GBit/s",
        "device": "BIH.OLT.27 (Hóa An)",
        "ip": "172.20.160.27",
        "status": "OK",
        "last_scan": "18 s",
        "last_up": "18 s",
        "last_down": "34 m 3 s",
        "uptime": "99.9455%",
        "downtime": "0.0545%",
        "coverage": "100%",
        "type": "SNMP Traffic 64bit",
        "speed": "10 GBit/s",
        "max_kbits": 81849,
        "min_kbits": 42,
        "mode": "live",
        "scale": 0.08
    },
    {
        "id": "900003",
        "name": "XE0/3 Link1 connect nx3000Traffic 10 GBit/s",
        "device": "BIH.OLT.05 (Long Thành)",
        "ip": "172.19.117.35",
        "status": "OK",
        "last_scan": "22 s",
        "last_up": "22 s",
        "last_down": "2 d 8 h 46 m",
        "uptime": "99.7700%",
        "downtime": "0.2300%",
        "coverage": "100%",
        "type": "SNMP Traffic 64bit",
        "speed": "10 GBit/s",
        "max_kbits": 4485260,
        "min_kbits": 349271,
        "mode": "2days",
        "scale": 4.5
    },
    {
        "id": "900004",
        "name": "XE0/4 Link2 connect nx3000Traffic 10 GBit/s",
        "device": "BIH.OLT.05 (Long Thành)",
        "ip": "172.19.117.35",
        "status": "OK",
        "last_scan": "35 s",
        "last_up": "35 s",
        "last_down": "2 d 8 h 46 m",
        "uptime": "99.7869%",
        "downtime": "0.2131%",
        "coverage": "100%",
        "type": "SNMP Traffic 64bit",
        "speed": "10 GBit/s",
        "max_kbits": 4316371,
        "min_kbits": 365255,
        "mode": "2days",
        "scale": 4.3
    },
    {
        "id": "900002",
        "name": "XE0/2 [Downlink][Xe0/1][BIH.OLT.19]Traffic 10 GBit/s",
        "device": "BIH.OLT.019 (Long Bình Tân)",
        "ip": "172.20.160.21",
        "status": "OK",
        "last_scan": "36 s",
        "last_up": "36 s",
        "last_down": "-",
        "uptime": "100.0000%",
        "downtime": "0.0000%",
        "coverage": "100%",
        "type": "SNMP Traffic 64bit",
        "speed": "10 GBit/s",
        "max_kbits": 1076831,
        "min_kbits": 73739,
        "mode": "2days",
        "scale": 1.1
    },
    {
        "id": "900001",
        "name": "XE0/1 XE0/1Traffic 10 GBit/s",
        "device": "BIH.OLT.019 (Long Bình Tân)",
        "ip": "172.20.160.21",
        "status": "Down",
        "last_scan": "60 s",
        "last_up": "-",
        "last_down": "5 h 12 m",
        "uptime": "0.0000%",
        "downtime": "100.0000%",
        "coverage": "100%",
        "type": "SNMP Traffic 64bit",
        "speed": "10 GBit/s",
        "max_kbits": 0,
        "min_kbits": 0,
        "mode": "alarm",
        "scale": 0,
        "message": "No response (check: firewalls, routing, snmp settings of device, IPs, SNMP version, community, passwords etc) (SNMP error # -2003)"
    }
]

def _seeded_rng(*parts):
    """Deterministic RNG so mock data is stable between reloads."""
    h = hashlib.md5(("|".join(str(p) for p in parts)).encode("utf-8")).hexdigest()
    return random.Random(int(h[:8], 16))


def generate_olt_ports(maolt):
    rng = _seeded_rng("olt_ports", maolt)
    # OLT type/model lookup (fallback ZTE C620)
    olt_info = {}
    for _prov, olts in OLTS_BY_PROVINCE.items():
        for o in olts:
            olt_info[o["OLTID"]] = o
    info = olt_info.get(maolt, {"TYPE": "ZTE", "MODEL": "ZXA10 C620"})
    ports = []
    for slot in range(1, 3):
        for port in range(1, 9):
            act = rng.randint(35, 62)
            inact = rng.randint(1, 7)
            ports.append({
                "PORTPON": f"1/{slot}/{port}",
                "ACTONU": act,
                "INACTONU": inact,
                "TOTALONU": act + inact,
                "TYPE_OLT": info["TYPE"],
                "MODELS": info["MODEL"]
            })
    return ports


# Reference data pools for mock ONU generation (ported from VTVcab)
_MOCK_MODELS = ["ZXHN F670L", "ZXHN F6600P", "ZXHN F660", "HG6245D", "HG8145V5", "ZXHN F680"]
_MOCK_PROFILES = ["HSI_150M_IPTV", "HSI_200M_VIP", "HSI_100M", "HSI_300M_GAME", "HSI_80M"]
_MOCK_BRANCHES = ["Đồng Nai - Thống Nhất", "Đồng Nai - Biên Hòa", "Đồng Nai - Long Thành",
                  "Đồng Nai - Trảng Dài", "Đồng Nai - Long Khánh"]
_MOCK_STREETS = ["Đường 21/4, TT. Dầu Giây", "Ấp Hưng Nghĩa, Xã Hưng Lộc", "KP 3, P. Tân Hiệp",
                 "Ấp Bình Minh, Xã Bình Minh", "Đường Võ Thị Sáu, P. Thống Nhất",
                 "KP 5, P. Long Bình Tân", "Ấp Tân Lập, Xã Bàu Hàm"]
_MOCK_FW = ["V1.1.0P1T1", "V1.1.0P2T2", "V2.0.1P3T1", "V1.0.0P1T5"]


def generate_mock_onus(maolt, portpon, count=None):
    """Generate deterministic mock ONUs for a given OLT port (DS ONU per port)."""
    rng = _seeded_rng("port_onus", maolt, portpon)
    olt_info = {}
    for _prov, olts in OLTS_BY_PROVINCE.items():
        for o in olts:
            olt_info[o["OLTID"]] = o
    info = olt_info.get(maolt, {"TYPE": "ZTE", "MODEL": "ZXA10 C620", "IP": "172.19.117.34"})
    if count is None:
        count = rng.randint(8, 16)
    onus = []
    for i in range(1, count + 1):
        sn = "ZTEGC" + "".join(rng.choice("0123456789ABCDEF") for _ in range(8))
        active = rng.random() > 0.12
        rx = round(rng.uniform(-27.5, -17.5), 2)
        model = rng.choice(_MOCK_MODELS)
        onus.append({
            "ROW_NUM": i,
            "SNONU": sn,
            "STATUS_NAME": "Active" if active else "Offline",
            "RXPOWER": rx,
            "RXPOWER_1310": round(rx - rng.uniform(0.3, 1.5), 2),
            "BRANCH": rng.choice(_MOCK_BRANCHES),
            "ADDRESS": f"{rng.randint(1, 350)} {rng.choice(_MOCK_STREETS)}",
            "MODE_NAME": rng.choice(["Route", "Bridge"]),
            "PROFILEREG": rng.choice(_MOCK_PROFILES),
            "FIRMWARE": rng.choice(_MOCK_FW),
            "DEACTIVE_NAME": "-" if active else rng.choice(["LOSi", "DyingGasp", "PowerOff"]),
            "INACTIVE_TIME": 0 if active else rng.randint(60, 86400),
            "SNOLT": maolt,
            "PORTPON": portpon,
            "ONUID": rng.randint(1, 64),
            "MODEL": model,
            "DISTANCE": f"{rng.randint(200, 8500)} m",
            "CREATEDATE": f"2026-{rng.randint(1, 9):02d}-{rng.randint(1, 28):02d} "
                          f"{rng.randint(0, 23):02d}:{rng.randint(0, 59):02d}:00",
            "TYPE_OLT": info["TYPE"],
            "OLTIP": info["IP"],
            "MODELS": model
        })
    return onus


# In-memory operation history log (port of api/data/loaddata_themmoilichsu.php)
HISTORY_LOG = []


def _mock_firmware_list(model):
    """Deterministic firmware list per ONU model (xn=loadListFW)."""
    rng = _seeded_rng("fw_list", model or "GENERIC")
    base = (model or "F670L").replace("ZXHN ", "").replace(" ", "")
    vers = ["V1.1.0P1T1", "V1.1.0P2T2", "V2.0.1P3T1", "V1.0.0P1T5"]
    rng.shuffle(vers)
    return [{"NAME_FIRMWARE": f"{base}_{v}.bin"} for v in vers[:3]]


def _mock_odf_info(snonu):
    """Mock ODF/S2 path info (xn=getODF)."""
    rng = _seeded_rng("odf", snonu)
    return f"""
<pre style="background: #000; color: #7CFC00; padding: 12px; border-radius: 4px; font-family: Consolas, monospace; font-size: 13px; line-height: 1.5;">
[ODF / HOP S2] - ONU: {snonu}
---------------------------------------------------------------------
Splitter Level 1      : S1-{rng.randint(1, 16):02d} (ODF Trung tam)
Splitter Level 2      : S2-{rng.randint(1, 8):02d} (Hop cap {rng.randint(1, 48)})
Port S2               : {rng.randint(1, 16)}
Suy hao do duoc       : {round(rng.uniform(0.8, 2.4), 2)} dB
Trang thai hop        : OK
---------------------------------------------------------------------
</pre>"""


def _mock_customer_info(snonu):
    """Mock customer info (api/tools/layttkh.php)."""
    rng = _seeded_rng("customer", snonu)
    return f"""
<table class="table table-bordered table-sm" style="font-size: 13px;">
<tbody>
<tr><th width="180">Ma ONU</th><td><b>{snonu}</b></td></tr>
<tr><th>Khach hang</th><td>Nguyen Van {rng.choice(['An', 'Binh', 'Chi', 'Dung', 'Em'])}</td></tr>
<tr><th>Dia chi lap dat</th><td>{rng.randint(1, 350)} {rng.choice(_MOCK_STREETS)}</td></tr>
<tr><th>So dien thoai</th><td>09{rng.randint(10000000, 99999999)}</td></tr>
<tr><th>Goi cuoc</th><td>{rng.choice(_MOCK_PROFILES)}</td></tr>
<tr><th>Trang thai thue bao</th><td><span class="badge badge-success">Dang hoat dong</span></td></tr>
</tbody>
</table>"""


def _mock_onu_diagnostics(maonu, portpon, onuid, tientrinh, typeolt):
    """Mock ONU telnet diagnostics (tientrinh=pppoe | real)."""
    rng = _seeded_rng("onu_diag", maonu, tientrinh)
    if tientrinh == "pppoe":
        user = f"kh{rng.randint(10000, 99999)}@vtvcab"
        return f"""
<pre style="background: #000; color: #f8cb00; padding: 12px; border-radius: 4px; font-family: Consolas, monospace; font-size: 13px; line-height: 1.5;">
[PPPoE DIAGNOSTICS] - ONU: {maonu} (ID {onuid}, Port {portpon})
---------------------------------------------------------------------
PPPoE Session         : Up
Username              : {user}
Session ID            : {rng.randint(1000, 9999)}
Session Uptime        : {rng.randint(1, 72)}h {rng.randint(0, 59)}m
IP Address            : 14.{rng.randint(160, 190)}.{rng.randint(0, 255)}.{rng.randint(2, 254)}
Gateway               : 14.160.0.1
DNS                   : 203.162.4.191 / 203.162.4.190
---------------------------------------------------------------------
</pre>"""
    rx = round(rng.uniform(-27.5, -17.5), 2)
    tx = round(rng.uniform(-3.0, 2.5), 2)
    return f"""
<pre style="background: #000; color: #f8cb00; padding: 12px; border-radius: 4px; font-family: Consolas, monospace; font-size: 13px; line-height: 1.5;">
[SIGNAL DIAGNOSTICS] - ONU: {maonu} (ID {onuid}, Port {portpon}, {typeolt})
---------------------------------------------------------------------
Rx Power (1490nm)     : {rx} dBm
Tx Power (1310nm)     : {tx} dBm
Temperature           : {round(rng.uniform(35.0, 55.0), 1)} C
Voltage               : {round(rng.uniform(3.2, 3.4), 2)} V
Distance              : {rng.randint(200, 8500)} m
ONU Status            : Online
---------------------------------------------------------------------
</pre>"""


def _mock_firmware_os(maonu_label, onuid):
    rng = _seeded_rng("fw_os", maonu_label, str(onuid))
    cur = rng.choice(["V1.1.0P1T1", "V1.1.0P2T2"])
    return f"""
<table class="table table-bordered table-sm" style="font-size: 13px;">
<thead><tr><th>OS</th><th>Firmware Version</th><th>Trang thai</th></tr></thead>
<tbody>
<tr><td><b>OS1</b></td><td>{cur}</td><td><span class="badge badge-success">Active</span></td></tr>
<tr><td><b>OS2</b></td><td>V1.0.0P1T5</td><td><span class="badge badge-secondary">Standby</span></td></tr>
</tbody>
</table>"""

MOCK_ONUS = [
    {
        "ROW_NUM": 1,
        "SNONU": "ZTEGC7A19B32",
        "STATUS_NAME": "Active",
        "RXPOWER": -19.45,
        "RXPOWER_1310": -20.12,
        "BRANCH": "Đồng Nai - Thống Nhất",
        "ADDRESS": "142 Đường 21/4, TT. Dầu Giây",
        "MODE_NAME": "Route",
        "PROFILEREG": "HSI_150M_IPTV",
        "FIRMWARE": "V1.1.0P1T1",
        "DEACTIVE_NAME": "-",
        "INACTIVE_TIME": 0,
        "SNOLT": "BIH.OLT.04",
        "PORTPON": "1/1/1",
        "ONUID": 14,
        "MODEL": "ZXHN F670L",
        "DISTANCE": "1250 m",
        "CREATEDATE": "2026-03-12 09:30:15",
        "TYPE_OLT": "ZTE",
        "OLTIP": "172.19.117.34",
        "MODELS": "F670L"
    },
    {
        "ROW_NUM": 2,
        "SNONU": "ZTEGC8B23C41",
        "STATUS_NAME": "Active",
        "RXPOWER": -22.10,
        "RXPOWER_1310": -23.05,
        "BRANCH": "Đồng Nai - Thống Nhất",
        "ADDRESS": "88 Ấp Hưng Nghĩa, Xã Hưng Lộc",
        "MODE_NAME": "Route",
        "PROFILEREG": "HSI_200M_VIP",
        "FIRMWARE": "V1.1.0P2T2",
        "DEACTIVE_NAME": "-",
        "INACTIVE_TIME": 0,
        "SNOLT": "BIH.OLT.04",
        "PORTPON": "1/1/1",
        "ONUID": 22,
        "MODEL": "ZXHN F6600P",
        "DISTANCE": "2180 m",
        "CREATEDATE": "2026-04-05 14:15:20",
        "TYPE_OLT": "ZTE",
        "OLTIP": "172.19.117.34",
        "MODELS": "F6600P"
    }
]


def _fmt_bw(bps):
    if bps >= 1e9:
        return f"{bps / 1e9:.2f}G"
    if bps >= 1e6:
        return f"{bps / 1e6:.2f}M"
    if bps >= 1e3:
        return f"{bps / 1e3:.0f}K"
    return f"{bps:.0f}"


# ------------------------------------------------- SNMP bandwidth config
def _load_snmp_config():
    cfg = {"enabled": False, "community": "public", "devices": [],
           "poll_interval": 60, "timeout": 4, "port": 161}
    try:
        base = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base, "config.json"), encoding="utf-8") as f:
            user = json.load(f).get("snmp", {})
        cfg.update({k: v for k, v in user.items() if not str(k).startswith("_")})
    except Exception:
        pass
    return cfg


SNMP_CONFIG = _load_snmp_config()

try:
    import snmp_poller
    _SNMP_OK = True
except Exception:
    _SNMP_OK = False

BW_POLLER = None


def _mock_bandwidth_links():
    """Deterministic mock uplink data (used when SNMP is unavailable)."""
    rng = _seeded_rng("weathermap", time.strftime("%Y-%m-%d %H"))
    links = []
    pairs = [("BIH.OLT.02", "xgei-1/4/1", 1.65e9),
             ("BIH.OLT.03", "xgei-1/4/1", 2.82e9),
             ("BIH.OLT.04", "xgei-1/4/1", 1.35e9)]
    for oltid, name, base in pairs:
        total = base * rng.uniform(0.85, 1.15)
        links.append({"oltid": oltid, "ip": "", "name": name,
                      "in_bps": int(total * 0.85), "out_bps": int(total * 0.15),
                      "in_str": _fmt_bw(total * 0.85), "out_str": _fmt_bw(total * 0.15),
                      "total_str": _fmt_bw(total)})
    return links


class NOCUnifiedHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        content_len = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_len).decode('utf-8', errors='ignore')
        params = parse_qs(post_body)
        xn = params.get('xn', [''])[0]

        # 1. API: getDataUnit.php
        if 'getDataUnit.php' in parsed.path:
            if xn == 'getODF':
                # HTML fragment (not JSON) - inserted into #ketquaODF
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                snonu = params.get('snonu', [''])[0]
                self.wfile.write(_mock_odf_info(snonu).encode('utf-8'))
                return
            if xn == 'updateCustomerInfo':
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(b'TRUE')
                return
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            if xn == 'getProvinceOLT':
                self.wfile.write(json.dumps(PROVINCES).encode('utf-8'))
                return
            elif xn == 'getSingleOLT':
                tentinh = params.get('tentinh', ['Đồng Nai'])[0]
                olts = OLTS_BY_PROVINCE.get(tentinh, OLTS_BY_PROVINCE['Đồng Nai'])
                self.wfile.write(json.dumps(olts).encode('utf-8'))
                return
            elif xn == 'loadListFW':
                type_fw = params.get('type_fw', [''])[0]
                self.wfile.write(json.dumps(_mock_firmware_list(type_fw)).encode('utf-8'))
                return

        # 2. API: loaddata_olt.php  (xn=loadPortOlt)
        elif 'loaddata_olt.php' in parsed.path:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            maolt = params.get('maolt', ['BIH.OLT.01'])[0]
            draw = int(params.get('draw', ['1'])[0] or 1)
            ports = generate_olt_ports(maolt)
            res = {"draw": draw, "recordsTotal": len(ports), "recordsFiltered": len(ports), "data": ports}
            self.wfile.write(json.dumps(res).encode('utf-8'))
            return

        # 3. API: loaddata_onu.php  (searchOnu / DS ONU per port)
        elif 'loaddata_onu.php' in parsed.path:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            maonu_filter = params.get('maonu', [''])[0].strip().upper()
            maolt_filter = params.get('maolt', [''])[0].strip()
            portpon_filter = params.get('portpon', [''])[0].strip()
            draw = int(params.get('draw', ['1'])[0] or 1)
            if portpon_filter:
                # DS ONU theo port: mock ONU sinh theo (maolt, portpon)
                onus = generate_mock_onus(maolt_filter or 'BIH.OLT.01', portpon_filter)
                total = len(onus)
                if maonu_filter and maonu_filter != 'ALL':
                    onus = [o for o in onus if maonu_filter in o['SNONU'].upper()
                            or maonu_filter in o['ADDRESS'].upper()]
                res = {"draw": draw, "recordsTotal": total, "recordsFiltered": len(onus), "data": onus}
            else:
                onus = list(MOCK_ONUS)
                if maolt_filter:
                    onus = [o for o in onus if maolt_filter in o['SNOLT']]
                if maonu_filter and maonu_filter != 'ALL':
                    onus = [o for o in onus if maonu_filter in o['SNONU'].upper()
                            or maonu_filter in o['ADDRESS'].upper()]
                # loitinhieu: Rx Power < -26 dBm ; trangthai: Active
                if params.get('loitinhieu', [''])[0] == 'true':
                    onus = [o for o in onus if o['RXPOWER'] < -26]
                if params.get('trangthai', [''])[0] == 'true':
                    onus = [o for o in onus if o['STATUS_NAME'] == 'Active']
                res = {"draw": draw, "recordsTotal": len(MOCK_ONUS), "recordsFiltered": len(onus), "data": onus}
            self.wfile.write(json.dumps(res).encode('utf-8'))
            return

        # 4. API: getTelnet.php  (Show Port / PPPoE / Signal diagnostics)
        elif 'getTelnet.php' in parsed.path:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            maolt = params.get('maolt', [''])[0]
            olt_ip = params.get('oltIP', ['172.19.117.34'])[0]
            portpon = params.get('portpon', ['1/1/1'])[0]
            onuid = params.get('onuid', [''])[0]
            maonu = params.get('maonu', [''])[0]
            tientrinh = params.get('tientrinh', [''])[0]
            typeolt = params.get('typeolt', params.get('type_olt', ['ZTE']))[0]
            models = params.get('models', ['ZXA10 C620'])[0]
            if tientrinh in ('pppoe', 'real'):
                self.wfile.write(_mock_onu_diagnostics(maonu, portpon, onuid, tientrinh, typeolt).encode('utf-8'))
                return
            rng = _seeded_rng("port_telnet", maolt or olt_ip, portpon)
            act = rng.randint(35, 62)
            tx = round(rng.uniform(2.5, 6.5), 2)
            temp = round(rng.uniform(38.0, 52.0), 1)
            volt = round(rng.uniform(3.25, 3.40), 2)
            res_html = f"""
<pre style="background: #000; color: #f8cb00; padding: 12px; border-radius: 4px; font-family: Consolas, monospace; font-size: 13px; line-height: 1.5;">
[PORT DIAGNOSTICS] - OLT: {maolt or olt_ip} ({typeolt} {models})
---------------------------------------------------------------------
Port                  : gpon_olt-{portpon} (SFP GPON Class C+)
Port State            : Up / Enabled
SFP Module Model      : GPON-OLT-CLASS-C+
TX Optical Power      : +{tx} dBm
Supply Voltage        : {volt} V
Temperature           : {temp} C
Active ONUs           : {act} ONUs
---------------------------------------------------------------------
</pre>"""
            self.wfile.write(res_html.encode('utf-8'))
            return

        # 5. API: laydanhsach_firmware_os.php  (firmware OS versions)
        elif 'laydanhsach_firmware_os.php' in parsed.path:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            onuid = params.get('onuid', [''])[0]
            olt_ip = params.get('oltIP', [''])[0]
            self.wfile.write(_mock_firmware_os(olt_ip, onuid).encode('utf-8'))
            return

        # 6. API: telnet_update_firmware_onu.php  (Download FW)
        elif 'telnet_update_firmware_onu.php' in parsed.path:
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'TRUE')
            return

        # 7. API: telnet_commit_firmware_onu.php  (Commit OS)
        elif 'telnet_commit_firmware_onu.php' in parsed.path:
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'TRUE')
            return

        # 8. API: telnet_reset_onu.php  (xn=reset)
        elif 'telnet_reset_onu.php' in parsed.path:
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            if xn == 'reset':
                HISTORY_LOG.append({
                    "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "noidung": "Reset ONU: OLT=%s;PortPon=%s;ONUID=%s" % (
                        params.get('oltIP', [''])[0], params.get('portpon', [''])[0],
                        params.get('onuid', [''])[0])
                })
                self.wfile.write(b'TRUE')
            else:
                self.wfile.write(b'FALSE')
            return

        # 9. API: layttkh.php  (customer info)
        elif 'layttkh.php' in parsed.path:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            snonu = params.get('snonu', [''])[0]
            self.wfile.write(_mock_customer_info(snonu).encode('utf-8'))
            return

        # 10. API: loaddata_themmoilichsu.php  (operation history log)
        elif 'loaddata_themmoilichsu.php' in parsed.path:
            if xn == 'getHistory':
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                maonu = params.get('maonu', [''])[0]
                entries = [e for e in HISTORY_LOG if not maonu or maonu in e['noidung']]
                entries = entries[-100:]
                self.wfile.write(json.dumps({"data": entries}).encode('utf-8'))
                return
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            noidung = params.get('noidung', [''])[0]
            if noidung:
                HISTORY_LOG.append({
                    "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "noidung": noidung
                })
            self.wfile.write(b'TRUE')
            return

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status": "ok"}')

    def do_GET(self):
        parsed = urlparse(self.path)

        # Bandwidth: live uplink data (SNMP) or mock fallback
        if parsed.path == '/api/bandwidth/uplinks':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            if BW_POLLER is not None:
                snap = BW_POLLER.snapshot()
                if snap["links"]:
                    self.wfile.write(json.dumps(snap).encode('utf-8'))
                    return
            res = {"mode": "mock", "updated": time.strftime("%Y-%m-%d %H:%M:%S"),
                   "links": _mock_bandwidth_links(), "errors": {}}
            self.wfile.write(json.dumps(res).encode('utf-8'))
            return

        # Bandwidth: discover interfaces via SNMP walk (find uplink ifindex)
        elif parsed.path == '/api/bandwidth/discover':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            query = parse_qs(parsed.query)
            ip = query.get('ip', [''])[0]
            community = query.get('community', [SNMP_CONFIG.get('community', 'public')])[0]
            if not _SNMP_OK or not ip:
                self.wfile.write(json.dumps(
                    {"ok": False, "error": "SNMP unavailable or missing ip"}).encode('utf-8'))
                return
            try:
                rows = snmp_poller.snmp_walk(ip, community, snmp_poller.IF_DESCR,
                                             timeout=SNMP_CONFIG.get('timeout', 4),
                                             port=SNMP_CONFIG.get('port', 161))
                ifs = [{"ifindex": int(r[0].split('.')[-1]), "descr": r[1]} for r in rows]
                self.wfile.write(json.dumps(
                    {"ok": True, "ip": ip, "interfaces": ifs}).encode('utf-8'))
            except Exception as e:
                self.wfile.write(json.dumps(
                    {"ok": False, "error": str(e)[:200]}).encode('utf-8'))
            return

        # PRTG API: Get list of sensors
        elif parsed.path == '/api/prtg/sensors':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(PRTG_SENSORS).encode('utf-8'))
            return

        # PRTG API: Telemetry data for a specific sensor (Live Data vs 2-days)
        elif parsed.path == '/api/prtg/sensor_traffic':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()

            query = parse_qs(parsed.query)
            sensor_id = query.get('id', ['285279233'])[0]
            time_range = query.get('range', ['live'])[0]
            sensor = next((s for s in PRTG_SENSORS if s['id'] == sensor_id), PRTG_SENSORS[0])
            scale = sensor.get('scale', 1.0)

            timeline = []
            traffic_in = []
            traffic_out = []
            traffic_total = []
            downtime_flags = []
            table_rows = []

            now = time.time()

            # Mode 1: Live Data (Matches image 5 & 6: 285279233 xgei-1/4/1)
            if time_range == 'live' or sensor['id'] == '285279233':
                # Generate ~35 points for the last 2 hours (every 1 min)
                for i in range(35, -1, -1):
                    t = now - (i * 60)
                    time_label = time.strftime("%I:%M %p", time.localtime(t))
                    date_time_full = time.strftime("%m/%d/%Y %I:%M:%S %p", time.localtime(t))
                    timeline.append(time_label)

                    # Simulating downtime before 9:25 PM as seen in screenshot
                    is_down = 1 if i > 12 else 0
                    downtime_flags.append(is_down * 100)

                    if is_down:
                        k_in = 0
                        k_out = 0
                        k_tot = 0
                    else:
                        # Recent active traffic (spike to 81k, avg around 63k-70k)
                        k_in = int(random.uniform(40_000, 75_000))
                        k_out = int(random.uniform(8_000, 15_000))
                        k_tot = k_in + k_out

                    traffic_in.append(k_in)
                    traffic_out.append(k_out)
                    traffic_total.append(k_tot)

                    # Table records
                    vol_tot = int(k_tot * 60 / 8)  # KByte
                    vol_in = int(k_in * 60 / 8)
                    table_rows.append({
                        "datetime": date_time_full,
                        "tot_vol": f"{vol_tot:,} KByte",
                        "tot_speed": f"{k_tot:,} kbit/s",
                        "in_vol": f"{vol_in:,} KByte",
                        "in_speed": f"{k_in:,} kbit/s"
                    })

                # Reverse table so latest is on top
                table_rows.reverse()

            else:
                # Mode 2: 2-day historical curve (Matches images 1, 2, 3)
                for i in range(120, -1, -1):
                    t = now - (i * 1200)
                    hour = time.localtime(t).tm_hour
                    time_label = time.strftime("%m/%d %I:%M %p", time.localtime(t))
                    timeline.append(time_label)
                    downtime_flags.append(0)

                    peak = 1.9 if 18 <= hour <= 22 else (0.2 if 2 <= hour <= 6 else 0.8)
                    k_tot = int((math.sin(i / 10) * 800_000 + 1_500_000 + random.uniform(-100_000, 150_000)) * peak * (scale / 4.0))
                    k_tot = max(200_000, k_tot)

                    k_in = int(k_tot * 0.9)
                    k_out = int(k_tot * 0.1)

                    traffic_in.append(k_in)
                    traffic_out.append(k_out)
                    traffic_total.append(k_tot)

            res = {
                "sensor": sensor,
                "timeline": timeline,
                "traffic_total": traffic_total,
                "traffic_in": traffic_in,
                "traffic_out": traffic_out,
                "downtime": downtime_flags,
                "max_kbits": max(traffic_total) if traffic_total else sensor['max_kbits'],
                "min_kbits": min(filter(lambda x: x > 0, traffic_total), default=sensor['min_kbits']),
                "table_rows": table_rows[:33]
            }
            self.wfile.write(json.dumps(res).encode('utf-8'))
            return

        # PRTG API: Device Overview (Image 4)
        elif parsed.path == '/api/prtg/device':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            device_data = {
                "name": "Device BIH.OLT.019 (Long Bình Tân)",
                "dns_ip": "172.20.160.21",
                "status": "OK",
                "sensors_down": 2,
                "sensors_total": 2,
                "dependency": "Parent",
                "interval": "every 60 seconds",
                "sensors": [
                    {
                        "pos": "1.",
                        "name": "Ping",
                        "status": "Down",
                        "message": "Destination host unreachable (ICMP error # 11003)",
                        "priority": "★★★☆☆"
                    },
                    {
                        "pos": "2.",
                        "name": "(900001) XE0/1 XE0/1Traffic 10 GBit/s",
                        "status": "Down",
                        "message": "No response (check: firewalls, routing, snmp settings of device, IPs, SNMP version, community, passwords etc) (SNMP error # -2003)",
                        "priority": "★★★☆☆"
                    }
                ]
            }
            self.wfile.write(json.dumps(device_data).encode('utf-8'))
            return

        # Legacy APIs
        elif parsed.path == '/api/traffic':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            now = time.time()
            timeline = [time.strftime("%H:%M", time.localtime(now - i * 300)) for i in range(288, -1, -1)]
            inbound = [int(abs(math.sin(i / 12) * 50 + 75) * 1_000_000) for i in range(289)]
            outbound = [int(abs(math.cos(i / 15) * 550 + 800) * 1_000_000) for i in range(289)]
            self.wfile.write(json.dumps({
                "interface": "DNI-N3KPon01 - Traffic - Ethernet1/31",
                "timeline": timeline,
                "inbound": inbound,
                "outbound": outbound,
                "stats": {"in_curr": 14_490_000, "in_avg": 80_000_000, "in_max": 228_270_000, "out_curr": 101_340_000, "out_avg": 922_000_000, "out_max": 1_960_000_000}
            }).encode('utf-8'))
            return

        if self.path in ('/', ''):
            self.path = '/index.html'

        return super().do_GET()


class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("=" * 65)
    print(f"[*] NOC & PRTG 10G Full Portal Running on Port {PORT}")
    print(f"[*] Local:   http://localhost:{PORT}")
    print(f"[*] LAN:     http://192.168.100.71:{PORT}")
    print(f"[*] WAN:     http://116.104.90.25:{PORT}")
    print("=" * 65)

    if _SNMP_OK and SNMP_CONFIG.get("enabled") and SNMP_CONFIG.get("devices"):
        BW_POLLER = snmp_poller.BandwidthPoller(
            devices=SNMP_CONFIG["devices"],
            community=SNMP_CONFIG.get("community", "public"),
            interval=SNMP_CONFIG.get("poll_interval", 60),
            timeout=SNMP_CONFIG.get("timeout", 4),
            port=SNMP_CONFIG.get("port", 161))
        BW_POLLER.start()
        print(f"[*] SNMP bandwidth poller started ({len(SNMP_CONFIG['devices'])} devices)")
    else:
        print("[*] SNMP bandwidth poller disabled -> mock mode")

    try:
        with ThreadingHTTPServer((HOST, PORT), NOCUnifiedHandler) as server:
            server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Server shutdown.")
        sys.exit(0)
