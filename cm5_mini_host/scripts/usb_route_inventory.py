#!/usr/bin/env python3
"""Native pcbnew measured USB2 segment inventory and conservative SVG copper visualization.
The SVG uses track centerlines and simplified pads, *not* Gerber manufacturing geometry.
"""
import pcbnew, csv, math
from pathlib import Path
from xml.sax.saxutils import escape

src=Path("cm5_mini_host/CM5_MINIMA_3.kicad_pcb")
out=Path("reports")
out.mkdir(exist_ok=True)
b=pcbnew.LoadBoard(str(src))
nets={
  "/CM5/USB2P.D_P":("USB701 host P","#df3d25"),
  "/CM5/USB2P.D_N":("USB701 host N","#0878dc"),
  "/USB_C.D_P":("J101 floating data P","#dd831b"),
  "/USB_C.D_N":("J101 floating data N","#8857b1"),
}
def mm(u):return pcbnew.ToMM(u)
def xy(v):return (mm(v.x),mm(v.y))
def fmt(v):return f"{v:.4f}"
rows=[]
for tr in b.GetTracks():
    net=tr.GetNetname()
    if net not in nets:continue
    via=isinstance(tr,pcbnew.PCB_VIA)
    if via:
        x,y=xy(tr.GetPosition());p=(x,y);q=(x,y)
        layer="via"; length=0; drill=mm(tr.GetDrill())
    else:
        p=xy(tr.GetStart());q=xy(tr.GetEnd())
        layer=b.GetLayerName(tr.GetLayer())
        length=mm(tr.GetLength());drill=0
    rows.append([net,"VIA" if via else ("ARC" if isinstance(tr,pcbnew.PCB_ARC) else "TRACK"),layer,
                 *map(fmt,p),*map(fmt,q),fmt(mm(tr.GetWidth())),fmt(length),fmt(drill)])
with (out/"usb_route_segments.csv").open("w",newline="") as f:
    w=csv.writer(f);w.writerow(["net","type","layer","x1_mm","y1_mm","x2_mm","y2_mm","width_mm","centerline_length_mm","via_drill_mm"]);w.writerows(rows)
pads=[]
for fp in b.GetFootprints():
    for pad in fp.Pads():
        net=pad.GetNetname()
        if net not in nets:continue
        x,y=xy(pad.GetPosition())
        pads.append([net,fp.GetReference(),pad.GetNumber(),x,y,mm(pad.GetSize().x),mm(pad.GetSize().y)])
with (out/"usb_route_pads.csv").open("w",newline="") as f:
    w=csv.writer(f);w.writerow(["net","reference","pin","x_mm","y_mm","pad_x_mm","pad_y_mm"]);w.writerows(pads)
# Relative geometry: down-scaled entire board, with all tracks grey and selected USB nets colored.
x0,x1,y0,y1=74,138,19,86
scale=11
W=(x1-x0)*scale;H=(y1-y0)*scale
pieces=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
'<rect x="0" y="0" width="100%" height="100%" fill="#f8fafc"/>']
for tr in b.GetTracks():
    if isinstance(tr,pcbnew.PCB_VIA):continue
    p=xy(tr.GetStart());q=xy(tr.GetEnd())
    col=nets.get(tr.GetNetname(),(None,"#e0e4e7"))[1]
    thick=max(1.1,mm(tr.GetWidth())*scale)
    pieces.append(f'<line x1="{(p[0]-x0)*scale:.2f}" y1="{(p[1]-y0)*scale:.2f}" x2="{(q[0]-x0)*scale:.2f}" y2="{(q[1]-y0)*scale:.2f}" stroke="{col}" stroke-width="{thick:.2f}" stroke-linecap="round"/>')
for tr in b.GetTracks():
    if isinstance(tr,pcbnew.PCB_VIA) and tr.GetNetname() in nets:
        x,y=xy(tr.GetPosition())
        pieces.append(f'<circle cx="{(x-x0)*scale:.2f}" cy="{(y-y0)*scale:.2f}" r="{max(2,mm(tr.GetWidth())*scale/2):.2f}" fill="none" stroke="#111827" stroke-width="1"/>')
for net,ref,num,x,y,sx,sy in pads:
    col=nets[net][1]
    pieces.append(f'<circle cx="{(x-x0)*scale:.2f}" cy="{(y-y0)*scale:.2f}" r="3" fill="{col}" stroke="#111827" stroke-width=".8"/>')
for fp in b.GetFootprints():
    if fp.GetReference() in {"USB701","J101","Module301","Module302","J1","J601"}:
        x,y=xy(fp.GetPosition())
        pieces.append(f'<text x="{(x-x0)*scale+6:.2f}" y="{(y-y0)*scale-5:.2f}" font-size="12" fill="#17202a">{escape(fp.GetReference())}</text>')
pieces.append("</svg>")
(out/"usb_route_overview.svg").write_text("\n".join(pieces),encoding="utf-8")
totals={n:0 for n in nets}
for row in rows:totals[row[0]]+=float(row[-2])
with (out/"usb_route_summary.md").open("w") as f:
    f.write("# USB physical copper-only route audit\n\n")
    for n,(label,col) in nets.items():
        f.write(f"- {label}: **{totals[n]:.3f} mm**, {sum(r[0]==n for r in rows)} tracks/vias\n")
        for p in pads:
            if p[0]==n:f.write(f"  - {p[1]}.{p[2]} at ({p[3]:.3f}, {p[4]:.3f}) mm\n")
    f.write("\n**Important:** this is track centerline length only. Real USB2 timing includes pad, via barrel and connector discontinuity. No SI signoff.\n")
print((out/"usb_route_summary.md").read_text())
