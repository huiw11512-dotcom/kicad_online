# Linux MiniHost A1 — engineering status, 2026-11-15 (Rev 1.0)

Authoritative architecture decisions: [A1_MASTER_BASELINE_REV1.md](A1_MASTER_BASELINE_REV1.md). This status file records implementation progress only.

## Frozen product baseline

- RK3568 FCBGA636L, 4GB LPDDR4X x32 target, 32GB eMMC 5.1 target.
- HDMI 2.0a, Gigabit Ethernet, one USB3 Host1, two USB2 Host2/3, Micro-USB USB3_OTG0 service/download, Wi-Fi/BT SDIO+UART, 40-pin GPIO.
- USB-C PD 15V/3A; 15V-to-5V_SYS main converter target 5A.
- Six-layer FR-4; 85 × 56 mm outline target, not yet mechanically frozen.

## Actual KiCad implementation

| Block | State |
|---|---|
| USB-C PD input | Initial native schematic exists: HUSB238, 15V/3A request resistors, input path switch |
| 15V to 5V_SYS | Initial native schematic exists: LM76005, 5V/5A target |
| RK809-5 PMIC | Page 2 added and linked: 69-pin symbol, QFN68 candidate footprint, 53 placed symbols/components, pin map and BOM; rail mapping/land-pattern validation open |
| RK3568 SoC | Not yet placed in the root schematic |
| LPDDR4X | Not yet placed; exact part/template/BIN pairing open |
| eMMC / MicroSD | Not yet drawn |
| USB / HDMI / Ethernet / Wi-Fi / GPIO | Not yet drawn |
| PCB | No placement or routing |
| Validation | Native KiCad load, ERC, netlist, DRC and hardware bring-up not yet completed |

## Work completed in this revision

- Added native KiCad page `hardware/kicad/A1_RK809_PMIC.kicad_sch` as page 2 and linked it from the root sheet.
- Added RK809-5 69-pin symbol, 68+EP candidate QFN68 footprint, pin map and PMIC BOM.
- Implemented VCC input bypass, four active buck stages, LDO/SWOUT bypass, VDC divider, PWRON/SLEEP controls, open-drain pull-ups, RTC crystal and RESETB filter.
- Held BUCK3 feedback divider and PMIC-to-SoC rail allocation open pending exact LPDDR4X and full EVB cross-check.

- Created [A1_MASTER_BASELINE_REV1.md](A1_MASTER_BASELINE_REV1.md) as the single source of truth.
- Resolved conflicting project notes: Rev 1 input is 15V/3A (not 9V, 12V or 20V); USB is one USB3 Host1, two USB2 Host2/3 and a dedicated Micro-USB OTG0 download/service port.
- Confirmed from Hynetek's HUSB238 reference guide that RVSET=14kΩ requests 15V and RISET=22.6kΩ requests 3.0A.
- Checked RK3568 package information against Datasheet Rev 2.1: FCBGA636L, 19 × 19 mm, 0.65 mm pitch.
- Confirmed the three old work branches contain only .gitkeep; main remains the active project branch.

## Open engineering gates

1. SoC: validate all 636 ball names/numbers against Rockchip Datasheet Rev 2.1 and validate the BGA land pattern.
2. DDR: close exact LPDDR4X part ↔ AVL ↔ PCB template ↔ DDR BIN compatibility.
3. Power: verify RK809-5 output-to-SoC mapping against the complete EVB schematic; finalize BUCK3 divider from exact DRAM rail; verify all startup rails.
4. Power integrity: verify AO4407A transient margin, add/verify input protection, and complete LM76005 ripple/DC-bias/thermal checks.
5. Interfaces: finish pinmux, IO-bank voltage, PHY straps, USB ESD and VBUS current limits.
6. Native validation: load in KiCad, export netlist, run ERC/DRC and visually inspect every sheet.

No fabrication is authorized until these gates are closed.
