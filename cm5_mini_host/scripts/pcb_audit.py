#!/usr/bin/env python3
"""Static PCB copper-length and geometry review; requires KiCad pcbnew Python API.

Note: lengths here are physical segment/arc center-line sums, NOT 3D electrical
lengths. They exclude pad and connector discontinuity, via vertical delay,
in-package skew, AC coupling capacitors and return path impedance.
"""
import sys, csv, collections, re
from pathlib import Path
try:
    import pcbnew
except ImportError:
    raise SystemExit("pcbnew module missing: run under /usr/bin/python3 with KiCad Python package installed")

board_path=Path(sys.argv[1] if len(sys.argv)>1 else "CM5_MINIMA_3.kicad_pcb")
report_dir=Path(sys.argv[2] if len(sys.argv)>2 else "reports")
report_dir.mkdir(parents=True,exist_ok=True)
board=pcbnew.LoadBoard(str(board_path))
tracks=collections.defaultdict(lambda:{"mm":0.0,"segments":0,"vias":0,"layers":set()})
for t in board.GetTracks():
    n=t.GetNetname()
    if not n:
        continue
    ent=tracks[n]
    if isinstance(t,pcbnew.PCB_VIA):
        ent["vias"]+=1
        continue
    try:
        ent["mm"]+=pcbnew.ToMM(t.GetLength())
    except Exception:
        pass
    ent["segments"]+=1
    ent["layers"].add(board.GetLayerName(t.GetLayer()))
with (report_dir/"net_copper_lengths.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.writer(f)
    w.writerow(["Net","CopperTraceLength_mm_excl_via","TrackArcCount","ViaCount","Layers"])
    for n,d in sorted(tracks.items()):
        w.writerow([n,round(d["mm"],3),d["segments"],d["vias"],"|".join(sorted(d["layers"]))])
pairs=collections.defaultdict(dict)
for n,d in tracks.items():
    m=re.match(r"^(.*?)(?:[_-])(P|N)$",n,re.I)
    if not m:
        m=re.match(r"^(.*?)(?:[_-])(DP|DN)$",n,re.I)
    if m:
        pref=m.group(1)
        polarity="P" if m.group(2).upper().endswith("P") else "N"
        pairs[pref][polarity]=(n,d)
with (report_dir/"differential_pairs.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.writer(f)
    w.writerow(["PairKey","PositiveNet","NegativeNet","P_length_mm","N_length_mm","AbsDelta_mm","P_vias","N_vias","Scope"])
    for name,pol in sorted(pairs.items()):
        if "P" not in pol or "N" not in pol:
            continue
        p,dp=pol["P"]; n,dn=pol["N"]
        w.writerow([name,p,n,round(dp["mm"],3),round(dn["mm"],3),
                    round(abs(dp["mm"]-dn["mm"]),3),dp["vias"],dn["vias"],
                    "trace-only (check pin/pad/via offsets by hand)"])
with (report_dir/"board_inventory.md").open("w",encoding="utf-8") as f:
    f.write("# Board quick audit\n\n")
    f.write(f"Source: {board_path.name}\n\n")
    f.write(f"KiCad/pcbnew: {pcbnew.Version()}\n\n")
    f.write(f"Footprints: {len(board.GetFootprints())}\n\n")
    f.write(f"Net names with traces: {len(tracks)}\n\n")
    f.write(f"Copper segments/arcs: {sum(x['segments'] for x in tracks.values())}\n\n")
    f.write(f"Copper vias: {sum(x['vias'] for x in tracks.values())}\n\n")
    f.write(f"Recognized differential pairs: {sum('P' in x and 'N' in x for x in pairs.values())}\n\n")
    f.write("**Not a sign-off:** excludes full-wave/SI channel loss, via vertical length, crosstalk, return path, connector and pad matching. Check fabrication stackup and DRC reports.\n")
print((report_dir/"board_inventory.md").read_text())
