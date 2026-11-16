# RK3568 LPDDR4X 首板模板 / DDR BIN 确认请求

**用途：** 向 Rockchip FAE 或原厂支持渠道确认 A1 Rev1 首板 DRAM 的正式模板、DDR BIN、WDQS 要求和工作频率。  
**当前状态：** 等待官方确认；本文中的 SD6 与 1560MHz v1.26 均为候选，不是已冻结配置。

## 1. 板卡与内存信息

| 项目 | 当前设计 |
|---|---|
| SoC | Rockchip RK3568，FCBGA636 |
| DRAM | Micron MT53E512M32D1ZW-046B WT:B（D8FLP） |
| 容量 | 2GB / 16Gb |
| 数据位宽 | x32，两个 x16 通道 A/B |
| Rank / Die | Single Rank / Single Die |
| 封装 | 200-ball TFBGA ZW，10.0 × 14.5mm |
| DRAM 供电 | VDD1=1.8V，VDD2=1.1V，VDDQ=0.6V |
| SoC DDR PHY 供电 | DDRPHY_VDDQ=1.1V，DDRPHY_VDDQL=0.6V |

公开 Rockchip DDR AVL v3.01 转录中，该完整 MPN 在 RK3568 栏为 T/A，未见 Application Note [35]/[36] 标记。请以当前官方 AVL 核实。

## 2. 当前参考资料与候选

- RK3568 Hardware Design Guide Rev1.2 §2.1.7.5 提及基础参考模板：RK3568_Template_LP4XD200P132SD6_43x28_1600MHz。
- rockchip-linux/rkbin 的 RK3568 WDQS-capable 模板列表中包含 SD4 系列；该表说明只有需要 WDQS 的颗粒才使用对应 WDQS DDR BIN。
- 当前公开 rkbin 仓库存在标准 BIN 候选：rk3568_ddr_1560MHz_v1.26.bin、1332MHz、1056MHz、920MHz v1.26。
- 当前初步评估顺序：先按非 WDQS 路径，评估 SD6 基础模板与 1560MHz v1.26 标准 BIN；最终以 Rockchip 确认结果为准。

## 3. 需要 Rockchip / FAE 明确答复

1. MT53E512M32D1ZW-046B WT:B（D8FLP）是否适用于 RK3568 Rev1.x 设计？当前官方 AVL 对应状态是什么？
2. 该颗粒是否不需要 WDQS？是否存在其他 Application Note 或额外时序/布线要求？
3. 对应的正式 PCB Template 是否为 RK3568_Template_LP4XD200P132SD6_43x28_1600MHz？请提供模板文件包和版本号。
4. 对应的标准 DDR 初始化 BIN 应使用哪个文件、版本和频率？rk3568_ddr_1560MHz_v1.26.bin 是否适用，还是应采用其他版本/频率？
5. 该颗粒的推荐 DDR 运行频率、ODT/驱动强度、CA/DQ/DQS 时序和长度匹配规则是什么？
6. 是否有该 MPN 对应的 RK3568 EVB 原理图、DDR Layout 参考图、阻抗/拓扑约束和 DDR Training 说明？
7. 请确认 SoC DDR_RZQ（H7）120Ω±1% 接 1.1V，以及 DRAM ZQ0 240Ω±1% 接 0.6V 的连接要求是否与该组合一致。

## 4. 当前设计中的 DDR 终端电阻

- R40：Micron U10 ZQ0 → 240Ω±1% → VCC0V6_DDR（0.6V）。
- R41：RK3568 DDR_RZQ H7 → 120Ω±1% → VCC_DDR_1V1（1.1V）。

两者分别属于 DRAM 和 SoC 侧，不可互相替代。

## 5. 参考链接

- Rockchip RK3568 Hardware Design Guide Rev1.2：https://dl.xkwy2018.com/downloads/RK3568/RK356X/Hardware/Rockchip_RK3568_Hardware_Design_Guide_V1.2_EN.pdf
- Rockchip RK3568 DDR template / BIN 表：https://github.com/rockchip-linux/rkbin/blob/master/specific/Rockchip_Specific_PCB_Template_and_DDR_bin_Configuration_Table.md
- 标准 BIN 候选：https://github.com/rockchip-linux/rkbin/blob/master/bin/rk35/rk3568_ddr_1560MHz_v1.26.bin
- Micron MT53E512M32D1ZW-046B WT:B datasheet / part page：https://my.micron.com/products/memory/lpddr-components/lpddr4/part-catalog/part-detail/mt53e512m32d1zw-046bwt-b
