"""Bounded consistency checks for the explicit approximation-to-exactness barrier."""
from pathlib import Path
import json
import numpy as np

rng = np.random.default_rng(73189)
d = 3
e = np.eye(9, dtype=complex)
ket = lambda i, j: e[:, 3 * i + j]
proj = lambda x: np.outer(x, x.conj())
P = proj(sum(ket(i, i) for i in range(3)) / np.sqrt(3))
sp = sum(proj(ket(i, (i+1)%3)) for i in range(3))/3
sm = sum(proj(ket(i, (i-1)%3)) for i in range(3))/3
s0 = sum(proj(ket(i, i)) for i in range(3))/3
W = 3*s0 + 3*sm - sum(np.outer(ket(i,i), ket(j,j).conj()) for i in range(3) for j in range(3) if i != j)
w = np.exp(2j*np.pi/3)
A = np.zeros((9,9),dtype=complex)
for a in range(3):
    for b in range(3):
        u = np.array([1,w**a,w**b])/np.sqrt(3)
        A += proj(np.kron(u,u.conj()))/9
rho0 = (2*P+3*sp+2*sm)/7
pt = lambda M: M.reshape(3,3,3,3).transpose(0,3,2,1).reshape(9,9)
margin = lambda M: float(np.linalg.eigvalsh(M).min())
norm1 = lambda M: float(np.linalg.svd(M,compute_uv=False).sum())
assert np.allclose(A,(P+sp+sm)/3)
assert np.allclose(rho0,(6*A+sp)/7)
checks=[]
filter_checks=0
for t in [1e-8,1e-5,.01,.1,.2,.5,1.]:
    rho=(2*P+(3+t)*sp+(2-t)*sm)/7
    q=7/(7+3*t)
    E=q*rho+(1-q)*np.eye(9)/9
    Esep=(6*A+t*s0+(1+2*t)*sp)/(7+3*t)
    assert np.allclose(E,Esep)
    assert np.isclose(np.trace(W@rho).real,-t/7)
    assert margin(pt(rho)) >= -1e-14
    assert margin(rho-(1-t/2)*rho0) >= -1e-14
    assert margin((1+t/3)*rho0-rho) >= -1e-14
    margins=[]
    for rank_a in [1,2,3]:
        for rank_b in [1,2,3]:
            for tiny in [1.,1e-6,1e-12]:
                def rand_filter(rank):
                    U,_=np.linalg.qr(rng.normal(size=(3,3))+1j*rng.normal(size=(3,3)))
                    V,_=np.linalg.qr(rng.normal(size=(3,3))+1j*rng.normal(size=(3,3)))
                    s=np.zeros(3)
                    s[:rank]=np.geomspace(1.,tiny,rank)
                    return U@np.diag(s)@V.conj().T
                F=np.kron(rand_filter(rank_a),rand_filter(rank_b))
                R=F@rho@F.conj().T; S=F@rho0@F.conj().T
                dist=norm1(R/np.trace(R)-S/np.trace(S))
                assert dist <= t/(1-t/2)+1e-12
                margins.append(t/(1-t/2)-dist)
                filter_checks+=1
    record={'t':t,'ppt_min_eigenvalue':margin(pt(rho)),
            'witness_expectation':float(np.trace(W@rho).real),
            'repair_decomposition_error':float(np.linalg.norm(E-Esep)),
            'filter_bound_min_slack':min(margins)}
    if t <= .2:
        rh=(1-t*t)*rho+t*t*np.eye(9)/9
        sh=(1-t*t)*rho0+t*t*np.eye(9)/9
        assert np.trace(W@rh).real<0
        assert margin(rh-(1-t/2)*sh)>=-1e-14
        assert margin((1+t/3)*sh-rh)>=-1e-14
        assert np.allclose(q*rh+(1-q)*np.eye(9)/9,(1-t*t)*E+t*t*np.eye(9)/9)
        record['full_rank_witness_expectation']=float(np.trace(W@rh).real)
        record['full_rank_theoretical_min_eigenvalue']=t*t/9
    checks.append(record)
result={'phase_decomposition_error':float(np.linalg.norm(A-(P+sp+sm)/3)),
        'local_filter_checks':filter_checks,'checks':checks,
        'scope':'Consistency checks only; the analytic proof is in FILTER_UNIFORM_APPROXIMATION_EXACTNESS_BARRIER.md.'}
out=Path(__file__).with_name('filter_uniform_exactness_barrier_verification.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
