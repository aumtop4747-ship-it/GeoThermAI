
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[2]

FOLDER = ROOT / "derived" / "northern_evidence"
INPUT = FOLDER / "northern_drilling_registry.csv"
OUTPUT = FOLDER / "drilling_quality_report.csv"

with INPUT.open("r", encoding="utf-8-sig", newline="") as f:
    records = list(csv.DictReader(f))

reports = []
seen = set()

print("=== Northern Drilling Quality Check ===")

for row in records:
    well = (row.get("well_id") or "").strip()
    site = (row.get("site_name") or "").strip()
    status = (row.get("verification_status") or "").strip()

    issues = []

    # ตรวจพิกัด
    lat = (row.get("latitude") or "").strip()
    lon = (row.get("longitude") or "").strip()

    if not lat or not lon:
        issues.append("MISSING_COORDINATES")
    else:
        try:
            latitude = float(lat)
            longitude = float(lon)
            if not (-90 <= latitude <= 90 and
                    -180 <= longitude <= 180):
                issues.append("INVALID_COORDINATES")
        except ValueError:
            issues.append("INVALID_COORDINATES")

    # ตรวจรายการซ้ำ
    key = (site.lower(), well.lower())

    if key in seen:
        issues.append("DUPLICATE_WELL")
    seen.add(key)

    # ตรวจความขัดแย้งจากเอกสาร
    if "CONFLICT" in status:
        issues.append("SOURCE_CONFLICT")

    if status != "PRIMARY_SOURCE_VERIFIED":
        issues.append("SOURCE_NOT_FULLY_VERIFIED")

    # ยังไม่อนุมัติให้ใช้ฝึก AI
    reports.append({
        "site_name": site,
        "well_id": well,
        "training_status": "NOT_READY",
        "issues": "; ".join(issues)
    })

    print(f"\nWell: {well}")
    print("Issues:", ", ".join(issues) or "NONE")
    print("Training: NOT_READY")

# ส่งออกรายงาน
with OUTPUT.open(
    "w", encoding="utf-8-sig", newline=""
) as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "site_name", "well_id",
            "training_status", "issues"
        ]
    )
    writer.writeheader()
    writer.writerows(reports)

print("\nTotal wells:", len(reports))
print("Report saved:", OUTPUT.name)
print("=== Validation Completed ===")
