#!/usr/bin/env python3
"""RJ45 manufacturer+fab specific Edge.Cuts controlled 30µm adjustment.

KYCON A4 drawing defines pad 15/16 2.10x3.10mm and customer-selectable PCB
overhang. Board F.Cu pads center y 27.000/45.300; near-pad notch boundaries
y 28.241421 and 44.033579. Current shield copper-to-routed-edge is 0.1914
and 0.2164mm. JLCPCB 6L routed board published minimum is 0.20mm.

Translation of ONLY upper notch straight edge and upper right R0.20mm arc
by +0.030mm in y yields >=0.20mm on both shield pads without reducing
copper, moving holes/traces or sacrificing nominal >=15.5mm opening.
Maintain a 0.372mm custom clearance everywhere except J1 (0.20mm fab min).
DFM and housing tolerance verification remain mandatory; never auto-release.
"""
import re,json
from pathlib import Path
import pcbnew

root=Path("cm5_mini_host")
pcb=root/"CM5_MINIMA_3.kicad_pcb"
proj=root/"CM5_MINIMA_3.kicad_pro"
dru=root/"CM5_MINIMA_3.kicad_dru"
source=pcb.read_text(encoding="utf-8")
def expr_end(s,k):
    dep=0;q=False;esc=False
    for j in range(k,len(s)):
        c=s[j]
        if q:
            if esc:esc=False
            elif c=="\\":esc=True
            elif c=='"':q=False
        else:
            if c=='"':q=True
            elif c=='(':dep+=1
            elif c==')':
                dep-=1
                if dep==0:return j+1
    raise ValueError("KiCad S-expression imbalance")
def modified_shape(s,uid,edits):
    matches=[]
    for m in re.finditer(r'\(gr_(?:line|arc)\b',s):
        en=expr_end(s,m.start())
        st=s[m.start():en]
        if '(uuid "'+uid+'")' in st:
            matches.append((m.start(),en,st))
    if len(matches)!=1:raise SystemExit(f"Expected exactly one outline UUID {uid}")
    st,en,block=matches[0]
    if '(layer "Edge.Cuts")' not in block:raise SystemExit("Wrong layer")
    for original,new in edits:
        if block.count(original)!=1:
            raise SystemExit(f"Unsafe board primitive change: {uid}, expected exactly one {original} got {block.count(original)}")
        block=block.replace(original,new,1)
    return s[:st]+block+s[en:]
patches={
    # Small left join: preserve upstream left corner R section. Only its upper
    # endpoint moves 0.03mm; the 0.12mm connector neck remains continuous.
    "45c02ec7-4bd2-4967-9959-9f264c9bd456":[
        ("(start 78.37 28.241421)","(start 78.37 28.271421)")],
    "7452d5d8-f08d-4d64-aee4-6d1b2950fa98":[
        ("(start 89.283579 28.241421)","(start 89.283579 28.271421)"),
        ("(end 78.37 28.241421)","(end 78.37 28.271421)")],
    # Translate whole fillet to retain its original 0.20mm radius exactly.
    "01392533-60ff-4401-b92b-76b9590f7907":[
        ("(start 89.283579 28.241421)","(start 89.283579 28.271421)"),
        ("(mid 89.425007 28.299993)","(mid 89.425007 28.329993)"),
        ("(end 89.483579 28.441421)","(end 89.483579 28.471421)")],
    "34ca15aa-c78e-40f4-831e-3592c20f8bae":[
        ("(start 89.483579 28.441421)","(start 89.483579 28.471421)")],
}
before=pcbnew.LoadBoard(str(pcb))
def footprints(board):
    return sorted((f.GetReference(),f.GetValue(),
        sorted((p.GetNumber(),p.GetNetname(),p.GetPosition().x,p.GetPosition().y,
                p.GetSize().x,p.GetSize().y,p.GetDrillSize().x,p.GetDrillSize().y) for p in f.Pads()))
        for f in board.GetFootprints())
initialfp=footprints(before);initialtracks=len(before.GetTracks())
initialzones=len(before.Zones());initialnets=before.GetNetCount()
initialdrawings=len(before.GetDrawings())
for uid,edits in patches.items():
    source=modified_shape(source,uid,edits)
pcb.write_text(source,encoding="utf-8")
after=pcbnew.LoadBoard(str(pcb))
if footprints(after)!=initialfp or len(after.GetTracks())!=initialtracks or len(after.Zones())!=initialzones or after.GetNetCount()!=initialnets or len(after.GetDrawings())!=initialdrawings:
    raise SystemExit("Copper/netlist/tracks/holes or board primitives unexpectedly altered")

config=json.loads(proj.read_text(encoding="utf-8"))
rule=config["board"]["design_settings"]["rules"]
if abs(rule["min_copper_edge_clearance"]-0.372)>1e-6:raise SystemExit("Unexpected current board edge DRC threshold")
rule["min_copper_edge_clearance"]=0.2 # verified physical factory min; larger custom margin elsewhere
proj.write_text(json.dumps(config,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
if dru.exists():raise SystemExit("Existing custom DRC file must be reconciled manually")
dru.write_text('''(version 1)
# Physical manufacturing minimum for routed 6L JLCPCB board: 0.2mm.
# Default enhanced design target: retain original 0.372mm elsewhere.
(rule "Robust 0p372 edge copper margin other than RJ45"
    (constraint edge_clearance (min 0.372mm)))
# Kycon GLPLX-SMT-188S7 board-edge shield tabs (pads 15 and 16):
# within manufacturer's 15.5mm central slot and recommended copper lands,
# edge clearance >= 0.2mm after upper notch 0.030mm adjustment.
(rule "Kycon J1 board-edge solder tabs manufacturer allowance"
    (constraint edge_clearance (min 0.2mm))
    (condition "A.memberOfFootprint('J1') || B.memberOfFootprint('J1')"))
''',encoding="utf-8")
print("Native geometry preserved: copper, footprint pads, nets, zones, tracks, count unchanged.")
print("Moved only 4 contiguous Edge.Cuts segments/fillet upper boundary +0.030mm.")
print("New routed opening width =",round(44.033579-28.271421,6),"mm; vendor's nominal 15.5mm housing width.")
print("New shield pad 16 clearance =",round(28.271421-(27+1.05),6),"mm; pad 15 =",round((45.3-1.05)-44.033579,6),"mm.")
print("KiCad global absolute min 0.20mm per JLC fab; custom 0.372mm except J1.")
