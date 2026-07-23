"""
Isolation Forest score diagnostics.

Goal: figure out whether your decision_function scores actually separate
anomalies from normal points, or whether the model genuinely isn't
finding contrast (e.g. because of max_samples being too large).

Usage:
    from if_score_diagnostics import run_diagnostics
    run_diagnostics(model, X, known_anomaly_mask=my_bool_array)

Where:
    model              : a fitted sklearn IsolationForest
    X                  : the feature matrix you trained on (same shape/order)
    known_anomaly_mask : optional boolean array/Series, True for rows you've
                          manually flagged as suspicious (e.g. rare admin
                          EventIDs). Pass None if you don't have any yet.
"""

import numpy as np
import matplotlib.pyplot as plt


def run_diagnostics(model, X, known_anomaly_mask=None, title_prefix=""):
    scores = model.decision_function(X)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # --- Plot 1: histogram of decision_function scores ---
    ax = axes[0]
    ax.hist(scores, bins=100, color="orange", alpha=0.8, label="all points")
    if known_anomaly_mask is not None:
        known_scores = scores[np.asarray(known_anomaly_mask)]
        if len(known_scores) > 0:
            for s in known_scores:
                ax.axvline(s, color="red", alpha=0.5, linewidth=1)
            ax.axvline(
                known_scores[0],
                color="red",
                alpha=0.5,
                linewidth=1,
                label=f"known suspicious (n={len(known_scores)})",
            )
    ax.axvline(
        0, color="black", linestyle="--", linewidth=1, label="decision boundary (0)"
    )
    ax.set_title(f"{title_prefix}Decision function distribution")
    ax.set_xlabel("decision_function score (lower = more anomalous)")
    ax.set_ylabel("count")
    ax.legend()

    # --- Plot 2: sorted score rank plot (look for an elbow) ---
    ax = axes[1]
    order = np.argsort(scores)
    sorted_scores = scores[order]
    ax.plot(sorted_scores, color="steelblue", linewidth=1)
    if known_anomaly_mask is not None:
        mask_sorted = np.asarray(known_anomaly_mask)[order]
        ranks = np.where(mask_sorted)[0]
        ax.scatter(
            ranks,
            sorted_scores[ranks],
            color="red",
            s=15,
            zorder=5,
            label="known suspicious",
        )
        ax.legend()
    ax.axhline(0, color="black", linestyle="--", linewidth=1)
    ax.set_title(f"{title_prefix}Sorted scores")
    ax.set_xlabel("rank (sorted ascending)")
    ax.set_ylabel("decision_function score")

    plt.tight_layout()
    plt.show()

    # --- Printed summary stats ---
    print(f"n points               : {len(scores)}")
    print(f"score min / max         : {scores.min():.4f} / {scores.max():.4f}")
    print(f"score mean / std        : {scores.mean():.4f} / {scores.std():.4f}")
    for p in [0.1, 0.5, 1, 2, 5]:
        cutoff = np.percentile(scores, p)
        print(
            f"  {p:>4}th percentile     : {cutoff:.4f}  "
            f"({int(len(scores) * p / 100)} points below)"
        )

    if known_anomaly_mask is not None and np.asarray(known_anomaly_mask).sum() > 0:
        known_scores = scores[np.asarray(known_anomaly_mask)]
        pct_rank = [(scores < s).mean() * 100 for s in known_scores]
        print("\nKnown suspicious points - percentile rank (lower = more anomalous):")
        print(f"  mean percentile rank  : {np.mean(pct_rank):.2f}")
        print(f"  median percentile rank: {np.median(pct_rank):.2f}")
        print(f"  best (lowest) rank    : {np.min(pct_rank):.2f}")
        print(f"  worst (highest) rank  : {np.max(pct_rank):.2f}")

    return scores


def compare_max_samples(
    X,
    sample_sizes=(256, 512, 1024, 2048, 4096),
    n_estimators=512,
    max_features=0.8,
    random_state=42,
):
    """
    Quick sweep: refit IsolationForest at different max_samples values and
    compare score spread (std) and tail extent (1st percentile - min gap
    from median) to see which setting gives the most separation.
    """
    from sklearn.ensemble import IsolationForest

    results = []
    fig, ax = plt.subplots(figsize=(8, 5))

    for ms in sample_sizes:
        ms_eff = min(ms, len(X))
        model = IsolationForest(
            n_estimators=n_estimators,
            max_features=max_features,
            max_samples=ms_eff,
            contamination="auto",
            n_jobs=-1,
            random_state=random_state,
        )
        model.fit(X)
        scores = model.decision_function(X)
        ax.hist(scores, bins=80, alpha=0.4, label=f"max_samples={ms_eff}")
        results.append(
            {
                "max_samples": ms_eff,
                "std": scores.std(),
                "p1": np.percentile(scores, 1),
                "median": np.median(scores),
                "spread_p1_to_median": np.median(scores) - np.percentile(scores, 1),
            }
        )

    ax.axvline(0, color="black", linestyle="--", linewidth=1)
    ax.set_title("Score distribution across max_samples values")
    ax.set_xlabel("decision_function score")
    ax.legend()
    plt.tight_layout()
    plt.show()

    print(
        f"{'max_samples':>12} | {'std':>8} | {'p1':>8} | {'median':>8} | {'p1->median gap':>15}"
    )
    for r in results:
        print(
            f"{r['max_samples']:>12} | {r['std']:>8.4f} | {r['p1']:>8.4f} | "
            f"{r['median']:>8.4f} | {r['spread_p1_to_median']:>15.4f}"
        )
    print(
        "\nLarger 'p1->median gap' generally means better separation "
        "between the tail and the bulk of the data."
    )

    return results
