# Linux MiniHost A1

RK3568 ARM64 Linux SBC，目标是树莓派4B级别的接口体验和独立Linux启动能力。

## 当前KiCad工程（2026-11-16）

**已建立：** USB-C PD 15V输入、15V→5V_SYS主Buck、5V→3.3V SYS预PMIC Buck、RK809-5 PMIC、LPDDR4X 0.6V/1.8V电源、RK3568 SoC 17单元/636球、VDD_CPU独立TCS4525 Buck、32GB eMMC 5.1、24MHz晶振/复位/启动配置/恢复键/UART2调试。

**尚未完成：** 实际4GB LPDDR4X颗粒及完整布线表、DDR原厂模板和DDR BIN相容性、USB接口及下载口、HDMI、千兆PHY/RJ45、Wi-Fi/BT、MicroSD、40pin GPIO、局部电源去耦和匹配网络、PCB布局布线。

**制造状态：禁止投板。** 新符号/候选BGA封装仍需与原厂球图/land pattern核对；尚未运行原生KiCad ERC/DRC、网表验证和实际Linux启动测试。

## 打开工程

KiCad工程入口：`hardware/kicad/A1.kicad_pro`

主原理图：`hardware/kicad/A1.kicad_sch`（A2根页 + 7张子原理图）。

| 子页 | 文件 | 当前状态 |
|---|---|---|
| RK809-5 PMIC | `A1_RK809_PMIC.kicad_sch` | 69焊盘定义，输入3.3V，控制及Buck/LDO网络，待板级验证 |
| DDR_POWER | `A1_DDR_POWER.kicad_sch` | LPDDR4X 0.6V、1.8V，仍缺颗粒配套验证 |
| 3V3_POWER | `A1_3V3_POWER.kicad_sch` | 5V→VCC3V3_SYS TPS62132 |
| RK3568_SOC | `A1_RK3568_SOC.kicad_sch` | 17个符号单元全部入图，636个球位逐项建网 |
| CPU_POWER | `A1_CPU_POWER.kicad_sch` | TCS4525动态CPU Buck，反馈/使能/I2C |
| EMMC_32GB | `A1_EMMC_32GB.kicad_sch` | Samsung KLMBG2JETD-B041，153球，8bit总线，封装候选 |
| BOOT_DEBUG | `A1_BOOT_OSC_DEBUG.kicad_sch` | 24MHz、FLASH_VOL_SEL、nPOR、UART2、Recovery |

## 基线与核验

- [Rev1设计基线](docs/A1_MASTER_BASELINE_REV1.md)
- [RK3568球位连接CSV](hardware/kicad/A1_RK3568_PINNETS.csv)
- [RK3568接线审计](hardware/kicad/docs/RK3568_SOC_WIRING_AUDIT.md)
- [CPU电源设计审计](hardware/kicad/docs/A1_CPU_POWER_DESIGN_REV1.md)
- [eMMC设计审计](hardware/kicad/docs/A1_EMMC_DESIGN_REV1.md)
- [启动电路审计](hardware/kicad/docs/A1_BOOT_OSC_DEBUG_REV1.md)

主工程中只有“网络预留”的信号 **不代表** 外设已接通。必须完成真实电路并通过原生ERC/DRC才可认为工程可生产。
