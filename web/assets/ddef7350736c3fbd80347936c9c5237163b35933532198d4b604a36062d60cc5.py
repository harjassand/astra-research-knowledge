#!/usr/bin/env python3
"""Integrity/status replay only: no theorem or numerical quantum test."""
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[3]
FROZEN = {
 "INDEPENDENT_BASELINE.txt":"f9047660d8bacc5e555941ce73977e88fa826e84993d29e7208ccadbb6df2ca7",
 "NORMAL_CMI_DEPENDENCY_CLOSURE.txt":"42af35d5d9dc6f0a2736abdfcf0215c93819dbdc0c21371b555ea7f144c8074e",
 "STRONGER_GATE_AND_FALSIFIERS.txt":"e241d72893d86ff92b87feb7bb37d17ac619cf5c994b69f1d90d2f7b7386ec24"
}
REVIEWS = {
 "work/agents/spin1_anisotropic_sol/cycle06_double_markov_review/NORMAL_CMI_CLOSURE.txt":"6cc5fc875f6e6ee73a3f6a272bf6a84eed4b7efd3989e3e85f5987b4f947165d",
 "work/agents/spin1_anisotropic_sol/cycle06_double_markov_review/EXPOSED_RECORD_TRANSFER_AUDIT.txt":"9a91a53e78fda3a7727cc1edb495cfc372b570dbb605e7261543823b7eb33529"
}
def digest(path):
 return hashlib.sha256(path.read_bytes()).hexdigest()
for filename, expected in FROZEN.items():
 assert digest(ROOT/filename)==expected, "Frozen bytes changed: "+filename
for filename, expected in REVIEWS.items():
 assert digest(WORKSPACE/filename)==expected, "Review bytes changed: "+filename
registry=json.loads((ROOT/"PRIMARY_SOURCE_REGISTRY.json").read_text())
assert len(registry["sources"])==5
for source in registry["sources"]:
 assert source["cache_status"]=="CACHED"
 path=ROOT/source["cache_path"]
 assert path.stat().st_size==source["bytes"]
 assert digest(path)==source["sha256"]
opportunities=json.loads((ROOT/"opportunities.json").read_text())
assert opportunities["task_status"]=="COMPLETE_NO_PENDING"
assert opportunities["pending_tasks"]==[]
assert len(opportunities["opportunities"])==1
assert opportunities["opportunities"][0]["ambitious_endpoint"]["status"]=="UNKNOWN"
report=(ROOT/"REPORT.txt").read_text()
assert "TASK STATUS: COMPLETE_NO_PENDING" in report
assert "I-free" not in report or "UNKNOWN" in report
inventory=[]
for path in sorted(ROOT.rglob("*")):
 if path.is_file() and path.name!="MANIFEST.json":
  rel=str(path.relative_to(ROOT))
  if rel in FROZEN:
   category="IMMUTABLE_ORIGIN_FREEZE"
  elif rel.startswith("primary/"):
   category="PRIMARY_HTML_CACHE"
  elif rel=="POST_EXPOSURE_STATUS_CLOSURE.txt":
   category="AUTHORIZED_EXPOSURE_CLOSURE"
  elif rel.endswith(".py"):
   category="INTEGRITY_OR_CACHE_SCRIPT"
  elif rel=="PRIMARY_SOURCE_REGISTRY.json":
   category="SOURCE_VERSION_REGISTRY"
  else:
   category="FINAL_REPORT_OR_CLAIM_LEDGER"
  inventory.append(dict(path=rel,category=category,
                        bytes=path.stat().st_size,sha256=digest(path)))
manifest={
 "schema":1,"date":"2026-10-09","task_status":"COMPLETE_NO_PENDING",
 "scope":"Artifact/status/source integrity only; not theorem validation or formal proof.",
 "frozen_origin_hashes":FROZEN,"authorized_review_hashes":REVIEWS,
 "primary_sources":5,"pending_tasks":[],"files":inventory
}
(ROOT/"MANIFEST.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps({"integrity":"PASS","origin_freezes":len(FROZEN),
                  "authorized_reviews":len(REVIEWS),"primary_sources":5,
                  "files":len(inventory),"pending_tasks":0,
                  "manifest_sha256":digest(ROOT/"MANIFEST.json")}))

