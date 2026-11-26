
from pathlib import Path
import csv
import shutil

# ตำแหน่งโฟลเดอร์หลักของ GeoThermAI
ROOT = Path(__file__).resolve().parents[2]

REGISTRY = (
    ROOT / "derived" / "northern_evidence"
    / "northern_drilling_registry.csv"
)

# ตรวจสอบว่าไฟล์ข้อมูลเดิมมีอยู่จริง
if not REGISTRY.exists():
    raise FileNotFoundError(
        "Drilling registry not found"
    )

# อ่านข้อมูลเดิม โดยไม่แก้ไขต้นฉบับ
with REGISTRY.open(
    "r", encoding="utf-8-sig", newline=""
) as file:
    reader = csv.DictReader(file)
    columns = reader.fieldnames or []
    existing = list(reader)

required = {
    "site_name",
    "well_id",
    "depth_m",
    "temperature_c",
    "drilling_result",
    "source_paper",
    "source_page",
    "verification_status",
}

if not required.issubset(set(columns)):
    raise ValueError("Registry columns do not match")

# เตรียมข้อมูล GTE-7 จากงานวิจัย
record = {column: "" for column in columns}

record.update({
    "site_name": "San Kamphaeng",
    "well_id": "GTE-7",
    "depth_m": "",
    "temperature_c": "",
    "drilling_result": (
        "Reported dry well; bottom-hole temperature "
        "99 C; conflicting depths: 1227 m and 1277 m"
    ),
    "source_paper": (
        "3_Manop_Raksaskulwong.pdf; thailand.pdf"
    ),
    "source_page": (
        "Manop PDF p.2; "
        "thailand PDF p.3 and p.11"
    ),
    "verification_status": (
        "SOURCE_CONFLICT_DEPTH_PENDING_REVIEW"
    ),
})

# ตรวจสอบว่ามี GTE-7 อยู่แล้วหรือไม่
duplicate = any(
    row["well_id"] == "GTE-7"
    and row["site_name"] == "San Kamphaeng"
    for row in existing
)

if duplicate:
    print("GTE-7 already exists. Skipped.")
else:
    # สำรอง CSV เดิมก่อนเพิ่มข้อมูล
    backup = REGISTRY.with_name(
        "northern_drilling_registry_before_gte7.csv"
    )

    if not backup.exists():
        shutil.copy2(REGISTRY, backup)

    # เพิ่มข้อมูลใหม่โดยไม่ลบข้อมูลเดิม
    with REGISTRY.open(
        "a", encoding="utf-8", newline=""
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=columns
        )
        writer.writerow(record)

    print("Added drilling record: GTE-7")

# ตรวจสอบจำนวนรายการหลังนำเข้า
with REGISTRY.open(
    "r", encoding="utf-8-sig", newline=""
) as file:
    total = len(list(csv.DictReader(file)))

print("Total drilling records:", total)
print("=== Import Completed ===")
