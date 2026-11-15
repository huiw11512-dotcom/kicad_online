# A1需求基线 Rev 0.1

| ID | 功能 | 规格 | 优先级 |
|---|---|---|---|
| SYS-001 | SoC | RK3568 FCBGA636L | P |
| SYS-002 | CPU | 4 × Cortex-A55，最高2.0GHz | P |
| MEM-001 | RAM | 4GB LPDDR4X，32-bit | P |
| STO-001 | eMMC | 32GB eMMC 5.1，8-bit | P |
| STO-002 | MicroSD | SD 3.0 | P |
| PWR-001 | 输入 | USB-C PD，9V/3A目标 | P |
| DISP-001 | 显示 | 1 × HDMI 2.0a | P |
| NET-001 | 以太网 | 1 × 10/100/1000M RJ45 | P |
| USB-001 | USB高速 | 2 × USB 3.0 Host | P |
| USB-002 | USB2 | 2 × USB 2.0 Host | P |
| WIR-001 | 无线 | Wi-Fi + Bluetooth模块 | P |
| GPIO-001 | 扩展 | 40-pin兼容排针 | P |
| DBG-001 | 调试 | UART TX/RX/GND | P |
| CTRL-001 | 控制 | Power、Reset、Recovery | P |
| THM-001 | 散热 | SoC散热片区域，预留风扇焊盘 | P |
| MEC-001 | 外形 | 85 × 56mm目标 | P |
| PCB-001 | PCB | 6层、1.6mm FR-4起步 | P |

## 设计约束

- RK3568支持32-bit DDR接口，LPDDR4X最高3200Mbps；A1先以4GB容量和原厂支持模板为准。
- USB3 Host和USB3 DRD使用不同Multi-PHY资源，按PinMux和PHY复用表核对；DRD固定配置为Host。
- 高速接口按原厂设计指南和实际板厂叠层计算阻抗。
- HDMI、USB、RJ45附近配置匹配的低电容ESD。
- 无线天线净空不得被金属外壳、散热片或高速线破坏。
- 85 × 56mm为目标尺寸，不得为追求尺寸压缩DDR布线、供电铜皮或插拔空间。
