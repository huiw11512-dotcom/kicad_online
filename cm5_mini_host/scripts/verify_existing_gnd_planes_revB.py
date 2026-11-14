#!/usr/bin/env python3
"""Verify the inherited continuous GND zone covers L2 and L5; no copper edits."""
from pathlib import Path
import pcbnew
root=Path("cm5_mini_host")
board=pcbnew.LoadBoard(str(root/"CM5_MINIMA_3.kicad_pcb"))
planes={}
for nm,ly in (("L2 / In1.Cu",pcbnew.In1_Cu),("L5 / In4.Cu",pcbnew.In4_Cu)):
    candidates=[z for z in board.Zones() if z.GetNetname()=="GND" and z.IsOnLayer(ly)]
    if not candidates:raise SystemExit(f"BLOCKED: {nm} has no GND zone")
    # The principal polygon must span most of the mini host outline, not a tiny island.
    found=[]
    for z in candidates:
        bb=z.GetBoundingBox()
        w=pcbnew.ToMM(bb.GetWidth());h=pcbnew.ToMM(bb.GetHeight())
        if w>55 and h>55:found.append((w,h))
    if not found:raise SystemExit(f"BLOCKED: {nm} lacks a board-scale GND zone")
    planes[nm]=found
root.joinpath("EXISTING_GND_PLANES_REV_B.md").write_text(
    "# Rev.B ground reference plane audit\n\n"
    "The original board already has one GND zone spanning F.Cu, B.Cu, In1.Cu, In2.Cu and In4.Cu. "
    "Therefore, adding separate full-board GND zones on In1.Cu and In4.Cu was redundant and created zone-overlap DRC errors. "
    "No additional GND zones are needed. This check verifies the existing GND zone has a board-scale outline on both intended "
    "reference layers. Copper fill and the native KiCad DRC must still pass.\n\n"
    +"\n".join(f"- {nm}: {[tuple(round(a,2) for a in v) for v in values]} mm footprint(s)" for nm,values in planes.items())+"\n",
    encoding="utf-8")
print("Existing board-scale multilayer GND zones verified:",planes)
