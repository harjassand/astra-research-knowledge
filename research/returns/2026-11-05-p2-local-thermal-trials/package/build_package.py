"""Package completed constructions and preserve the previous archive unchanged."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT=Path(__file__).resolve().parent
WARM_NAME='predictive_preparation_research_package.zip'
WARM_SHA='f27ebd9ecf24cee11732056db140095c06683869fef81ea8133f447e6fc8557c'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    warm=ROOT/'warm'/WARM_NAME
    if not warm.exists(): warm=ROOT.parent/WARM_NAME
    assert warm.stat().st_size==6965783 and sha(warm)==WARM_SHA
    prior={'name':WARM_NAME,'bytes':warm.stat().st_size,'sha256':WARM_SHA,
           'method':'unchanged nested archive, no prior proof or execution modified'}
    (ROOT/'PRESERVATION.json').write_text(json.dumps(prior,indent=2)+'\n')
    finite=json.loads((ROOT/'uncertainty/finite_receiver/results.json').read_text())
    receipt={
        'selected_result':'finite local thermal randomized-intervention construction',
        'status':'completed conditional classical theorem and finite instrument construction',
        'historical_priority':'not established',
        'laboratory_implementation':'not performed',
        'norm':'total variation is half L1; earlier quantum half-diamond unchanged',
        'analytic_scope':'nonlinear Hamiltonian environment, factorized kinetic Gibbs coordinate, actual fresh local Langevin port, reference-inclusive finite entropy, private bounded-density timing, priced finite metrology',
        'finite_receiver':{'attempts':finite['attempts'],
            'clock_successes':finite['successful_clock_trials'],
            'conditional_model_error_before_hardware':finite['theorem_contract']['conditional_success_joint_error_bound_before_hardware_discrepancies'],
            'scope':finite['scope']},
        'preservation':prior,
        'report_sha256':sha(ROOT/'local_thermal_trials.pdf')
    }
    (ROOT/'COMPLETE_RESULT_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    files=[p for p in sorted(ROOT.rglob('*')) if p.is_file()
           and '__pycache__' not in p.parts and 'warm' not in p.relative_to(ROOT).parts
           and p.name!='MANIFEST.json'
           and p.suffix not in {'.pyc','.aux','.log','.out','.toc'}]
    manifest={'format':'sha256','files':[{'path':str(p.relative_to(ROOT)),
        'bytes':p.stat().st_size,'sha256':sha(p)} for p in files]}
    manifest['files'].append({'path':'warm/'+WARM_NAME,'bytes':warm.stat().st_size,'sha256':WARM_SHA})
    mf=ROOT/'MANIFEST.json';mf.write_text(json.dumps(manifest,indent=2)+'\n')
    target=ROOT.parent/'local_thermal_trials_research_package.zip'
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=8) as z:
        for p in files+[mf]:z.write(p,str(p.relative_to(ROOT)))
        z.write(warm,'warm/'+WARM_NAME)
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        for item in manifest['files']:
            data=z.read(item['path'])
            assert len(data)==item['bytes']
            assert hashlib.sha256(data).hexdigest()==item['sha256']
    print(json.dumps({'archive':str(target),'bytes':target.stat().st_size,
        'sha256':sha(target),'members':len(manifest['files'])+1,
        'warm_preserved':True},indent=2))

if __name__=='__main__':main()
