#!/usr/bin/env python3
"""De-duplicate two coincident nonplated CM5 alignment holes.

CM5 MINIMA represents a single physical CM5 module with two electrical
footprints Module301 (GPIO) and Module302 (HSS). Both imported footprints
contain the same two unnumbered NPTH pads at identical positions but DIFFERENT drill diameters (2.7 vs 3.0 mm),
resulting in [holes_co_located] x2 in native KiCad DRC.

Keep Module301 physical drill definitions. Remove the redundant *non-electrical*
NPTH objects only from Module302 AND the project-local HSS footprint library.
Official CM5 module mounting uses four M2.5 hardware holes. The 2.7 mm GPIO holes are kept.
Do not edit any signal pad, network, track, copper zone or board outline.
"""
from pathlib import Path
import pcbnew

root=Path("cm5_mini_host")
boardfile=root/"CM5_MINIMA_3.kicad_pcb"
b=pcbnew.LoadBoard(str(boardfile))
lookup=lambda ref:next((f for f in b.GetFootprints() if f.GetReference()==ref),None)
a=lookup("Module301");c=lookup("Module302")
assert a and c,"Module301/Module302 are both required"

mm=pcbnew.ToMM
xy=lambda x:(round(mm(x.x),3),round(mm(x.y),3))
def alignment_pads(fp):
    return [p for p in fp.Pads()
            if p.GetAttribute()==pcbnew.PAD_ATTRIB_NPTH
            and not p.GetNumber() and not p.GetNetname()
            and xy(p.GetPosition()) in {(127.25,29.6),(127.25,77.6)}]
pa=alignment_pads(a)
pb=alignment_pads(c)
if len(pa)!=2 or len(pb)!=2:raise SystemExit(f"Expected exactly two identical alignment holes per connector half: GPIO {len(pa)} HSS {len(pb)}")
def detail(p):
    return (xy(p.GetPosition()),xy(p.GetSize()),xy(p.GetDrillSize()),int(p.GetAttribute()))
print("Module301 candidate NPTH:",sorted(map(detail,pa)))
print("Module302 candidate NPTH:",sorted(map(detail,pb)))
# Both logical CM5 halves reproduce the same two mounting positions, but the
# board-embedded drill diameters DIFFER: GPIO uses 2.7 mm, HSS uses 3.0 mm.
# The official CM5 drawing specifies M2.5 mounting hardware. Retain the
# explicit 2.7 mm M2.5 clearance holes from GPIO; remove redundant 3.0 mm HSS
# drills, avoiding contradictory drilling data at the exact same XY points.
pa_sorted=sorted(map(detail,pa))
pb_sorted=sorted(map(detail,pb))
if [x[0] for x in pa_sorted]!=[x[0] for x in pb_sorted]:
    raise SystemExit("Holes are not at the same physical positions; abort")
if any(x[1]!=(2.7,2.7) or x[2]!=(2.7,2.7) for x in pa_sorted):
    raise SystemExit("Expected M2.5-compatible 2.7 mm GPIO clearance holes")
if any(x[1]!=(3.0,3.0) or x[2]!=(3.0,3.0) for x in pb_sorted):
    raise SystemExit("Expected redundant 3.0 mm HSS drill objects")
for p in pb:
    c.Remove(p)
print("Removed 2 coincident non-electrical NPTHs from Module302, retained their physical copies in Module301")
assert len(alignment_pads(c))==0 and len(alignment_pads(a))==2
# Save board; KiCad writes all component pad geometry but preserves existing copper.
orig_tracks=len(b.GetTracks());orig_nets=b.GetNetCount()
pcbnew.SaveBoard(str(boardfile),b)
b2=pcbnew.LoadBoard(str(boardfile))
assert len(b2.GetTracks())==orig_tracks and b2.GetNetCount()==orig_nets
assert len(alignment_pads(next(f for f in b2.GetFootprints() if f.GetReference()=="Module302")))==0
# Synchronize project-local HSS library to avoid untracked footprint-library drift.
lib=root/"CM5IO.pretty"
name="Raspberry-Pi-5-Compute-Module_HSS"
io=pcbnew.PCB_IO_KICAD_SEXPR()
h=next(f for f in b2.GetFootprints() if f.GetReference()=="Module302")
io.FootprintSave(str(lib),h)
readback=io.FootprintLoad(str(lib),name)
assert readback is not None
npths=[p for p in readback.Pads() if p.GetAttribute()==pcbnew.PAD_ATTRIB_NPTH and not p.GetNumber()]
assert len(npths)==0,f"Exported HSS library still has {len(npths)} unnumbered NPTH pads"
print("Synchronized and roundtrip checked local HSS footprint library; no electrical pin count changes")
