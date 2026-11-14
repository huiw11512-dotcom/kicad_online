# MiniHost Rev.A dangling-via candidate

Before: {'erc': 0, 'hard': 2, 'parity': 0, 'unconnected': 0, 'dangling': 3, 'total': 86, 'categories': {'copper_edge_clearance': 2, 'silk_overlap': 8, 'silk_over_copper': 7, 'lib_footprint_mismatch': 50, 'silk_edge_clearance': 15, 'via_dangling': 3, 'isolated_copper': 1}}

After: {'erc': 0, 'hard': 2, 'parity': 0, 'unconnected': 0, 'dangling': 2, 'total': 85, 'categories': {'copper_edge_clearance': 2, 'silk_overlap': 8, 'silk_over_copper': 7, 'lib_footprint_mismatch': 50, 'silk_edge_clearance': 15, 'via_dangling': 2, 'isolated_copper': 1}}

Exact removed via center: /USB_C.D_P (85.8480,48.5204) mm. The PWR_BUT and +BATT vias remain because removing all three created two new dangling track warnings. The removed USB D+ via joined two F.Cu trace endpoints and had no B.Cu track connection. Existing copper tracks, SMT pads, net names and board outline were not changed. This eliminates unused plated-via discontinuities on selected signal nets, but does not constitute SI/PI signoff.
