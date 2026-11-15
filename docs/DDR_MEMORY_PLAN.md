# LPDDR4X内存方案评估

状态：容量和组织方式已形成候选方案；颗粒仍未冻结，DDR区域尚未进入原理图/PCB设计。

## 1. 容量与组织

目标：8GB LPDDR4X，64-bit总数据宽度。

候选组织：
- 2颗32Gb（每颗4GB）x32 LPDDR4X器件。
- 两颗合计64Gb = 8GB。
- 两颗x32组成64-bit数据接口，对应RK3588四通道x16的组织要求。
- Rockchip RK3588 EVB User Guide V1.0记载：EVB采用两颗4GB LPDDR4X，总容量8GB。

该组织方式是架构候选，不代表球位、Byte Lane、CA/CK分配已经确定。最终以Rockchip DDR模板和对应PinOut为准。

## 2. 候选器件

### Candidate A：Samsung K4UBE3D4AB-MGCL

| 项目 | 参数 |
|---|---|
| 制造商 | Samsung |
| 完整料号 | K4UBE3D4AB-MGCL |
| 类型 | LPDDR4X |
| 密度 | 32Gb（4GB） |
| 组织 | x32 |
| 封装 | 200-FBGA，10 × 15 mm |
| 速率等级 | 4266 Mbps |
| 工作温度 | -25°C 至 +85°C |
| LCSC | C5827966 |
| Rockchip支持状态 | DDR Support List Ver3.00中K4UBE3D4AB-MG**条目列有T/A状态；需确认对应RK3588列及完整后缀 |

评价：
- 容量、位宽和封装与双颗粒8GB方案匹配。
- LCSC/JLC目录可查到该完整料号和FBGA-200封装；实时库存、交期和批次仍需下单前核实。
- T/A不是量产完全验证；必须完成样品板验证和PVT。

### Candidate B：Micron MT53E1G32D2FW-046

| 项目 | 参数 |
|---|---|
| 制造商 | Micron |
| 料号系列 | MT53E1G32D2FW-046 |
| 密度 | 32Gb（4GB） |
| 组织 | x32 |
| 封装 | 200-ball |
| 类型 | LPDDR4/LPDDR4X系列 |
| Rockchip支持状态 | Ver3.00公开表中存在T/A条目；须核对准确温度/版本后缀及LPDDR4X工作模式 |

评价：
- 可作为备选供应源。
- 必须核对实际订货后缀、速度等级、工作模式、初始化参数和可采购性。
- 未完成这些核对前不得与Candidate A直接互换。

## 3. 明确排除项

Samsung K4UBE3D4AA-MGCL不作为A1候选：
- Rockchip DDR Support List历史修订记录将K4UBE3D4AA-MG**调整为RK3588 N/A。
- 公开清单同时将该AA系列标记为EOL。
- 不得因为AA与AB前缀相似就视为兼容替代。

## 4. 设计约束

1. 取得Rockchip最新DDR Support List原始文件，并向FAE确认K4UBE3D4AB-MGCL的准确支持状态。
2. 取得对应DDR模板和Hardware Design Guide V1.3，按原厂要求保留DRAM区域的参考布局/拓扑/布线模型；这不等于复制完整EVB主板。
3. 不允许自行交换DQ、CA、CK或Byte Lane顺序。
4. 依据所选颗粒数据手册确认ZQ、ODT_CA、RESET、CKE及各电源脚要求。
5. DDR初始化bin、BL31和BSP必须与颗粒、速度和板级配置匹配。
6. 先完成颗粒选型和原厂模板核对，再生成SoC/DDR原理图和PCB。
7. DDR必须完成上电、训练日志、全容量识别和压力测试；仅通过ERC/DRC不构成验证。

## 5. 资料链接

- Rockchip DDR Support List Ver3.00（公开镜像）：https://www.scribd.com/document/1026606197/瑞芯微DDR兼容列表-2025最新版
- Samsung K4UBE3D4AB-MGCL Datasheet：https://www.ic-golden.com/wp-content/uploads/2024/07/K4UBE3D4AB-MGCL_Rev1.0-datasheet.pdf
- LCSC K4UBE3D4AB-MGCL，C5827966：https://www.lcsc.com/zh-CN/product-detail/ddr-sdram_samsung-k4ube3d4ab-mgcl_C5827966.html
- Micron MT53E1G32D2FW-046 Datasheet：https://www.uttc.com.tw/wp-content/uploads/2025/12/LPDDR4XLPDDR4-SDRAM_MT53E_Rev.-I-042023-EN_Data-sheet.pdf
