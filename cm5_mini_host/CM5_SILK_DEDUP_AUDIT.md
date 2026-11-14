# CM5 double module outline removal (GPIO/HSS two-footprint design)

KiCad before (ERC/hard DRC/footprint parity/unconnected/silk_overlap/total): (0, 2, 0, 0, 33, 230)

After: (0, 2, 0, 0, 9, 198)

Removed only 4 duplicated long outer F.SilkS strokes and 4 corner arcs from Module302 (flipped B.SilkS) and from its project-local HSS footprint. Retained full Module301 body outline and HSS connector location marks. Native pcbnew parser confirmed all footprints, pad counts, nets, zones and tracks unchanged. Board physical mating and manufacturer dimensions are separate review gates.
