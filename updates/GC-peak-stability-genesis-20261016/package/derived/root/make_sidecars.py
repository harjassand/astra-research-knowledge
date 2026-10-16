#!/usr/bin/env python3
"""Stage provenance-linked GC checkpoint, workflow, and opportunity sidecars.

The renderer reads the pinned Astra checkout and a root-authored GC claim
configuration. It writes a new review tree outside the checkout and has no
apply mode. Scientific content is referenced from the configuration and frozen
worker reports; the renderer does not author or promote claims.
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

BASE = "9dbe934e5475f415c2d160a6c0715534aafa546b"
INTAKE = "GC-peak-stability-genesis-20261016"
PREFIX = f"updates/{INTAKE}/"
BOUNDARY = (
    "source_derived_unreviewed; external correctness, historical priority, physical capability, "
    "and matched practical advantage remain UNKNOWN. Hashes and schema checks are integrity "
    "checks only."
)
UNKNOWN_FIELDS = (
    "external_correctness", "historical_priority", "physical_capability",
    "formal_verification", "empirical_confirmation",
)
CARD_ROUTES = {
    "N894": "control",
    "N895": "homogeneous tube",
    "N896": "kinetic output",
    "N897": "equal-duty catalysis",
}


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def run_git(repo: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), *args], text=True, stderr=subprocess.PIPE
    ).strip()


def safe_repo_path(value: object) -> str:
    need(isinstance(value, str) and value and not Path(value).is_absolute(),
         "Evidence path must be repository-relative")
    path = Path(value)
    need(".." not in path.parts and "\\" not in value, "Unsafe evidence path: " + value)
    return value


def check_repo(repo: Path, expected_head: str) -> None:
    actual = run_git(repo, "rev-parse", "HEAD")
    need(re.fullmatch(r"[0-9a-f]{40}", expected_head) is not None,
         "Config expected_branch_head must be a full Git SHA")
    need(actual == expected_head, f"Astra HEAD mismatch: expected {expected_head}, observed {actual}")
    subprocess.check_call(["git", "-C", str(repo), "cat-file", "-e", BASE + "^{commit}"])
    need(not run_git(repo, "status", "--porcelain"),
         "Astra checkout is not clean; refusing to stage sidecars")


def load_sources(repo: Path, config_path: Path, config: dict) -> dict[str, dict]:
    sources: dict[str, dict] = {}
    source_ids: set[str] = set()
    records = config.get("sources")
    need(isinstance(records, list), "claim config must contain a sources array")
    for item in records:
        need(isinstance(item, dict) and isinstance(item.get("record"), dict),
             "Each configured source needs a record")
        record = item["record"]
        path = safe_repo_path(record.get("path"))
        need(path.startswith(PREFIX), "GC source must be under " + PREFIX + path)
        for key in ("source_id", "sha256", "bytes", "extraction"):
            need(key in record, "Source record is missing " + key + ": " + path)
        need(re.fullmatch(r"src-GC-[A-Za-z0-9_-]+", record["source_id"]) is not None,
             "Configured source ID must use src-GC- namespace: " + path)
        need(record["source_id"] not in source_ids, "Duplicate configured source ID: " + record["source_id"])
        source_ids.add(record["source_id"])
        source_name = item.get("source_file")
        if source_name is None:
            source_path = (repo / path).resolve()
        else:
            source_path = Path(source_name)
            if not source_path.is_absolute():
                source_path = (config_path.parent / source_path).resolve()
        need(source_path.is_file(), "Configured source file is missing: " + str(source_path))
        raw = source_path.read_bytes()
        need(sha(raw) == record["sha256"], "Configured source hash mismatch: " + path)
        need(len(raw) == record["bytes"], "Configured source byte-count mismatch: " + path)
        try:
            raw.decode("utf-8")
            extraction = "original_utf8_bytes"
        except UnicodeDecodeError:
            extraction = "original_binary_bytes"
        need(record["extraction"] == extraction, "Configured extraction disagrees with bytes: " + path)
        need(path not in sources, "Duplicate configured source path: " + path)
        sources[path] = {"record": record, "bytes": raw, "external_path": source_path}
    return sources


class RefBuilder:
    def __init__(self, repo: Path, sources: dict[str, dict]):
        self.repo = repo
        self.sources = sources
        self.refs: dict[str, dict] = {}
        self.bytes_by_id: dict[str, bytes] = {}

    def add(self, source: dict, *, fallback_id: str | None = None) -> str:
        path = safe_repo_path(source.get("path"))
        digest = source.get("sha256")
        need(isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest),
             "Invalid source SHA-256: " + path)
        lines = source.get("lines")
        need(isinstance(lines, list) and len(lines) == 2
             and all(type(x) is int for x in lines), "Source reference needs inclusive line range: " + path)
        metadata = self.sources.get(path)
        if metadata is not None:
            raw = metadata["bytes"]
            record = metadata["record"]
        else:
            source_path = (self.repo / path).resolve()
            need(source_path.is_relative_to(self.repo) and source_path.is_file(),
                 "Reference is neither configured nor present in pinned checkout: " + path)
            raw = source_path.read_bytes()
            record = {}
        need(sha(raw) == digest, "Reference hash mismatch: " + path)
        try:
            line_count = len(raw.decode("utf-8").splitlines())
        except UnicodeDecodeError:
            raise ValueError("Line reference points to non-UTF-8 bytes: " + path) from None
        need(1 <= lines[0] <= lines[1] <= line_count, "Reference lines exceed source: " + path)
        source_revision = source.get("source_revision")
        need(source_revision is None or re.fullmatch(r"[0-9a-f]{40}", source_revision) is not None,
             "Invalid source_revision: " + path)
        if source_revision is not None:
            pinned = subprocess.check_output(["git", "-C", str(self.repo), "show", source_revision + ":" + path])
            need(sha(pinned) == digest, "Pinned source revision/hash mismatch: " + path)
        source_id = source.get("source_id") or record.get("source_id")
        if record:
            need(source_id == record["source_id"], "Reference/source catalog ID mismatch: " + path)
        label_seed = f"{path}\0{digest}\0{lines[0]}\0{lines[1]}".encode("utf-8")
        ref_id = fallback_id or ("gc-ref-" + sha(label_seed)[:20])
        status = source.get("status") or BOUNDARY
        value = {
            "id": ref_id,
            "path": path,
            "sha256": digest,
            "lines": lines,
            "source_revision": source_revision,
            "source_id": source_id,
            "status": status,
        }
        if ref_id in self.refs:
            need(self.refs[ref_id] == value, "Reference ID collision: " + ref_id)
        else:
            self.refs[ref_id] = value
            self.bytes_by_id[ref_id] = raw
        return ref_id

    def add_config_file(self, path: str, *, fallback_id: str | None = None) -> str:
        path = safe_repo_path(path)
        item = self.sources.get(path)
        need(item is not None, "Required file is not indexed in claim config: " + path)
        raw = item["bytes"]
        try:
            lines = len(raw.decode("utf-8").splitlines())
        except UnicodeDecodeError:
            raise ValueError("Configured reference must be UTF-8 text: " + path) from None
        return self.add({
            "path": path,
            "sha256": sha(raw),
            "lines": [1, lines],
            "source_revision": None,
            "source_id": item["record"]["source_id"],
            "status": BOUNDARY,
        }, fallback_id=fallback_id)

    def add_card(self, card: dict) -> str:
        card_id = card["id"]
        status = card.get("status_record")
        need(isinstance(status, dict), "Configured card needs its exact status record: " + card_id)
        path = safe_repo_path(status.get("card_path"))
        need(path == f"cards/{card_id}.txt" and status.get("card_id") == card_id,
             "Configured card path/ID mismatch: " + card_id)
        raw = card["card_text"].encode("utf-8")
        digest = sha(raw)
        need(status.get("card_sha256") == digest, "Configured card text hash differs from its status record: " + card_id)
        lines = len(raw.decode("utf-8").splitlines())
        ref_id = "card-" + card_id.lower()
        value = {
            "id": ref_id,
            "path": path,
            "sha256": digest,
            "lines": [1, lines],
            "source_revision": None,
            "source_id": None,
            "status": BOUNDARY,
        }
        if ref_id in self.refs:
            need(self.refs[ref_id] == value, "Card reference ID collision: " + ref_id)
        else:
            self.refs[ref_id] = value
            self.bytes_by_id[ref_id] = raw
        return ref_id


def card_refs(config: dict, refs: RefBuilder) -> dict[str, list[str]]:
    cards = config.get("cards")
    need(isinstance(cards, list) and len(cards) == 4,
         "Root claim config must contain the four GC cards")
    by_route: dict[str, list[str]] = {}
    for card in cards:
        need(isinstance(card, dict) and isinstance(card.get("id"), str), "Malformed configured card")
        route = card["id"].split("-", 1)[0]
        need(route in CARD_ROUTES, "Card route is outside N894-N897: " + card["id"])
        need(route not in by_route, "Duplicate card route: " + route)
        status = card.get("status_record")
        need(isinstance(status, dict) and status.get("claim_status") == "source_derived_unreviewed",
             "Every GC card status must remain source_derived_unreviewed: " + card["id"])
        validation = status.get("validation")
        need(isinstance(validation, dict) and all(validation.get(field) == "UNKNOWN" for field in UNKNOWN_FIELDS),
             "External and capability fields must remain UNKNOWN: " + card["id"])
        located = status.get("proof_availability", {}).get("located_proof_sources", [])
        need(isinstance(located, list) and located, "Card needs exact located proof references: " + card["id"])
        by_route[route] = [refs.add(source) for source in located]
    need(set(by_route) == set(CARD_ROUTES), "Config must include one card on each route N894-N897")
    return by_route


def unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def check_config(config: dict, repo: Path) -> dict:
    need(config.get("schema") == "astra.gc-claim-config.v1", "Unsupported GC config schema")
    need(config.get("intake_id") == INTAKE, "Unexpected GC intake ID")
    pins = config.get("pins")
    need(isinstance(pins, dict) and pins.get("base_revision") == BASE,
         "Config base_revision must use the frozen GC source pin")
    expected_head = pins.get("expected_branch_head")
    check_repo(repo, expected_head)
    return pins


def worker_deployment(sources: dict[str, dict]) -> tuple[str, dict]:
    path = next((path for path in sources if path.endswith("/WORKER_DEPLOYMENT.json")), None)
    need(path is not None, "Claim config must index WORKER_DEPLOYMENT.json")
    data = json.loads(sources[path]["bytes"])
    need(data.get("schema") == "astra.gc-worker-deployment.v1"
         and data.get("source_pin") == BASE
         and data.get("initial_workers") == 10
         and data.get("initial_sol_max") == 8
         and data.get("initial_luna_max") == 2
         and data.get("total_worker_invocations") == 12,
         "Worker deployment counts or base pin differ from the frozen GC dispatch record")
    roles = {item.get("role") for item in data.get("followup_dispatches", []) if isinstance(item, dict)}
    need("External checkpoint/workflow/technology sidecar renderer" in roles
         and "Public archive rehydration and evidence replay orchestration" in roles,
         "Worker deployment must include the renderer and identity public-replay follow-ups")
    return path, data


def make_checkpoint(repo: Path, card_refs_by_route: dict[str, list[str]], refs: RefBuilder,
                    synthesis_ref: str, worker_ref_ids: list[str], current_head: str) -> dict:
    evidence = unique([*card_refs_by_route["N894"], *card_refs_by_route["N895"],
                       *card_refs_by_route["N896"], *card_refs_by_route["N897"],
                       synthesis_ref, *worker_ref_ids])
    cp = json.loads((repo / "agent/templates/BRANCH_CHECKPOINT.json").read_text(encoding="utf-8"))
    cp.update(
        checkpoint_id="2026-10-16-peak-stability-genesis",
        branch_id="worker-gc-peak-stability-genesis",
        branch_purpose="Preserve scoped peak-control, homogeneous-tube, kinetic-output, and equal-duty research records with exact provenance.",
        session_id="astra-gc-peak-stability-genesis-20261016",
        created_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        base_revision=current_head,
        source_handling="source=DATA",
        task={
            "goal": "Stage the four root-authored GC cards and provenance-linked follow-up records for review.",
            "question": "Which exact configured sources and open acquisition obligations accompany N894-N897?",
            "scope": "Metadata and reference rendering only; source claims retain their producer-defined scopes and unreviewed status.",
        },
        contract={
            "assumptions": [
                "The root-authored GC claim config is the source of card IDs, texts, statuses, and located proof references.",
                "Worker reports and frozen receipts retain their producer scopes; renderer checks do not establish scientific truth.",
                "Proposed technology work describes only unacquired control, causal-test, and backward-weight interfaces.",
            ],
            "interface": "Repository-relative source paths, exact SHA-256 values, and inclusive UTF-8 line ranges from the root config.",
            "costs": {
                "physical": "No physical control or causal experiment was acquired by this renderer.",
                "computational": "No scientific computation was performed by this renderer; only metadata and reference integrity are checked.",
                "inference": None,
            },
        },
        inputs={
            "inherited_or_supplied": [
                f"Root-authored GC claim config; supplied Astra source package pin {BASE}.",
                "Frozen worker reports and receipts cited by each configured card.",
            ],
            "acquired": ["No new scientific or physical acquisition was performed by the sidecar renderer."],
        },
        latest_substantive_result={
            "summary": "The external sidecar stage carries the configured N894-N897 records and their exact references; no renderer-level scientific result is asserted.",
            "scientific_status": "source_derived_unreviewed; external correctness, historical priority, and physical capability remain UNKNOWN.",
            "evidence_ref_ids": evidence,
        },
        current_objective="Preserve exact source boundaries, open acquisition gates, and append-only review artifacts.",
        strongest_obstacle="External correctness review and the physical or causal acquisition obligations remain open.",
        failed_attempts=[],
        mechanisms_under_investigation=[
            "Unacquired private-refresh physical control and its full action/support interface.",
            "Prospective equal-duty causal experiment with measured exposure and output costs.",
            "Unacquired goal-specific backward weights with a complete residual bound for the kinetic output.",
        ],
        cross_branch_updates=[],
        next_decisive_step="Review each configured card and acquire only its stated missing operation, including the exact model, controls, uncertainty, and full resource costs.",
        unresolved_or_UNKNOWN=[
            "External correctness", "Historical priority", "Physical capability", "Causal interpretation",
            "Goal-specific backward-weight certification", "Aggregate inference usage and cost",
        ],
        work_progress={
            "status": "reviewed",
            "note": "The sidecar renderer inspected source scopes and validates references; this is not external scientific review.",
        },
        status_note="Draft sidecar only. No claim is promoted, no checkpoint ancestry is invented, and no canonical publication is performed.",
        evidence_refs=[refs.refs[ref_id] for ref_id in sorted(evidence)],
    )
    return cp


def make_workflow(repo: Path, card_refs_by_route: dict[str, list[str]], refs: RefBuilder,
                  synthesis_ref: str, identity_ref: str | None, worker_ref_ids: list[str],
                  worker_count: int, current_head: str,
                  card_output_ids: dict[str, str]) -> dict:
    workflow = json.loads((repo / "evaluation/templates/WORKFLOW_TRACE.json").read_text(encoding="utf-8"))
    output_ids = [synthesis_ref, *[card_output_ids[route] for route in sorted(CARD_ROUTES)]]
    if identity_ref is not None:
        output_ids.append(identity_ref)
    context_ids = [synthesis_ref]
    if identity_ref is not None:
        context_ids.append(identity_ref)
    all_refs = unique([*output_ids, *worker_ref_ids,
                       *[rid for route in CARD_ROUTES for rid in card_refs_by_route[route]]])
    workflow.update(
        id="RW-gc-peak-stability-genesis-20261016",
        mode="source_intensive_multi_agent",
        context={
            "conversation_relation": "same",
            "retained_context": (
                "The initial worker round comprised 8 Sol Max and 2 Luna Max assignments. "
                "This sidecar-renderer task and the identity-public-replay task were follow-ups. "
                "No inference-token, model-cost, or full usage receipts are available."
            ),
            "capital_access": (
                f"Read-only Astra checkout at {current_head}; supplied source package pin {BASE}; "
                "route IDs N894-N897 are the staged intake context."
            ),
            "context_ref_ids": context_ids,
        },
        model={"provider": None, "model_id": None, "immutable_version": None, "reasoning_effort": None},
        prompt_availability="UNKNOWN",
        prompt_ref_ids=[],
        output_ref_ids=unique(output_ids),
        status="completed",
        resources={
            "reported_inference_seconds": None,
            "reported_duration_ref_ids": [],
            "usage": {
                "context_tokens": None, "input_tokens_total": None, "output_tokens_total": None,
                "model_calls": None, "tool_calls": None, "wall_seconds": None, "cpu_seconds": None,
                "gpu_seconds": None, "compute_usd": None, "parallel_workers": None,
            },
            "usage_receipt_ref_ids": [],
            "worker_invocations": worker_count,
            "worker_receipt_ref_ids": unique(worker_ref_ids),
        },
        advance={
            "kind": "none",
            "summary": None,
            "scientific_status": "source_derived_unreviewed; workflow bookkeeping does not evaluate correctness, priority, or capability.",
            "verification": "unassessed",
            "evidence_ref_ids": [],
            "verification_receipt": None,
        },
        matched_run_id=None,
        refs=[refs.refs[ref_id] for ref_id in sorted(all_refs)],
        next_obligation="Obtain exact prompt and per-model usage/cost receipts before any workflow comparison; review scientific claims and acquisition gates separately.",
    )
    return workflow


TECHNOLOGY = {
    "N894": {
        "slug": "private-control-acquisition",
        "domain": "hybrid",
        "problem": "Acquire and qualify a finite-duration private-refresh control operation under its stated pointwise action envelope and shared-bath interface.",
        "current_best": "The frozen reports identify established randomized dynamical-decoupling comparators; no matched physical implementation for this intake is recorded as acquired.",
        "limitation": "A physical dilation, pointwise envelope, private-bit integrity, finite-width gate support, controller/bath isolation, reset, and matched full costs remain unacquired.",
        "mechanism": "Measure one declared private-refresh schedule together with its actual time-dependent action bound, support, leakage controls, and complete preparation, switching, reset, and reservation costs.",
        "next": "Acquire an exact pointwise envelope and qualify one complete finite-duration private-refresh operation, including all support, privacy, ramp, reset, and matched-comparator costs.",
        "metric": "Scope-matched endpoint error and complete control cost under the acquired envelope",
        "unit": "No numeric physical target has been acquired",
        "comparator": "An equally informed randomized-control comparator with identical task and resource accounting; no matched device result is recorded.",
    },
    "N896": {
        "slug": "kinetic-backward-weights",
        "domain": "software",
        "problem": "Obtain a goal-specific backward-weight or committor representation for the stated kinetic output with a rigorous full-model remainder.",
        "current_best": "No acquired full-state backward approximation and certified residual for the configured output is recorded.",
        "limitation": "Backward weights, the exact generator/output pairing, all sink and join terms, and a complete residual or rounding bound remain unacquired for the proposed certificate.",
        "mechanism": "Generate candidate goal-specific backward weights, then independently enclose their exact-generator residual, time joins, terminal term, representation error, and all sink/overflow contributions.",
        "next": "Acquire and independently verify a goal-specific backward approximation and complete residual against the exact capped process before making any output-bound or solver-cost claim.",
        "metric": "Certified enclosure of the requested kinetic output with all residual and representation terms",
        "unit": "No numerical target or verified backward weights are supplied by this opportunity record",
        "comparator": "Equally informed FSP, absorbing tensor evolution, and splitting; no matched full solve or cost comparison is recorded as acquired.",
    },
    "N897": {
        "slug": "equal-duty-causal-test",
        "domain": "hybrid",
        "problem": "Acquire a prospective causal test for the equal-duty catalysis observation with calibrated exposure, output, and uncertainty measurements.",
        "current_best": "The frozen package contains scoped reported means and sampled traces; it does not contain a prospective randomized causal record with complete measurement and resource costs.",
        "limitation": "Native calibration, replicate-level uncertainty, matched exposure, fresh-cohort recovery, complete electrical and material work, and useful-product output remain unacquired for a causal technology claim.",
        "mechanism": "Predeclare randomized equal-duty blocks, measure protocol-specific exposure and current, track fresh-cohort recovery, and quantify isotope-specific useful output with calibration and failure accounting.",
        "next": "Run a prospective randomized causal test only after the input, exposure, electrical, isotope-specific measurement, fresh-cohort, uncertainty, and full-cost contracts are fixed.",
        "metric": "Causal output change and useful product per complete measured resource cost",
        "unit": "No prospective effect size, uncertainty, or numeric acceptance target is acquired",
        "comparator": "Exposure-matched static and periodic protocols under the same measured input, product definition, and full cost boundary.",
    },
}


def make_technology(route: str, card_ids: list[str], refs: RefBuilder) -> dict:
    spec = TECHNOLOGY[route]
    ref_ids = unique(card_ids)
    return {
        "schema": "astra-technology/1",
        "id": "T-gc-" + spec["slug"],
        "version": 1,
        "previous": None,
        "fixture": False,
        "disclosure": "public",
        "domain": spec["domain"],
        "stage": "opportunity",
        "disposition": "active",
        "capability": {
            "problem": spec["problem"],
            "current_best": spec["current_best"],
            "limitation": spec["limitation"],
            "proposed_mechanism": spec["mechanism"],
            "baseline_ref_ids": ref_ids,
            "target": {
                "metric": spec["metric"], "baseline": None, "desired": None,
                "unit": spec["unit"], "conditions": spec["next"], "comparator": spec["comparator"],
            },
        },
        "assessment": {
            "potential_significance": {
                "judgement": "UNKNOWN; no acquired capability or practical advantage is established.",
                "basis_ref_ids": ref_ids,
                "limits": BOUNDARY,
            },
            "scientific_evidence": {
                "judgement": "source_derived_unreviewed",
                "basis_ref_ids": ref_ids,
                "limits": "Cited internal records only; these are not external validation or evidence of a realized technology.",
            },
            "feasibility_and_readiness": {
                "judgement": "UNKNOWN; the named control, causal test, or backward-weight interface remains unacquired.",
                "basis_ref_ids": ref_ids,
                "limits": BOUNDARY,
            },
            "next_step_value": {
                "judgement": "UNKNOWN until the missing acquisition and its complete costs are measured.",
                "basis_ref_ids": ref_ids,
                "limits": "An opportunity record is not an experiment result, prototype, or capability demonstration.",
            },
        },
        "refs": [refs.refs[ref_id] for ref_id in sorted(ref_ids)],
        "next_obligation": spec["next"],
    }


def validate_staged_records(repo: Path, stage: dict[str, bytes], records: list[tuple[str, dict]],
                            refs: RefBuilder, cards: list[dict]) -> dict:
    """Run the repository's record validators against exact bytes in a temp root."""
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(repo))
    from state.publish_checkpoint import validate_record as validate_checkpoint
    from evaluation.workflow_trace import validate as validate_workflow
    from technology.validate import validate as validate_technology

    with tempfile.TemporaryDirectory(prefix="gc-sidecar-validation-") as temp_name:
        temp_root = Path(temp_name).resolve()
        for ref_id, reference in refs.refs.items():
            target = (temp_root / reference["path"]).resolve()
            need(target.is_relative_to(temp_root), "Reference path escapes temporary validation root")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(refs.bytes_by_id[ref_id])
        (temp_root / "evaluation/workflows/records").mkdir(parents=True, exist_ok=True)
        (temp_root / "technology/records").mkdir(parents=True, exist_ok=True)
        (temp_root / "frontier").mkdir(parents=True, exist_ok=True)
        routes_file = repo / "technology/routes.tsv"
        (temp_root / "technology/routes.tsv").write_bytes(routes_file.read_bytes())
        with routes_file.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                path = safe_repo_path(row["entry_point"])
                source = (repo / path).resolve()
                need(source.is_relative_to(repo) and source.is_file(),
                     "Repository route entry point is missing: " + path)
                target = temp_root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(source.read_bytes())
        status_rows = [card["status_record"] for card in cards]
        (temp_root / "frontier/CURRENT_CLAIM_STATUS.jsonl").write_bytes(
            b"".join((json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
                     for row in status_rows)
        )
        (temp_root / "frontier/OPEN_PROOF_GATES.jsonl").write_text("", encoding="utf-8")
        (temp_root / "state/checkpoints").mkdir(parents=True, exist_ok=True)
        outcomes = {}
        for kind, record in records:
            if kind == "checkpoint":
                validate_checkpoint(record, temp_root)
                outcomes[kind] = "PASS_SCHEMA_HASH_LINES"
            elif kind == "workflow":
                validate_workflow(record, temp_root)
                outcomes[kind] = "PASS_SCHEMA_HASH_LINES_LINKS"
            elif kind == "technology":
                validate_technology(record, temp_root)
                outcomes[kind + ":" + record["id"]] = "PASS_SCHEMA_HASH_LINES_LINKS"
    return {
        "individual_draft_validated": True,
        "canonical_publication": False,
        "records": outcomes,
        "scope": "Record schema, repository-relative paths, exact hashes, UTF-8 line ranges, and reference links only; no scientific validation.",
        "external_truth_certified": False,
    }


def add_output(stage: dict[str, bytes], path: str, data: bytes) -> None:
    need(path not in stage, "Duplicate staged path: " + path)
    stage[path] = data


def build(repo: Path, config_path: Path, output: Path) -> dict:
    repo = repo.resolve()
    config_path = config_path.resolve()
    output = output.resolve()
    need(config_path.is_file(), "Missing root-authored claim config: " + str(config_path))
    need(not config_path.is_relative_to(repo), "Claim config must be outside Astra checkout")
    need(not output.is_relative_to(repo), "Output must remain outside Astra checkout")
    need(not output.exists(), "Refusing to overwrite existing sidecar output directory: " + str(output))
    config_raw = config_path.read_bytes()
    config = json.loads(config_raw)
    pins = check_config(config, repo)
    source_records = load_sources(repo, config_path, config)
    deployment_path, deployment = worker_deployment(source_records)
    refs = RefBuilder(repo, source_records)
    by_route = card_refs(config, refs)
    cards_by_route = {card["id"].split("-", 1)[0]: card for card in config["cards"]}

    synthesis_path = next((path for path in source_records
                           if path.endswith("/SCIENTIFIC_SYNTHESIS.md")), None)
    need(synthesis_path is not None, "Claim config must index root SCIENTIFIC_SYNTHESIS.md")
    synthesis_ref = refs.add_config_file(synthesis_path, fallback_id="gc-synthesis")
    identity_path = next((path for path in source_records
                          if path.endswith("/gc_identity_replay/IDENTITY_RECEIPT.json")), None)
    identity_ref = refs.add_config_file(identity_path, fallback_id="gc-identity-replay") if identity_path else None
    worker_paths = [path for path in source_records
                    if path.endswith("/WORKER_DEPLOYMENT.json") or path.endswith("/FROZEN.json")]
    worker_ref_ids = [refs.add_config_file(path) for path in sorted(worker_paths)]
    if identity_ref is not None:
        worker_ref_ids = unique([*worker_ref_ids, identity_ref])

    card_output_ids = {
        route: refs.add_card(cards_by_route[route]) for route in CARD_ROUTES
    }
    cp = make_checkpoint(repo, by_route, refs, synthesis_ref, worker_ref_ids,
                         pins["expected_branch_head"])
    workflow = make_workflow(repo, by_route, refs, synthesis_ref, identity_ref,
                             worker_ref_ids, deployment["total_worker_invocations"],
                             pins["expected_branch_head"], card_output_ids)
    technologies = [make_technology(route, by_route[route] + [card_output_ids[route]], refs)
                    for route in TECHNOLOGY]

    stage: dict[str, bytes] = {}
    sidecar_root = "overlay/"
    add_output(stage, sidecar_root + PREFIX + "CHECKPOINT_DRAFT.v0001.json", json_bytes(cp))
    add_output(stage, sidecar_root + "evaluation/workflows/records/" + workflow["id"] + "/v0001.json",
               json_bytes(workflow))
    for technology in technologies:
        add_output(stage, sidecar_root + "technology/records/" + technology["id"] + "/v0001.json",
                   json_bytes(technology))
    validation = validate_staged_records(repo, stage, [("checkpoint", cp), ("workflow", workflow)]
                                         + [("technology", tech) for tech in technologies], refs, config["cards"])
    add_output(stage, sidecar_root + PREFIX + "CHECKPOINT_VALIDATION.v0001.json", json_bytes(validation))

    existing = set(run_git(repo, "ls-tree", "-r", "--name-only", "HEAD").splitlines())
    for staged_path in stage:
        target = staged_path.removeprefix("overlay/")
        local = (repo / target).resolve()
        need(local.is_relative_to(repo), "Staged target escapes Astra checkout: " + target)
        need(target not in existing and not local.exists(), "Staged target already exists in Astra: " + target)

    hashes = {path: sha(data) for path, data in sorted(stage.items())}
    plan = {
        "schema": "astra.gc-sidecar-stage-plan.v1",
        "intake_id": INTAKE,
        "base_revision": BASE,
        "expected_branch_head": pins["expected_branch_head"],
        "card_ids": [cards_by_route[route]["id"] for route in CARD_ROUTES],
        "technology_ids": [item["id"] for item in technologies],
        "staged_files": hashes,
        "staged_file_count": len(stage),
        "application": "NOT_PERFORMED; sidecars remain in external staging directory",
        "scientific_validation": "NOT_PERFORMED; all claim status remains source_derived_unreviewed",
    }
    stage["PLAN.json"] = json_bytes(plan)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=output.name + ".tmp-", dir=output.parent) as temp_name:
        temp_base = Path(temp_name).resolve()
        payload = temp_base / "payload"
        payload.mkdir()
        for relative, data in stage.items():
            target = (payload / relative).resolve()
            need(target.is_relative_to(payload), "Staged path escapes output directory: " + relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
        need(not output.exists(), "Output appeared during generation; refusing replacement")
        os.rename(payload, output)
    return plan


def main() -> int:
    default_repo = Path("/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016")
    package_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=default_repo,
                        help="Read-only Astra checkout at the pinned base revision")
    parser.add_argument("--config", type=Path, default=package_root / "root/claim_config.json",
                        help="Root-authored GC claim config outside the Astra checkout")
    parser.add_argument("--output", type=Path, required=True,
                        help="New external review directory; existing paths are never overwritten")
    args = parser.parse_args()
    plan = build(args.repo, args.config, args.output)
    print(json.dumps({"status": "STAGED_FOR_REVIEW", "output": str(args.output.resolve()),
                      "files": plan["staged_file_count"], "cards": plan["card_ids"],
                      "technology": plan["technology_ids"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError,
            subprocess.CalledProcessError) as error:
        print("GC sidecar staging failed closed: " + str(error), file=sys.stderr)
        raise SystemExit(1)
