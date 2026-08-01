import io
import pandas as pd
import numpy as np

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sqlmodel import Session

from anomaly_detection.api.models import Evaluation
from anomaly_detection.api.services.paths import RESULTS_DIR


def plot_score_histogram(
    scores, decision_boundary=None, title="Decision function distribution", bins=100
):
    scores = np.asarray(scores)

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.hist(scores, bins=bins, color="orange", alpha=0.8, label="all points")

    if decision_boundary is not None:
        ax.axvline(
            decision_boundary,
            color="black",
            linestyle="--",
            linewidth=1,
            label=f"decision boundary ({decision_boundary:.4f})",
        )

    ax.set_title(title)
    ax.set_xlabel("decision_function score (lower = more anomalous)")
    ax.set_ylabel("count")
    ax.legend()

    fig.tight_layout()

    return fig


def score_histogram_to_png_bytes(
    scores, decision_boundary=None, title="Decision function distribution", bins=100
):
    fig = plot_score_histogram(scores, decision_boundary, title, bins)

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=100)
    plt.close(fig)
    buffer.seek(0)

    return buffer.getvalue()


def get_score_histogram(evaluation_id, session: Session):
    evaluation = session.get(Evaluation, evaluation_id)
    assert evaluation is not None

    evaluation_filename = f"{evaluation_id}.csv"
    results_df = pd.read_csv(RESULTS_DIR / evaluation_filename)

    scores = results_df["anomaly_score"].to_numpy()

    return score_histogram_to_png_bytes(
        scores,
        decision_boundary=evaluation.decision_boundary,
        title=f"Evaluation {evaluation_id} - decision function distribution",
    )
