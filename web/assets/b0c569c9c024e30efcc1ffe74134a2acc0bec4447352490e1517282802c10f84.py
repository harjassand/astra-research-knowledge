"""Independent finite-N characteristic-function diagnostics for unital noise.

Uses a two-by-two symmetric-power character for the unpaired spin block,
not the finite-N filtered-moment formula in verify_threshold.py.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.linalg import expm
from verify_threshold import spin_weights, stationary_dense, local_channel, PAULI, I2


def pauli_bloch(probs):
    p=np.asarray(probs,float)
    return np.diag([p[0]+p[1]-p[2]-p[3],p[0]-p[1]+p[2]-p[3],p[0]-p[1]-p[2]+p[3]])


def finite_characteristic(n:int,nu:float,T,tvec):
    """Tr[Lambda^tensor(n)(rho) exp(i tvec.J/sqrt(n))].

    Supplied real T must be the Bloch matrix of a unital CPTP qubit map.
    The formula remains valid for non-diagonal T; this script diagnoses
    diagonal Pauli channels along generic measurement axes.
    """
    if not nu>0: raise ValueError('nu must be positive')
    T=np.asarray(T,float); tvec=np.asarray(tvec,float)
    if T.shape!=(3,3) or tvec.shape!=(3,): raise ValueError('Invalid shape')
    ell=float(np.linalg.norm(tvec))
    if ell==0: return 1+0j
    u=tvec/ell; theta=ell/(2*math.sqrt(n)); c=math.cos(theta); s=math.sin(theta)
    D=c*I2+1j*s*sum(a*p for a,p in zip(T.T@u,PAULI))
    q=nu/(1+nu)
    eigen=np.linalg.eigvals(np.diag([q,1.])@D)
    # Sorting is solely for stable exponentiation when a root is near one.
    a,b=sorted(eigen,key=abs,reverse=True)
    M,lw,_=spin_weights(n)
    if abs(a-b)<1e-10:
        active=(M+1)*a**M*(1-q)/(-np.expm1((M+1)*math.log(q)))
    else:
        active=(a**(M+1)-b**(M+1))/(a-b)*(1-q)/(-np.expm1((M+1)*math.log(q)))
    pair=c*c+float(u@(T@T.T)@u)*s*s
    pairpart=np.exp(((n-M)/2)*math.log(pair)) if pair>0 else np.where(n==M,1.,0.)
    return complex(np.sum(np.exp(lw)*pairpart*active))


def limiting_characteristic(T,tvec):
    T=np.asarray(T,float); t=np.asarray(tvec,float)
    Sigma=(np.eye(3)-T@T.T)/4; v=T[:,2]; b=float(t@v)/2
    density=lambda x: math.sqrt(2/math.pi)*x*x*math.exp(-x*x/2)
    real=quad(lambda x:density(x)*math.cos(b*x),0,np.inf,epsabs=1e-12)[0]
    imag=-quad(lambda x:density(x)*math.sin(b*x),0,np.inf,epsabs=1e-12)[0]
    return math.exp(-float(t@Sigma@t)/2)*complex(real,imag)


def run():
    rng=np.random.default_rng(8112026); count=0; maxerr=0.
    for n in range(2,7):
        for nu in [.2,1.,3.]:
            rho,J=stationary_dense(n,nu)
            for _ in range(3):
                probs=rng.dirichlet(np.ones(4)); T=pauli_bloch(probs)
                rn=local_channel(rho,n,probs)
                for __ in range(2):
                    t=rng.normal(size=3)*2
                    dense=complex(np.trace(rn@expm(1j*sum(x*a for x,a in zip(t,J))/math.sqrt(n))))
                    formula=finite_characteristic(n,nu,T,t)
                    err=abs(formula-dense); maxerr=max(maxerr,err); count+=1
                    assert err<2e-10,(n,nu,t,dense,formula)
    records=[]
    Ts=[np.diag([.58,.58,.58]),np.diag([.9,.7,.65]),np.diag([.1,.1,1.])]
    tvecs=[np.array([1.,0,0]),np.array([0.,0,1.]),np.array([.7,-.4,1.3])]
    for T in Ts:
        for t in tvecs:
            target=limiting_characteristic(T,t)
            for n in [100,10000,1000000,100000000]:
                got=finite_characteristic(n,1.,T,t)
                records.append({'n':n,'T_diagonal':np.diag(T).tolist(),'t':t.tolist(),
                    'finite_real':got.real,'finite_imag':got.imag,
                    'limit_real':target.real,'limit_imag':target.imag,'abs_error':abs(got-target)})
    out={'status':'fresh internal diagnostic; not external validation',
         'dense_characteristic_checks':{'count':count,'max_abs_error':maxerr},
         'large_n_characteristic_checks':records}
    Path(__file__).with_name('characteristic_results.json').write_text(json.dumps(out,indent=2,allow_nan=False))
    print(out['dense_characteristic_checks'])
    print('largest n=10^8 error:',max(r['abs_error'] for r in records if r['n']==100000000))
    return out

if __name__=='__main__':run()
