# A1 DDR 内存方案 Rev1.0

**首板容量：2GB。状态：原理图已建立，Rockchip 模板/BIN 兼容性仍未关闭，不能投板。**

## 1. 首板选型

| 项目 | 方案 |
|---|---|
| 颗粒 | Micron MT53E512M32D1ZW-046B WT:B |
| 容量 | 16Gb = 2GB |
| 位宽 | x32（两个 x16 通道 A/B） |
| 组织 | 单颗、单 Die、Single Rank |
| 封装 | 200-ball TFBGA ZW，10.0 × 14.5 × 1.05mm |
| 球距 | 横向 0.8mm，纵向 0.65mm |
| 焊盘 | Micron 封装图指定 Ø0.40mm SMD ball pads |
| 额定速率 | 4266MT/s；实际运行速率以 Rockchip 匹配模板/BIN 为准 |
| 电源 | VDD1=1.8V；VDD2=1.1V；VDDQ=0.6V |

首板先采用 2GB 单 Die / 单 Rank，优先降低 DDR 拓扑与启动风险。4GB 候选 MT53E1G32D2FW-046 WT:C 在公开 Rockchip DDR AVL v3.01 转录中也显示 RK3568 T/A，但其 D2/FW 双 Die 组织属于独立容量版本，不能直接沿用本次 2GB 球位图和 DDR BIN。

## 2. Rockchip 基础模板与 WDQS / DDR BIN

- RK3568 Hardware Design Guide Rev1.2 §2.1.7.5 的 LPDDR4/LPDDR4X 参考设计命名为 RK3568_Template_LP4XD200P132SD6_43x28_1600MHz；将其作为首板基础模板候选。
- rockchip-linux/rkbin 的 RK3568 表列出带 WDQS 能力的模板版本集合，其中包含 SD4。该表明确说明：只有需要 WDQS 的 LPDDR4/LPDDR4X 颗粒，才使用对应的 wdqs DDR BIN。
- Rockchip 对 WDQS 需求的判断依据是 AVL Application Note [35]/[36] 或 Reference Vendor List Application Note [5]/[6]。
- 当前 2GB MPN 在公开 AVL v3.01 转录中标记 RK3568 T/A，未见 [35]/[36] 标记；目前按标准 non-WDQS 路径推进，但须以当前官方 AVL 和 FAE 确认。
- 当前公开 rkbin 仓库存在标准 BIN 候选：rk3568_ddr_1560MHz_v1.26.bin、rk3568_ddr_1332MHz_v1.26.bin、rk3568_ddr_1056MHz_v1.26.bin、rk3568_ddr_920MHz_v1.26.bin。先评估 1560MHz v1.26 与 SD6 参考布局的匹配性，不将其直接冻结为最终 BIN。
- 1560MHz v1.26 文件：https://github.com/rockchip-linux/rkbin/blob/master/bin/rk35/rk3568_ddr_1560MHz_v1.26.bin
- 未获得官方应用注释或 FAE 确认前，不使用 rk3568_ddr_XXXXMHz_wdqs_vX.XX.bin。

SD4 出现在 WDQS-capable 模板集合，不构成选定颗粒必须使用 SD4 的证据。真正未关闭的门槛是取得 SD6 基础模板文件、精确 MPN 映射、标准 DDR BIN 版本/频率和 Bootloader 集成说明。未确认前不开始 DDR 关键走线。

## 3. 原理图与球位映射

- 原理图：hardware/kicad/A1_LPDDR4X_2GB.kicad_sch
- 完整 200 球映射：hardware/kicad/A1_LPDDR4X_2GB_PINMAP.csv
- U10 封装：A1_DDR:LPDDR4X_200Ball_ZW
- 67 个 DRAM 信号连接到 RK3568 对应球位；脚本核对未发现缺失网络、球号不匹配或重复占用。
- Micron CA0..CA5→RK3568 A0..A5；CK_t/c→CLKP/CLKN；DQS_t/c→DQSxP/N；DMI→DM；CS0→CS0n；RESET_n→RESETn。
- 单 Rank 不使用 RK3568 CS1n、CKE1、ODT1_CA（A/B 通道），对应 6 个 SoC 球位标记 NC。
- DRAM 电源：VDD1→VCC1V8_DDR；VDD2→VCC_DDR_1V1；VDDQ→VCC0V6_DDR；VSS→GND。
- R40：DRAM ZQ0 至 VCC0V6_DDR，240Ω ±1%。
- R41：RK3568 DDR_RZQ H7 至 VCC_DDR_1V1，120Ω ±1%。

## 4. Footprint 静态核对

- 封装 pad 数量：200。
- 球位表行数：200。
- 缺失 pad：0；额外 pad：0；重复 pad 名称：0。
- Pad 尺寸：0.40×0.40mm。
- 列中心距：0.8mm；行中心距：0.65mm。
- 中心跨度：X=8.8mm，Y=13.65mm。
- 保留 L/M 空行位置，A1 位于顶视图左上。

以上为源文件几何核对，最终铜焊盘、阻焊开窗、钢网和装配工艺仍需按 Micron package drawing、Rockchip 模板和装配厂 DFM 确认。

## 5. 冻结条件

1. 取得 Rockchip 当前 DDR Approved Vendor List，核对完整 MPN 和应用注释。
2. 取得 SD6 基础模板文件，确认 Micron MPN-to-template 映射和标准 DDR 初始化 BIN。
3. 根据官方 AVL/FAE 确认该 MPN 不需要 WDQS，并确认标准 BIN 版本、启动频率和 Bootloader 集成方式。
4. 按正式模板完成 Byte Lane、DQS/CA/CK 时序、阻抗、过孔及长度约束。
5. 核对 Micron 封装 land pattern、钢网、阻焊和板厂装配能力。
6. 原生 KiCad ERC/Netlist/DRC 通过后，再进行 DDR Training、内存压力测试和 Linux 启动验证。

## 6. 参考资料

- Micron MT53E512M32D1ZW-046B WT:B: https://my.micron.com/products/memory/lpddr-components/lpddr4/part-catalog/part-detail/mt53e512m32d1zw-046bwt-b
- Micron Z42M datasheet Rev.I 04/2023: https://www.mouser.com/datasheet/2/671/Micron_05092023_z42m_embedded_lpddr4x_lpddr4-3175595.pdf
- Rockchip RK3568 Hardware Design Guide Rev1.2: https://dl.xkwy2018.com/downloads/RK3568/RK356X/Hardware/Rockchip_RK3568_Hardware_Design_Guide_V1.2_EN.pdf
- Rockchip DDR template/BIN table: https://github.com/rockchip-linux/rkbin/blob/master/specific/Rockchip_Specific_PCB_Template_and_DDR_bin_Configuration_Table.md
- Public transcription of Rockchip DDR AVL v3.01; verify against official current PDF: https://cseker.com/zh-cn/news/40.html
