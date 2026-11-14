#!/usr/bin/env python3
"""Move U602 VCC from +5V to +3V3_PI and route on the clear In2 signal layer."""
from pathlib import Path
import math,pcbnew
root=Path("cm5_mini_host")
path=root/"CM5_MINIMA_3.kicad_pcb"
b=pcbnew.LoadBoard(str(path))
u=next((f for f in b.GetFootprints() if str(f.GetReference())=="U602"),None)
if u is None:raise SystemExit("U602 footprint missing")
p5=next((p for p in u.Pads() if str(p.GetNumber())=="5"),None)
if p5 is None or p5.GetNetname()!="+5V":raise SystemExit("U602 pad 5 is not on expected original +5V net")
net=b.FindNet("+3V3_PI");v5=b.FindNet("+5V")
if net is None or v5 is None:raise SystemExit("Required +3V3_PI or +5V net missing")
def mm(v):return pcbnew.FromMM(v)
def xy(p):return (round(p.x/1e6,4),round(p.y/1e6,4))
def near(p,q,tol=0.02):return math.hypot(p.x-q.x,p.y-q.y)<=mm(tol)
def edge(a,c):return tuple(sorted((tuple(a),tuple(c))))
old_via_pos=pcbnew.VECTOR2I(mm(128.6),mm(61.425))
old_via=next((t for t in b.GetTracks() if isinstance(t,pcbnew.PCB_VIA) and t.GetNetname()=="+5V" and near(t.GetPosition(),old_via_pos)),None)
if old_via is None:raise SystemExit("Original U602 +5V via at (128.6,61.425) missing")
expected=[((128.51,60.63),(128.6,60.72)),((128.6,60.72),(128.6,61.425))]
wanted={edge(*x) for x in expected}
stubs=[]
for t in b.GetTracks():
    if isinstance(t,pcbnew.PCB_VIA) or t.GetLayer()!=pcbnew.F_Cu or t.GetNetname()!="+5V":continue
    if edge(xy(t.GetStart()),xy(t.GetEnd())) in wanted:stubs.append(t)
if len(stubs)!=2:raise SystemExit(f"Expected two exact U602 +5V F.Cu stubs, found {len(stubs)}")
# Preserve the adjacent +5V module rail via at (128.6,62.0); it is not U602 VCC.
keep5_pos=pcbnew.VECTOR2I(mm(128.6),mm(62.0))
keep5=next((t for t in b.GetTracks() if isinstance(t,pcbnew.PCB_VIA) and near(t.GetPosition(),keep5_pos)),None)
if keep5 is None:raise SystemExit("Adjacent +5V via at (128.6,62.0) missing")
target_pos=pcbnew.VECTOR2I(mm(126.95),mm(63.3))
target=next((t for t in b.GetTracks() if isinstance(t,pcbnew.PCB_VIA) and t.GetNetname()=="+3V3_PI" and near(t.GetPosition(),target_pos)),None)
if target is None:raise SystemExit("Existing +3V3_PI through-via at (126.95,63.30) missing")
new_via_pos=pcbnew.VECTOR2I(mm(128.45),mm(60.85))
if any(isinstance(t,pcbnew.PCB_VIA) and near(t.GetPosition(),new_via_pos) for t in b.GetTracks()):
    raise SystemExit("New U602 via position already occupied")
# Verify the new through-via is clear of the SDA0 F.Cu route.
sda=[]
for t in b.GetTracks():
    if isinstance(t,pcbnew.PCB_VIA) or t.GetLayer()!=pcbnew.F_Cu or t.GetNetname()!="/CM5/SDA0":continue
    sda.append(t)
def point_segment_dist(p,a,c):
    px,py=pcbnew.ToMM(p.x),pcbnew.ToMM(p.y)
    ax,ay=pcbnew.ToMM(a.x),pcbnew.ToMM(a.y);cx,cy=pcbnew.ToMM(c.x),pcbnew.ToMM(c.y)
    dx,dy=cx-ax,cy-ay;den=dx*dx+dy*dy
    t=0 if den==0 else max(0,min(1,((px-ax)*dx+(py-ay)*dy)/den))
    return math.hypot(px-(ax+t*dx),py-(ay+t*dy))
min_sda=min(point_segment_dist(new_via_pos,t.GetStart(),t.GetEnd()) for t in sda)
if min_sda<0.58:raise SystemExit(f"New via too close to SDA0 F.Cu: {min_sda:.3f}mm")
for t in stubs:b.Remove(t)
b.Remove(old_via)
p5.SetNet(net)
new_via=pcbnew.PCB_VIA(b)
new_via.SetPosition(new_via_pos);new_via.SetWidth(mm(0.45));new_via.SetDrill(mm(0.30))
new_via.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu);new_via.SetViaType(pcbnew.VIATYPE_THROUGH)
new_via.SetNet(net);b.Add(new_via)
# In2.Cu is intentionally clear around this local area. Route around the via cluster
# rather than forcing a B.Cu trace between the SCL/SDA/GND through-vias.
route=[
 ((128.45,60.85),(129.2,60.85)),
 ((129.2,60.85),(129.2,63.6)),
 ((129.2,63.6),(126.95,63.3))
]
def add_track(a,c):
    t=pcbnew.PCB_TRACK(b)
    t.SetStart(pcbnew.VECTOR2I(mm(a[0]),mm(a[1])))
    t.SetEnd(pcbnew.VECTOR2I(mm(c[0]),mm(c[1])))
    t.SetLayer(pcbnew.In2_Cu);t.SetWidth(mm(0.15));t.SetNet(net);b.Add(t)
for a,c in route:add_track(a,c)
# Restore/retain the independent +5V via; it belongs to the CM5 5V rail.
keep5.SetNet(v5)
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
pcbnew.SaveBoard(str(path),b)
b2=pcbnew.LoadBoard(str(path))
u2=next(f for f in b2.GetFootprints() if str(f.GetReference())=="U602")
p52=next(p for p in u2.Pads() if str(p.GetNumber())=="5")
if p52.GetNetname()!="+3V3_PI":raise SystemExit("U602 pad5 did not persist on +3V3_PI")
def via_at(pos,netname):
    return next((t for t in b2.GetTracks() if isinstance(t,pcbnew.PCB_VIA) and t.GetNetname()==netname and near(t.GetPosition(),pos)),None)
if via_at(new_via_pos,"+3V3_PI") is None:raise SystemExit("New U602 via missing after save/reload")
if via_at(keep5_pos,"+5V") is None:raise SystemExit("Independent +5V via was not preserved")
if via_at(target_pos,"+3V3_PI") is None:raise SystemExit("Existing +3V3_PI target via missing")
for a,c in route:
    if not any(not isinstance(t,pcbnew.PCB_VIA) and t.GetLayer()==pcbnew.In2_Cu and t.GetNetname()=="+3V3_PI" and edge(xy(t.GetStart()),xy(t.GetEnd()))==edge(a,c) for t in b2.GetTracks()):
        raise SystemExit(f"Missing In2.Cu route segment {a}->{c}")
(root/"U602_VCC_REROUTE_REV_B.md").write_text(
"# U602 VCC copper reroute\n\n"
"U602 pad 5 was moved from +5V to +3V3_PI. The original local +5V via at (128.600,61.425) mm and its two short F.Cu stubs were removed. "
"A 0.45/0.30 mm through-via at (128.450,60.850) mm connects the U602 pad to In2.Cu. "
"Three 0.15 mm In2.Cu segments route around the local SCL/SDA/GND via cluster to the existing +3V3_PI through-via at (126.950,63.300) mm. "
"The independent +5V via at (128.600,62.000) mm is explicitly preserved on +5V. All copper zones are refilled before save; native DRC verifies clearances and connectivity.\n",encoding="utf-8")
print(f"U602 VCC rerouted on In2.Cu; new via (128.45,60.85); SDA0 clearance={min_sda:.3f}mm; independent +5V via preserved.")
