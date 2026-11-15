# 项目任务书：Linux MiniHost A1

## 1. 目标

设计一块小型、低成本、可独立运行ARM64 Linux的CM5载板。优先实现稳定启动、基本显示、网络、USB和NVMe扩展，不追求接口数量和复杂度。

## 2. 设计边界

采用官方Raspberry Pi Compute Module 5（CM5）作为计算模块。模块已集成SoC、LPDDR4X、eMMC、无线模块（选购版本）和核心电源管理。

自主设计范围：
- CM5双100-pin连接器及其PCB封装
- 5V输入、USB-C供电协商、输入保护和外设供电
- USB 3.0、USB 2.0下载/维护接口
- HDMI、Gigabit Ethernet MagJack
- M.2 M-Key PCIe Gen2 x1
- Power Button、UART调试、Fan接口
- PCB、机械外壳、BOM、制造与测试

不自主设计：
- BCM2712芯片内部电路
- LPDDR4X与eMMC颗粒级布线
- CM5模块上的PMIC和无线射频电路

## 3. 首版必须实现

1. CM5模块可靠供电和启动。
2. 通过板载eMMC运行ARM64 Linux。
3. HDMI显示正常。
4. 千兆以太网正常。
5. 两路USB 3.0主机接口可用。
6. USB 2.0下载/维护通道可用。
7. M.2 NVMe PCIe Gen2 x1枚举和读写正常。
8. Power Button、UART调试和散热风扇接口可用。

## 4. 首版不做

- RK3588裸芯片主板
- 自研DDR和eMMC
- 双HDMI
- MIPI摄像头/显示屏
- PoE
- 40-pin HAT扩展排针
- 多路电源管理PMIC
- 10层HDI
- 复杂音频Codec和额外无线模块

## 5. 交付

- 完整KiCad原理图和PCB
- CM5连接器符号、封装和3D模型
- BOM及可采购型号
- 4层板叠层和阻抗说明
- ERC/DRC报告
- Gerber、钻孔、贴片坐标和装配图
- 首板启动、接口、功耗和温升测试记录
