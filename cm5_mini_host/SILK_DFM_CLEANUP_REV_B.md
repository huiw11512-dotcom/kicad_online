# Rev.B silkscreen DFM cleanup

Moved clipped or overlapping footprint body graphics from silkscreen to the corresponding fabrication layer; reference/value text remains on silkscreen. This preserves component outlines and orientation marks in assembly artwork while keeping the board-edge and label clearances manufacturable.

## Footprints

- C702: 3 graphical primitives moved to Fab
- J1: 9 graphical primitives moved to Fab
- J101: 10 graphical primitives moved to Fab
- J501: 8 graphical primitives moved to Fab
- J701: 12 graphical primitives moved to Fab
- Module301: 13 graphical primitives moved to Fab
- SW101: 14 graphical primitives moved to Fab
- SW501: 9 graphical primitives moved to Fab
- TP101: 1 graphical primitives moved to Fab
- U702: 3 graphical primitives moved to Fab
- USB701: 10 graphical primitives moved to Fab

- Board-level silk segment nearest (130.13,62.07) mm moved to F.Fab (distance 0.0000 mm).

No copper, pads, tracks, vias, zones, drills, nets, component placement or reference/value text was changed.
