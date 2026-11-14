#!/usr/bin/env python3
"""Inspect exact eight risk-bearing KiCad library discrepancies.
Read-only. Native pcbnew 10.0.x data, actual per-pin local position, pad shape,
copper size, drill, and mask/paste. Do not classify a mechanical NPTH as a
lost signal pad.
"""
from pathlib import Path
from collections import defaultdict
import pcbnew

root=Path("cm5_mini_host")
reps=("U703","U602","C702","R702","R703","U1","J701","Module301")
b=pcbnew.LoadBoard(str(root/"CM5_MINIMA_3.kicad_pcb"))
byref={f.GetReference():f for f in b.GetFootprints()}
io=pcbnew.PCB_IO_KICAD_SEXPR()
def mm(x):return round(pcbnew.ToMM(x),5)
def sig(p):
    a=p.GetFPRelativePosition()
    d=p.GetDrillSize()
    return {
      "number":str(p.GetNumber()),"attr":int(p.GetAttribute()),"shape":int(p.GetShape()),
      "x":mm(a.x),"y":mm(a.y),"sx":mm(p.GetSize().x),"sy":mm(p.GetSize().y),
      "dx":mm(d.x),"dy":mm(d.y),
    }
def key(p):return (p["number"],p["attr"],p["shape"],p["x"],p["y"],p["sx"],p["sy"],p["dx"],p["dy"])
lines=["# High-priority footprint geometry differences (8 components)","",
  "**Source:** verified 50-component KiCad 10 mismatch inventory on MiniHost Rev.A.",
  "Actual KiCad PCB-internal footprints compared to the exact named local/stock library (read-only).",
  "The report compares local pad positions, dimensions, drill and pad type. It does NOT automatically replace any pads, mounts or net routing.",
  ""]
totals={}
for ref in reps:
    fp=byref.get(ref)
    if fp is None:raise SystemExit(f"Missing PCB footprint {ref}")
    name=str(fp.GetFPID().GetLibItemName())
    nick=str(fp.GetFPID().GetLibNickname())
    base=(root/(nick+".pretty")) if (root/(nick+".pretty")).exists() else Path("/usr/share/kicad/footprints")/(nick+".pretty")
    lib=io.FootprintLoad(str(base),name)
    if lib is None:raise SystemExit(f"Cannot load {nick}:{name}")
    ar=[sig(p) for p in fp.Pads()]
    br=[sig(p) for p in lib.Pads()]
    onlypcb=sorted([x for x in ar if key(x) not in {key(v) for v in br}],key=key)
    onlylib=sorted([x for x in br if key(x) not in {key(v) for v in ar}],key=key)
    ap=defaultdict(list);bp=defaultdict(list)
    for x in ar:ap[x["number"]].append(x)
    for x in br:bp[x["number"]].append(x)
    nums=sorted(set(ap)|set(bp))
    rows=[]
    for n in nums:
        a=sorted(ap[n],key=key);z=sorted(bp[n],key=key)
        if a==z:continue
        # present one entry per pad-number group; report duplicates NPTH separately
        if n=="":
            for q in a: rows.append(("PCB-only unnamed NPTH / mechanical",q,None))
            for q in z: rows.append(("Library unnamed NPTH / mechanical",None,q))
        else:
            for k in range(max(len(a),len(z))):
                v=a[k] if k<len(a) else None
                w=z[k] if k<len(z) else None
                if v!=w:rows.append((f"pad {n}",v,w))
    lines+=[f"## {ref} — {nick}:{name}","",
      f"- Actual board pad count: **{len(ar)}**; library pad count: **{len(br)}**",
      f"- Changed individual pad-number groups: **{len(set(r[0] for r in rows))}**",
      f"- Difference category is determined only from pad geometry; actual part datasheet and assembly height still need review",
      ""]
    if len(rows)>100:
        lines.append(f"**Caution:** {len(rows)} pad-level comparisons differ from the library for {ref}; only the first 20 are displayed. This can indicate a different coordinate frame or an alternate footprint revision. Do not assume these are all independent copper errors. Compare connector orientation and physical manufacturer pin map before editing.\n")
        rows=rows[:20]
    lines+=["| Pad | Board x,y (mm) | Library x,y (mm) | Board size / drill (mm) | Library size / drill (mm) | Notes |",
            "|---|---|---|---|---|---|"]
    fmt=lambda p,which:"—" if p is None else (
      f"{p[which[0]]:.5f},{p[which[1]]:.5f}" if len(which)==2 else
      f"{p[which[0]]:.5f}×{p[which[1]]:.5f}; drill {p['dx']:.5f}×{p['dy']:.5f}"
    )
    for label,a,z in rows:
        if a and z:
            notes=[]
            if a["attr"]!=z["attr"]:notes.append("pad type differs")
            if a["shape"]!=z["shape"]:notes.append("pad shape differs")
            if a["x"]!=z["x"] or a["y"]!=z["y"]:notes.append("local position differs")
            if a["sx"]!=z["sx"] or a["sy"]!=z["sy"]:notes.append("copper size differs")
            if a["dx"]!=z["dx"] or a["dy"]!=z["dy"]:notes.append("drill differs")
        else:notes=["unmatched local pad definition (often non-electrical NPTH)"]
        lines.append(f"| {label or '(unnumbered)'} | {fmt(a,['x','y'])} | {fmt(z,['x','y'])} | {fmt(a,['sx','sy','dx'])} | {fmt(z,['sx','sy','dx'])} | {', '.join(notes)} |")
    lines.append("")
    totals[ref]={"count_board":len(ar),"count_lib":len(br),"diff_rows":len(rows)}
lines+=["## Safe decision rule","",
 "- A change solely to unnumbered NPTH may be fixable by restoring local-library consistency **after** the fabrication drill drawing is confirmed.",
 "- Signal pad offsets and dimensions must match the actually purchased device's recommended land pattern, not the newest KiCad default by assumption.",
 "- No KiCad DRC warning should be ignored solely because the parts appear correctly connected; physical component pads can differ while the netlist remains unchanged.",
 ""]
p=root/"EIGHT_FOOTPRINT_PAD_DELTA.md"
p.write_text("\n".join(lines),encoding="utf-8")
print("Per-pad detail report",p,"summary:",totals)
