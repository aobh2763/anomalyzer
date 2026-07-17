import pandas as pd


def compute_deltatime(timestamps):
    """Compute deltatime between consecutive, already-sorted timestamps. The first
    row has no predecessor (NaT by default) -- filled with the mean of all other
    deltatimes instead, so it doesn't break downstream numeric handling.

    Args:
        timestamps (list[pd.Timestamp]): Chronologically sorted timestamps.

    Returns:
        list[pd.Timedelta]: One deltatime per row, first entry set to the mean.
    """
    deltas = pd.Series(timestamps).diff()
    mean_delta = deltas.mean()  # pandas skips the leading NaT automatically
    deltas.iloc[0] = mean_delta
    return deltas.tolist()


def compute_sequence_features(rows):
    """Compute previous_event_id and event_id_frequency for a list of already-sorted
    flat rows, mutating them in place. Both are None-only placeholders before this call.

    Args:
        rows (list[dict]): Flat rows, each with an "event_id" key, in chronological order.
    """
    event_ids = [row["event_id"] for row in rows]
    freq = pd.Series(event_ids).value_counts(normalize=True)

    for i, row in enumerate(rows):
        row["previous_event_id"] = event_ids[i - 1] if i > 0 else event_ids[0]
        row["event_id_frequency"] = freq[row["event_id"]]
