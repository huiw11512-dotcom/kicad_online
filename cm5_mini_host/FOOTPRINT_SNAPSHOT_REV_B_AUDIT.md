# Rev.B exact embedded-footprint snapshot audit

- Board footprints: 111
- Unique local footprint definitions: 32
- Split duplicate-ID variants: 4 instances
- Tracks unchanged: 2513
- Zones unchanged: 14
- Nets unchanged: 221

KiCad save/reload preserved all pad numbers, pad types/shapes, local and world coordinates, copper sizes, drills and net assignments. This removes ambiguity between board-embedded geometry and installed library versions; it does NOT certify manufacturer land patterns, paste/mask, body/courtyard, sourcing or assembly fit.

## Split variants

- D701: Package_TO_SOT_SMD:SOT-416 -> Package_TO_SOT_SMD:SOT-416__D701
- R702: Resistor_SMD:R_0402_1005Metric -> Resistor_SMD:R_0402_1005Metric__R702__R703
- R703: Resistor_SMD:R_0402_1005Metric -> Resistor_SMD:R_0402_1005Metric__R702__R703
- TP101: TestPoint:TestPoint_Pad_D1.0mm -> TestPoint:TestPoint_Pad_D1.0mm__TP101
