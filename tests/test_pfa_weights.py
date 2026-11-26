
import numpy as np

from geothermai.prediction_architecture import ModelABaselinePFA


def test_pfa_uses_declared_weights():
    # คะแนนจำลอง: Geology, Structure, Terrain
    X = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
    ])

    model = ModelABaselinePFA(
        weights={
            "geology": 0.4,
            "structure": 0.4,
            "terrain": 0.2,
        }
    )

    actual = model.predict_favorability(X)
    expected = np.array([0.4, 0.2])

    np.testing.assert_allclose(
        actual,
        expected,
        atol=1e-8,
    )

