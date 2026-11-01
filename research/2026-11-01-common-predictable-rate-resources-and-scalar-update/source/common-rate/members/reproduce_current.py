"""Current runtime first, then full frozen audit, all in fresh temporary copies."""
from pathlib import Path
import tempfile,shutil,subprocess,json,os,hashlib,sys
from restore_historical_aliases import verify_payload,restore,check,safe
ROOT=Path(__file__).resolve().parent

def run(script,cwd,*args):
    p=subprocess.run([sys.executable,script,*args],cwd=cwd,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
    if p.stderr:raise AssertionError(p.stderr.decode())
    return p.stdout

def main():
    physical=verify_payload(ROOT)
    allow=json.loads((ROOT/'STRICT_ALLOWLIST.json').read_text())['members']
    current_files=json.loads((ROOT/'runtime/ARTIFACT_ALLOWLIST.json').read_text())['members']
    author_runs=[];independent=[]
    with tempfile.TemporaryDirectory(prefix='received_common_box_') as temp:
        work=Path(temp);current=work/'current';current.mkdir()
        for name in current_files:
            target=safe(current,name);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/'runtime'/name,target)
        # All current runtime bytes are present without historical reconstruction.
        for script,expected in [('check_common_box.py','common_box.stdout'),('check_box_large_tiers.py','large_tiers.stdout'),('check_scalar_extremes.py','scalar_extremes.stdout'),('check_v2_receiving.py','v2_receiving.stdout')]:
            out=run(script,current)
            assert out==(ROOT/'runtime'/expected).read_bytes(),script+' differs'
            author_runs.append({'script':script,'stdout_sha256':hashlib.sha256(out).hexdigest()})
        for name in current_files:assert (current/name).read_bytes()==(ROOT/'runtime'/name).read_bytes(),name
        full=work/'full';full.mkdir()
        for name in allow:
            target=safe(full,name);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
        restored=restore(full);audit=full/'whole_audit'
        saved_verification=run('verify_saved_audit.py',audit).decode().strip()
        # Put the ACTUALLY replayed current bytes in the audit's documented import location.
        for name in current_files:
            target=audit/'replay_v2'/name;assert target.read_bytes()==(current/name).read_bytes();shutil.copyfile(current/name,target)
        gate=audit/'theorem_gate';run('independent_box_checks.py',gate)
        # Compare against the still-immutable source snapshot, not a just-overwritten result.
        gate_expected=json.loads((ROOT/'LOGICAL_BINDINGS.json').read_text())['files']['whole_audit/theorem_gate/CHECK_RESULTS.json']
        check(gate/'CHECK_RESULTS.json',gate_expected)
        for script,args,result in [('independent_arithmetic.py',['v2'],'arithmetic_v2_results.json'),('independent_controls.py',['v2'],'controls_v2_results.json'),('independent_repair.py',[],'repair_v2_results.json'),('final_supplement.py',[],'supplement_results.json')]:
            expected=json.loads((audit/result).read_text());run(script,audit,*args);got=json.loads((audit/result).read_text())
            old_seconds=expected.pop('seconds',None);new_seconds=got.pop('seconds',None)
            assert got==expected,script+' substantive replay differs'
            independent.append({'script':script,'assertions':got['checks'],'timing_only_may_differ':old_seconds is not None or new_seconds is not None})
        verify_payload(ROOT)
        report={'status':'PASS_CURRENT_RUNTIME_AND_COMPLETE_RELOCATED_AUDIT','physical_bindings':physical,'author_runtime_before_alias_restore':True,'author_runs':author_runs,'historical_restoration':restored,'saved_audit_verification':saved_verification,'theorem_assertions':4046,'independent_v2_assertions':sum(x['assertions'] for x in independent),'independent_runs':independent,'original_payloads_unchanged':True,'v1_status':'FAILURE_HISTORY_ONLY_NOT_ACCEPTED'}
    return report

if __name__=='__main__':print(json.dumps(main(),sort_keys=True,indent=2))
