#!/usr/bin/env python3
"""Read-only inventory of multiple embedded pad geometries sharing one FPID."""
from pathlib import Path
from collections import defaultdict
import json,hashlib,pcbnew
root=Path("cm5_mini_host")
board=pcbnew.LoadBoard(str(root/"CM5_MINIMA_3.kicad_pcb"))
groups=defaultdict(lambda:defaultdict(list))
details=defaultdict(dict)
def signature(fp):
    pads=[]
    for p in fp.Pads():
        pos=p.GetFPRelativePosition();size=p.GetSize();dr=p.GetDrillSize()
        pads.append((str(p.GetNumber()),int(p.GetAttribute()),int(p.GetShape()),
                     int(pos.x),int(pos.y),int(size.x),int(size.y),int(dr.x),int(dr.y)))
    return tuple(sorted(pads))
for fp in board.GetFootprints():
    lib=str(fp.GetFPID().GetLibNickname());name=str(fp.GetFPID().GetLibItemName())
    if not name:continue
    sig=signature(fp)
    digest=hashlib.sha256(repr(sig).encode()).hexdigest()[:12]
    groups[(lib,name)][digest].append(str(fp.GetReference()))
    details[(lib,name)][digest]=[
        {"pad":str(p.GetNumber()),"type":int(p.GetAttribute()),"shape":int(p.GetShape()),
         "x_mm":round(pcbnew.ToMM(p.GetFPRelativePosition().x),5),
         "y_mm":round(pcbnew.ToMM(p.GetFPRelativePosition().y),5),
         "sx_mm":round(pcbnew.ToMM(p.GetSize().x),5),
         "sy_mm":round(pcbnew.ToMM(p.GetSize().y),5),
         "drill_x_mm":round(pcbnew.ToMM(p.GetDrillSize().x),5),
         "drill_y_mm":round(pcbnew.ToMM(p.GetDrillSize().y),5)}
        for p in sorted(fp.Pads(),key=lambda x:(str(x.GetNumber()),x.GetFPRelativePosition().x,x.GetFPRelativePosition().y))
    ]
rows=[]
for (lib,name),variants in sorted(groups.items()):
    if len(variants)>1:
        rows.append({"library":lib,"footprint":name,
                     "variants":[{"signature":h,"references":sorted(refs),
                         "pads":details[(lib,name)][h]} for h,refs in sorted(variants.items())]})
md=["# Multiple embedded footprint variants sharing the same library ID","",
    "Read-only KiCad 10.0.8 analysis of the native PCB. Local pad coordinates, pad number/type/shape, copper dimensions and drill are included in each signature. No board/library files were changed.",""]
for item in rows:
    md += [f"## {item['library']}:{item['footprint']}",""]
    for v in item["variants"]:
        md.append(f"- Signature {v['signature']}: references {', '.join(v['references'])}")
        md.append("  - Pads: "+", ".join(f"{p['pad']}@({p['x_mm']},{p['y_mm']}) {p['sx_mm']}x{p['sy_mm']} mm" for p in v["pads"]))
    md.append("")
(root/"FOOTPRINT_VARIANT_CONFLICTS.md").write_text("\n".join(md)+"\n",encoding="utf-8")
(root/"FOOTPRINT_VARIANT_CONFLICTS.json").write_text(json.dumps(rows,indent=2)+"\n",encoding="utf-8")
print("Multiple-variant library IDs:",len(rows))
for item in rows:print(item["library"],item["footprint"],item["variants"])
