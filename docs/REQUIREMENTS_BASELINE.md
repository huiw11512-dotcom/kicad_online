# A1需求基线

| ID | 功能 | 优先级 | A1要求 |
|---|---|---|---|
| SYS-001 | Linux系统 | P | ARM64 Linux独立启动 |
| SYS-002 | 计算模块 | P | Raspberry Pi CM5 |
| SYS-003 | 内存/存储 | P | 4GB RAM + 32GB eMMC候选 |
| PWR-001 | 电源输入 | P | USB-C 5V/5A |
| DISP-001 | 显示 | P | 1 × HDMI 2.0 |
| NET-001 | 有线网络 | P | 1 × Gigabit Ethernet |
| USB-001 | USB高速主机 | P | 2 × USB 3.0 Type-A |
| USB-002 | 下载/维护 | P | 1 × USB 2.0接口，支持CM5 USB boot |
| STO-001 | 高速存储 | P | 1 × M.2 M-Key 2230，PCIe Gen2 x1 |
| DBG-001 | 调试 | P | UART TX/RX/GND测试点 |
| CTRL-001 | 控制 | P | Power Button、nRPIBOOT跳线/测试点 |
| THM-001 | 散热 | P | SoC散热器安装空间，预留风扇接口 |
| WIR-001 | 无线 | O | 使用CM5带无线版本，不另加无线芯片 |
| GPIO-001 | 扩展GPIO | O | 首版不放40-pin排针，保留少量测试点 |
| MEC-001 | 外形 | P | 约100 × 70 mm目标，未冻结 |
| PCB-001 | PCB层数 | P | 4层优先，必要时6层；不采用10层HDI |
| PCB-002 | 阻抗 | P | 按CM5数据手册和板厂叠层计算 |

## 冻结条件

- CM5模块完整料号和采购来源确认。
- 两个100-pin连接器的配套型号、焊盘和堆叠高度确认。
- 200-pin信号映射与原厂数据手册逐项核对。
- 5V/5A供电、USB外设预算及M.2 3.3V电源完成核算。
- USB、PCIe、HDMI和Ethernet差分线阻抗由实际叠层确认。
- 接口开窗、模块天线净空、散热器和安装孔完成机械检查。
