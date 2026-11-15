# A1验证计划

## 原理图
- RK3568全部636球位、NC、电源球、GND球和PinMux核对。
- LPDDR4X的DQ/DQS/CA/CK/CS/RESET/ZQ与模板逐项核对。
- RK809-5电源树和上电时序核对。
- eMMC、MicroSD、电压域和启动配置核对。
- USB3 Host/DRD Multi-PHY复用和USB2 Host资源核对。
- HDMI、RTL8211F、MagJack和ESD电路核对。
- Wi-Fi/BT模块电源、SDIO、UART和天线网络核对。
- KiCad ERC无未解释错误。

## PCB
- 6层叠层与阻抗计算书核对。
- DDR区域和拓扑与匹配模板对照。
- BGA逃线、过孔、焊盘和板厂工艺能力确认。
- USB3/HDMI/RGMII差分线及参考平面检查。
- SoC、PMIC、DDR电源回路和去耦位置检查。
- USB/HDMI/RJ45插拔空间、天线净空和散热器检查。
- KiCad DRC无未解释错误。

## 首板功能
1. 不装SoC前检查输入电源、短路和待机电源。
2. 限流上电，检查PMIC启动时序和RESETn。
3. UART读取BootROM/DDR训练/U-Boot日志。
4. eMMC启动Linux并识别4GB RAM。
5. HDMI、千兆网络、USB3/USB2测试。
6. Wi-Fi吞吐、Bluetooth连接测试。
7. MicroSD读写、GPIO测试。
8. CPU+DDR+网络+USB联合压力测试，记录功耗和温升。
