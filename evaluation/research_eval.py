#!/usr/bin/env python3
"""Offline, append-only experiment registry. It never calls a model or checks a proof."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import sys
from datetime import datetime, timezone

SCHEMA = "astra-research-evaluation/1"
LEDGERS = ("FROZEN_TASKS.jsonl", "MODEL_COMPARISONS.jsonl", "VERIFIED_OUTCOMES.jsonl")
BUDGET_KEYS = ("context_tokens", "input_tokens_total", "output_tokens_total", "model_calls",
               "tool_calls", "wall_seconds", "cpu_seconds", "gpu_seconds", "compute_usd",
               "parallel_workers")
MODELS = ("provider", "model_id", "immutable_version", "reasoning_effort",
          "context_window_tokens", "tokenizer", "tokenizer_version")


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def need(condition, message):
    if not condition:
        raise ValueError(message)


def identity(value):
    need(isinstance(value, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,95}", value),
         "IDs must be 1-96 ASCII letters/numbers/underscore/dot/hyphen")
    return value


def sha(value):
    need(isinstance(value, str) and re.fullmatch(r"[a-f0-9]{64}", value), "Expected SHA-256")
    return value


def number(value, label):
    need(type(value) in (int, float) and math.isfinite(value) and value >= 0,
         label + " must be a finite nonnegative number")


def utc(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    need(parsed.tzinfo is not None, "Timestamp must include a UTC offset")
    return parsed.astimezone(timezone.utc)


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


class Registry:
    def __init__(self, store, private_root):
        self.store = Path(store).resolve()
        self.private = Path(private_root).resolve() if private_root else None
        if self.private:
            # No private prompts, gold or condition mapping under the published repository.
            repo = self.store.parent
            need(self.private != repo and repo not in self.private.parents,
                 "Private root must be outside the knowledge repository")
            need(not Path(private_root).is_symlink(), "Private root cannot be a symlink")

    def rows(self, ledger):
        file = self.store / ledger
        if not file.exists():
            return []
        return [json.loads(line) for line in file.read_text(encoding="utf-8").splitlines() if line.strip()]

    def find(self, ledger, key, value, kind):
        rows = [r for r in self.rows(ledger) if r.get("kind") == kind and r.get(key) == value]
        need(len(rows) == 1, "Expected exactly one %s %s" % (kind, value))
        return rows[0]

    def unique(self, ledger, key, value):
        need(not any(r.get(key) == value for r in self.rows(ledger)), "ID already registered: " + value)

    def append(self, ledger, record):
        self.store.mkdir(parents=True, exist_ok=True)
        record = dict(record, schema=SCHEMA)
        # An exclusive, short-lived lock prevents interleaved writes; no stale-lock deletion.
        lock = self.store / ".registry.lock"
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        try:
            with (self.store / ledger).open("ab") as out:
                out.write(canonical(record) + b"\n")
                out.flush()
                os.fsync(out.fileno())
        finally:
            os.close(fd)
            lock.unlink()
        return record

    def seal(self, namespace, key, payload, files):
        need(self.private is not None, "--private-root is required for registration")
        self.private.mkdir(parents=True, exist_ok=True, mode=0o700)
        need(self.private.stat().st_mode & 0o077 == 0,
             "Private root must have mode 0700 (chmod 700 before registration)")
        target = self.private / namespace / identity(key)
        need(not target.exists(), "Private record already exists; do not overwrite frozen evidence")
        target.mkdir(parents=True, mode=0o700)
        entries = []
        try:
            for position, (kind, path) in enumerate(files):
                source = Path(path)
                need(source.is_file() and not source.is_symlink(), "Missing/symlinked file: " + str(source))
                data = source.read_bytes()
                h = hashlib.sha256(data).hexdigest()
                blob = target / ("%04d-" % position + h)
                with blob.open("xb") as out:
                    out.write(data)
                blob.chmod(0o600)
                entries.append({"kind": kind, "slot": position, "sha256": h, "bytes": len(data)})
            sealed = {"payload": payload, "files": entries}
            (target / "manifest.json").write_bytes(canonical(sealed) + b"\n")
            (target / "manifest.json").chmod(0o600)
            return digest(sealed), entries
        except Exception:
            # Failure occurred before any public commitment; no accepted evidence is removed.
            shutil.rmtree(target)
            raise

    def private_payload(self, namespace, key, expected):
        need(self.private is not None, "--private-root is required")
        target = self.private / namespace / identity(key)
        manifest = read_json(target / "manifest.json")
        need(digest(manifest) == expected, "Frozen private manifest changed")
        for file in manifest["files"]:
            blob = target / ("%04d-" % file["slot"] + file["sha256"])
            data = blob.read_bytes()
            need(len(data) == file["bytes"] and hashlib.sha256(data).hexdigest() == file["sha256"],
                 "Frozen private evidence changed")
        return manifest

    def register_task(self, contract):
        need(not contract.get("template_only"), "Templates are not registered scientific tasks; replace placeholders")
        task_id = identity(contract["task_id"])
        self.unique(LEDGERS[0], "task_id", task_id)
        need(contract["split"] in ("development", "unseen_candidate"), "Invalid split")
        provenance = contract["provider"]
        need(bool(provenance["identity"]), "Name the acquiring task provider")
        contamination = contract["contamination"]
        need(set(contamination) == {"repository_overlap", "prior_operator_or_worker_exposure",
             "foundation_pretraining", "screening_evidence_file"}, "Unexpected contamination fields")
        need(contamination["repository_overlap"] in ("known_overlap", "not_found_by_logged_search", "unknown"),
             "Invalid repository overlap status")
        need(contamination["prior_operator_or_worker_exposure"] in ("known_exposed", "no_known_exposure", "unknown"),
             "Invalid exposure status")
        need(contamination["foundation_pretraining"] == "unknown", "Pretraining cannot be certified unseen here")
        if contract["split"] == "unseen_candidate":
            need(provenance["independent_from_repository_authors"] is True and
                 provenance["independent_from_run_operators"] is True,
                 "Unseen candidates require independent acquisition attestations")
            need(contamination["repository_overlap"] == "not_found_by_logged_search" and
                 contamination["prior_operator_or_worker_exposure"] == "no_known_exposure",
                 "Known/unknown exposure is development-only")
        gates = read_json(contract["proof_gate_file"])
        need(gates.get("success_rule") == "all_primary", "Success rule must be all_primary")
        gate_ids = [identity(g["gate_id"]) for g in gates["gates"]]
        need(len(gate_ids) == len(set(gate_ids)) and gate_ids, "Gate IDs must be distinct and nonempty")
        primary = gates["primary_gate_ids"]
        need(primary and set(primary).issubset(gate_ids), "Name valid primary proof gates")
        for gate in gates["gates"]:
            need(gate["kind"] in ("full_mathematical_proof", "formal_kernel", "counterexample",
                                  "subtheorem", "finite_diagnostic", "scope_interface", "novelty_review"),
                 "Invalid proof gate kind")
            need(gate.get("acceptance") and gate.get("requirements"), "Specify exact gate acceptance requirements")
        files = [("task_statement", contract["task_statement_file"]),
                 ("proof_gates", contract["proof_gate_file"]),
                 ("provider_receipt", provenance["receipt_file"]),
                 ("contamination_screen", contamination["screening_evidence_file"])]
        files += [("common_input", f) for f in contract["common_input_files"]]
        files += [("private_reference", f) for f in contract["private_reference_files"]]
        safe = {"task_id": task_id, "split": contract["split"],
                "provider_identity": provenance["identity"],
                "independent_acquisition_attested": provenance["independent_from_repository_authors"] is True and
                    provenance["independent_from_run_operators"] is True,
                "contamination": {k: v for k, v in contamination.items() if k != "screening_evidence_file"},
                "gate_definition": gates}
        commitment, entries = self.seal("tasks", task_id, safe, files)
        return self.append(LEDGERS[0], {"kind": "frozen_task", "task_id": task_id,
            "frozen_at": now(), "commitment_sha256": commitment, "files": entries,
            "split": safe["split"], "contamination": safe["contamination"],
            "independent_acquisition_attested": safe["independent_acquisition_attested"],
            "unseen_status": "candidate_attestation_only_pretraining_unknown" if safe["split"] == "unseen_candidate"
                else "exposed_or_unadmitted_development",
            "gate_ids": gate_ids, "primary_gate_ids": primary,
            "statement_and_gold_public": False})

    def register_comparison(self, plan):
        need(not plan.get("template_only"), "Templates are not registered experiment plans; replace placeholders")
        comparison_id = identity(plan["comparison_id"])
        self.unique(LEDGERS[1], "comparison_id", comparison_id)
        need(plan["task_ids"] and len(plan["task_ids"]) == len(set(plan["task_ids"])), "Distinct task IDs required")
        tasks = [self.find(LEDGERS[0], "task_id", t, "frozen_task") for t in plan["task_ids"]]
        for task in tasks:
            self.private_payload("tasks", task["task_id"], task["commitment_sha256"])
        common_hash = digest({t["task_id"]: [f for f in t["files"] if f["kind"] in
            ("task_statement", "common_input", "proof_gates")] for t in tasks})
        need(plan["replicates"] >= 1 and type(plan["replicates"]) is int, "Positive integer replicates required")
        arms = plan["arms"]
        need(len({a["arm_id"] for a in arms}) == len(arms), "Duplicate arm IDs")
        conditions = {a["condition"] for a in arms}
        need({"raw_archive", "structured_repository"}.issubset(conditions) and
             conditions.issubset({"raw_archive", "structured_repository", "no_repository"}),
             "Compare raw_archive and structured_repository; optional no_repository")
        need(len(conditions) == len(arms), "One arm per condition")
        for arm in arms:
            identity(arm["arm_id"])
            need(set(arm["model"]) == set(MODELS), "Model configuration keys must exactly match protocol")
            need(all(arm["model"].get(k) is not None and arm["model"].get(k) != "" for k in MODELS),
                 "Exact model/version/reasoning/context/tokenizer configuration required")
            need(arm["model"]["immutable_version"] not in ("unknown", "latest", "REPLACE"),
                 "Pin the actual available model version; mutable/latest labels are not exact")
            sha(arm["common_information_sha256"])
            need(arm["common_information_sha256"] == common_hash,
                 "Common task-information commitment must be " + common_hash)
            sha(arm["allowed_information_manifest_sha256"])
            need(set(arm["budget"]) == set(BUDGET_KEYS), "Budget keys must exactly match protocol")
            for key in BUDGET_KEYS:
                number(arm["budget"][key], key)
            need(arm["budget"]["context_tokens"] <= arm["model"]["context_window_tokens"], "Context exceeds model")
            need(arm["compute_recipe"] and arm["tool_policy"], "Freeze hardware/compute and tool policy")
        control = arms[0]
        for arm in arms[1:]:
            for key in ("model", "budget", "common_information_sha256", "compute_recipe", "tool_policy"):
                need(arm[key] == control[key], "Unequal comparison field: " + key)
        informed = [a for a in arms if a["condition"] != "no_repository"]
        need(informed[0]["allowed_information_manifest_sha256"] == informed[1]["allowed_information_manifest_sha256"],
             "Raw and structured arms must expose the same source mathematics")
        need(plan["checker_blinding"] == "independent_checker_arm_mapping_withheld", "Freeze checker blinding")
        need(plan["charge_setup_and_failed_attempts"] is True, "All setup and failures must be charged")
        need(plan["randomization_file"] and plan["primary_metric"] == "all_primary_proof_gates_passed",
             "Freeze assignment and primary metric")
        files = [("randomization", plan["randomization_file"])]
        files += [("arm_prompt", a["prompt_file"]) for a in arms]
        files += [("information_manifest", a["information_manifest_file"]) for a in arms]
        for arm in arms:
            actual = hashlib.sha256(Path(arm["information_manifest_file"]).read_bytes()).hexdigest()
            need(actual == arm["allowed_information_manifest_sha256"], "Information manifest bytes/hash mismatch")
        private_plan = json.loads(json.dumps(plan))
        private_plan.pop("randomization_file")
        for arm in private_plan["arms"]:
            arm.pop("prompt_file")
            arm.pop("information_manifest_file")
        commitment, entries = self.seal("comparisons", comparison_id, private_plan, files)
        public_arms = [{k: v for k, v in a.items() if k not in ("condition", "prompt_file", "information_manifest_file")}
                       for a in arms]
        return self.append(LEDGERS[1], {"kind": "comparison_plan", "comparison_id": comparison_id,
            "frozen_at": now(), "commitment_sha256": commitment, "files": entries,
            "task_ids": plan["task_ids"], "replicates": plan["replicates"], "arms": public_arms,
            "primary_metric": plan["primary_metric"], "arm_mapping": "sealed_until_adjudication",
            "independence_and_isolation": "protocol_obligations_not_software_certification",
            "discovery_eligibility": all(t["split"] == "unseen_candidate" for t in tasks)})

    def record_run(self, record):
        need(not record.get("template_only"), "Templates are not observed model runs")
        need(set(record) == {"run_id", "comparison_id", "task_id", "arm_id", "replicate",
             "started_at", "ended_at", "status", "actual_model", "usage", "transcript_file",
             "resource_receipt_file", "output_files"}, "Unexpected run fields; keep proof/transcript content private")
        run_id = identity(record["run_id"])
        self.unique(LEDGERS[1], "run_id", run_id)
        plan = self.find(LEDGERS[1], "comparison_id", record["comparison_id"], "comparison_plan")
        self.private_payload("comparisons", plan["comparison_id"], plan["commitment_sha256"])
        need(record["task_id"] in plan["task_ids"], "Task not assigned to comparison")
        arm = next((a for a in plan["arms"] if a["arm_id"] == record["arm_id"]), None)
        need(arm is not None, "Unregistered arm")
        need(type(record["replicate"]) is int and 1 <= record["replicate"] <= plan["replicates"], "Invalid replicate")
        for prior in self.rows(LEDGERS[1]):
            if prior.get("kind") == "run_record":
                need(any(prior.get(k) != record.get(k) for k in ("comparison_id", "task_id", "arm_id", "replicate")),
                     "Replicate already recorded; failures cannot be silently retried")
        need(utc(record["started_at"]) >= utc(plan["frozen_at"]) and
             utc(record["ended_at"]) >= utc(record["started_at"]), "Run must begin after the frozen plan")
        need(utc(record["ended_at"]) <= utc(now()), "Cannot record a run that has not yet ended")
        need(record["status"] in ("completed", "failed", "timeout", "aborted", "budget_exceeded"), "Invalid run status")
        need(record["actual_model"] == arm["model"], "Actual model differs from frozen arm")
        usage = record["usage"]
        need(set(usage) == set(BUDGET_KEYS), "Record all resource charges; unknown must be null")
        over, unknown = [], []
        for key in BUDGET_KEYS:
            if usage[key] is None:
                unknown.append(key)
            else:
                number(usage[key], key)
                if usage[key] > arm["budget"][key]:
                    over.append(key)
        measured = (utc(record["ended_at"]) - utc(record["started_at"])).total_seconds()
        if usage["wall_seconds"] is not None:
            need(usage["wall_seconds"] >= measured, "Wall charge cannot be shorter than recorded run interval")
        files = [("transcript", record["transcript_file"]), ("resource_receipt", record["resource_receipt_file"])]
        files += [("output", f) for f in record["output_files"]]
        safe = {k: v for k, v in record.items() if k not in ("transcript_file", "resource_receipt_file", "output_files")}
        commitment, entries = self.seal("runs", run_id, safe, files)
        return self.append(LEDGERS[1], dict(safe, kind="run_record", recorded_at=now(),
            commitment_sha256=commitment, files=entries, budget_excess=over, unmeasured_charges=unknown,
            budget_status="exceeded" if over else "unknown" if unknown else "within_frozen_limits",
            eligible_for_success=not over and not unknown and record["status"] == "completed"))

    def record_outcome(self, receipt):
        need(not receipt.get("template_only"), "Templates are not independent checker results")
        need(set(receipt) == {"outcome_id", "run_id", "checker_identity", "independence_attested",
             "blinded_to_arm_mapping", "checker_relationship", "checked_output_sha256",
             "gate_results", "evidence_files", "independence_evidence_file"}, "Unexpected checker fields")
        outcome_id = identity(receipt["outcome_id"])
        self.unique(LEDGERS[2], "outcome_id", outcome_id)
        run = self.find(LEDGERS[1], "run_id", receipt["run_id"], "run_record")
        run_manifest = self.private_payload("runs", run["run_id"], run["commitment_sha256"])
        task = self.find(LEDGERS[0], "task_id", run["task_id"], "frozen_task")
        task_manifest = self.private_payload("tasks", task["task_id"], task["commitment_sha256"])
        need(not any(r.get("run_id") == run["run_id"] and r.get("kind") == "checker_outcome"
                     for r in self.rows(LEDGERS[2])), "Outcome already recorded; preserve reassessment separately")
        need(receipt["checker_identity"] and receipt["independence_attested"] is True and
             receipt["blinded_to_arm_mapping"] is True, "Independent, blinded checker attestation required")
        need(receipt["checker_relationship"] in ("external_expert", "independent_formal_checker_operator"),
             "Internal/audit/producer checks cannot enter verified outcomes")
        hashes = {f["sha256"] for f in run_manifest["files"] if f["kind"] == "output"}
        has_exact_submission = bool(hashes) and bool(receipt["checked_output_sha256"]) and \
            set(receipt["checked_output_sha256"]).issubset(hashes)
        empty_failed_submission = not hashes and receipt["checked_output_sha256"] == [] and run["status"] != "completed"
        need(has_exact_submission or empty_failed_submission,
             "Checker must reference exact submitted output hashes")
        definitions = {g["gate_id"]: g for g in task_manifest["payload"]["gate_definition"]["gates"]}
        results = receipt["gate_results"]
        need(len(results) == len(definitions) and {g["gate_id"] for g in results} == set(definitions),
             "Every frozen gate needs one result")
        for gate in results:
            need(gate["status"] in ("passed", "failed", "unknown", "not_assessed"), "Invalid gate status")
            need(gate.get("reason"), "Record acceptance/failure reason, including unknown")
        need(receipt["evidence_files"] and receipt["independence_evidence_file"], "Checker evidence files required")
        passed = {g["gate_id"] for g in results if g["status"] == "passed"}
        success = run["eligible_for_success"] and set(task["primary_gate_ids"]).issubset(passed)
        scientific_primary = any(definitions[g]["kind"] in ("full_mathematical_proof", "formal_kernel",
                                "counterexample", "subtheorem") for g in task["primary_gate_ids"])
        safe = {k: v for k, v in receipt.items() if k not in ("evidence_files", "independence_evidence_file")}
        files = [("checker_independence_receipt", receipt["independence_evidence_file"])]
        files += [("checker_evidence", f) for f in receipt["evidence_files"]]
        commitment, entries = self.seal("outcomes", outcome_id, safe, files)
        return self.append(LEDGERS[2], dict(safe, kind="checker_outcome", recorded_at=now(),
            comparison_id=run["comparison_id"], task_id=run["task_id"], arm_id=run["arm_id"],
            replicate=run["replicate"], commitment_sha256=commitment, files=entries,
            primary_success=success, scientific_proof_gate_success=success and scientific_primary,
            independence_status="receipt_attested_not_certified_by_registry",
            historical_novelty="not_established_by_this_record"))

    def report(self, comparison_id):
        plan = self.find(LEDGERS[1], "comparison_id", comparison_id, "comparison_plan")
        runs = [r for r in self.rows(LEDGERS[1]) if r.get("kind") == "run_record" and r["comparison_id"] == comparison_id]
        outcomes = {r["run_id"]: r for r in self.rows(LEDGERS[2]) if r.get("kind") == "checker_outcome"}
        expected = len(plan["task_ids"]) * plan["replicates"]
        arms = []
        for arm in plan["arms"]:
            assigned = [r for r in runs if r["arm_id"] == arm["arm_id"]]
            scored = [outcomes[r["run_id"]] for r in assigned if r["run_id"] in outcomes]
            charges = {}
            for key in BUDGET_KEYS:
                known = [r["usage"][key] for r in assigned if r["usage"][key] is not None]
                charges[key] = {"known_record_count": len(known), "unknown_record_count": len(assigned) - len(known),
                    "aggregation": "peak" if key in ("context_tokens", "parallel_workers") else "sum",
                    "measured_value": (max(known) if key in ("context_tokens", "parallel_workers") else sum(known))
                        if known else None}
            arms.append({"arm_id": arm["arm_id"], "assigned": expected, "recorded": len(assigned),
                "missing_runs": expected - len(assigned), "unadjudicated": len(assigned) - len(scored),
                "primary_successes": sum(o["primary_success"] for o in scored),
                "scientific_proof_gate_successes": sum(o["scientific_proof_gate_success"] for o in scored),
                "failed_or_ineligible_runs": sum(not r["eligible_for_success"] for r in assigned),
                "budget_exceeded": sum(bool(r["budget_excess"]) for r in assigned),
                "unknown_cost_runs": sum(bool(r["unmeasured_charges"]) for r in assigned), "charges": charges})
        complete = all(a["missing_runs"] == 0 and a["unadjudicated"] == 0 for a in arms)
        paired = []
        for task in plan["task_ids"]:
            for replicate in range(1, plan["replicates"] + 1):
                row = {"task_id": task, "replicate": replicate, "arms": {}}
                for arm in plan["arms"]:
                    matching = [r for r in runs if r["task_id"] == task and r["replicate"] == replicate
                                and r["arm_id"] == arm["arm_id"]]
                    run = matching[0] if matching else None
                    outcome = outcomes.get(run["run_id"]) if run else None
                    row["arms"][arm["arm_id"]] = {"run_status": run["status"] if run else "missing",
                        "primary_success": outcome["primary_success"] if outcome else None}
                paired.append(row)
        mapping = "sealed_until_all_assigned_runs_adjudicated"
        if complete and self.private:
            frozen = self.private_payload("comparisons", comparison_id, plan["commitment_sha256"])
            mapping = {a["arm_id"]: a["condition"] for a in frozen["payload"]["arms"]}
        return {"comparison_id": comparison_id, "discovery_task_admission": plan["discovery_eligibility"],
                "arms": arms, "paired_task_results": paired, "complete": complete, "arm_mapping": mapping,
                "interpretation": "Descriptive receipts only; no automatic Astra capability, novelty or discovery claim."}

    def validate(self):
        counts = {}
        for ledger in LEDGERS:
            rows = self.rows(ledger)
            counts[ledger] = len(rows)
            allowed = {LEDGERS[0]: {"frozen_task"},
                LEDGERS[1]: {"comparison_plan", "run_record", "historical_navigation_comparison"},
                LEDGERS[2]: {"checker_outcome", "historical_navigation_outcome"}}[ledger]
            seen = set()
            for row in rows:
                need(row.get("schema") == SCHEMA, "Unexpected schema in " + ledger)
                need(row.get("kind") in allowed, "Unexpected record kind in " + ledger)
                key = {"frozen_task": "task_id", "comparison_plan": "comparison_id", "run_record": "run_id",
                    "checker_outcome": "outcome_id", "historical_navigation_comparison": "comparison_id",
                    "historical_navigation_outcome": "outcome_id"}[row["kind"]]
                record_id = (row["kind"], row[key])
                need(record_id not in seen, "Duplicate ledger ID")
                seen.add(record_id)
                if row["kind"] == "comparison_plan":
                    for task_id in row["task_ids"]:
                        self.find(LEDGERS[0], "task_id", task_id, "frozen_task")
                elif row["kind"] == "run_record":
                    self.find(LEDGERS[1], "comparison_id", row["comparison_id"], "comparison_plan")
                elif row["kind"] == "checker_outcome":
                    self.find(LEDGERS[1], "run_id", row["run_id"], "run_record")
                if row["kind"].startswith("historical_navigation_"):
                    need(row.get("scientific_discovery_evidence") is False and
                         row.get("independent_scientific_verification") is False and row.get("model_calls") == 0,
                         "Historical navigation cannot be promoted to scientific evidence")
                    for evidence in row["evidence"]:
                        file = (self.store.parent / evidence["path"]).resolve()
                        need(self.store.parent in file.parents, "Historical evidence path escapes repository")
                        data = file.read_bytes()
                        need(hashlib.sha256(data).hexdigest() == evidence["sha256"] and
                             len(data) == evidence["bytes"], "Historical evidence bytes changed")
                if "commitment_sha256" in row:
                    sha(row["commitment_sha256"])
                    if self.private:
                        namespace, key = {"frozen_task": ("tasks", "task_id"),
                            "comparison_plan": ("comparisons", "comparison_id"),
                            "run_record": ("runs", "run_id"),
                            "checker_outcome": ("outcomes", "outcome_id")}[row["kind"]]
                        self.private_payload(namespace, row[key], row["commitment_sha256"])
        return {"valid_jsonl": True, "rows": counts,
                "private_hashes_checked": self.private is not None,
                "proofs_checked": False, "models_called": 0}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--private-root", help="Evaluator-only 0700 directory outside the repository")
    sub = parser.add_subparsers(dest="command", required=True)
    for action in ("register-task", "register-comparison", "record-run", "record-outcome"):
        item = sub.add_parser(action)
        item.add_argument("json_file")
    sub.add_parser("validate")
    item = sub.add_parser("report")
    item.add_argument("comparison_id")
    args = parser.parse_args(argv)
    registry = Registry(args.store, args.private_root)
    try:
        if args.command == "validate":
            result = registry.validate()
        elif args.command == "report":
            result = registry.report(args.comparison_id)
        else:
            method = getattr(registry, args.command.replace("-", "_"))
            result = method(read_json(args.json_file))
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as error:
        print("Registry rejected input: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
