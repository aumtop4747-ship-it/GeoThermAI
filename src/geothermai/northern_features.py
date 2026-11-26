
from pathlib import Path
import csv

# === GeoThermAI Northern Feature Readiness ===

ROOT = Path(__file__).resolve().parents[2]

DATA = ROOT / "derived" / "northern_evidence"

# อ่านข้อมูล CSV ที่สร้างไว้ก่อนหน้านี้
def read_csv(filename):
    path = DATA / filename

    if not path.exists():
        raise FileNotFoundError(f"Missing: {path}")

    with path.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        return list(csv.DictReader(file))


wells = read_csv("northern_drilling_registry.csv")
quality = read_csv("drilling_quality_report.csv")
fang = read_csv("northern_drilling_site_summary.csv")

# ตรวจไฟล์ข้อมูล GIS ตามตำแหน่งที่รายงานระบุ
geology_file = (
    ROOT / "tasks"
    / "phase_1c_label_expansion_gis_foundation"
    / "rock_unit_250k_northern_esrijson.json"
)

terrain_file = (
    ROOT / "tasks"
    / "phase_1c_label_expansion_gis_foundation"
    / "northern_terrain_variable_summary.csv"
)

geology_status = (
    "SOURCE_FOUND_REVIEW_REQUIRED"
    if geology_file.exists()
    else "SOURCE_NOT_FOUND_AT_EXPECTED_PATH"
)

terrain_status = (
    "SUMMARY_ONLY"
    if terrain_file.exists()
    else "NOT_FOUND"
)

# จากรายงาน Fault Audit เดิม
structure_status = "RESTRICTED_REUSE"

# รายชื่อพื้นที่จากทะเบียนสองประเภท
sites = sorted(
    {
        row["site_name"].strip()
        for row in wells + fang
        if row.get("site_name", "").strip()
    }
)

# รายงานความพร้อมรายพื้นที่
results = []

for site in sites:

    site_wells = [
        row for row in wells
        if row["site_name"].strip() == site
    ]

    site_quality = [
        row for row in quality
        if row["site_name"].strip() == site
    ]

    site_summaries = [
        row for row in fang
        if row["site_name"].strip() == site
    ]

    ready_wells = sum(
        row["training_status"] == "READY"
        for row in site_quality
    )

    results.append({
        "site_name": site,
        "individual_well_records": len(site_wells),
        "training_ready_wells": ready_wells,
        "aggregate_summary_rows": len(site_summaries),
        "geology_status": geology_status,
        "structure_status": structure_status,
        "terrain_status": terrain_status,
        "pfa_status": "INSUFFICIENT_EVIDENCE",
        "drilling_prediction_status": "NOT_READY",
    })

# สร้าง CSV สำหรับ Dashboard
output = DATA / "northern_feature_readiness.csv"

columns = [
    "site_name",
    "individual_well_records",
    "training_ready_wells",
    "aggregate_summary_rows",
    "geology_status",
    "structure_status",
    "terrain_status",
    "pfa_status",
    "drilling_prediction_status",
]

with output.open(
    "w", encoding="utf-8-sig", newline=""
) as file:

    writer = csv.DictWriter(
        file, fieldnames=columns
    )

    writer.writeheader()
    writer.writerows(results)

# แสดงผลใน Terminal
print("=== GeoThermAI Northern Feature Readiness ===")

for row in results:
    print("\nSite:", row["site_name"])
    print("Well records:", row["individual_well_records"])
    print("Training-ready:", row["training_ready_wells"])
    print("Summary rows:", row["aggregate_summary_rows"])
    print("Geology:", row["geology_status"])
    print("Structure:", row["structure_status"])
    print("Terrain:", row["terrain_status"])
    print("PFA:", row["pfa_status"])

print("\nSaved:", output.name)
print("=== Readiness Check Completed ===")
