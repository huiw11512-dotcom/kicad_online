# A1连接器与关键接口计划

| Ref | 接口 | 初步规格 | 数量 | 状态 |
|---|---|---|---:|---|
| J1/J2 | CM5模块连接器 | Amphenol 10164227-1001A1RLF或10164227-1004A1RLF | 2 | 待封装与堆叠高度核验 |
| J3 | USB-C电源 | 5V/5A，CC1/CC2连接CM5协商脚 | 1 | 待选具体连接器 |
| J4 | USB-C/USB2下载 | USB2.0数据，支持nRPIBOOT下载 | 1 | 待确认角色与保护 |
| J5/J6 | USB-A | USB3.0 SuperSpeed | 2 | 待选带壳连接器 |
| J7 | HDMI | HDMI 2.0 Type-A | 1 | 待选连接器与ESD |
| J8 | Ethernet | 1:1 Gigabit MagJack | 1 | CM5内置PHY，载板接磁性RJ45 |
| J9 | M.2 | M-Key 2230，PCIe Gen2 x1 | 1 | 待核对机械高度和供电 |
| J10 | Fan | 4-pin风扇接口候选 | 1 | PWM/Tacho按模块引脚核对 |
| TP1–TPn | UART/Boot/Power | 1.27mm或测试焊盘 | 若干 | 待布局 |

## 关键注意

- CM5有两个100-pin高密度连接器，必须按官方模块Pinout建立连接器符号。
- Amphenol 10164227-1001A1RLF堆叠高度1.5mm；10164227-1004A1RLF堆叠高度4.0mm并提供约2.5mm模块下方间隙。选择前需核对连接器实物、封装、焊盘和模块机械空间。
- Ethernet使用1:1 MagJack；不额外添加外部PHY。
- PCIe仅按Gen2 x1设计，不能按Gen3要求承诺。
- USB2下载接口要能将nRPIBOOT拉低，并保证USB数据线映射正确。
