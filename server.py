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

def generate_olt_ports(maolt):
    ports = []
    for slot in range(1, 3):
        for port in range(1, 9):
            act = random.randint(35, 62)
            inact = random.randint(1, 7)
            ports.append({
                "PORTPON": f"1/{slot}/{port}",
                "ACTONU": act,
                "INACTONU": inact,
                "TOTALONU": act + inact,
                "TYPE_OLT": "ZTE",
                "MODELS": "ZXA10 C620"
            })
    return ports

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

        # 2. API: loaddata_olt.php
        elif 'loaddata_olt.php' in parsed.path:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            maolt = params.get('maolt', ['BIH.OLT.01'])[0]
            ports = generate_olt_ports(maolt)
            res = {"draw": 1, "recordsTotal": len(ports), "recordsFiltered": len(ports), "data": ports}
            self.wfile.write(json.dumps(res).encode('utf-8'))
            return

        # 3. API: loaddata_onu.php
        elif 'loaddata_onu.php' in parsed.path:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            maonu_filter = params.get('maonu', [''])[0].strip().upper()
            filtered = [onu for onu in MOCK_ONUS if not maonu_filter or maonu_filter == 'ALL' or maonu_filter in onu['SNONU'].upper()]
            res = {"draw": 1, "recordsTotal": len(MOCK_ONUS), "recordsFiltered": len(filtered), "data": filtered}
            self.wfile.write(json.dumps(res).encode('utf-8'))
            return

        # 4. API: getTelnet.php
        elif 'getTelnet.php' in parsed.path:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            olt_ip = params.get('oltIP', ['172.19.117.34'])[0]
            portpon = params.get('portpon', ['1/1/1'])[0]
            res_html = f"""
<pre style="background: #000; color: #f8cb00; padding: 12px; border-radius: 4px; font-family: Consolas, monospace; font-size: 13px; line-height: 1.4;">
[PORT STATUS: {olt_ip}] - Port: gpon_olt-{portpon} (SFP 10G Uplink)
---------------------------------------------------------------------
Port State              : Up / Enabled
SFP Module Model        : GPON-OLT-CLASS-C+ (10G SFP+)
TX Optical Power        : +5.32 dBm
Supply Voltage          : 3.32 V
Temperature             : 46.2 C
Active ONUs             : 48 ONUs
---------------------------------------------------------------------
</pre>"""
            self.wfile.write(res_html.encode('utf-8'))
            return

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status": "ok"}')

    def do_GET(self):
        parsed = urlparse(self.path)

        # PRTG API: Get list of sensors
        if parsed.path == '/api/prtg/sensors':
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

    try:
        with ThreadingHTTPServer((HOST, PORT), NOCUnifiedHandler) as server:
            server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Server shutdown.")
        sys.exit(0)
