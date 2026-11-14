#!/usr/bin/env python3
"""Safely drop exactly three KiCad-flagged single-layer dangling vias.

These are not ground stitching via arrays. Precise net+XY identities are from
KiCad 10 DRC [via_dangling]. Do not touch any other vias or trace segments.
For each candidate, verify connected track endpoints occupy at most ONE
copper layer; vias linking two routed layers are absolutely excluded.
Electrical design parity and new DRC still gate any commit.
"""
from pathlib import Path
import math
import pcbnew

path=Path("cm5_mini_host/CM5_MINIMA_3.kicad_pcb")
b=pcbnew.LoadBoard(str(path))
target=[
    ("/USB_C.D_P",85.8480,48.5204),
    ("/CM5/PWR_BUT",130.9594,65.5595),
    ("+BATT",81.4500,72.5000),
]
def mm(v):return pcbnew.ToMM(v)
def dist(v,x,y):return math.hypot(mm(v.x)-x,mm(v.y)-y)
padsig=sorted((f.GetReference(),p.GetNumber(),p.GetNetname(),p.GetPosition().x,p.GetPosition().y,p.GetSize().x,p.GetSize().y)
               for f in b.GetFootprints() for p in f.Pads())
trackbefore=len(b.GetTracks())
netbefore=b.GetNetCount()
zonebefore=len(b.Zones())
nvia_before=sum(isinstance(t,pcbnew.PCB_VIA) for t in b.GetTracks())
delete=[]
for name,x,y in target:
    vias=[t for t in b.GetTracks() if isinstance(t,pcbnew.PCB_VIA) and
          t.GetNetname()==name and dist(t.GetPosition(),x,y)<=0.002]
    if len(vias)!=1:
        raise SystemExit(f"Expected exactly 1 dangling via at {name} ({x},{y}), found {len(vias)}")
    v=vias[0]
    layers=set()
    touching=[]
    for t in b.GetTracks():
        if t is v or isinstance(t,pcbnew.PCB_VIA) or t.GetNetname()!=name:continue
        if dist(t.GetStart(),x,y)<=0.005 or dist(t.GetEnd(),x,y)<=0.005:
            touching.append((b.GetLayerName(t.GetLayer()),round(mm(t.GetWidth()),3)))
            layers.add(t.GetLayer())
    if len(layers)>1:
        raise SystemExit(f"REJECT {name} ({x},{y}): touches routed tracks on BOTH outer layers {touching}")
    # Exact center of a solder pad is not an expendable dangling via.
    pad_centers=[f"{f.GetReference()}.{p.GetNumber()}"
                 for f in b.GetFootprints() for p in f.Pads()
                 if p.GetNetname()==name and dist(p.GetPosition(),x,y)<0.01]
    if pad_centers:
        raise SystemExit(f"REJECT {name} ({x},{y}): via is pad-centered {pad_centers}")
    delete.append(v)
    print(f"Dangling via {name} ({x:.4f},{y:.4f}) F-B; connected trace endpoint layers: {touching}")
assert len(delete)==3
for v in delete:b.Remove(v)
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
pcbnew.SaveBoard(str(path),b)
c=pcbnew.LoadBoard(str(path))
padnew=sorted((f.GetReference(),p.GetNumber(),p.GetNetname(),p.GetPosition().x,p.GetPosition().y,p.GetSize().x,p.GetSize().y)
               for f in c.GetFootprints() for p in f.Pads())
assert padnew==padsig
assert c.GetNetCount()==netbefore and len(c.Zones())==zonebefore
assert len(c.GetTracks())==trackbefore-3
assert sum(isinstance(t,pcbnew.PCB_VIA) for t in c.GetTracks())==nvia_before-3
print("Roundtrip: 3 suspect vias removed; no other PCB traces, pad geometry, nets or zone definitions edited.")
