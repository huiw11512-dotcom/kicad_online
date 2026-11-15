# KiCad工程目录 — Linux SBC A1

从空白KiCad工程创建自主RK3568单板计算机。

## 原理图分页
1. RK3568 SoC、时钟、复位、Boot配置
2. LPDDR4X 4GB及DDR电源
3. RK809-5 PMIC、VDD_CPU和电源输入
4. eMMC、MicroSD、启动与恢复
5. HDMI 2.0a
6. USB3 Host/DRD、USB2 Host及保护
7. RTL8211F-CG千兆PHY和RJ45
8. AP6275 Wi-Fi/BT模块
9. 40-pin GPIO、UART、按键、风扇

## 符号和封装
- RK3568 FCBGA636L符号按官方Pin Out生成，并按Bank/功能分页。
- BGA焊盘编号、球距、球径和禁布区必须从封装图核验。
- LPDDR封装按颗粒数据手册和Rockchip DDR模板核验。
- RK809-5、TCS4525及外部PHY使用完整制造商封装。
- 所有连接器需要3D模型和插头插拔空间检查。

不得使用CM5模块或第三方SBC工程作为本项目原理图/PCB起点。
