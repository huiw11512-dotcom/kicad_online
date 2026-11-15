# Linux MiniHost A1

一块自主设计的紧凑型 ARM64 Linux 小主机载板。采用 Raspberry Pi Compute Module 5（CM5）作为计算核心，载板从空白 KiCad 工程独立设计。

**本项目自主设计的是载板（Carrier Board），不是重新设计 CM5 模块内部的 SoC、LPDDR 和 eMMC。** CPU、RAM、eMMC、无线模块和核心电源管理由官方 CM5 模块提供。我们独立完成双 100-pin 连接器、供电输入、USB、HDMI、Ethernet、NVMe、调试、PCB、外壳和生产验证。

不复制 CM5 MiniHost、CM5IO 或其他第三方载板的原理图、PCB布局和布线。官方CM5数据手册、Pinout与参考资料只用于核对接口和电气约束。

## A1基线

| 项目 | 当前基线 |
|---|---|
| 计算核心 | Raspberry Pi Compute Module 5 |
| 候选模块料号 | CM5104032 |
| CPU | Broadcom BCM2712，4 × Cortex-A76，2.4 GHz |
| 内存 | 4 GB LPDDR4X |
| 启动存储 | 32 GB eMMC |
| 无线 | 模块集成 Wi-Fi / Bluetooth |
| 有线网络 | 1 × Gigabit Ethernet |
| 显示 | 1 × HDMI 2.0 |
| USB | 2 × USB 3.0 Type-A；1 × USB 2.0 下载/维护口 |
| 扩展 | 1 × M.2 M-Key 2230，PCIe Gen 2 x1 |
| 电源 | USB-C 5 V / 5 A 输入 |
| 调试 | UART测试点、Power / Reset控制 |
| PCB | 4层优先评估；确有布线需要时再评估6层 |
| 外形 | 约100 × 70 mm初始目标，待接口和机械核对 |

模块料号、供货和价格须在下单前核实。

## 项目范围

- 自主绘制CM5模块双连接器符号与载板原理图
- 自主设计电源输入、USB供电保护、接口ESD和M.2 3.3 V供电
- 自主完成PCB布局布线、叠层、阻抗和DFM
- 自主设计外壳、安装孔、接口开窗和散热结构
- 使用Raspberry Pi OS / Debian等ARM64 Linux完成启动与功能测试

## 目录

- docs/：需求、架构、连接器、电源、资料与验证
- hardware/kicad/：KiCad原理图、PCB和项目库
- hardware/mechanical/：板框、接口位置、散热和外壳
- hardware/si_pi/：USB、PCIe、HDMI、Ethernet信号完整性
- software/linux/：启动、系统镜像和测试记录
- bom/：BOM、替代料和采购核对
- manufacturing/：叠层、Gerber、钻孔和装配资料

## 当前状态

- 项目方向：已缩减为CM5自主载板
- 计算模块：CM5104032候选，待核价和采购确认
- 连接器：双100-pin，优先核对Amphenol 10164227-1001A1RLF / 10164227-1004A1RLF
- 原理图：待建立
- PCB：待建立
- 投板状态：禁止投板，接口映射、供电和机械尚未完成核验
