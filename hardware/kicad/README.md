# KiCad工程目录

本目录用于从空白工程建立A1自主CM5载板。

## 首轮原理图页

1. CM5双100-pin连接器与模块接口
2. USB-C 5V输入、保护和电源分配
3. USB3双端口与USB2下载接口
4. HDMI与Ethernet MagJack
5. M.2 PCIe Gen2 x1及3.3V电源
6. Power Button、nRPIBOOT、UART、Fan和RTC

先建立CM5完整200-pin符号，并与官方Pinout逐项核对。封装优先使用官方推荐Amphenol配套连接器，实际Footprint和3D模型必须与制造商图纸核验。

禁止从第三方MiniHost工程复制原理图或PCB。
