"""Dense and exact checks for the robustness theorem and signed compiler."""
from __future__ import annotations
import json,sys,math,itertools,time
from pathlib import Path
import numpy as np
import sympy as sp
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from fermion_completion import *
from gaussian_robustness import *

# Import helpers without executing the comprehensive test suite.
scope={"__file__":str(Path(__file__).with_name('check_all.py'))}
text=Path(__file__).with_name('check_all.py').read_text()
exec(text[:text.index('start=time.perf_counter()')],scope)
bcs_vector=scope['bcs_vector'];density_formula=scope['density_formula']
fock_covariance=scope['fock_covariance'];covariance_distribution=scope['covariance_distribution']
fock_lift=scope['fock_lift'];unitary=scope['unitary']
PRUNED=[];TERMINAL_CLIPPING=[]
def covariance_distribution(g):
    # Dense diagnostic only: avoid ill-conditioned branches with total mass
    # below 1e-11. Report, rather than hide, every discarded probability.
    m=len(g)//2;out=np.zeros(2**m);discarded=0.
    def rec(h,p,mask,depth):
        nonlocal discarded
        if depth==m:out[mask]=p;return
        if depth==m-1:
            TERMINAL_CLIPPING.append(p*max(0.,abs(float(h[0,1]))-1)/2)
            pp=float(np.clip((1+h[0,1])/2,0,1))
            out[mask]=p*(1-pp);out[mask|(1<<depth)]=p*pp
            return
        if p<=1e-11:discarded+=p;return
        for bit in (0,1):
            prob=float(np.clip((1+(2*bit-1)*h[0,1])/2,0,1))
            if p*prob<=1e-11:discarded+=p*prob;continue
            w,new=condition_first_mode(h,bit)
            rec(new,p*w,mask|(bit<<depth),depth+1)
    rec(g,1.,0,0);PRUNED.append(discarded)
    return out


def pure(v):return np.outer(v,v.conj())

def ensemble(e):
    a,b=(1-e)**2,e*e;R=magic_robustness(e)
    z=math.sqrt(b/(2*a)) if b<=2*a and a>0 else 1.
    ew=(a+b+R)/(1+R)
    out=[]
    for ell in range(3):
        phase=np.exp(2j*math.pi*ell/3)
        f=canonical_pair_matrix(np.array([z*phase,z*phase]))
        out.append((1,(1+R)*ew/3,bcs_vector(f)))
    for j in range(4):
        v=np.zeros(16,complex);v[1<<j]=1
        out.append((1,e*(1-e)/2,v))
    vac=np.eye(16,dtype=complex)[:,0];full=np.eye(16,dtype=complex)[:,15]
    if b<=2*a:out.append((-1,R,full))
    else:
        out.extend([(-1,b/2-a,vac),(-1,b/2,full)])
    return [(sg,w,v) for sg,w,v in out if w>0]

start=time.perf_counter();max_id=max_witness=max_engine=0.;cases=0
phi=np.zeros(16,complex);phi[3]=phi[12]=1/math.sqrt(2)
P2=np.diag([float(k.bit_count()==2) for k in range(16)])
s=canonical_pair_matrix(np.array([1,1])/math.sqrt(2))
for e in [0.,.001,.03,.1,.3,.5,math.sqrt(2)/(1+math.sqrt(2)),.65,.8,.95,1.]:
    rho=density_formula(s,e);ens=ensemble(e);R=magic_robustness(e)
    signed=sum(sign*w*pure(v) for sign,w,v in ens)
    max_id=max(max_id,float(np.max(abs(signed-rho))))
    assert abs(sum(w for _,w,_ in ens)-(1+2*R))<1e-12
    if e>0:
        a,b=(1-e)**2,e*e;t=min(b/(4*a),.5) if a>0 else .5
        W=pure(phi)-P2/2;W[0,0]-=t;W[15,15]-=1/(4*t)
        lower=float(np.trace(4*t*W@rho).real)
        max_witness=max(max_witness,abs(lower-R))
        assert np.linalg.eigvalsh(4*t*W)[0]>=-1-1e-10
        positive=sum(w*pure(v) for sign,w,v in ens if sign==1)
        assert abs(np.trace(W@positive).real)<1e-8
    u=unitary(4);lift=fock_lift(u)
    target=np.diag(lift@rho@lift.conj().T).real
    estimate=sum(sign*w*covariance_distribution(gaussian_loss(fock_covariance(v,4),u)) for sign,w,v in ens)
    max_engine=max(max_engine,float(np.max(abs(target-estimate))));cases+=1
assert max(max_id,max_witness,max_engine)<1e-8
# Exact symbolic witness optimum (both branches).
a,b=sp.symbols('a b',positive=True);t=b/(4*a)
assert sp.simplify(2*b*t-4*a*t*t-b*b/(4*a))==0
assert sp.simplify((2*b*sp.Rational(1,2)-4*a*sp.Rational(1,4))-(b-a))==0
# Two-block signed tensor contraction, all 256 probabilities.
es=[.3,.65];enss=[ensemble(e) for e in es];u=unitary(8);lift=fock_lift(u)
rho=np.kron(density_formula(s,es[1]),density_formula(s,es[0]))
true=np.diag(lift@rho@lift.conj().T).real;computed=np.zeros(256)
for (s1,w1,v1),(s2,w2,v2) in itertools.product(*enss):
    g=np.zeros((16,16));g[:8,:8]=fock_covariance(v1,4);g[8:,8:]=fock_covariance(v2,4)
    computed+=s1*s2*w1*w2*covariance_distribution(gaussian_loss(g,u))
err=float(np.max(abs(true-computed)));assert err<1e-10
# Actual Monte Carlo signed engine, observable in [0,1].
result=estimate_output_function([.35],np.eye(4),lambda bits:float(bits.sum()==2),draws=12000,seed=20261007)
truth=.35**2
assert abs(result['estimate']-truth)<result['hoeffding_radius']
out={"status":"all assertions passed","single_block_transmissions":cases,
     "max_signed_density_identity_error":max_id,"max_robustness_witness_equality_error":max_witness,
     "max_signed_covariance_outcome_error":max_engine,"exact_symbolic_identities":2,"max_discarded_dense_diagnostic_branch_mass":max(PRUNED),"diagnostic_cutoff":1e-11,"sum_terminal_clipping_mass_over_all_diagnostics":sum(TERMINAL_CLIPPING),
     "two_block_all_outcome_max_error":err,"signed_tensor_components":len(enss[0])*len(enss[1]),
     "monte_carlo_execution":result,"monte_carlo_truth":truth,"elapsed_seconds":time.perf_counter()-start}
Path(__file__).with_name('robustness_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
