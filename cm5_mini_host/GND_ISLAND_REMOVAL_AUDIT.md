# GND disconnected zone fill removal

Before: {'erc': 0, 'unrouted': 0, 'parity': 0, 'hard': 0, 'total': 83, 'cats': {'silk_overlap': 8, 'silk_over_copper': 7, 'lib_footprint_mismatch': 50, 'silk_edge_clearance': 15, 'via_dangling': 2, 'isolated_copper': 1}}

After: {'erc': 0, 'unrouted': 0, 'parity': 0, 'hard': 0, 'total': 82, 'cats': {'silk_overlap': 8, 'silk_over_copper': 7, 'lib_footprint_mismatch': 50, 'silk_edge_clearance': 15, 'via_dangling': 2}}

Changed the giant 5-layer GND zone only from area-limited island removal (mode 2; 5mm²) to **always remove islands** (mode 0) using official KiCad zone semantics, and refilled. Original contour, copper traces, vias, component pads, nets and GND fill-rule thickness/thermal parameters remained unchanged. No actual grounded connected copper was intentionally removed; verification must still include SI/EMC return path study.
Reference: https://dev-docs.kicad.org/en/file-formats/sexpr-intro/index.html
