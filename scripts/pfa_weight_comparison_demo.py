from pathlib import Path
import sys

import numpy as np
import matplotlib.pyplot as plt

# Find GeoThermAI root directory
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from geothermai.prediction_architecture import ModelABaselinePFA

# Synthetic data used for algorithm testing
# Feature order: Geology, Structure, Terrain
X = np.array([
    [1.0, 0.0, 0.0],
    [0.0, 0.0, 1.0],
])

# Before: equal-weight average
old_scores = np.mean(X, axis=1)

# After: weighted PFA calculation
model = ModelABaselinePFA()
new_scores = model.predict_favorability(X)

labels = ["Geology only", "Terrain only"]
positions = np.arange(len(labels))

fig, ax = plt.subplots(figsize=(9, 5))

ax.plot(
    positions,
    old_scores,
    marker="o",
    linewidth=2,
    label="Before: Equal Mean",
)

ax.plot(
    positions,
    new_scores,
    marker="o",
    linewidth=2,
    label="After: Weighted PFA",
)

ax.set_xticks(positions)
ax.set_xticklabels(labels)
ax.set_ylabel("Relative Favorability Score")
ax.set_ylim(0, 0.5)
ax.set_title(
    "GeoThermAI: PFA Algorithm Comparison\n"
    "SYNTHETIC DATA - DEMONSTRATION ONLY"
)

fig.text(
    0.5, 0.02,
    "Synthetic test inputs only. Not real drilling data "
    "or validated prediction accuracy.",
    ha="center",
    fontsize=9,
)

fig.tight_layout(rect=[0, 0.06, 1, 1])
ax.legend()
ax.grid(True, alpha=0.25)

fig.tight_layout()

# Save graph
output = ROOT / "derived" / "pfa_weight_comparison_line_demo.png"
output.parent.mkdir(parents=True, exist_ok=True)

fig.savefig(output, dpi=180)
plt.close(fig)

print("Old scores:", old_scores)
print("New scores:", new_scores)
print("Graph saved:", output)