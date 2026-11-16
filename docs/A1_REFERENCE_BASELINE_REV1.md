# A1 Rev1 — 原厂参考设计采用边界与电路实现基线

日期：2026-11-16
状态：参考边界记录；容量和接口现状以 A1_MASTER_BASELINE_REV1.md 为准。与[A1_MASTER_BASELINE_REV1.md](A1_MASTER_BASELINE_REV1.md)冲突时，以主基线为准。

## 1. 采用的参考资料

A1不复制第三方SBC工程。SoC供电、DDR拓扑、PMIC时序、PHY参考电路属于芯片厂商定义的约束，必须以Rockchip原厂资料为基准。

| 设计块 | 采用的原厂依据 | A1使用方式 |
|---|---|---|
| RK3568 ball map | RK3568 Datasheet Rev 2.1 Table 2-1 + package drawing | 逐球映射；不可按第三方板子猜测 |
| RK3568电源树 | RK3568 Hardware Design Guide V1.2 Figure 2-62 | 按RK809-5参考方案逐网重建 |
| 上电时序 | RK3568 Hardware Design Guide V1.2 Figure 2-63 + EVB User Guide | 保持RK809-5固化时序 |
| LPDDR4X供电 | Hardware Design Guide V1.2 Figure 2-29、2-51 | PHY 1.1V/0.6V；DRAM rails按颗粒datasheet |
| LPDDR4X拓扑 | Hardware Design Guide V1.2 Figure 2-27 | 单颗32-bit DQ/CA point-to-point |
| DDR模板/BIN | rockchip-linux/rkbin Specific PCB Template and DDR BIN table | 模板和BIN成套选用；WDQS按AVL application note决定 |
| RGMII PHY | RTL8211F官方datasheet + Rockchip EVB | PHY strap、时钟延时、磁性器件完整复核 |
| CPU动态Buck | TCS4525 datasheet + Rockchip参考设计 | 仅在输入/输出/瞬态/补偿验证后使用 |

## 2. DDR设计边界

Rockchip公开 rkbin 配置表列出具有 WDQS-capable 版本的 RK3568 模板系列（不是普通基础模板的完整清单）：
- RK3568_Template_LP4XD200P132SD4_43x28_1600MHz
- RK3568_Template_LP4XD200P232DD61346_43R0x28R0_1056MHz
- RK3568_Template_LP4XD320P164SD6H1_46X28_1600MHz
- RK3568_Template_LP4XeM254P132SS61346_48R6x33R0_2666Mbps

WDQS并非所有LPDDR4X颗粒都要启用。Rockchip说明需要WDQS的器件由AVL中的Application Note [35]/[36]等标识；只有匹配相应模板后，才使用对应WDQS DDR BIN。

因此：
- A1 Rev1 首板采用 Micron MT53E512M32D1ZW-046B WT:B，2GB、x32、单 Die、单 Rank。
- 4GB MT53E1G32D2FW-046 WT:C 作为后续独立版本候选；公开 Rockchip DDR AVL v3.01 转录也显示 RK3568 T/A，但不能直接沿用首板 2GB 球位图。
- Rockchip Hardware Design Guide Rev1.2 将 SD6 列为 LPDDR4X 基础参考模板；rkbin 表中的 SD4 属于 WDQS-capable 模板集合。当前 MPN 无公开 WDQS 应用注释标记，首板按标准 non-WDQS 路径推进，正式模板/BIN 仍需 FAE 确认。
- DDR原理图必须先取得准确ball map、AVL application note、模板和DDR BIN文件名/版本。
- 若Micron候选无法闭环，优先改选Rockchip明确支持的颗粒/拓扑，不修改原厂模板去迁就颗粒。
- 参考模板文件可以作为DDR网络拓扑和布线约束来源；不能直接复制未经验证的旧版LPDDR4或DDR4电路到LPDDR4X板。

## 3. A1 Rev1接口数量最终决策

为降低首板风险，冻结为：

| 接口 | 数量 | 说明 |
|---|---:|---|
| USB 3.x Type-A | 1 | Host |
| USB 2.0 Type-A | 2 | USB2_HOST2/3 Host |
| USB-C service | 1 | USB3_OTG0_DP/DM USB2 firmware download and service |
| HDMI 2.0a | 1 | HDMI TX |
| Gigabit Ethernet | 1 | RGMII + external PHY |
| MicroSD | 1 | SDMMC0 4-bit |
| eMMC | 1 | 32GB目标，8-bit |
| Wi-Fi/BT | 1模块 | SDIO + UART |
| 40-pin GPIO | 1 | 2.54mm，PinMux确认后定义 |
| Debug UART | 1 | 3.3V TTL |
| USB-C PD | 1 | 15V/3A（45W）目标输入 |

明确删除：第二个USB3、M.2/NVMe、SATA、PCIe插槽、摄像头、DSI/LCD、音频Codec、第二网口。后续不得在Rev1擅自增加。

## 4. 主电源功率约束

- PD输入目标15V/3A，理论输入功率45W。
- 15V经过主Buck产生5V_SYS；PMIC RK809-5只能由合规2.7–5.5V电源供电。
- 45W输入不能被理解为所有外设最大负载与SoC峰值功耗可同时满足；5V_SYS输出能力必须按转换效率、SoC峰值、USB VBUS、Wi-Fi、HDMI/PHY及启动浪涌联合核算。
- 设计中应设置USB总线电流预算与限流开关，系统过载时优先限制USB外设供电。
- 12V PD未协商成功时，禁止进入满载运行；需提供欠压/过流检测和安全关机策略。

## 5. KiCad交付规则

- 每个IC必须使用经数据手册核对的符号、封装、Pin 1方向和完整pin map。
- SoC、DDR、eMMC、PMIC及高速PHY的符号和封装在核对前不得发布为可投板状态。
- 所有器件的电源引脚必须明确连接，不能仅用隐藏电源脚或泛化标签掩盖供电域。
- ERC必须解决电源输入/输出冲突、未连接关键引脚和跨页标签不匹配。
- 生成网表后，逐项核对SoC power ball、DDR DQ/DQS/CA/CK、eMMC bus、RGMII、USB和HDMI。
- 最终交付需包含KiCad原生工程、独立符号库、封装库、BOM、ERC报告、设计风险清单。

## 6. 公开参考

1. Rockchip RK3568 Hardware Design Guide V1.2:
   https://dl.xkwy2018.com/downloads/RK3568/RK356X/Hardware/Rockchip_RK3568_Hardware_Design_Guide_V1.2_EN.pdf
2. Rockchip RK3568 EVB User Guide V1.2:
   https://dl.xkwy2018.com/downloads/RK3568/RK356X/Hardware/Rockchip_RK3568_EVB_User_Guide_V1.2_EN.pdf
3. Rockchip RK3568 PinOut and reference hardware documents:
   https://github.com/hqnicolas/RK3568-hardware-design
4. Rockchip RK3568 DDR template/BIN mapping:
   https://github.com/rockchip-linux/rkbin/blob/master/specific/Rockchip_Specific_PCB_Template_and_DDR_bin_Configuration_Table.md
