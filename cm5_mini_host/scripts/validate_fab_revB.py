#!/usr/bin/env python3
"""Conservative content gate for KiCad fab artifacts; no DFM or SI signoff implied."""
from pathlib import Path
import csv,re,sys,json
out=Path(sys.argv[1])
drc=(out/"audit/drc.rpt").read_text(encoding="utf8",errors="replace")
erc=(out/"audit/erc.rpt").read_text(encoding="utf8",errors="replace")
if not re.search(r'\*\* Found 0 DRC violations \*\*',drc):raise SystemExit("BLOCKED: DRC not zero")
if not re.search(r'\*\* Found 0 unconnected pads \*\*',drc):raise SystemExit("BLOCKED: unconnected pads remain")
if not re.search(r'ERC messages:\s*0\s+Errors\s+0\s+Warnings\s+0',erc):
    raise SystemExit("BLOCKED: ERC not zero")
# KiCad emits Protel extensions by default (gtl/gbl/g1..g4/gts/gbs/gto/gbo/gtp/gbp/gm1).
gerber_ext={".gtl",".gbl",".g1",".g2",".g3",".g4",".gts",".gbs",".gto",".gbo",".gtp",".gbp",".gm1",".gbr"}
gerber=sorted(p for p in (out/"gerber_drill").iterdir() if p.suffix.lower() in gerber_ext)
drills=sorted((out/"gerber_drill").glob("*.drl"))
copper=["F_Cu","In1_Cu","In2_Cu","In3_Cu","In4_Cu","B_Cu"]
missing=[c for c in copper if not any(c in p.name for p in gerber)]
if missing:raise SystemExit(f"BLOCKED: missing copper Gerbers: {missing}")
if len(gerber)<12:raise SystemExit(f"BLOCKED: too few Gerber layers {len(gerber)}")
if len(drills)<2:raise SystemExit("BLOCKED: PTH and NPTH drills must be separate files")
with (out/"assembly/BOM_Parts.csv").open(newline="",encoding="utf-8-sig") as f:
    bom=list(csv.reader(f))
if len(bom)<15:raise SystemExit("BLOCKED: BOM unexpectedly empty")
summary=json.loads((out/"assembly/bom_audit_summary.json").read_text(encoding="utf-8"))
missing_mpn=int(summary["refs_missing_both_mpn_and_lcsc"])
mpn_conflicts=int(summary["refs_with_known_value_or_package_conflicts"])
if not (out/"assembly/BOM_Missing_ManufacturerPart.csv").exists():
    raise SystemExit("BLOCKED: detailed BOM missing-part report was not generated")
if not (out/"assembly/BOM_MPN_Conflicts.csv").exists():
    raise SystemExit("BLOCKED: detailed BOM conflict report was not generated")
for fn in ["Top_PickPlace.csv","Bottom_PickPlace.csv"]:
    if (out/"assembly"/fn).stat().st_size<50:
        raise SystemExit(f"BLOCKED: placement data empty {fn}")
facts={
 "gerber_count":len(gerber),"drill_count":len(drills),
 "bom_rows":len(bom)-1,
 "bom_refs_missing_mpn_and_lcsc":missing_mpn,
 "bom_refs_with_value_or_package_conflicts":mpn_conflicts,
 "assembly_bom_complete":bool(summary["assembly_bom_complete"]),
 "bom_identifiers_catalog_verified":False,
 "copper_layers_present":copper,
 "drc_violations":0,"erc_violations":0,
 "status":"BARE_PCB_FAB_CANDIDATE_ONLY__SMT_BOM_REVIEW_REQUIRED",
 "limits":[f"{missing_mpn} assembly references have neither MPN nor LCSC code; see BOM_Missing_ManufacturerPart.csv",
           f"{mpn_conflicts} assembly references contain conflicting value/package identifiers; see BOM_MPN_Conflicts.csv",
           "all populated LCSC/MPN identifiers still require live catalog and footprint verification",
           "PCB manufacturer DFM review pending",
           "90/100 ohm impedance coupon / stackup acceptance pending",
           "USB 2.0 physical end-to-end route skew requires signoff",
           "Parts sourcing, CM5 connector stack height and enclosure fit require signoff",
           "First prototype power-on and PCIe/HDMI/USB/RJ45 tests not performed"]}
(out/"audit/fab_manifest.json").write_text(json.dumps(facts,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print("Fab candidate passed content gate:",json.dumps(facts,ensure_ascii=False))
