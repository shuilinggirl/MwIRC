# Paper 1 code release

## Scope

The release covers the paper's central evidence chain:

1. Gaussian-MMI PhiID edge decomposition (`sts`, `rtr`, and lagged MI);
2. MwC, MwSynC, MwRedC, and DeltaMwIRC construction;
3. matched DK68 replication in AUF, Monash, and QNLD;
4. split-half reliability and metric-specificity audits;
5. cognitive complementarity and Neurosynth decoding;
6. secondary CMRO2 and mitochondrial annotations;
7. regeneration of final Figures 2-6 from frozen results.

ADNI analyses, directed MwC, dynamic indices, longitudinal consequences, gene
analyses, and exploratory indicator screens are intentionally outside Paper 1.

## Quick start

Run commands from the project root:

```bash
export PYTHONPATH="$PWD/src"
python manuscript/paper1/code_release/paper1_pipeline.py check
python manuscript/paper1/code_release/paper1_pipeline.py plan
```

Create an exact SHA-256 inventory of source files and frozen outputs:

```bash
python manuscript/paper1/code_release/paper1_pipeline.py snapshot
```

Run a low-cost smoke analysis before a full stage:

```bash
python manuscript/paper1/code_release/paper1_pipeline.py run harmonized_auf_monash --debug
python manuscript/paper1/code_release/paper1_pipeline.py run split_half_reliability --debug
python manuscript/paper1/code_release/paper1_pipeline.py run cognitive_complementarity --debug
```

Run one complete stage, for example:

```bash
python manuscript/paper1/code_release/paper1_pipeline.py run harmonized_auf_monash
```

Regenerate final Figures 2-6 from the current frozen result tables:

```bash
python manuscript/paper1/code_release/paper1_pipeline.py run final_figures
```

Figure 1 (`framework1.pdf`) is a manually assembled editable framework figure.
It is checked as a required manuscript artifact but is not altered by the runner.

## Environment

The frozen manifests record Python 3.12.7 and the package versions in
`requirements.txt`. A new environment can be created with:

```bash
cd manuscript/paper1/code_release
conda env create -f environment.yml
conda activate paper1-information-mwc
cd ../../..
export PYTHONPATH="$PWD/src"
```

## Verification

```bash
PYTHONPATH=src pytest -q manuscript/paper1/code_release/tests
```

The tests verify the final-file allowlist, manuscript figure references, source
availability, and absence of private absolute paths or credentials in release
metadata. Statistical unit tests remain in the project-level `tests/` directory;
their Paper 1 subset is listed in `CODE_MAP.md`.

## Important reproducibility rules

- Pair PET and fMRI by participant identifier, never by file order.
- Preserve the DK68 ROI names and ordering defined by the canonical metadata.
- Use 294 valid transitions for the matched primary replication.
- Treat participant-level summaries as inferential units; edge and ROI analyses
  require the spatial or clustered null models described in the manuscript.
- Do not compare physical FDG units across cohorts. Analyses use within-cohort
  effects after the documented cortical-mean normalization.
- Do not interpret MwSynC or MwRedC as information amount, metabolic efficiency,
  or causal energy flow.

See `DATA_MANIFEST.md` for required data and path settings, and `CODE_MAP.md` for
the exact claim-to-code-to-output mapping.
