# Claim-to-code map

This is the authoritative allowlist for Paper 1. Files outside this table are not
automatically part of the manuscript's evidential chain.

| Manuscript component | Computation entry point | Frozen result | Final figure source |
|---|---|---|---|
| PhiID decomposition and AUF information-specific MwC | `scripts/run_information_specific_mwc.py` | `results/information_specific_mwc/run_manifest.json` and AUF matrices/tables under the same root | Figure 1 is manually assembled and not regenerated |
| Edge MI-rtr/sts structure and DK68 cross-cohort metabolic associations | `scripts/run_harmonized_dk68_replication.py`; `scripts/run_qnld_replication_and_consequence.py` | `harmonized_dk68_replication/subject_endpoints.csv`; `qnld_consequence/analysis/subject_endpoints.csv` | `manuscript/paper1/scripts/make_figure2_2x2_alternative.py` |
| Information-specificity beyond conventional MwC | `manuscript/paper1/scripts/audit_core_metric_specificity.py` | `pnas_core_specificity_audit/subject_core_specificity.csv` | included in Figure 2 / supplementary reporting as specified in the manuscript |
| Split-half reliability | `scripts/analyze_paper1_reliability.py` | `paper1_reliability/*.csv` and `analysis_manifest.json` | `manuscript/paper1/scripts/make_figure3_reliability_enriched.py` |
| Cognitive complementarity and cognitive-neighbourhood diversity | `scripts/run_cognitive_complementarity_replication.py` | `cognitive_complementarity_replication/*.csv`, spin nulls, and manifests | `manuscript/paper1/scripts/make_figure4_cognitive_complementarity_enriched.py --age-stratified` |
| Cross-cohort cognitive decoding | `scripts/analyze_cross_cohort_neurosynth_decoding.py` | `cross_cohort_neurosynth_decoding/*.csv`, spin nulls, and `analysis_manifest.json` | `manuscript/paper1/scripts/make_figure5_cross_cohort_cognitive_decoding.py` |
| Secondary external biology | `scripts/analyze_mitochondrial_validation.py` | `mitochondrial_validation/*.csv` and `run_manifest.json` | `manuscript/paper1/scripts/make_figure6_external_biology_enriched.py` |
| AUF edge-level MIP | `scripts/analyze_metabolic_information_preference.py` | `metabolic_information_preference/*.csv` | supplementary/contextual result; not a universal cross-cohort endpoint |

All result paths in the table are relative to
`results/information_specific_mwc/` unless otherwise stated.

## Core implementation modules

- `src/metabolic_information_mwc/phiid.py`: Gaussian-MMI PhiID.
- `src/metabolic_information_mwc/centrality.py`: normalized metabolic weighting.
- `src/metabolic_information_mwc/harmonized.py`: matched DK68 metrics and spatial statistics.
- `src/metabolic_information_mwc/cognitive_complementarity_replication.py`: independent cognitive-topology replication.
- `src/metabolic_information_mwc/neurosynth.py` and `neurosynth_advanced.py`: cognitive annotation.
- `src/metabolic_information_mwc/mip.py`: edge-level metabolic-information preference.
- `src/metabolic_information_mwc/mitochondrial.py`: external biological annotation.

## Paper 1 test subset

```text
tests/test_information_specific_mwc.py
tests/test_harmonized_dk68.py
tests/test_monash_replication.py
tests/test_paper1_reliability.py
tests/test_metabolic_information_preference.py
tests/test_cognitive_complementarity_replication.py
tests/test_cognitive_complementarity_consensus.py
tests/test_cognitive_neighborhood_diversity.py
tests/test_cognitive_complementarity_network_strata.py
tests/test_neurosynth_analysis.py
tests/test_neurosynth_advanced.py
tests/test_mitochondrial_validation.py
tests/test_submission_validation.py
```

Run this subset from the project root with `PYTHONPATH=src pytest -q` followed by
the listed paths. ADNI, directed-connectome, longitudinal, and exploratory-index
tests belong to other projects and are deliberately excluded here.
