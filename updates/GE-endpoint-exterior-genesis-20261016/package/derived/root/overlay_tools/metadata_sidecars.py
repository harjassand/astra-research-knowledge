#!/usr/bin/env python3
"""Add neutral checkpoint and workflow metadata to an external GE review stage.

The script reads only a root-authored GE config, the supplied research package,
and the pinned Astra checkout. It does not author scientific claims, infer
model or inference usage, or write to the Astra checkout.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_overlay import (  # noqa: E402
    INTAKE, PREFIX, ROUTES, STATUS, UNKNOWN_FIELDS,
    check_pins, json_bytes, need, read_source, run_git, sha,
)

FORBIDDEN_PARTS = {
    "acquired_excluded_from_publication", "acquired_full_texts", "third_party_full_texts",
}


def safe_evidence_path(value: object) -> str:
    need(isinstance(value, str) and value and not Path(value).is_absolute(),
         "Evidence path must be repository-relative")
    path = Path(value)
    need(".." not in path.parts and "\\" not in value, "Unsafe evidence path: " + value)
    need(not (FORBIDDEN_PARTS & set(path.parts)),
         "Excluded acquired full-text material cannot be referenced: " + value)
    return value


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


class RefBuilder:
    def __init__(self, repo: Path, sources: dict[str, dict]):
        self.repo = repo.resolve()
        self.sources = sources
        self.refs: dict[str, dict] = {}
        self.bytes_by_id: dict[str, bytes] = {}

    def add(self, source: dict) -> str:
        path = safe_evidence_path(source.get("path"))
        digest = source.get("sha256")
        need(isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest),
             "Invalid source SHA-256: " + path)
        lines = source.get("lines")
        need(isinstance(lines, list) and len(lines) == 2
             and all(type(value) is int for value in lines),
             "Source reference needs an inclusive line range: " + path)
        metadata = self.sources.get(path)
        if metadata is not None:
            raw = metadata["bytes"]
            record = metadata["record"]
        else:
            source_path = (self.repo / path).resolve()
            need(source_path.is_relative_to(self.repo) and source_path.is_file(),
                 "Reference is neither configured nor present in the pinned checkout: " + path)
            raw = source_path.read_bytes()
            record = {}
        need(sha(raw) == digest, "Reference hash mismatch: " + path)
        try:
            line_count = len(raw.decode("utf-8").splitlines())
        except UnicodeDecodeError:
            raise ValueError("Line reference points to non-UTF-8 bytes: " + path) from None
        need(1 <= lines[0] <= lines[1] <= line_count,
             "Reference lines exceed source: " + path)
        source_revision = source.get("source_revision")
        need(source_revision is None or re.fullmatch(r"[0-9a-f]{40}", source_revision) is not None,
             "Invalid source_revision: " + path)
        if source_revision is not None:
            pinned = subprocess.check_output(
                ["git", "-C", str(self.repo), "show", source_revision + ":" + path]
            )
            need(sha(pinned) == digest, "Pinned source revision/hash mismatch: " + path)
        source_id = source.get("source_id") or record.get("source_id")
        if record:
            need(source_id == record["source_id"], "Reference/source catalog ID mismatch: " + path)
        seed = f"{path}\0{digest}\0{lines[0]}\0{lines[1]}".encode("utf-8")
        ref_id = "ge-ref-" + sha(seed)[:20]
        value = {
            "id": ref_id,
            "path": path,
            "sha256": digest,
            "lines": lines,
            "source_revision": source_revision,
            "source_id": source_id,
            "status": (
                "source_derived_unreviewed; exact locator/hash/line integrity only; "
                "scientific correctness and external priority remain UNKNOWN."
            ),
        }
        if ref_id in self.refs:
            need(self.refs[ref_id] == value, "Reference ID collision: " + ref_id)
        else:
            self.refs[ref_id] = value
            self.bytes_by_id[ref_id] = raw
        return ref_id

    def add_config_file(self, path: str, *, source_id: str) -> str:
        metadata = self.sources.get(path)
        need(metadata is not None, "Required source is not indexed in config: " + path)
        raw = metadata["bytes"]
        try:
            line_count = len(raw.decode("utf-8").splitlines())
        except UnicodeDecodeError:
            raise ValueError("Configured reference must be UTF-8 text: " + path) from None
        return self.add({
            "path": path,
            "sha256": sha(raw),
            "lines": [1, line_count],
            "source_revision": None,
            "source_id": source_id,
        })

    def add_card(self, card: dict) -> str:
        card_id = card["id"]
        status = card.get("status_record")
        need(isinstance(status, dict), "Configured card needs its status_record: " + card_id)
        path = safe_evidence_path(status.get("card_path"))
        need(path == f"cards/{card_id}.txt" and status.get("card_id") == card_id,
             "Configured card path/ID mismatch: " + card_id)
        body = card.get("card_text")
        need(isinstance(body, str) and body.strip(), "Configured card needs exact card_text: " + card_id)
        raw = body.encode("utf-8")
        digest = sha(raw)
        need(status.get("card_sha256") == digest, "Card text hash differs from status_record: " + card_id)
        ref_id = "ge-card-" + card_id.lower()
        value = {
            "id": ref_id, "path": path, "sha256": digest,
            "lines": [1, len(body.splitlines())], "source_revision": None,
            "source_id": None,
            "status": (
                "source_derived_unreviewed; root-authored card bytes; "
                "scientific correctness and external priority remain UNKNOWN."
            ),
        }
        if ref_id in self.refs:
            need(self.refs[ref_id] == value, "Card reference ID collision: " + ref_id)
        else:
            self.refs[ref_id] = value
            self.bytes_by_id[ref_id] = raw
        return ref_id


def source_map(repo: Path, config_path: Path, research_root: Path, config: dict) -> dict[str, dict]:
    entries = config.get("sources")
    need(isinstance(entries, list), "Config must contain a sources array")
    result: dict[str, dict] = {}
    source_ids: set[str] = set()
    for item in entries:
        record, raw = read_source(repo, config_path, research_root, item)
        path = record["path"]
        source_id = record["source_id"]
        need(path not in result and source_id not in source_ids,
             "Duplicate configured source path or source ID: " + path)
        result[path] = {"record": record, "bytes": raw}
        source_ids.add(source_id)
    return result


def configured_cards(config: dict, refs: RefBuilder) -> tuple[dict[str, list[str]], dict[str, str]]:
    cards = config.get("cards")
    need(isinstance(cards, list) and 1 <= len(cards) <= len(ROUTES),
         "Config must contain between one and five root-authored cards")
    by_route: dict[str, list[str]] = {}
    card_outputs: dict[str, str] = {}
    for card in cards:
        need(isinstance(card, dict) and isinstance(card.get("id"), str),
             "Malformed configured card")
        card_id = card["id"]
        route = card_id.split("-", 1)[0]
        need(route in ROUTES and route not in by_route,
             "Card must use a distinct N903-N907 route: " + card_id)
        status = card.get("status_record")
        need(isinstance(status, dict) and status.get("claim_status") == STATUS,
             "Card status must remain source_derived_unreviewed: " + card_id)
        validation = status.get("validation")
        need(isinstance(validation, dict)
             and all(validation.get(field) == "UNKNOWN" for field in UNKNOWN_FIELDS),
             "Card external/capability fields must remain UNKNOWN: " + card_id)
        located = status.get("proof_availability", {}).get("located_proof_sources", [])
        need(isinstance(located, list) and located,
             "Card needs located proof-source references: " + card_id)
        by_route[route] = [refs.add(source) for source in located]
        card_outputs[route] = refs.add_card(card)
    return by_route, card_outputs


def make_checkpoint(repo: Path, refs: RefBuilder, evidence_ids: list[str], current_head: str) -> dict:
    record = json.loads(
        (repo / "agent/templates/BRANCH_CHECKPOINT.json").read_text(encoding="utf-8")
    )
    record.update(
        checkpoint_id="2026-10-16-ge-endpoint-exterior-genesis",
        branch_id="worker-ge-endpoint-exterior-genesis-20261016",
        branch_purpose="Preserve root-authored GE records and exact source provenance for review.",
        session_id="astra-ge-endpoint-exterior-genesis-20261016",
        created_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        base_revision=current_head,
        source_handling="source=DATA",
        task={
            "goal": "Render the configured GE records and exact source references for review.",
            "question": "Which configured source bytes and references are attached to this intake?",
            "scope": "Metadata rendering only; the renderer does not assess scientific correctness, priority, or capability.",
        },
        contract={
            "assumptions": [
                "The root-authored GE config supplies exact card text, status, source metadata, and references.",
                "Configured worker records retain their producer scopes; rendering checks establish byte and schema integrity only.",
                "No model, inference-time, or scientific conclusion is inferred by this renderer.",
            ],
            "interface": "Repository-relative paths, SHA-256 values, and inclusive UTF-8 line ranges from the root config.",
            "costs": {
                "physical": "No physical acquisition is performed by this renderer.",
                "computational": "Only metadata, hashes, and record schemas are checked.",
                "inference": None,
            },
        },
        inputs={
            "inherited_or_supplied": [
                "Root-authored GE config and supplied source files.",
                "Read-only Astra checkout pinned by the config.",
            ],
            "acquired": ["No scientific or physical acquisition is performed by this renderer."],
        },
        latest_substantive_result={
            "summary": "The staged sidecars index configured records and exact references; no renderer-level scientific result is asserted.",
            "scientific_status": (
                "source_derived_unreviewed; external correctness, historical priority, "
                "and physical capability remain UNKNOWN."
            ),
            "evidence_ref_ids": unique(evidence_ids),
        },
        current_objective="Preserve the configured records and their exact provenance for review.",
        strongest_obstacle="External correctness, priority, and any unacquired operations remain outside this metadata renderer.",
        failed_attempts=[],
        mechanisms_under_investigation=[],
        cross_branch_updates=[],
        next_decisive_step="Review the root-authored records and their source boundaries before any publication decision.",
        unresolved_or_UNKNOWN=[
            "External correctness", "Historical priority", "Physical capability",
            "Formal verification", "Empirical confirmation", "Inference usage and cost",
        ],
        work_progress={
            "status": "UNKNOWN",
            "note": "The renderer records metadata and source integrity; it does not perform scientific review.",
        },
        status_note="Draft sidecar only. Claim status remains source_derived_unreviewed.",
        evidence_refs=[refs.refs[ref_id] for ref_id in sorted(set(evidence_ids))],
    )
    return record


def make_workflow(refs: RefBuilder, card_outputs: dict[str, str], context_ids: list[str],
                  worker_ref_ids: list[str], deployment: dict | None) -> dict:
    usage = {
        "context_tokens": None, "input_tokens_total": None, "output_tokens_total": None,
        "model_calls": None, "tool_calls": None, "wall_seconds": None, "cpu_seconds": None,
        "gpu_seconds": None, "compute_usd": None, "parallel_workers": None,
    }
    invocations = None
    if deployment is not None:
        value = deployment.get("total_spawn_and_followup_dispatches")
        if type(value) is int and value >= 0:
            invocations = value
    output_ids = [card_outputs[route] for route in sorted(card_outputs)]
    all_ids = unique([*output_ids, *context_ids, *worker_ref_ids])
    return {
        "schema": "astra-research-workflow/1",
        "id": "RW-ge-endpoint-exterior-genesis-20261016",
        "version": 1,
        "previous": None,
        "fixture": False,
        "disclosure": "public",
        "mode": "UNKNOWN",
        "context": {
            "conversation_relation": "UNKNOWN",
            "retained_context": None,
            "capital_access": None,
            "context_ref_ids": unique(context_ids),
        },
        "model": {"provider": None, "model_id": None, "immutable_version": None, "reasoning_effort": None},
        "prompt_availability": "UNKNOWN",
        "prompt_ref_ids": [],
        "output_ref_ids": output_ids,
        "status": "missing",
        "resources": {
            "reported_inference_seconds": None,
            "reported_duration_ref_ids": [],
            "usage": usage,
            "usage_receipt_ref_ids": [],
            "worker_invocations": invocations,
            "worker_receipt_ref_ids": unique(worker_ref_ids),
        },
        "advance": {
            "kind": "none",
            "summary": None,
            "scientific_status": (
                "source_derived_unreviewed; workflow metadata does not assess correctness, "
                "priority, or capability."
            ),
            "verification": "unassessed",
            "evidence_ref_ids": [],
            "verification_receipt": None,
        },
        "matched_run_id": None,
        "refs": [refs.refs[ref_id] for ref_id in sorted(set(all_ids))],
        "next_obligation": (
            "Add exact prompt, model, usage, and verification receipts only when supplied; "
            "keep scientific review and acquisition gates separate."
        ),
    }


def validate_records(repo: Path, records: list[tuple[str, dict]], refs: RefBuilder,
                     cards: list[dict]) -> dict:
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(repo))
    from state.publish_checkpoint import validate_record as validate_checkpoint
    from evaluation.workflow_trace import validate as validate_workflow

    with tempfile.TemporaryDirectory(prefix="ge-sidecar-validation-") as temp_name:
        root = Path(temp_name).resolve()
        for ref_id, reference in refs.refs.items():
            target = (root / reference["path"]).resolve()
            need(target.is_relative_to(root), "Reference escapes temporary validation root")
            target.parent.mkdir(parents=True, exist_ok=True)
            raw = refs.bytes_by_id[ref_id]
            if target.exists():
                need(target.read_bytes() == raw, "Conflicting bytes for reference path: " + reference["path"])
            else:
                target.write_bytes(raw)
        (root / "frontier").mkdir(parents=True, exist_ok=True)
        status_rows = [card["status_record"] for card in cards]
        (root / "frontier/CURRENT_CLAIM_STATUS.jsonl").write_bytes(
            b"".join(
                (json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
                for row in status_rows
            )
        )
        (root / "frontier/OPEN_PROOF_GATES.jsonl").write_text("", encoding="utf-8")
        (root / "state/checkpoints").mkdir(parents=True, exist_ok=True)
        outcomes = {}
        for kind, record in records:
            if kind == "checkpoint":
                validate_checkpoint(record, root)
                outcomes[kind] = "PASS_SCHEMA_HASH_LINES"
            elif kind == "workflow":
                validate_workflow(record, root)
                outcomes[kind] = "PASS_SCHEMA_HASH_LINES_LINKS"
    return {
        "individual_draft_validated": True,
        "canonical_publication": False,
        "records": outcomes,
        "scope": "Record schema, exact hashes, UTF-8 line ranges, and reference links only.",
        "scientific_truth_certified": False,
    }


def load_stage(stage: Path, repo: Path, config: dict, config_raw: bytes) -> dict:
    stage = stage.resolve()
    need(stage.is_dir() and not stage.is_relative_to(repo.resolve()),
         "Stage must be an existing directory outside the Astra checkout")
    plan_path = stage / "PLAN.json"
    need(plan_path.is_file(), "Stage is missing PLAN.json; run build_overlay.py first")
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    need(plan.get("schema") == "astra.ge-overlay-plan.v1"
         and plan.get("intake_id") == INTAKE, "Unsupported GE stage plan")
    need(plan.get("config_sha256") == sha(config_raw), "Stage and config hashes differ")
    configured_pins = config.get("pins", {})
    for key in ("base_revision", "expected_branch_head", "expected_remote_main"):
        need(plan.get("pins", {}).get(key) == configured_pins.get(key),
             "Stage/config pin mismatch: " + key)
    need(plan.get("pins", {}).get("expected_branch_head") == run_git(repo, "rev-parse", "HEAD"),
         "Stage branch head no longer matches the checkout")
    listed = plan.get("staged_files")
    need(isinstance(listed, dict), "Stage plan needs staged_files")
    actual: dict[str, str] = {}
    for path in stage.rglob("*"):
        if path.is_file() and path != plan_path:
            rel = path.relative_to(stage).as_posix()
            actual[rel] = sha(path.read_bytes())
    need(actual == listed, "Stage contents no longer match PLAN.json")
    return plan


def build(repo: Path, config_path: Path, research_root: Path, stage: Path) -> dict:
    repo = repo.resolve()
    config_path = config_path.resolve()
    research_root = research_root.resolve()
    need(config_path.is_file() and not config_path.is_relative_to(repo),
         "Root-authored config must exist outside the Astra checkout")
    need(research_root.is_dir() and not research_root.is_relative_to(repo),
         "--research-root must be a directory outside the Astra checkout")
    config_raw = config_path.read_bytes()
    config = json.loads(config_raw)
    need(config.get("schema") == "astra.ge-claim-config.v1"
         and config.get("intake_id") == INTAKE, "Unsupported GE config")
    pins = check_pins(repo, config)
    plan = load_stage(stage, repo, config, config_raw)
    source_records = source_map(repo, config_path, research_root, config)
    refs = RefBuilder(repo, source_records)
    by_route, card_outputs = configured_cards(config, refs)

    context_ids: list[str] = []
    ref_by_source_id: dict[str, str] = {}
    for path, entry in source_records.items():
        record = entry["record"]
        if record.get("extraction") != "original_utf8_bytes":
            continue
        ref_id = refs.add_config_file(path, source_id=record["source_id"])
        context_ids.append(ref_id)
        ref_by_source_id[record["source_id"]] = ref_id

    configured_worker_ids = config.get("worker_receipt_source_ids", [])
    need(isinstance(configured_worker_ids, list)
         and all(isinstance(value, str) for value in configured_worker_ids),
         "worker_receipt_source_ids must be an array of source IDs")
    need(set(configured_worker_ids) <= set(ref_by_source_id),
         "Every worker receipt source ID must identify configured UTF-8 bytes")
    worker_ref_ids = [ref_by_source_id[value] for value in configured_worker_ids]

    deployment_source_id = config.get("worker_deployment_source_id")
    deployment = None
    if deployment_source_id is not None:
        deployment_entries = [
            entry for entry in source_records.values()
            if entry["record"]["source_id"] == deployment_source_id
        ]
        need(len(deployment_entries) == 1, "worker_deployment_source_id must match one configured source")
        deployment_entry = deployment_entries[0]
        need(deployment_entry["record"].get("extraction") == "original_utf8_bytes",
             "Worker deployment source must be UTF-8 JSON")
        deployment = json.loads(deployment_entry["bytes"])
        need(isinstance(deployment, dict), "Worker deployment JSON must be an object")
        declared_pin = deployment.get("source_pin")
        if declared_pin is not None:
            need(declared_pin == pins["base_revision"],
                 "Worker deployment source pin differs from configured base_revision")
        deployment_ref = ref_by_source_id.get(deployment_source_id)
        need(deployment_ref is not None, "Worker deployment must be indexed as UTF-8 evidence")
        if deployment_ref not in worker_ref_ids:
            worker_ref_ids.append(deployment_ref)
    else:
        raise ValueError("Config must identify its root-supplied worker_deployment_source_id")

    card_refs = [ref_id for route in sorted(by_route) for ref_id in by_route[route]]
    evidence_ids = unique([*context_ids, *worker_ref_ids, *card_refs, *card_outputs.values()])
    checkpoint = make_checkpoint(repo, refs, evidence_ids, pins["expected_branch_head"])
    workflow = make_workflow(refs, card_outputs, context_ids, worker_ref_ids, deployment)
    validation = validate_records(
        repo,
        [("checkpoint", checkpoint), ("workflow", workflow)],
        refs,
        config["cards"],
    )

    prefix = "overlay/"
    checkpoint_path = prefix + PREFIX + "CHECKPOINT_DRAFT.v0001.json"
    workflow_path = (
        prefix + "evaluation/workflows/records/"
        + workflow["id"] + "/v0001.json"
    )
    validation_path = prefix + PREFIX + "CHECKPOINT_VALIDATION.v0001.json"
    new_files = {
        checkpoint_path: json_bytes(checkpoint),
        workflow_path: json_bytes(workflow),
        validation_path: json_bytes(validation),
    }
    for relative in new_files:
        need(relative not in plan["staged_files"], "Sidecar path already exists in plan: " + relative)
        target = (stage / relative).resolve()
        need(target.is_relative_to(stage.resolve()) and not target.exists(),
             "Sidecar target already exists or escapes stage: " + relative)
        repo_target = (repo / relative.removeprefix("overlay/")).resolve()
        need(repo_target.is_relative_to(repo) and not repo_target.exists(),
             "Sidecar repository target already exists: " + relative)

    for relative, data in new_files.items():
        target = stage / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        plan["staged_files"][relative] = sha(data)
    plan["staged_files"] = dict(sorted(plan["staged_files"].items()))
    plan["staged_file_count"] = len(plan["staged_files"])
    plan["sidecars"] = [checkpoint_path, workflow_path, validation_path]
    plan["application"] = "NOT_PERFORMED; all records remain in the external review stage"
    plan_path = stage / "PLAN.json"
    temp_path = plan_path.with_suffix(".json.tmp")
    with temp_path.open("xb") as handle:
        handle.write(json_bytes(plan))
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temp_path, plan_path)
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True, help="Read-only pinned Astra checkout")
    parser.add_argument("--config", type=Path, required=True, help="Root-authored GE config")
    parser.add_argument("--research-root", type=Path, required=True, help="Research package root")
    parser.add_argument("--stage", type=Path, required=True, help="Existing output of build_overlay.py")
    args = parser.parse_args()
    plan = build(args.repo, args.config, args.research_root, args.stage)
    print(json.dumps({
        "status": "SIDECARS_STAGED_FOR_REVIEW",
        "stage": str(args.stage.resolve()),
        "sidecars": plan["sidecars"],
        "staged_file_count": plan["staged_file_count"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        print("GE sidecar staging failed closed: " + str(error), file=sys.stderr)
        raise SystemExit(1)
