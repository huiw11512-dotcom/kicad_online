# A1 Rev1 — 已核实的电气实现决策

日期：2026-11-15
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
4. USB3 OTG0_DP/DM → 独立Micro-USB service connector，仅作MaskROM/Loader/ADB调试口；OTG0 SuperSpeed的MULTI_PHY0不接外部接口，按原厂unused-module规则处理。
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

USB VBUS总电流预算暂定1.9A（USB3 Host1 0.9A + 两个USB2 Host各0.5A），每口独立限流。Service Micro-USB为Device下载接口，不向主机反向供电；VBUS只作检测并按原厂推荐电路处理。

PD Sink器件必须明确支持15V/3A PDO、输入额定电压、CC状态及过压保护。HUSB238当前阻值：RVSET=14kΩ请求15V，RISET=22.6kΩ请求3.0A（Hynetek参考设计电阻表）；仍须按芯片版本和目标适配器PDO实测确认。

## 3. eMMC启动与Recovery

- eMMC连接RK3568专用EMMC 8-bit接口，含D0–D7、CMD、CLK、RSTn及DATA_STROBE（若所选eMMC/模式使用）。
- eMMC VCC/VCCQ电压按所选颗粒数据手册及RK3568 VCCIO2/FLASH_VOL_SEL要求匹配。
- Recovery按键使用SARADC_VIN0，默认10kΩ上拉到VCCA_1V8，按下拉低；必须保留该上拉。
- MicroSD使用SDMMC0，VCCIO3按3.3V默认方案，D0–D3/CMD/CLK串联22Ω，DET串联100Ω，SD3.0 ESD结电容<1pF。
- SDMMC0与JTAG复用，A1优先保留Recovery与UART2调试，JTAG使用测试焊盘而非占用SDMMC0连接器信号。

## 4. Wi-Fi / Bluetooth

- 优先采用已集成Wi-Fi/BT的焊接式combo模块，不在A1首版单独设计RF前端。
- Wi-Fi优先使用SDMMC1（默认分配），UART接口接Bluetooth；需核对模块是否支持该总线宽度、IO电压、UART流控和32.768kHz要求。
- 低功耗待机时，如果VDD_LOGIC会关断，SDIO Wi-Fi相关控制脚需迁移到PMUIO1/2域或保证模块掉电策略；不能把普通VCCIO域GPIO作为掉电后保持状态的控制脚。
- 天线端保留π型匹配位和净空区；模块型号、天线形式及认证约束冻结前不得出PCB。
- 不再预设SDMMC2作为Wi-Fi总线，待与40-pin GPIO、PinMux和电压域一起做全局冲突审查后选择唯一控制器。

## 5. Ethernet

- 使用GMAC0 RGMII + RTL8211F系列PHY候选。
- PHY具体后缀、25MHz晶振/时钟输入方式、PHY strap、RGMII TX/RX delay模式、LED配置、磁性器件和RJ45必须按PHY完整数据手册与RK3568 EVB核对。
- 不能同时在MAC和PHY端重复加入RGMII延时。
- RJ45每对线按磁性器件推荐电路，连接器侧预留ESD和共模EMI调试位。
- GMAC0与SDMMC/其他GPIO存在PinMux和VCCIO Bank复用风险，所有信号必须以最终PinOut表逐球核对。

## 6. 不再变更的首版范围

- 1×USB3 Host Type-A
- 2×USB2 Host Type-A
- 1×Micro-USB service/download
- 1×HDMI
- 1×Gigabit Ethernet
- 1×MicroSD
- 1×32GB eMMC目标
- 1×4GB LPDDR4X目标
- 1×Wi-Fi/BT combo module
- 1×40-pin GPIO header
- 1×USB-C PD 15V/3A input
- 6-layer PCB

## 7. 依据

- Rockchip RK3568 Hardware Design Guide V1.2, §2.3.4 USB2.0/USB3.0: controllers, PHY sharing, OTG download port, VBUSDET, ESD, series components and VBUS current limiting.
  https://dl.xkwy2018.com/downloads/RK3568/RK356X/Hardware/Rockchip_RK3568_Hardware_Design_Guide_V1.2_EN.pdf
- Rockchip RK3568 Hardware Design Guide V1.2, §2.3.1 SDMMC0/1/2 and SDIO Wi-Fi standby requirements.
- Rockchip RK3568 Hardware Design Guide V1.2, §2.2 and Figures 2-62/2-63 for RK809-5 rail assignment and fixed power-on sequence.
