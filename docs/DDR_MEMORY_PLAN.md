# A1 DDR内存方案

状态：**2GB单颗x32方案已进入原理图；Rockchip模板/BIN匹配仍待确认，不能投板。**

## 基线选型

| 项目 | 方案 |
|---|---|
| 颗粒 | Micron MT53E512M32D1ZW-046B WT:B |
| 容量 | 16Gb = 2GB |
| 位宽 | x32（两个x16通道A/B） |
| 组织 | 单颗、单Die、Single Rank |
| 封装 | 200-ball TFBGA ZW，10.0 × 14.5 × 1.05mm |
| 球距 | 横向0.8mm，纵向0.65mm |
| 额定速率 | 4266MT/s；实际运行速率以Rockchip匹配模板/BIN为准 |
| 电源 | VDD1=1.8V；VDD2=1.1V；VDDQ=0.6V |

首版先采用2GB，优先确保Linux启动和DDR训练路径清晰。原4GB候选MT53E1G32D2FW-046 WT:C保留为后续备选，不进入首版冻结BOM。

## Rockchip模板候选

首先核验：
- RK3568_Template_LP4XD200P132SD4_43x28_1600MHz

该模板是单颗x32方向的优先核验对象，不代表已确认与上述完整料号匹配。必须取得Rockchip当前AVL、应用注释和匹配DDR BIN后才能冻结。

## 原理图与球位映射

- 原理图：`hardware/kicad/A1_LPDDR4X_2GB.kicad_sch`
- 完整200球映射：`hardware/kicad/A1_LPDDR4X_2GB_PINMAP.csv`
- U10封装：`A1_DDR:LPDDR4X_200Ball_ZW`
- 67个DRAM信号连接到RK3568对应球位；ZQ0通过R40接VDDQ。
- Micron CA0..CA5→RK3568 A0..A5；CK_t/c→CLKP/CLKN；DQS_t/c→DQSxP/N；DMI→DM；CS0→CS0n；RESET_n→RESETn。
- 单Rank不使用RK3568 CS1n、CKE1、ODT1_CA（A/B通道），对应6个SoC球位标记NC。
- R40：240Ω ±1%，ZQ0至VDDQ(0.6V)。

## 冻结条件

1. 取得Rockchip当前DDR Approved Vendor List并确认完整料号及应用注释。
2. 确认200-ball单Rank x32模板及对应DDR初始化BIN。
3. 确认是否需要WDQS及对应工具/BIN。
4. 按模板完成DDR布线拓扑、Byte Lane、DQS/CA/CK时序、阻抗、过孔及长度约束。
5. 核对Micron封装land pattern、钢网、阻焊及板厂装配能力。
6. 原生KiCad ERC/Netlist/DRC通过后，再进行DDR训练、内存压力测试和Linux启动验证。
