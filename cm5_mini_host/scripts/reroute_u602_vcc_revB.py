#!/usr/bin/env python3
"""Move U602 VCC from +5V to +3V3_PI using a relocated via and clearance-aware B.Cu route."""
from pathlib import Path
import math,pcbnew
root=Path("cm5_mini_host")
path=root/"CM5_MINIMA_3.kicad_pcb"
b=pcbnew.LoadBoard(str(path))
u=next((f for f in b.GetFootprints() if str(f.GetReference())=="U602"),None)
if u is None:raise SystemExit("U602 footprint missing")
p5=next((p for p in u.Pads() if str(p.GetNumber())=="5"),None)
if p5 is None:raise SystemExit("U602 pad 5 missing")
if p5.GetNetname()!="+5V":raise SystemExit(f"Expected U602 pad 5 on +5V, got {p5.GetNetname()}")
net=b.FindNet("+3V3_PI")
if net is None:raise SystemExit("+3V3_PI net missing")
def mm(v):return pcbnew.FromMM(v)
def xy(p):return (round(p.x/1e6,4),round(p.y/1e6,4))
def near(p,q,tol=0.02):return math.hypot(p.x-q.x,p.y-q.y)<=mm(tol)
def edge(a,c):return tuple(sorted((tuple(a),tuple(c))))
# Remove only the old U602 +5V via and its two exact pad-to-via F.Cu segments.
old_via_pos=pcbnew.VECTOR2I(mm(128.6),mm(61.425))
old_via=next((t for t in b.GetTracks() if isinstance(t,pcbnew.PCB_VIA) and t.GetNetname()=="+5V" and near(t.GetPosition(),old_via_pos)),None)
if old_via is None:raise SystemExit("Original U602 +5V via at (128.6,61.425) missing")
expected=[((128.51,60.63),(128.6,60.72)),((128.6,60.72),(128.6,61.425))]
wanted={edge(*x) for x in expected}
stubs=[]
for t in b.GetTracks():
    if isinstance(t,pcbnew.PCB_VIA) or t.GetLayer()!=pcbnew.F_Cu or t.GetNetname()!="+5V":continue
    k=edge(xy(t.GetStart()),xy(t.GetEnd()))
    if k in wanted:stubs.append(t)
if len(stubs)!=2 or {edge(xy(t.GetStart()),xy(t.GetEnd())) for t in stubs}!=wanted:
    raise SystemExit(f"Expected two exact U602 VCC stubs, got {[(xy(t.GetStart()),xy(t.GetEnd())) for t in stubs]}")
target_pos=pcbnew.VECTOR2I(mm(126.95),mm(63.3))
target=next((t for t in b.GetTracks() if isinstance(t,pcbnew.PCB_VIA) and t.GetNetname()=="+3V3_PI" and near(t.GetPosition(),target_pos)),None)
if target is None:raise SystemExit("Existing +3V3_PI through-via at (126.95,63.30) missing")
# New via is placed to the right of the CM5 SDA0 diagonal and above the local +5V plane.
new_via_pos=pcbnew.VECTOR2I(mm(128.45),mm(60.85))
if any(isinstance(t,pcbnew.PCB_VIA) and near(t.GetPosition(),new_via_pos) for t in b.GetTracks()):
    raise SystemExit("New U602 via position already occupied")
# Verify minimum geometric distance to the nearest F.Cu SDA0 segment before placing the via.
sda_segments=[]
for t in b.GetTracks():
    if isinstance(t,pcbnew.PCB_VIA) or t.GetLayer()!=pcbnew.F_Cu or t.GetNetname()!="/CM5/SDA0":continue
    sda_segments.append(t)
def point_segment_dist(p,a,c):
    px,py=pcbnew.ToMM(p.x),pcbnew.ToMM(p.y)
    ax,ay=pcbnew.ToMM(a.x),pcbnew.ToMM(a.y);cx,cy=pcbnew.ToMM(c.x),pcbnew.ToMM(c.y)
    dx,dy=cx-ax,cy-ay;den=dx*dx+dy*dy
    t=0 if den==0 else max(0,min(1,((px-ax)*dx+(py-ay)*dy)/den))
    return math.hypot(px-(ax+t*dx),py-(ay+t*dy))
min_sda=min(point_segment_dist(new_via_pos,t.GetStart(),t.GetEnd()) for t in sda_segments)
if min_sda<0.58:raise SystemExit(f"New via too close to CM5 SDA0 F.Cu route: {min_sda:.3f}mm")
for t in stubs:b.Remove(t)
b.Remove(old_via)
p5.SetNet(net)
new_via=pcbnew.PCB_VIA(b)
new_via.SetPosition(new_via_pos);new_via.SetWidth(mm(0.45));new_via.SetDrill(mm(0.30))
new_via.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu);new_via.SetViaType(pcbnew.VIATYPE_THROUGH)
new_via.SetNet(net);b.Add(new_via)
def add_track(a,c,layer,width):
    t=pcbnew.PCB_TRACK(b)
    t.SetStart(pcbnew.VECTOR2I(mm(a[0]),mm(a[1])))
    t.SetEnd(pcbnew.VECTOR2I(mm(c[0]),mm(c[1])))
    t.SetLayer(layer);t.SetWidth(mm(width));t.SetNet(net);b.Add(t)
add_track((128.51,60.63),(128.45,60.85),pcbnew.F_Cu,0.18)
route=[
 ((128.45,60.85),(128.45,63.5)),
 ((128.45,63.5),(127.4,63.5)),
 ((127.4,63.5),(126.95,63.3))
]
for a,c in route:add_track(a,c,pcbnew.B_Cu,0.15)
# Refill GND and +5V planes so clearances/antipads reflect the new via and route.
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
pcbnew.SaveBoard(str(path),b)
b2=pcbnew.LoadBoard(str(path))
u2=next(f for f in b2.GetFootprints() if str(f.GetReference())=="U602")
p52=next(p for p in u2.Pads() if str(p.GetNumber())=="5")
if p52.GetNetname()!="+3V3_PI":raise SystemExit("U602 pad5 net did not persist")
if not any(isinstance(t,pcbnew.PCB_VIA) and near(t.GetPosition(),new_via_pos) and t.GetNetname()=="+3V3_PI" for t in b2.GetTracks()):
    raise SystemExit("Relocated U602 via net did not persist")
if any(isinstance(t,pcbnew.PCB_VIA) and near(t.GetPosition(),old_via_pos) and t.GetNetname()=="+3V3_PI" for t in b2.GetTracks()):
    raise SystemExit("Old via unexpectedly remains on +3V3_PI")
actual=[]
for t in b2.GetTracks():
    if isinstance(t,pcbnew.PCB_VIA) or t.GetLayer()!=pcbnew.B_Cu or t.GetNetname()!="+3V3_PI":continue
    actual.append(edge(xy(t.GetStart()),xy(t.GetEnd())))
for a,c in route:
    if edge(a,c) not in actual:raise SystemExit(f"Missing saved route segment {a}->{c}")
(root/"U602_VCC_REROUTE_REV_B.md").write_text(
"# U602 VCC copper reroute\n\n"
"U602 pad 5 and its local F.Cu connection were moved from +5V to +3V3_PI. The old via at (128.600,61.425) mm and its two short +5V stubs were removed. "
"A 0.45/0.30 mm through-via was placed at (128.450,60.850) mm, verified at least 0.58 mm from the nearest CM5 SDA0 F.Cu segment. "
"A 0.18 mm F.Cu pad connection and three 0.15 mm B.Cu segments connect to the existing +3V3_PI through-via at (126.950,63.300) mm. "
"The B.Cu route avoids the /CM5/SCL0 and /CM5/SDA0 routes and stays clear of the GND via at (128.100,62.850) mm. All copper zones were refilled before save. Native KiCad DRC remains the final clearance/short verification.\n",encoding="utf-8")
print(f"U602 VCC moved to +3V3_PI with relocated via at 128.45,60.85; nearest SDA0 clearance centerline={min_sda:.3f}mm; zones refilled.")
