# A1 DDR compatibility gate — Rev 0.2

**Status: OPEN — no DDR schematic or PCB routing is frozen.**

## Candidate memory

Micron **MT53E1G32D2FW-046 WT:C** is a real 32Gb LPDDR4/LPDDR4X component:
- 32Gb density = 4GB raw capacity
- x32 bus width
- 200-ball TFBGA
- 10.0 × 14.5 × 1.10mm package
- Micron lists 4266MT/s maximum data rate and 1.1V/0.6V I/O rails.

This establishes the device's published characteristics only. It does **not** establish a successful RK3568 design, production availability, or an approved PCB/BIN pairing.

## Rockchip template facts

The public Rockchip RK3568 PCB Template / DDR BIN configuration table lists these LPDDR4X candidates:
- `RK3568_Template_LP4XD200P132SD4_43x28_1600MHz`
- `RK3568_Template_LP4XD200P232DD61346_43R0x28R0_1056MHz`
- `RK3568_Template_LP4XD320P164SD6H1_46X28_1600MHz`
- `RK3568_Template_LP4XeM254P132SS61346_48R6x33R0_2666Mbps`

Rockchip's Hardware Design Guide V1.2 also shows a 200-ball x32 LPDDR4/LPDDR4X compatible reference design and explains the LPDDR4 vs LPDDR4X component population differences.

The template name alone is not enough to select the design. In particular, do not infer SD4/SD6, die organization, rank, WDQS requirement, or BIN compatibility from a marketing description.

## Required closure evidence

Before freezing the DDR schematic:
1. Obtain the exact Micron datasheet revision and package ball map for the full ordering code.
2. Identify the exact matching row and application notes in the current Rockchip DDR Approved Vendor List.
3. Determine whether the device requires WDQS using Rockchip's AVL application-note rules.
4. Obtain Rockchip confirmation of the matching RK3568 PCB template and DDR initialization BIN.
5. Cross-check SoC DDR PHY pin mapping, DRAM DQ byte lanes, DQS, CA, CK, CS, RESET, ZQ, ODT and all power pins against the selected template.
6. Verify VDD1, VDD2, VDDQ and RK3568 DDRPHY rails against the exact Micron datasheet and Rockchip reference design.
7. Record the exact BIN filename, version, supported frequency and bootloader integration path.
8. Only then release DDR schematic, placement constraints and length-matching rules.

## Decision

Keep MT53E1G32D2FW-046 WT:C as the **4GB x32 candidate**, not as a frozen approved part. If the exact template/BIN pairing cannot be demonstrated, switch to a Rockchip-supported memory organization rather than forcing this part into an unverified layout.

## Primary references

- Micron part page: https://www.micron.com/products/memory/lpdram-components/lpddr4/part-catalog/part-detail/mt53e1g32d2fw-046-wt-c
- Rockchip template/BIN table: https://github.com/rockchip-linux/rkbin/blob/master/specific/Rockchip_Specific_PCB_Template_and_DDR_bin_Configuration_Table.md
- Rockchip RK3568 Hardware Design Guide V1.2: https://dl.xkwy2018.com/downloads/RK3568/RK356X/Hardware/Rockchip_RK3568_Hardware_Design_Guide_V1.2_EN.pdf
- Public AVL mirror (verify against current Rockchip-issued PDF): https://blog.armsom.org/articles/025-rockchip-ddr-avl/
