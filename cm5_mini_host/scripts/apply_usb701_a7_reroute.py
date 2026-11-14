#!/usr/bin/env python3
"""Conservative candidate: shorten *only* the USB701 A7 USB2 N branch on B.Cu.
Six existing B.Cu track segments are replaced by a direct 0.14 mm segment.
Original net, connector pads, ESD, vias, layer stackup and other tracks unchanged.
A separate GitHub workflow performs before/after DRC and commits only if safe.
"""
from pathlib import Path
import math
import pcbnew

path=Path("cm5_mini_host/CM5_MINIMA_3.kicad_pcb")
board=pcbnew.LoadBoard(str(path))
name="/CM5/USB2P.D_N"
mm=pcbnew.FromMM
mm2=pcbnew.ToMM
def pair(v):return (round(mm2(v.x),4),round(mm2(v.y),4))
def key(a,b):return tuple(sorted((tuple(a),tuple(b))))
route=[
 ((85.8,63.9),(85.85,63.85)),
 ((85.85,63.85),(87.1,63.85)),
 ((87.1,63.85),(87.81,63.14)),
 ((87.81,63.14),(87.81,60.8927)),
 ((87.81,60.8927),(86.6173,59.7)),
 ((86.6173,59.7),(86.452,59.7))
]
required={key(*e) for e in route}
found=[]
for tr in board.GetTracks():
    if tr.GetNetname()!=name or tr.GetLayer()!=pcbnew.B_Cu or isinstance(tr,pcbnew.PCB_VIA):
        continue
    k=key(pair(tr.GetStart()),pair(tr.GetEnd()))
    if k in required:
        if int(tr.GetWidth())!=mm(0.14):raise SystemExit("Unexpected USB track width; refusing to modify")
        found.append((k,tr))
seen={k for k,_ in found}
if len(found)!=6 or seen!=required:raise SystemExit(f"Expected exactly six specific track segments, found {len(found)}")
old_len=sum(mm2(tr.GetLength()) for _,tr in found)
assert old_len>6.3 and old_len<6.6
netcode=found[0][1].GetNetCode()
for _,tr in found:board.Remove(tr)
new=pcbnew.PCB_TRACK(board)
new.SetStart(pcbnew.VECTOR2I(mm(85.8),mm(63.9)))
new.SetEnd(pcbnew.VECTOR2I(mm(86.452),mm(59.7)))
new.SetLayer(pcbnew.B_Cu)
new.SetWidth(mm(0.14))
new.SetNetCode(netcode)
board.Add(new)
new_len=mm2(new.GetLength())
if old_len-new_len<2.0 or old_len-new_len>2.3:raise SystemExit("Implausible expected length delta")
pcbnew.ZONE_FILLER(board).Fill(board.Zones())
pcbnew.SaveBoard(str(path),board)
print(f"USB701 A7 N branch copper centerline shortened from {old_len:.4f} to {new_len:.4f} mm, saved {old_len-new_len:.4f} mm.")
print("Note: complete USB2 SI and impedance are not validated by this geometry edit.")
