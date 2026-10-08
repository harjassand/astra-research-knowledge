"""Diagnostics for the separate balanced-product extremality derivation.
Finite tests do not establish optimization over all product states. No subagents.
Run: OPENBLAS_NUM_THREADS=1 python casimir_extremality_checks.py
"""
import json, math
from pathlib import Path
import numpy as np
from universal_probe_checks import spin_ops, sector_exact, dense_probe
ROOT=Path(__file__).resolve().parent

def pure_product(rng,N):
    psi=np.array([1.+0j])
    for i in range(N):
        z=rng.normal(size=2)+1j*rng.normal(size=2); z/=np.linalg.norm(z)
        psi=np.kron(psi,z)
    return psi

def main():
    rng=np.random.default_rng(8102028)
    out={'status':'internally executed diagnostics, not proof certification', 'seed':8102028}
    fixtures=[]; random_cases=[]
    for N in [2,4,6,8]:
        rho,Js,J2=dense_probe(N)
        ev,U=np.linalg.eigh(J2)
        n=N//2; B=math.comb(N,n)
        mult=np.array([math.comb(N,n-j)-(math.comb(N,n-j-1) if n-j else 0) for j in range(n+1)])
        q=mult/B
        # Computational basis: n up (0), then n down (1).
        balanced=np.zeros(2**N,complex); balanced[2**n-1]=1
        en=np.arange(n+1)*(np.arange(n+1)+1)
        for t in [.01,.1,.5,1.,5.,20.]:
            A=(U*np.exp(-t*np.maximum(ev,0)))@U.conj().T
            bound=float(np.dot(q,np.exp(-t*en)))
            exact=float(np.vdot(balanced,A@balanced).real)
            fixtures.append({'N':N,'t':t,'balanced_value':exact,'separable_bound':bound,'equality_error':abs(exact-bound)})
            for z in range(50):
                psi=pure_product(rng,N)
                value=float(np.vdot(psi,A@psi).real)
                random_cases.append({'N':N,'t':t,'value':value,'bound':bound,'slack':bound-value})
                assert value<=bound+1e-10
            assert abs(exact-bound)<1e-10
    entropy=[]
    for N in [2,4,6,8,16,32,64,128,256,512]:
        ps,C=sector_exact(N); p=np.array(list(map(float,ps))); n=N//2
        B=math.comb(N,n)
        q=np.array([(math.comb(N,n-j)-(math.comb(N,n-j-1) if n-j else 0))/B for j in range(n+1)])
        ok=p>0
        upper=float(np.dot(p[ok],np.log(p[ok]/q[ok])))
        en=np.arange(n+1)*(np.arange(n+1)+1)
        b=float(np.dot(q,np.exp(-en)))
        lower=-float(C)-math.log(b)
        dist_target=float(np.dot(p,np.exp(-en/math.sqrt(N))))
        dist_sep=float(np.dot(q,np.exp(-en/math.sqrt(N))))
        dist=dist_target-dist_sep
        elementary=1-7/math.sqrt(N)-2/N
        assert lower<=upper+1e-9
        assert upper<=math.log(n+1)+1e-9
        assert dist>=elementary-1e-9
        entropy.append({'N':N,'relative_entropy_lower_t1':lower,'relative_entropy_to_balanced_twirl':upper,
                        'upper_minus_logN':upper-math.log(N),'heat_distance_lower':dist,'elementary_distance_lower':elementary})
    out.update({'balanced_equalities':fixtures,'random_product_cases':random_cases,'entropy_brackets':entropy,
                'counts':{'balanced_equalities':len(fixtures),'random_products':len(random_cases),'entropy_brackets':len(entropy)},
                'max_balanced_equality_error':max(x['equality_error'] for x in fixtures),
                'min_random_product_slack':min(x['slack'] for x in random_cases)})
    (ROOT/'casimir_extremality_results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({k:v for k,v in out.items() if k not in ['balanced_equalities','random_product_cases']},indent=2))
if __name__=='__main__': main()
