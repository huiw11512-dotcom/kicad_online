# Unused +BATT power-via stub clean

Native KiCad before: [0, 0, 0, 82, 0, 2, 0]

After: [0, 0, 0, 81, 0, 1, 0]

Removed one 0.60mm 0.40mm-wide In3.Cu track from (81.45,72.50) to (82.05,72.50) and only the branch endpoint F-B via at 81.45,72.50. The live battery power track on In3.Cu and its through-layer junction at (82.05,72.50) remain. No pad, net, segment on the remaining battery trunk, or zone outline was changed. Cloud KiCad ERC/parity/unrouted still zero. No physical battery power-delivery testing claimed.
