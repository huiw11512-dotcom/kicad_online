# Linux SBC A1 — engineering status, 2026-11-15 (Rev 0.4)

## Product definition

A compact, independently designed ARM64 Linux SBC, functionally comparable in intended use to Raspberry Pi 4B. RK3568, DRAM, PMIC, eMMC and I/O devices are mounted on one PCB. It is not a CM5 carrier and is not a copy of a third-party board.

## Architecture baseline

| Block | Baseline | Status |
|---|---|---|
| SoC | Rockchip RK3568 FCBGA636L | Selected; exact purchasable ordering code still to confirm |
| RAM | 4GB LPDDR4X, x32 | Capacity fixed; Micron candidate not yet matched to exact Rockchip template/BIN |
| Boot storage | 32GB eMMC 5.1 | Candidate class; exact datasheet and package ball map open |
| Removable storage | MicroSD | Planned |
| PMIC | RK809-5 | Selected architecture; rail mapping follows RK3568 EVB power tree |
| CPU rail | Independent ≥4A dynamic Buck | TCS4525 family is candidate; exact implementation open |
| Display | 1 × HDMI 2.0a | Planned |
| Ethernet | 1 × Gigabit Ethernet | GMAC0 + external PHY candidate; PHY timing and package open |
| USB | 1 × USB3 Host + 1 × USB3 DRD fixed Host + 2 × USB2 Host | Must respect Multi-PHY resources and DTS |
| Wireless | Wi-Fi + Bluetooth module | Exact module and firmware open |
| GPIO | 40-pin header | PinMux and voltage domains open |
| Input | USB-C PD, 9V/3A target | 9V must first be converted to 5V; 27W system budget open |
| PCB | 6-layer, 1.6mm starting target | Final stackup and impedance open |
| Board size | 85 × 56mm target | Mechanical placement validation open |

## Work completed this turn

- Reviewed Rockchip RK3568 Hardware Design Guide V1.2 sections 2.1.7.5 and 2.2.2–2.2.3.
- Corrected the power plan: RK809-5 input is 2.7–5.5V, so 9V PD must not connect directly to PMIC.
- Recorded the reference PMIC power-tree mapping: BUCK1→VDD_LOGIC, BUCK2→VDD_GPU, BUCK3→VCC_DDR, BUCK4→VDD_NPU; CPU uses a separate external dynamic Buck.
- Recorded RK809-5 channel current limits, startup constraints, VCC_RTC/VCC9 requirements, FB3 setting and capacitor/inductor constraints.
- Recorded LPDDR4X-specific SoC DDR PHY rails (1.1V and 0.6V) and the separate VCC_DDR/VCC0V6_DDR networks.
- Explicitly excluded NPU from the first board's required feature set; the power and DTS treatment still needs to follow the unused-module guidance.
- Updated `docs/POWER_PLAN.md` to Rev 0.4.

## Not completed — do not claim otherwise

- No complete electrical schematic.
- No verified RK3568 636-ball symbol/footprint library release.
- No frozen DRAM part, topology, or DDR BIN.
- No completed PMIC/power schematic or exact regulator component values.
- No complete USB/HDMI/Ethernet/Wi-Fi schematics.
- No PCB placement, routing, impedance calculation, ERC/DRC, or fabrication output.
- No Linux boot test or hardware validation.

## Next engineering sequence

1. Verify exact RK3568 package ball map and KiCad symbol/footprint.
2. Close DRAM compatibility using exact Micron datasheet, Rockchip AVL row, template and BIN.
3. Transcribe the complete RK3568 EVB RK809-5 power tree into a rail-by-rail A1 allocation table, including VCC5/6/7 LDO input domains, VCC8/9, Switch1/2 and external Buck rails.
4. Close 9V-to-5V input power and total load budget.
5. Create the hierarchical schematic and validate every power domain and pin assignment.
6. Only after schematic review, start placement and DDR/high-speed PCB design.

## Release rule

No fabricated board is authorized from this status snapshot. Open items must be closed with a cited datasheet/reference-design check or measured result.
