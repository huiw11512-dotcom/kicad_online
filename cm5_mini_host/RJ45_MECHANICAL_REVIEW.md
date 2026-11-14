# MiniHost Rev.A — RJ45 mechanical blockers and resolution plan

**Status (2026-11-14):** Manufacturing release **BLOCKED**. KiCad 10.0.8 schematic ERC = 0; PCB unconnected = 0; PCB schematic footprint parity = 0; remaining **2 hard PCB DRC violations** are copper-to-Edge.Cuts spacing at RJ45 pad 15/16. The earlier two courtyard overlaps were fixed by a verified nonrectangular pad-aware F.CrtYd, not by moving or shrinking copper.

## Grounded drawing and coordinates

- [Kycon GLPLX-SMT-188S7-QQ-Y/G official product drawing, A4 revision dated 2025-03-26](https://www.kycon.com/Pub_Eng_Draw/GLPLX-SMT-188S7-QQ-YG.pdf).
- [Measured-location overlay (SVG)](RJ45_MECHANICAL_CONFLICT_MAP.svg).
- The manufacturer drawing explicitly identifies **recommended PCB layout**, **edge of PCB** and **PCB over-hang (customer's preference)**; pin/shell solder pads and chassis interference should be reviewed together, not independently.
- Baseline board outline bounding box: x = 75.025 to 136.275 mm; y = 20.225 to 84.475 mm, nominal **61.25 × 64.25 mm**.
- J1 footprint x/y position = (88.900, 36.150) mm; current aggregate footprint bounding box x 75.897–100.276, y 24.900–47.400 mm. This aggregate bounding box **does not equal** exact 3D body or F.CrtYd polygon; official part drawing is authoritative for fit.
- Front-end cutout: horizontal Edge.Cuts segments from (78.370,28.2414) to (89.2836,28.2414) and from (78.370,44.0336) to (89.2836,44.0336), connected by a right-side vertical edge.

### Originally reported hard KiCad DRC errors (updated resolution)

| DRC category | Measured location | Violation | Required engineering work |
| --- | --- | --- | --- |
| copper_edge_clearance | J1 pad 16, (83.996,27.000) | actual **0.1914 mm**, required 0.3720 mm | Reconcile upper RJ45 solder-shield land with PCB cutout and recommended land geometry |
| copper_edge_clearance | J1 pad 15, (83.996,45.300) | actual **0.2164 mm**, required 0.3720 mm | Reconcile lower RJ45 solder-shield land with board edge and real enclosure cutout |
| courtyards_overlap | J1 (88.900,36.150), J601 (99.650,49.850) | **RESOLVED** by pad-aware body contour | Verified KiCad courtyard overlaps 2→0, without changing copper/placement |
| courtyards_overlap | J1 (88.900,36.150), H102 (78.150,23.350) | **RESOLVED** by pad-aware body contour | Same verified 2→0 Courtyard no-regression test; no mounting hole moved |

### Why these are not simply suppressed

1. The connector uses a **board-edge opening**. The two shield pads and the cutout are not arbitrary clearance objects. A smaller land, wider cutout or weaker edge clearance may degrade solder-joint support or lead to routing/mechanical incompatibility.
2. The F.CrtYd overlap at J601 reflects an actual need for assembly access and fan plug mating volume. Simply reducing a courtyard polygon could misrepresent the real mechanical envelope.
3. H102 is a screw hole with Ø2.7 mm drill and 5.4 mm copper pad, so even if the RJ45 plastic housing can pass it, the fastening hardware/washer and edge mechanical stiffness need checking.
4. The design has an M.2 SSD extending over much of the central board region. Moving the fan header toward the M.2 region can create new vertical height conflicts not represented by ordinary planar DRC.

### Candidate MiniHost-specific topology choices

**Updated (implemented):** Preserve the Kycon RJ45 electrical net mapping and actual solder pads; use a closed 12-edge Courtyard following the 17.6 mm nominal body and separately enclosing the shield-solder tabs. It eliminates KiCad's phantom overlap with J601 and H102, without removing either. **Still requires real physical enclosure and cable clearance review**: DRC Courtyard=0 does not certify mating geometry. The two remaining copper-edge violations need independent board-opening treatment. Compute the exact RJ45 PCB overhang from the official A4 land pattern and the enclosure opening before modifying the edge profile.

**Alternative design choice:** If compactness/thermal behavior favor a passive heatsink, omit the fan header in a subsequent **functional** redesign, with actual cooling tests and thermal requirements. This must include schematic and PCB updates and does not by itself solve H102 or edge-solder clearance.

**Do not do:** shrink J1 pad 15/16 solely to satisfy DRC, move only the rectangular courtyard, disable courtyard/edge errors, or call the result fabrication-ready before assembly and fit checks.

## Verification gates for future physical edits

- Actual KiCad DRC before/after: no new electrical errors, and ideally **2 → 0 remaining hard errors**.
- Flat mechanical fit and vertical clearance against a current Kycon A4 drawing and CM5/M.2 installed hardware.
- Four fan nets parity, no accidental shorts, both shield connections still correct.
- Preserve J1 transformer / Ethernet pair connectivity and diff-pair geometry after any footprint relocation.
- All four screw holes properly supported by new board outline and matched to the actual enclosure pattern.
- Manufacture-ready footprint, paste, drill and copper edge Gerber inspection by the selected fabricator.

Updated validated courtyard trial: [RJ45_COURTYARD_RESHAPE_AUDIT.md](RJ45_COURTYARD_RESHAPE_AUDIT.md), hard errors 4→2, courtyard overlaps 2→0, untouched pads and board edge. Original conflict drawing depicts original state and is retained for traceability.

This review is separate from the **completed** electrical tasks: ERC 0, zero unmatched footprint parity items, zero unrouted items, two USB2 network groups matched, 8 project-local custom footprints exported and checked, and the USB701 A7 controlled route shortening. Do not conflate those with full signal-integrity validation.
