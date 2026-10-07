"""Finite diagnostics only; no fixture is a theorem or a priority certificate."""
import json
from pathlib import Path
import numpy as np

rng = np.random.default_rng(20261007)

def herm(x):
    return (x + x.conj().T) / 2

def fun(x, f):
    v, u = np.linalg.eigh(herm(x))
    return (u * f(v)) @ u.conj().T

def root(x):
    return fun(x, lambda v: np.sqrt(np.maximum(v, 0)))

def norm1(x):
    return float(np.linalg.svd(x, compute_uv=False).sum())

def norm2(x):
    return float(np.linalg.norm(x))

def density(x):
    x = herm(x)
    return x / np.trace(x).real

def random_h(n):
    x = herm(rng.normal(size=(n,n)) + 1j*rng.normal(size=(n,n)))
    return x / max(abs(np.linalg.eigvalsh(x)))

def gap(a,b):
    z = root(a) @ root(b)
    return max(0., norm1(z) - np.trace(z).real)

def canonical(omega, rho):
    s = root(omega)
    invs = fun(omega, lambda v: 1/np.sqrt(v))
    return herm(invs @ root(s @ rho @ s) @ invs)

results = {"scope": "finite floating fixtures; not proof or novelty certification"}
canonical_checks = 0
max_canonical_ratio = 0.
max_comm_ratio = 0.
max_identity_residual = 0.
for n in [2,3,5,8,12]:
    for _ in range(40):
        weights = np.exp(rng.uniform(-7,0,n)); weights /= weights.sum()
        omega = np.diag(weights)
        s = root(omega)
        h = random_h(n) * rng.uniform(.05,.9)
        eh = fun(h, np.exp)
        rho = density(s @ eh @ s)
        x = canonical(omega,rho)
        q = root(rho)
        c = float(np.linalg.eigvalsh(fun(omega,lambda v:1/np.sqrt(v)) @ rho @ fun(omega,lambda v:1/np.sqrt(v))).max())
        delta = gap(omega,rho)
        rhs = 2*np.sqrt(c)*delta
        lhs = norm2(x@s-q)**2
        max_canonical_ratio = max(max_canonical_ratio,lhs/max(rhs,1e-15))
        max_comm_ratio = max(max_comm_ratio,norm2(x@s-s@x)/(2*np.sqrt(max(rhs,1e-15))))
        max_identity_residual = max(max_identity_residual,norm1(x@omega@x-rho))
        assert lhs <= rhs + 2e-8
        assert norm2(x@s-s@x) <= 2*np.sqrt(max(rhs,0)) + 2e-7
        assert np.linalg.eigvalsh(x).max() <= np.sqrt(c)+2e-7
        canonical_checks += 1
results["canonical"] = {"fixtures":canonical_checks,"max_defect_to_bound":max_canonical_ratio,"max_commutator_to_bound":max_comm_ratio,"max_rho_identity_residual":max_identity_residual}

log_checks=0; max_log_ratio=0.
for n in [2,4,9,16]:
    for _ in range(30):
        weights=np.exp(rng.uniform(-15,0,n));weights/=weights.sum()
        s=np.sqrt(weights);a=random_h(n);t=rng.uniform(.02,1)
        logdiff=np.abs(np.log(s[:,None]/s[None,:]))
        p=np.minimum(1,logdiff/t)
        expected=float(np.sum(abs(a)**2*weights[None,:]*p))
        xi=norm2(a@np.diag(s)-np.diag(s)@a)
        bound=3*xi/t
        max_log_ratio=max(max_log_ratio,expected/bound)
        assert expected<=bound+1e-12
        log_checks+=1
results["log_bin_expectation"]={"fixtures":log_checks,"max_ratio":max_log_ratio}

central_checks=0;max_central_ratio=0.
for n in [2,4,7,11]:
    for _ in range(40):
        x=fun(random_h(n),lambda v:v+1.01)
        y=fun(random_h(n),lambda v:v+1.01)
        x/=np.sqrt(np.trace(x@x).real/n)
        y/=np.sqrt(np.trace(y@y).real/n)
        rx=x@x/n;ry=y@y/n
        delta=gap(rx,ry)
        l=max(np.linalg.eigvalsh(x).max(),np.linalg.eigvalsh(y).max())
        lhs=norm2(x@y-y@x)/np.sqrt(n)
        rhs=2*np.sqrt(2)*l*np.sqrt(delta)
        max_central_ratio=max(max_central_ratio,lhs/max(rhs,1e-15))
        assert lhs<=rhs+2e-10
        central_checks+=1
results["central_gap_commutator"]={"fixtures":central_checks,"max_ratio":max_central_ratio}

def mub_prime(d):
    states=[]
    for j in range(d):
        v=np.eye(d,dtype=complex)[:,j];states.append(np.outer(v,v.conj()))
    for a in range(d):
        for b in range(d):
            v=np.exp(2j*np.pi*(a*np.arange(d)**2+b*np.arange(d))/d)/np.sqrt(d)
            states.append(np.outer(v,v.conj()))
    return states

mub_results=[]
for d in [3,5,7]:
    states=mub_prime(d)
    moment=sum(np.kron(p,p) for p in states)/len(states)
    swap=np.zeros((d*d,d*d))
    for i in range(d):
        for j in range(d):swap[i*d+j,j*d+i]=1
    residual=norm2(moment-(np.eye(d*d)+swap)/(d*(d+1)))
    assert residual<1e-12
    measured=[np.eye(d)[:,j:j+1]@np.eye(d)[j:j+1,:] for j in range(d)]
    avg=sum(sum(np.trace(e@p).real*np.trace(p@e).real for e in measured) for p in states)/len(states)
    assert abs(avg-2/(d+1))<1e-12
    mub_results.append({"d":d,"states":len(states),"2design_residual":residual,"dephasing_average_survival":avg,"pair_gap":d**(-.5)-d**(-1)})
results["MUB_obstruction"]=mub_results

qubit_a=np.array([[.8,.12j],[-.12j,.2]])
qubit_b=np.array([[.55,.2],[.2,.45]])
basegap=gap(qubit_a,qubit_b)
tensor_results=[]
for d in [1,3,9,27]:
    ra=np.kron(np.eye(d)/d,qubit_a);rb=np.kron(np.eye(d)/d,qubit_b)
    dg=gap(ra,rb)
    assert abs(dg-basegap)<1e-12
    tensor_results.append({"background_rank":d,"gap":dg,"raw_density_commutator_HS":norm2(ra@rb-rb@ra)})
results["diffuse_background_stress"]=tensor_results

out=Path(__file__).with_name("lemma_diagnostics.json")
out.write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
