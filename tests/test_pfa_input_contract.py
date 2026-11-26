
import pandas as pd
import pytest

from geothermai.prediction_architecture import ModelABaselinePFA


def test_pfa_rejects_invalid_evidence_scores():

    invalid_scores = pd.DataFrame(
        [[-0.5, 0.2, 1.4]],
        columns=["geology", "structure", "terrain"],
    )

    model = ModelABaselinePFA()

    with pytest.raises(ValueError):
        model.predict_validated_evidence(invalid_scores)
