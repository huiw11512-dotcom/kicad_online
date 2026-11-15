# Linux MiniHost A1

自主设计RK3568 ARM64 Linux SBC。目标是树莓派4B级别的应用场景和接口便利性，整板集成SoC、LPDDR4X、eMMC、PMIC、网络PHY、无线模块及外部接口；不是CM5载板，也不复制第三方SBC工程。

## Rev 1.0硬件基线

| 模块 | 决策 |
|---|---|
| SoC | Rockchip RK3568，FCBGA636L，19 × 19 mm |
| CPU/GPU | 4 × Cortex-A55；Mali-G52 |
| RAM | 4GB LPDDR4X，32-bit；颗粒/模板/BIN匹配待闭环 |
| 存储 | 32GB eMMC 5.1 + MicroSD |
| PMIC | RK809-5 + 独立VDD_CPU动态Buck |
| 显示 | 1 × HDMI 2.0a |
| 网络 | 1 × Gigabit Ethernet，GMAC0 RGMII + 外置PHY |
| USB | 1 × USB3.x Host + 2 × USB2.0 Host |
| 下载调试 | 1 × Micro-USB，连接USB3_OTG0_DP/DM，保留MaskROM/Loader/ADB |
| 无线 | 焊接式Wi-Fi/BT combo模块，SDIO + UART |
| GPIO | 40-pin、2.54 mm排针 |
| 电源 | USB-C PD 15V/3A（45W）→ 5V_SYS |
| PCB | 6层FR-4，1.6 mm起步；85 × 56 mm外形目标 |

RK3568采用Cortex-A55，树莓派4B采用Cortex-A72；本项目对标的是整机功能和使用场景，不宣称CPU跑分相同。

## 工程状态

- 当前KiCad原生原理图仅有USB-C PD输入及15V→5V主Buck初步电路。
- RK3568、RK809-5、LPDDR4X、eMMC、USB/HDMI/以太网/Wi-Fi等尚未完成原理图。
- DDR颗粒与Rockchip模板/BIN、SoC封装球位、PMIC完整电源树仍是投板前硬门槛。
- 当前工程未完成KiCad原生ERC/网表检查、PCB布局布线或硬件启动验证，不可投板。

## 设计入口

- [A1 Rev1唯一硬件基线](docs/A1_MASTER_BASELINE_REV1.md)
- [当前工程状态](docs/DESIGN_STATUS_20261115.md)
- [一次性原理图分页计划](docs/A1_SCHEMATIC_FREEZE_REV1.md)
- [电源设计计划](docs/POWER_PLAN.md)
