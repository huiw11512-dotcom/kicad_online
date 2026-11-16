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
| 12 | A1_USB2_HOSTS.kicad_sch | Two independent USB2 HOST2/HOST3 Type-A ports; TPS2553DBVR per-port VBUS switches; ESD5341N on each D+/D− line; separate BOM and USB-A footprint |

## Rev1 DDR implementation

- U10: Micron MT53E512M32D1ZW-046B WT:B, 2GB (16Gb), x32, two x16 channels, single rank.
- DRAM symbol: 178 electrical pins (68 signal pins + 110 hidden supply/ground pins).
- Candidate footprint: 200 pads named by Micron ball coordinate; 22 NC/DNU positions are not electrical symbol pins.
- Package row grid retains vacant L/M positions. Outer ball-row center distance is 13.65mm; pitch is 0.65mm. Column pitch is 0.8mm. A1 is upper-left in top view.
- 67 DRAM signal nets map to 67 RK3568 balls. Static comparison against A1_RK3568_PINNETS.csv found no ball-number mismatch or duplicate SoC ball assignment.
- R40: DRAM ZQ0 → 240Ω ±1% → VCC0V6_DDR.
- R41: RK3568 DDR_RZQ H7 → 120Ω ±1% → VCC_DDR_1V1.
- Full package map: A1_LPDDR4X_2GB_PINMAP.csv; component list: A1_LPDDR4X_2GB_BOM.csv.

Rockchip Hardware Design Guide Rev1.2 names SD6 as the LPDDR4/LPDDR4X base reference. The rkbin RK3568 table lists WDQS-capable template variants including SD4; the selected Micron MPN has no WDQS marker in the public AVL transcription, so the standard non-WDQS path is the working assumption. Exact template/BIN/frequency still requires FAE confirmation.

## microSD implementation status

- J4: XKB TFP09-2-12B, LCSC C2911421; footprint A1_IO:TFP09-2-12B_microSD.
- SDMMC0 4-bit mapping: D2, D3, CMD, CLK, D0, D1 and DET to RK3568.
- R50–R55: 22Ω series on DAT[3:0], CMD and CLK; R56: 100Ω series on DET.
- D20–D26: TECH PUBLIC ESD5341N, LCSC C3021106, one per signal including DET.
- Card VDD is supplied by RK809-5 SWOUT2 on VCC3V3_SD (sequence slot 4); R57 0Ω bypass from VCC3V3_SYS is DNP to preserve the switch. C80=10µF and C81=100nF are retained close to the socket.
- VCCIO_SD is connected to RK809-5 LDO5 / RK3568 VCCIO3 domain; 3.3V default and 1.8V UHS transition still require PMIC/DTS validation.
- BOM: A1_SD_CARD_BOM.csv.

## USB2 HOST2/HOST3 implementation

- SoC pin mapping: R1=USB2_HOST2_DM, R2=USB2_HOST2_DP; T1=USB2_HOST3_DM, T2=USB2_HOST3_DP. Four pins were previously incorrectly labeled as VDD_CPU / VDD_LOGIC_0V9 and are now corrected on the SoC sheet; the pin assignment CSV is updated.
- U12/U13: TPS2553DBVR (LCSC C55266), active-high EN tied to VCC3V3_SYS; FAULT pins intentionally NC.
- R71/R72: 43.2kΩ 1% (Yageo AF0402FR-0743K2L, LCSC C2097969). TI Table 9-2 current-limit threshold: 544.3mA minimum, 604.6mA nominal, 673.1mA maximum.
- C105/C108: 100nF input bypass; C106/C109: Panasonic 20SVPF120M 120uF 20V polymer (LCSC C186713); C107/C110: 100nF output bypass (Samsung CL05B104KO5NNNC, LCSC C1525).
- D38–D41: ESD5341N (LCSC C3021106), one device per USB2 data line. J6/J7: Ckmtw U-USBAR04P-F002 (LCSC C386736), USB-A-TH_USB-302-T footprint; pads 5/6 are grounded shell tabs. Note: C386736 is commercial grade, rated 0-50C; place away from SoC/PMIC hot spots or substitute an 0-85C part after footprint verification.
- USB2 page contains 16 component instances and 46 global labels. `A1_USB2_HOSTS_BOM.csv` records the parts. The USB2 D+/D− pairs require 90Ω differential routing and short stubs in PCB layout.
- USB2 ports are always enabled with the main 3.3V rail; Linux port power switching is not implemented in this Rev1 baseline.

## Static source checks completed

- Eleven hierarchical child schematic files are linked from the root sheet. On 2026-11-16, all child-sheet symbol instance paths and `sheet_instances` records were corrected to the full `/root-sheet-uuid/child-sheet-uuid` hierarchy path; six misassigned component paths on the 3V3 page were also corrected. Static S-expression and path checks pass; native KiCad ERC/netlist still pending.
- Child schematic files checked so far pass balanced S-expression checks, including the new USB2 HOST2/HOST3 page. The new USB2 page has 16 component instances, 46 global labels, and the full hierarchical sheet-instance path.
- U7 RK3568 has 17 units; all 636 ball positions are represented as 607 labeled nets + 29 explicit NC markers.
- U8 TCS4525 symbol and candidate footprint: 20 balls each.
- U9 eMMC symbol and candidate footprint: 153 balls each.
- U10 DRAM footprint: 200 unique pads; pin map: 200 unique ball rows.
- DRAM pin-map-to-SoC-ball comparison: 67/67 signals found; 0 mismatches; 0 duplicate SoC balls.
- R41 SoC DDR_RZQ termination is present in the LPDDR4X page and BOM.
- LPDDR4X-unused SoC pins are explicitly NC: 11 ECC pins, P8 DDR_VREFOUT and F5 (no LPDDR4 function); six single-rank control pins remain NC.

Static source parsing is not an authoritative KiCad ERC/DRC. Native KiCad CLI is not available in the current execution environment, so **native KiCad load, ERC, netlist and DRC have not been run**.

## Remaining minimum Linux-boot requirements

- Confirm exact Rockchip-approved LPDDR4X MPN/template/BIN pairing and WDQS requirement.
- Run native ERC/netlist on the USB host pages; validate VBUS inrush, thermal margin and USB2 enumeration on hardware.
- Complete Gigabit Ethernet PHY/RJ45, HDMI/display, Wi-Fi/BT and 40-pin GPIO.
- Confirm all vendor package pad/paste patterns, sourcing, thermal and power startup.
- Complete PCB layout using the confirmed Rockchip DDR template and board-house impedance stackup.
