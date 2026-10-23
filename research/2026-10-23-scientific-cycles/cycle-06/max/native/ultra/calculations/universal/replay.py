#!/usr/bin/env python3
"""Bounded actual-state admissions for the universal readout theorem.

No optimizer, unknown-memory inference, hardware data or universal numerical
proof. Integer coefficient fixtures and POVM construction are explicit inputs.
"""
import os
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:
    os.environ[key]='1'
import itertools,json,math,resource,sys,time
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent
cpu0,wall0=time.process_time(),time.perf_counter()
m=math.log(2);C=2-m
def entropy(rho):
    lam=np.maximum(np.linalg.eigvalsh((rho+rho.conj().T)/2),0)
    return float(-sum(x*math.log(x) for x in lam if x>1e-13))
def partial(x,sites,n):
    t=x.reshape((2,)*(2*n));cur=n
    for s in sorted(sites,reverse=True):
        t=np.trace(t,axis1=s,axis2=s+cur);cur-=1
    return t.reshape(2**cur,2**cur)
def embed(a,sites,n):
    out=np.zeros((2**n,2**n),complex);rest=[j for j in range(n) if j not in sites]
    def packed(v,ss):
        return sum(((v>>(n-1-s))&1)<<(len(ss)-1-j) for j,s in enumerate(ss))
    for u in range(2**n):
        for v in range(2**n):
            if packed(u,rest)==packed(v,rest):out[u,v]=a[packed(u,sites),packed(v,sites)]
    return out
def erase(x,sites,n):
    return embed(partial(x,sites,n),[s for s in range(n) if s not in sites],n)/2**len(sites)
def sqrt_psd(a):
    v,u=np.linalg.eigh(a)
    return (u*np.sqrt(np.maximum(v,0)))@u.conj().T
def tensor(ops):
    out=np.ones((1,1),complex)
    for a in ops:out=np.kron(out,a)
    return out
I=np.eye(2);PX=np.array([[0,1],[1,0]]);PY=np.array([[0,-1j],[1j,0]]);PZ=np.diag([1,-1])
def povm(c,kind):
    if kind=='alice':single=[(I+PX)/4,(I-PX)/4,(I+PZ)/4,(I-PZ)/4]
    elif kind=='bob':single=[(I+PY)/4,(I-PY)/4,(I+PZ)/4,(I-PZ)/4]
    else:
        first=[(I+PZ)/4,(I-PZ)/4,I/2]
        return [tensor([a]+[I]*(c-1)) for a in first]
    return [tensor(ops) for ops in itertools.product(single,repeat=c)]

fixtures=json.loads((ROOT/'INPUTS.json').read_text())
states={}
for f in fixtures['pure_coefficients']:
    q=2**(f['r']*f['N'])
    z=np.array(f['real'],float).reshape(q,q)+1j*np.array(f['imag'],float).reshape(q,q)
    states[f['id']]=z/np.linalg.norm(z)

def evaluate(ensemble,r,N,bobkind):
    n=r*N;q=2**n
    Eensemble=sum(w*entropy(X.conj().T@X) for w,X in ensemble)
    score=0.;Qtot=0.;Ctot=0.;Rtot=0.;Rquant=0.;rows=[]
    non=max(float(np.linalg.norm(X.conj().T@X-X@X.conj().T)) for w,X in ensemble)
    rho=sum(w*(X.conj().T@X) for w,X in ensemble)
    compS=[]
    for a in range(r):
        task=list(range(a*N,(a+1)*N));comp=[j for j in range(n) if j not in task]
        A=povm(len(comp),'alice');B=povm(len(comp),bobkind)
        assert np.linalg.norm(sum(A)-np.eye(2**len(comp)))<1e-12
        assert np.linalg.norm(sum(B)-np.eye(2**len(comp)))<1e-12
        Af=[embed(v,comp,n) for v in A];Bf=[embed(v,comp,n) for v in B]
        As=[sqrt_psd(v) for v in Af];Bs=[sqrt_psd(v) for v in Bf]
        ranks=[int(np.count_nonzero(np.linalg.eigvalsh(v)>1e-10)) for v in B]
        ps=[sum(w*float(np.linalg.norm(erase(X,task[:i],n))**2) for w,X in ensemble) for i in range(1,N+1)]
        scorea=m*sum(ps);score+=scorea
        cq=[sum(w*partial(X.conj().T@aa@X,task,n) for w,X in ensemble) for aa in Af]
        py=np.array([float(np.trace(v).real) for v in cq])
        joint=np.array([[sum(w*float(np.linalg.norm(sa@X@sb)**2) for w,X in ensemble) for sb in Bs] for sa in As])
        assert abs(joint.sum()-1)<1e-12 and np.max(np.abs(joint.sum(axis=1)-py))<1e-12
        for y,z in [(0,0),(min(2,len(A)-1),min(1,len(B)-1))]:
            direct=sum(w*float(np.vdot(X.reshape(-1),np.kron(Af[y],Bf[z].T)@X.reshape(-1)).real) for w,X in ensemble)
            assert abs(direct-joint[y,z])<1e-12
        Q=sum(p*entropy(v/p) for p,v in zip(py,cq) if p>1e-14)
        Hcond=-sum(joint[y,z]*math.log(joint[y,z]/py[y]) for y in range(len(A)) for z in range(len(B)) if joint[y,z]>1e-14)
        rankcost=float(joint.sum(axis=0)@np.log(ranks))
        classical=Hcond+rankcost
        assert Q<=classical+2e-10
        # Fixed normalized soft predictor; never fit from this test law.
        pi=np.full(joint.shape,.3/len(B))
        for y in range(len(A)):pi[y,y%len(B)]+=.7
        costs=np.log(np.array(ranks)[None,:]/pi)
        cross=float(np.sum(joint*costs));assert classical<=cross+1e-10
        # Fixed strictly positive quantum references on coefficient-side complement.
        qcost=0.
        d=2**len(comp)
        for y,v in enumerate(cq):
            phase=np.exp(2j*np.pi*(y+1)*np.arange(d)/d)/math.sqrt(d)
            omega=.75*np.outer(phase,phase.conj())+.25*np.eye(d)/d
            lam,U=np.linalg.eigh(omega);H=(U*(-np.log(lam)))@U.conj().T
            qcost+=float(np.trace(v@H).real)
        assert Q<=qcost+1e-10
        Qpureavg=0.;branchE=0.;branchscore=np.zeros(N)
        if len(ensemble)==1:
            X=ensemble[0][1]
            for y,sa in enumerate(As):
                XY=sa@X;p=float(np.linalg.norm(XY)**2)
                if p>1e-14:Qpureavg+=p*entropy(partial(XY.conj().T@XY,task,n)/p)
                for sb in Bs:
                    V=XY@sb;weight=float(np.linalg.norm(V)**2)
                    if weight>1e-14:branchE+=weight*entropy(V.conj().T@V/weight)
                    for i in range(1,N+1):branchscore[i-1]+=float(np.linalg.norm(erase(V,task[:i],n))**2)
            assert abs(Qpureavg-Q)<1e-11
            assert max(abs(branchscore-np.array(ps)))<1e-11
            assert scorea<=branchE+C+1e-10
            pz=joint.sum(axis=0)
            MI=sum(joint[y,z]*math.log(joint[y,z]/(py[y]*pz[z])) for y in range(len(A)) for z in range(len(B)) if joint[y,z]>1e-14)
            assert branchE+MI<=Eensemble+1e-10
        Qavg=0.
        for w,X in ensemble:
            for aa in Af:
                v=partial(X.conj().T@aa@X,task,n);p=float(np.trace(v).real)
                if p>1e-14:Qavg+=w*p*entropy(v/p)
        assert Qavg<=Q+1e-10
        compS.append(entropy(partial(rho,task,n)))
        Qtot+=Q;Ctot+=classical;Rtot+=cross;Rquant+=qcost
        rows.append({'task':a,'prefix_probabilities':ps,'quantum_conditional_entropy':Q,
                     'classical_conditional_entropy':Hcond,'weighted_rank':rankcost,
                     'fixed_kernel_cost':cross,'fixed_quantum_reference_cost':qcost,
                     'Bob_effect_ranks':ranks,'ensembled_quantum_penalty':Qavg})
    assert sum(compS)>=(r-1)*entropy(rho)-1e-10
    for penalty in [Qtot,Ctot,Rtot,Rquant]:assert score-r*C-penalty<=Eensemble+1e-10
    return {'r':r,'N':N,'bob_POVM':bobkind,'ensemble_size':len(ensemble),
            'known_ensemble_entanglement_upper':Eensemble,'score':score,'Q_total':Qtot,
            'rank_conditional_total':Ctot,'linear_kernel_total':Rtot,'linear_quantum_reference_total':Rquant,
            'max_nonnormal_commutator_HS':non,'tasks':rows}

records=[]
for r,N in [(2,2),(3,1)]:
    for name in [f'r{r}_N{N}_s17',f'r{r}_N{N}_s31',f'r{r}_N{N}_identity']:
        records.append(evaluate([(1.,states[name])],r,N,'bob'))
    records.append(evaluate([(.4,states[f'r{r}_N{N}_s17']),(.6,states[f'r{r}_N{N}_s31'])],r,N,'coarse'))
assert max(row['max_nonnormal_commutator_HS'] for row in records)>.01
raw=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
result={'status':'PASS','scope':'eight fixed actual-state admissions; mixed checks use known ensemble upper, not an optimal E_F solver',
        'records':records,'numerical_tolerance':2e-10,'numpy':np.__version__,
        'cpu_seconds':time.process_time()-cpu0,'wall_seconds':time.perf_counter()-wall0,
        'peak_RSS_bytes':raw if sys.platform=='darwin' else raw*1024,
        'universal_proof':'analytic; finite checks are diagnostics only','total_discovery_cost':'UNKNOWN'}
(ROOT/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','cpu_seconds','wall_seconds','peak_RSS_bytes']}))
