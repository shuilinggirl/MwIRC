#!/usr/bin/env python3
"""Inspect and run the Paper 1 reproducibility workflow without deleting results."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PIPELINE = HERE / "pipeline.json"
LOG_ROOT = ROOT / "results" / "information_specific_mwc" / "paper1_release_logs"


def load_pipeline() -> dict:
    return json.loads(PIPELINE.read_text(encoding="utf-8"))


def commands(stage: dict, debug: bool = False) -> list[list[str]]:
    raw = stage.get("debug_command") if debug and stage.get("debug_command") else stage["command"]
    if raw and isinstance(raw[0], str):
        raw = [raw]
    return [[sys.executable if token == "{python}" else token for token in command] for command in raw]


def status(path: str) -> str:
    target = ROOT / path
    if not target.exists():
        return "MISSING"
    if target.is_file():
        return f"OK ({target.stat().st_size:,} B)"
    return "OK"


def show_plan(data: dict) -> int:
    print(f"Project root: {ROOT}")
    print(f"Pipeline: {PIPELINE.relative_to(ROOT)}")
    for name, stage in data["stages"].items():
        outputs = stage.get("outputs", [])
        complete = bool(outputs) and all((ROOT / item).exists() for item in outputs)
        marker = "complete" if complete else "incomplete"
        print(f"\n[{name}] {marker}\n  {stage['description']}")
        for command in commands(stage):
            print("  $ " + " ".join(command))
        for output in outputs:
            print(f"  output: {output} :: {status(output)}")
    return 0


def check(data: dict) -> int:
    errors: list[str] = []
    warnings: list[str] = []
    for name, stage in data["stages"].items():
        for source in stage.get("sources", []):
            if not (ROOT / source).exists():
                errors.append(f"{name}: missing source: {source}")
        for output in stage.get("outputs", []):
            if not (ROOT / output).exists():
                warnings.append(f"{name}: missing output: {output}")

    final_figure_one = ROOT / "manuscript/paper1/latex/figures/framework1.pdf"
    if not final_figure_one.exists():
        errors.append("missing manually assembled Figure 1: manuscript/paper1/latex/figures/framework1.pdf")

    print(f"Sources: {'PASS' if not errors else 'FAIL'}")
    print(f"Frozen outputs: {'PASS' if not warnings else 'INCOMPLETE'}")
    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARNING: {message}")
    return 1 if errors else 0


def run_stage(data: dict, name: str, debug: bool) -> int:
    if name not in data["stages"]:
        available = ", ".join(data["stages"])
        raise SystemExit(f"Unknown stage {name!r}. Available: {available}")
    stage = data["stages"][name]
    missing = [item for item in stage.get("sources", []) if not (ROOT / item).exists()]
    if missing:
        raise SystemExit("Missing stage sources:\n" + "\n".join(f"- {item}" for item in missing))

    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    environment = os.environ.copy()
    source_root = str(ROOT / "src")
    environment["PYTHONPATH"] = source_root + os.pathsep + environment.get("PYTHONPATH", "")
    log_path = LOG_ROOT / f"{name}{'_debug' if debug else ''}.log"
    with log_path.open("a", encoding="utf-8") as log:
        for command in commands(stage, debug=debug):
            rendered = " ".join(command)
            print(f"Running: {rendered}")
            log.write(f"\n$ {rendered}\n")
            log.flush()
            result = subprocess.run(command, cwd=ROOT, env=environment, stdout=log, stderr=subprocess.STDOUT, check=False)
            if result.returncode:
                print(f"FAILED ({result.returncode}); see {log_path.relative_to(ROOT)}")
                return result.returncode
    print(f"Completed {name}; log: {log_path.relative_to(ROOT)}")
    return 0


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def snapshot(data: dict, destination: Path) -> int:
    records = []
    paths: set[str] = set()
    for stage in data["stages"].values():
        paths.update(stage.get("sources", []))
        paths.update(stage.get("outputs", []))
    paths.add("manuscript/paper1/latex/figures/framework1.pdf")
    for relative in sorted(paths):
        target = ROOT / relative
        records.append({
            "path": relative,
            "exists": target.is_file(),
            "bytes": target.stat().st_size if target.is_file() else None,
            "sha256": sha256(target) if target.is_file() else None,
        })
    destination = destination if destination.is_absolute() else ROOT / destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps({"schema_version": 1, "files": records}, indent=2) + "\n", encoding="utf-8")
    print(destination)
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="action", required=True)
    sub.add_parser("plan", help="Show stages, commands and frozen-output status")
    sub.add_parser("check", help="Check the release allowlist without running analyses")
    run = sub.add_parser("run", help="Run one named stage")
    run.add_argument("stage")
    run.add_argument("--debug", action="store_true")
    snap = sub.add_parser("snapshot", help="Write SHA-256 inventory for allowlisted files")
    snap.add_argument("--output", type=Path, default=HERE / "release_inventory.json")
    return result


def main() -> int:
    args = parser().parse_args()
    data = load_pipeline()
    if args.action == "plan":
        return show_plan(data)
    if args.action == "check":
        return check(data)
    if args.action == "run":
        return run_stage(data, args.stage, args.debug)
    if args.action == "snapshot":
        return snapshot(data, args.output)
    raise AssertionError(args.action)


if __name__ == "__main__":
    raise SystemExit(main())
