# CM5 mechanical alignment hole de-duplication

Before (0, 2, 0, 0, 2)

After (0, 2, 0, 0, 0)

Removed only two no-net, no-number coincident NPTH pads in HSS footprint Module302 while retaining the same two physical holes in GPIO half Module301. Validated by native pcbnew and original HSS KiCad footprint library roundtrip. Copper, nets, and copper tracks preserved. Manufacturer connector drawing and 3D assembly still require separate confirmation.
