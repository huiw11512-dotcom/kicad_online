# Mechanical CM5 body contour vs mounted switches

Before: {'erc': 0, 'hard': 0, 'parity': 0, 'unrouted': 0, 'total': 80, 'cats': {'silk_overlap': 8, 'silk_over_copper': 7, 'lib_footprint_mismatch': 49, 'silk_edge_clearance': 15, 'via_dangling': 1}}

After: {'erc': 0, 'hard': 0, 'parity': 0, 'unrouted': 0, 'total': 74, 'cats': {'silk_overlap': 8, 'silk_over_copper': 1, 'lib_footprint_mismatch': 49, 'silk_edge_clearance': 15, 'via_dangling': 1}}

One 48 mm CM5 body-outline segment, originally on B.SilkS from Module301, crossed SW101/SW501 solder-mask pad openings. Moved the identical stroke to B.Fab, leaving full visual CM5 outline in assembly drawings while keeping all connector and board markings elsewhere unchanged. Updated project-local CM5IO library corresponding F.SilkS stroke to F.Fab; KiCad native pad/trace/zone comparison verified no electrical change. Six soldermask/silkscreen collision warnings were removed without disabling fabrication checks.
