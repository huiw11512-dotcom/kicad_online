# Tiny KiBuzzard generated reference cleanup

Before: {'erc': 0, 'hard': 2, 'parity': 0, 'unconnected': 0, 'text_height': 27, 'text_thickness': 27, 'total': 198}

After: {'erc': 0, 'hard': 2, 'parity': 0, 'unconnected': 0, 'text_height': 0, 'text_thickness': 0, 'total': 140}

Set 27 KiBuzzard footprint reference fields to hidden. Each was <0.01 mm in size, carried no pad and is not the actual visual label. All original silkscreen polygons remain; native KiCad reload confirms no track, pad, net, placement or zone changes. This is a visible-label-preserving DRC fix, not disabling a rule globally.
