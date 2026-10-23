#!/usr/bin/env python3
"""Replay lead from its own public transcript before opening control tables."""
import hashlib
import json
from pathlib import Path
import time

from benchmark import FullGridMethod, LeadMethod, OSStarMethod, config_dict

HERE = Path(__file__).resolve().parent


def compare(name, public, replayed):
    checks = {
        "task_counts_match": replayed["task_counts"] == public["task_counts"],
        "outputs_match": replayed["outputs"] == public["outputs"],
        "events_match_exactly": replayed["events"] == public["events"],
        "bit_segments_match_exactly": replayed["bit_segments"] == public["bit_segments"],
        "bit_tape_consumed_exactly": replayed["bit_tape"] == public["bit_tape"],
    }
    if name == "fullgrid":
        checks["paid_control_table_matches"] = (
            replayed["control_paid_grid_table"] == public["control_paid_grid_table"])
    if not all(checks.values()):
        raise AssertionError(f"public replay mismatch: {name}: {checks}")
    return checks


def leq_ratio(left, right):
    """Exact comparison of public [numerator, denominator] pairs."""
    an, ad = map(int, left)
    bn, bd = map(int, right)
    return an * bd <= bn * ad


def main():
    # First phase: read only the lead's paid transcript. In particular, the
    # exact full-grid control table has not yet been opened or passed anywhere.
    lead_path = HERE / "LEAD_PUBLIC_TRANSCRIPT.json"
    lead_public = json.loads(lead_path.read_text())
    if lead_public.get("config") != config_dict():
        raise AssertionError("lead public config differs from the visible benchmark")
    current_source_hash = hashlib.sha256((HERE / "benchmark.py").read_bytes()).hexdigest()
    if lead_public.get("source_sha256") != current_source_hash:
        raise AssertionError("lead transcript code hash does not match visible benchmark.py")
    lead_obj = LeadMethod("lead_demand_refinement", 0, lead_public["bit_tape"])
    lead = lead_obj.run_lead()
    checks = {"lead": compare("lead", lead_public, lead)}
    if lead_obj.bits.pos != len(lead_public["bit_tape"]):
        raise AssertionError("lead public tape was not consumed exactly")
    counts = lead["task_counts"]

    # Second phase: controls get the realized lead count sequence. Each runs
    # only from its own transcript and code; the OS* control never receives the
    # full-grid table. The full-grid table is opened only for its own replay.
    os_path = HERE / "OSSTAR_PUBLIC_TRANSCRIPT.json"
    os_public = json.loads(os_path.read_text())
    if os_public.get("config") != config_dict() or os_public.get("source_sha256") != current_source_hash:
        raise AssertionError("OS* public config/source hash mismatch")
    os_obj = OSStarMethod("retained_OS_star", 0, os_public["bit_tape"])
    os_result = os_obj.run(counts)
    checks["osstar"] = compare("osstar", os_public, os_result)
    if os_obj.bits.pos != len(os_public["bit_tape"]):
        raise AssertionError("OS* public tape was not consumed exactly")

    full_path = HERE / "FULLGRID_PUBLIC_TRANSCRIPT.json"
    full_public = json.loads(full_path.read_text())
    if full_public.get("config") != config_dict() or full_public.get("source_sha256") != current_source_hash:
        raise AssertionError("full-grid public config/source hash mismatch")
    full_obj = FullGridMethod(0, full_public["bit_tape"])
    full_result = full_obj.run(counts)
    checks["fullgrid"] = compare("fullgrid", full_public, full_result)
    if full_obj.bits.pos != len(full_public["bit_tape"]):
        raise AssertionError("full-grid public tape was not consumed exactly")

    # The full-grid control's already-paid exact weights provide a separate
    # evaluator check of every task-start interval, after the lead-only replay.
    audit_start = time.perf_counter()
    certificate_checks = {}
    audit_integer_comparisons = 0
    for name, result in (("lead", lead), ("osstar", os_result)):
        ok = []
        key = "posterior_normalizer_interval_at_each_task_start"
        for cert in result[key]:
            true_evidence = full_obj.weight_cache[cert["s"]][3]
            true_q = [str(true_evidence.numerator), str(true_evidence.denominator)]
            lower_ok = leq_ratio(cert["z_lower"], true_q)
            upper_ok = leq_ratio(true_q, cert["z_upper"])
            audit_integer_comparisons += 2
            ok.append({"task": cert["task"], "s": cert["s"],
                       "lower_le_exact": lower_ok, "exact_le_upper": upper_ok})
        certificate_checks[name] = {"all_enclosed": all(x["lower_le_exact"] and x["exact_le_upper"] for x in ok),
                                    "tasks": ok}
    full_certs = full_result["posterior_normalizer_exact_at_each_task_start"]
    certificate_checks["fullgrid"] = {
        "all_equal_exact_evidence": all(c["z_lower"] == c["z_upper"] and
                                         c["z_lower"] == [str(full_obj.weight_cache[c["s"]][3].numerator),
                                                           str(full_obj.weight_cache[c["s"]][3].denominator)]
                                         for c in full_certs),
        "task_count": len(full_certs),
    }
    if not certificate_checks["lead"]["all_enclosed"] or not certificate_checks["osstar"]["all_enclosed"] or not certificate_checks["fullgrid"]["all_equal_exact_evidence"]:
        raise AssertionError(f"task-start evidence certificate failure: {certificate_checks}")
    audit_seconds = time.perf_counter() - audit_start

    files = {"lead": lead_path, "osstar": os_path, "fullgrid": full_path}
    result_map = {"lead": lead, "osstar": os_result, "fullgrid": full_result}
    output = {
        "status": "PASS",
        "scope": "exact deterministic recomputation from visible code and public consumed bit tapes; lead is replayed before the full-grid control transcript is opened",
        "fairness_boundary": "OS* and full-grid get the same lead-generated task counts; the OS* execution receives no full-grid table; the full-grid table is opened only to verify the paid full-grid control",
        "prng_boundary": "replay proves conditional transcript consistency, not iid/fairness of Python PRNG bits",
        "task_counts_lead_generated": counts,
        "checks": checks,
        "task_start_evidence_certificate_validation": {
            "status": "PASS", "source": "full-grid control's paid exact weight vectors, accessed only after lead replay",
            "integer_cross_product_comparisons": audit_integer_comparisons,
            "wall_seconds": audit_seconds,
            "results": certificate_checks,
        },
        "transcript_sha256": {name: hashlib.sha256(path.read_bytes()).hexdigest()
                              for name, path in files.items()},
        "source_sha256": hashlib.sha256((HERE / "benchmark.py").read_bytes()).hexdigest(),
        "method_costs": {name: {"counters": res["counters"],
                                "rational_ledger": res["rational_ledger"],
                                "wall_seconds_including_exact_logic": res["wall_seconds_including_exact_logic"]}
                         for name, res in result_map.items()},
    }
    (HERE / "PUBLIC_REPLAY_VERIFICATION.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "checks": checks,
                      "task_counts": counts}, indent=2))


if __name__ == "__main__":
    main()
