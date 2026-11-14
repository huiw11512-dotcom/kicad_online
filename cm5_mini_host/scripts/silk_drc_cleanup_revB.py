#!/usr/bin/env python3
"""Move DRC-clipped/overlapping footprint body graphics from silk to Fab.
Reference/value text is retained on silk. Copper, pads, nets, drills and placement are untouched.
"""
from pathlib import Path
import math,pcbnew
root=Path("cm5_mini_host")
p=root/"CM5_MINIMA_3.kicad_pcb"
b=pcbnew.LoadBoard(str(p))
targets={
 "J1":("F.SilkS","F.Fab"),
 "J101":("F.SilkS","F.Fab"),
 "J701":("F.SilkS","F.Fab"),
 "J501":("F.SilkS","F.Fab"),
 "USB701":("F.SilkS","F.Fab"),
 "SW501":("F.SilkS","F.Fab"),
 "Module301":("B.SilkS","B.Fab"),
 "SW101":("B.SilkS","B.Fab"),
 "C702":("F.SilkS","F.Fab"),
 "TP101":("F.SilkS","F.Fab"),
 "U702":("F.SilkS","F.Fab"),
}
layer_ids={
 "F.SilkS":pcbnew.F_SilkS,"B.SilkS":pcbnew.B_SilkS,
 "F.Fab":pcbnew.F_Fab,"B.Fab":pcbnew.B_Fab,
}
byref={str(fp.GetReference()):fp for fp in b.GetFootprints()}
missing=set(targets)-set(byref)
if missing:raise SystemExit(f"Missing target footprints: {sorted(missing)}")
moved={}
for ref,(src_name,dst_name) in targets.items():
    fp=byref[ref]; src=layer_ids[src_name]; dst=layer_ids[dst_name]; count=0
    for item in list(fp.GraphicalItems()):
        if item.GetLayer()==src and isinstance(item,pcbnew.PCB_SHAPE):
            item.SetLayer(dst); count+=1
    moved[ref]=count

# One board-level F.SilkS segment is the remaining non-footprint overlap at (130.13,62.07).
# Find it geometrically and fail closed if the source board no longer matches the audited item.
target=pcbnew.VECTOR2I(pcbnew.FromMM(130.13),pcbnew.FromMM(62.07))
def dist_point_segment(p,a,c):
    px,py=float(p.x),float(p.y); ax,ay=float(a.x),float(a.y); cx,cy=float(c.x),float(c.y)
    dx,dy=cx-ax,cy-ay
    den=dx*dx+dy*dy
    t=0 if den==0 else max(0,min(1,((px-ax)*dx+(py-ay)*dy)/den))
    return math.hypot(px-(ax+t*dx),py-(ay+t*dy))
candidates=[]
for item in b.GetDrawings():
    if not isinstance(item,pcbnew.PCB_SHAPE) or item.GetLayer()!=pcbnew.F_SilkS:continue
    try:
        a=item.GetStart(); c=item.GetEnd()
    except Exception:
        continue
    d=dist_point_segment(target,a,c)
    candidates.append((d,item))
candidates.sort(key=lambda x:x[0])
if not candidates or candidates[0][0]>pcbnew.FromMM(0.15):
    nearest=[(round(pcbnew.ToMM(d),4),str(type(it).__name__)) for d,it in candidates[:5]]
    raise SystemExit(f"Cannot identify audited board-level silk segment near (130.13,62.07); nearest={nearest}")
d,item=candidates[0]
item.SetLayer(pcbnew.F_Fab)
b.Save(str(p))
(root/"SILK_DFM_CLEANUP_REV_B.md").write_text(
    "# Rev.B silkscreen DFM cleanup\n\n"
    "Moved clipped or overlapping footprint body graphics from silkscreen to the corresponding fabrication layer; reference/value text remains on silkscreen. "
    "This preserves component outlines and orientation marks in assembly artwork while keeping the board-edge and label clearances manufacturable.\n\n"
    "## Footprints\n\n"+"\\n".join(f"- {ref}: {count} graphical primitives moved to Fab" for ref,count in sorted(moved.items()))+
    f"\\n\\n- Board-level silk segment nearest (130.13,62.07) mm moved to F.Fab (distance {pcbnew.ToMM(d):.4f} mm).\\n\\n"
    "No copper, pads, tracks, vias, zones, drills, nets, component placement or reference/value text was changed.\\n",encoding="utf-8")
print("Moved footprint silk graphics to Fab:",moved)
print(f"Moved audited board-level silk segment; distance={pcbnew.ToMM(d):.4f} mm")
