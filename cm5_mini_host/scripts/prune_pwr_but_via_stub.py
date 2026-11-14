#!/usr/bin/env python3
"""Find and prune a standalone PWR_BUT F.Cu dead-end trace chain.

Do NOT delete the functional B.Cu connection at the other end. Start from
KiCad DRC via_dangling at (130.959409,65.559501) and follow F.Cu single
path of tracks until the first actual via or tee joint. An F.Cu track may not
be removed if it touches an electrical pad in the interior. The structural
test and stringent KiCad DRC before/after gate must both pass.
"""
from pathlib import Path
from collections import defaultdict
import math,pcbnew
p=Path("cm5_mini_host/CM5_MINIMA_3.kicad_pcb")
b=pcbnew.LoadBoard(str(p))
net='/CM5/PWR_BUT'
mm=pcbnew.ToMM
targets=[t for t in b.GetTracks() if isinstance(t,pcbnew.PCB_VIA) and t.GetNetname()==net and
         abs(mm(t.GetPosition().x)-130.959409)<.003 and abs(mm(t.GetPosition().y)-65.559501)<.003]
if len(targets)!=1:raise SystemExit('Expected one exact PWR_BUT dangling via')
dead=targets[0]
def pos(v):return (v.x,v.y)
tracks=[t for t in b.GetTracks() if isinstance(t,pcbnew.PCB_TRACK) and not isinstance(t,pcbnew.PCB_VIA) and
        t.GetNetname()==net and b.GetLayerName(t.GetLayer())=="F.Cu"]
neigh=defaultdict(list)
for t in tracks:
    neigh[pos(t.GetStart())].append((t,pos(t.GetEnd())))
    neigh[pos(t.GetEnd())].append((t,pos(t.GetStart())))
start=pos(dead.GetPosition())
if len(neigh[start])!=1:raise SystemExit('Dangling via must touch exactly one front-copper segment')
other_vias={pos(t.GetPosition()):t for t in b.GetTracks() if isinstance(t,pcbnew.PCB_VIA) and
            t.GetNetname()==net and t is not dead}
switchpads=[(f,pad) for f in b.GetFootprints() for pad in f.Pads() if
            f.GetReference()=="SW501" and pad.GetNumber()=="1" and pad.GetNetname()==net]
if len(switchpads)!=1:
    raise SystemExit("Expected existing SW501.1 /CM5/PWR_BUT signal pad")
swpad=switchpads[0][1]
stop_pad=pos(swpad.GetPosition())
if abs(mm(stop_pad[0])-129.67)>.005 or abs(mm(stop_pad[1])-64.62)>.005:
    raise SystemExit("Unexpected power-switch physical solder pad center")
path=[];point=start;prev=None
while True:
    choices=[(t,q) for t,q in neigh[point] if t is not prev]
    if len(choices)!=1:raise SystemExit(f"Unexpected F.Cu branch/termination at {tuple(mm(v) for v in point)}")
    t, nxt=choices[0]
    if t in path:raise SystemExit('F.Cu route loops to itself')
    if abs(mm(t.GetWidth())-.2)>.055:raise SystemExit('Unexpected tail segment width, review manually')
    path.append(t)
    if nxt==stop_pad:
        endpoint=nxt
        break
    if nxt in other_vias:
        raise SystemExit("The dead tail reached a second via before SW501 pad; cannot prune")
    if len(neigh[nxt])!=2:
        raise SystemExit('The dangling via tail is not a simple standalone chain to a live via')
    if len(path)>30:raise SystemExit('Impossibly long PWR_BUT route')
    prev=t;point=nxt
ex,ey=map(mm,endpoint)
if abs(ex-129.67)>.01 or abs(ey-64.62)>.01:
    raise SystemExit(f'Tail endpoint at {ex},{ey}, expected SW501 pin1 physical solder pad')
length=sum(mm(t.GetLength()) for t in path)
if not 1.2<length<4.0:raise SystemExit(f'Unexpected copper stub length {length:.3f}mm')
# The SW501 pad must retain its other, live F.Cu track back toward CM5.
if len(neigh[endpoint])!=2 or sum(t not in path for t,q in neigh[endpoint])!=1:
    raise SystemExit("SW501.1 would lose its only routed connection")
# Reject if any PWR_BUT pad center occupies any of the path segments or is
# within a pad-sized margin around their straight-line copper. If present,
# this would remove a genuine pad connection despite an apparent terminal via.
for f in b.GetFootprints():
    for pad in f.Pads():
        if pad.GetNetname()!=net:continue
        X,Y=map(mm,pos(pad.GetPosition()))
        for t in path:
            a=t.GetStart();z=t.GetEnd()
            ax,ay=map(mm,pos(a));bx,by=map(mm,pos(z))
            dx=bx-ax;dy=by-ay
            lam=max(0,min(1,((X-ax)*dx+(Y-ay)*dy)/max(dx*dx+dy*dy,1e-10)))
            dist=math.hypot(X-(ax+lam*dx),Y-(ay+lam*dy))
            # The intended SW501.1 land is connected exactly at the LAST
            # endpoint; removing this terminal dead-end trace preserves the
            # second, live SW501.1 track to the CM5 via.
            if dist<.35 and not (f.GetReference()=="SW501" and pad.GetNumber()=="1" and
                                   t is path[-1] and pos(pad.GetPosition())==endpoint):
                raise SystemExit(f'Unsafe: PWR_BUT pad {f.GetReference()}.{pad.GetNumber()} touches candidate dead-end route')
# Verify functional opposite end of SW501 pin1 still continues on F.Cu.
active=[(t,q) for t,q in neigh[endpoint] if t not in path]
if len(active)!=1 or abs(mm(active[0][1][0])-129.67)>.01 or abs(mm(active[0][1][1])-64.77)>.01:
    raise SystemExit("Retained SW501.1 CM5-directed segment missing")
before_pad=sorted((f.GetReference(),x.GetNumber(),x.GetNetname(),pos(x.GetPosition()))
                  for f in b.GetFootprints() for x in f.Pads())
oldtracks=len(b.GetTracks());oldnets=b.GetNetCount();oldzones=len(b.Zones())
for t in path:b.Remove(t)
b.Remove(dead)
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
pcbnew.SaveBoard(str(p),b)
chk=pcbnew.LoadBoard(str(p))
assert len(chk.GetTracks())==oldtracks-len(path)-1 and chk.GetNetCount()==oldnets and len(chk.Zones())==oldzones
assert sorted((f.GetReference(),x.GetNumber(),x.GetNetname(),pos(x.GetPosition()))
                  for f in chk.GetFootprints() for x in f.Pads())==before_pad
print(f'Pruned {len(path)} unused front-copper segments ({length:.4f}mm) from power-switch pin SW501.1 to dead via. Active SW501.1-to-CM5 route retained.')
