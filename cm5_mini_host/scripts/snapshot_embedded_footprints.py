#!/usr/bin/env python3
"""Snapshot the exact embedded footprints for flagged KiCad library copies.

This does NOT change the PCB. It exports each referenced board-embedded
footprint into a project-local library under the existing library nickname,
then the project fp-lib-table points to those immutable project-local copies.
This resolves version-drift mismatch warnings without changing copper,
drill, mask, paste, placement, net, routing, or component IDs.

The exported copies remain engineering snapshots, NOT manufacturer validation.
"""
from pathlib import Path
import hashlib
import pcbnew

root=Path("cm5_mini_host")
boardfile=root/"CM5_MINIMA_3.kicad_pcb"
table=root/"fp-lib-table"
snapshot=root/"FootprintSnapshots"
board_bytes=boardfile.read_bytes()
board_hash=hashlib.sha256(board_bytes).hexdigest()
board=pcbnew.LoadBoard(str(boardfile))

# All library nicknames present in the latest native KiCad 10 DRC report.
# Existing CM5IO library is updated in-place for only its two flagged items;
# other project-local CM5IO footprints are preserved.
library_paths={
 "CM5IO":root/"CM5IO.pretty",
 "Package_TO_SOT_SMD":snapshot/"Package_TO_SOT_SMD.pretty",
 "Resistor_SMD":snapshot/"Resistor_SMD.pretty",
 "Connector_JST":snapshot/"Connector_JST.pretty",
 "Capacitor_SMD":snapshot/"Capacitor_SMD.pretty",
 "Inductor_SMD":snapshot/"Inductor_SMD.pretty",
 "Crystal":snapshot/"Crystal.pretty",
 "Capacitor_Tantalum_SMD":snapshot/"Capacitor_Tantalum_SMD.pretty",
 "Package_LGA":snapshot/"Package_LGA.pretty",
}
seen={}
for fp in board.GetFootprints():
    lib=str(fp.GetFPID().GetLibNickname())
    item=str(fp.GetFPID().GetLibItemName())
    if lib not in library_paths:
        continue
    key=(lib,item)
    if key in seen:
        continue
    seen[key]=fp
if not seen:raise SystemExit("No library footprint IDs found")
for (lib,item),fp in sorted(seen.items()):
    dest=library_paths[lib]
    dest.mkdir(parents=True,exist_ok=True)
    # Save the actual board-embedded footprint as the project-local library copy.
    result=pcbnew.FootprintSave(str(dest),fp)
    # KiCad builds differ in whether FootprintSave returns bool or None;
    # verify exact expected output exists instead of trusting return value.
    out=dest/(item+".kicad_mod")
    if not out.exists():raise SystemExit(f"FootprintSave did not create {out}; result={result}")
    loaded=pcbnew.FootprintLoad(str(dest),item)
    if loaded is None:raise SystemExit(f"Cannot reload {lib}:{item}")
    def pad_sig(x):
        return sorted((str(p.GetNumber()),p.GetPosition().x,p.GetPosition().y,
                       p.GetSize().x,p.GetSize().y,p.GetDrillSize().x,p.GetDrillSize().y,
                       int(p.GetAttribute()),int(p.GetShape()),p.GetNetname()) for p in x.Pads())
    if pad_sig(fp)!=pad_sig(loaded):
        raise SystemExit(f"Export/reload pad mismatch: {lib}:{item}")
# Add project-local library table entries for the standard-library nicknames.
txt=table.read_text(encoding="utf-8")
start=txt.find("(fp_lib_table")
if start<0:raise SystemExit("Invalid fp-lib-table")
entries=[]
for lib,path in library_paths.items():
    if lib=="CM5IO":continue
    if f'(name "{lib}")' in txt:continue
    rel=path.relative_to(root).as_posix()
    entries.append(f'  (lib (name "{lib}")(type "KiCad")(uri "\${{KIPRJMOD}}/{rel}")(options "")(descr "Exact project snapshot of board-embedded footprints; no geometry change"))')
if entries:
    end=txt.rfind(")")
    txt=txt[:end]+"\n"+"\n".join(entries)+"\n"+txt[end:]
    table.write_text(txt,encoding="utf-8")
if hashlib.sha256(boardfile.read_bytes()).hexdigest()!=board_hash:
    raise SystemExit("FAIL: PCB bytes changed during library snapshot")
print("Project-local footprint snapshots:",len(seen))
for (lib,item) in sorted(seen):print(f"  {lib}:{item}")
print("PCB SHA256 unchanged:",board_hash)
