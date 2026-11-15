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
| 9 | A1_LPDDR4X_2GB.kicad_sch | Micron 2GB x32 LPDDR4X, U10, 200-ball map, R40 ZQ |

## Libraries

Local symbol tables are `sym-lib-table`; local footprint tables are `fp-lib-table`. Local libraries:
`A1_CUSTOM.kicad_sym`, `A1_SOC.kicad_sym`, `A1_PMIC.kicad_sym`, `A1_DDR.kicad_sym`, `A1_POWER.kicad_sym`, `A1_CPU.kicad_sym`, `A1_EMMC.kicad_sym`, `A1_BOOT.kicad_sym`.

## DDR implementation status

- U10: Micron MT53E512M32D1ZW-046B WT:B, 2GB (16Gb), x32, two x16 channels, single rank.
- DRAM symbol: 178 electrical pins (68 signal pins + 110 hidden supply/ground pins).
- Candidate footprint: 200 pads named by Micron ball coordinate; 22 NC/DNU pads are intentionally not represented as electrical symbol pins.
- The package row grid preserves the vacant L/M rows. Outer ball-row center distance is 13.65mm; pitch is 0.65mm. Column pitch is 0.8mm. A1 is upper-left in top view.
- 67 DRAM signal nets map to 67 RK3568 balls. Six second-rank CS1n/CKE1/ODT1_CA signals are marked no-connect.
- R40: 240Ω ±1% from ZQ0 to VDDQ (0.60V).
- Full package map: `A1_LPDDR4X_2GB_PINMAP.csv`; component list: `A1_LPDDR4X_2GB_BOM.csv`.

## Static audit results

- Eight hierarchical child schematic files are linked from the root sheet.
- All eight child pages pass source-level balanced S-expression checks.
- U7 RK3568 has 17 units and exactly 636 ball labels; all are recorded in `A1_RK3568_PINNETS.csv`.
- U8 TCS4525 symbol and candidate footprint: 20 balls each.
- U9 eMMC symbol and candidate footprint: 153 balls each.
- U10 DRAM footprint: 200 pads; pin map: 200 ball rows.
- The 67 mapped DDR signal nets are marked `DDR_BUS_MAPPED_MT53E512M32D1ZW_2GB`; six unused rank-control nets are marked `DDR_BUS_NC_SINGLE_RANK`.
- `fp-lib-table` includes the local `A1_DDR.pretty` library.

Static source parsing is not an authoritative KiCad ERC/DRC. Native KiCad CLI is not available in the current execution environment, so **native KiCad load, ERC, netlist and DRC have not been run**.

## Remaining minimum Linux-boot requirements

- Confirm the exact Rockchip-approved LPDDR4X MPN/template/DDR BIN pairing and WDQS requirement.
- Complete MicroSD, USB download/recovery, Ethernet, display, USB Host and Wi-Fi/BT.
- Confirm all vendor package pad and paste patterns, sourcing availability, thermal and power startup.
- Complete PCB layout using the matched Rockchip DDR template and board-house impedance stackup.
