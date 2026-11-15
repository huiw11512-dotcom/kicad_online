# A1高速信号与电源完整性

## 重点网络
- LPDDR4X：DQ/DQS/CA/CK/CS/RESET/ZQ，严格按Rockchip对应模板。
- USB3：Host和DRD各一组SuperSpeed差分对。
- HDMI 2.0a：TMDS差分对、DDC、HPD和CEC。
- RGMII：SoC至RTL8211F-CG，检查时钟方向、延时和长度约束。
- SDIO：SoC至Wi-Fi模块。
- eMMC：8-bit总线。

## PCB原则
- RK3568首版采用6层，L2/L5优先保持完整GND。
- DDR走线先于外围接口布线。
- 高速差分线按器件指南和实际叠层计算阻抗，不提前硬编码线宽。
- 电源轨分别进行最大负载、压降、纹波和温升核算。
- 不在DDR/高速接口下方切割参考地。
