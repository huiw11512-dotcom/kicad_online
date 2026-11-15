# Linux SBC A1 — 一次性原理图冻结基线 Rev 1.0

**目的：** 将A1首版原理图的产品范围、接口数量、器件架构和各页交付范围一次性固定，避免每轮只推进一个小模块。此文件是设计输入冻结，不等同于已完成的电气原理图或投板批准。

## 1. 产品定义

- 独立RK3568 ARM64 Linux SBC，整板SoC+DRAM+PMIC+存储+接口，不采用CM5/SoM。
- 目标是树莓派4B级别的使用场景和接口便利性，不宣称CPU性能等同Cortex-A72。
- 首版以“能稳定启动Linux、网络/USB/HDMI可用、可扩展GPIO”为成功标准。
- 85×56mm为目标外形，不为追求外形尺寸牺牲DDR布线、BGA扇出、散热和连接器可制造性。

## 2. 首版功能范围（冻结）

| 功能 | A1 Rev1决策 |
|---|---|
| SoC | RK3568 FCBGA636L |
| RAM | 4GB LPDDR4X，32-bit；颗粒必须与Rockchip模板/BIN匹配后冻结 |
| 系统盘 | 32GB eMMC 5.1，8-bit |
| 扩展存储 | 1×MicroSD，4-bit |
| 显示 | 1×HDMI 2.0a |
| 有线网络 | 1×Gigabit Ethernet，RGMII PHY + MagJack |
| USB | 1×USB3.x Type-A Host1 + 2×USB2.0 Type-A Host2/3 + 1×Micro-USB USB3_OTG0 service/download |
| 无线 | 1个焊接式Wi-Fi/BT模块，SDIO + UART；模块型号待接口/供货核验 |
| GPIO | 40-pin 2.54mm排针；只引出已确认的3.3V GPIO/I2C/SPI/UART/PWM，保留5V/GND |
| 调试 | 1×3-pin 3.3V UART，1×MaskROM/Recovery按键 |
| 电源输入 | USB-C PD，目标15V/3A（45W）；PD协商失败时不启动满载模式 |
| PCB | 6层FR-4，1.6mm初始目标，板厂阻抗计算后冻结 |
| 不做 | M.2/NVMe、SATA、PCIe插槽、音频Codec、摄像头接口、LCD/DSI、第二网口、PoE |

## 3. 电源总体架构（电气冻结前的拓扑）

1. USB-C PD Sink接收15V/3A合同；输入保护、反灌/过流保护后形成15V_IN。
2. 15V_IN经主Buck形成5V_SYS（设计目标6A等级，实际按36W输入预算降额）。
3. RK809-5仅由5V_SYS供电；绝不将12V直接接入RK809-5。
4. VDD_CPU使用独立动态调压Buck，能力不低于Rockchip要求；TCS4525仅作为候选，必须完成数据手册与EVB电路核对。
5. RK809-5的BUCK/LDO/SW输出按RK3568 EVB V1.2完整电源图逐网映射，不得根据简化框图猜接。
6. LPDDR4X的SoC DDR PHY供电与DRAM VDD1/VDD2/VDDQ分开列网；按最终颗粒数据手册和匹配模板设计。
7. HDMI/USB3/Multi-PHY/GMAC模拟电源按Rockchip指南低噪声方案供电。
8. 所有外设VBUS由独立限流开关控制；USB端口供电能力受总输入功率约束。

## 4. 原理图分页——一次性交付清单

| Sheet | 页名 | 必须完整包含 |
|---|---|---|
| 01 | USB-C_PD_INPUT | Type-C receptacle、CC/PD sink、12V输入保护、保险/电子保险、输入电容、VBUS/CC ESD、PD状态/故障指示 |
| 02 | MAIN_POWER | 15V→5V主Buck、5V_SYS电源树、输入/输出电容、反馈、软启动、PG、使能、测试点、热/电流预算 |
| 03 | RK809_PMIC | RK809-5完整引脚、全部Buck/LDO/SW外围、VCCx输入分配、I2C、INT、PWRON、RESETB、32k晶体、RTC、电池/未用引脚处理 |
| 04 | CPU_GPU_LOGIC_POWER | CPU动态Buck、GPU/Logic/NPU所需电源、FB远端采样、补偿/电感/电容、PG/EN、SoC电源轨网络 |
| 05 | RK3568_SOC | 636-ball SoC、全部电源/地球、24MHz、32.768kHz（如需）、Reset、Boot straps、UART调试、I2C、JTAG/测试点 |
| 06 | LPDDR4X_4GB | 颗粒、完整DQ/CA/CK/DQS映射、ZQ、RESET、ODT、全部DRAM电源与去耦；严格复制匹配Rockchip DDR模板的拓扑约束，不复制其他整板 |
| 07 | EMMC_MICROSD | eMMC 8-bit、RST、CLK、CMD、DATA、STROBE、VCC/VCCQ、MicroSD 4-bit、卡座检测、ESD |
| 08 | GIGABIT_ETHERNET | RGMII、PHY strap、25MHz时钟、MDC/MDIO、RESET、RSET、磁性器件/RJ45、LED、ESD |
| 09 | USB3_USB2 | USB3_HOST1、USB2_HOST2/3及USB3_OTG0 Micro-USB下载口、差分线、Type-A连接器、VBUS限流开关、OC/EN、ESD、USB2端口 |
| 10 | HDMI | HDMI TX差分对、DDC、HPD、CEC、+5V source、ESD、共模/滤波按原厂方案 |
| 11 | WIFI_BT_GPIO | SDIO、UART、模块电源、天线净空/连接器、40-pin排针、按键、风扇接口、状态LED |
| 12 | TEST_RECOVERY | MaskROM/Recovery、启动模式选择、UART、JTAG测试点、关键电源测试点、生产测试焊盘 |

## 5. 必须先关闭的三个硬门槛

### Gate A — RK3568封装与球位
- 使用Rockchip官方RK3568 Datasheet/PinOut版本。
- 636个Ball编号、坐标、A1方向、所有电源/地脚必须逐项导入并校验。
- BGA land pattern使用Rockchip封装图/官方参考PCB数据；不以自行猜测的0.30mm焊盘直接投板。

### Gate B — LPDDR4X
- 最终颗粒必须同时满足：可采购、完整数据手册、32-bit组织与模板匹配、Rockchip AVL/应用说明可接受、对应DDR BIN存在。
- 若单颗32Gb x32候选无法闭环，直接改用Rockchip模板明确支持的双颗x16方案；不为坚持某个料号强行改模板。
- 在Gate B关闭前，Sheet 06不得宣称电气冻结。

### Gate C — RK809-5与电源时序
- 逐引脚参考RK3568 EVB完整电源原理图，而非只抄Power Tree框图。
- 确认VCC1–VCC9、VCC_RTC、各LDO输入脚、BUCK5、SW1/SW2、外部Buck及全部PG/EN网络。
- RK809-5固化上电顺序必须保持。
- 15V输入只进入外部主Buck，PMIC由合规5V供电。

## 6. 全部页的统一交付标准

每页必须同时交付：
1. KiCad原生可编辑原理图页；
2. 完整器件型号/封装/可采购料号或明确标记候选；
3. 每个IC逐引脚连接，不允许“按参考设计连接”代替实际网络；
4. 电阻、电容、电感数值与耐压/精度/封装；
5. 连接器Pin 1方向和每脚定义；
6. 电源域、IO电压域、上电时序和测试点；
7. 对应datasheet/reference schematic来源；
8. ERC结果与未关闭问题清单。

整套原理图完成后统一执行一次全局ERC、未连接引脚检查、网络表导出、BOM汇总和跨页电源审查。不得再用“下次继续补某一页”的方式将未完成设计说成已完成。

## 7. 项目交付状态

当前仓库仅有KiCad工程壳和设计文档；尚无完整电气原理图。上述12页是一次性完整交付目标。由于Gate A/B/C尚未关闭，不应伪造连接或将候选器件当成已验证器件。
