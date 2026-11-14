# Local footprint provenance
These footprints were **recovered from embedded PCB geometry** of the attributed CM5 MINIMA Rev3 baseline, not redrawn, verified against datasheets or confirmed as stocked parts. They are provided to make the editable board reproducible on a fresh KiCad installation and in web viewers. Source is the same CERN-OHL-S-2.0 licensed upstream design linked from README.

The extraction script checks every unique footprint's pad number, pad type, copper size and drill size by saving to and reloading from the KiCad library. **It does not validate the manufacturer's body, courtyard, stencil, plating or placement**. Do not fabricate until physical drawings, 3D height and pin mapping are checked.

See `FOOTPRINT_SNAPSHOT.json` for each footprint and its source reference.
