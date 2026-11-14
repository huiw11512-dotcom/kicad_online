#!/usr/bin/env python3
"""Remove only +BATT branch copper stub 0.60mm with its unconnected via.

Native KiCad DRC flagged via at (81.45,72.50) F/B, but it meets only the
single In3.Cu track (81.45,72.50) to (82.05,72.50). That endpoint is not a
required footprint pad. The main In3.Cu +BATT path from (85.15,72.50) to
(82.05,72.50) and the other layer connection at 82.05 MUST remain.
"""
from pathlib import Path
import math,pcbnew
p=Path("cm5_mini_host/CM5_MINIMA_3.kicad_pcb")
b=pcbnew.LoadBoard(str(p))
mm=pcbnew.ToMM
def at(v,x,y):return abs(mm(v.x)-x)<0.003 and abs(mm(v.y)-y)<0.003
via=[t for t in b.GetTracks() if isinstance(t,pcbnew.PCB_VIA) and t.GetNetname()=="+BATT" and at(t.GetPosition(),81.45,72.5)]
if len(via)!=1:raise SystemExit("Expected exact one unused +BATT via")
path=[t for t in b.GetTracks() if isinstance(t,pcbnew.PCB_TRACK) and not isinstance(t,pcbnew.PCB_VIA) and t.GetNetname()=="+BATT" and
      ((at(t.GetStart(),81.45,72.5) and at(t.GetEnd(),82.05,72.5)) or
       (at(t.GetEnd(),81.45,72.5) and at(t.GetStart(),82.05,72.5)))]
if len(path)!=1 or b.GetLayerName(path[0].GetLayer())!="In3.Cu" or abs(mm(path[0].GetWidth())-0.4)>0.01:
    raise SystemExit("Expected only one 0.600mm / +BATT In3.Cu 0.4mm stub")
if any(at(pad.GetPosition(),81.45,72.5) for f in b.GetFootprints() for pad in f.Pads()):
    raise SystemExit("Do not remove pad-centered via")
touch=[t for t in b.GetTracks() if isinstance(t,pcbnew.PCB_TRACK) and
       t.GetNetname()=="+BATT" and (at(t.GetStart(),82.05,72.5) or at(t.GetEnd(),82.05,72.5)) and t is not path[0]]
if len(touch)<2:raise SystemExit("The trunk at stub-branch junction is not safely connected")
oldpads=sorted((f.GetReference(),pad.GetNumber(),pad.GetNetname(),pad.GetPosition().x,pad.GetPosition().y)
               for f in b.GetFootprints() for pad in f.Pads())
n=len(b.GetTracks());zones=len(b.Zones());nets=b.GetNetCount()
b.Remove(via[0]);b.Remove(path[0])
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
pcbnew.SaveBoard(str(p),b)
out=pcbnew.LoadBoard(str(p))
assert len(out.GetTracks())==n-2 and len(out.Zones())==zones and out.GetNetCount()==nets
assert sorted((f.GetReference(),pad.GetNumber(),pad.GetNetname(),pad.GetPosition().x,pad.GetPosition().y)
               for f in out.GetFootprints() for pad in f.Pads())==oldpads
print("Removed only unused +BATT 0.60mm branch and dangling F-B via. Trunk and all pads retained.")
