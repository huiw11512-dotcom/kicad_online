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
| 5 | A1_RK3568_SOC.kicad_sch | RK3568 in 17 units; 636 ball positions (630 net labels + 6 NC markers) |
| 6 | A1_CPU_POWER.kicad_sch | TCS4525 CPU regulator and remote feedback |
| 7 | A1_EMMC_32GB.kicad_sch | Samsung 32GB eMMC 5.1 153-pad candidate |
| 8 | A1_BOOT_OSC_DEBUG.kicad_sch | 24MHz clock, POR, FLASH_VOL_SEL, UART2, Recovery |
| 9 | A1_LPDDR4X_2GB.kicad_sch | Micron 2GB x32 LPDDR4X, U10, 200-ball map, R40 ZQ |
| 10 | A1_SD_CARD.kicad_sch | TFP09-2-12B microSD, SDMMC0 4-bit, 22R/100R series, 7-channel ESD, 3.3V card supply and switchable VCCIO_SD |

## Libraries

Local symbol tables are `sym-lib-table`; local footprint tables are `fp-lib-table`. Local libraries:
`A1_CUSTOM.kicad_sym`, `A1_SOC.kicad_sym`, `A1_PMIC.kicad_sym`, `A1_DDR.kicad_sym`, `A1_POWER.kicad_sym`, `A1_CPU.kicad_sym`, `A1_EMMC.kicad_sym`, `A1_BOOT.kicad_sym`, `A1_IO.kicad_sym`.

Footprint libraries include `A1_DDR.pretty` and `A1_IO.pretty`.

## DDR implementation status

- U10: Micron MT53E512M32D1ZW-046B WT:B, 2GB (16Gb), x32, two x16 channels, single rank.
- DRAM symbol: 178 electrical pins (68 signal pins + 110 hidden supply/ground pins).
- Candidate footprint: 200 pads named by Micron ball coordinate; 22 NC/DNU pads are intentionally not represented as electrical symbol pins.
- Package row grid retains vacant L/M positions. Outer ball-row center distance is 13.65mm; pitch is 0.65mm. Column pitch is 0.8mm. A1 is upper-left in top view.
- 67 DRAM signal nets map to 67 RK3568 balls. Six second-rank control pins are marked no-connect.
- R40: 240Ω ±1% from ZQ0 to VDDQ (0.60V).
- Full package map: `A1_LPDDR4X_2GB_PINMAP.csv`; component list: `A1_LPDDR4X_2GB_BOM.csv`.

## microSD implementation status

- J4: XKB TFP09-2-12B, LCSC C2911421; footprint `A1_IO:TFP09-2-12B_microSD`.
- SDMMC0 4-bit mapping: D2, D3, CMD, CLK, D0, D1 and DET to RK3568.
- R50–R55: 22Ω series on DAT[3:0], CMD and CLK; R56: 100Ω series on DET.
- D20–D26: TECH PUBLIC ESD5341N, LCSC C3021106, 0.35pF typical; one per signal including DET.
- Card VDD is 3.3V through R57=0Ω; C80=10µF and C81=100nF are retained close to the socket.
- VCCIO_SD is connected to RK809-5 LDO5 / RK3568 VCCIO3 domain, for 3.3V default and 1.8V switching when SD3.0/UHS mode is negotiated.
- R58=10k pull-up for card detect. SDMMC0 DAT/CMD pull-ups use the SoC internal pulls as specified by the RK3568 Hardware Design Guide; no external pull-up array is added.
- BOM: `A1_SD_CARD_BOM.csv`.

## Static audit results

- Nine hierarchical child schematic files are linked from the root sheet.
- All child schematic pages checked so far pass source-level balanced S-expression checks.
- U7 RK3568 has 17 units; all 636 ball positions are represented (630 net labels + 6 NC markers).
- U8 TCS4525 symbol and candidate footprint: 20 balls each.
- U9 eMMC symbol and candidate footprint: 153 balls each.
- U10 DRAM footprint: 200 pads; pin map: 200 ball rows.
- microSD connector footprint: 13 pads (9 signal/contact pins + 4 shell tabs), with seven ESD positions.
- `fp-lib-table` includes local `A1_DDR.pretty` and `A1_IO.pretty` libraries.

Static source parsing is not an authoritative KiCad ERC/DRC. Native KiCad CLI is not available in the current execution environment, so **native KiCad load, ERC, netlist and DRC have not been run**.

## Remaining minimum Linux-boot requirements

- Confirm exact Rockchip-approved LPDDR4X MPN/template/DDR BIN pairing and WDQS requirement.
- Complete USB download/recovery and USB2/USB3 host/device interfaces.
- Complete Gigabit Ethernet PHY/RJ45, HDMI/display, Wi-Fi/BT, audio and 40-pin GPIO as required by the minimum feature set.
- Confirm all vendor package pad and paste patterns, sourcing availability, thermal and power startup.
- Complete PCB layout using the matched Rockchip DDR template and board-house impedance stackup.
