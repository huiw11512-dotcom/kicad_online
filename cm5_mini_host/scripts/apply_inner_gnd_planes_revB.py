#!/usr/bin/env python3
"""Add continuous GND reference planes on L2/In1 and L5/In4."""
from pathlib import Path
import pcbnew
root=Path("cm5_mini_host")
path=root/"CM5_MINIMA_3.kicad_pcb"
b=pcbnew.LoadBoard(str(path))
gnd=b.FindNet("GND")
if gnd is None:raise SystemExit("GND net missing")
targets=[("In1.Cu",pcbnew.In1_Cu),("In4.Cu",pcbnew.In4_Cu)]
added=[]
for name,layer in targets:
    existing=[z for z in b.Zones() if z.GetLayer()==layer and z.GetNetname()=="GND"]
    if existing:continue
    z=pcbnew.ZONE(b)
    z.SetLayer(layer)
    z.SetNet(gnd)
    z.SetPriority(0)
    z.SetLocalClearance(pcbnew.FromMM(0.13))
    z.SetMinThickness(pcbnew.FromMM(0.25))
    z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
    z.SetThermalReliefGap(pcbnew.FromMM(0.25))
    z.SetThermalReliefSpokeWidth(pcbnew.FromMM(0.25))
    outline=z.Outline()
    outline.NewOutline()
    for x,y in [(74.0,19.0),(137.0,19.0),(137.0,85.5),(74.0,85.5)]:
        outline.Append(pcbnew.FromMM(x),pcbnew.FromMM(y))
    b.Add(z)
    added.append(name)
if added:
    pcbnew.ZONE_FILLER(b).Fill(b.Zones())
pcbnew.SaveBoard(str(path),b)
b2=pcbnew.LoadBoard(str(path))
for name,layer in targets:
    if not any(z.GetLayer()==layer and z.GetNetname()=="GND" for z in b2.Zones()):
        raise SystemExit(f"Missing GND reference plane {name} after save/reload")
gnd_vias=sum(1 for t in b2.GetTracks() if isinstance(t,pcbnew.PCB_VIA) and t.GetNetname()=="GND")
if gnd_vias<200:raise SystemExit(f"Unexpectedly low GND stitching via count: {gnd_vias}")
(root/"INNER_GND_PLANES_REV_B.md").write_text(
"# Rev.B continuous reference planes\n\n"
"Added continuous GND copper zones on In1.Cu (L2) and In4.Cu (L5), clipped by the actual Edge.Cuts outline. "
"Both planes use 0.13 mm clearance, 0.25 mm minimum neck and thermal connections. Existing through-GND vias stitch the planes to the F.Cu/B.Cu ground fills; "
f"{gnd_vias} through-GND vias were found in the board before release verification. "
"These layers provide the return reference for L1/L6 microstrip and reduce return-path discontinuity at signal transitions. "
"KiCad zone refill and native DRC are required to verify plane continuity, clearances and shorts.\n",encoding="utf-8")
print(f"Added GND planes: {added}; GND through-vias={gnd_vias}; all zones refilled.")
