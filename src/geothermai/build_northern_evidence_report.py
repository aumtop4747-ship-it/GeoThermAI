
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "derived" / "northern_evidence"

def read_csv(filename):
    path = DATA / filename

    if not path.exists():
        raise FileNotFoundError(
            f"Missing file: {path}"
        )

    with path.open(
        "r", encoding="utf-8-sig", newline=""
    ) as f:
        return list(csv.DictReader(f))

# อ่านข้อมูลที่เราสร้างไว้
consistent = read_csv("northern_coord_consistent.csv")
review = read_csv("northern_coords_review.csv")
wells = read_csv("northern_drilling_registry.csv")
quality = read_csv("drilling_quality_report.csv")
fang = read_csv("northern_drilling_site_summary.csv")

ready = sum(
    row.get("training_status") == "READY"
    for row in quality
)

# เตรียมรายงาน
lines = [
    "# GeoThermAI - Northern Evidence Status",
    "",
    "## 1. Dataset Inventory",
    "",
    f"- Coordinate-consistent observations: {len(consistent)}",
    f"- Coordinate review required: {len(review)}",
    f"- Individual drilling records: {len(wells)}",
    f"- Fang summary table rows: {len(fang)}",
    f"- Training-ready well records: {ready}",
    "",
    "## 2. Drilling Evidence",
    "",
]

for row in wells:
    lines.extend([
        f"### {row.get('well_id', 'Unknown')}",
        f"- Site: {row.get('site_name', '')}",
        f"- Reported depth (m): {row.get('depth_m', '') or 'Unknown'}",
        f"- Result: {row.get('drilling_result', '')}",
        f"- Source: {row.get('source_paper', '')}",
        f"- Source pages: {row.get('source_page', '')}",
        f"- Verification: {row.get('verification_status', '')}",
        "",
    ])

lines.extend([
    "## 3. Fang Drilling Summary",
    "",
    "| Depth category | Reported count |",
    "|---|---:|",
])

for row in fang:
    lines.append(
        f"| {row['depth_category_m']} | "
        f"{row['reported_well_count']} |"
    )

lines.extend([
    "",
    "The depth categories may overlap. "
    "Do not sum them without source verification.",
    "",
    "## 4. Research Limitations",
    "",
    "- Hot spring observations are not drilling outcomes.",
    "- Coordinate consistency is not field verification.",
    "- Fang data is aggregated, not individual well data.",
    "- No validated drilling prediction is available yet.",
    "- No drilling cost savings have been demonstrated.",
    "",
])

# สร้างไฟล์รายงาน
OUTPUT = DATA / "NORTHERN_EVIDENCE_STATUS.md"
OUTPUT.write_text(
    "\n".join(lines), encoding="utf-8"
)

print("=== Northern Evidence Report ===")
print("Hot spring records:", len(consistent) + len(review))
print("Individual wells:", len(wells))
print("Fang summary rows:", len(fang))
print("Training-ready wells:", ready)
print("Report saved:", OUTPUT.name)
print("=== Report Completed ===")
