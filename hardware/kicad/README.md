# KiCad Linux MiniHost A1 — Working Hardware Source

**Date:** 2026-11-16  
**Status:** partial hierarchical schematic; NOT production-ready.

Open A1.kicad_pro, then A1.kicad_sch.

## Hierarchical native schematics

The root sheet currently links **11 child sheets**.

| Sheet | File | Current content / status |
|---|---|---|
| Main | A1.kicad_sch | USB-C PD 15V/3A input, LM76005 5V Buck, hierarchical links |
| 2 | A1_RK809_PMIC.kicad_sch | RK809-5 PMIC, BUCK/LDO, RTC, input domains; EVB rail mapping still open |
| 3 | A1_DDR_POWER.kicad_sch | LPDDR4X 1.1V / 0.6V / 1.8V rail generation |
| 4 | A1_3V3_POWER.kicad_sch | Pre-PMIC TPS62132 5V→3.3V |
| 5 | A1_RK3568_SOC.kicad_sch | RK3568 in 17 units; 636 ball positions accounted for |
| 6 | A1_CPU_POWER.kicad_sch | TCS4525 CPU regulator and remote feedback; power-up and load validation open |
| 7 | A1_EMMC_32GB.kicad_sch | Samsung KLMBG2JETD-B041 32GB eMMC 5.1 candidate, 153-pad map |
| 8 | A1_BOOT_OSC_DEBUG.kicad_sch | 24MHz clock, POR, FLASH_VOL_SEL, UART2, Recovery |
| 9 | A1_LPDDR4X_2GB.kicad_sch | Micron MT53E512M32D1ZW-046B WT:B, 2GB x32, 200-ball map, R40 and R41 |
| 10 | A1_SD_CARD.kicad_sch | TFP09-2-12B microSD, SDMMC0 4-bit, series resistors and ESD |
| 11 | A1_USB_PORTS.kicad_sch | One USB3 HOST1 Type-A and one USB-C OTG0 USB2 recovery/download connector |
| 12 | A1_USB2_HOST23.kicad_sch | Two independent USB2 HOST2/HOST3 Type-A ports; TPS2553 VBUS switches, GPIO enables, 2.2Ω series resistors and ESD5341N protection |

## Rev1 DDR implementation

- U10: Micron MT53E512M32D1ZW-046B WT:B, 2GB (16Gb), x32, two x16 channels, single rank.
- DRAM symbol: 178 electrical pins (68 signal pins + 110 hidden supply/ground pins).
- Candidate footprint: 200 pads named by Micron ball coordinate; 22 NC/DNU positions are not electrical symbol pins.
- Package row grid retains vacant L/M positions. Outer ball-row center distance is 13.65mm; pitch is 0.65mm. Column pitch is 0.8mm. A1 is upper-left in top view.
- 67 DRAM signal nets map to 67 RK3568 balls. Static comparison against A1_RK3568_PINNETS.csv found no ball-number mismatch or duplicate SoC ball assignment.
- R40: DRAM ZQ0 → 240Ω ±1% → VCC0V6_DDR.
- R41: RK3568 DDR_RZQ H7 → 120Ω ±1% → VCC_DDR_1V1.
- Full package map: A1_LPDDR4X_2GB_PINMAP.csv; component list: A1_LPDDR4X_2GB_BOM.csv.

The Rockchip Hardware Design Guide Rev1.2 names an SD6 template while the current rkbin configuration table lists an SD4 template. The exact template/BIN pair is not frozen.

## microSD implementation status

- J4: XKB TFP09-2-12B, LCSC C2911421; footprint A1_IO:TFP09-2-12B_microSD.
- SDMMC0 4-bit mapping: D2, D3, CMD, CLK, D0, D1 and DET to RK3568.
- R50–R55: 22Ω series on DAT[3:0], CMD and CLK; R56: 100Ω series on DET.
- D20–D26: TECH PUBLIC ESD5341N, LCSC C3021106, one per signal including DET.
- Card VDD is 3.3V through R57=0Ω; C80=10µF and C81=100nF are retained close to the socket.
- VCCIO_SD is connected to RK809-5 LDO5 / RK3568 VCCIO3 domain; 3.3V default and 1.8V UHS transition still require PMIC/DTS validation.
- BOM: A1_SD_CARD_BOM.csv.

## Static source checks completed

- Ten hierarchical child schematic files are linked from the root sheet.
- Child schematic files checked so far pass balanced S-expression checks.
- U7 RK3568 has 17 units; all 636 ball positions are represented.
- U8 TCS4525 symbol and candidate footprint: 20 balls each.
- U9 eMMC symbol and candidate footprint: 153 balls each.
- U10 DRAM footprint: 200 unique pads; pin map: 200 unique ball rows.
- DRAM pin-map-to-SoC-ball comparison: 67/67 signals found; 0 mismatches; 0 duplicate SoC balls.
- R41 SoC DDR_RZQ termination is now present in the LPDDR4X page and BOM.

Static source parsing is not an authoritative KiCad ERC/DRC. Native KiCad CLI is not available in the current execution environment, so **native KiCad load, ERC, netlist and DRC have not been run**.

## Remaining minimum Linux-boot requirements

- Confirm exact Rockchip-approved LPDDR4X MPN/template/BIN pairing and WDQS requirement.
- Validate the new USB2 HOST2/HOST3 page with native ERC/netlist, regulator GPIO device-tree mapping and hot-plug tests; also validate USB3 host and OTG0 recovery path.
- Complete Gigabit Ethernet PHY/RJ45, HDMI/display, Wi-Fi/BT and 40-pin GPIO.
- Confirm all vendor package pad/paste patterns, sourcing, thermal and power startup.
- Complete PCB layout using the confirmed Rockchip DDR template and board-house impedance stackup.
