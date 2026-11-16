# Linux SBC A1 — 一次性原理图冻结基线 Rev1.0

**日期：** 2026-11-16  
**状态：** 首板设计输入冻结；KiCad 原理图部分完成；未达到投板条件。

本文件用于固定首板产品范围、器件架构和接口资源，避免每轮只推进一个小模块。修改容量、封装、接口或 pinmux 时，必须同步更新主基线、KiCad 原理图和 BOM。

## 1. 产品定义

- 独立 RK3568 ARM64 Linux SBC，整板 SoC + DRAM + PMIC + 存储 + 接口，不采用 CM5/SoM。
- 目标是树莓派 4B 级别的使用场景和接口便利性，不宣称 CPU 性能等同 Cortex-A72。
- 首板成功标准：稳定启动 Linux，eMMC、网络、USB、HDMI 可用，并具备可扩展 GPIO。
- 85×56mm 为机械目标，不得为追求尺寸牺牲 DDR 布线、BGA 扇出、散热和连接器可制造性。

## 2. 首板功能范围

| 功能 | A1 Rev1 决策 | 当前状态 |
|---|---|---|
| SoC | RK3568 FCBGA636L | 17 单元 / 636 球位已建图，封装仍需原厂核验 |
| RAM | 2GB LPDDR4X x32，Micron MT53E512M32D1ZW-046B WT:B，单 Die / 单 Rank | 已进原理图；AVL、模板/BIN 和 DDR 训练未闭环 |
| 4GB RAM | MT53E1G32D2FW-046 WT:C 作为后续独立版本候选 | 不进入首板 BOM；须单独核对 D2/FW 双 Die 拓扑 |
| 系统盘 | 32GB eMMC 5.1，8-bit | Samsung KLMBG2JETD-B041 候选已进原理图 |
| 扩展存储 | 1×MicroSD，SDMMC0 4-bit | 原理图页已建立，电压切换/DTS 待验证 |
| 显示 | 1×HDMI 2.0a | 已新增第13页设计草案；电气/供电/ERC待验证 |
| 有线网络 | 1×Gigabit Ethernet，RGMII PHY + MagJack | 已新增第14页设计草案；MagJack精确封装缺失 |
| USB Host | 1×USB3 HOST1 Type-A + 2×USB2 HOST2/HOST3 Type-A | USB3 HOST1/OTG0 页已建立；USB2 HOST2/HOST3 独立页已建立，ERC/网表待验证 |
| 下载/恢复 | USB3_OTG0 DP/DM → USB-C 服务接口，USB2 Device / MaskROM / Loader | 原理图已建立，需核对 VBUSDET、角色切换和下载验证 |
| 无线 | 1 个焊接式 Wi-Fi/BT Combo 模块，SDIO + UART | 已新增第15页AP6256候选；SDMMC2+UART4已分配，模块仍待验证 |
| GPIO | 40-pin 2.54mm 排针 | 已新增第16页，28路3.3V信号加供电/地，pinmux与保护仍待验证 |
| 调试 | 3-pin 3.3V UART + Recovery/MaskROM | UART2、Recovery 已建立；生产测试点待补 |
| 电源输入 | USB-C PD 15V/3A（45W） | 原理图原型已建立，保护与 PDO 实测待完成 |
| PCB | 六层 FR-4，1.6mm 初始目标 | 叠层/阻抗需板厂确认 |

首板只采用 2GB 单 Die / 单 Rank。4GB 方案不与首板共用未经验证的 DDR 配置。

## 3. 电源总体架构

1. USB-C PD Sink 请求 15V/3A；输入保护、反灌/过流保护后形成 15V_IN。
2. 15V_IN 经 LM76005 主 Buck 形成 5V_SYS，设计目标 5A；25W 是 5V 输出端的名义功率上限，不是 45W PD 合同功率。
3. 5V_SYS 经 TPS62132 形成 VCC3V3_SYS，供 RK809-5 VCC1–VCC9 / VCC_RTC。
4. RK809-5 各 BUCK/LDO/SW 输出按 RK3568 EVB 完整电源图逐网核对，不得只按简化 Power Tree 猜接。
5. VDD_CPU 使用独立动态 Buck；TCS4525_WT 为候选，需核对远端反馈、EN 时序和负载能力。
6. LPDDR4X：DRAM VDD1=1.8V、VDD2=1.1V、VDDQ=0.6V；RK3568 DDRPHY_VDDQ=1.1V、DDRPHY_VDDQL=0.6V。
7. DRAM ZQ0 使用 R40=240Ω±1% 接 VCC0V6_DDR；RK3568 DDR_RZQ（H7）使用 R41=120Ω±1% 接 VCC_DDR_1V1。
8. HDMI、USB3/Multi-PHY、GMAC 模拟电源按 Rockchip 指南采用独立滤波和就近去耦。
9. 所有 USB Host VBUS 使用独立限流开关；总负载受 5V_SYS 功率预算约束。

## 4. 原理图分页和交付范围

| 页面 | 文件/模块 | 必须完成的内容 |
|---|---|---|
| 01 | 根页 / USB-C PD / MAIN_POWER | Type-C、HUSB238、输入保护、15V→5V Buck、软启动、PG、测试点、电流/热预算 |
| 02 | RK809_PMIC | 全部引脚、BUCK/LDO/SW、VCC 输入分配、I2C、INT、PWRON、RESETB、RTC、未用引脚 |
| 03 | DDR_POWER | 1.1V、0.6V、1.8V 轨，反馈、使能、去耦、时序 |
| 04 | 3V3_POWER | 5V_SYS→3.3V 预 PMIC Buck |
| 05 | CPU_POWER | CPU 动态 Buck、远端反馈、EN/VSEL/I2C、补偿和负载验证 |
| 06 | RK3568_SOC | 636 球位、电源/地、时钟、Reset、Boot、UART、I2C、DDR_RZQ |
| 07 | LPDDR4X_2GB | Micron 颗粒、67 条信号、200-ball map、R40/R41、完整电源和去耦 |
| 08 | EMMC_MICROSD | eMMC 8-bit、MicroSD 4-bit、RST/CLK/CMD/DATA/STROBE、VCC/VCCQ、ESD |
| 09 | USB3_USB2 | USB3 HOST1、USB2 HOST2/3、OTG0 下载口、VBUS 限流、OC/EN、ESD |
| 10 | HDMI | HDMI TX、DDC、HPD、CEC、+5V、ESD |
| 11 | GIGABIT_ETHERNET | RGMII、PHY Strap、25MHz、MDC/MDIO、磁性器件、RJ45、ESD |
| 12 | WIFI_BT_GPIO | Combo 模块、SDIO、UART、天线净空、40-pin GPIO、按键和 LED |
| 13 | TEST_RECOVERY | UART、MaskROM/Recovery、JTAG 测试点、电源测试点、生产测试焊盘 |

当前根页及15张子页已存在。HDMI、Ethernet、Wi-Fi/BT、GPIO均已有原生可编辑设计草案；完整ERC、器件签核和生产测试页仍未完成，绝不可投板。

## 5. 必须先关闭的硬门槛

### Gate A — RK3568 封装与球位

- 使用 Rockchip 官方 RK3568 Datasheet / PinOut。
- 636 个 Ball 编号、坐标、A1 方向、电源/地脚逐项校验。
- BGA land pattern 依据原厂封装图和装配厂建议，不以自行猜测的焊盘尺寸投板。

### Gate B — LPDDR4X

- 首板 MPN：MT53E512M32D1ZW-046B WT:B，2GB、x32、单 Die / 单 Rank。
- 公开 Rockchip DDR AVL v3.01 转录中该 MPN 在 RK3568 栏为 T/A；须以当前官方 AVL 核对。
- Rockchip Hardware Design Guide Rev1.2 使用 SD6 模板名；当前 rkbin 配置表列出 SD4 模板名。必须由 Rockchip/FAE 确认实际适用模板、版本和完整文件。
- 取得匹配 DDR 初始化 BIN、频率、WDQS 要求和 Bootloader 集成说明。
- 按确认模板完成 Byte Lane、DQS、CA、CK、CS、RESET、ODT、ZQ 的连接与布线约束。
- 在 Gate B 关闭前，不得将 DDR 页标记为电气冻结。

### Gate C — RK809-5 与电源时序

- 逐引脚参考 RK3568 EVB 完整电源原理图。
- 确认 VCC1–VCC9、VCC_RTC、BUCK、LDO、SWOUT、外部 CPU Buck、PG/EN 网络。
- 核对 1.1V / 0.6V / 1.8V DDR 电源轨、上电顺序、峰值电流、纹波和热设计。
- RK809 固定上电顺序必须保持；15V 输入不得直接进入 PMIC。

## 6. 统一交付标准

每页必须同时具备：

1. KiCad 原生可编辑原理图；
2. 完整器件型号、封装、可采购料号或明确标注候选；
3. 每个 IC 逐引脚连接；
4. 电阻、电容、电感数值及耐压/精度/封装；
5. 连接器 Pin 1 方向和每脚定义；
6. 电源域、IO 电压域、上电时序和测试点；
7. 对应 Datasheet / Reference Design 来源；
8. ERC 结果和未关闭问题清单。

整套原理图完成后统一执行全局 ERC、未连接引脚检查、网络表导出、BOM 汇总和跨页电源审查。不得将预留网络或部分原理图称为完整设计。

## 7. 当前交付状态

- 已有：RK3568 主控球位图、RK809-5、主电源、3.3V、CPU Buck、2GB LPDDR4X、eMMC、MicroSD、启动/调试、部分 USB。
- 已修正：SoC DDR_RZQ H7 的 R41=120Ω±1% 接 VCC_DDR_1V1；DRAM ZQ0 的 R40=240Ω±1% 接 VCC0V6_DDR。
- 未完成：DDR 模板/BIN 确认、HDMI/以太网/无线/GPIO电气签核、MagJack封装、生产测试、完整电源审查。
- GitHub Actions原生KiCad ERC/网表导出流程已提交，结果必须结合实际运行日志确认；PCB DRC、DDR Training、Linux 启动验证均未完成。

**当前工程为 DESIGN-IN-PROGRESS，禁止投板。**
