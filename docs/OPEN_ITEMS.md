# A1未决事项

| ID | 项目 | 待确认 | 关闭条件 |
|---|---|---|---|
| OI-001 | RK3568 | 完整订货型号、价格、交期、渠道 | 可追溯报价 |
| OI-002 | LPDDR4X | MT53E512M32D1ZW-046B WT:B的Rockchip AVL条目、D200P132模板、匹配DDR BIN及WDQS要求 | Rockchip/FAE确认完整颗粒/模板/BIN组合 |
| OI-003 | eMMC | 32GB完整料号、HS200能力、供货 | 数据手册/采购确认 |
| OI-004 | RK809-5 | 供货、QFN68 land pattern、EVB rail mapping、BUCK3 divider | PMIC输出与SoC电源树逐项核对，封装经板厂确认 |
| OI-005 | VDD_CPU | TCS4525及电感/反馈网络 | 原厂电源树核验 |
| OI-006 | USB-C PD | HUSB238 15V/3A PDO与PD适配器兼容性 | 实测15V/3A协商及输入保护验证 |
| OI-007 | Wi-Fi/BT | AP6256正式料号/47Pad机械封装、37.4MHz/32k时钟、1.8V SDIO、UART流控、天线与固件 | 模组原厂资料、装配与Linux接口联调 |
| OI-008 | Ethernet | RTL8211F-CG复用/时钟/PHY延时及MagJack缺失精确封装 | PHY/RJ45厂商图核验和链路测试 |
| OI-009 | USB3 | Host/DRD PHY资源分配 | Multi-PHY/PinMux复核 |
| OI-010 | GPIO | 40-pin与SoC PinMux协调 | PinMux表通过 |
| OI-011 | PCB | 6层板厂叠层和阻抗 | 板厂阻抗计算书 |
| OI-012 | 机械 | 85×56mm板框、接口高度、天线和散热 | 3D装配无干涉 |
| OI-013 | Linux | DDR BIN、U-Boot、Kernel、Wi-Fi固件 | eMMC启动及外设实测 |

| OI-014 | microSD socket | TFP09-2-12B LCSC C2911421 stock and JLC extended C2887880 availability; supplier land pattern orientation | Confirm orderable stock and compare 15-pad footprint to current supplier drawing |
| OI-015 | SDMMC0 UHS-I | RK809 LDO5 VCCIO_SD 3.3V↔1.8V switching, device-tree supplies and timing | Confirm PMIC register/driver configuration and test SD 3.0/SDR104 negotiation |
| OI-016 | ESD5341N | LCSC C3021106 current stock and DFN1006-2 land pattern | Confirm stock, package drawing and assembly capability |

| OI-017 | HDMI | 5V经Schottky可能低于4.8V；RK809 Image LDO1/9使能 | 满载电压测量与ERC通过 |
| OI-018 | GPIO | 40Pin外部5V反灌/ESD、3.3V银行及Linux pinctrl | 安全审查与系统测试 |
| OI-019 | KiCad | GitHub Actions ERC已提交，实际运行与阻断错误待处理 | 原生ERC报告和网表通过审查 |
| OI-020 | 生产测试 | 第17页TP1701/TP1702已加入；核对Pogo治具针位、1.27mm焊盘对位、测试电压和流程 | 治具图纸、限压规范和首板测试流程验证通过 |
