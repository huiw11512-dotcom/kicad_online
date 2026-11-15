# Linux SBC A1系统架构

## 计算核心
RK3568直接焊接在主板中心区域；LPDDR4X紧邻SoC并按Rockchip DDR模板放置。PMIC和CPU Buck靠近SoC电源球及输入电容，缩短电源环路。

## 存储
32GB eMMC作为默认启动盘，MicroSD作为可移动存储和恢复介质。eMMC与SDMMC按数据手册的电压域、时序和走线要求处理。

## 显示/网络/USB
- HDMI 2.0a直接从SoC HDMI TX输出。
- GMAC经RTL8211F-CG转换为RGMII PHY，再接MagJack。
- USB3 Host和USB3 DRD各驱动一个USB-A口；DRD固定Host模式。
- 两个USB2 Host分别驱动两个USB-A口。

## 无线
AP6275系列模块候选，Wi-Fi走SDIO，Bluetooth走UART，天线按模块射频参考设计布置。若无法取得稳定供货或SDK支持，切换为Rockchip SDK明确支持的其他模块。

## 供电
USB-C PD协商9V输入，主Buck产生5V_SYS；RK809-5及独立CPU Buck按官方电源树产生SoC各路电压。

## 机械
外形目标85×56mm，SoC顶部预留散热片，USB/HDMI/RJ45沿板边排布，40-pin GPIO位于长边。最终板框以连接器实物、天线净空和散热器装配为准。
