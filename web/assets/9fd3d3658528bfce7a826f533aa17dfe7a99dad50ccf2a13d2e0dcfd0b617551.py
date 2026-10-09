"""Read-only byte, JSON, navigation and DAG check; not proof validation."""
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
INDEX=json.loads((HERE/"SQUARE_CLAIM_DEPENDENCY_ARTIFACT_INDEX.json").read_text())
ART={a["id"]:a for a in INDEX["artifacts"]}
CLAIMS={c["id"]:c for c in INDEX["claims"]}
TASKS={t["id"]:t for t in INDEX["next_tasks"]}
assert len(ART)==len(INDEX["artifacts"])
assert len(CLAIMS)==len(INDEX["claims"])
assert len(TASKS)==len(INDEX["next_tasks"])
for a in ART.values():
    data=(ROOT/a["path"]).read_bytes()
    assert hashlib.sha256(data).hexdigest()==a["sha256"], a["id"]
    assert len(data)==a["bytes"], a["id"]
    if a["path"].endswith(".json"): json.loads(data)
for c in CLAIMS.values():
    assert set(c["artifact_ids"])<=ART.keys(),c["id"]
    assert set(c["depends_on_claim_ids"])<=CLAIMS.keys(),c["id"]
for t in TASKS.values():
    assert set(t["minimal_artifact_ids"])<=ART.keys(),t["id"]
    assert set(t["depends_on_open_task_ids"])<=TASKS.keys(),t["id"]
    assert t["status"]=="OPEN_NOT_EXECUTED_CHECKPOINT_ONLY"
for c in INDEX["mandatory_corrections"]:
    assert set(c["origin_artifact_ids"]+c["required_artifact_ids"])<=ART.keys(),c["id"]
for c in INDEX["counterexamples"]:
    assert set(c["artifact_ids"])<=ART.keys(),c["id"]

def acyclic(items,field):
    done=set();active=set()
    def visit(key):
        if key in done:return
        assert key not in active,("dependency cycle",key)
        active.add(key)
        for dep in items[key][field]:visit(dep)
        active.remove(key);done.add(key)
    for key in items:visit(key)
acyclic(CLAIMS,"depends_on_claim_ids")
acyclic(TASKS,"depends_on_open_task_ids")
receipt=json.loads((HERE/"ADAPTIVE_REVIEW_STATUS_AND_PRECISION.json").read_text())
assert receipt["origin_artifact_id"] in ART
assert set(receipt["review_artifact_ids"])<=ART.keys()
assert INDEX["whole_square_interface_theorem"]=="NOT_ACQUIRED"
assert INDEX["sle_identification"]=="NOT_ACQUIRED"
assert INDEX["preservation_incidents"][0]["original_bytes_status"]=="LOST_NOT_RESTORED"
manifest_path=HERE/"MANIFEST.json"
if manifest_path.exists():
    manifest=json.loads(manifest_path.read_text())
    for rel,digest in manifest["files"].items():
        assert hashlib.sha256((HERE/rel).read_bytes()).hexdigest()==digest,rel
print(json.dumps({"status":"PASS_INTEGRITY_AND_ROUTING_ONLY","artifact_count":len(ART),"claims":len(CLAIMS),"open_tasks":len(TASKS),"proof_validation":False}))
