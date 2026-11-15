# Linux SBC A1 — engineering status, 2026-11-15

## Product definition

A compact, independently designed ARM64 Linux SBC, functionally comparable in intended use to Raspberry Pi 4B. This is a monolithic SBC: RK3568, DRAM, PMIC, eMMC and I/O devices are mounted on the same PCB. It is not a CM5 carrier and is not a copy of a third-party board.

## Current architecture baseline

| Block | Current baseline | Status |
|---|---|---|
| SoC | Rockchip RK3568 FCBGA636L | Selected, procurement/variant check open |
| RAM | 4GB LPDDR4X, x32 | Capacity fixed; exact part/template/BIN open |
| Boot storage | 32GB eMMC 5.1 | Candidate class only; exact datasheet/ball map open |
| Removable storage | MicroSD | Planned |
| PMIC | RK809-5 | Candidate; exact power tree/OTP/sequence open |
| CPU rail | Dedicated high-current buck, TCS4525 family candidate | Candidate; datasheet design verification open |
| Display | 1 × HDMI 2.0a | Planned |
| Ethernet | 1 × Gigabit Ethernet | PHY and RGMII timing open |
| USB | 1 × USB3 Host + 1 × USB3 DRD fixed as Host + 2 × USB2 Host | Must respect RK3568 Multi-PHY resource sharing |
| Wireless | Wi-Fi + Bluetooth module | Exact module, firmware, antenna and pinmux open |
| GPIO | 40-pin expansion header | Pinmux and voltage domains open |
| Input | USB-C PD, 9V/3A target | PD source compatibility and power budget open |
| PCB | 6-layer, 1.6mm starting target | Final stackup and controlled impedance open |
| Board size | 85 × 56mm target | Mechanical placement validation open |

## Work completed

- Product requirements and interface scope documented.
- RK3568 selected as the first platform to evaluate.
- Initial power architecture and six-layer stackup strategy documented.
- 4GB x32 LPDDR4X capacity selected as the target.
- Public Rockchip DDR template/BIN table and Micron part characteristics reviewed.
- DDR compatibility gate added; candidate explicitly remains unapproved until the exact template/BIN match is evidenced.
- KiCad project shell created in this repository.

## Not completed — do not claim otherwise

- No complete electrical schematic.
- No verified RK3568 636-ball symbol/footprint library release.
- No frozen DRAM part, topology, or DDR BIN.
- No completed PMIC/power schematic.
- No complete USB/HDMI/Ethernet/Wi-Fi schematics.
- No PCB placement, routing, impedance calculation, ERC/DRC, or fabrication output.
- No Linux boot test or hardware validation.

## Next engineering sequence

1. Close the RK3568 package/ball-map and KiCad symbol/footprint verification.
2. Close DRAM compatibility using the exact Micron datasheet, Rockchip AVL row, template and BIN.
3. Derive the RK809-5 and CPU/DDR rail assignment from the matching official reference design.
4. Create the hierarchical schematic and validate every power domain and pin assignment.
5. Only after schematic review, start placement and DDR/high-speed PCB design.

## Release rule

No fabricated board is authorized from this status snapshot. Any item marked open must be closed with a cited datasheet/reference-design check or measured result.
