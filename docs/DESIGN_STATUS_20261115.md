# Linux MiniHost A1 — Actual engineering status, 2026-11-16

Source branch: `main`. Target: independent compact RK3568 SBC for Linux, comparable in application class to Raspberry Pi 4B.

## Native KiCad sheets completed as editable drafts
- USB-C PD15V + 15V→5V main Buck: root schematic.
- RK809-5 PMIC schematic: `A1_RK809_PMIC.kicad_sch`.
- LPDDR4X DDR power rails: `A1_DDR_POWER.kicad_sch`.
- 5V→3.3V pre-PMIC Buck: `A1_3V3_POWER.kicad_sch`.
- RK3568 SoC: 17 multi-unit symbols, all 636 balls labeled: `A1_RK3568_SOC.kicad_sch`.
- Dynamic CPU Buck: TCS4525, I2C and remote feedback: `A1_CPU_POWER.kicad_sch`.
- 32GB eMMC 5.1: Samsung KLMBG2JETD-B041: `A1_EMMC_32GB.kicad_sch`.
- 24MHz oscillator, boot voltage strap, UART2, Recovery key: `A1_BOOT_OSC_DEBUG.kicad_sch`.
- LPDDR4X DRAM: Micron MT53E512M32D1ZW-046B WT:B, 2GB x32 single-rank baseline; 200-ball map, U10, ZQ resistor R40: `A1_LPDDR4X_2GB.kicad_sch`.

## DDR integration completed in the source
- 67 DRAM signal nets mapped to 67 RK3568 balls.
- Six second-rank control pins (CS1n, CKE1, ODT1_CA for channels A/B) marked NC.
- U10 supply mapping: VDD1/VDD2/VDDQ/VSS → 1.8V/1.1V/0.6V/GND.
- R40=240Ω ±1% from ZQ0 to VDDQ.
- 200-pad footprint uses the Micron 22-row ball-grid indexing, including vacant L/M rows; outer ball-row center distance is 13.65mm.

## Corrected electrical points
- RK809-5 VCC inputs receive pre-PMIC VCC3V3_SYS, not 5V_SYS.
- RK809-5 I2C, interrupt, reset and CLK32K pull-ups receive VCC3V3_PMU (3.3V), matching RK3568 PMUIO domain; CLK32K pull-up requirements should be verified against PMIC output specs.
- LPDDR4X SoC DDRPHY_VDDQ uses VCC_DDR_1V1; DDRPHY_VDDQL uses VCC0V6_DDR.
- eMMC VCCQ 1.8V and NAND VCC 3.3V separated, VDDI treated as internal reference requiring bypass.
- FLASH_VOL_SEL tied high to VCC3V3_PMU because VCCIO2 runs at 1.8V.
- RK3568 XOUT24M includes 22Ω in series; 1M feedback from XOUT to XIN.
- VDD_CPU_COM remains dedicated CPU remote-sense net.

## Engineering gates open
1. Confirm exact RK3568 PCB template, current approved-vendor entry, WDQS requirement and matching DDR initialization BIN for the 2GB DRAM.
2. Complete MicroSD, USB service/download, USB3/USB2 Host, HDMI, Gigabit Ethernet PHY/RJ45, Wi-Fi/BT, and 40-pin GPIO.
3. Confirm board power capacity and all SoC/PHY/PMIC decoupling, enable, strap and sequencing.
4. Confirm RK3568 BGA636, TCS4525 WCSP20, eMMC BGA153, DRAM BGA200 and RK809 QFN68 footprint land patterns against vendor and assembler documents.
5. Run native KiCad schematic load, ERC, full netlist comparison, PCB layout, impedance/length constraints and DRC.
6. Assemble prototype, power sequencing bring-up, DDR memory training and boot Linux.

Current release: **DESIGN IN PROGRESS; DO NOT FABRICATE.** The source has not passed native KiCad ERC or hardware validation.
