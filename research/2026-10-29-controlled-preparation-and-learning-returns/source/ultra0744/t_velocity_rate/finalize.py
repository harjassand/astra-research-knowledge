"""Freeze a scoped producer receipt; hashes are transport, not proof/audit."""
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parent
acquisition=json.loads((root/"outputs/ACQUISITION.json").read_text())
algebra=json.loads((root/"outputs/GENERATOR_CERTIFICATE.json").read_text())
assert algebra["status"]=="PASS_exact_algebra_only"
for batch in acquisition["recursive"]:
    counts=batch["counts"]
    attempts=counts["final_attempts"] if batch["mode"]=="normalized_currency" else batch["size"]
    assert counts["source_draws"]==counts["events"]+attempts
    assert counts["exponentials"]==2*counts["events"]+attempts
    assert counts["angles"]==counts["collision_accepts"]
    if batch["mode"]=="normalized_currency":
        assert batch["output_weight"]["min"]==batch["output_weight"]["max"]==1
        assert counts["final_rejects"]==attempts-batch["size"]
manifest=[]
for path in sorted(root.rglob("*")):
    if not path.is_file() or path.name=="FINAL_RECEIPT.json":
        continue
    data=path.read_bytes()
    manifest.append({"path":str(path.relative_to(root)),"bytes":len(data),
                     "sha256":hashlib.sha256(data).hexdigest()})
receipt={
    "status":"CONSTRUCTED_producer_theorem_and_executed_floating_controls",
    "date":"2026-10-29",
    "operation":"normalized iid homogeneous hard-sphere velocity via conserved-currency lineage",
    "target_rate":"actual |v-w|, normalized uniform outgoing relative direction",
    "input":"independent bounded initial source, warranted support and exact known energy; a>0",
    "proved_by_producer":["normalized positive generator","Fournier-adapted stopped-counter nonexplosion",
                           "physical-law identification and final rejection","explicit finite-time expected work",
                           "quartic moment cost bound","bounded-test iid Hoeffding consequence"],
    "independent_internal_review":"not yet claimed for new hard-sphere theorem",
    "exact_consumer":"generic algebra and literal rational controls only, not a termination test",
    "finite_sample_diagnostics":"all declared times/seeds/comparators retained; not exact-law proof",
    "fixed_recursive_sample_count":sum(b["size"] for b in acquisition["recursive"]),
    "finite_population_particles":80000,
    "acquisition_seconds_after_imports":acquisition["elapsed_seconds_total"],
    "same_input_ordinary_methods":["Fournier exact weighted recursion","continuous-time finite-N Kac/DSMC"],
    "ordinary_result":"finite-N method much faster; population bias not certified",
    "NOT_ACHIEVED":["historical novelty","general practical incumbent advantage","uniform-in-time work",
                    "exact finite-bit continuous output","physical gas/model qualification",
                    "spatial/non-cutoff kernel extension"],
    "no_new_workers_paid_physical_public_or_outreach_actions":True,
    "files_excluding_receipt":manifest,
    "bytes_excluding_receipt":sum(f["bytes"] for f in manifest),
}
(root/"FINAL_RECEIPT.json").write_text(json.dumps(receipt,indent=2,allow_nan=False)+"\n")
print(json.dumps({"status":receipt["status"],"files":len(manifest),
                  "bytes":receipt["bytes_excluding_receipt"],
                  "acquisition_seconds":receipt["acquisition_seconds_after_imports"]},indent=2))
