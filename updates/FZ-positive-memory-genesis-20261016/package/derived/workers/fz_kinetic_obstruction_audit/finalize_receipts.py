"""Read-only source integrity and bounded saved-result metadata audit.

Writes only beside this file. It never imports or runs the simulation programs.
"""
from pathlib import Path
from fractions import Fraction
import datetime
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parent
SOURCE = Path("/Users/harjas/Downloads/astra_kinetic_investigation")
manifest = json.loads((SOURCE / "MANIFEST.json").read_text())
entries = [dict(name=p.name, bytes=p.stat().st_size,
                sha256=hashlib.sha256(p.read_bytes()).hexdigest())
           for p in sorted(SOURCE.iterdir()) if p.is_file()]
actual = {e["name"]: e for e in entries}
mismatches = [dict(expected=e, actual=actual.get(e["name"]))
              for e in manifest["files"] if actual.get(e["name"]) != e]
before = json.loads((ROOT / "source_snapshot_before.json").read_text())
source_unchanged = entries == before["entries"]
after = dict(source=str(SOURCE),
             timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
             entries=entries, manifest_files=len(manifest["files"]),
             manifest_mismatches=mismatches, unchanged_since_before=source_unchanged)
(ROOT / "source_snapshot_after.json").write_text(json.dumps(after, indent=2) + "\n")

repetitions = [json.loads((SOURCE / f"split_rep_{j:02}.json").read_text())
               for j in range(12)]
summary = json.loads((SOURCE / "experiment_summary.json").read_text())
estimates = [r["estimate"] for r in repetitions]
seeds = [r["seed"] for r in repetitions]
products = []
for j, result in enumerate(repetitions):
    product = Fraction(1)
    for stage in result["stages"]:
        product *= Fraction(stage["successes"], stage["particles"])
    products.append(dict(repetition=j, exact_fraction=str(product),
                         reported_estimate=result["estimate"],
                         rounded_exact_product=float(product),
                         absolute_rounding_difference=result["estimate"] - float(product)))
mean = math.fsum(estimates) / len(estimates)
sd = math.sqrt(math.fsum((x - mean) ** 2 for x in estimates) / (len(estimates) - 1))
se = sd / math.sqrt(len(estimates))
saved_algebra = json.loads((SOURCE / "algebra_checks.json").read_text())
replayed_algebra = json.loads((ROOT / "replay/algebra_checks.json").read_text())
exact_keys = ["exact_checks_passed", "checks", "triangle_rational_witness",
              "triangle_exact_growth_margin", "kappa", "relative_h_error",
              "rarity_p_example"]
exact_match = {key: saved_algebra[key] == replayed_algebra[key] for key in exact_keys}
numeric_keys = ["triangle_float_spectral_radius", "CT_float_spectral_abscissa",
                "two_state_clock_marginalized_normalized_second_moment"]
numeric_values = {key: dict(source=saved_algebra[key], replay=replayed_algebra[key])
                  for key in numeric_keys}
checks = dict(
    source_manifest_all_30_entries_match=len(manifest["files"]) == 30 and not mismatches,
    source_packet_unchanged=source_unchanged,
    copied_script_byte_identical=hashlib.sha256((ROOT / "replay/verify_algebra.py").read_bytes()).hexdigest()
        == actual["verify_algebra.py"]["sha256"],
    source_exact_output_fields_match=all(exact_match.values()),
    master_seeds_match_supplied_schedule=seeds == [8017 + 1009 * j for j in range(12)],
    master_seeds_distinct=len(set(seeds)) == 12,
    main_contract_consistent=all(r["shape"] == [2, 4] and r["particles"] == 256
        and r["deadline"] == 1.0 and r["cap"] == -1
        and r["levels"] == list(range(47, 14, -2)) and len(r["stages"]) == 17
        for r in repetitions),
    stage_event_sums_consistent=all(r["total_events"] == sum(st["events"] for st in r["stages"])
        for r in repetitions),
    total_events_matches_summary=sum(r["total_events"] for r in repetitions) == summary["total_events"],
    observed_max_matches_summary=max(st["max_count"] for r in repetitions for st in r["stages"])
        == summary["max_observed_count"],
    reported_estimate_array_matches_summary=estimates == summary["estimates"],
    empirical_mean_matches_summary=math.isclose(mean, summary["estimate_mean"], rel_tol=1e-14),
    empirical_se_matches_summary=math.isclose(se, summary["empirical_se"], rel_tol=1e-14),
    wall_sum_matches_summary=math.isclose(math.fsum(r["wall_seconds"] for r in repetitions),
        summary["total_wall_seconds"], rel_tol=1e-14),
    product_rounding_difference_small=all(abs(x["absolute_rounding_difference"])
        <= 1e-14 * x["reported_estimate"] for x in products))
result = dict(scope="Saved metadata and exact-source-output consistency only; no stochastic or FSP execution",
              checks=checks, master_seeds=seeds,
              derived_stage_seeds_saved=False,
              seed_preregistration_independently_timestamped=False,
              ideal_PRNG_independence_proved=False,
              exact_output_field_matches=exact_match,
              floating_output_comparison=numeric_values,
              product_checks=products,
              recomputed_descriptive_statistics=dict(mean=mean, sd=sd, se=se,
                  relative_se=se / mean, total_events=sum(r["total_events"] for r in repetitions),
                  wall_sum_seconds=math.fsum(r["wall_seconds"] for r in repetitions)))
(ROOT / "metadata_audit.json").write_text(json.dumps(result, indent=2) + "\n")
assert all(checks.values()), checks
print(json.dumps(dict(all_metadata_checks_passed=True, checks=len(checks),
                     source_unchanged=source_unchanged,
                     manifest_mismatches=len(mismatches), original_exact_checks=replayed_algebra["exact_checks_passed"])))
