"""Explicit broadcaster calibrations and growing tensor rounding checks."""
from pathlib import Path
import json
import math
import numpy as np
from detailed_balance_sdp import basis, hs_matrix, solve_rounding, petz_correct, ptrace, trnorm

rng=np.random.default_rng(7107609)
records=[]
for d in (2,3,4):
    fs=basis(d)
    swap=np.zeros((d*d,d*d),complex)
    for i in range(d):
        for j in range(d): swap[i*d+j,j*d+i]=1
    sym=(np.eye(d*d)+swap)/2
    def joint(x): return (2/(d+1))*sym@np.kron(x,np.eye(d))@sym
    def marginal(x): return ptrace(joint(x),d,0)
    sm=hs_matrix(marginal,fs)
    eta=(d+2)/(2*(d+1))
    assert np.max(np.abs(sm-np.diag([1]+[eta]*(d*d-1))))<1e-10
    for kind,mat in [('raw',sm),('petz',petz_correct(marginal,d,fs))]:
        # At d=4 this is only a PPT feasibility diagnostic; the exact
        # depolarizing c=2 statement is proved separately by Haar estimation.
        result={'kind':'universal_'+kind,'d':d,'eta':eta,
                'rounding':solve_rounding(mat,fs,positive=True)}
        records.append(result); print(json.dumps(result),flush=True)

v0=np.array([[1,0],[0,1/math.sqrt(2)],[0,1/math.sqrt(2)],[0,0]],complex)
x=np.array([[0,1],[1,0]],complex)
v1=np.kron(x,x)@v0@x
def plane_joint(z): return (v0@z@v0.conj().T+v1@z@v1.conj().T)/2
def plane_marginal(z): return ptrace(plane_joint(z),2,0)
fs=basis(2)
plane=hs_matrix(plane_marginal,fs)
for kind,mat in [('raw',plane),('petz',petz_correct(plane_marginal,2,fs))]:
    result={'kind':'plane_'+kind,'d':2,'spectrum':np.linalg.eigvalsh(mat).tolist(),
            'rounding':solve_rounding(mat,fs,positive=True)}
    records.append(result); print(json.dumps(result),flush=True)

# Scalar eigenvalue inequality for tensor products of known compatible factors.
factors=[np.array([1,2/3,2/3,2/3]),
         np.array([1,1/math.sqrt(2),1/math.sqrt(2),.5]),
         np.array([1,1-2e-8,0,0]),
         np.array([1,.999,0,0]),
         np.array([1,.2,.2,.2])]
tensor=[]
for count in range(1,8):
    lam=np.array([1.]);mu=np.array([1.])
    for j in range(count):
        q=factors[j%len(factors)]
        z=np.maximum(0,2*q-1)
        assert abs(z[0]-1)<1e-12 and sum(z[1:])<=1+1e-12
        lam=np.kron(lam,q);mu=np.kron(mu,z)
    slack=2*(1-lam)-(1-mu)
    assert min(slack)>-1e-12
    tensor.append({'qubits':count,'hilbert_dimension':2**count,
                   'superoperator_eigenvalue_count':len(lam),'min_majorization_slack':float(min(slack))})

# Actual three-qubit arbitrary bounded likelihood fixtures in the diagonal
# tensor basis; each factor's EB property is explicit in the symbolic report.
paulis=[np.eye(2),np.array([[0,1],[1,0]],complex),
        np.array([[0,-1j],[1j,0]],complex),np.diag([1,-1])]
ops=[np.kron(np.kron(a,b),c) for a in paulis for b in paulis for c in paulis]
lam=np.kron(np.kron(factors[0],factors[1]),factors[2])
mu=np.kron(np.kron(np.maximum(0,2*factors[0]-1),np.maximum(0,2*factors[1]-1)),
           np.maximum(0,2*factors[2]-1))
d=8
def spectral_apply(z,eigen): return sum(np.trace(a@z)*l*a/d for a,l in zip(ops,eigen))
state_checks=[]
for trial in range(40):
    raw=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
    h=(raw+raw.conj().T)/2;h-=np.trace(h).real*np.eye(d)/d
    h*=.5/np.linalg.norm(h,2)
    rho=(np.eye(d)+h)/d
    r=trnorm(spectral_apply(rho,lam)-rho)
    err=trnorm(spectral_apply(rho,mu)-rho)/2
    bound=math.sqrt(2*.5*r)/2
    assert err<=bound+1e-12
    state_checks.append({'trial':trial,'residual':r,'eb_error':err,'bound':bound})

result={'calibrations':records,'tensor_checks':tensor,'state_checks':state_checks,
        'limitation':'General d>2 PPT feasibility is not an EB certificate; depolarizing and tensor EB channels here also have independent explicit constructions.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'tensor_checks':len(tensor),'bounded_state_fixtures':len(state_checks)}))
