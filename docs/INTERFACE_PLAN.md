# A1外部接口规划 Rev1

| 接口 | 数量 | 实现 |
|---|---:|---|
| HDMI 2.0a | 1 | RK3568 HDMI TX，Micro-HDMI Type-D（原理图待补） |
| USB 3.x Type-A | 1 | USB3 HOST1，独立限流 |
| USB 2.0 Type-A | 2 | USB2 HOST2/HOST3，各自独立限流 |
| USB-C Service | 1 | USB2 OTG0 Device，MaskROM/Loader/ADB 下载恢复 |
| RJ45 Gigabit | 1 | GMAC0 RGMII + RTL8211F-CG 候选 + HR911130A MagJack；初步页已建立 |
| Wi-Fi/BT | 1模块 | AMPAK AP6275S 候选；Wi-Fi SDIO 接 SDMMC2 M0，BT HCI UART 接 UART8 M0 |
| USB-C PD | 1 | 15V/3A 输入目标，HUSB238 + 15V→5V 主 Buck |
| MicroSD | 1 | SDMMC0，SD 3.0，VDD 由 RK809 SWOUT2 控制 |
| eMMC | 1 | 32GB eMMC 5.1，8-bit |
| GPIO | 40-pin | 兼容树莓派排针定义目标；PinMux/电压域审核后冻结 |
| UART Debug | 1组 | UART2，3.3V TTL |
| Power/Reset | 各1 | 按键和测试点 |
| Recovery | 1组 | USB-C OTG0 + Boot/MaskROM 测试焊盘 |

## PinMux约束

- GMAC0 RGMII 使用与 SDMMC1 复用的 RK3568 球位，因此 SDMMC1 不再分配给 Wi-Fi。
- Wi-Fi 临时分配 SDMMC2 M0（VCCIO6=1.8V），目标 SDIO SDR50/100MHz；RK3568 SDMMC2 上限 150MHz，不能按 SDR104/208MHz 设计。
- Bluetooth 临时分配 UART8 M0（VCCIO4=1.8V）。
- AP6275S 的 VDDIO 为 1.8V，VBAT 为 3.3V，峰值电流、37.4MHz 晶体、32.768kHz LPO 和低功耗唤醒控制仍须完成电路设计。
- 6层 PCB；首版不引出 M.2 NVMe、SATA、第二网口、第二 HDMI、MIPI CSI/DSI、PoE、音频 Codec 和工业总线。
