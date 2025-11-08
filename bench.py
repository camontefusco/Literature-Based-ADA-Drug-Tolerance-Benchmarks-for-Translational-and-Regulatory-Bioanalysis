from pathlib import Path
import pandas as pd
import numpy as np

def load_all_sources(src_dir: Path) -> pd.DataFrame:
    files = list((src_dir/"literature_sources").glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSVs in {src_dir/'literature_sources'}")
    dfs = []
    for f in files:
        df = pd.read_csv(f)
        df["source_file"] = f.name
        dfs.append(df)
    out = pd.concat(dfs, ignore_index=True)
    return out

def normalize_units(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # enforce numeric types + bounds
    df["recovery_pct"] = pd.to_numeric(df["recovery_pct"], errors="coerce")
    df["drug_conc_ug_per_mL"] = pd.to_numeric(df["drug_conc_ug_per_mL"], errors="coerce")
    df = df.dropna(subset=["recovery_pct","drug_conc_ug_per_mL"])
    # constrain recovery 0..100
    df["recovery_pct"] = df["recovery_pct"].clip(0, 100)
    # canonical method labels
    df["assay_method"] = df["assay_method"].replace({
        "PANDA": "PandA", "Panda": "PandA", "pandA":"PandA",
        "standard":"Standard", "STD":"Standard"
    })
    return df

def pass_alert_flag(df: pd.DataFrame, cutoff=80.0) -> pd.DataFrame:
    """Flag each row as PASS (≥ cutoff) or ALERT (< cutoff)."""
    df = df.copy()
    df["flag"] = np.where(df["recovery_pct"] >= cutoff, "PASS", "ALERT")
    return df

def summarize_tolerance(df: pd.DataFrame, window=(10,200)) -> pd.DataFrame:
    """Within exposure-relevant window, compute min recovery by method/publication."""
    lo, hi = window
    sub = df[(df["drug_conc_ug_per_mL"] >= lo) & (df["drug_conc_ug_per_mL"] <= hi)]
    if sub.empty:
        return pd.DataFrame(columns=["publication_id","assay_method","min_recovery_window"])
    grp = sub.groupby(["publication_id","assay_method"], as_index=False)["recovery_pct"].min()
    grp.rename(columns={"recovery_pct":"min_recovery_window"}, inplace=True)
    return grp

def save_parquet(df: pd.DataFrame, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)

def load_sim_recovery(sim_reports: Path) -> pd.DataFrame:
    """
    Expect a parquet or CSV with simulated recovery vs free drug by method.
    Minimal schema:
      method: 'Standard'/'PandA'
      drug_conc_ug_per_mL
      recovery_pct
    """
    # If using ada-panda-mini, you can export a CSV with these three columns.
    candidates = [sim_reports/"recovery_standard.csv", sim_reports/"recovery_panda.csv"]
    dfs = []
    for c in candidates:
        if c.exists():
            d = pd.read_csv(c)
            # standardize schema
            m = "Standard" if "standard" in c.name else "PandA"
            if "drug_ugmL" in d.columns:
                d = d.rename(columns={"drug_ugmL":"drug_conc_ug_per_mL","recovery":"recovery_pct"})
            d["assay_method"] = m
            dfs.append(d[["assay_method","drug_conc_ug_per_mL","recovery_pct"]])
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

def align_bins(lit: pd.DataFrame, sim: pd.DataFrame, bins=np.array([0.1,1,10,50,100,200,800])) -> pd.DataFrame:
    """Bin drug concentrations and compute mean recovery per bin for lit vs sim."""
    def bin_df(df, label):
        d = df.copy()
        d["bin"] = pd.cut(d["drug_conc_ug_per_mL"], bins=bins, include_lowest=True)
        agg = d.groupby(["assay_method","bin"], as_index=False)["recovery_pct"].mean()
        agg["source"] = label
        return agg
    a = bin_df(lit, "literature")
    b = bin_df(sim, "simulation")
    out = pd.concat([a,b], ignore_index=True)
    return out
import numpy as np

def pass_alert_flag(df: pd.DataFrame, cutoff: float = 80.0) -> pd.DataFrame:
    """
    Add a 'flag' column:
      PASS  if recovery_pct >= cutoff
      ALERT if recovery_pct < cutoff
    """
    out = df.copy()
    out["flag"] = np.where(out["recovery_pct"] >= cutoff, "PASS", "ALERT")
    return out


def summarize_tolerance(df: pd.DataFrame, window=(10, 200)) -> pd.DataFrame:
    """
    Within an exposure-relevant window (e.g. 10–200 µg/mL),
    compute the *minimum* recovery per (publication_id, assay_method).

    This gives a conservative view of performance within that window.
    """
    lo, hi = window
    sub = df[(df["drug_conc_ug_per_mL"] >= lo) & (df["drug_conc_ug_per_mL"] <= hi)].copy()

    if sub.empty:
        return pd.DataFrame(columns=["publication_id", "assay_method", "min_recovery_window"])

    grp = (
        sub.groupby(["publication_id", "assay_method"], as_index=False)["recovery_pct"]
        .min()
        .rename(columns={"recovery_pct": "min_recovery_window"})
    )
    return grp


def save_parquet(df: pd.DataFrame, out_path: Path):
    """
    Save a DataFrame to Parquet, creating parent folders if needed.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)

