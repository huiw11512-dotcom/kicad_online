#!/usr/bin/env python3
"""Snapshot embedded footprints into local libraries without changing copper geometry."""
from pathlib import Path
from collections import defaultdict
import json,re,hashlib,shutil,pcbnew

root=Path("cm5_mini_host")
board_path=root/"CM5_MINIMA_3.kicad_pcb"
want={"CM5IO","EasyEDA","Samacsys","_pico","Package_TO_SOT_SMD","Resistor_SMD",
      "Connector_JST","Capacitor_SMD","Inductor_SMD","Crystal",
      "Capacitor_Tantalum_SMD","Package_LGA"}
board=pcbnew.LoadBoard(str(board_path))

def pad_sig(fp):
    out=[]
    for p in fp.Pads():
        pos=p.GetFPRelativePosition(); size=p.GetSize(); drill=p.GetDrillSize()
        layers=str(p.GetLayerSet().FmtHex()) if hasattr(p.GetLayerSet(),"FmtHex") else str(p.GetLayerSet())
        raw_mask=p.GetLocalSolderMaskMargin() if hasattr(p,"GetLocalSolderMaskMargin") else None
        mask=0 if raw_mask is None else int(raw_mask)
        out.append((str(p.GetNumber()),int(p.GetAttribute()),int(p.GetShape()),
                    int(pos.x),int(pos.y),int(size.x),int(size.y),int(drill.x),int(drill.y),mask,layers))
    return tuple(sorted(out))

def state(b):
    result={}
    for fp in b.GetFootprints():
        ref=str(fp.GetReference()); pads=[]
        for p in fp.Pads():
            pos=p.GetPosition(); rel=p.GetFPRelativePosition(); size=p.GetSize(); drill=p.GetDrillSize()
            pads.append((str(p.GetNumber()),str(p.GetNetname()),int(pos.x),int(pos.y),
                         int(rel.x),int(rel.y),int(size.x),int(size.y),int(drill.x),int(drill.y)))
        result[ref]=(str(fp.GetValue()),int(fp.GetPosition().x),int(fp.GetPosition().y),
                     int(fp.GetOrientationDegrees()),tuple(sorted(pads)))
    return result

before=state(board); track_count=len(board.GetTracks()); zone_count=len(board.Zones()); net_count=board.GetNetCount()
groups=defaultdict(lambda:defaultdict(list))
for fp in board.GetFootprints():
    nick=str(fp.GetFPID().GetLibNickname()); name=str(fp.GetFPID().GetLibItemName())
    if nick in want:groups[(nick,name)][pad_sig(fp)].append(fp)

io=pcbnew.PCB_IO_KICAD_SEXPR() if hasattr(pcbnew,"PCB_IO_KICAD_SEXPR") else pcbnew.PCB_IO()
if io is None:raise SystemExit("KiCad PCB_IO unavailable")
exports=defaultdict(dict); updates=[]
for (nick,name),variants in sorted(groups.items()):
    ordered=sorted(variants.items(),key=lambda x:(-len(x[1]),sorted(str(f.GetReference()) for f in x[1])))
    for idx,(sig,instances) in enumerate(ordered):
        refs=sorted(str(f.GetReference()) for f in instances)
        newname=name if idx==0 else name+"__"+"__".join(refs)
        if newname in exports[nick] and exports[nick][newname][0]!=sig:
            raise SystemExit(f"Footprint variant name collision {nick}:{newname}")
        for fp in instances:
            old=f"{nick}:{name}"
            if newname!=name:
                fp.SetFPID(pcbnew.LIB_ID(nick,newname))
                updates.append({"reference":str(fp.GetReference()),"old":old,"new":f"{nick}:{newname}"})
        exports[nick][newname]=(sig,instances[0],refs)

def expr_end(s,k):
    d=0;q=False;e=False
    for i in range(k,len(s)):
        c=s[i]
        if q:
            if e:e=False
            elif c=="\\":e=True
            elif c=='"':q=False
        elif c=='"':q=True
        elif c=='(':d+=1
        elif c==')':
            d-=1
            if d==0:return i+1
    raise ValueError("Unbalanced schematic S-expression")

for u in updates:
    ref,old,new=u["reference"],u["old"],u["new"]; found=0
    for sch in sorted(root.glob("*.kicad_sch")):
        s=sch.read_text(encoding="utf-8"); token=f'(property "Reference" "{ref}"'
        if token not in s:continue
        pos=s.index(token); start=s.rfind("\n\t(symbol",0,pos)+2
        if start<2:raise SystemExit(f"Cannot locate schematic symbol for {ref}")
        end=expr_end(s,start); block=s[start:end]
        oldprop=f'(property "Footprint" "{old}"'
        if block.count(oldprop)!=1:raise SystemExit(f"{ref}: expected exactly one {old} footprint property")
        block=block.replace(oldprop,f'(property "Footprint" "{new}"',1)
        sch.write_text(s[:start]+block+s[end:],encoding="utf-8"); found+=1
    if found!=1:raise SystemExit(f"{ref}: expected one schematic symbol instance, found {found}")

base=root/"FootprintSnapshots"
if base.exists():shutil.rmtree(base)
base.mkdir()
rows=[]
for nick,items in sorted(exports.items()):
    libdir=base/(nick+".pretty"); libdir.mkdir()
    for name,(sig,fp,refs) in sorted(items.items()):
        io.FootprintSave(str(libdir),fp)
        path=libdir/(name+".kicad_mod")
        if not path.exists():raise SystemExit(f"Missing exported footprint {path}")
        loaded=io.FootprintLoad(str(libdir),name)
        if loaded is None or pad_sig(loaded)!=sig:raise SystemExit(f"Footprint roundtrip mismatch {nick}:{name}")
        rows.append({"library":nick,"footprint":name,"references":refs,"pad_count":len(fp.Pads()),
                     "pad_signature":hashlib.sha256(repr(sig).encode()).hexdigest()})

table=["(fp_lib_table)"]
table=["(fp_lib_table"]
for nick in sorted(want):
    if nick in exports:
        table.append(f'  (lib (name "{nick}")(type "KiCad")(uri "${{KIPRJMOD}}/FootprintSnapshots/{nick}.pretty")(options "")(descr "Exact embedded board footprint snapshot; vendor validation separate"))')
table.append(")")
(root/"fp-lib-table").write_text("\n".join(table)+"\n",encoding="utf-8")
pcbnew.SaveBoard(str(board_path),board)
after_board=pcbnew.LoadBoard(str(board_path))
after=state(after_board)
if before!=after:raise SystemExit("FAIL: pad/net/position/value changed during footprint ID normalization")
if len(after_board.GetTracks())!=track_count or len(after_board.Zones())!=zone_count or after_board.GetNetCount()!=net_count:
    raise SystemExit("FAIL: tracks, zones or net count changed")
for fp in after_board.GetFootprints():
    nick=str(fp.GetFPID().GetLibNickname()); name=str(fp.GetFPID().GetLibItemName())
    if nick in want and name not in exports[nick]:raise SystemExit(f"Missing project-local footprint {nick}:{name}")
(root/"FOOTPRINT_SNAPSHOT_REV_B.json").write_text(json.dumps(rows,indent=2)+"\n",encoding="utf-8")
(root/"FOOTPRINT_SNAPSHOT_REV_B_AUDIT.md").write_text(
    "# Rev.B exact embedded-footprint snapshot audit\n\n"
    f"- Board footprints: {len(before)}\n- Unique local footprint definitions: {len(rows)}\n"
    f"- Split duplicate-ID variants: {len(updates)} instances\n- Tracks unchanged: {track_count}\n"
    f"- Zones unchanged: {zone_count}\n- Nets unchanged: {net_count}\n\n"
    "KiCad save/reload preserved all pad numbers, pad types/shapes, local and world coordinates, copper sizes, drills and net assignments. This removes ambiguity between board-embedded geometry and installed library versions; it does NOT certify manufacturer land patterns, paste/mask, body/courtyard, sourcing or assembly fit.\n\n"
    "## Split variants\n\n"+"\n".join(f"- {u['reference']}: {u['old']} -> {u['new']}" for u in updates)+"\n",encoding="utf-8")
print(f"Exported {len(rows)} exact footprints across {len(exports)} libraries; renamed {len(updates)} variant instances.")
print(f"Board invariants passed: {len(before)} footprints, {track_count} tracks, {zone_count} zones, {net_count} nets.")
