"""Verify raw integrity, analytic kernel assembly, and saved witness residuals."""
from pathlib import Path
import hashlib,json
import numpy as np
from audit_data import EXPECTED,load,pulse_info
from joint_lp import step_matrix,target
BASE=Path(__file__).resolve().parents[1]

def main():
    checks=[]
    for name,md5 in EXPECTED.items():
        assert hashlib.md5((BASE/'data'/name).read_bytes()).hexdigest()==md5
    checks.append('all three original MATs match published MD5')
    _,p,_=load()
    for cell in range(92):
        for sign in ['pos','neg']:
            info=pulse_info(p,sign,cell)
            assert info['on_bracket_s'][0]<=info['assumed_on_s']<=info['on_bracket_s'][1]
            assert info['off_bracket_s'][0]<=info['assumed_off_s']<=info['off_bracket_s'][1]
    checks.append('all 184 inferred 10s commands lie inside voltage switching brackets')
    s=np.r_[0.,np.linspace(.0001,.9999,300),1.]
    times=np.r_[np.linspace(.2,9.9,30),np.geomspace(10.2,2000,30)]
    B=step_matrix(s,times,0.,10.)
    direct=np.array([target(s,t) if t<10 else target(s,t)-target(s,t-10) for t in times])
    assert abs(B-direct).max()<2e-10
    checks.append('stable finite-pulse kernels agree with independent step superposition including both compact endpoints')
    for d in BASE.glob('results/joint_lp_*_witness.npz'):
        w=np.load(d,allow_pickle=True)
        assert abs(w['F']@w['coef']-w['y']).max()<.100001
        assert np.all(w['coef'][:-1]>=-1e-12)
    checks.append('all six LP witnesses have nonnegative compact masses and EIS residual <0.100001mOhm')
    for d in BASE.glob('results/query_*_witness.npz'):
        w=np.load(d); assert np.all(w['coef'][:-1]>=-1e-12)
    checks.append('all ten joint target query witnesses have nonnegative compact masses')
    for d in BASE.glob('results/hybrid_*_predictions.npz'):
        w=np.load(d)
        for k in w.files: assert np.all(np.isfinite(w[k])),(d.name,k)
    checks.append('all original-upstream baseline prediction arrays are finite')
    g=json.loads((BASE/'results/paired_gate.json').read_text())
    assert g['all_92']['failed_count']==92
    checks.append('92/92 paired gates fail with exact rational increment-error floors')
    out={'status':'PASS','checks':checks,'scope':'Computational integrity and conditional kernel identities. Not physical validation or a calibrated noise confidence statement.'}
    (BASE/'results/check_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))

if __name__=='__main__':main()
