#!/usr/bin/env python3
"""Remove only the PCB-only KiCad decorative logo from the MiniHost board.
Not a component, testpoint, mechanical hole, copper or net. Existing license,
source author attribution and full edit history are retained separately.
"""
from pathlib import Path
import pcbnew
path=Path("cm5_mini_host/CM5_MINIMA_3.kicad_pcb")
b=pcbnew.LoadBoard(str(path))
c=[fp for fp in b.GetFootprints() if fp.GetReference()=="REF**"]
assert len(c)==1, f"Expected 1 decorative REF** footprint, found {len(c)}"
fp=c[0]
assert fp.GetValue()=="KiCad-Logo2_5mm_SilkScreen"
assert str(fp.GetFPID().GetLibNickname())=="Symbol"
assert "KiCad-Logo2_5mm_SilkScreen" in str(fp.GetFPID().GetLibItemName())
assert len(fp.Pads())==0, "Unexpected electrical pads, refuse to delete"
assert abs(pcbnew.ToMM(fp.GetPosition().x)-116.7)<0.002
assert abs(pcbnew.ToMM(fp.GetPosition().y)-77.79)<0.002
before=len(b.GetFootprints())
b.Remove(fp)
assert len(b.GetFootprints())==before-1
pcbnew.SaveBoard(str(path),b)
print("Removed non-electrical decorative REF** footprint only.")
print("PCB footprints:",before,"->",len(b.GetFootprints()))
