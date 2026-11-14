#!/usr/bin/env python3
"""Set ONLY M.2 J701 pad-local mask expansion 0.102 mm -> 0.020 mm.

M.2 Key M 0.5mm pitch has 0.3mm copper pads: the original 0.102mm
per-side solder-mask expansion causes nominal -0.004mm aperture overlap.
For JLCPCB LDI multilayer, 1 oz outer copper, GREEN mask, 0.02mm per-side
gives a nominal 0.16mm mask web (>= factory 0.10mm minimum), with 0.02mm
mask-to-copper registration relief.

No changes to any copper, pads, paste apertures, drill, tracks, net names,
placement or board outline. This profile is not automatically applicable to
2oz/black/white masks or other fabs. Treat factory signoff as mandatory.
"""
from pathlib import Path
import pcbnew

root=Path("cm5_mini_host")
boardfile=root/"CM5_MINIMA_3.kicad_pcb"
libfile=root/"CM5IO.pretty"/"M.2 M Key socket_2230_2242.kicad_mod"
b=pcbnew.LoadBoard(str(boardfile))
item=[f for f in b.GetFootprints() if f.GetReference()=="J701"]
if len(item)!=1: raise SystemExit("J701 expected exactly once")
f=item[0]
libname=str(f.GetFPID().GetLibNickname());name=str(f.GetFPID().GetLibItemName())
if (libname,name)!=("CM5IO","M.2 M Key socket_2230_2242"):
    raise SystemExit(f"Wrong J701 footprint {libname}:{name}")
allpads=list(f.Pads())
pads=[p for p in allpads if p.GetAttribute()==pcbnew.PAD_ATTRIB_SMD]
if len(allpads)!=71 or len(pads)!=69:
    raise SystemExit(f"Expected 69 SMT signal/power pads plus two mechanical NPTHs, got {len(pads)} SMD and {len(allpads)} total")
nm=pcbnew.FromMM
def snapshot(board):
    fp=next(x for x in board.GetFootprints() if x.GetReference()=="J701")
    return sorted((p.GetNumber(),p.GetNetname(),p.GetPosition().x,p.GetPosition().y,
                   p.GetSize().x,p.GetSize().y,p.GetDrillSize().x,p.GetDrillSize().y,
                   p.GetLayerSet().FmtHex()) for p in fp.Pads())
before=snapshot(b)
tracks=len(b.GetTracks());netcount=b.GetNetCount();zones=len(b.Zones())
for pad in pads:
    current=pad.GetLocalSolderMaskMargin()
    if abs(current-nm(0.102))>nm(0.0001):
        raise SystemExit(f"J701 pad {pad.GetNumber()} mask margin expected 0.102, got {pcbnew.ToMM(current):.6f} mm")
    pad.SetLocalSolderMaskMargin(nm(0.020))
pcbnew.SaveBoard(str(boardfile),b)
checked=pcbnew.LoadBoard(str(boardfile))
assert snapshot(checked)==before and len(checked.GetTracks())==tracks and checked.GetNetCount()==netcount and len(checked.Zones())==zones
assert all(abs(p.GetLocalSolderMaskMargin()-nm(0.020))<nm(0.0001)
           for f in checked.GetFootprints() if f.GetReference()=="J701" for p in f.Pads() if p.GetAttribute()==pcbnew.PAD_ATTRIB_SMD)

io=pcbnew.PCB_IO_KICAD_SEXPR()
libdir=root/"CM5IO.pretty"
master=io.FootprintLoad(str(libdir),name)
if master is None:raise SystemExit("Cannot load local project M.2 footprint")
mlist=list(master.Pads())
msmt=[p for p in mlist if p.GetAttribute()==pcbnew.PAD_ATTRIB_SMD]
if len(mlist)!=71 or len(msmt)!=69:raise SystemExit(f"Library M.2 pad count unexpected: total {len(mlist)}, SMT {len(msmt)}")
for pad in msmt:
    if abs(pad.GetLocalSolderMaskMargin()-nm(0.102))>nm(0.0001):
        raise SystemExit("Library pad mask expansion different from board baseline")
    pad.SetLocalSolderMaskMargin(nm(0.020))
io.FootprintSave(str(libdir),master)
master2=io.FootprintLoad(str(libdir),name)
assert master2 is not None and len(list(master2.Pads()))==71
assert all(abs(p.GetLocalSolderMaskMargin()-nm(0.020))<nm(0.0001) for p in master2.Pads() if p.GetAttribute()==pcbnew.PAD_ATTRIB_SMD)
print("J701: 69 local mask margins 0.102 -> 0.020 mm, project footprint synchronized, KiCad read/write verified.")
print("Nominal 0.5 - 0.3 - 2*0.02 = 0.16 mm green solder mask web. Check actual fab process.")
