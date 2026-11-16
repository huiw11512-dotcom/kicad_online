# Linux MiniHost A1

RK3568 ARM64 Linux SBC。目标是树莓派 4B 级别的独立 Linux 单板计算机，优先保证稳定启动、存储、显示、网络和 USB 接口；不宣称与树莓派 4B 的 CPU 性能相同。

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

<badge>DESIGN IN PROGRESS — DO NOT FABRICATE</badge>

KiCad 主工程已建立层级原理图：**1 张根页 + 12 张子页**。当前源文件结构如下：

1. 根页：USB-C PD、输入保护、15V→5V Buck
2. RK809-5 PMIC
3. DDR 电源
4. 预 PMIC 3.3V 电源
5. RK3568 SoC（17 个 unit）
6. CPU 动态 Buck
7. 32GB eMMC
8. Boot、时钟、复位、UART2 与 Recovery
9. Micron 2GB LPDDR4X
10. MicroSD
11. USB3 HOST1 与 USB-C OTG0 下载/恢复
12. USB2 HOST2/HOST3 两个独立 Type-A Host
13. 初步 Gigabit Ethernet PHY / MagJack 页面

### 已完成的源文件核对

- RK3568：636 个唯一球位；Pin assignment CSV 为 610 个已分配网络 + 26 个显式 NC。
- SoC 原理图 global labels 与 CSV 做坐标级交叉核对：0 个网络标签错配；26 个 NC 标记与 CSV 一致。
- USB2 HOST2/3：SoC R1/R2 对应 HOST2 D−/D+，T1/T2 对应 HOST3 D−/D+；此前误放在 K17/K18/M12/M17 电源球位上的 USB 标签已纠正。
- Wi-Fi/BT pinmux：由于 GMAC0 RGMII 与 SDMMC1 复用球位冲突，Wi-Fi 临时改分配到 SDMMC2 M0，Bluetooth UART 临时分配 UART8 M0；AP6275S 仍是候选模块，电源、时钟、唤醒控制和模块页尚未完成。
- MicroSD：VCC 由 RK809-5 SWOUT2 控制；R57 0Ω 旁路为 DNP，不得装配。
- Ethernet：RTL8211F-CG + HR911130A 初步页已建立；PHY strap、电源、时钟、RGMII 延时、MagJack 引脚和网表审查仍未关闭。

以上是源文件结构与静态映射检查，不等于 KiCad 原生 ERC、网表、电气规则、PCB DRC 或硬件验证通过。

## 尚未完成

- HDMI 完整电路。
- Wi-Fi/BT 模块电路、AP6275S 50-pad footprint、3.3V VBAT/1.8V VDDIO、37.4MHz 晶体、1.8V/32.768kHz LPO 和唤醒控制。
- Ethernet PHY 逐引脚审查与千兆链路验证。
- 40-pin GPIO 最终 pinmux、电压域和连接器。
- 生产测试点、完整电源预算、热设计和局部去耦审查。
- 整板 PCB 布局尚未开始。

## 打开工程

GitHub 网页预览不会把整个 KiCad 层级工程渲染成一张可编辑原理图。请下载完整的 `hardware/kicad` 目录，保留其中的子原理图、符号库和封装库，再用桌面 KiCad 打开工程文件：

- [KiCad 工程文件 A1.kicad_pro](hardware/kicad/A1.kicad_pro)
- [根原理图 A1.kicad_sch](hardware/kicad/A1.kicad_sch)
- [完整 KiCad 工程目录](hardware/kicad/)
- [KiCad 工程说明](hardware/kicad/README.md)

## 关键设计文件

- [Rev1 主设计基线](docs/A1_MASTER_BASELINE_REV1.md)
- [电气实现决策](docs/A1_ELECTRICAL_DECISIONS_REV1.md)
- [Wi-Fi/BT pinmux 与电气基线](hardware/kicad/docs/A1_WIFI_BT_PINMUX_REV1.md)
- [Ethernet PHY 审查清单](hardware/kicad/docs/A1_ETHERNET_VALIDATION_REV1.md)
- [DDR 选型与兼容性门槛](docs/DDR_COMPATIBILITY_GATE.md)
- [DDR 首轮审计记录](docs/A1_DDR_AUDIT_2026-11-16.md)
- [Rockchip DDR 模板 / BIN 确认请求](docs/RK3568_DDR_FAE_REQUEST.md)

## 投板前硬门槛

1. 取得当前官方 Rockchip DDR AVL、精确模板文件、DDR BIN 和 WDQS 适用说明。
2. 完成 RK809-5 全部电源轨与上电时序逐网核对。
3. 完成 HDMI、Ethernet、Wi-Fi/BT、GPIO 等外围原理图。
4. 用原生 KiCad 执行 ERC、网表导出、封装检查和 PCB DRC。
5. 完成六层叠层、阻抗、DDR 拓扑/长度约束、BGA 扇出和电源完整性审查。
6. 首板完成 DDR Training、eMMC 启动、外设功能和联合压力测试。

在上述门槛关闭前，不发布制造版 Gerber、坐标文件或投板 BOM。
