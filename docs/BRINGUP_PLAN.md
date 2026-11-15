# 首板Bring-up计划

1. 不插CM5，限流检查USB-C 5V输入、CC协商和板上短路。
2. 检查5V主电源是否稳定在CM5要求范围内。
3. 检查USB-A VBUS开关、M.2 3.3V和风扇电源。
4. 安装CM5，检查连接器方向、插合和固定。
5. 通过UART观察启动日志。
6. 首次从板载eMMC启动Raspberry Pi OS 64-bit。
7. 进入系统后检查CPU、内存、eMMC和温度。
8. 逐项测试HDMI、Ethernet、USB3和NVMe。
9. 使用nRPIBOOT和USB2下载口验证恢复/重刷能力。
10. 执行CPU与NVMe联合负载，记录5V输入压降和模块温度。

首板出现启动问题时，优先检查5V压降、连接器焊接、Power Button、nRPIBOOT和UART日志，不在载板上重复设计模块内部电源。
