# ada-literature-benchmark
Curate and visualize **real-world ADA drug-tolerance data** (recovery vs free drug) to benchmark simulations.

## 🎯 Goals
- Extract **drug tolerance (µg/mL)** and **recovery (%)** from literature (tables/figures).
- Normalize units and methods (Standard vs PandA-like).
- Compare to simulated outputs from **ada-panda-mini**.
- Export `benchmarks_lit.parquet` for integration into other repos.

## 📦 Repo contents
- `data/literature_sources/*.csv` — curated numeric points from papers
- `notebooks/`
  - **01_import_clean** — load CSVs → tidy/validate → `benchmarks_lit.parquet`
  - **02_compare_to_sim** — overlay sim vs literature; pass/fail summaries
  - **03_generate_summary_figs** — publication-level figures & tables
- `reports/` — comparative CSV + figures

## 🔧 Data schema (long format)
`data/literature_sources/*.csv` columns:
- `publication_id` (str): e.g., `zoghbi_2015`
- `assay_method` (str): `"Standard"` or `"PandA"` (or `"PandA-like"`)
- `drug_name` (str): e.g., `adalimumab`
- `matrix` (str): `serum` / `plasma`
- `recovery_pct` (float): 0–100
- `drug_conc_ug_per_mL` (float): free drug on x-axis
- `figure_ref` (str): e.g., `Fig 3A`
- `notes` (str): free text

## ▶️ How to run
```bash
pip install -r requirements.txt
```
# 1) Build harmonized parquet from literature CSVs
jupyter notebook notebooks/01_import_clean.ipynb

# 2) Compare to ada-panda-mini (set SIM_REPORTS path in notebook)
jupyter notebook notebooks/02_compare_to_sim.ipynb

# 3) Generate figures and a summary CSV
jupyter notebook notebooks/03_generate_summary_figs.ipynb

🔗 Upstream sim repo (for comparison)

ada-panda-mini → reports/tlgs.parquet, reports/benchmarks.parquet & recovery curves

📄 Outputs

data/harmonized/benchmarks_lit.parquet

reports/literature_vs_sim.csv

reports/figures/comparison_bars.png

reports/figures/tolerance_ranges.png

🧪 PASS/ALERT rule

PASS: recovery ≥ 80% at the exposure-relevant drug concentration window.

Otherwise ALERT.

📚 Papers to include (examples)

Zoghbi et al., 2015 — PandA method (PEG + acid) drug tolerance

Sanofi EBF 2024 — practical defaults & tolerance ranges

This is a curation exercise with standardized export for cross-repo benchmarking.
