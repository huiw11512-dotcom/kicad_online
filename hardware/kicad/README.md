# KiCad Linux MiniHost A1 — Working Hardware Source

**Date:** 2026-11-16  
**Status:** partial schematic; NOT production-ready.

Open `A1.kicad_pro`, then `A1.kicad_sch`.

## Hierarchical native schematics

| Sheet | File | Content |
|---|---|---|
| Main | A1.kicad_sch | USB-C PD 15V/3A + LM76005 5V Buck + hierarchical links |
| 2 | A1_RK809_PMIC.kicad_sch | RK809-5 PMIC, BUCK/LDO, RTC, input domains |
| 3 | A1_DDR_POWER.kicad_sch | LPDDR4X 0.6V and 1.8V power |
| 4 | A1_3V3_POWER.kicad_sch | Pre-PMIC TPS62132 5V→3.3V |
| 5 | A1_RK3568_SOC.kicad_sch | RK3568 in 17 units; 636 ball labels |
| 6 | A1_CPU_POWER.kicad_sch | TCS4525 CPU regulator and remote feedback |
| 7 | A1_EMMC_32GB.kicad_sch | Samsung 32GB eMMC 5.1 153-pad candidate |
| 8 | A1_BOOT_OSC_DEBUG.kicad_sch | 24MHz clock, POR, FLASH_VOL_SEL, UART2, Recovery |

## Libraries

Local symbol tables are `sym-lib-table`; local footprint tables are `fp-lib-table`. Local libraries:
`A1_CUSTOM.kicad_sym`, `A1_SOC.kicad_sym`, `A1_PMIC.kicad_sym`, `A1_DDR.kicad_sym`, `A1_POWER.kicad_sym`, `A1_CPU.kicad_sym`, `A1_EMMC.kicad_sym`, `A1_BOOT.kicad_sym`.

## Static audit results

- All 7 linked child schematic files exist.
- All 7 child files parse as balanced S-expressions.
- Every placed symbol has a corresponding embedded symbol definition.
- No duplicate references across child sheets (except intentional U7 SoC multi-unit references).
- U7 RK3568 has 17 units and exactly 636 global net labels; every ball is recorded in `A1_RK3568_PINNETS.csv`.
- U8 TCS4525 symbol and candidate footprint: 20 balls each.
- U9 eMMC symbol and candidate footprint: 153 balls each.
- `sym-lib-table` was normalized to use ${KIPRJMOD} without an extra backslash.

Static source parsing is not an authoritative KiCad ERC/DRC. **Native KiCad load, ERC, netlist and DRC are not executed yet.**

## Remaining minimum Linux-boot requirements

- Exact validated LPDDR4X part and timing/template/DDR BIN pairing.
- Full DDR DQ/DQS/CA/CLK/RESET pin-to-pin mapping and PCB escape/length/impedance rules.
- Mandatory Rockchip reset/boot straps/decoupling/ESD network validation.
- USB download/recovery connector, Ethernet, display, USB Host and Wi-Fi/BT.
- Confirm all vendor package pad and paste patterns, sourcing availability, thermal and power startup.
