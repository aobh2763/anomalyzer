"""
USED ONLY FOR ANALYSIS

Profiling helpers for per-EventID EventData/UserData schemas.

Workflow:
    1. event_dfs = load_eventdata(evtx_path)          # dict[EventID, DataFrame]
    2. profiles = profile_all(event_dfs, keep_list)    # dict[EventID, profile DataFrame]
    3. print_summary(profiles)                         # quick human-readable overview
    4. constants = summarize_constants(profiles)        # {EventID: {col: value}}
    5. export_profiles_csv(profiles, output_dir)        # one CSV per EventID, for the report
"""

import pandas as pd


def profile_eventid(
    df, exclude_cols=("EventID", "EventRecordID", "TimeCreated", "PayloadSource")
):
    """Profile a single EventID's DataFrame: null rate, cardinality, top value.

    Args:
        df (DataFrame): One EventID's flattened payload DataFrame (from load_eventdata()[eid]).
        exclude_cols (tuple[str]): Bookkeeping columns to skip, not real payload fields.

    Returns:
        DataFrame: One row per field, columns: null_rate, nunique, top_value, top_value_share, is_constant.
    """
    cols = [c for c in df.columns if c not in exclude_cols]
    rows = []

    if not cols:
        return pd.DataFrame(
            columns=[
                "null_rate",
                "nunique",
                "top_value",
                "top_value_share",
                "is_constant",
            ]
        ).rename_axis("field")

    for col in cols:
        series = df[col]
        null_rate = series.isna().mean()
        non_null = series.dropna()
        nunique = non_null.nunique()

        if len(non_null) > 0:
            top_value = non_null.value_counts().idxmax()
            top_value_share = non_null.value_counts(normalize=True).max()
        else:
            top_value = None
            top_value_share = None

        is_constant = (nunique == 1) and (null_rate == 0)

        rows.append(
            {
                "field": col,
                "null_rate": round(null_rate, 4),
                "nunique": nunique,
                "top_value": top_value,
                "top_value_share": (
                    round(top_value_share, 4) if top_value_share is not None else None
                ),
                "is_constant": is_constant,
            }
        )

    return pd.DataFrame(rows).set_index("field")


def profile_all(event_dfs, event_ids=None):
    """Profile every EventID in event_dfs (or just event_ids, if given).

    Args:
        event_dfs (dict[int, DataFrame]): Output of load_eventdata().
        event_ids (list[int] | None): Restrict profiling to these EventIDs. Defaults to all present.

    Returns:
        dict[int, DataFrame]: EventID -> profile DataFrame (see profile_eventid).
    """
    ids_to_profile = event_ids if event_ids is not None else list(event_dfs.keys())

    profiles = {}
    for eid in ids_to_profile:
        df = event_dfs.get(eid)
        if df is None or df.empty:
            continue
        profiles[eid] = profile_eventid(df)

    return profiles


def categorize_fields(profile, high_null_threshold=0.95):
    """Split one EventID's profiled fields into three buckets.

    Args:
        profile (DataFrame): Output of profile_eventid() for one EventID.
        high_null_threshold (float): null_rate at/above this is considered "too sparse to use".

    Returns:
        dict[str, list[str]]: {"constant": [...], "high_null": [...], "variable": [...]}.
    """
    constant = profile[profile["is_constant"]].index.tolist()
    high_null = profile[
        (~profile["is_constant"]) & (profile["null_rate"] >= high_null_threshold)
    ].index.tolist()
    variable = profile[
        (~profile["is_constant"]) & (profile["null_rate"] < high_null_threshold)
    ].index.tolist()

    return {"constant": constant, "high_null": high_null, "variable": variable}


def print_summary(profiles, event_dfs=None, high_null_threshold=0.95):
    """Print a compact per-EventID summary: record count, constant fields, high-null fields,
    and variable fields (the extractor candidates).

    Args:
        profiles (dict[int, DataFrame]): Output of profile_all().
        event_dfs (dict[int, DataFrame] | None): Pass the original dict to include record counts.
        high_null_threshold (float): Passed through to categorize_fields().
    """
    for eid, profile in profiles.items():
        count = len(event_dfs[eid]) if event_dfs is not None else "?"
        buckets = categorize_fields(profile, high_null_threshold)

        print(f"\nEventID {eid} ({count} records)")
        print(f"  constant  : {buckets['constant'] if buckets['constant'] else '-'}")
        print(f"  >=95% null: {buckets['high_null'] if buckets['high_null'] else '-'}")
        print(f"  variable  : {buckets['variable'] if buckets['variable'] else '-'}")


def build_extractor_candidates(profiles, high_null_threshold=0.95):
    """Collapse every EventID's variable fields into a single lookup, ready to hand-write extractors from.

    Args:
        profiles (dict[int, DataFrame]): Output of profile_all().
        high_null_threshold (float): Passed through to categorize_fields().

    Returns:
        dict[int, list[str]]: EventID -> list of field names worth extracting as features.
    """
    return {
        eid: categorize_fields(profile, high_null_threshold)["variable"]
        for eid, profile in profiles.items()
    }


def summarize_constants(profiles, event_dfs):
    """Collapse each EventID's constant fields down to {field: value} for quick reference/report use.

    Args:
        profiles (dict[int, DataFrame]): Output of profile_all().
        event_dfs (dict[int, DataFrame]): Original dict, needed to read the actual constant value.

    Returns:
        dict[int, dict[str, object]]: EventID -> {field_name: constant_value}.
    """
    result = {}
    for eid, profile in profiles.items():
        constant_fields = profile[profile["is_constant"]].index.tolist()
        df = event_dfs[eid]
        result[eid] = {col: df[col].dropna().iloc[0] for col in constant_fields}

    return result


def export_profiles_csv(profiles, output_dir):
    """Write one CSV per EventID's profile to output_dir, named profile_<EventID>.csv.

    Args:
        profiles (dict[int, DataFrame]): Output of profile_all().
        output_dir (Path): Directory to write CSVs into (must already exist).
    """
    for eid, profile in profiles.items():
        profile.to_csv(output_dir / f"profile_{eid}.csv")


def find_rare_event_ids(event_dfs, max_count=50, exclude=()):
    """Identify EventIDs with few records, not worth aggregate profiling, better inspected as raw rows.

    Args:
        event_dfs (dict[int, DataFrame]): Output of load_eventdata().
        max_count (int): EventIDs with this many records or fewer are considered rare.
        exclude (tuple[int]): EventIDs to skip (e.g. ones already in your keep_list).

    Returns:
        list[int]: Rare EventIDs, sorted by count ascending (rarest first).
    """
    counts = {eid: len(df) for eid, df in event_dfs.items() if eid not in exclude}
    rare = [eid for eid, c in counts.items() if c <= max_count]
    return sorted(rare, key=lambda eid: counts[eid])


def show_rare_events(
    event_dfs, rare_ids, drop_cols=("PayloadSource",), max_rows_per_id=5
):
    """Print full (non-aggregated) rows for each rare EventID, for quick manual review.

    Args:
        event_dfs (dict[int, DataFrame]): Output of load_eventdata().
        rare_ids (list[int]): EventIDs to display, e.g. from find_rare_event_ids().
        drop_cols (tuple[str]): Bookkeeping columns to hide for readability.
        max_rows_per_id (int): Cap on rows shown per EventID, in case a "rare" one still has several.
    """
    for eid in rare_ids:
        df = event_dfs[eid]
        cols = [c for c in df.columns if c not in drop_cols]
        non_null_cols = [c for c in cols if df[c].notna().any()]

        print(f"\n--- EventID {eid} ({len(df)} records) ---")
        with pd.option_context("display.max_columns", None, "display.width", 160):
            print(df[non_null_cols].head(max_rows_per_id).to_string(index=False))
