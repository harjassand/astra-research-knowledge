#!/usr/bin/env python3
"""Integrity and status replay only; it does not validate mathematical truth."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[3]
FROZEN={
 "INDEPENDENT_BASELINE.txt":"5c0130da8b3c4b5a20ed9f6bc1e1d7474f9c7a6eac526248a53de0f0e073c347",
 "SPIN_COVARIANT_CONSTRUCTION.txt":"2ff90c968165bd57194431f56f54e4b2eaf863d5152ea920e2281fda140c675f",
 "RARE_SECTOR_TENSOR_GATE.txt":"b7dd4448ceea3bc166f9f931be6bf0059adb2f2e0bd71bf4e731f84a27e942fe",
 "ONE_CLASSICAL_RECORD_ADDENDUM.txt":"d173fe8f312e9512a692ac4b75e0873d6ffab1b22d3dd162b4b38ae3d67f8b17",
 "REPORT.txt":"fb63dd36db35cfcb573bc3ebc8bf7d2fdff736af266d1ac9156c61285f1f3fee",
 "opportunities.json":"25bc4381666def2e72f81bf6d0f33fba242f24eca52de1e2d29f2368c9c902e2"
}
OLD={
 "INDEPENDENT_BASELINE.txt":"f9047660d8bacc5e555941ce73977e88fa826e84993d29e7208ccadbb6df2ca7",
 "NORMAL_CMI_DEPENDENCY_CLOSURE.txt":"42af35d5d9dc6f0a2736abdfcf0215c93819dbdc0c21371b555ea7f144c8074e",
 "STRONGER_GATE_AND_FALSIFIERS.txt":"e241d72893d86ff92b87feb7bb37d17ac619cf5c994b69f1d90d2f7b7386ec24"
}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for path,sha in FROZEN.items():assert digest(ROOT/path)==sha,path
for path,sha in OLD.items():assert digest(ROOT.parent/"cycle06_record_transfer"/path)==sha,path
registry=json.loads((ROOT/"PRIMARY_SOURCE_REGISTRY.json").read_text())
assert len(registry["sources"])==4
for s in registry["sources"]:
 p=ROOT/s["path"];assert p.stat().st_size==s["bytes"];assert digest(p)==s["sha256"]
diagnostics=["FINITE_DIAGNOSTICS.json","RARE_SECTOR_DIAGNOSTICS.json","ONE_RECORD_DIAGNOSTICS.json"]
for path in diagnostics:assert json.loads((ROOT/path).read_text())["status"]=="PASS"
opp=json.loads((ROOT/"opportunities.json").read_text())
assert opp["origin_task_status"]=="COMPLETE" and opp["pending_origin_tasks"]==[]
assert opp["general_target"]["status"]=="UNKNOWN"
receipts_path=ROOT/"POST_EXPOSURE_REVIEW_RECEIPTS.json"
receipts=[]
if receipts_path.exists():
 receipts=json.loads(receipts_path.read_text())["reviews"]
 for r in receipts:assert digest(WORKSPACE/r["path"])==r["sha256"]
inventory=[]
for p in sorted(ROOT.rglob("*")):
 if not p.is_file() or p.name=="MANIFEST.json":continue
 rel=str(p.relative_to(ROOT))
 if rel in FROZEN:category="IMMUTABLE_ORIGIN_PROOF_OR_REPORT"
 elif rel.startswith("primary/"):category="PRIMARY_VERSION_CACHE"
 elif rel.endswith(".py"):category="CACHE_OR_FINITE_DIAGNOSTIC_OR_INTEGRITY_SCRIPT"
 elif "DIAGNOSTICS" in rel:category="FINITE_DIAGNOSTIC_ONLY"
 elif rel=="PRIMARY_SOURCE_REGISTRY.json":category="SOURCE_SCOPE_REGISTRY"
 elif rel.startswith("POST_EXPOSURE"):category="AUTHORIZED_SEPARATE_REVIEW_CLOSURE"
 else:category="UNCLASSIFIED"
 assert category!="UNCLASSIFIED",rel
 inventory.append(dict(path=rel,category=category,bytes=p.stat().st_size,sha256=digest(p)))
manifest={"schema":1,"date":"2026-10-09","origin_task_status":"COMPLETE","pending_origin_tasks":[],
 "general_gate":"UNKNOWN","scope":"Integrity/status/source replay; not theorem validation or formal proof.",
 "frozen_origin_hashes":FROZEN,"preserved_cycle06_hashes":OLD,
 "primary_sources":4,"authorized_review_receipts":receipts,"files":inventory}
(ROOT/"MANIFEST.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps({"integrity":"PASS","origin_freezes":len(FROZEN),
 "preserved_old_freezes":len(OLD),"primary_sources":4,
 "diagnostic_reports":len(diagnostics),"files":len(inventory),
 "authorized_exposed_reviews":len(receipts),
 "manifest_sha256":digest(ROOT/"MANIFEST.json")}))

