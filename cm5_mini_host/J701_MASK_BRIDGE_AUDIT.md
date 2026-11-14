# J701 M.2 copper-preserving mask expansion correction

Before: {'erc': 0, 'hard': 2, 'parity': 0, 'unconnected': 0, 'mask': 54, 'total': 140}

After: {'erc': 0, 'hard': 2, 'parity': 0, 'unconnected': 0, 'mask': 0, 'total': 86}

**Physical geometry:** copper pad width 0.3mm, pitch 0.5mm. Original per-pad mask expansion 0.102mm on each edge yields -0.004mm aperture overlap. Corrected to 0.020mm per edge, giving 0.16mm nominal mask dam. All 69 J701 pad copper sizes, positions, nets, paste, vias and other PCB geometry preserved; M.2 project footprint synchronized.

**Factory-specific:** proposed process is JLCPCB 6-layer PCB, green LDI solder mask, outer 1oz copper. JLCPCB official stated soldermask bridge min 0.10mm for 1oz green, per https://jlcpcb.com/capabilities/Capabilities . The design's 0.16mm nominal bridge is not a guarantee of defect-free production; mask registration and stackup must be verified by the selected fabricator. 2oz copper or black/white mask may require different minimum widths.

This reduces DRC violations without weakening/waiving board rules and without modifying M.2 copper pad or connector pitch.
