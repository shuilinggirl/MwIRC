from __future__ import annotations

import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[2]


def test_pipeline_sources_and_final_outputs_exist() -> None:
    pipeline = json.loads((HERE / "pipeline.json").read_text(encoding="utf-8"))
    for stage in pipeline["stages"].values():
        for relative in stage.get("sources", []):
            assert (ROOT / relative).is_file(), relative
        for relative in stage.get("outputs", []):
            assert (ROOT / relative).is_file(), relative


def test_final_manuscript_uses_allowlisted_figures() -> None:
    manuscript = (ROOT / "manuscript/paper1/latex/main_zh.tex").read_text(encoding="utf-8")
    expected = {
        "framework1.pdf",
        "figure2_2x2_alternative.pdf",
        "figure3_reliability_enriched.pdf",
        "figure4_cognitive_complementarity_age_stratified_annotated_v4.pdf",
        "figure5_cross_cohort_cognitive_decoding.pdf",
        "figure6_external_biology_enriched.pdf",
    }
    for name in expected:
        assert name in manuscript


def test_core_package_imports() -> None:
    assert importlib.util.find_spec("metabolic_information_mwc") is not None


def test_release_metadata_contains_no_private_absolute_paths() -> None:
    for path in [HERE / "pipeline.json", HERE / "README.md", HERE / "DATA_MANIFEST.md", HERE / "CODE_MAP.md"]:
        text = path.read_text(encoding="utf-8")
        assert "/Users/" not in text
        assert "loginKey=" not in text
        assert "password=" not in text.lower()
