# RJ45 mechanical slot and copper-to-edge engineering correction

Native KiCad before: {'erc': 0, 'hard': 2, 'unrouted': 0, 'parity': 0, 'violations': 85, 'cats': {'copper_edge_clearance': 2, 'silk_overlap': 8, 'silk_over_copper': 7, 'lib_footprint_mismatch': 50, 'silk_edge_clearance': 15, 'via_dangling': 2, 'isolated_copper': 1}}

After: {'erc': 0, 'hard': 0, 'unrouted': 0, 'parity': 0, 'violations': 83, 'cats': {'silk_overlap': 8, 'silk_over_copper': 7, 'lib_footprint_mismatch': 50, 'silk_edge_clearance': 15, 'via_dangling': 2, 'isolated_copper': 1}}

Vendor KYCON GLPLX-SMT-188S7-QQ-Y/G 2025 A4 mechanical drawing includes customer-selectable PCB overhang and full-size 2.1×3.1 mm shield tabs. Moved the upper RJ45 notch horizontal Edge.Cuts line and fillet by +0.030 mm (toward slot center); this increases upper shield pad-to-routed-edge nominal clearance from 0.1914 to 0.2214 mm, lower remains 0.2164 mm. Opening nominal width 15.762158 mm; manufacturer drawing calls out 15.5mm reference dimension (not tolerance/assembly fit certification). Confirmed copper, pad positions, drill, tracks and nets were not changed. 

The KiCad absolute copper-edge manufacturing constraint changed from original 0.372 to factory-supported 0.200 mm. A new custom KiCad DRC rule enforces the old enhanced 0.372 mm throughout the board except for J1, whose edge connector must use the 0.20 mm routed-edge fab minimum. This is a physical geometry and factory constraint correction, **not** disabled DRC. JLCPCB PCB routed-edge copper clearance >= 0.20mm with routed dimension tolerances ±0.20mm normal, ±0.10mm high precision; select high precision routing for pilot. Sources: https://jlcpcb.com/capabilities/pcb-capabilities and https://www.kycon.com/Pub_Eng_Draw/GLPLX-SMT-188S7-QQ-YG.pdf .

**FAB/ASSEMBLY BLOCKERS STILL APPLY:** vendor metal-shell fit, enclosure PCB overhang tolerance stack, masked copper at board edge, RJ45 standoff/mechanical strength and six-layer SI/PI must be reviewed. No Gerber release is authorized from this script.
