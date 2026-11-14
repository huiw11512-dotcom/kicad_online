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
lines=["# Footprint inventory and DRC object diagnostics","",f"KiCad {pcbnew.Version()}",f"Board: {src.name}",""]
nicks=set()
for fp in sorted(b.GetFootprints(),key=lambda f:f.GetReference()):
    try: nick=str(fp.GetFPID().GetLibNickname()); name=str(fp.GetFPID().GetLibItemName())
    except: nick=""; name=""
    nicks.add(nick)
    try: bb=fp.GetBoundingBox(True,True); box=f"{xy(bb.GetOrigin())}..{xy(bb.GetEnd())}"
    except: box="?"
    lines.append(f"- {fp.GetReference():8s} {fp.GetValue():32s} lib={nick}:{name} pos={xy(fp.GetPosition())} box={box}")
lines += ["","## Used footprint library nicknames",*["- "+n for n in sorted(nicks)]]
lines += ["","## Critical footprint pad details"]
for fp in sorted(b.GetFootprints(),key=lambda f:f.GetReference()):
    ref=fp.GetReference()
    if ref not in {"J1","J601","H101","H102","H103","J101","USB701","SW101","J701","U702","L701","R704","R705","R706","C707"}:
        continue
    try: fpid=f"{fp.GetFPID().GetLibNickname()}:{fp.GetFPID().GetLibItemName()}"
    except: fpid=str(fp.GetFPID())
    lines += [f"### {ref} — {fp.GetValue()} — {fpid}",f"Position mm: {xy(fp.GetPosition())}"]
    for p in fp.Pads():
        num=p.GetNumber()
        if ref=="J701" and not (num.startswith("M") or num.startswith("S") or num in {"1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","67","68","69","70","71","72","73","74","75"}):
            continue
        try: drill=xy(p.GetDrillSize())
        except: drill="?"
        try: attr=p.GetAttribute()
        except: attr="?"
        lines.append(f"- Pad {num!r} net={p.GetNetname()!r} pos={xy(p.GetPosition())} size={xy(p.GetSize())} drill={drill} attr={attr}")
    lines.append("")
lines += ["","## Edge.Cuts geometry near J1"]
for d in b.GetDrawings():
    try:
        if d.GetLayer()!=pcbnew.Edge_Cuts: continue
        if hasattr(d,"GetStart") and hasattr(d,"GetEnd"):
            lines.append(f"- {xy(d.GetStart())} -> {xy(d.GetEnd())} shape={d.GetShape()}")
        else:
            lines.append(f"- drawing {type(d).__name__}: {str(d)[:200]}")
    except Exception as e: lines.append(f"- edge item note: {e}")
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
lines += ["","## Footprint save APIs",str([x for x in dir(pcbnew) if "Footprint" in x and "Save" in x])]
for f in ["/usr/share/kicad/template/fp-lib-table","/usr/share/kicad/template/sym-lib-table"]:
    lines.append(f"- template {f}: {Path(f).exists()}")
for nick in sorted(nicks):
    lines.append(f"- footprint library {nick}: stock={(Path('/usr/share/kicad/footprints')/(nick+'.pretty')).exists()}")
try:
    sample=next(fp for fp in b.GetFootprints() if str(fp.GetFPID().GetLibNickname()) in {"EasyEDA","Samacsys","_pico"})
    testlib=out/"FootprintExportTest.pretty"
    testlib.mkdir(parents=True,exist_ok=True)
    sample_name=str(sample.GetFPID().GetLibItemName())
    pcbnew.FootprintSave(str(testlib/(sample_name+".kicad_mod")),sample)
    saved=list(testlib.glob("*.kicad_mod"))
    lines.append(f"- FootprintSave test: {len(saved)} file(s), "+(saved[0].name if saved else "none"))
    if saved:
        raw=saved[0].read_text(errors="replace")
        lines.append(f"- Saved footprint contains net assignments: {'(net ' in raw}")
except Exception as e:
    lines.append(f"- FootprintSave test failed: {type(e).__name__}: {e}")
(out/"footprint_inventory.md").write_text("\n".join(lines),encoding="utf-8")
print("\n".join(lines))
