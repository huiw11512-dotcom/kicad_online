#!/usr/bin/env python3
"""Report the existing U602 VCC copper path and nearest CM5_3.3V attachment points."""
from pathlib import Path
import json,math,pcbnew
root=Path("cm5_mini_host")
b=pcbnew.LoadBoard(str(root/"CM5_MINIMA_3.kicad_pcb"))
u=next((fp for fp in b.GetFootprints() if str(fp.GetReference())=="U602"),None)
if u is None:raise SystemExit("U602 missing")
p5=next((p for p in u.Pads() if str(p.GetNumber())=="5"),None)
if p5 is None:raise SystemExit("U602 pad 5 missing")
origin=p5.GetPosition()
def mm(v):return pcbnew.ToMM(v)
def xy(v):return (round(mm(v.x),4),round(mm(v.y),4))
def dxy(a,c):return math.hypot(mm(a.x-c.x),mm(a.y-c.y))
def ptseg(p,a,c):
    px,py=mm(p.x),mm(p.y); ax,ay=mm(a.x),mm(a.y); cx,cy=mm(c.x),mm(c.y)
    dx,dy=cx-ax,cy-ay; den=dx*dx+dy*dy
    t=0 if den==0 else max(0,min(1,((px-ax)*dx+(py-ay)*dy)/den))
    return math.hypot(px-(ax+t*dx),py-(ay+t*dy))
rows={"u602_pad5":{"xy":xy(origin),"net":p5.GetNetname()},"nearby_3v3_pads":[],"nearby_3v3_tracks":[],"nearby_5v_tracks":[],"nearby_vias":[],"zones":[]}
for fp in b.GetFootprints():
    for pad in fp.Pads():
        if pad.GetNetname()=="+3V3_PI":
            dist=dxy(origin,pad.GetPosition())
            if dist<25:
                rows["nearby_3v3_pads"].append({"ref":str(fp.GetReference()),"pad":str(pad.GetNumber()),"xy":xy(pad.GetPosition()),"distance_mm":round(dist,3)})
for t in b.GetTracks():
    net=t.GetNetname()
    if isinstance(t,pcbnew.PCB_VIA):
        pos=t.GetPosition(); dist=dxy(origin,pos)
        if dist<25:
            rows["nearby_vias"].append({"net":net,"xy":xy(pos),"layer":t.GetLayerName(),"distance_mm":round(dist,3),"diameter_mm":round(mm(t.GetWidth()),3),"drill_mm":round(mm(t.GetDrill()),3)})
    else:
        a=t.GetStart(); c=t.GetEnd()
        dist=ptseg(origin,a,c)
        if net=="+3V3_PI" and dist<25:
            rows["nearby_3v3_tracks"].append({"xy":[xy(a),xy(c)],"layer":t.GetLayerName(),"width_mm":round(mm(t.GetWidth()),3),"distance_mm":round(dist,3)})
        if net=="+5V" and dist<5:
            rows["nearby_5v_tracks"].append({"xy":[xy(a),xy(c)],"layer":t.GetLayerName(),"width_mm":round(mm(t.GetWidth()),3),"distance_mm":round(dist,3)})
for z in b.Zones():
    net=z.GetNetname()
    if net in ("+3V3_PI","+5V"):
        bb=z.GetBoundingBox()
        rows["zones"].append({"net":net,"layer":z.GetLayerName(),"bbox":[xy(bb.GetOrigin()),xy(bb.GetEnd())]})
for k in ["nearby_3v3_pads","nearby_3v3_tracks","nearby_5v_tracks","nearby_vias"]:
    rows[k].sort(key=lambda x:x.get("distance_mm",999))
(root/"U602_VCC_ROUTE_DIAGNOSTIC.json").write_text(json.dumps(rows,indent=2)+"\n",encoding="utf-8")
print(json.dumps(rows,indent=2))
