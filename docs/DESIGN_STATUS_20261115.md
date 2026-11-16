# Linux MiniHost A1 — Actual engineering status, 2026-11-16

Source branch: `main`. Target: independent compact RK3568 SBC for Linux, comparable in application class to Raspberry Pi 4B.

## Native KiCad sheets currently linked from the root
- USB-C PD15V + 15V→5V main Buck: root schematic.
- RK809-5 PMIC: `A1_RK809_PMIC.kicad_sch`.
- LPDDR4X DDR power rails: `A1_DDR_POWER.kicad_sch`.
- 5V→3.3V pre-PMIC Buck: `A1_3V3_POWER.kicad_sch`.
- RK3568 SoC: 17 multi-unit symbols, 636 unique balls; current pin map has 610 assigned nets + 26 NC. Coordinate-level audit of schematic labels vs CSV reports zero mismatches: `A1_RK3568_SOC.kicad_sch`.
- Dynamic CPU Buck: TCS4525, I2C and remote feedback: `A1_CPU_POWER.kicad_sch`.
- 32GB eMMC 5.1: Samsung KLMBG2JETD-B041: `A1_EMMC_32GB.kicad_sch`.
- 24MHz oscillator, boot voltage strap, UART2, Recovery key: `A1_BOOT_OSC_DEBUG.kicad_sch`.
- LPDDR4X DRAM: Micron MT53E512M32D1ZW-046B WT:B, 2GB x32 single-rank baseline, 200-ball map, U10, R40: `A1_LPDDR4X_2GB.kicad_sch`.
- microSD: XKB TFP09-2-12B, 4-bit SDMMC0, ESD, series resistors and card detect: `A1_SD_CARD.kicad_sch`. Card VDD is from RK809 SWOUT2; R57 0Ω bypass is DNP.

- USB2 HOST2/HOST3: `A1_USB2_HOSTS.kicad_sch`; SoC R1/R2/T1/T2 now carry the matching D−/D+ labels. Four misplaced labels formerly on K17/K18/M12/M17 power balls were corrected to VDD_CPU/VDD_LOGIC_0V9; no-connect markers removed from R1/R2/T1/T2.
- Ethernet: preliminary RTL8211F-CG + HR911130A page exists at `A1_ETHERNET.kicad_sch`; pin/strap/power/RGMII validation remains open.
- Wi-Fi/BT pinmux: provisional AP6275S allocation uses SDMMC2 M0 (VCCIO6, 1.8V) and UART8 M0 (VCCIO4, 1.8V); module page, clocks and wake controls remain open.

## DDR integration
- 67 DRAM signal nets mapped to 67 RK3568 balls.
- Six second-rank controls (CS1n, CKE1, ODT1_CA for A/B) marked NC.
- U10 supplies: VDD1/VDD2/VDDQ/VSS → 1.8V/1.1V/0.6V/GND.
- R40=240Ω ±1% from ZQ0 to VDDQ.
- 200-pad footprint retains vacant L/M rows; outer ball-row center distance is 13.65mm.

## microSD integration
- J4 TFP09-2-12B; pinout 1 DAT2, 2 DAT3, 3 CMD, 4 VDD, 5 CLK, 6 VSS, 7 DAT0, 8 DAT1, 9 CD; shell pads 10 tied to GND.
- SDMMC0_D[3:0], CMD, CLK and DET are connected to the RK3568 ball map.
- R50–R55=22Ω series on DAT[3:0], CMD, CLK; R56=100Ω series on DET.
- D20–D26 ESD5341N, LCSC C3021106, 0.35pF typical, one at each signal near socket.
- Card VDD=3.3V from RK809-5 SWOUT2 (VCC3V3_SD); R57=0Ω bypass from VCC3V3_SYS is DNP. C80=10µF and C81=100nF are local bypass.
- VCCIO_SD connects to RK809-5 LDO5 / RK3568 VCCIO3; default 3.3V and switched to 1.8V for SD3.0/UHS operation.
- R58=10k card-detect pull-up to VCCIO_SD. DAT/CMD pulls use RK3568 internal pulls per hardware guide.

## Corrected electrical points
- RK809-5 VCC inputs receive pre-PMIC VCC3V3_SYS, not 5V_SYS.
- RK809-5 I2C, interrupt, reset and CLK32K pull-ups receive VCC3V3_PMU (3.3V), matching RK3568 PMUIO domain; CLK32K pull-up requirements still need PMIC output review.
- LPDDR4X SoC DDRPHY_VDDQ uses VCC_DDR_1V1; DDRPHY_VDDQL uses VCC0V6_DDR.
- eMMC VCCQ 1.8V and NAND VCC 3.3V separated; VDDI treated as internal reference requiring bypass.
- FLASH_VOL_SEL tied high to VCC3V3_PMU because VCCIO2 runs at 1.8V.
- RK3568 XOUT24M includes 22Ω in series; 1M feedback from XOUT to XIN.
- VDD_CPU_COM remains dedicated CPU remote-sense net.

## Engineering gates open
1. Confirm exact RK3568 PCB template, current approved-vendor entry, WDQS requirement and matching DDR initialization BIN for the 2GB DRAM.
2. Complete native ERC/netlist review for USB and preliminary Ethernet pages; add HDMI, Wi-Fi/BT module circuit and 40-pin GPIO. Audio codec is intentionally excluded from Rev1.
3. Confirm board power capacity and all SoC/PHY/PMIC decoupling, enable, strap and sequencing.
4. Confirm RK3568 BGA636, TCS4525 WCSP20, eMMC BGA153, DRAM BGA200, RK809 QFN68 and microSD connector footprints against vendor and assembler documents.
5. Run native KiCad schematic load, ERC, full netlist comparison, PCB layout, impedance/length constraints and DRC.
6. Assemble prototype, power sequencing bring-up, DDR training and boot Linux.

Current release: **DESIGN IN PROGRESS; DO NOT FABRICATE.** The source has not passed native KiCad ERC or hardware validation.
