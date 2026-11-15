# A1电源架构 Rev 0.1

## 输入
- USB-C PD输入，目标协商9V/3A。
- HUSB238作为PD Sink控制器候选，待核对完整料号、封装、保护和采购。
- 9V经同步Buck转换为5V_SYS，设计能力目标5A。
- USB-C端配置TVS、保险/电子保险丝、过流和浪涌保护。

## 核心电源
采用RK3568官方RK809-5电源架构：
- RK809-5按原厂电源树生成VDD_LOGIC、VDD_GPU、DDR相关电源及IO/模拟电源。
- VDD_CPU采用独立高电流Buck，参考Rockchip指南中的TCS4525方案。
- LPDDR4X的VDDQ/VDD2/VDD1等依实际颗粒和原厂参考设计确定。
- HDMI PHY、USB PHY、GMAC PHY模拟电源按原厂低噪声供电和去耦方式设计。
- 24MHz主晶振、PMIC 32.768kHz RTC晶振按实际负载电容选型。

## 电源树

| 电源域 | 供电方式 | 备注 |
|---|---|---|
| 9V_IN | USB-C PD | 输入保护后进入主Buck |
| 5V_SYS | 9V转5V同步Buck | USB外设及系统电源入口 |
| VDD_CPU | 独立Buck | 参考TCS4525及原厂电源树 |
| VDD_LOGIC/GPU/NPU | RK809-5 Buck/LDO | 按原厂电源树分配 |
| DDR rails | PMIC/专用电源轨 | 由所选LPDDR4X决定 |
| 1V8/3V3 IO | PMIC或独立Buck/LDO | 按IO电压域分配 |
| PHY analog rails | 低噪声LDO/滤波 | 按原厂参考电路 |

## 约束
- RK809-5不同子型号上电时序不可混用。
- RESETn在相关电源稳定后释放。
- 不删减SoC参考设计要求的去耦电容。
- CPU、逻辑和DDR电源逐轨核算峰值电流、压降、纹波和温升。
