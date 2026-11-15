# 架构决策记录

## ADR-001：采用官方CM5计算模块

状态：A1基线选定，具体供货待核实。

候选料号：**CM5104032**
- BCM2712，4 × Cortex-A76，2.4 GHz
- 4 GB LPDDR4X
- 32 GB eMMC
- 集成Wi-Fi和Bluetooth
- 双100-pin载板连接器

官方数据手册列出的该型号对应4GB RAM、32GB eMMC和无线功能。若采购成本或供货不合适，再调整模块配置。

## ADR-002：自主设计载板，不复制现有载板

载板原理图、PCB布局布线、连接器位置、接口组合和外壳均从空白工程独立完成。官方CM5IO只作为接口与电气约束参考，不直接复制其PCB。

## ADR-003：首版只保留核心接口

- 1 × HDMI 2.0
- 1 × Gigabit Ethernet
- 2 × USB 3.0 Type-A
- 1 × USB 2.0下载/维护接口
- 1 × M.2 2230 PCIe Gen2 x1
- USB-C 5V/5A输入
- UART、Power Button、Fan接口

不做第二HDMI、MIPI、PoE、HAT、音频Codec。

## ADR-004：电源简化

CM5模块需要受控5V输入，模块内部已经集成主要电源管理。载板不再设计SoC多路PMIC电源树。

载板只负责：
- USB-C输入及5V/5A协商
- 输入保护和大电流铜箔
- USB-A端口VBUS限流开关
- M.2独立3.3V电源
- 必要的风扇电源与控制

## ADR-005：PCB采用4层优先

优先评估常规4层FR-4板，顶层布置高速接口并保持连续参考地。若CM5连接器扇出、M.2和外部接口的布线密度不允许，再升级6层。禁止预设10层HDI。

## ADR-006：Linux软件沿用官方生态

优先使用Raspberry Pi OS 64-bit或官方支持的Debian系镜像。先验证eMMC启动，再配置NVMe数据盘和外围接口。
