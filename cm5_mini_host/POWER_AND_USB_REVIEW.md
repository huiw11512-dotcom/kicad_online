# MiniHost Rev.A — Power and USB interface review
Date: 2026-11-14

## Source and scope

This is a netlist-grounded electrical review of the sourced **CM5 MINIMA R3** carrier, with our Rev.A repairs and USB701 A7 reroute. KiCad verification is automatic, but no board has been fabricated or bench tested.

- Upstream open hardware attribution and license: [CM5 MINIMA R3](https://github.com/piecol/CM5_MINIMA_REV3), CERN-OHL-S-2.0.
- [Raspberry Pi official CM5 datasheet, Release 3](https://pip-assets.raspberrypi.com/categories/944-raspberry-pi-compute-module-5/documents/RP-008180-DS-7-cm5-datasheet.pdf), physical pinout pages 19–22.
- [Official CM5 IO Board reference](https://www.raspberrypi.com/documentation/computers/compute-module.html#compute-module-5-io-board).
- [Diodes AP3441/L official data sheet](https://www.diodes.com/datasheet/download/AP3441.pdf).
- [Diodes AP22653 USB switch datasheet](https://www.diodes.com/part/view/AP22653).

## Confirmed netlist power interface map

| Net | Connectivity seen in exported KiCad netlist | Engineering meaning |
|---|---|---|
| +5V | J101 A4/A9/B4/B9 → Module301 pins 77/79/81/83/85/87; U702 pin 3; U701 pin 1; J601 pin 1; input capacitors | Main bus from USB-C connector to CM5, NVMe buck, USB switch, fan and other loads |
| /CC1 | J101 A5 → Module301 pin 94 | Uses CM5 on-module CC1 sink / 5 V, 5 A PD negotiations |
| /CC2 | J101 B5 → Module301 pin 96 | Uses CM5 on-module CC2 sink / 5 V, 5 A PD negotiations |
| M2_3V3 | L701 pin 2 → M.2 J701 pins 2/4/12/14/16/18/70/72/74, plus local capacitors | NVMe SSD 3.3 V after U702 buck |
| VBUS_USB2.0 | U701 pin 6 → USB701 A4/A9/B4/B9, C702/C703 | Switched 5 V USB-C host bus |
| /CM5/VBUS_EN | Module302 pin 111 → U701 pin 3 | CM5 controls USB host VBUS switch |
| /USB_C.D_P/N | J101 D+ / D− and Module302 pins 105 / 103 | Power connector J101 also has USB 2.0 data in the **corrected Rev.A schematic/PCB** |
| /CM5/USB2P.D_P/N | USB701 A6/B6, A7/B7, Module302 pins 134/136, D701 | Separate USB 2.0 host pair from the CM5 USB3-0 DP/DM pins |

**Important:** The source's first draft was internally inconsistent for J101 USB data; the repaired Rev.A grouped bus and our `verify_usb_parity.py` now confirm all four D+/D− networks match in KiCad netlist versus actual PCB pads.

### CM5 power

Official CM5 5V input specification is 4.75–5.25 V. Pins 94 and 96 are explicitly CC1 and CC2 supporting 5 V / 5 A negotiation when wired to Type-C. **Do not insert a generic CC resistor or duplicate PD sink controller without re-reviewing the on-module power architecture**.

The official CM5IO reference describes 5 V / 5 A (25 W) input or 5 V / 3 A with a strict 600 mA peripheral constraint. This carrier is NOT yet verified for the full 5 A continuous current: the USB-C connector's rated contacts, connector thermal rise, net widths, copper thickness, fuse/ESD, and layout must be checked against the fabricator's stackup and a physical load test.

### NVMe 3.3V

U702 = `AP3441SHE-7B`, a 2.7–5.5 V input, 1 MHz, **up-to-3 A** synchronous buck. 3 A is its rated output ceiling, **not the guaranteed continuous NVMe current nor the module's actual requirement**. Check the 2.2 µH L701 DCR/saturation at peak current, converter efficiency/thermal derating, startup inrush, SSD power-good behavior, output ripple and transient droop under a real NVMe workload. LCSC reference: `C2070918` (availability unverified as of current revision).

### USB701 bus switch

U701 is `AP22653W6`, active-high enable (pin 3), with current-limit and overtemperature protection; CM5 pin 111 provides VBUS_EN. Verify the limit programming resistor and enable logic electrically, and that the output capacitors comply with device/USB host inrush requirements. Actual downstream peak demand can exceed the chosen planning allocation.

## Working power envelope — **example allocation, not measured or guaranteed**

| Branch | Preliminary reserved input power |
|---|---:|
| CM5 module | 12.5 W |
| NVMe 3.3V × 1.5A with assumed 85% efficiency | 5.82 W |
| USB external 5V × 0.5A | 2.50 W |
| Fan 5V × 0.2A | 1.00 W |
| HDMI/indicators/other loads | 0.80 W |
| **Planned total** | **22.62 W** |
| **Nominal headroom vs 5V × 5A = 25W** | **2.38 W** |

These are **design allocations only**, not CM5 or SSD maximum specifications. A heavy-load CM5, an SSD drawing near the AP3441's 3 A output rating, a higher-current USB device or startup peaks can invalidate this envelope. At 5V × 3A = 15W the allocations **do not fit**; do not assume a 3A charger is sufficient for full-featured operation.

## Gates remaining before prototype order

- [ ] Confirm physical J101 Type-C part's contact current rating and pad/plating, validate combined main 5V power-copper current/temperature.
- [ ] Calculate regulator output feedback resistors and tolerances from current schematic, verify measured 3.3V and efficiency over SSD load.
- [ ] Review USB701 U701 current-limit resistor, power-on deglitch/inrush, and host port current cap.
- [ ] Test CM5 boot on known-good **USB-C PD 5V/5A source**; log 5V sag at CM5 and SSD buck at cold power-on and 100% CPU+I/O workload.
- [ ] Compute controlled impedance with real six-layer fabrication stackup, dielectric and actual copper weights; validate USB2 90Ω differential and PCIe/HDMI pair parameters.
- [ ] Review complete connector AC/DC discharge, ESD and chassis grounding.
- [ ] Clear four remaining **hard** PCB DRC mechanical/edge problems at RJ45 J1/J601/H102 based on actual manufacturer dimensions.
- [ ] Clear separate M.2 symbol/footprint parity differences; baseline CI still reports 5 footprint items.
- [ ] Close remaining KiCad 0-ERC / 4-hard-DRC state plus contextual warnings; no Gerber manufacturing release until approved.

## Related reports

`USB_REROUTE_AUDIT.md` documents 2.1738 mm shortening of USB701 A7 N return branch with 4→4 hard DRC and 0→0 disconnected pads. Cloud CI shows verified mechanical and ERC status. Board data and library snapshots remain editable on `minihost-revA`.
