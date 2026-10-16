# VTVcab GPON Monitor & PRTG 10G Uplink Telemetry Portal

Hệ thống giám sát vận hành mạng cáp quang GPON, thiết bị OLT và đo kiểm lưu lượng băng thông Uplink 10G (PRTG Network Monitor) được port hoàn chỉnh từ hệ thống VTVcab NOC.

---

## 🌐 Địa chỉ truy cập hệ thống

Mở trình duyệt web và truy cập theo các địa chỉ tương ứng:

* **Máy cục bộ (Local)**: [http://localhost:8765](http://localhost:8765)
* **Mạng nội bộ (LAN)**: [http://192.168.100.71:8765](http://192.168.100.71:8765)
* **Truy cập từ xa qua WAN**: [http://116.104.90.25:8765](http://116.104.90.25:8765) *(yêu cầu NAT port 8765 trên Router)*

---

## 📁 Cấu trúc thư mục dự án (`GponMonitorSystem`)

```
GponMonitorSystem/
│
├── index.html                  # Giao diện người dùng hợp nhất (PRTG 10G, Công cụ OLT, Công cụ ONU, Weathermap)
├── server.py                   # Máy chủ HTTP backend độc lập chạy port 8765
├── run_server.bat              # Phím tắt khởi động nhanh trên Windows (click đúp để chạy)
├── README.md                   # Tài liệu hướng dẫn sử dụng & cấu hình
│
├── backend/
│   ├── olt_monitoring.sql      # Cấu trúc cơ sở dữ liệu MySQL/MariaDB
│   └── api_olt_monitor.php     # API PHP cho môi trường Apache/Nginx
│
├── tools/
│   └── web_reconstructor.py    # Công cụ trích xuất và giải nén Source Map tự động
│
└── raw_sources/                # Mã nguồn gốc đã trích xuất từ server VTVcab
    ├── vtvcab_index.html       # Khung HTML gốc
    ├── vtvcab_app.js           # Bộ điều hướng CoreUI SPA gốc
    ├── vtvcab_quanlyonu.php    # Giao diện gốc views/quanlyonu.php
    ├── vtvcab_quanlyonu.js     # Script gốc js/views/quanlyonu.js
    ├── views_congcuolt.php     # Màn hình đăng nhập/redirect
    ├── views_quanlyolt.php     # Giao diện gốc views/quanlyolt.php
    └── js_views_quanlyolt.js   # Script gốc js/views/quanlyolt.js
```

---

## 🚀 Cách khởi động máy chủ

### Cách 1: Click đúp vào file
Click đúp chuột vào file **`run_server.bat`**.

### Cách 2: Chạy lệnh trong Terminal / PowerShell
```powershell
cd c:\Users\ByActive\Desktop\Jb\GponMonitorSystem
python server.py
```

---

## 🌟 Các phân hệ chính trong hệ thống

1. **Tab Băng thông Uplink 10G (PRTG Monitor)**:
   - Tích hợp telemetry cảm biến 10 GBit/s từ PRTG Paessler:
     - `(285279233) xgei-1/4/1 Traffic 10 GBit/s` - `BIH.OLT.27 (Hóa An)`: Chế độ Live Data, đồ thị tốc độ và bảng thống kê dung lượng chi tiết.
     - `(900003) XE0/3 Link1 connect nx3000 (10 GBit/s)` - `BIH.OLT.05 (Long Thành)`: Đỉnh 4.48 Gbps.
     - `(900004) XE0/4 Link2 connect nx3000 (10 GBit/s)` - `BIH.OLT.05 (Long Thành)`: Đỉnh 4.31 Gbps.
     - `(900002) XE0/2 [Downlink][Xe0/1][BIH.OLT.19] (10 GBit/s)`: Đỉnh 1.07 Gbps.
     - `Device BIH.OLT.019 (Long Bình Tân)`: Bảng quản lý 2 cảm biến Down (Ping & XE0/1).
   - Đồ thị phối màu trực quan: Total (Cyan fill), In (Blue), Out (Pink), Downtime (Red dotted).

2. **Tab Công cụ OLT (`views/quanlyolt.php`)**:
   - Tra cứu OLT theo Tỉnh/Thành (`Đồng Nai`...) và Mã OLT (`BIH.OLT.01` đến `BIH.OLT.06`).
   - Thống kê chi tiết từng Port PON: số lượng ONU hoạt động, không hoạt động, tổng thuê bao.
   - Nút thao tác nhanh `DS ONU` và `Show Port` (đo kiểm module quang SFP).

3. **Tab Công cụ ONU (`views/quanlyonu.php`)**:
   - Tra cứu ONU theo Serial, địa chỉ, OLT.
   - Bộ lọc cảnh báo suy hao quang (`Rx < -26 dBm`) và trạng thái Active.
   - Bảng DataTables 22 cột đầy đủ thông tin kỹ thuật, PPPoE và chẩn đoán Telnet/CLI trực tiếp.

4. **Tab Weathermap & Admin RRDtool**:
   - Bản đồ liên kết mạng từ Switch Core (`SWcore`) tới các trạm OLT vệ tinh.
   - Đồ thị chu kỳ lưu lượng 24h đo bằng RRDtool.
