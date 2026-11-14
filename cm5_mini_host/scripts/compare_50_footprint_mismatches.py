#!/usr/bin/env python3
"""Assess library mismatch DRC warnings by native KiCad pad data, never auto-update.

For every footprint flagged lib_footprint_mismatch in the current board DRC:
 compare PCB-embedded footprint vs project/installed KiCad 10 stock footprint
 for pad numbers/counts, local positions (if API exposes them), dimensions,
 drills, fabrication pad attributes and per-pad mask expansion.
Graphics, silkscreen, Fab, 3D, assembly and BOM remain MANUAL REVIEW.
"""
from pathlib import Path
import re, collections, pcbnew

root=Path("cm5_mini_host")
out=Path("reports")
out.mkdir(exist_ok=True)
report=(out/"drc.rpt").read_text(errors="replace")
pattern=r'(?m)^\[lib_footprint_mismatch\]:[^\n]*\n(?:[ \t]+[^\n]*\n)*'
blocks=re.findall(pattern,report)
refs=[]
for block in blocks:
    m=re.search(r'Footprint ([A-Za-z0-9_*.-]+)',block)
    if m:refs.append(m.group(1))
refs=list(dict.fromkeys(refs))
if len(refs)!=50:raise SystemExit(f"Expected 50 KiCad lib footprint mismatches, found {len(refs)}")
board=pcbnew.LoadBoard(str(root/"CM5_MINIMA_3.kicad_pcb"))
footprints={f.GetReference():f for f in board.GetFootprints()}
io=pcbnew.PCB_IO_KICAD_SEXPR()
def pad_geom(fp):
    res=[]
    complete=True
    for p in fp.Pads():
        if hasattr(p,"GetFPRelativePosition"):
            pos=p.GetFPRelativePosition()
        else:
            complete=False
            pos=p.GetPosition()
        drill=p.GetDrillSize()
        res.append((
            str(p.GetNumber()),int(p.GetAttribute()),int(p.GetShape()),
            int(pos.x),int(pos.y),
            int(p.GetSize().x),int(p.GetSize().y),
            int(drill.x),int(drill.y),
        ))
    return sorted(res),complete
def pad_process(fp):
    vals=[]
    for p in fp.Pads():
        vals.append((str(p.GetNumber()),int(p.GetLocalSolderMaskMargin()),
                     int(p.GetLocalSolderPasteMargin())))
    return sorted(vals)
rows=[]
for ref in refs:
    fp=footprints.get(ref)
    if fp is None:
        rows.append((ref,"NO_PCB_REF","","","Cannot find reference in PCB"))
        continue
    lib=str(fp.GetFPID().GetLibNickname())
    name=str(fp.GetFPID().GetLibItemName())
    base=(root/(lib+".pretty")) if (root/(lib+".pretty")).exists() else (Path("/usr/share/kicad/footprints")/(lib+".pretty"))
    file=base/(name+".kicad_mod")
    if not file.exists():
        rows.append((ref,"MISSING_LIBRARY",f"{lib}:{name}","",str(file)))
        continue
    try:
        f=io.FootprintLoad(str(base),name)
        if f is None:raise ValueError("KiCad PCB_IO FootprintLoad returned None")
        a,ap=pad_geom(fp); b,bp=pad_geom(f)
        aa=pad_process(fp); bb=pad_process(f)
        if not ap or not bp:
            category="PAD_XY_API_UNAVAILABLE"
            detail="Local pad coordinate API absent; cannot make position comparison"
        elif len(a)!=len(b) or sorted(x[0] for x in a)!=sorted(x[0] for x in b):
            category="PAD_NUMBER_OR_COUNT"
            detail=f"PCB {len(a)} pads vs library {len(b)} pads"
        elif a!=b:
            category="PAD_GEOMETRY"
            diff=sum(x!=y for x,y in zip(a,b))
            detail=f"Pad attr, XY, size, shape or drill differs in {diff} sorted entries"
        elif aa!=bb:
            category="MASK_PASTE_MARGIN"
            detail="Pad copper/drill/position identical; local soldermask/paste margin differs"
        else:
            category="NON_PAD_VERSION_OR_GRAPHICS"
            detail="Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata"
        rows.append((ref,category,f"{lib}:{name}",f"{len(a)}/{len(b)}",detail))
    except Exception as exc:
        rows.append((ref,"LIBRARY_LOAD_ERROR",f"{lib}:{name}","",f"{type(exc).__name__}: {exc}"))
counts=collections.Counter(x[1] for x in rows)
lines=[
    "# KiCad 10 footprint-library mismatch pad audit",
    "",
    "Source: current cm5_mini_host KiCad 10 DRC (50 lib_footprint_mismatch warnings).",
    "",
    "**This is a comparative audit, not an instruction to replace footprints.**",
    "The audit checks native KiCad 10 pad numbers, local positions, pad shapes/sizes, drill and pad-level mask/paste margins where the API allows it. A visual 3D enclosure and mechanical manufacturer drawing check is still mandatory.",
    "",
    "## Classifications",
    "",
]
for k,n in sorted(counts.items()):
    lines.append(f"- **{k}**: {n}")
lines+=["","## Per-footprint differences","",
        "| Ref | Class | Embedded footprint ID | Pads board/lib | Finding |",
        "|---|---|---|---|---|"]
for ref,cat,fpid,pc,detail in rows:
    lines.append(f"| {ref} | {cat} | {fpid} | {pc} | {detail.replace('|','/')} |")
lines+=["","## DFM interpretation","",
        "- PAD_NUMBER_OR_COUNT / PAD_GEOMETRY are high priority; confirm datasheet pinout and exact purchased reel before any PCB order.",
        "- MASK_PASTE_MARGIN differences require manufacturing process signoff; do not copy stock values blindly, especially J701 0.16mm mask dam.",
        "- NON_PAD_VERSION_OR_GRAPHICS does **not** mean safe: may still change 3D envelope, courtyard, polarity mark or exposed copper wording; review the vendor's mechanical drawing.",
        "- This report did not modify any design files, PCB copper or circuit values.",
        ""]
outpath=root/"FOOTPRINT_MISMATCH_PAD_AUDIT.md"
outpath.write_text("\n".join(lines),encoding="utf-8")
print("Compared",len(rows),"DRC-reported footprints, classes:",dict(counts))
for t in rows:
    if t[1] not in {"NON_PAD_VERSION_OR_GRAPHICS","MASK_PASTE_MARGIN"}:print(*t,sep=" | ")
print("Wrote",outpath)
