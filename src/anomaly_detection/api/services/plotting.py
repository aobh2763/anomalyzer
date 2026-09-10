import io
import pandas as pd
import numpy as np

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sqlmodel import Session

from anomaly_detection.api.models import Evaluation
from anomaly_detection.api.services.paths import RESULTS_DIR


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def plot_score_histogram(
    scores, decision_boundary=None, title="Decision function distribution", bins=100
):
    scores = np.asarray(scores)

    fig, ax = plt.subplots(figsize=(9, 5.5))

    counts, bin_edges = np.histogram(scores, bins=bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    bin_widths = np.diff(bin_edges)

    if decision_boundary is None:
        ax.bar(
            bin_centers,
            counts,
            width=bin_widths,
            color="#F08C00",
            edgecolor="white",
            linewidth=0.3,
        )
        legend_handles = [mpatches.Patch(color="#F08C00", label="events")]
    else:
        is_anomaly = bin_centers < decision_boundary
        bar_colors = np.where(is_anomaly, "#E03131", "#2F9E44")

        ax.bar(
            bin_centers,
            counts,
            width=bin_widths,
            color=bar_colors,
            edgecolor="white",
            linewidth=0.3,
        )

        ax.axvline(
            decision_boundary,
            color="black",
            linestyle="--",
            linewidth=1.2,
            label=f"decision boundary ({decision_boundary:.3f})",
        )

        legend_handles = [
            mpatches.Patch(color="#E03131", label="anomalous"),
            mpatches.Patch(color="#2F9E44", label="normal"),
            ax.get_lines()[0],
        ]

    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Decision Function Score (lower = more anomalous)", fontsize=10)
    ax.set_ylabel("Event Count", fontsize=10)

    ax.grid(axis="y", linestyle="-", alpha=0.25)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="both", labelsize=9)

    ax.legend(handles=legend_handles, frameon=False, fontsize=9)

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
        title=f"Decision Function Distribution - {evaluation.evaluation_id}",
    )
