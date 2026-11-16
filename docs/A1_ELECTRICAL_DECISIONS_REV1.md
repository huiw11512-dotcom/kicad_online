# A1 Rev1 — 已核实的电气实现决策

日期：2026-11-16
状态：架构/接口决策。不是已完成KiCad原理图。与[A1_MASTER_BASELINE_REV1.md](A1_MASTER_BASELINE_REV1.md)冲突时，以主基线为准。

## 1. 重要更正：USB控制器资源

RK3568不是“任意组合两个USB3+两个USB2”。原厂指南2.3.4说明：
- 1个USB3 OTG0：SuperSpeed使用MULTI_PHY0，USB2兼容速率使用USB2 OTG0 PHY。
- 1个USB3 HOST1：SuperSpeed使用MULTI_PHY1，USB2兼容速率使用USB2 HOST1 PHY。
- 另有USB2 HOST2和USB2 HOST3两个独立Host PHY。
- USB3 OTG0_DP/DM是系统固件下载口；原厂明确要求开发和生产阶段必须保留，且USB3_OTG0_VBUSDET必须连接。
- OTG0在U-Boot前默认为Device模式；如果只作为Host使用，烧录/ADB仍需切回Device模式。

**A1 Rev1最终USB分配：**
1. USB3 HOST1 → 1个USB3 Type-A（Host）。
2. USB2 HOST2 → 1个USB2 Type-A（Host）。
3. USB2 HOST3 → 1个USB2 Type-A（Host）。
4. USB3 OTG0_DP/DM → 独立USB-C service connector，仅作MaskROM/Loader/ADB调试口；OTG0 SuperSpeed的MULTI_PHY0不接外部接口，按原厂unused-module规则处理。
5. OTG0_ID、OTG0_VBUSDET按原厂推荐电路处理；VBUSDET不得悬空。
6. 各Host VBUS使用独立限流开关、GPIO使能、过流状态反馈和连接器侧ESD。
7. USB2 DP/DM串联2.2Ω；USB3 TX串联100nF AC耦合电容（0201），RX预留0Ω；USB3 ESD寄生电容≤0.4pF；USB2 ESD按原厂≤3pF要求。
8. MULTI_PHY和USB PHY模拟电源的磁珠隔离、4.7µF+100nF去耦不得省略。

## 2. 输入电源决策

A1 Rev 1输入冻结为USB-C PD 15V/3A（45W），与当前KiCad输入级一致。
选择15V/3A的原因：与现有HUSB238电路及LM76005输入设计匹配，45W PD合同对5V/5A（25W）主Buck有输入余量；不得把45W合同误认为5V_SYS可输出45W。

电源链：
USB-C PD Sink → 输入保险/电子保险及TVS/反灌保护 → 15V_IN → 5V_SYS同步Buck → RK809-5及后级DC/DC。
RK809-5工作输入为2.7–5.5V，不允许15V直接进入PMIC。

USB VBUS总限流阈值预算按2.34A计（USB3 HOST1 0.989A max + USB2 HOST2/HOST3各0.673A max），每口独立限流。该值是限流阈值上限之和，不是预期持续负载；5V_SYS功率预算必须覆盖最坏情况并校核PD/主Buck余量。Service USB-C为Device下载接口，不向主机反向供电；VBUS只作检测并按原厂推荐电路处理。

PD Sink器件必须明确支持15V/3A PDO、输入额定电压、CC状态及过压保护。HUSB238当前阻值：RVSET=14kΩ请求15V，RISET=22.6kΩ请求3.0A（Hynetek参考设计电阻表）；仍须按芯片版本和目标适配器PDO实测确认。

## 3. eMMC启动与Recovery

- eMMC连接RK3568专用EMMC 8-bit接口，含D0–D7、CMD、CLK、RSTn及DATA_STROBE（若所选eMMC/模式使用）。
- eMMC VCC/VCCQ电压按所选颗粒数据手册及RK3568 VCCIO2/FLASH_VOL_SEL要求匹配。
- Recovery按键使用SARADC_VIN0，默认10kΩ上拉到VCCA_1V8，按下拉低；必须保留该上拉。
- MicroSD使用SDMMC0，VCCIO3按3.3V默认方案，D0–D3/CMD/CLK串联22Ω，DET串联100Ω，SD3.0 ESD结电容<1pF。
- SDMMC0与JTAG复用，A1优先保留Recovery与UART2调试，JTAG使用测试焊盘而非占用SDMMC0连接器信号。

## 4. Wi-Fi / Bluetooth

- 组合模块候选为 AMPAK AP6275S；首版不单独设计 RF 前端。
- **不能继续使用 SDMMC1 作为 Wi-Fi 总线。** A1 的 GMAC0 RGMII 引脚与 RK3568 SDMMC1 复用球位重叠，二者不能同时占用。
- 当前临时分配为 **SDMMC2 M0 / VCCIO6=1.8V** 承载 4-bit SDIO；**UART8 M0 / VCCIO4=1.8V** 承载 Bluetooth HCI UART。SoC 原理图和 pin assignment CSV 已同步更新，详见 `hardware/kicad/docs/A1_WIFI_BT_PINMUX_REV1.md`。
- AP6275S 支持 SDR50 100MHz、SDR104 208MHz 和 DDR50 50MHz；RK3568 SDMMC2 上限 150MHz，首版按 SDR50/100MHz 设计，不得宣称 SDR104/208MHz。
- AP6275S 的 VBAT=3.0–3.8V（典型3.3V，峰值约1.2A），VDDIO=1.8V；需为 VBAT 预留至少1.5A瞬态余量并验证整板3.3V电源预算。
- 模块需要 37.4MHz 晶体/参考及 1.8V 幅度的 32.768kHz LPO。当前 PMIC/SoC 32kHz 网络位于 3.3V PMUIO2 域，不可直接接模块 LPO，必须增加合适的 1.8V 缓冲/电平转换或独立时钟源。
- AA1/AA5 暂分配 WIFI_HOST_WAKE/WIFI_REG_ON，但位于 VCCIO6，不能保证 VDD_LOGIC 关闭时保持。BT_REG_ON、BT_WAKE、BT_HOST_WAKE 尚未分配；需先确定是否要求深度待机唤醒，再决定 PMUIO 保持域与 1.8V 电平转换。
- 天线端保留 π 型匹配位和净空区；模块型号、封装、天线形式及认证约束冻结前不得出 PCB。

## 5. Ethernet

- 使用 GMAC0 RGMII + RTL8211F-CG + HR911130A（LCSC C54408）；初步原理图页已建立。
- PHY strap 已从当前原理图解码：PHYAD[2:0]=001，Linux PHY address=1；CFG_EXT=0、CFG_LDO[1:0]=10，使用内部 1.8V RGMII I/O LDO；TXDLY=1、RXDLY=1，PHY 两方向均加入约2ns内部时钟延迟。
- 因 PHY 已启用 TX/RX 内部延迟，RK3568 MAC/设备树不得再叠加 TX/RX delay；首版按无额外延迟的 RGMII 模式配置，最终以 Rockchip 驱动和 PHY driver 实际配置核实。
- 25MHz 时钟当前由 RK3568 `ETH0_REFCLKO_25M` 经 R134=22Ω 串联电阻送到 RTL8211F pin37 XTAL_OUT/EXT_CLK；pin36 XTAL_IN 接地。SoC VCCIO4=1.8V，符合 Realtek 外部时钟输入 VIH≥1.4V / VIL≤0.4V 门限，但仍需验证频率、占空比、抖动和边沿。
- MDIO 上拉 R138=1.5kΩ 到 VCC_1V8；PHYRSTB 上拉 R136=10kΩ 到 VCC3V3_SYS；PHY_INT_N 上拉 R137=4.7kΩ 到 VCC3V3_SYS；RSET R148=2.49kΩ 到 GND。
- HR911130A 绿色 LED 极性已纠正：pin11 anode 经 R149=510Ω 接 PHY LED1（active-high），pin12 cathode 接 GND；黄色 LED pin14 anode 经 R150=510Ω 接 3.3V，pin13 cathode 接 PHY LED2（active-low）。
- GMAC0 RGMII 与 SDMMC1 复用球位重叠，Wi-Fi 已改分配到 SDMMC2 M0；不得再把 SDMMC1 分配给 Wi-Fi。
- 尚未关闭：PHY 全部供电/去耦与上电时序、MagJack P10/TCT/屏蔽端接、ESD、native ERC/netlist、RGMII/MDI PCB 阻抗和首板链路验证。详见 `hardware/kicad/docs/A1_ETHERNET_VALIDATION_REV1.md`。

## 6. 不再变更的首版范围

- 1×USB3 Host Type-A
- 2×USB2 Host Type-A
- 1×USB-C service/download（USB2 OTG0）
- 1×HDMI
- 1×Gigabit Ethernet
- 1×MicroSD
- 1×32GB eMMC目标
- 1×2GB LPDDR4X首板基线（Micron MT53E512M32D1ZW-046B WT:B）；4GB D2FW 作为独立后续版本
- 1×Wi-Fi/BT combo module
- 1×40-pin GPIO header
- 1×USB-C PD 15V/3A input
- 6-layer PCB

## 7. LPDDR4X 首板决策

- 首板采用 Micron MT53E512M32D1ZW-046B WT:B，2GB、x32、单 Die、单 Rank。
- 4GB MT53E1G32D2FW-046 WT:C 作为后续独立版本候选；公开 Rockchip DDR AVL v3.01 转录也显示 RK3568 T/A，但需单独核对双 Die/rank、封装和模板/BIN。
- DRAM ZQ0 使用 240Ω±1% 接 VCC0V6_DDR；RK3568 DDR_RZQ H7 使用 120Ω±1% 接 VCC_DDR_1V1。
- Rockchip Hardware Design Guide Rev1.2 将 SD6 列为 LPDDR4X 基础参考模板；rkbin 中 SD4 属于 WDQS-capable 模板集合。当前 MPN 无公开 WDQS 应用注释标记，按标准 non-WDQS 路径推进；正式模板/BIN 仍需 FAE 确认。
- 67 条 DRAM 信号与 SoC 球位表已做源文件比对，未发现球号错配；该检查不等于 KiCad ERC/DRC 或 DDR Training。

## 8. 依据

- Rockchip RK3568 Hardware Design Guide V1.2, §2.3.4 USB2.0/USB3.0: controllers, PHY sharing, OTG download port, VBUSDET, ESD, series components and VBUS current limiting.
  https://dl.xkwy2018.com/downloads/RK3568/RK356X/Hardware/Rockchip_RK3568_Hardware_Design_Guide_V1.2_EN.pdf
- Rockchip RK3568 Hardware Design Guide V1.2, §2.3.1 SDMMC0/1/2 and SDIO Wi-Fi standby requirements.
- Rockchip RK3568 Hardware Design Guide V1.2, §2.2 and Figures 2-62/2-63 for RK809-5 rail assignment and fixed power-on sequence.\n- AMPAK AP6275S Datasheet Rev.2.7 for SDIO modes, 1.8V VDDIO, 3.3V VBAT, LPO and 37.4MHz crystal requirements.
