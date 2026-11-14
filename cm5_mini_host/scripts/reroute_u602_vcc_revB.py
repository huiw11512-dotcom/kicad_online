#!/usr/bin/env python3
"""Move U602 VCC from +5V to +3V3_PI using its existing via and a clearance-aware B.Cu route."""
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
# Reuse the existing via at (128.6,61.425) rather than adding a new via near CM5 SDA0.
old_via_pos=pcbnew.VECTOR2I(mm(128.6),mm(61.425))
via=next((t for t in b.GetTracks() if isinstance(t,pcbnew.PCB_VIA) and t.GetNetname()=="+5V" and near(t.GetPosition(),old_via_pos)),None)
if via is None:raise SystemExit("Original U602 +5V through-via at (128.6,61.425) missing")
# Verify the two exact existing F.Cu stubs from U602 pad 5 to this via.
expected=[
 ((128.51,60.63),(128.6,60.72)),
 ((128.6,60.72),(128.6,61.425))
]
def edge(a,c):return tuple(sorted((tuple(a),tuple(c))))
wanted={edge(*x) for x in expected}
stubs=[]
for t in b.GetTracks():
    if isinstance(t,pcbnew.PCB_VIA) or t.GetLayer()!=pcbnew.F_Cu or t.GetNetname()!="+5V":continue
    k=edge(xy(t.GetStart()),xy(t.GetEnd()))
    if k in wanted:stubs.append(t)
if len(stubs)!=2 or {edge(xy(t.GetStart()),xy(t.GetEnd())) for t in stubs}!=wanted:
    raise SystemExit(f"Expected two exact U602 VCC stubs, got {[(xy(t.GetStart()),xy(t.GetEnd())) for t in stubs]}")
# Target is an existing +3V3_PI through-via and the adjacent B.Cu route is kept
# below SDA0 and above PWR_BUT. It skirts the GND via at (128.1,62.85)
# with 0.20 mm nominal copper clearance (min rule 0.13 mm).
target_pos=pcbnew.VECTOR2I(mm(126.95),mm(63.3))
target=next((t for t in b.GetTracks() if isinstance(t,pcbnew.PCB_VIA) and t.GetNetname()=="+3V3_PI" and near(t.GetPosition(),target_pos)),None)
if target is None:raise SystemExit("Existing +3V3_PI through-via at (126.95,63.30) missing")
route=[
 ((128.6,61.425),(128.6,63.5)),
 ((128.6,63.5),(127.4,63.5)),
 ((127.4,63.5),(126.95,63.3))
]
for a,c in route:
    for t in b.GetTracks():
        if isinstance(t,pcbnew.PCB_VIA) or t.GetNetname()!="+3V3_PI" or t.GetLayer()!=pcbnew.B_Cu:continue
        if edge(xy(t.GetStart()),xy(t.GetEnd()))==edge(a,c):
            raise SystemExit("U602 B.Cu reroute already exists; refusing duplicate")
# Change the existing two pad-to-via segments and existing via to +3V3_PI.
for t in stubs:t.SetNet(net)
via.SetNet(net)
p5.SetNet(net)
def add_track(a,c):
    t=pcbnew.PCB_TRACK(b)
    t.SetStart(pcbnew.VECTOR2I(mm(a[0]),mm(a[1])))
    t.SetEnd(pcbnew.VECTOR2I(mm(c[0]),mm(c[1])))
    t.SetLayer(pcbnew.B_Cu);t.SetWidth(mm(0.15));t.SetNet(net);b.Add(t)
for a,c in route:add_track(a,c)
# Refill all copper zones so the new +3V3 tracks have real antipads/clearances
# in the GND and +5V planes before native DRC.
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
pcbnew.SaveBoard(str(path),b)
b2=pcbnew.LoadBoard(str(path))
u2=next(f for f in b2.GetFootprints() if str(f.GetReference())=="U602")
p52=next(p for p in u2.Pads() if str(p.GetNumber())=="5")
if p52.GetNetname()!="+3V3_PI":raise SystemExit("U602 pad5 net did not persist")
v2=next((t for t in b2.GetTracks() if isinstance(t,pcbnew.PCB_VIA) and near(t.GetPosition(),old_via_pos)),None)
if v2 is None or v2.GetNetname()!="+3V3_PI":raise SystemExit("Reused U602 via net did not persist")
if not any(isinstance(t,pcbnew.PCB_VIA) and near(t.GetPosition(),target_pos) and t.GetNetname()=="+3V3_PI" for t in b2.GetTracks()):
    raise SystemExit("Existing +3V3_PI target via lost")
actual=[]
for t in b2.GetTracks():
    if isinstance(t,pcbnew.PCB_VIA) or t.GetLayer()!=pcbnew.B_Cu or t.GetNetname()!="+3V3_PI":continue
    actual.append(edge(xy(t.GetStart()),xy(t.GetEnd())))
for a,c in route:
    if edge(a,c) not in actual:raise SystemExit(f"Missing saved route segment {a}->{c}")
(root/"U602_VCC_REROUTE_REV_B.md").write_text(
"# U602 VCC copper reroute\n\n"
"U602 pad 5 and its existing F.Cu connection were moved from +5V to +3V3_PI. The original through-via at (128.600,61.425) mm was reused; no extra via was added. "
"Three 0.15 mm B.Cu segments connect that via to the existing +3V3_PI through-via at (126.950,63.300) mm via (128.600,63.500) and (127.400,63.500) mm. "
"The path avoids the /CM5/SCL0 and /CM5/SDA0 B.Cu routes and keeps 0.20 mm nominal copper clearance from the GND via at (128.100,62.850) mm. "
"All copper zones were refilled before save. Native KiCad DRC must confirm the final clearances, shorts and unconnected count.\n",encoding="utf-8")
print("U602 pad5, two existing F.Cu stubs and existing via moved to +3V3_PI; 3 B.Cu route segments added; all zones refilled.")
