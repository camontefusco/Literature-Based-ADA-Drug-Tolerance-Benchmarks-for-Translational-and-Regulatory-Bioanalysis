# 📚 ADA Literature Benchmark

Curated benchmark dataset for **anti-drug antibody (ADA)** assay drug tolerance, built from peer-reviewed sources.  
This repository harmonizes literature data into a reproducible format to compare with simulated ADA assay recovery results (from [`ada-panda-mini`](https://github.com/camontefusco/ada-panda-mini)).

---

## 🎯 Purpose

To quantify and visualize real-world ADA assay **drug tolerance** and **recovery performance**, bridging:
- Bioanalytical assay validation results from literature  
- Simulation outputs from *PandA* and *Standard* assay models  
- Regulatory-style interpretation thresholds (e.g. 80% PASS/ALERT)

---

## 🧩 Repository Structure

```arduino
ada-literature-benchmark/
├── data/
│ ├── literature_sources/
│ │ ├── zoghbi_2015.csv
│ │ ├── sanofi_ebf2024.csv
│ │ └── ...
│ ├── harmonized/
│ │ └── benchmarks_lit.parquet
│ └── recovery_standard.csv (from ada-panda-mini)
│ └── recovery_panda.csv (from ada-panda-mini)
│
├── notebooks/
│ ├── 01_import_clean.ipynb # ingest + harmonize raw literature data
│ ├── 02_compare_to_sim.ipynb # align vs simulation recovery
│ └── 03_generate_summary_figs.ipynb # produce figures & summaries
│
├── reports/
│ ├── figures/
│ │ ├── comparison_bars.png
│ │ └── tolerance_ranges.png
│ └── literature_vs_sim.csv
│
└── src/
└── bench.py # helper functions for harmonization & QC
```

---

## 🔬 Example Figure — Literature vs Simulation

### Literature Drug Tolerance Ranges
![Literature drug tolerance ranges](https://raw.githubusercontent.com/camontefusco/Literature-Based-ADA-Drug-Tolerance-Benchmarks-for-Translational-and-Regulatory-Bioanalysis/refs/heads/main/figures/tolerance_ranges.png)

**Interpretation:**
- *Standard bridging assays* lose recovery rapidly above ~10 µg/mL, dropping below 80% by ~100 µg/mL.  
- *PandA assays* maintain ≥80% recovery up to ~200 µg/mL and only begin to drop near 1000 µg/mL.  
- This validates the **drug masking correction** modeled in `ada-panda-mini`.

---

### Literature vs Simulation Comparison
![Comparison bars](https://raw.githubusercontent.com/camontefusco/Literature-Based-ADA-Drug-Tolerance-Benchmarks-for-Translational-and-Regulatory-Bioanalysis/refs/heads/main/figures/comparison_bars.png)

Shows alignment between **simulated recovery curves** and **empirical literature data**.  
Deviations highlight assay-specific differences and provide benchmarks for model tuning.

---

## 🧾 Typical Output

| Assay Method | Drug Tolerance (µg/mL, 80% Recovery) | PASS/ALERT |
|---------------|--------------------------------------|-------------|
| Standard | ~10 | ⚠️ ALERT |
| PandA | ~200 | ✅ PASS |

---

## 🔗 Interoperability Context

This dataset feeds into:
- [`bioanalytical-ADA-drug-interference-to-pandA-correction-method-development`](https://github.com/camontefusco/bioanalytical-ADA-drug-interference-to-pandA-correction-method-development) — simulation of ADA masking & recovery
- [`regulatory-clinpharm-ADA-immunogenicity-reporting-and-bioanalytical-summary`](https://github.com/camontefusco/regulatory-clinpharm-ADA-immunogenicity-reporting-and-bioanalytical-summary) — BAR/ISI-style regulatory summary
- [`ADA-Immunogenicity-ClinPharm-CDISC-FHIR-Interoperability-Framework`](https://github.com/camontefusco/ADA-Immunogenicity-ClinPharm-CDISC-FHIR-Interoperability-Framework) — data standards & interoperability

---

## 🧠 Key Takeaways

✅ Validates simulation-based ADA masking corrections  
✅ Provides **literature-grounded PASS/ALERT thresholds**  
✅ Ensures reproducibility and transparency  
✅ Bridges **BioA → ClinPharm → Regulatory** understanding

---

## 🧪 References

1. **Zoghbi et al., AAPS J (2015)** — PandA method improves drug tolerance in ADA assays  
2. **Sanofi EBF Workshop (2024)** — Practical defaults for PandA validation  
3. **FDA Guidance (2019)** — *Immunogenicity Testing of Therapeutic Protein Products*

---

## 💡 Summary of Utility

This repository provides a **trusted benchmark** for ADA assay performance — essential for:
- Calibrating ADA detection simulations  
- Supporting regulatory submissions  
- Demonstrating bioanalytical assay robustness  
- Building machine-readable assay metadata for CDISC / FHIR workflows

---

🧩 *Part of the integrated ADA–PandA → ClinPharm → Regulatory data ecosystem.*
