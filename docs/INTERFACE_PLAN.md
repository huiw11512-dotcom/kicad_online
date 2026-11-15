# A1外部接口规划

| 接口 | 数量 | 实现 |
|---|---:|---|
| HDMI 2.0a | 1 | SoC HDMI TX，Micro-HDMI Type-D |
| USB 3.0 Type-A | 2 | 1 × USB3 Host + 1 × USB3 DRD固定Host |
| USB 2.0 Type-A | 2 | 2 × USB2 Host |
| RJ45 Gigabit | 1 | GMAC RGMII + RTL8211F-CG |
| Wi-Fi/BT | 1模块 | AP6275系列候选，SDIO + UART |
| USB-C PD | 1 | 9V/3A目标输入 |
| MicroSD | 1 | SD 3.0 |
| eMMC | 1 | 32GB eMMC 5.1，8-bit |
| GPIO | 40-pin | 兼容树莓派排针定义目标 |
| UART Debug | 1组 | 3.3V TTL |
| Power/Reset | 各1 | 按键和测试点 |
| Recovery | 1组 | 优先保留Boot/USB恢复测试焊盘 |

首版删除M.2 NVMe、SATA、第二网口、第二HDMI、MIPI CSI/DSI、PoE、音频Codec和工业总线。
