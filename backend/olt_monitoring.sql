-- Bảng danh sách thiết bị OLT
CREATE TABLE IF NOT EXISTS `tbl_olt_devices` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `olt_code` VARCHAR(50) NOT NULL UNIQUE,       -- BIH.OLT.01, BIH.OLT.27
    `olt_name` VARCHAR(100) NOT NULL,
    `ip_address` VARCHAR(45) NOT NULL,            -- 172.20.160.27
    `snmp_community` VARCHAR(50) DEFAULT 'public',
    `snmp_version` VARCHAR(10) DEFAULT '2c',
    `hardware_model` VARCHAR(100) DEFAULT 'ZXA10 C620',
    `firmware_version` VARCHAR(50) DEFAULT 'V2.0.10',
    `uptime_ticks` BIGINT DEFAULT 0,
    `location` VARCHAR(255),
    `status` ENUM('online', 'offline', 'warning') DEFAULT 'online',
    `last_poll` DATETIME,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Bảng lưu cổng giao tiếp Uplink / PON
CREATE TABLE IF NOT EXISTS `tbl_olt_interfaces` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `olt_id` INT NOT NULL,
    `if_index` INT NOT NULL,
    `if_name` VARCHAR(50) NOT NULL,              -- Ethernet1/31, xgei-1/4/1
    `if_speed_bps` BIGINT DEFAULT 10000000000,    -- 10G Uplink
    `in_octets_prev` BIGINT DEFAULT 0,
    `out_octets_prev` BIGINT DEFAULT 0,
    `current_in_bps` BIGINT DEFAULT 0,
    `current_out_bps` BIGINT DEFAULT 0,
    `load_percent` DECIMAL(5,2) DEFAULT 0.00,
    `last_poll` DATETIME,
    FOREIGN KEY (`olt_id`) REFERENCES `tbl_olt_devices`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Bảng định nghĩa liên kết Topology Weathermap
CREATE TABLE IF NOT EXISTS `tbl_weathermap_links` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `link_name` VARCHAR(100) NOT NULL,
    `source_node` VARCHAR(50) NOT NULL,          -- SWcore
    `target_node` VARCHAR(50) NOT NULL,          -- BIH.OLT.01
    `olt_interface_id` INT,
    `capacity_bps` BIGINT DEFAULT 10000000000,   -- 10 Gbps
    FOREIGN KEY (`olt_interface_id`) REFERENCES `tbl_olt_interfaces`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
