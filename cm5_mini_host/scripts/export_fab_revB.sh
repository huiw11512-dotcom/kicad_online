#!/usr/bin/env bash
set -euo pipefail
# Trial fabrication candidate only: no manufacturer SI / parts signoff implied.
ROOT="cm5_mini_host"
BOARD="$ROOT/CM5_MINIMA_3.kicad_pcb"
SCHEMATIC="$ROOT/CM5_MINIMA_3.kicad_sch"
OUT="fab_revB_candidate"
mkdir -p "$OUT/gerber_drill" "$OUT/assembly" "$OUT/audit"
cp reports/erc.rpt reports/drc.rpt reports/cm5.net "$OUT/audit/"
cp "$ROOT/JLC06161H_3313_STACKUP_REV_B.md" "$ROOT/EXISTING_GND_PLANES_REV_B.md" "$OUT/audit/"
kicad-cli pcb export gerbers \
  --output "$OUT/gerber_drill/" \
  --layers F.Cu,In1.Cu,In2.Cu,In3.Cu,In4.Cu,B.Cu,F.Mask,B.Mask,F.SilkS,B.SilkS,F.Paste,B.Paste,Edge.Cuts \
  --check-zones "$BOARD"
kicad-cli pcb export drill \
  --format excellon --excellon-units mm --drill-origin absolute --excellon-separate-th \
  --generate-report --report-path "$OUT/audit/drill_report.rpt" \
  --output "$OUT/gerber_drill/" "$BOARD"
kicad-cli pcb export pos \
  --side front --format csv --units mm --smd-only --exclude-dnp \
  --output "$OUT/assembly/Top_PickPlace.csv" "$BOARD"
kicad-cli pcb export pos \
  --side back --format csv --units mm --smd-only --exclude-dnp \
  --output "$OUT/assembly/Bottom_PickPlace.csv" "$BOARD"
kicad-cli sch export bom --exclude-dnp \
  --fields 'Reference,Value,Footprint,P/N,QUANTITY,DNP' \
  --labels 'Refs,Value,Footprint,ManufacturerPart,Qty,DNP' \
  --output "$OUT/assembly/BOM_Parts.csv" "$SCHEMATIC"
python3 "$ROOT/scripts/validate_fab_revB.py" "$OUT"
python3 - <<'PY'
from pathlib import Path
import zipfile
root=Path("fab_revB_candidate")
with zipfile.ZipFile("MiniHost_RevB_Fabrication_Candidate.zip","w",compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
    for p in sorted(root.rglob("*")):
        if p.is_file():z.write(p,p.relative_to(root))
print("Wrote MiniHost_RevB_Fabrication_Candidate.zip")
PY
