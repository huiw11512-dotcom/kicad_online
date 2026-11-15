# A1电源架构 Rev 1.0 — RK3568 + RK809-5 参考电源树

状态：电源拓扑按Rockchip指南及EVB参考设计进一步明确；尚未完成逐球映射、器件值核算和KiCad电气原理图。

## 1. 输入电源与母线

- USB-C PD输入冻结为15V/3A（45W）。
- 15V_IN经同步Buck降为5V_SYS。
- RK809-5工作输入范围2.7–5.5V，因此不得将15V直接接入RK809-5；PMIC输入由5V_SYS供电。
- 5V_SYS同时供USB VBUS开关和各后级电源转换器。
- 5V_SYS总电流预算、SoC峰值负载和USB外设预算必须以45W PD合同为输入上限联合核算，同时受5V/5A（25W）主Buck输出能力约束。Rev 1仅配置1个USB3 Host和2个USB2 Host，Type-A VBUS初始总预算1.9A。
- HUSB238为当前PD控制器；Hynetek参考设计表给出RVSET=14kΩ对应15V、RISET=22.6kΩ对应3.0A。输入限流、TVS/过压、反灌保护及适配器PDO仍需验证。

## 2. RK3568 + RK809-5参考电源树（功能映射）

参考Rockchip RK3568 Hardware Design Guide V1.2 Figure 2-62，以及RK3568 EVB参考电源图：

| RK809-5输出 | 参考分配 | A1决策 |
|---|---|---|
| BUCK1（VCC1，2.5A max） | VDD_LOGIC | 按原厂默认电压、动态调压和电容要求实现 |
| BUCK2（VCC2，2.5A max） | VDD_GPU | 按原厂DVFS要求实现 |
| BUCK3（VCC3，1.5A max） | VCC_DDR | FB3外部分压必须按实际LPDDR4X电压设置；LPDDR4X模式按指南另配置VCC0V6_DDR |
| BUCK4（VCC4，1.5A max） | VDD_NPU | A1首版不启用NPU时，按官方未使用模块处理并在DTS禁用；不可把1.5A输出当作满足≥2A替代Buck要求 |
| LDO1 | VDDA0V9_IMAGE | 未使用Image PHY时按原厂建议关闭/处理 |
| LDO2 | VDDA0V9 | 参考原厂模拟电源分配 |
| LDO3 | VDDA0V9_PMU | PMU低噪声电源 |
| LDO4 | Audio codec VDDIO | A1首版不使用RK809音频Codec时，按官方未用引脚规则处理 |
| LDO5 | VCCIO_SD / SDMMC0 IO | 参考EVB分配；若MicroSD采用3.3V IO，需确保Bank和DTS匹配 |
| LDO6 | VCC3V3_PMU | PMUIO1/PMUIO2的3.3V域，需结合PMUIO2最终配置 |
| LDO7 | VCCA_1V8 | PMUPLL_AVDD_1V8等参考电源 |
| LDO8 | VCCA1V8_PMU | PMU 1.8V域 |
| LDO9 | VCCA1V8_IMAGE | 未使用Image PHY时按原厂建议关闭/处理 |
| BUCK5 / Switch1 | VCC_3V3、VCC_1V8的系统电源路径 | 依Figure 2-62及完整EVB原理图确认具体网络和开关连接 |
| Switch2 | VCC3V3_SD / MicroSD卡电源 | 按MicroSD卡电源控制需求决定是否采用 |

注意：以上是原厂参考电源树功能分配，不是已经完成的A1逐脚电路。所有LDO的VCC5/VCC6/VCC7输入分配、Switch1/2供电、BUCK5及VCC8/VCC9/VCC_RTC连接，必须对照完整RK809-5参考原理图核对后再绘制。

## 2A. 外部电源支路与参考实现

公开的RK3568 LPDDR4 32-bit参考原理图（96Boards CE schematic）提供了一个可交叉核对的RK809-5实现示例：
- 外部Buck为VDD_CPU供电，参考设计能力6A；RK3568指南要求至少4A。
- BUCK1→VDD_LOGIC（0.9V）。
- BUCK2→VDD_GPU（0.9V）。
- BUCK3→VDD_DDR，FB3可调。
- BUCK4→VDD_NPU，参考设计默认关闭。
- LDO2→VDDA_0V9；LDO3→VDDA0V9_PMU。
- LDO5→VCCIO_SD；LDO6→VCC3V3_PMU。
- LDO7→VCCA_1V8；LDO8→VCCA1V8_PMU。
- BUCK5→VCC_1V8；SW1→VCC_3V3；SW2→VCC3V3_SD。
- 外部Buck生成VCC3V3_SYS；外部LDO用于该参考设计的VCC2V5_DDR。

该参考图采用LPDDR4配置，不能将其中的VCC2V5_DDR直接移植到A1的LPDDR4X方案。LPDDR4X必须按Rockchip Figure 2-29及LPDDR4X模板改为相应1.8V/1.1V/0.6V供电结构，并按具体颗粒核对。

参考资料：96Boards BEIQI CE RK3568 LPDDR4 schematic，Power Diagram/Power Sequence。
https://www.96boards.org/documentation/consumer/tb-96ai-3586ce/hardware-docs/files/tb-96ai-3586ce-schematics.pdf



Rockchip指南V1.2：
- VDD_CPU：独立Buck，输出能力≥4A，动态调压；VDD_CPU_COM接Buck FB远端反馈；精度±1.5%；10%至80%负载跃迁斜率1A/µs，纹波±3%；总输出电容>135µF。
- VDD_GPU：Buck能力≥2A；峰值约1.2A；精度±1.5%；总输出电容>90µF。
- VDD_NPU：指南要求Buck能力≥2A；峰值约1A。A1首版禁用NPU，需同时在电源树和DTS明确处理。
- VDD_LOGIC：指南2.2.2.7要求Buck能力≥2A；峰值约1.2A；总输出电容>90µF。参考RK809-5 BUCK1 2.5A。
- PMU_VDD_LOGIC_0V9：峰值50mA，可与PMUPLL_AVDD_0V9合并。
- SYSPLL/PMUPLL模拟电源：优先低噪声LDO，PSRR@1kHz >65dB。

Rockchip离散电源章节另允许GPU与NPU在特定功耗场景下共用≥3A动态Buck；A1不采用该合并方案作为默认设计。

## 4. LPDDR4X电源

RK3568 LPDDR4X模式下：
- DDRPHY_VDDQ = 1.1V。
- DDRPHY_VDDQL = 0.6V。
- RK3568 VCC_DDR与VCC0V6_DDR为两组供电网络。
- LPDDR4X ZQ电阻：240Ω、1%接VCC0V6_DDR。
- Rockchip RK809-5方案需同步调整BUCK3 FB3（Pin 27）分压，使VCC_DDR匹配所选DRAM。
- Rockchip参考设计包含LPDDR4/LPDDR4X兼容电路，LPDDR4X时R3804不装，绿色框内元件需装配。
- LPDDR4X待机自刷新时，1.8V供电必须保持。
- SoC VCC_DDR/VCC0V6_DDR去耦按指南Figure 2-51及PCB Figure 3-34至3-37布置。
- Micron颗粒VDD1/VDD2/VDDQ必须按完整料号数据手册逐一核对，不能直接把SoC PHY 1.1V/0.6V当成DRAM电源脚定义。

DDR颗粒、模板和BIN未完成配对，因此VCC_DDR/0.6V电源具体器件及分压暂不冻结。

## 5. CPU Buck

TCS4525_WT作为候选，需与Rockchip参考方案核对：
- 输入电压来自5V_SYS。
- 输出动态调压范围按RK3568指南和DVFS软件配置确定。
- 输出能力≥4A。
- 反馈接VDD_CPU_COM。
- 输入电容、输出电容、电感饱和电流、补偿和散热按TCS4525正式数据手册及参考原理图设计。
- 不因器件标称5A就直接认定满足动态响应与热设计要求。

## 6. RK809-5关键限制

- 输入范围2.7–5.5V；VCC_RTC需为最高电压电源或满足Vmax-0.3V，推荐与VCC9同源。
- VCC_RTC先于或同时于其他供电上电。
- VCC9上电后需高于3.0V；VDC启动门限>0.55V，推荐约1.2V；EXT_EN拉高后VCC9需在1.5ms内达到3.0V。
- RK809-5上电时序固化，不可修改，不可与RK809-1/-2/-3混用。
- PWRON按键启动需拉低超过500ms。
- 32.768kHz晶体负载电容按晶体CL计算，指南推荐22pF且不低于18pF。
- RESETB保留100nF电容；SDA/SCL/INT/CLK32K/RESETB开漏信号需正确上拉。
- 不使用Fuel Gauge时，BATDIV、SNSP、SNSN按指南接地。
- BUCK1/2输入电容>10µF、输出电容>30µF。
- BUCK3输入电容>10µF、输出电容>30µF；FB3参考电压0.8V，分压按VCC_DDR目标计算。
- BUCK4输入电容>10µF、输出电容>30µF。
- BUCK5输入电容>10µF、输出电容>33µF。
- 电感参考0.47µH，饱和电流>3.5A，DCR<50mΩ，优先<20mΩ。

## 7. IO Bank电源

- PMUIO0固定1.8V，PMUIO1固定3.3V；PMUIO2与VCCIO1、VCCIO3–VCCIO7必须与DTS配置一致。
- VCCIO2是Flash IO域，1.8V时FLASH_VOL_SEL拉高，3.3V时拉低。
- A1计划使用eMMC、SDMMC0、SDMMC2、GMAC0、UART/I2C，所有IO Bank需根据最终PinMux统一定电压。
- USB3 PHY、MULTI_PHY、HDMI PHY模拟电源按原厂低噪声LDO/磁珠/去耦网络实现。
- 不使用的PHY电源可按指南关闭，但对应DTS节点必须禁用。

## 8. 原理图下一步

1. 获取Rockchip RK3568 EVB完整RK809-5原理图，逐项核对Figure 2-62的VCC1–VCC9、LDO输入和Switch网络。
2. 逐球核对RK3568所有电源球位和网络名。
3. 计算15V→5V_SYS输入功率、5V负载和各后级稳压器的热耗散。
4. 完成CPU/GPU/Logic/DDR Buck外围元件值与电源完整性核算。
5. 完成PMIC上电、复位、晶振、I2C及电源键电路。
6. KiCad绘制并完成ERC后再进入SoC信号页。

## 参考资料

- Rockchip RK3568 Hardware Design Guide V1.2, Sections 2.1.7.5, 2.2.2–2.2.3, Figures 2-28–2-63.
  https://dl.xkwy2018.com/downloads/RK3568/RK356X/Hardware/Rockchip_RK3568_Hardware_Design_Guide_V1.2_EN.pdf
- RK3568 EVB User Guide V1.2, Power Diagram.
  https://dl.xkwy2018.com/downloads/RK3568/RK356X/Hardware/Rockchip_RK3568_EVB_User_Guide_V1.2_EN.pdf
- RK809 Datasheet Rev 2.5.
  https://www.boardcon.com/download/Rockchip_RK809_Datasheet_V2.5-20250407.pdf
- RK3568 public reference design index (schematic and PCB review references):
  https://github.com/hqnicolas/RK3568-hardware-design


## RK809-5 PMIC page implementation (2026-11-15)

- Native page: `hardware/kicad/A1_RK809_PMIC.kicad_sch` (page 2).
- RK809-5 VCC1..VCC9 and VCC_RTC are supplied from 5V_SYS; VCC_RTC is therefore not below any other PMIC input.
- VCC_1P8A/D are supplied from BUCK5 1.8V output; BUCK5 FB5 is sensed at that output.
- Active buck channels represented: BUCK1, BUCK2, BUCK3 and BUCK5; BUCK4 is held OFF per RK809-5 OTP default.
- 0.47uH inductors use Isat >=4A and DCR <20mOhm as design targets. Two 47uF output capacitors per active buck are nominal values only; verify effective capacitance at DC bias.
- BUCK3 feedback resistor values are intentionally TBD until the selected LPDDR4X rail voltage is known.
- Open-drain I2C/INT/RESETB/CLK32K lines pull up to the 1.8V domain; RESETB has 100nF; VDC divider 100k/33k gives approximately 1.24V.
- This PMIC page does not yet assign its outputs to individual RK3568 supply balls. That mapping must be checked against the complete Rockchip EVB power tree and exact memory configuration.
