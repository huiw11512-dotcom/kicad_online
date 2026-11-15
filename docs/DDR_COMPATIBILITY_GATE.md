# A1 DDR compatibility gate — Rev 0.3

**Status: OPEN — 2GB single-rank candidate is now represented in the editable schematic, but the exact Rockchip template/BIN pairing is not yet released.**

## Current schematic baseline

Micron **MT53E512M32D1ZW-046B WT:B**:
- 16Gb density = 2GB raw capacity
- x32 total bus width, implemented as two x16 channels in one package
- Single die / single rank
- 200-ball TFBGA ZW, 10.0 × 14.5 × 1.05mm
- 0.8mm column pitch, 0.65mm row pitch, Ø0.40mm SMD ball pads
- Micron product data lists 4266MT/s maximum data rate and 1.1V/0.6V I/O rails; VDD1 is 1.8V.

This is a conservative 2GB first-spin baseline. It is not a claim that the board has passed DDR training or is ready for fabrication.

## Rockchip compatibility evidence

The public Rockchip RK3568 PCB Template / DDR BIN configuration table lists:
- `RK3568_Template_LP4XD200P132SD4_43x28_1600MHz`
- `RK3568_Template_LP4XD200P232DD61346_43R0x28R0_1056MHz`
- `RK3568_Template_LP4XD320P164SD6H1_46X28_1600MHz`
- `RK3568_Template_LP4XeM254P132SS61346_48R6x33R0_2666Mbps`

The public AVL mirror includes `MT53E512M32D1ZW-046 B WT:B` with a T/A entry in the RK3568 column. Treat this as a useful candidate lead only; confirm against the current Rockchip-issued Approved Vendor List and the corresponding application notes. The exact template/BIN pairing still needs Rockchip/FAE confirmation.

The previously discussed 4GB part `MT53E1G32D2FW-046 WT:C` remains an unselected alternate. The public consumer AVL row does not show the same positive RK3568 mark, so it is not used as the first-spin baseline.

## Schematic progress

- `A1_LPDDR4X_2GB.kicad_sch` adds U10 and the ZQ network.
- `A1_LPDDR4X_2GB_PINMAP.csv` contains all 200 package-ball positions.
- 67 DRAM signal nets are mapped to 67 RK3568 balls; ZQ0 uses R40 to VDDQ.
- Six RK3568 second-rank control pins (CS1n, CKE1, ODT1_CA for channels A/B) are explicitly marked NC for this single-rank device.
- DRAM supply mapping: VDD1→1.8V, VDD2→1.1V, VDDQ→0.6V, VSS→GND.
- R40: 240Ω ±1% from ZQ0 to VDDQ.

## Required closure evidence

1. Obtain current Rockchip-issued AVL and verify exact full MPN and application-note requirements.
2. Confirm `RK3568_Template_LP4XD200P132SD4_43x28_1600MHz` is the correct topology/land-pattern template for this exact 200-ball single-rank x32 part.
3. Obtain the matching RK3568 DDR initialization BIN, version, frequency and bootloader integration instructions.
4. Confirm WDQS requirement and whether a WDQS-enabled template/BIN is mandatory.
5. Cross-check all SoC/DRAM balls, byte lanes, DQS, CA, CK, CS, RESET, ZQ, ODT and power pins against the current Rockchip reference.
6. Verify Micron land pattern, mask/paste and assembly-house capability.
7. Run native KiCad ERC/netlist/DRC, then DDR training, eyescan/frequency tests if required, and memory stress tests.

## Primary references

- Micron part page: https://my.micron.com/products/memory/lpddr-components/lpddr4/part-catalog/part-detail/mt53e512m32d1zw-046bwt-b
- Micron Z42M data sheet: https://www.mouser.com/datasheet/2/671/Micron_05092023_z42m_embedded_lpddr4x_lpddr4-3175595.pdf
- Rockchip template/BIN table: https://github.com/rockchip-linux/rkbin/blob/master/specific/Rockchip_Specific_PCB_Template_and_DDR_bin_Configuration_Table.md
- Public AVL mirror (verify against current Rockchip-issued PDF): https://cseker.com/zh-cn/news/40.html
