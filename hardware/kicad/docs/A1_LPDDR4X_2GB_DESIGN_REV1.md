# LPDDR4X 2GB memory — A1 Rev1 design note

Status: native editable schematic, 200-ball footprint, package map and ZQ network added. **Not a fabrication release.**

## Selected engineering baseline

| Item | Selection |
|---|---|
| DRAM | Micron MT53E512M32D1ZW-046B WT:B |
| Density | 16Gb = 2GB |
| Organization | x32 total, two x16 channels (A/B), single rank, one die |
| Package | 200-ball TFBGA ZW, 10.0 × 14.5 × 1.05mm |
| Ball array | 0.8mm column pitch × 0.65mm row pitch; Ø0.40mm SMD ball pads |
| Rated speed | 4266MT/s per pin; actual RK3568 operating rate is set by the validated template/BIN |
| Rails | VDD1 1.8V; VDD2 1.1V; VDDQ 0.6V; VSS GND |

The 2GB baseline replaces the previously discussed 4GB x32 candidate for the first board. The 4GB MT53E1G32D2FW-046 WT:C remains an unselected alternate; it requires its own positive Rockchip MPN/template/BIN confirmation.

## Schematic and mapping

- Schematic page: `A1_LPDDR4X_2GB.kicad_sch`, U10.
- Footprint: `A1_DDR.pretty/LPDDR4X_200Ball_ZW.kicad_mod`.
- Full 200-ball map: `A1_LPDDR4X_2GB_PINMAP.csv`.
- BOM: `A1_LPDDR4X_2GB_BOM.csv`.
- 67 DRAM signal nets map to 67 RK3568 balls; ZQ0 is external and does not connect to an SoC ball.
- Micron CA0..CA5 map to RK3568 A0..A5; CK_t/c map to CLKP/CLKN; DQS_t/c map to DQSxP/N; DMI maps to DM; CS0 maps to active-low CS0n; RESET_n maps to RESETn.
- Single-rank device does not use RK3568 CS1n_A/B, CKE1_A/B or ODT1_CA_A/B. These six SoC pins are marked no-connect.
- Hidden DRAM supply pins are assigned to VCC1V8_DDR, VCC_DDR_1V1, VCC0V6_DDR and GND.
- R40 is 240Ω ±1% from ZQ0 to VDDQ (0.60V), as required by the Micron data sheet.

## Package grid and orientation

The Micron ZW package drawing defines 22 row positions: A, B, C, D, E, F, G, H, J, K, L, M, N, P, R, T, U, V, W, Y, AA and AB. Rows L and M are vacant, but their 0.65mm pitch positions must remain in the grid. The footprint therefore uses A-to-AB outer-row center spacing of 13.65mm, not a compressed 20-row array. Column groups are 1–5 and 8–12 at 0.8mm pitch. In top view, A1 is upper-left.

The 200 footprint pads are Ø0.40mm, as specified for the SMD ball pads. The mask opening, paste aperture and copper land must still be checked against the selected assembly house and the exact Rockchip reference PCB template before release.

## Rockchip template/BIN gate

The public Rockchip RK3568 template table lists `RK3568_Template_LP4XD200P132SD4_43x28_1600MHz` as the first single-device x32 template to evaluate. It is a **candidate template**, not a confirmed pairing for this exact ordering code. Obtain the current Rockchip DDR Approved Vendor List and matching DDR initialization BIN; confirm WDQS requirement, BIN version, frequency and bootloader integration with Rockchip/FAE.

## Validation still required

1. Confirm exact MPN and current stock/traceability with the supplier.
2. Confirm current Rockchip AVL row, template and DDR BIN pairing.
3. Validate the 200-ball footprint land pattern, mask and paste against Micron and the assembly house.
4. Complete DDR byte-lane routing, impedance, topology, via and length-matching rules using the matching Rockchip template.
5. Run native KiCad load/ERC/netlist/DRC, then prototype DDR training and memory stress tests.

## References

- Micron part page: https://my.micron.com/products/memory/lpddr-components/lpddr4/part-catalog/part-detail/mt53e512m32d1zw-046bwt-b
- Micron Z42M data sheet: https://www.mouser.com/datasheet/2/671/Micron_05092023_z42m_embedded_lpddr4x_lpddr4-3175595.pdf
- Rockchip RK3568 PCB template / DDR BIN table: https://github.com/rockchip-linux/rkbin/blob/master/specific/Rockchip_Specific_PCB_Template_and_DDR_bin_Configuration_Table.md
- Public AVL mirror (verify against current Rockchip-issued PDF): https://cseker.com/zh-cn/news/40.html
