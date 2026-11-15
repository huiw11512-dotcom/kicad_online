# Linux SBC A1 项目任务书

## 目标

自主设计一块尺寸接近Raspberry Pi 4B、可独立运行ARM64 Linux的单板计算机。首版优先实现稳定启动、显示、网络、USB、无线和存储，不追求高端AI或工业接口堆叠。

## 自主设计范围

- RK3568 SoC及BGA封装
- LPDDR4X内存及DDR电源/布线
- RK809-5 PMIC和CPU核心电源
- eMMC、MicroSD和启动/恢复电路
- HDMI、USB3、USB2、千兆以太网
- Wi-Fi/BT模块及天线接口
- 40-pin GPIO、UART调试、按键
- 6层PCB、散热结构、外壳和制造资料

## 首版必须实现

1. RK3568从eMMC启动Linux。
2. 4GB RAM完整识别并通过内存压力测试。
3. HDMI显示、千兆以太网。
4. 2路USB3和2路USB2主机接口。
5. Wi-Fi和Bluetooth工作。
6. MicroSD识别及备用启动/恢复。
7. 40-pin GPIO基础功能。
8. UART调试、Reset/Recovery控制。
9. 满载运行时电源稳定、温升可接受。

## 首版不做

CM5载板、RK3588平台、M.2 NVMe、SATA、双网口、双HDMI、MIPI摄像头/显示、PoE、CAN/RS485、复杂音频Codec、10层HDI。

## 交付

完整KiCad工程、BOM、DDR模板/初始化配置说明、6层叠层与阻抗说明、ERC/DRC报告、Gerber/钻孔/贴片坐标、首板Bring-up和测试记录。
