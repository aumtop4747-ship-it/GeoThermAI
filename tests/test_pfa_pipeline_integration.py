
import numpy as np
import pandas as pd


from geothermai.prediction_architecture import (
    ModelABaselinePFA,
    PredictionPipeline,
)

from geothermai.experiment_config import (
    get_default_northern_thailand_experiment_config,
)



def test_pipeline_uses_unscaled_pfa_evidence(monkeypatch):
    # สร้างข้อมูลจำลอง 12 รายการ
    rng = np.random.default_rng(42)

    X = pd.DataFrame({
        "geology": rng.uniform(0, 1, 12),
        "structure": rng.uniform(0, 1, 12),
        "terrain": rng.uniform(0, 1, 12),
    })

    y = np.array([1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0])

    groups = np.repeat(["G1", "G2", "G3", "G4"], 3)
    coordinates = rng.uniform(0, 100000, size=(12, 2))

    # บันทึกข้อมูลที่ Model A ได้รับจริง
    received = []
    original = ModelABaselinePFA.predict_validated_evidence

    def spy(self, evidence):
        received.append(evidence.copy())
        return original(self, evidence)

    monkeypatch.setattr(
        ModelABaselinePFA,
        "predict_validated_evidence",
        spy,
    )

    config = get_default_northern_thailand_experiment_config()

    pipeline = PredictionPipeline(
        config,
        bypass_gate_for_testing=True,
    )

    pipeline.fit_and_evaluate(X, y, groups, coordinates)

    # ต้องเรียกเส้นทาง PFA ใหม่อย่างน้อยหนึ่งครั้ง
    assert len(received) > 0

    # ข้อมูลต้องคงค่าเดิม ไม่ผ่าน Z-score
    for evidence in received:
        pd.testing.assert_frame_equal(
            evidence,
            X.loc[evidence.index, X.columns],
        )
