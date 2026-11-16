# Linux MiniHost A1 — Master Hardware Baseline Rev 1.0

**Date:** 2026-11-16  
**Status:** Rev1 design baseline for schematic development; partial native schematic; not a fabrication release.

This is the single source of truth for the Rev1 first-spin architecture. Any capacity, package, pinmux or interface change must be reflected in this file and the corresponding KiCad sheets/BOM.

## 1. Product definition

An independently designed RK3568 ARM64 Linux single-board computer. The functional target is a compact Raspberry Pi 4B-class Linux board: boot Linux from onboard eMMC, provide HDMI, Gigabit Ethernet, USB, Wi-Fi/Bluetooth and a 40-pin GPIO header. It is not a CM5 carrier and is not a copy of another SBC.

Performance note: RK3568 uses four Cortex-A55 cores; Raspberry Pi 4B uses Cortex-A72. A1 targets a similar application class and interface set, not identical CPU benchmark performance.

## 2. Rev1 first-spin architecture

| Block | Rev1 first-spin decision | Status |
|---|---|---|
| SoC | Rockchip RK3568, FCBGA636L, 19 × 19mm | Selected; ball map and land pattern still require package-level verification |
| RAM | 2GB LPDDR4X, x32, single package/single rank | Selected first-spin baseline: Micron MT53E512M32D1ZW-046B WT:B |
| RAM alternate | 4GB LPDDR4X x32 | MT53E1G32D2FW-046 WT:C retained as a separate future variant; not current schematic baseline |
| Boot storage | 32GB eMMC 5.1, 8-bit | Samsung KLMBG2JETD-B041 candidate; sourcing, package and voltage checks open |
| Removable storage | MicroSD, SDMMC0 4-bit | Schematic page added; VCCIO switching and DTS validation open |
| PMIC | RK809-5 | Selected; full EVB rail map, unused-pin treatment and startup sequence still require review |
| CPU rail | Separate dynamic Buck, TCS4525_WT candidate | Schematic added; startup timing, feedback and load validation open |
| Display | 1 × HDMI 2.0a | Native page 13 added; ERC, voltage and compliance pending |
| Ethernet | 1 × Gigabit Ethernet, GMAC0 RGMII + external PHY | Page 14 RTL8211F-CG candidate added, MagJack footprint missing, ERC pending |
| USB host | 1 × USB 3.x HOST1 Type-A + 2 × USB 2.0 HOST2/HOST3 Type-A | USB3 HOST1/OTG0 page plus separate HOST2/HOST3 page added; native ERC and PCB validation pending |
| Service/download | USB3_OTG0 DP/DM on a USB-C service connector, USB2 download/recovery mode | Connector and OTG0 USB2 path are present; verify VBUSDET, role behavior and flashing |
| Wireless | 1 soldered Wi-Fi/Bluetooth combo module, SDIO + UART | Page 15 AP6256 SDMMC2 1.8V + UART4 level shifter, power and RF pending |
| GPIO | 40-pin, 2.54mm header | Page 16: 40 pins/28 user 3.3V signals; ESD and voltage-domain signoff pending |
| Debug | 3-pin 3.3V UART + Recovery/MaskROM access | UART2 and Recovery page present; production test pads still open |
| Input | USB-C PD 15 V / 3 A (45 W) | Schematic prototype present; PDO and protection validation open |
| Main rail | 15 V_IN → 5 V_SYS, LM76005, 5A target | Schematic prototype; power/thermal/transient validation open |
| Pre-PMIC rail | 5 V_SYS → VCC3V3_SYS, TPS62132RGTT, 3.3 V / 3 A target | Schematic page added; full-load thermal/transient validation open |
| PCB | 6-layer FR-4, 1.6mm initial target | Fabricator stackup and controlled impedance still to be confirmed |
| Outline | 85 × 56mm target | Mechanical target only; freeze after connector, DDR and thermal placement |

The 2GB part is the Rev1 first-spin choice to reduce memory topology and bring-up risk. Public transcription of Rockchip DDR AVL v3.01 shows T/A for the selected 2GB part in the RK3568 column; the 4GB D2FW alternate also shows T/A. T/A is sample-tested/applicable status, not proof of A1 board-level DDR training. Confirm both rows against the current official Rockchip-issued AVL before release.

## 3. USB resource allocation

- USB3_HOST1 + MULTI_PHY1 → one USB3 Type-A host port. This is present in the current USB page.
- USB2_HOST2 → one USB2 Type-A host port. Implemented on A1_USB2_HOST23.kicad_sch with R1/R2, TPS2553 and GPIO4_C2 enable; ERC/netlist pending.
- USB2_HOST3 → one USB2 Type-A host port. Implemented on A1_USB2_HOST23.kicad_sch with T1/T2, TPS2553 and GPIO4_D2 enable; ERC/netlist pending.
- USB3_OTG0_DP/DM → USB-C service/download connector, USB2 device/recovery path. Present in the current USB page.
- OTG0 SuperSpeed MULTI_PHY0 is not allocated to a user connector in Rev1.
- USB3_OTG0_VBUSDET must be connected as required by Rockchip. Verify connector-side VBUS detection and no reverse sourcing.
- Each Type-A VBUS must have an independent current-limited load switch, connector-side ESD, enable and over-current handling. Current USB3 host uses TPS2553; the two USB2 host load switches are now drawn on the separate USB2 page; current-limit tolerance and GPIO/DTS mapping still require validation.
- Planned host VBUS budget: USB3 HOST1 0.9A + USB2 HOST2/HOST3 up to approximately 0.62A each = 2.14A; reserve 2.2A total. The 5V_SYS power budget must be rechecked with this load.

## 4. Power baseline

1. USB-C PD Sink negotiates 15V/3A. HUSB238 remains the selected controller candidate.
2. HUSB238 resistor targets from Hynetek's reference-design guide: RVSET = 14kΩ for 15V; RISET = 22.6kΩ for 3.0A. Verify against the exact controller revision and actual adapters.
3. Protected 15V_IN feeds the main synchronous Buck.
4. LM76005 is the current 5V/5A converter candidate. 5V_SYS feeds the pre-PMIC 3.3V buck, PMIC and other 5V loads. The 5V converter's 5A output limit is the binding board-level power limit (25W nominal), not the 45W PD contract.
5. The power budget must include conversion losses, SoC/DDR/PHY, Wi-Fi, HDMI, and up to 1.9A USB VBUS. USB ports must be current-limited and total load managed.
6. RK809-5 VCC1–VCC9 and VCC_RTC use VCC3V3_SYS (3.3V); VCC_SPK_HP retains a separate filtered 5V_SYS supply. Never connect 15V_IN directly to the PMIC.
7. VDD_CPU uses an independent dynamic Buck with remote feedback to VDD_CPU_COM. TCS4525_WT is a candidate, not a validated production choice.
8. RK809-5 rails and fixed power-on sequence must follow the complete RK3568 EVB reference schematic and Hardware Design Guide, not a simplified block diagram.
9. LPDDR4X SoC PHY rails and DRAM VDD1/VDD2/VDDQ are separate networks. For the selected Micron part: VDD1=1.8V, VDD2=1.1V, VDDQ=0.6V. RK3568 DDRPHY_VDDQ=1.1V and DDRPHY_VDDQL=0.6V.

### Existing input-stage review flags

- The current KiCad prototype uses AO4407A (30V VDS) as the P-MOS path switch. This is not automatically accepted for production: TVS/clamp voltage, cable/transient conditions, MOSFET SOA and thermal margin must be checked.
- LM76005 5V/5A values, inductor and capacitor bank remain provisional until TI datasheet design equations, DC-bias derating, ripple, loop stability and thermal rise are checked.
- Add/verify input fuse or eFuse, TVS, reverse-current behavior, input bulk capacitance and test points before freezing the input page.

## 5. LPDDR4X decision and hard gate

### Selected first-spin part

- Micron MT53E512M32D1ZW-046B WT:B.
- 16Gb density = 2GB raw capacity.
- x32 total bus width, two x16 channels A/B, single die, single rank.
- 200-ball TFBGA ZW, 10.0 × 14.5 × 1.05mm.
- 0.8mm column pitch, 0.65mm row pitch; Micron package drawing specifies Ø0.40mm SMD ball pads.
- DRAM rails: VDD1=1.8V, VDD2=1.1V, VDDQ=0.6V.
- Micron datasheet ZQ0 requires 240Ω ±1% to VDDQ. A1 R40 implements this.
- Rockchip RK3568 guide specifies SoC DDR_RZQ H7 with 120Ω ±1% to VCC_DDR. A1 R41 implements this separately.

### Compatibility status

- Public transcription of Rockchip DDR AVL v3.01 lists the selected 2GB MPN as T/A for RK3568.
- The 4GB MT53E1G32D2FW-046 WT:C alternate also appears T/A in the RK3568 column, but its D2/FW dual-die organization is not the current first-spin schematic.
- The public rkbin template table lists RK3568_Template_LP4XD200P132SD4_43x28_1600MHz.
- Rockchip Hardware Design Guide Rev1.2 names RK3568_Template_LP4XD200P132SD6_43x28_1600MHz for its LPDDR4/LPDDR4X-compatible reference circuit.
- This SD4/SD6 discrepancy is unresolved. Do not freeze DDR PCB placement/routing or claim template compatibility until Rockchip/FAE supplies the current exact template files, confirms the MPN mapping, and provides the matching DDR BIN.
- Confirm whether the selected MPN carries any WDQS application-note requirement in the current official AVL/reference list. Do not choose a WDQS or non-WDQS BIN by guess.

## 6. Current schematic page inventory

The KiCad root sheet currently links fifteen child pages:

1. RK809-5 PMIC
2. DDR power rails
3. Pre-PMIC 3.3V
4. RK3568 SoC, 17 units / 636 balls
5. CPU dynamic Buck
6. 32GB eMMC
7. Boot / clock / reset / UART2 / Recovery
8. LPDDR4X 2GB
9. MicroSD
10. USB3 HOST1 / USB-C OTG0 recovery
11. USB2 HOST2 / HOST3
12. HDMI TX (native KiCad page 13)
13. RTL8211F-CG Ethernet (native KiCad page 14)
14. AP6256 Wi-Fi / BT (native KiCad page 15)
15. 40-pin GPIO (native KiCad page 16)

Production test/recovery point page and electrical signoff remain outstanding. Page existence is NOT a passed ERC or design release.

## 7. Hard gates before fabrication

- Gate A — SoC: verify all 636 ball numbers/names against Rockchip RK3568 Datasheet Rev2.1; verify BGA origin, A1 orientation, pitch and land dimensions against package drawing and assembly recommendation.
- Gate B — DDR: official AVL + exact MPN + exact reference template + matching DDR BIN + WDQS status + full DQ/DQS/CA/CK/CS/RESET/ZQ/ODT mapping.
- Gate C — PMIC/power: transcribe the full EVB RK809-5 implementation pin-by-pin; verify every rail, startup sequence, current, ripple, DC drop and thermal rise.
- Gate D — interfaces: finalize pinmux, IO-bank voltages, USB Multi-PHY allocation, PHY straps, ESD and connector circuits.
- Gate E — PCB: 6-layer stackup and impedance controlled by fabricator; DDR placement/routing follows the confirmed Rockchip template; complete ERC/DRC and netlist review.

No board fabrication is authorized until all gates are closed and native KiCad ERC/DRC reports have been reviewed.

## 8. Primary references

- Rockchip RK3568 Datasheet Rev2.1 (2024-06-21): https://www.boardcon.com/download/Rockchip_RK3568_Datasheet_V2.1-20240621.pdf
- Rockchip RK3568 Hardware Design Guide Rev1.2: https://dl.xkwy2018.com/downloads/RK3568/RK356X/Hardware/Rockchip_RK3568_Hardware_Design_Guide_V1.2_EN.pdf
- Rockchip RK3568 DDR template/BIN configuration table: https://github.com/rockchip-linux/rkbin/blob/master/specific/Rockchip_Specific_PCB_Template_and_DDR_bin_Configuration_Table.md
- Public transcription of Rockchip DDR AVL v3.01; verify against official current PDF: https://cseker.com/zh-cn/news/40.html
- Hynetek HUSB238 Sink Reference Design Guide: https://en.hynetek.com/2525.html

## 9. Release status

The project has native editable hierarchical schematics and local symbols/footprints. Native KiCad 9 ERC/netlist verification has an automated GitHub Actions workflow, but no result may be claimed without checking the actual run. PCB DRC and hardware bring-up remain outstanding. Static source parsing and ball-map comparisons do not replace these checks. **Rev1 remains DESIGN-IN-PROGRESS and NOT FABRICATION READY.**
