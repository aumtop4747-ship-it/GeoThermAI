
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[2]

OUTPUT = (
    ROOT / "derived" / "northern_evidence"
    / "northern_drilling_site_summary.csv"
)

COLUMNS = [
    "site_name",
    "province",
    "organization",
    "depth_category_m",
    "reported_well_count",
    "study_years",
    "source_paper",
    "source_page",
    "verification_status",
]

# จำนวนหลุมตามแถวในตารางงานวิจัย
depth_groups = [
    ("<100", 27),
    ("<150", 10),
    ("<200", 7),
    ("<500", 3),
]

records = []

for depth, count in depth_groups:
    records.append({
        "site_name": "Fang",
        "province": "Chiang Mai",
        "organization": "EGAT",
        "depth_category_m": depth,
        "reported_well_count": count,
        "study_years": "1981-1985",
        "source_paper": "3_Manop_Raksaskulwong.pdf",
        "source_page": "Printed page 9, Table 1",
        "verification_status":
            "REPORTED_DEPTH_BINS_OVERLAP_UNRESOLVED",
    })

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

# อ่านข้อมูลเดิม หากเคยสร้างไฟล์ไว้แล้ว
existing = []

if OUTPUT.exists():
    with OUTPUT.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.DictReader(file)

        if reader.fieldnames != COLUMNS:
            raise ValueError("CSV columns do not match")

        existing = list(reader)

# ป้องกันการเพิ่มรายการซ้ำ
added = 0

for record in records:
    key = (
        record["site_name"],
        record["depth_category_m"],
        record["source_paper"],
    )

    duplicate = any(
        (
            row["site_name"],
            row["depth_category_m"],
            row["source_paper"],
        ) == key
        for row in existing
    )

    if not duplicate:
        existing.append(record)
        added += 1

# บันทึกข้อมูล
with OUTPUT.open(
    "w", encoding="utf-8-sig", newline=""
) as file:
    writer = csv.DictWriter(
        file, fieldnames=COLUMNS
    )
    writer.writeheader()
    writer.writerows(existing)

print("=== Fang Drilling Summary ===")
print("New rows added:", added)
print("Total summary rows:", len(existing))
print("Output:", OUTPUT.name)
print("=== Import Completed ===")

