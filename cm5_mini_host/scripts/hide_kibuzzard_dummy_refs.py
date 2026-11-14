#!/usr/bin/env python3
"""Hide 27 nonfunctional near-zero-size KiBuzzard generated reference placeholders.

Each KiBuzzard footprint draws real PCB labeling through custom F.SilkS
polygons. Its <0.01 mm reference field is only a dummy artifact and triggers
both min-text-height and min-text-thickness DRC warnings. Hide only the dummy
references, retain all text polygons, all positions/rotations, and all nets/pads.
"""
from pathlib import Path
import pcbnew
p=Path("cm5_mini_host/CM5_MINIMA_3.kicad_pcb")
b=pcbnew.LoadBoard(str(p))
k=[f for f in b.GetFootprints() if f.GetReference().startswith("kibuzzard-")]
assert len(k)==27,f"Expected exactly 27 generated KiBuzzard labels, found {len(k)}"
def mm(i):return pcbnew.ToMM(i)
pad_count=sum(len(f.Pads()) for f in b.GetFootprints())
track_count=len(b.GetTracks());net_count=b.GetNetCount();zone_count=len(b.Zones())
footprint_places={f.GetReference():(f.GetPosition().x,f.GetPosition().y,len(f.Pads())) for f in b.GetFootprints()}
for f in k:
    ref=f.Reference()
    x=mm(ref.GetTextSize().x);y=mm(ref.GetTextSize().y)
    thick=mm(ref.GetTextThickness())
    if x>0.01 or y>0.01:
        raise RuntimeError(f"{f.GetReference()}: not a near-zero-size dummy ({x},{y} mm text, stored pen {thick} mm)")
    if len(f.Pads())!=0:
        raise RuntimeError(f"{f.GetReference()}: contains electrical pads")
    graphics=sum(1 for _ in f.GraphicalItems())
    if graphics==0:
        raise RuntimeError(f"{f.GetReference()}: lacks real visible graphical lettering")
    ref.SetVisible(False)
    print(f.GetReference(),"dummy field hidden; retained",graphics,"artwork primitives")
pcbnew.SaveBoard(str(p),b)
check=pcbnew.LoadBoard(str(p))
assert len(check.GetTracks())==track_count and check.GetNetCount()==net_count and len(check.Zones())==zone_count
assert sum(len(f.Pads()) for f in check.GetFootprints())==pad_count
assert {f.GetReference():(f.GetPosition().x,f.GetPosition().y,len(f.Pads())) for f in check.GetFootprints()}==footprint_places
for f in check.GetFootprints():
    if f.GetReference().startswith("kibuzzard-"):
        assert not f.Reference().IsVisible()
print("Validated board roundtrip: 27 dummy fields hidden, all 27 visible graphic labels retained, pads, nets, tracks, copper zones unchanged")
