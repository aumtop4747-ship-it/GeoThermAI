
from pathlib import Path
from collections import Counter
import csv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FOLDER = PROJECT_ROOT / "tasks"

files = list(
    DATA_FOLDER.rglob("geothermal_label_master_registry.csv")
)

print("=== Northern Thailand Data Quality ===")

if not files:
    print("Dataset not found!")

else:
    file_path = files[0]

    with file_path.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        rows = list(csv.DictReader(file))

    northern_data = [
        row for row in rows
        if row["source_region"].strip() == "Northern Thailand"
    ]

    print("Northern records:", len(northern_data))

    coordinate_status = Counter(
        row["coordinate_validation_status"].strip() or "MISSING"
        for row in northern_data
    )

    print("\n=== Coordinate Quality ===")
    for status, count in sorted(coordinate_status.items()):
        print(f"{status}: {count} records")

    observation_types = Counter(
        row["observation_type"].strip() or "MISSING"
        for row in northern_data
    )

    print("\n=== Observation Types ===")
    for observation, count in sorted(observation_types.items()):
        print(f"{observation}: {count} records")

print("\n=== Analysis Completed ===")


print("\n=== Northern Records Needing Review ===")

if files:
    for row in northern_data:
        status = row.get("coordinate_validation_status", "").strip()

        if status != "CRS_AND_DMS_CONSISTENT":
            print("\nSite:", row.get("source_site_name"))
            print("Record ID:", row.get("record_uid"))
            print("Status:", status)
            print("Note:", row.get("coordinate_quality_note"))
            print("Source:", row.get("source_id"))
            print("-" * 40)


# === Step 9: Export Northern Evidence ===

if files and northern_data:

    output_folder = (
        PROJECT_ROOT / "derived" / "northern_evidence"
    )

    output_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    consistent = []
    need_review = []

    for row in northern_data:
        status = row["coordinate_validation_status"].strip()

        if status == "CRS_AND_DMS_CONSISTENT":
            consistent.append(row)
        else:
            need_review.append(row)

    fieldnames = list(northern_data[0].keys())

    outputs = [
        ("northern_coord_consistent.csv", consistent),
        ("northern_coords_review.csv", need_review),
    ]

    for filename, records in outputs:
        output_path = output_folder / filename

        with output_path.open(
            "w", encoding="utf-8-sig", newline=""
        ) as file:
            writer = csv.DictWriter(
                file, fieldnames=fieldnames
            )
            writer.writeheader()
            writer.writerows(records)

        print(f"Saved: {filename} ({len(records)} records)")

    print("\nNorthern Evidence Export Completed!")
