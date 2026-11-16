# A1 DDR compatibility gate — Rev 1.0

**Status: OPEN.** The 2GB single-die x32 candidate is in the editable schematic and its ball-map source checks pass. The exact Rockchip template/BIN release is not closed.

## 1. First-spin memory decision

Micron **MT53E512M32D1ZW-046B WT:B**:

- 16Gb density = 2GB raw capacity
- x32 total bus width, implemented as two x16 channels A/B
- Single die / single rank
- 200-ball TFBGA ZW, 10.0 × 14.5 × 1.05mm
- 0.8mm column pitch, 0.65mm row pitch
- Micron package drawing specifies Ø0.40mm SMD ball pads
- DRAM rails: VDD1=1.8V, VDD2=1.1V, VDDQ=0.6V

This is the Rev1 first-spin baseline. The goal is to reduce memory topology and bring-up risk before a higher-capacity variant.

## 2. Rockchip AVL evidence

The public transcription of Rockchip DDR Approved Vendor List v3.01 shows:

- MT53E512M32D1ZW-046B WT:B (D8FLP) — T/A in the RK3568 column.
- MT53E1G32D2FW-046 WT:C (D8DVT) — also T/A in the RK3568 column.

T/A is the list's sample-tested/applicable status; it is not proof that the A1 board has trained DDR or passed mass-production qualification. Verify the full ordering code, application-note flags and status against the current official Rockchip-issued AVL before release.

The 4GB D2/FW part is a valid future alternate lead, not the current schematic baseline. Its dual-die package and rank topology require a separate package-map, template, BIN and routing review. Do not copy the 2GB single-rank map to the 4GB part.

## 3. Base template and WDQS interpretation

The earlier SD4/SD6 wording looked like a direct conflict, but the Rockchip sources describe different template contexts:

- RK3568 Hardware Design Guide Rev1.2 §2.1.7.5 names RK3568_Template_LP4XD200P132SD6_43x28_1600MHz for the LPDDR4/LPDDR4X reference circuit. Treat this as the base-template candidate for the selected x32 first-spin device.
- The RK3568 section of the current rockchip-linux/rkbin table lists template families that have WDQS-capable versions; SD4 appears in that list. The table explicitly says the WDQS DDR BINs are only for LPDDR4/LPDDR4X parts that require WDQS.
- Rockchip defines WDQS-required parts by Application Note [35]/[36] in the Approved Vendor List or [5]/[6] in the Reference Vendor List.
- The selected MT53E512M32D1ZW-046B WT:B row has T/A for RK3568 and no [35]/[36] marker in the public AVL v3.01 transcription. This points to the standard non-WDQS path, subject to confirmation against the current official list.
- The public rkbin repository currently contains standard BIN candidates including rk3568_ddr_1560MHz_v1.26.bin, rk3568_ddr_1332MHz_v1.26.bin, rk3568_ddr_1056MHz_v1.26.bin and rk3568_ddr_920MHz_v1.26.bin. The 1560MHz v1.26 binary is the first candidate to evaluate against the guide's 1600MHz reference layout; it is not yet selected or proven for this exact MPN.
- Candidate binary file: https://github.com/rockchip-linux/rkbin/blob/master/bin/rk35/rk3568_ddr_1560MHz_v1.26.bin
- Do not use rk3568_ddr_XXXXMHz_wdqs_vX.XX.bin unless the official AVL/reference list or Rockchip FAE confirms that this exact MPN requires WDQS.

The SD4 entry in the WDQS-capable template list is therefore not evidence that the selected non-WDQS Micron part should use SD4 instead of the guide's SD6 base reference. The remaining gate is to obtain the actual template package, confirm the MPN-to-template mapping, and obtain Rockchip/FAE confirmation of the standard DDR BIN version, frequency and bootloader integration.

## 4. Schematic and source-level audits

- A1_LPDDR4X_2GB.kicad_sch contains U10, DRAM ZQ0 R40 and SoC DDR_RZQ R41.
- A1_LPDDR4X_2GB_PINMAP.csv contains 200 unique package-ball rows.
- The footprint contains 200 unique pads; no missing or extra pad names against the pin map.
- Footprint pad size: 0.40 × 0.40mm; column pitch 0.8mm; row pitch 0.65mm; center spans 8.8 × 13.65mm.
- 67 DRAM signal nets map to 67 RK3568 balls. Script comparison against A1_RK3568_PINNETS.csv found 0 missing signal nets, 0 ball-number mismatches and 0 duplicate SoC ball assignments.
- Six second-rank SoC control pins (CS1n, CKE1, ODT1_CA for channels A/B) are marked no-connect for this single-rank device.
- DRAM power mapping: VDD1→1.8V; VDD2→1.1V; VDDQ→0.6V; VSS→GND.
- R40: DRAM U10 ZQ0 → 240Ω ±1% → VCC0V6_DDR.
- R41: RK3568 DDR_RZQ H7 → 120Ω ±1% → VCC_DDR_1V1.

These are source-file and mapping checks only. They are not KiCad ERC/netlist/DRC results and do not prove DDR training.

## 5. Required closure evidence

1. Obtain current official Rockchip DDR AVL and confirm exact full MPN and application-note requirements.
2. Obtain the official LPDDR4X base template package (guide reference: SD6) and confirm the exact MPN-to-template mapping.
3. Confirm the standard non-WDQS DDR BIN version, operating frequency and bootloader integration with Rockchip/FAE.
4. Confirm from the official AVL/reference list that this MPN uses the standard non-WDQS path; obtain FAE confirmation.
5. Cross-check SoC/DRAM balls, byte lanes, DQS, CA, CK, CS, RESET, ZQ, ODT and power pins against the released template.
6. Validate the 200-ball footprint land pattern, mask and paste against Micron and the assembly house.
7. Complete DDR placement/routing using the released topology and constraints.
8. Run native KiCad load/ERC/netlist/DRC, then prototype DDR training, memory stress tests and thermal tests.

## 6. FAE confirmation request

See [RK3568_DDR_FAE_REQUEST.md](RK3568_DDR_FAE_REQUEST.md) for the exact MPN, template, WDQS, BIN and frequency questions to send to Rockchip/FAE.

## 7. References

- Micron part page: https://my.micron.com/products/memory/lpddr-components/lpddr4/part-catalog/part-detail/mt53e512m32d1zw-046bwt-b
- Micron Z42M LPDDR4X/LPDDR4 datasheet, Rev.I 04/2023, Figures 5 and 9, Table 5: https://www.mouser.com/datasheet/2/671/Micron_05092023_z42m_embedded_lpddr4x_lpddr4-3175595.pdf
- Rockchip RK3568 Hardware Design Guide Rev1.2, §§2.1.7.2, 2.1.7.3, 2.1.7.5 and §3.2.3: https://dl.xkwy2018.com/downloads/RK3568/RK356X/Hardware/Rockchip_RK3568_Hardware_Design_Guide_V1.2_EN.pdf
- Rockchip template/BIN table: https://github.com/rockchip-linux/rkbin/blob/master/specific/Rockchip_Specific_PCB_Template_and_DDR_bin_Configuration_Table.md
- Public transcription of Rockchip DDR AVL v3.01; verify against official current PDF: https://cseker.com/zh-cn/news/40.html
