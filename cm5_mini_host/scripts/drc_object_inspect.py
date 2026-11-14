#!/usr/bin/env python3
from pathlib import Path
import sys
import pcbnew
src=Path(sys.argv[1] if len(sys.argv)>1 else "cm5_mini_host/CM5_MINIMA_3.kicad_pcb")
out=Path(sys.argv[2] if len(sys.argv)>2 else "reports")
out.mkdir(parents=True,exist_ok=True)
b=pcbnew.LoadBoard(str(src))
def mm(v):
    try:return round(pcbnew.ToMM(v),4)
    except:return str(v)
def xy(v):
    try:return f"({mm(v.x)},{mm(v.y)})"
    except:return str(v)
lines=["# Detailed geometry for critical nets",""]
targets=["/USB_C.D_P","/USB_C.D_N","/CM5/USB2P.D_P","/CM5/USB2P.D_N"]
for net in targets:
    lines += [f"## {net}",""]
    for t in b.GetTracks():
        if t.GetNetname()!=net: continue
        if isinstance(t,pcbnew.PCB_VIA):
            lines.append(f"- VIA at {xy(t.GetPosition())}, dia={mm(t.GetWidth())} mm, drill={mm(t.GetDrill())} mm")
        else:
            typ="ARC" if isinstance(t,pcbnew.PCB_ARC) else "SEG"
            lines.append(f"- {typ} {xy(t.GetStart())} -> {xy(t.GetEnd())}, width={mm(t.GetWidth())} mm, layer={b.GetLayerName(t.GetLayer())}, length={mm(t.GetLength())} mm")
    lines.append("")
for fp in b.GetFootprints():
    for pad in fp.Pads():
        if pad.GetNetname() in targets:
            lines.append(f"PAD {fp.GetReference()}.{pad.GetNumber()} net={pad.GetNetname()} pos={xy(pad.GetPosition())} size={xy(pad.GetSize())}")
lines += ["","## Pad attribute enum"]
for k in dir(pcbnew):
    if k.startswith("PAD_ATTRIB_"): lines.append(f"- {k}={getattr(pcbnew,k)}")
lines += ["","## Copper zones"]
for i,z in enumerate(b.Zones()):
    try: ls=[b.GetLayerName(x) for x in range(pcbnew.PCB_LAYER_ID_COUNT) if z.GetLayerSet().Contains(x)]
    except: ls=["?"]
    try: net=z.GetNetname()
    except: net="?"
    try: pri=z.GetAssignedPriority()
    except: pri="?"
    try: rule=z.GetIsRuleArea()
    except: rule="?"
    lines.append(f"- zone {i}: net={net}, layers={ls}, priority={pri}, rule_area={rule}")
try:
    bb=b.GetBoardEdgesBoundingBox()
    lines += ["","## Board outline bounding box",f"- min={xy(bb.GetOrigin())}, max={xy(bb.GetEnd())}, size={xy(bb.GetSize())}"]
except Exception as e: lines.append(f"Outline API note: {e}")
lines += ["","## Net classes"]
try:
    ncmap=b.GetNetClasses()
    for name in ncmap.keys():
        nc=ncmap[name]
        try: lines.append(f"- {name}: width={mm(nc.GetTrackWidth())} mm, clearance={mm(nc.GetClearance())} mm, diff_width={mm(nc.GetDiffPairWidth())} mm, diff_gap={mm(nc.GetDiffPairGap())} mm")
        except Exception as e: lines.append(f"- {name}: {e}")
except Exception as e: lines.append(str(e))
(out/"critical_geometry.md").write_text("\n".join(lines),encoding="utf-8")
print("\n".join(lines))
