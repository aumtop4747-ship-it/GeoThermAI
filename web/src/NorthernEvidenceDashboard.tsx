
import { useEffect, useState } from "react";

type ReadinessRow = {
  site_name: string;
  individual_well_records: string;
  training_ready_wells: string;
  aggregate_summary_rows: string;
  geology_status: string;
  structure_status: string;
  terrain_status: string;
  pfa_status: string;
  drilling_prediction_status: string;
};

function parseReadinessCsv(text: string): ReadinessRow[] {
  const lines = text
    .replace(/^\uFEFF/, "")
    .trim()
    .split(/\r?\n/);

  const headers = lines[0]?.split(",").map((s) => s.trim());

  if (!headers || !headers.includes("site_name") ||
      !headers.includes("pfa_status") ||
      !headers.includes("training_ready_wells")) {
    throw new Error("Invalid readiness CSV columns");
  }

  return lines.slice(1).filter(Boolean).map((line) => {
    const values = line.split(",");
    if (values.length !== headers.length) {
      throw new Error("Invalid readiness CSV row");
    }

    return Object.fromEntries(
      headers.map((key, i) => [key, values[i]?.trim() ?? ""])
    ) as ReadinessRow;
  });
}

export function NorthernEvidenceDashboard({
  language,
}: {
  language: "th" | "en";
}) {
  const [rows, setRows] = useState<ReadinessRow[] | null>(null);
  const [error, setError] = useState("");
  const th = language === "th";

  useEffect(() => {
    const controller = new AbortController();

    fetch("/data/northern_feature_readiness.csv", {
      signal: controller.signal,
    })
      .then(async (response) => {
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        return parseReadinessCsv(await response.text());
      })
      .then(setRows)
      .catch((err: unknown) => {
        if (!controller.signal.aborted) {
          setError(String(err));
        }
      });

    return () => controller.abort();
  }, []);

  const totalWells = rows?.reduce(
    (sum, row) => sum + Number(row.individual_well_records || 0),
    0
  ) ?? 0;

  const readyWells = rows?.reduce(
    (sum, row) => sum + Number(row.training_ready_wells || 0),
    0
  ) ?? 0;

  return (
    <div className="page status-page">
      <div className="page-intro">
        <div>
          <p className="eyebrow">GeoThermAI / Northern Thailand</p>
          <h1>{th ? "หลักฐานการสำรวจภาคเหนือ" : "Northern Evidence Dashboard"}</h1>
          <p>
            {th
              ? "ตรวจสอบความพร้อมของข้อมูลสำหรับการวิจัยพื้นที่เป้าหมายการเจาะ"
              : "Data readiness for geothermal exploration research"}
          </p>
        </div>
        <span className="status-pill amber">
          {th ? "ยังไม่พร้อมทำนาย" : "Prediction Not Ready"}
        </span>
      </div>

      {error && (
        <section className="panel">
          <p role="alert">
            {th ? "โหลดข้อมูลไม่สำเร็จ" : "Data loading failed"}: {error}
          </p>
        </section>
      )}

      {!rows && !error && (
        <section className="panel">
          {th ? "กำลังอ่านข้อมูล..." : "Loading evidence..."}
        </section>
      )}

      {rows && (
        <section className="status-grid">
          <article className="panel status-card">
            <p className="eyebrow">
              {th ? "พื้นที่นำร่อง" : "Pilot Sites"}
            </p>
            <h2>{rows.length}</h2>
          </article>

          <article className="panel status-card">
            <p className="eyebrow">
              {th ? "ข้อมูลรายหลุม" : "Individual Well Records"}
            </p>
            <h2>{totalWells}</h2>
          </article>

          <article className="panel status-card">
            <p className="eyebrow">
              {th ? "หลุมที่พร้อมฝึก AI" : "Training-ready Wells"}
            </p>
            <h2>{readyWells}</h2>
          </article>

          <article className="panel span-2">
            <h2>{th ? "สถานะแต่ละพื้นที่" : "Site Readiness"}</h2>

            <div className="two-column-list">
              {rows.map((row) => (
                <div key={row.site_name}>
                  <h3>{row.site_name}</h3>
                  <p>
                    {th ? "ข้อมูลรายหลุม" : "Well records"}:{" "}
                    {row.individual_well_records}
                  </p>
                  <p>
                    {th ? "แถวข้อมูลสรุป" : "Summary rows"}:{" "}
                    {row.aggregate_summary_rows}
                  </p>
                  <p>Geology: {row.geology_status}</p>
                  <p>Structure: {row.structure_status}</p>
                  <p>Terrain: {row.terrain_status}</p>
                  <p>PFA: {row.pfa_status}</p>
                  <p>
                    Prediction: {row.drilling_prediction_status}
                  </p>
                </div>
              ))}
            </div>
          </article>

          <article className="panel span-2">
            <h2>{th ? "ข้อจำกัดงานวิจัย" : "Research Limitations"}</h2>
            <p>
              {th
                ? "สถานะ GIS เป็นข้อมูลความพร้อมระดับชุดข้อมูล ไม่ใช่ผลตรวจพิกัดเฉพาะพื้นที่"
                : "GIS statuses describe dataset-level readiness, not site-specific validation."}
            </p>
            <p>
              {th
                ? "ระบบยังไม่มีผลทำนายความสำเร็จของการเจาะที่ผ่านการตรวจสอบ"
                : "Validated drilling-success predictions are not yet available."}
            </p>
          </article>
        </section>
      )}
    </div>
  );
}
