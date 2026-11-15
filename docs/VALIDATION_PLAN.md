# A1载板验证计划

## 原理图检查

- CM5两个100-pin连接器的200个信号逐项与官方Pinout核对。
- 电源输入、CC1/CC2、PMIC_Enable、Power Button、nRPIBOOT和VBAT连接核对。
- USB3、USB2、PCIe、HDMI、Ethernet的差分对和控制脚核对。
- 所有未使用引脚按CM5数据手册处理。
- KiCad ERC无未解释错误。

## PCB检查

- 两个100-pin连接器位置、方向、焊盘编号和堆叠高度双重核对。
- USB3和PCIe按90Ω差分阻抗设计。
- HDMI和Ethernet按100Ω差分阻抗设计。
- 高速线下方保持连续GND参考，不跨分割或开槽。
- 5V主电源和M.2 3.3V电源按最大负载核算铜厚、线宽和温升。
- 模块天线、M.2 SSD、散热器和外壳空间检查。
- KiCad DRC无未解释错误。

## 首板测试

1. 先不插CM5，检查5V输入、短路、CC协商和外设电源。
2. 插入CM5，测量5V输入电压和启动电流。
3. UART读取启动日志。
4. eMMC启动Raspberry Pi OS 64-bit。
5. HDMI显示。
6. Ethernet链路与吞吐。
7. 两路USB3枚举和持续传输。
8. USB2下载/恢复模式。
9. M.2 NVMe PCIe Gen2 x1枚举、读写和温升。
10. 风扇、按键、无线和长时间稳定性测试。

ERC/DRC通过不等于首板功能通过。每项测试记录板卡版本、CM5料号、系统版本、仪器和结果。
