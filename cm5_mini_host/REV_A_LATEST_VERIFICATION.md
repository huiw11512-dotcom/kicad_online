# MiniHost Rev.A — latest verified engineering status

**Latest MiniHost-specific native KiCad run:** GitHub Actions run [43606720543](https://github.com/huiw11512-dotcom/kicad_online/actions/runs/43606720543), KiCad 10.0.8, 2026-11-14 22:48 China time. PCB and schematic content in the latest branch commit `aad9e7a53026f50dd344da9da240ea55c8e1c909` is unchanged from the checked board revision; the subsequent commit only adjusted the snapshot workflow.

## 1. Native KiCad result

| Check | Latest result | Meaning |
|---|---:|---|
| Schematic ERC hard errors | **0** | no ERC errors |
| Schematic ERC warnings | **41** | must still be reviewed |
| PCB DRC hard errors | **0** | no DRC items marked error |
| PCB DRC warnings | **73** | not yet clean |
| Unconnected PCB pads | **0** | all pads have KiCad net connectivity |
| Schematic-to-PCB footprint parity errors | **0** | no missing/unmatched footprint parity |
| Board footprints | 111 | |
| Routed copper segments/arcs | 2,071 | |
| Vias | 441 | |
| Recognized differential pairs | 18 | copper centerline audit only |

**Important:** 0 hard errors is a milestone, not a fabrication release. The current board is still an engineering prototype. No Gerber/NC drill release is authorized.

## 2. Remaining PCB warnings — exact report breakdown

The latest `drc.rpt` contains exactly 73 warnings:

| Warning type | Count | Next action |
|---|---:|---|
| `lib_footprint_mismatch` | 49 | compare embedded pad geometry/drills to the actual purchased part and land-pattern datasheet; do not blindly update to KiCad 10 stock libraries |
| `silk_edge_clearance` | 15 | move/trim nonessential silk that reaches the board edge |
| `silk_overlap` | 8 | resolve overlapping labels and component graphics without removing useful I/O identifiers |
| `silk_over_copper` | 1 | correct the one silk graphic intersecting a solder-mask opening |
| **Total** | **73** | |

Earlier dangling-via and isolated-copper findings are not present in this latest DRC report. The 49 footprint warnings are not equivalent to 49 broken nets; they indicate embedded-vs-library footprint differences and require per-part pad/drill review.

## 3. Remaining schematic ERC warnings — exact report breakdown

| Warning type | Count | Next action |
|---|---:|---|
| `lib_symbol_issues` | 23 | restore project-local symbol-library resolution; verify cached custom symbols are the intended symbols |
| `pin_to_pin` | 11 | inspect generic/untyped switch pins and power connections, especially SW101, SW501 and CN1 |
| `lib_symbol_mismatch` | 5 | reconcile USB-C, LIS3DH and LED cached symbols with the intended library definitions |
| `unconnected_wire_endpoint` | 1 | inspect the 2.54 mm wire stub at (180.34,119.38 mm) on the schematic |
| `footprint_link_issues` | 1 | resolve the Antmicro footprint-library reference |
| **Total** | **41** | |

Do not suppress these warning classes globally. In particular, the unconnected wire and switch pin electrical types need source-sheet review before any change.

## 4. High-speed routing inventory

Native copper centerline length differences from `differential_pairs.csv`:

| Interface | Pair | Absolute P/N trace-length difference |
|---|---|---:|
| PCIe Gen 2 | CLK | 0.010 mm |
| PCIe Gen 2 | RX | 0.000 mm |
| PCIe Gen 2 | TX | 0.010 mm |
| HDMI | CLK / D0 / D1 / D2 | 0.000 mm each |
| Ethernet | four pairs | 0.132–0.232 mm |
| USB2 host | D+/D− | 2.573 mm |
| USB-C data | D+/D− | 2.968 mm |

USB route parity was verified: J101 USB-C D+/D− and USB701 host D+/D− all match between schematic nets and actual PCB pads (4/4 groups, mismatch count 0).

These are **2D copper centerline lengths only**. They exclude via-barrel delay, pad/connector launch, ESD device discontinuity, package skew, return-path geometry, crosstalk and insertion loss. They do not prove PCIe, HDMI, Ethernet or USB compliance. USB host has one P via and two N vias; USB-C has one P via and three N vias, so via topology must be included in the next SI review.

## 5. Completed high-risk corrections

- **RJ45 J1 board-edge:** moved only the upper notch/fillet boundary +0.030 mm, preserved all copper pads/tracks/vias/nets. J1 shield pad edge clearance is now 0.2214 mm and 0.2164 mm. KiCad DRC hard errors **2→0**. Absolute routed-edge minimum is 0.20 mm for the J1 manufacturer-specific geometry; the 0.372 mm enhanced target remains elsewhere through a scoped rule. Manufacturer drawing and enclosure/overhang tolerance still require physical fit review.
- **U602:** corrected wrong Schmitt-inverter BOM entry to Diodes 74LVC1G07SE-7 (LCSC C67531), non-inverting open-drain. Correct vendor SOT-353 land pattern is 0.60 × 0.42 mm, 0.65 mm pitch; pad centers/nets/routes were preserved. KiCad local library and board now match. Actual LED behavior still needs first-power-on confirmation.
- **USB-C / USB2:** all four D+/D− schematic-to-PCB pad groups match.
- **USB host current advertisement:** Rp resistors 56 kΩ and AP22653 ILIM resistor 39 kΩ; default USB2 source-current advertisement is 500 mA. AP22653 calculated limit is approx. 0.564/0.636/0.710 A min/typ/max (excluding resistor tolerance).
- **M.2:** corrected symbol/footprint variant and reviewed mask opening; 0.16 mm nominal mask web remains subject to chosen fabricator's DFM.
- **CM5 mechanical mounting:** duplicate co-located NPTH definitions reconciled; mounting-hole geometry still needs actual enclosure/hardware validation.

## 6. Power and thermal review — not bench verified

- Main supply: design intent is USB-C PD 5 V / 5 A (25 W). Do not assume a 5 V / 3 A adapter can support full CM5 + NVMe + peripherals.
- NVMe rail: AP3441SHE-7B feedback network calculates approximately **3.327 V nominal**, regulator maximum rating 3 A. That is not a guarantee of continuous SSD current or thermal capability.
- USB2 external host port: advertised default 500 mA; current-limit threshold approximately 0.564/0.636/0.710 A.
- Preliminary budget allocates 22.62 W, or 23.67 W when reserving the switch's 0.71 A worst-case limit, leaving only 1.33 W against 25 W. These are engineering allocations, not measured load data.
- Still required: 5 V bus copper/connector temperature rise, regulator efficiency and inductor saturation, NVMe startup inrush, USB attach/detach, CM5 cold boot, sustained CPU+SSD thermal test and measured rail droop.

## 7. Remaining release gates

1. Review and resolve the 41 ERC warnings without suppressing actual electrical problems.
2. Inspect all 49 library mismatch warnings against BOM/manufacturer pad patterns; prioritize CM5 connectors, M.2, USB-C, Ethernet and power devices.
3. Clear the 24 remaining silkscreen warnings with readable reference/port labels retained.
4. Obtain the actual selected fabricator's six-layer stackup (dielectric thickness, Dk/Df, copper weights, prepreg/core, soldermask) and calculate/field-solve the differential geometries. Then validate PCIe Gen 2, HDMI, USB2 and Ethernet channels, not just lengths.
5. Complete power integrity, thermal, ESD and connector-current checks.
6. Verify CM5, M.2 SSD, RJ45 shell, fan and enclosure fit in a mechanical tolerance stack.
7. Generate Gerber, drill, paste and BOM only after all above are reviewed; run independent Gerber/NC drill DFM and prototype bring-up.

## 8. Project

- Web editor: https://designer.ziroeda.com/gh/huiw11512-dotcom/kicad_online/tree/minihost-revA/cm5_mini_host
- GitHub project: https://github.com/huiw11512-dotcom/kicad_online/tree/minihost-revA/cm5_mini_host
- Latest MiniHost KiCad audit and reports: https://github.com/huiw11512-dotcom/kicad_online/actions/runs/43606720543
- Latest snapshot workflow: https://github.com/huiw11512-dotcom/kicad_online/actions/runs/43606747974

**Bottom line:** the board now passes KiCad hard-error gates and has a complete editable Rev.A source snapshot, but the remaining 73 PCB warnings, 41 ERC warnings, SI/PI, thermal and mechanical validation mean it is not yet ready for production.
