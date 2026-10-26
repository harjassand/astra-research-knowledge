"""Independent exact checks and isolated byte-identical execution of 3 scripts."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import sympy as s

ROOT=Path(__file__).resolve().parent
R=s.Rational
t=s.Symbol('t',real=True)
S=s.Matrix([[2,1,0],[1,2,0],[0,0,t]])
e0=s.Matrix([1,0,0]);e1=s.Matrix([0,1,0]);e2=s.Matrix([0,0,1])


def skew(k):return s.Matrix([[0,0,k],[0,0,0],[-k,0,0]])


def direct_task(A):
    f=(e2.T*(A-skew(1)).inv()*e2)[0]-R(49,16)*(e2.T*(A-skew(2)).inv()*e2)[0]
    return s.cancel(f)


def main():
    j=json.loads((ROOT/'acquired_latent_controller_results.json').read_text())
    a=json.loads((ROOT/'active_latent_precision_results.json').read_text())
    b=json.loads((ROOT/'bias_cancelling_experiments_results.json').read_text())
    f=direct_task(S)
    expected= s.cancel(3/(3*t+2)-R(49,16)*3/(3*t+8))
    assert s.cancel(f-expected)==0
    derivative=s.factor(s.diff(f,t))
    expected_derivative=81*(t-2)*(33*t+46)/(16*(3*t+2)**2*(3*t+8)**2)
    assert s.cancel(derivative-expected_derivative)==0
    assert f.subs(t,2)==-R(9,32)
    assert f.subs(t,1)==-R(207,880)
    assert f.subs(t,3)<f.subs(t,1)
    # Do not trust the optimizing script's claims of exact range.
    chief=j['compiled_late_portfolios']['nonsymmetric_feedback_contrast_interior_optimum']
    assert chief['shared_source_outer']==['-9/32','-207/880']
    assert R(chief['width_reduction'])==R(2068,153)
    # Test the portfolio's precomputed bounds against exact direct matrix solves
    # for 21 independently selected rational models from the entire family.
    names=list(j['compiled_late_portfolios'])
    Ksym=s.diag(R(1,4),-R(1,4),R(1,3))
    Kmix=s.Matrix([[0,R(1,5),R(1,6)],[-R(1,6),0,0],[0,0,R(1,4)]])
    def port(name,A):
        inverse=lambda K:A.__sub__(K).inv()
        if name=='nonsymmetric_feedback_contrast_interior_optimum':
            return direct_task(A)
        if name=='three_controllers_signed_combo':
            return (2*(e2.T*inverse(skew(1))*e2)[0]
                   -3*(e2.T*inverse(skew(2))*e2)[0]
                   +(e2.T*inverse(skew(3))*e2)[0])
        if name=='cross_port_observables':
            return ((e0.T*inverse(skew(1))*e2)[0]
                    +(e1.T*inverse(skew(2))*e2)[0]
                    -2*(e2.T*inverse(skew(3))*e0)[0])
        if name=='symmetric_nonsymmetric_mixed_portfolio':
            return ((e2.T*inverse(Ksym)*e2)[0]
                    -R(7,5)*(e2.T*inverse(Kmix)*e2)[0]
                    +R(1,2)*(e0.T*inverse(skew(1))*e2)[0])
        raise AssertionError(name)
    tested=0
    for k in range(21):
        z=R(1)+R(k,10)
        matrix=S.subs(t,z)
        assert (matrix-s.eye(3)).is_positive_semidefinite
        assert (3*s.eye(3)-matrix).is_positive_semidefinite
        for name in names:
            lower,upper=map(R,j['compiled_late_portfolios'][name]['shared_source_outer'])
            answer=s.factor(port(name,matrix))
            assert lower<=answer<=upper,(name,z,answer)
            tested+=1
    # Rebuild the noisy indistinguishable source pair, independent of its script.
    sparam=R(1,1000);beta=(1-sparam*sparam)/(1+sparam*sparam)
    gamma=2*sparam/(1+sparam*sparam)
    eps=1-beta
    noisy=j['noise_stability_and_obstruction']
    assert str(eps)==noisy['allowed_euclidean_reading_error']
    for sg in [-1,1]:
        matrix=s.Matrix([[2,beta,0],[beta,2,sg*gamma],[0,sg*gamma,2]])
        assert (matrix-s.eye(3)).is_positive_semidefinite
        assert (3*s.eye(3)-matrix).is_positive_semidefinite
        assert (matrix*e0-s.Matrix([2,1,0])).norm()==eps
        lower,upper=map(s.sympify,noisy['certified_robust_range'])
        actual=direct_task(matrix)
        assert bool((actual-lower).evalf()>0) and bool((upper-actual).evalf()>0)
    # Verify the reference vector sensor calibration against native equations.
    new=b['exact_two_probe_reconstruction']
    fixedbias=s.Matrix([R(1,10),-R(1,5),R(3,10)])
    matrix=S.subs(t,R(7,4))
    assert [list(map(R,x)) for x in new['actual_readings']]==[list(matrix*e0+fixedbias),list(matrix*e2+fixedbias)]
    # The two adversarially indistinguishable families remain within per-read noise
    # on a broader list of simplex inputs, without relying on the generating script.
    eta=R(1,100)
    for k in range(41):
        u=R(k,40)
        q=(1-u)*e0+u*e2
        tplus=R(7,4)+2*eta;tminus=R(7,4)-2*eta
        bplus=fixedbias-eta*e2;bminus=fixedbias+eta*e2
        yplus=S.subs(t,tplus)*q+bplus
        yminus=S.subs(t,tminus)*q+bminus
        assert (yplus-yminus).norm()<=2*eta
    # Actual isolated independent rerun of all source-producing programmes.
    scripts=[('acquired_latent_controller_compiler.py','acquired_latent_controller_results.json'),
             ('active_latent_precision.py','active_latent_precision_results.json'),
             ('bias_cancelling_experiments.py','bias_cancelling_experiments_results.json')]
    replays=[]
    with tempfile.TemporaryDirectory(prefix='astra_pro3_latent_verified_') as tmp:
        target=Path(tmp)
        for script,_ in scripts:shutil.copy2(ROOT/script,target/script)
        for script,result in scripts:
            process=subprocess.run([sys.executable,str(target/script)],cwd=target,
                                    stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    text=True,timeout=45,check=True)
            original=(ROOT/result).read_bytes();regenerated=(target/result).read_bytes()
            assert original==regenerated,script
            replays.append(dict(script=script,result=result,sha256=hashlib.sha256(original).hexdigest(),
                                byte_identical=True,last_output_line=process.stdout.strip().splitlines()[-1]))
    data=dict(signed_controller_exact_range_verified=True,checked_direct_source_portfolio_inclusions=tested,
              independent_noisy_source_pairs_checked=2,independent_bias_counterexamples_checked=41,
              byte_identical_isolated_replays=replays,
              scope='All statements conditional on supplied linear-symmetric spectral and instrument error contracts; no external physical measurement')
    path=ROOT/'independent_verification_results.json'
    path.write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    print('INDEPENDENT VERIFICATION PASSED:',tested,'direct future-model checks;',len(replays),'byte-identical clean replays')

if __name__=='__main__':main()
