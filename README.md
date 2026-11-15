# Linux SBC A1

自主设计ARM64 Linux单板计算机，产品定位和使用场景参考Raspberry Pi 4B。RK3568 SoC、LPDDR4X、eMMC、PMIC、网络PHY、无线模块和全部外部接口直接集成在同一块PCB上；不是CM5载板，不复制第三方SBC工程。

## Rev 0.1基线

| 模块 | 选型/目标 |
|---|---|
| SoC | Rockchip RK3568，FCBGA636L |
| CPU/GPU | 4 × Cortex-A55，最高2.0GHz；Mali-G52 |
| RAM | 4GB LPDDR4X，32-bit |
| 存储 | 32GB eMMC 5.1 + MicroSD |
| PMIC | RK809-5 + 独立VDD_CPU Buck |
| 显示 | 1 × HDMI 2.0a |
| 网络 | 1 × Gigabit Ethernet，RTL8211F-CG候选 |
| USB | 2 × USB 3.0 Host + 2 × USB 2.0 Host |
| 无线 | AP6275系列Wi-Fi/BT模块候选，SDIO + UART |
| GPIO | 40-pin兼容排针 |
| 电源 | USB-C PD，9V/3A目标，转换为5V_SYS |
| 调试 | UART、Power/Reset/Recovery |
| PCB | 6层、1.6mm FR-4起步 |
| 外形 | 85 × 56mm目标，布局验证后冻结 |

## 性能边界

RK3568是四核Cortex-A55，树莓派4B采用四核Cortex-A72。A1以Pi 4B的整机功能和应用场景为参照，不宣称CPU基准性能相同。若跑分必须达到Pi 4B，再评估更高一级SoC。

## 设计规则

- SoC、DDR、PMIC、电源、存储和接口全部自主集成。
- 使用Rockchip数据手册、硬件设计指南、DDR模板和启动配置作为设计约束。
- DDR颗粒必须匹配Rockchip支持清单、PCB模板和DDR初始化BIN。
- 首版不做M.2 NVMe、双网口、MIPI摄像头、PoE、SATA和复杂音频。
- 不得在DDR/供电/阻抗尚未核验时投板。

## 当前状态

RK3568为首选；4GB LPDDR4X、32GB eMMC容量已定，具体料号待核；RK809-5为PMIC首选；原理图和PCB尚未完成。
