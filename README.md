# Linux MiniHost A1

RK3568 ARM64 Linux SBC。目标是树莓派 4B 级别的使用场景与接口体验，首要目标是独立、稳定启动 Linux；不宣称与树莓派 4B 的 CPU 性能相同。

## Rev1 首板基线

| 模块 | 首板方案 |
|---|---|
| SoC | Rockchip RK3568，FCBGA636 |
| RAM | 2GB LPDDR4X x32，Micron MT53E512M32D1ZW-046B WT:B，单颗、单 Die、单 Rank |
| 系统存储 | 32GB eMMC 5.1，Samsung KLMBG2JETD-B041 候选 |
| 扩展存储 | MicroSD，SDMMC0 4-bit |
| PMIC | RK809-5 |
| CPU 电源 | TCS4525_WT 独立动态 Buck，待完整时序与负载验证 |
| 输入 | USB-C PD 15V/3A |
| 主电源 | LM76005，15V_IN → 5V_SYS，5A 额定设计目标 |
| 预 PMIC 电源 | TPS62132，5V_SYS → 3.3V |
| PCB | 六层 FR-4；1.6mm 为初始目标，最终叠层与阻抗由板厂确认 |

4GB LPDDR4X 保留为后续容量版本，不混入本次 2GB 首板 BOM。4GB 候选虽也出现在公开 Rockchip DDR AVL v3.01 的 RK3568 T/A 项中，但其 D2/FW 双 Die 组织需要单独确认 rank、模板、BIN 与封装映射。

## 当前工程状态（2026-11-16）

**状态：原理图开发中，禁止投板。**

已建立的 KiCad 层级原理图包括根页及 10 张子页：

1. RK809-5 PMIC 与电源管理
2. LPDDR4X 电源
3. 预 PMIC 3.3V 电源
4. RK3568 SoC 636 球位
5. CPU 动态 Buck
6. 32GB eMMC
7. 24MHz、复位、启动配置、UART2 与 Recovery
8. Micron 2GB LPDDR4X
9. MicroSD
10. USB Host / Recovery

已完成的部分电路不等于完整产品接口已经完成。当前明确缺项：

- USB2 HOST2、USB2 HOST3 两个独立 Type-A 接口尚未完成；现有 USB 页包含一个 USB3 HOST1 Type-A 和一个 USB-C OTG0 下载/恢复接口。
- HDMI 完整电路尚未完成。
- 千兆 Ethernet PHY、磁性器件和 RJ45 尚未完成。
- Wi-Fi/BT 模块、天线及供电尚未完成。
- 40-pin GPIO 的最终 pinmux、电压域和连接器尚未完成。
- 生产测试点、完整电源预算、热设计和局部去耦仍需审查。
- 整板 PCB 尚未开始。

## DDR 首轮核验结果

- Micron 200-ball 封装图与当前 footprint 的 200 个 pad 名称逐一对应；未发现缺失或重复 pad。
- 当前 DRAM 球位表共 200 行：67 个信号连接、110 个电源/地、12 个 DNU、10 个 NC，以及 1 个 ZQ 电阻网络。
- 67 个 DRAM 信号均能在 RK3568 球位表中找到对应网络；本轮脚本核对未发现 SoC 球号错配或重复占用。
- RK3568 SoC 页的 11 个 ECC 球、P8 DDR_VREFOUT 和 F5 已按 LPDDR4X 使用条件标记 NC；全 SoC 636 球位为 607 个网络标签 + 29 个显式 NC。
- R40：DRAM ZQ0 → 240Ω ±1% → VCC0V6_DDR。
- R41：RK3568 DDR_RZQ（H7）→ 120Ω ±1% → VCC_DDR_1V1。
- Rockchip Hardware Design Guide Rev1.2 与当前 rkbin 模板表存在 SD6/SD4 模板名称差异，尚未取得 FAE 对应的正式模板与 DDR BIN 确认。

上述均为源文件与球位映射级检查，不等于 KiCad ERC、网表、电气规则或 DDR Training 通过。

## 打开工程

- KiCad 工程：hardware/kicad/A1.kicad_pro
- 根原理图：hardware/kicad/A1.kicad_sch
- [KiCad 工程说明](hardware/kicad/README.md)
- [Rev1 主设计基线](docs/A1_MASTER_BASELINE_REV1.md)
- [DDR 选型与兼容性门槛](docs/DDR_COMPATIBILITY_GATE.md)
- [DDR 首轮审计记录](docs/A1_DDR_AUDIT_2026-11-16.md)

## 投板前硬门槛

1. 取得当前官方 Rockchip DDR AVL、精确模板文件、DDR BIN 和 WDQS 适用说明。
2. 完成 RK809-5 全部电源轨与上电时序逐网核对。
3. 完成 HDMI、Ethernet、USB2、Wi-Fi/BT、GPIO 等外围原理图。
4. 用原生 KiCad 执行 ERC、网表导出、封装检查和 PCB DRC。
5. 完成六层叠层、阻抗、DDR 拓扑/长度约束、BGA 扇出和电源完整性审查。
6. 首板完成 DDR Training、eMMC 启动、外设功能和联合压力测试。

在上述门槛关闭前，不发布制造版 Gerber、坐标文件或投板 BOM。
