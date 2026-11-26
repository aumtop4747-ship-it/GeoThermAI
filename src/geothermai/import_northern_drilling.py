
from pathlib import Path
import csv

# ค้นหาโฟลเดอร์หลักของ GeoThermAI
ROOT = Path(__file__).resolve().parents[2]

# ไฟล์เก็บข้อมูลหลุมเจาะ
OUTPUT = (
    ROOT / "derived" / "northern_evidence"
    / "northern_drilling_registry.csv"
)

COLUMNS = [
    "site_name",
    "well_id",
    "latitude",
    "longitude",
    "depth_m",
    "temperature_c",
    "flow_l_s",
    "drilling_result",
    "source_paper",
    "source_page",
    "verification_status",
]

# ข้อมูลจากงานวิจัยที่ตรวจสอบแล้ว
record = {
    "site_name": "San Kamphaeng",
    "well_id": "GTE-8",
    "latitude": "",
    "longitude": "",
    "depth_m": "1300",
    "temperature_c": "125",
    "flow_l_s": "",
    "drilling_result":
        "Thermal water at 920 m; 40 tonnes/hour",
    "source_paper":
        "3_Manop_Raksaskulwong.pdf; thailand.pdf",
    "source_page": "PDF 2; PDF 3",
    "verification_status":
        "LITERATURE_REPORTED_PENDING_PRIMARY_CHECK",
}

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

# ตรวจสอบข้อมูลเดิมก่อนเพิ่มรายการ
if OUTPUT.exists():
    with OUTPUT.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.DictReader(file)

        if reader.fieldnames != COLUMNS:
            raise ValueError("CSV columns do not match")

        existing = list(reader)
else:
    existing = []

# ป้องกันการเพิ่มหลุมเจาะซ้ำ
duplicate = any(
    row["well_id"] == record["well_id"]
    and row["site_name"] == record["site_name"]
    for row in existing
)

if duplicate:
    print("GTE-8 already exists. Skipped.")
else:
    is_new = not OUTPUT.exists()

    with OUTPUT.open(
        "w" if is_new else "a",
        encoding="utf-8-sig" if is_new else "utf-8",
        newline=""
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=COLUMNS
        )

        if is_new:
            writer.writeheader()

        writer.writerow(record)

    print("Added drilling record: GTE-8")

print("Registry:", OUTPUT)
print("=== Import Completed ===")
