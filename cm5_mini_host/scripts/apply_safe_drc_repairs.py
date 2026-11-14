#!/usr/bin/env python3
"""Conservative DRC repairs for mechanical holes and overlapping same-net zones."""
from pathlib import Path
import pcbnew

path=Path("cm5_mini_host/CM5_MINIMA_3.kicad_pcb")
board=pcbnew.LoadBoard(str(path))
converted=[]
for ref in ("J101","USB701","SW101"):
    fp=next((f for f in board.GetFootprints() if f.GetReference()==ref),None)
    if fp is None: raise SystemExit(f"Missing expected footprint {ref}")
    pads=[p for p in fp.Pads() if not p.GetNumber() and not p.GetNetname()]
    if len(pads)!=2: raise SystemExit(f"{ref}: expected 2 unnumbered, no-net locating holes, found {len(pads)}")
    for p in pads:
        size=p.GetSize(); drill=p.GetDrillSize()
        if size.x!=drill.x or size.y!=drill.y:
            raise SystemExit(f"{ref}: pad {p.GetNumber()} is not a zero-annulus locating hole; refusing to change")
        if p.GetAttribute()==pcbnew.PAD_ATTRIB_PTH:
            p.SetAttribute(pcbnew.PAD_ATTRIB_NPTH)
            converted.append(f"{ref}@{pcbnew.ToMM(p.GetPosition().x):.3f},{pcbnew.ToMM(p.GetPosition().y):.3f}")
        elif p.GetAttribute()!=pcbnew.PAD_ATTRIB_NPTH:
            raise SystemExit(f"{ref}: unexpected pad attribute {p.GetAttribute()}; refusing to change")
if len(converted) not in (0,6): raise SystemExit(f"Expected 0 or 6 mechanical holes to convert, converted {len(converted)}")
zones=list(board.Zones())
candidates=[]
for z in zones:
    if z.GetNetname()!="M2_3V3" or z.GetAssignedPriority()!=10: continue
    layers=z.GetLayerSet()
    has_in3=layers.Contains(pcbnew.In3_Cu)
    has_f=layers.Contains(pcbnew.F_Cu)
    if has_in3 and not has_f:
        candidates.append(z)
if len(candidates)==1:
    candidates[0].SetAssignedPriority(11)
elif not any(z.GetNetname()=="M2_3V3" and z.GetAssignedPriority()==11 and z.GetLayerSet().Contains(pcbnew.In3_Cu) and not z.GetLayerSet().Contains(pcbnew.F_Cu) for z in zones):
    raise SystemExit("Expected either one priority-10 or an already repaired priority-11 M2_3V3 In3.Cu zone")
# Refill all zones after geometry/type/priority edits.
filler=pcbnew.ZONE_FILLER(board)
filler.Fill(zones)
pcbnew.SaveBoard(str(path),board)
print("Converted NPTH locating holes:")
for x in converted: print(" -",x)
print("Raised the overlapping M2_3V3 In3.Cu zone priority from 10 to 11.")
print("Refilled",len(zones),"zones and saved",path)
