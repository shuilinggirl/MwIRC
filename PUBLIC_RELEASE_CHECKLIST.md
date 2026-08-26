# Public release checklist

- [ ] Run `paper1_pipeline.py check` with no source errors.
- [ ] Run the Paper 1 test subset in `CODE_MAP.md`.
- [ ] Regenerate Figures 2-6 from frozen tables and compare file-level/visual QA.
- [ ] Keep the manually edited `framework1.pdf` unchanged.
- [ ] Generate `release_inventory.json` and retain SHA-256 hashes.
- [ ] Remove credentials, private absolute paths, raw participant data, and ADNI files.
- [ ] Include data accessions, licenses, and exact cohort inclusion criteria in the README.
- [ ] Include de-identified subject-level/ROI-level derived tables when licenses allow.
- [ ] Include the canonical DK68 ROI-order table and allowed spin permutations.
- [ ] Sync Chinese and English manuscripts before submission.
- [ ] Archive the exact LaTeX source, BibTeX file, final vector figures, and SI.
- [ ] Assign a versioned DOI (for example, through Zenodo) only after the archive passes QA.
