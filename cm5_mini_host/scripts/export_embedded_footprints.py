#!/usr/bin/env python3
"""Extract *board-embedded* missing custom footprints to project-local KiCad libraries.
This is a provenance-preserving engineering snapshot, NOT manufacturer validation.
"""
from pathlib import Path
from collections import defaultdict
import json, pcbnew

root=Path("cm5_mini_host")
board=pcbnew.LoadBoard(str(root/"CM5_MINIMA_3.kicad_pcb"))
want={"EasyEDA","Samacsys","_pico"}
io=pcbnew.IO_MGR.PluginFind(pcbnew.IO_MGR.KICAD_SEXPR)
assert io is not None, "KiCad footprint I/O plugin unavailable"
libs=defaultdict(dict)
for fp in board.GetFootprints():
    fid=fp.GetFPID()
    nick=str(fid.GetLibNickname())
    name=str(fid.GetLibItemName())
    if nick not in want: continue
    if not name: raise RuntimeError(f"Blank footprint name on {fp.GetReference()}")
    key=(nick,name)
    p=libs[nick].get(name)
    sig=lambda f: sorted((str(x.GetNumber()),int(x.GetAttribute()),
                         int(x.GetSize().x),int(x.GetSize().y),
                         int(x.GetDrillSize().x),int(x.GetDrillSize().y))
                         for x in f.Pads())
    if p is not None and sig(p)!=sig(fp):
        raise RuntimeError(f"Footprint {key} differs across board copies; manual review necessary")
    libs[nick][name]=fp

summary=[]
for nick in sorted(want):
    directory=root/(nick+".pretty")
    directory.mkdir(parents=True,exist_ok=True)
    for name,fp in sorted(libs[nick].items()):
        # KiCad serializer exports a standalone .kicad_mod from the embedded board copy.
        io.FootprintSave(str(directory),fp)
        exported=directory/(name+".kicad_mod")
        if not exported.exists(): raise RuntimeError(f"No exported file: {exported}")
        loaded=io.FootprintLoad(str(directory),name)
        if loaded is None: raise RuntimeError(f"Roundtrip library load failed: {nick}:{name}")
        sig=lambda f: sorted((str(x.GetNumber()),int(x.GetAttribute()),
                              int(x.GetSize().x),int(x.GetSize().y),
                              int(x.GetDrillSize().x),int(x.GetDrillSize().y))
                              for x in f.Pads())
        if sig(fp)!=sig(loaded):
            raise RuntimeError(f"Pad geometry changed on library roundtrip: {nick}:{name}")
        summary.append({"library":nick,"footprint":name,
                        "reference":str(fp.GetReference()),"pads":len(fp.Pads()),
                        "file":str(exported)})
        print(nick,name,"pads",len(fp.Pads()))
assert len(summary)>=5, f"Suspiciously few custom footprints: {len(summary)}"

# Keep existing CM5IO and extend, rather than replacing it.
table='(fp_lib_table\n'
for nick in ("CM5IO","EasyEDA","Samacsys","_pico"):
    table+=f'  (lib (name "{nick}")(type "KiCad")(uri "${{KIPRJMOD}}/{nick}.pretty")(options "")(descr "Project local — board-embedded snapshot"))\n'
table+=')\n'
(root/"fp-lib-table").write_text(table,encoding="utf-8")
(root/"FOOTPRINT_SNAPSHOT.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
(root/"FOOTPRINT_LIBRARIES.md").write_text("""# Local footprint provenance
These footprints were **recovered from embedded PCB geometry** of the attributed CM5 MINIMA Rev3 baseline, not redrawn, verified against datasheets or confirmed as stocked parts. They are provided to make the editable board reproducible on a fresh KiCad installation and in web viewers. Source is the same CERN-OHL-S-2.0 licensed upstream design linked from README.

The extraction script checks every unique footprint's pad number, pad type, copper size and drill size by saving to and reloading from the KiCad library. **It does not validate the manufacturer's body, courtyard, stencil, plating or placement**. Do not fabricate until physical drawings, 3D height and pin mapping are checked.

See `FOOTPRINT_SNAPSHOT.json` for each footprint and its source reference.
""",encoding="utf-8")
print(f"Exported and roundtrip checked {len(summary)} unique footprints across {len(want)} libraries.")
