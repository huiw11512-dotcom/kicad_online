# LPDDR4X 2GB memory — A1 Rev1 design note

Status: native editable schematic, 200-ball footprint, package map, DRAM ZQ0 and SoC DDR_RZQ networks added. **Not a fabrication release.**

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

The 2GB single-die/single-rank part is retained for the first spin because its package topology is simpler. The 4GB MT53E1G32D2FW-046 WT:C alternate also appears with T/A status in the public transcription of Rockchip DDR AVL v3.01 for RK3568, but it is a D2/FW dual-die package and is not the current schematic baseline; its rank organization, package map, exact template/BIN and land pattern must be verified separately.

## Schematic and mapping

- Schematic page: `A1_LPDDR4X_2GB.kicad_sch`, U10.
- Footprint: `A1_DDR.pretty/LPDDR4X_200Ball_ZW.kicad_mod`.
- Full 200-ball map: `A1_LPDDR4X_2GB_PINMAP.csv`.
- BOM: `A1_LPDDR4X_2GB_BOM.csv`.
- 67 DRAM signal nets map to 67 RK3568 balls; ZQ0 is external and does not connect to an SoC ball.
- Micron CA0..CA5 map to RK3568 A0..A5; CK_t/c map to CLKP/CLKN; DQS_t/c map to DQSxP/N; DMI maps to DM; CS0 maps to active-low CS0n; RESET_n maps to RESETn.
- Single-rank device does not use RK3568 CS1n_A/B, CKE1_A/B or ODT1_CA_A/B. These six SoC pins are marked no-connect.
- Hidden DRAM supply pins are assigned to VCC1V8_DDR, VCC_DDR_1V1, VCC0V6_DDR and GND.
- R40 is 240Ω ±1% from DRAM ZQ0 to VDDQ (0.60V), as required by Micron and Rockchip for LPDDR4X.
- R41 is 120Ω ±1% from RK3568 DDR_RZQ ball H7 to VCC_DDR_1V1 (1.1V), as required by Rockchip RK3568 Hardware Design Guide Rev1.2 §2.1.7.2. This is a separate SoC reference resistor; it must not be confused with DRAM R40.
- R41 BOM selection: YAGEO RC0402FR-07120RL, 0402, 120Ω ±1%, LCSC C114758; confirm live stock before ordering.

## Package grid and orientation

The Micron ZW package drawing defines 22 row positions: A, B, C, D, E, F, G, H, J, K, L, M, N, P, R, T, U, V, W, Y, AA and AB. Rows L and M are vacant, but their 0.65mm pitch positions must remain in the grid. The footprint therefore uses A-to-AB outer-row center spacing of 13.65mm, not a compressed 20-row array. Column groups are 1–5 and 8–12 at 0.8mm pitch. In top view, A1 is upper-left.

The 200 footprint pads are Ø0.40mm, as specified for the SMD ball pads. The mask opening, paste aperture and copper land must still be checked against the selected assembly house and the exact Rockchip reference PCB template before release.

## Rockchip template/BIN gate

The public `rockchip-linux/rkbin` configuration table lists `RK3568_Template_LP4XD200P132SD4_43x28_1600MHz` among RK3568 templates. However, the Rockchip Hardware Design Guide Rev1.2 names `RK3568_Template_LP4XD200P132SD6_43x28_1600MHz` for its LPDDR4/LPDDR4X-compatible reference circuit. The SD4/SD6 discrepancy is unresolved; neither name is frozen for PCB routing until Rockchip/FAE confirms the current template package and its exact MPN mapping. The AVL v3.01 transcription marks the selected Micron 2GB MPN T/A for RK3568; the 4GB D2FW alternate is also marked T/A. T/A is sample-tested/applicable status, not proof that this board has passed DDR training. Confirm the current official AVL, application-note flags, exact DDR BIN, WDQS requirement, frequency and bootloader integration with Rockchip/FAE.

## Validation still required

1. Confirm exact MPN and current stock/traceability with the supplier.
2. Obtain the current official Rockchip AVL and confirm the exact MPN row/application-note flags.
3. Resolve the Rockchip guide SD6 versus rkbin table SD4 template-name discrepancy and obtain the actual matching template files and DDR BIN.
4. Validate the 200-ball footprint land pattern, mask and paste against Micron and the assembly house.
5. Complete DDR byte-lane routing, impedance, topology, via and length-matching rules using the confirmed Rockchip template.
6. Run native KiCad load/ERC/netlist/DRC, then prototype DDR training and memory stress tests.

## References

- Micron part page: https://my.micron.com/products/memory/lpddr-components/lpddr4/part-catalog/part-detail/mt53e512m32d1zw-046bwt-b
- Micron Z42M data sheet: https://www.mouser.com/datasheet/2/671/Micron_05092023_z42m_embedded_lpddr4x_lpddr4-3175595.pdf
- Rockchip RK3568 PCB template / DDR BIN table: https://github.com/rockchip-linux/rkbin/blob/master/specific/Rockchip_Specific_PCB_Template_and_DDR_bin_Configuration_Table.md
- Rockchip RK3568 Hardware Design Guide Rev1.2, §§2.1.7.2, 2.1.7.3, 2.1.7.5 (SoC DDR_RZQ, LPDDR4X ZQ0, rails and template): https://dl.xkwy2018.com/downloads/RK3568/RK356X/Hardware/Rockchip_RK3568_Hardware_Design_Guide_V1.2_EN.pdf
- Public transcription of Rockchip DDR AVL v3.01 (verify against current official Rockchip PDF): https://cseker.com/zh-cn/news/40.html
- Public AVL mirror (verify against current Rockchip-issued PDF): https://cseker.com/zh-cn/news/40.html
