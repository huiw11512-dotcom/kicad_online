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

U702 = `AP3441SHE-7B`, a 2.7–5.5 V input, 1 MHz, **up-to-3 A** synchronous buck. The existing feedback resistors are **R705 = 10 kΩ (upper) and R706 = 2.2 kΩ (lower)**, giving ideal 0.6 V × (1 + 10/2.2) = **3.327 V nominal**. With only the 0.591–0.609 V datasheet VFB spread (ignoring resistor error), the calculated output is approximately **3.277–3.377 V**. Feed-forward capacitor C707 is 4.7 nF across R705; this differs substantially in time constant from the illustrative 22 pF across 200 kΩ on the datasheet example. Do **not** change it blindly; confirm regulator loop response and ripple under real SSD load. 3 A is its rated output ceiling, **not the guaranteed continuous NVMe current nor the module's actual requirement**. Check the 2.2 µH L701 DCR/saturation at peak current, converter efficiency/thermal derating, startup inrush, SSD power-good behavior, output ripple and transient droop under a real NVMe workload. LCSC reference: `C2070918` (availability unverified as of current revision).

### USB701 bus switch

U701 is `AP22653W6`, active-high enable (pin 3), with current-limit and overtemperature protection; CM5 pin 111 provides VBUS_EN.

**Electrical update verified in native schematic, PCB and KiCad netlist:** R702 and R703 (source Rp pullups from +5V to CC1/CC2) are **56 kΩ** each, advertising the USB Type-C **default** current (500 mA for USB 2.0), instead of 22 kΩ / 1.5 A. R701 (U701 pin 5 ILIM to GND) is now **39 kΩ**, giving a design current-limit threshold min/typ/max of approximately **0.564 / 0.636 / 0.710 A** using Diodes' best-fit equations, excluding resistor tolerance. These are **current-limit thresholds**, not a certified continuous current capability.

The previous 22 kΩ/15 kΩ arrangement advertised 1.5 A while the initial illustrative power budget allocated only 0.5 A; that discrepancy is corrected for a keyboard/mouse-focused MiniHost. See [successful before/after EDA electrical checks](USB_POWER_500MA_AUDIT.md). Review USB-C source attach detection, VBUS_EN behavior and cable detach before manufacturing; Rp resistors plus a power switch are not automatically a complete Type-C source controller.

U701 output capacitor C702 = 100 µF and C703 = 10 µF, **110 µF nominal total**. The AP22653 application note depicts 120 µF output capacitance for a USB port; verify the applicable host electrical requirements, capacitor bias derating and inrush before selecting final BOM. The FAULT output is currently unconnected, so the host cannot directly log overcurrent events unless an appropriate GPIO/pull-up is added.

## Working power envelope — **example allocation, not measured or guaranteed**

| Branch | Preliminary reserved input power |
|---|---:|
| CM5 module | 12.5 W |
| NVMe 3.3V × 1.5A with assumed 85% efficiency | 5.82 W |
| USB2 Type-C externally advertised default: 5V × 0.5A | 2.50 W |
| Fan 5V × 0.2A | 1.00 W |
| HDMI/indicators/other loads | 0.80 W |
| **Planned total** | **22.62 W** |
| **Nominal headroom vs 5V × 5A = 25W** | **2.38 W** |

These are **design allocations only**, not CM5 or SSD maximum specifications. Although the USB port advertises 0.5A, the protection switch's worst-case limit can be approximately 0.71A plus resistor effects; reserve roughly **3.55W** (instead of 2.50W) for a fault/overload headroom check. At that current the illustrative total becomes **23.67W**, leaving only **1.33W** versus nominal 25W. A heavy-load CM5, an SSD drawing near the AP3441's 3 A output rating, a higher-current USB device or startup peaks can invalidate this envelope. At 5V × 3A = 15W the allocations **do not fit**; do not assume a 3A charger is sufficient for full-featured operation.

## Gates remaining before prototype order

- [ ] Confirm physical J101 Type-C part's contact current rating and pad/plating, validate combined main 5V power-copper current/temperature.
- [x] Calculate nominal AP3441 divider voltage from actual schematic (3.327V ideal); [ ] verify tolerances, measured output and efficiency over SSD load.
- [x] Rework USB2 source CC Rp and AP22653 current-limit resistor for default 500mA USB2 use; [ ] validate attach/detach, output capacitance, power-on inrush and measured current limit.
- [ ] Test CM5 boot on known-good **USB-C PD 5V/5A source**; log 5V sag at CM5 and SSD buck at cold power-on and 100% CPU+I/O workload.
- [ ] Compute controlled impedance with real six-layer fabrication stackup, dielectric and actual copper weights; validate USB2 90Ω differential and PCIe/HDMI pair parameters.
- [ ] Review complete connector AC/DC discharge, ESD and chassis grounding.
- [ ] Clear four remaining **hard** PCB DRC mechanical/edge problems at RJ45 J1/J601/H102 based on actual manufacturer dimensions.
- [x] Clear M.2 symbol/footprint parity differences and remove non-electrical PCB logo — **0 parity issues** on latest Rev.A.
- [ ] Close remaining KiCad 0-ERC / 4-hard-DRC state plus contextual warnings; no Gerber manufacturing release until approved.

## Related reports

`USB_POWER_500MA_AUDIT.md` documents the verified 22k/15k → 56k/39k USB-C host power variant and 0/4/0/0 ERC/hard-DRC/parity/unrouted status. `USB_REROUTE_AUDIT.md` documents 2.1738 mm shortening of USB701 A7 N return branch with 4→4 hard DRC and 0→0 disconnected pads. Cloud CI shows verified mechanical and ERC status. Board data and library snapshots remain editable on `minihost-revA`.
