# CM5 MiniHost — high-speed carrier development

**Stage:** Rev.A engineering prototype derived from the attributed CM5 MINIMA reference. Native KiCad 10 schematic and PCB have been edited and cloud checked, but the board **has not been fabricated, signal-integrity validated, or released for manufacture**.

## Goal

A genuinely Linux-capable small computer using the **Raspberry Pi Compute Module 5**. Features to retain in our eventual custom revision:

- USB-C external 5 V supply and safe power sequencing
- HDMI display output
- Gigabit Ethernet
- PCIe Gen 2 ×1 to M.2 Key-M NVMe SSD
- USB 2.0 host/user interface (plus Wi-Fi/Bluetooth when the fitted CM5 supports it)
- Boot/service access, status indicators and thermal provisions

Unlike a microcontroller demo, CM5 includes CPU, RAM, and optional eMMC and can run Raspberry Pi OS.

## Origin and licensing

The starting electronic design is **CM5 MINIMA REV3** by Pierluigi Colangeli, source: https://github.com/piecol/CM5_MINIMA_REV3

Source snapshot commit: `6d77314dbbc26c8f5735add30ccb0588816cb71a`.

The original is open hardware under **CERN-OHL-S-2.0**. We retain the upstream license and identify changes in version history. Do not describe the baseline as independently designed or verified in this repository. See `SOURCE_README.md` after import.

## Manufacturing-risk BOM correction

**U602 corrected to Diodes 74LVC1G07SE-7 (JLC/LCSC C67531)** from the physically and logically incorrect SN74LVC1G14DBVR value. The existing schematic describes a non-inverting open-drain 1G07 that sinks the R605/D605 LED branch; original 1G14 was a SOT-23 Schmitt inverter, not pin/function/footprint-equivalent in practice. Both schematic P/N+Value and PCB P/N+Value fields synchronized and validated in KiCad: **ERC 0, hard DRC 2, parity 0, unconnected 0, total DRC 85 unchanged**. [U602 verified fix](U602_BOM_CORRECTION_AUDIT.md) / [root cause and remaining footprint checks](U602_COMPONENT_MISMATCH_REVIEW.md).

**Other footprint findings:** [50 mismatch summary](FOOTPRINT_MISMATCH_PAD_AUDIT.md) and [8 actual pad-by-pad comparison](EIGHT_FOOTPRINT_PAD_DELTA.md). Of the eight flagged devices, U602 had confirmed P/N/logic/package error; U1 LIS3DH and CM5 Module301 have a bottom-side coordinate-mirroring effect that must be normalized before interpreting pad offsets as routing faults; J701 difference involves alternate mounting holes. Do not automatically replace stock footprints to silence warnings.

## Latest verified board status — 2026-11-14

**Latest MiniHost-specific native KiCad 10.0.8 run:** [CI run 43606720543](https://github.com/huiw11512-dotcom/kicad_online/actions/runs/43606720543). Results: **ERC 0 errors / 41 warnings; PCB DRC 0 hard errors / 73 warnings; 0 unconnected pads; 0 schematic-to-PCB footprint parity errors.** The 73 PCB warnings are 49 embedded-vs-library footprint differences, 15 silk-edge, 8 silk-overlap and 1 silk-over-copper. They are still subject to review; no warning classes have been globally disabled.

The two RJ45 shield pad-to-edge hard errors have now been resolved by a controlled +0.030 mm notch/fillet adjustment and a manufacturer/fabricator-specific 0.20 mm J1 edge-clearance allowance, while retaining the enhanced 0.372 mm target elsewhere. U602 has also been corrected to Diodes 74LVC1G07SE-7 with its vendor SOT-353 land pattern. **The board is still not fabrication released**: ERC warnings, PCB warnings, stackup-controlled SI/PI, thermal/power and enclosure fit remain.

[Latest detailed verification and release gates](REV_A_LATEST_VERIFICATION.md) · [Latest warning-by-warning triage](DRC_WARNING_TRIAGE.md) · [Power and USB review](POWER_AND_USB_REVIEW.md).

## Rev.A completed and verified (2026-11-14)

- Reproduced actual six-layer CM5 Linux carrier in the native KiCad and web viewer.
- Repaired USB-C root bus naming and verified **4/4 D+/D− schematic-net-to-PCB-pad networks match**.
- Routed one tested USB701 A7 N backside branch from 6.4241 to 4.2503 mm copper centerline; before/after **4 → 4 hard DRC** and **0 → 0 unconnected**. This is not SI signoff.
- Recovered **8 custom PCB-embedded footprint types** into locally registered EasyEDA, Samacsys and _pico libraries, passing KiCad export/reimport pad checks.
- Reconciled the M.2 socket schematic's four nonexistent alternative mechanical pins M1..M4 against the installed 2230/2242 connector footprint.
- Adjusted **R701 15k→39k and R702/R703 22k→56k** in the native schematic and PCB for 500mA default-current USB2 host, with no DRC regression.
- Replaced the oversize rectangular RJ45 F.CrtYd with a **closed pad-aware 12-edge courtyard** in both board and project library: hard errors **4→2** and courtyard overlaps **2→0**, no electrical geometry changes.
- Reconciled conflicting duplicate CM5 NPTH drills: Module301 had **2.7 mm** holes, Module302 had **3.0 mm** holes in the very same locations. Preserved 2.7 mm M2.5 mounting holes and removed duplicate 3.0 mm holes, syncing the HSS project footprint. Native cloud report: **holes_co_located 2→0**, and **ERC/hard DRC/parity/unconnected stayed 0/2/0/0**.
- Initialized official KiCad 10 standard global footprint and symbol tables in CI to remove 65 false missing-library warnings; classified remaining DRC warnings without disabling them.
- Removed duplicate large CM5 outline from Module302/HSS only, leaving GPIO body outline and HSS connector marks: **230→198 DRC entries**.
- Properly hid 27 near-zero KiBuzzard autogenerated reference fields (without removing any visible polygon labels): **198→140 DRC entries**.
- Replaced J701 M.2's per-pad mask expansion 0.102→0.020 mm for its 69 SMT pads; copper/pitch untouched and 0.16 mm nominal mask web for a proposed 1oz green LDI process: **140→86**.
- Removed one redundant USB-C D+ via linking two same-layer F.Cu trace endpoints; net parity and DRC remained safe: **86→85**. Two other flagged vias require stub-level inspection and were retained.
- Removed one pad-free PCB-only demonstration logo footprint REF** (upstream license and attribution preserved).
- Latest *verified* electrical/DFM check after these changes: **ERC 0 errors, PCB schematic/footprint parity 0 issues, PCB unconnected 0**, with **2 remaining hard DRC errors** at the Kycon RJ45 shield solder pads and adjacent board-edge opening. Warnings still exist and require review.

## Current blockers / engineering documents

- [Verified RJ45 pad-aware courtyard audit](RJ45_COURTYARD_RESHAPE_AUDIT.md)
- [500mA USB host change audit](USB_POWER_500MA_AUDIT.md)
- [RJ45 physical conflict map](RJ45_MECHANICAL_CONFLICT_MAP.svg) and [manufacturer-grounded mechanical review](RJ45_MECHANICAL_REVIEW.md): J1 pads 15/16 board-edge hard errors resolved; physical connector/enclosure overhang still requires validation; the previous J1/J601 and J1/H102 courtyard overlaps were removed via geometry verified by KiCad
- [M.2 symbol/footprint verification](M2_SYMBOL_VARIANT_AUDIT.md) and [decorative logo cleanup verification](LOGO_CLEANUP_AUDIT.md)
- [Power, USB, CM5 5V/5A budget and startup review](POWER_AND_USB_REVIEW.md)
- [Controlled USB701 reroute and DRC no-regression](USB_REROUTE_AUDIT.md)
- [Actual KiCad 10 DRC warning triage](DRC_WARNING_TRIAGE.md) and [CM5 duplicate NPTH hole repair](CM5_ALIGNMENT_HOLE_AUDIT.md)
- [Original baseline audit — historical, before Rev.A corrections](AUDIT_2026-11-14.md)

**Next implementation gate:** resolve the two RJ45 shield solder land copper-to-edge gap violations based on Kycon's required PCB opening and full enclosure clearance; updated pad-aware courtyard eliminated two false overlaps and was verified with KiCad. Follow with exact factory stackup-controlled differential impedance, component datasheet verification, full PI/thermal checks, and a prototype bring-up plan. No release Gerbers have been approved.

## Open in ZiroEDA

https://designer.ziroeda.com/gh/huiw11512-dotcom/kicad_online/tree/minihost-revA/cm5_mini_host

If the deep link fails, use ZiroEDA → File → Open from GitHub, select `huiw11512-dotcom/kicad_online` → `cm5_mini_host` → `CM5_MINIMA_3.kicad_pro`.

This baseline includes complete routed source files; 3D manufacturer models may be omitted where large. Missing external 3D models do not affect native copper geometry.

## Important

Do **not** order boards based solely on a successful web import. Proper fabrication release requires electrical design review, pin-map and component-footprint verification, stackup and impedance calculation from the board fabricator, complete DRC/ERC closure, Gerber/NC drill and stencil review, and bench bring-up.
