"""Bounded rejection controls for the frozen independent certificate checker.

One valid N4 case and five corrupted exact-evidence cases test distinct
load-bearing interfaces. These are controls, not new scientific certificates.
"""
from pathlib import Path
import copy,datetime,hashlib,json,time
from optimal_prefix_independent_integer_verifier import Checker

OWN=Path(__file__).parent
ROOT=OWN.resolve().parents[3]

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    budget=ROOT/'work/cycle6/c05_s03/OPTIMAL_PREFIX_CORRUPT_CONTROL_BUDGET.json'
    admission=json.loads(budget.read_text())
    assert admission['declared_total_wall_cap_seconds']==10
    outpath=OWN/'optimal_prefix_adversarial_controls.json'
    assert not outpath.exists(),'Preserving earlier controls receipt'
    start=time.perf_counter();deadline=start+10
    source=ROOT/admission['source']
    data=json.loads(source.read_text())
    valid=copy.deepcopy(next(c for c in data['cases'] if c['N']==4))
    receipt={'status':'RUNNING','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'declared_total_wall_cap_seconds':10,'source':admission['source'],
             'source_sha256':sha(source),'checker_sha256':sha(OWN/'optimal_prefix_independent_integer_verifier.py'),
             'budget_sha256':sha(budget),'controls':[]}
    controls=[('valid N4 exact evidence',valid,False)]
    c=copy.deepcopy(valid);c['q_intervals'][0]=[0,0];c['q_intervals'][4]=[0,0]
    controls.append(('zero endpoint q contradicts independent exponential',c,True))
    c=copy.deepcopy(valid);c['matrices'][0]['diagonal_intervals'][0]=[0,0]
    controls.append(('zero first pivot violates strict positivity and enclosure',c,True))
    c=copy.deepcopy(valid);c['matrices'][0]['L_strict_lower_intervals'][1][0]=[0,0]
    controls.append(('zero nonzero L factor violates quotient cross multiplication',c,True))
    c=copy.deepcopy(valid);c['matrices'][0]['block_kind']='full_odd'
    controls.append(('wrong congruence block metadata',c,True))
    c=copy.deepcopy(valid);c['matrices'].pop()
    controls.append(('missing required congruence block',c,True))
    try:
        for name,case,expected_reject in controls:
            checker=Checker(768,64,deadline);checker.check_time(name)
            rejected=False;error=None
            try:checker.case(case)
            except AssertionError as e:rejected=True;error=repr(e)
            assert rejected==expected_reject,name+' failed its advertised control outcome'
            receipt['controls'].append({'control':name,'expected_reject':expected_reject,
                                        'observed_reject':rejected,'result':'PASS expected outcome',
                                        'rejection_stage':checker.stage if rejected else None,'error':error})
        receipt['status']='PASS valid control accepted and all five distinct corrupt controls rejected'
    except Exception as e:
        receipt['status']='INCOMPLETE';receipt['failure']=repr(e)
    receipt['wall_seconds']=time.perf_counter()-start
    receipt['script_sha256']=sha(Path(__file__))
    outpath.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
    if receipt['status']=='INCOMPLETE':raise SystemExit(1)

if __name__=='__main__':main()
