"""Nonmutating frozen-path replay. Default additionally generates charged test draws."""
from pathlib import Path
import json,hashlib,sys,gzip
import check_clock_response as T
import ordinary_coupled_geometric as O
ROOT=Path(__file__).resolve().parent
MANIFEST=ROOT/'REVIEW_FREEZE_MANIFEST_20261031_2348UTC.json'


def run(saved_only=False):
    manifest=json.loads(MANIFEST.read_text());verified=0
    for item in manifest['files']+manifest['dependencies']:
        path=ROOT.parent/item['path'];raw=path.read_bytes()
        assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256'];verified+=1
    saved=T.replay_saved();obs=json.loads((ROOT/'observed_response_v2.json').read_text());record=json.loads(gzip.decompress((ROOT/'observed_paired_paths.json.gz').read_bytes()))
    ordinary=O.receive_endpoint(record,expected_design=obs['design'],coin_seed=707)
    assert ordinary==json.loads((ROOT/'ordinary_matched_baseline.json').read_text())
    out=dict(status='PASS',verified_files=verified,saved=saved,ordinary_baseline_reproduced=True,new_source_calls=0)
    if not saved_only:
        checks=T.run();expected=json.loads((ROOT/'clock_checks_v3.json').read_text())
        assert {k:v for k,v in checks.items() if k!='seconds'}=={k:v for k,v in expected.items() if k!='seconds'}
        out['harness']=checks;out['new_source_calls']=checks['actual_source_calls_in_this_test_run']
    return out

if __name__=='__main__':print(json.dumps(run('--saved-only' in sys.argv),indent=2))
