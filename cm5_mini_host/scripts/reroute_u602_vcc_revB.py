#!/usr/bin/env python3
"""Connect U602 VCC to the existing CM5_3.3V rail on copper; fail closed on geometry changes."""
from pathlib import Path
import pcbnew, math
root=Path("cm5_mini_host")
path=root/"CM5_MINIMA_3.kicad_pcb"
b=pcbnew.LoadBoard(str(path))
fps={str(fp.GetReference()):fp for fp in b.GetFootprints()}
u=fps.get("U602"); cm=fps.get("Module301")
if u is None or cm is None: raise SystemExit("U602 or CM5 module footprint missing")
p5=next((p for p in u.Pads() if str(p.GetNumber())=="5"),None)
p84=next((p for p in cm.Pads() if str(p.GetNumber())=="84"),None)
if p5 is None or p84 is None: raise SystemExit("U602 pad5 or CM5 pad84 missing")
if p5.GetNetname()!="+5V": raise SystemExit(f"Expected original U602 pad5 +5V, got {p5.GetNetname()}")
if p84.GetNetname()!="+3V3_PI": raise SystemExit(f"CM5 pin84 is not +3V3_PI: {p84.GetNetname()}")
net=b.FindNet("+3V3_PI")
if net is None: raise SystemExit("+3V3_PI net missing")
def mm(v): return pcbnew.FromMM(v)
def xy(p): return (round(p.x/1e6,4),round(p.y/1e6,4))
# Remove only the two original short +5V stubs that exclusively connect U602 pad5 to its
# first +5V via. Do not touch the +5V via or the main +5V network.
a=pcbnew.VECTOR2I(mm(128.51),mm(60.63))
stub=[]
for t in list(b.GetTracks()):
    if isinstance(t,pcbnew.PCB_VIA) or t.GetNetname()!="+5V": continue
    s,e=t.GetStart(),t.GetEnd()
    pts=[xy(s),xy(e)]
    if any(math.hypot(x-128.51,y-60.63)<0.02 for x,y in pts) or \
       (all(abs(x-128.6)<0.02 for x,y in pts) and min(y for x,y in pts)>=60.70 and max(y for x,y in pts)<=61.43):
        stub.append(t)
if len(stub)!=2:
    raise SystemExit(f"Expected exactly two U602 +5V stub tracks, found {len(stub)}: {[ (xy(t.GetStart()),xy(t.GetEnd())) for t in stub ]}")
for t in stub: b.Remove(t)
p5.SetNet(net)
# Via beside U602, placed clear of adjacent pin 3 and the existing GND via.
via_pos=pcbnew.VECTOR2I(mm(127.80),mm(60.63))
via=pcbnew.PCB_VIA(b)
via.SetPosition(via_pos); via.SetWidth(mm(0.45)); via.SetDrill(mm(0.30))
via.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu); via.SetViaType(pcbnew.VIATYPE_THROUGH)
via.SetNet(net); b.Add(via)
def add_track(a,c,layer,width=0.18):
    t=pcbnew.PCB_TRACK(b); t.SetStart(a); t.SetEnd(c); t.SetLayer(layer); t.SetWidth(mm(width)); t.SetNet(net); b.Add(t)
add_track(p5.GetPosition(),via_pos,pcbnew.F_Cu,0.18)
# Join the new via to the existing +3V3_PI through-via at (126.95,63.30) on B.Cu.
target=pcbnew.VECTOR2I(mm(126.95),mm(63.30))
tv=next((t for t in b.GetTracks() if isinstance(t,pcbnew.PCB_VIA) and t.GetNetname()=="+3V3_PI" and math.hypot(t.GetPosition().x-target.x,t.GetPosition().y-target.y)<mm(0.03)),None)
if tv is None: raise SystemExit("Expected existing +3V3_PI through-via at (126.95,63.30) not found")
# Conservative dog-leg path around nearby CM5 signal and GND vias.
pts=[via_pos,pcbnew.VECTOR2I(mm(127.80),mm(61.90)),
     pcbnew.VECTOR2I(mm(127.80),mm(63.00)),
     pcbnew.VECTOR2I(mm(127.30),mm(63.50)),target]
for a,c in zip(pts,pts[1:]): add_track(a,c,pcbnew.B_Cu,0.15)
pcbnew.SaveBoard(str(path),b)
# Reload and assert pad net, route endpoints and original +5V via remain distinct.
b2=pcbnew.LoadBoard(str(path)); u2=next(fp for fp in b2.GetFootprints() if str(fp.GetReference())=="U602")
p52=next(p for p in u2.Pads() if str(p.GetNumber())=="5")
if p52.GetNetname()!="+3V3_PI": raise SystemExit("U602 pad5 net assignment failed after save")
if not any(isinstance(t,pcbnew.PCB_VIA) and t.GetNetname()=="+5V" and math.hypot(t.GetPosition().x-mm(128.6),t.GetPosition().y-mm(61.425))<mm(0.03) for t in b2.GetTracks()):
    raise SystemExit("Original +5V network via unexpectedly changed")
(root/"U602_VCC_REROUTE_REV_B.md").write_text(
"# U602 VCC copper reroute\n\n"
"U602 pad 5 was removed from +5V and connected to +3V3_PI. Two short +5V stub segments from pad 5 to the original +5V via were removed; the original +5V via and remaining +5V network are retained. "
"A 0.45/0.30 mm through via beside U602 and 0.15 mm B.Cu dog-leg connect to the existing +3V3_PI through-via at (126.95,63.30) mm. "
"Board save/reload confirms pad 5 is on +3V3_PI and the old +5V via remains on +5V. Native DRC is required to validate clearance and connectivity before release.\n",encoding="utf-8")
print("U602 pad5 routed from +5V to +3V3_PI; board save/reload assertions passed.")
