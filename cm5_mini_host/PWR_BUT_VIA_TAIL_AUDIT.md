# Unused power-button branch cleanup

Before: (0, 0, 0, 0, 74, {'silk_overlap': 8, 'silk_over_copper': 1, 'lib_footprint_mismatch': 49, 'silk_edge_clearance': 15, 'via_dangling': 1})

After: (0, 0, 0, 0, 73, {'silk_overlap': 8, 'silk_over_copper': 1, 'lib_footprint_mismatch': 49, 'silk_edge_clearance': 15})

Removed one KiCad-reported unused F/B via at 130.959409,65.559501 and exactly one unbranched F.Cu path back to an electrically connected existing via at 128.25,64.45, which was preserved. No pad, external button net assignment, or B.Cu route was modified. Full DRC and ERC confirm no orphaned pads or new dangling tracks. The power button mechanical actuator and logic still need power-on testing.
