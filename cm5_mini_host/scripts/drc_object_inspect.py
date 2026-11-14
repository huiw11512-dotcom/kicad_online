#!/usr/bin/env python3
from pathlib import Path
import sys, json, re
import pcbnew

src=Path(sys.argv[1] if len(sys.argv)>1 else "cm5_mini_host/CM5_MINIMA_3.kicad_pcb")
out=Path(sys.argv[2] if len(sys.argv)>2 else "reports")
out.mkdir(parents=True,exist_ok=True)
b=pcbnew.LoadBoard(str(src))
def mm(v):
    try: return round(pcbnew.ToMM(v),4)
    except Exception: return str(v)
def xy(v):
    try: return [mm(v.x),mm(v.y)]
    except Exception: return str(v)
lines=["# DRC object diagnostics", "",f"KiCad {pcbnew.Version()}",f"Board: {src.name}",""]
for fp in sorted(b.GetFootprints(),key=lambda f:f.GetReference()):
    ref=fp.GetReference()
    if ref not in {"J1","J601","H102","J101","USB701","SW101","J701","M1","M2","M3","M4"}:
        continue
    try: fpid=fp.GetFPID().GetLibItemName()
    except Exception: fpid=str(fp.GetFPID())
    lines += [f"## {ref} — {fp.GetValue()} — {fpid}",f"Position mm: {xy(fp.GetPosition())}",f"Orientation: {fp.GetOrientationDegrees()} deg"]
    for p in fp.Pads():
        try: drill=xy(p.GetDrillSize())
        except Exception: drill="?"
        try: shape=p.GetShape()
        except Exception: shape="?"
        try: attr=p.GetAttribute()
        except Exception: attr="?"
        try: layers=str(p.GetLayerSet().FmtHex())
        except Exception: layers="?"
        lines.append(f"- Pad {p.GetNumber()} net={p.GetNetname()!r} pos={xy(p.GetPosition())} size={xy(p.GetSize())} drill={drill} shape={shape} attr={attr} layers={layers}")
    lines.append("")
(out/"drc_objects.md").write_text("\n".join(lines),encoding="utf-8")
# project board properties
lines=["# Board configuration","",f"Footprints: {len(b.GetFootprints())}",f"Tracks: {sum(1 for t in b.GetTracks() if not isinstance(t,pcbnew.PCB_VIA))}",f"Vias: {sum(1 for t in b.GetTracks() if isinstance(t,pcbnew.PCB_VIA))}",f"Zones: {len(b.Zones())}",""]
try:
    ds=b.GetDesignSettings()
    lines.append(f"Minimum clearance mm: {mm(ds.GetDefault().GetClearance())}")
except Exception as e: lines.append(f"Design settings API note: {e}")
try:
    ns=b.GetNetClasses()
    lines.append(f"Net classes object: {ns}")
    for name in ns.GetClasses().keys():
        nc=ns.GetClasses()[name]
        lines.append(f"- {name}: width={mm(nc.GetTrackWidth())} clearance={mm(nc.GetClearance())} diff_width={mm(nc.GetDiffPairWidth())} diff_gap={mm(nc.GetDiffPairGap())}")
except Exception as e: lines.append(f"Net class API note: {e}")
(out/"board_config.md").write_text("\n".join(lines),encoding="utf-8")
print("\n".join(lines))
print("Wrote",out/"drc_objects.md")
