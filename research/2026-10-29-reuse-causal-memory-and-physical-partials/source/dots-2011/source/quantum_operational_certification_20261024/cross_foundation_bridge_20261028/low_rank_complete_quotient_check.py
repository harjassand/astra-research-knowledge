#!/usr/bin/env python3
"""Exact architectural rank/complete-kernel diagnostics; no acquisition or fit."""
from pathlib import Path
from hashlib import sha256
from itertools import product
import json
import sympy as s
HERE=Path(__file__).resolve().parent
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
zero=(I+Z)/2;plus=(I+X)/2
states=[(I+sign*P)/2 for P in [X,Y,Z] for sign in [1,-1]]
effects=[R/3 for R in states]
D=[I/6+sign*P/2 for P in [X,Y,Z] for sign in [1,-1]]
B=[3*A for A in D]
U=s.diag(1,1,1,-1)
rhot=plus
rhof=s.Matrix([[s.Rational(51,100),s.I/5],[-s.I/5,s.Rational(49,100)]])
assert rhof.det()>0 and s.trace(rhof)==1 and U.conjugate().T*U==s.eye(4)
def clean(A):return A.applyfunc(s.expand)
def tr(A):return s.expand(s.trace(A))
def vec(A):return s.Matrix(list(A))
def en(A):return sum(abs(s.re(x))+abs(s.im(x)) for x in A)
def unit(a,b):
    E=s.zeros(2);E[a,b]=1;return E
def induce(T,rho,E):
    W=U*s.kronecker_product(T,rho)*U
    return clean(s.Matrix([[sum(E[c,b]*W[2*m+b,2*n+c] for b,c in product(range(2),repeat=2))
                           for n in range(2)] for m in range(2)]))
def functional(F,A):
    n=A.rows//2
    return clean(sum((F[b,a]*A[a*n:(a+1)*n,b*n:(b+1)*n]
                     for a,b in product(range(2),repeat=2)),s.zeros(n)))
def traceM(A):return functional(I,A)
Fs=[I,zero/3]
cores={'true':[rhot,zero/6],'fit':[rhof,s.Rational(17,100)*zero]}
Hs={name:s.Matrix([[tr(F*T) for T in core] for F in Fs]) for name,core in cores.items()}
assert Hs['true']==s.Matrix([[1,s.Rational(1,6)],[s.Rational(1,6),s.Rational(1,18)]])
inv={name:H.inv() for name,H in Hs.items()}
ms={name:H[0,:] for name,H in Hs.items()}
assert sum(abs(x) for x in inv['true'])==50
for name,initial in [('true',rhot),('fit',rhof)]:
    assert induce(initial,plus,plus/3)==cores[name][1]

# Complete IC branch reachable span is 4, future span is 2; invariance makes these exact ranks.
rank_data={};Cs={};physical_section_failures={}
for name,initial in [('true',rhot),('fit',rhof)]:
    reached=[initial]+[induce(initial,rho,E) for rho,E in product(states,effects)]
    rr=s.Matrix.hstack(*[vec(A) for A in reached]).rank();assert rr==4
    futures=[]
    for rho,E in product(states,effects):
        # Dual effect by pairing all matrix units: F[b,a]=Tr Phi(E_ab).
        F=s.Matrix([[tr(induce(unit(b,a),rho,E)) for b in range(2)] for a in range(2)])
        assert F[0,1]==F[1,0]==0
        futures.append(F)
    oo=s.Matrix.hstack(*[vec(A) for A in [I]+futures]).rank();assert oo==2
    for rho,E,K in product(states,effects,[X,Y]):
        A=induce(K,rho,E)
        assert A[0,0]==A[1,1]==0 and tr(A)==0
    for u,v in product(range(6),repeat=2):
        Hz=s.Matrix([[tr(F*induce(T,states[u],effects[v])) for T in cores[name]] for F in Fs])
        C=clean(inv[name]*Hz);Cs[(name,u,v)]=C
        a0=tr(effects[v]*states[u]);a1=tr(effects[v]*Z*states[u]*Z)
        assert C==s.Matrix([[a1,0],[3*(a0-a1),a0]])
    # input +X, output -X: section error is nonzero but entirely invisible.
    direct=induce(initial,states[0],effects[1])
    c=Cs[(name,0,1)][:,0]
    representative=clean(sum((cores[name][j]*c[j] for j in range(2)),s.zeros(2)))
    residual=clean(direct-representative)
    assert residual!=s.zeros(2) and residual[0,0]==residual[1,1]==0
    physical_section_failures[name]=[[str(x) for x in residual.row(j)] for j in range(2)]
    rank_data[name]={'reachable_dimension':rr,'observable_dimension':oo,'invisible_dimension':rr-oo}
assert all(Cs[('true',u,v)]==Cs[('fit',u,v)] for u,v in product(range(6),repeat=2))

# Kernel invariance under full input/output matrix-element maps, not just scalars.
full_kernel_checks=0
for K in [X,Y]:
    for a,b in product(range(2),repeat=2):
        A=clean(U*s.kronecker_product(K,unit(a,b))*U)
        assert A[:2,:2]==s.zeros(2) and A[2:,2:]==s.zeros(2)
        full_kernel_checks+=1

def extract(A,name):
    ys=[functional(F,A) for F in Fs]
    return [clean(sum((inv[name][j,i]*ys[i] for i in range(2)),s.zeros(ys[0].rows))) for j in range(2)]
def lift(xs,name):
    return clean(sum((s.kronecker_product(cores[name][j],xs[j]) for j in range(2)),s.zeros(2*xs[0].rows)))
def readout(xs,name):return clean(sum((ms[name][j]*xs[j] for j in range(2)),s.zeros(xs[0].rows)))
blocks={(name,i,j,u):clean(sum((Cs[(name,u,v)][i,j]*B[v] for v in range(6)),s.zeros(2)))
        for name,i,j,u in product(['true','fit'],range(2),range(2),range(6))}
def coordinate_step(xs,name):
    partials={(j,u):functional(D[u],xs[j]) for j,u in product(range(2),range(6))}
    return [clean(sum((s.kronecker_product(blocks[(name,i,j,u)],partials[(j,u)])
                      for j,u in product(range(2),range(6))),s.zeros(xs[0].rows))) for i in range(2)]
def physical_step(A):
    n=A.rows//4;W=s.kronecker_product(U,s.eye(n))
    return clean(W*A*W)
# Ancilla dimension 3: initial input/reference has non-real phase and unequal amplitudes.
z=s.zeros(6,1);z[0]=s.Rational(3,5);z[5]=4*s.I/5
payload=z*z.conjugate().T
complete_checks=0
for name,initial in [('true',rhot),('fit',rhof)]:
    Omega=s.kronecker_product(initial,payload)
    for depth in range(1,4):
        xx=extract(Omega,name)
        direct=physical_step(Omega);pred=coordinate_step(xx,name)
        assert pred==extract(direct,name)
        invisible=clean(direct-lift(pred,name))
        assert invisible[:6,:6]==s.zeros(6) and invisible[6:,6:]==s.zeros(6)
        assert traceM(invisible)==s.zeros(6)
        assert readout(pred,name)==traceM(direct)
        assert en(traceM(physical_step(invisible)))==0
        Omega=direct;complete_checks+=1

# A two-call adaptive-stopping caller retaining a Bell reference and all branch records.
bell=s.Matrix([1,0,0,1]);Bell=bell*bell.T/2
L0=s.diag(1,s.Rational(4,5));L1=s.Matrix([[0,s.Rational(3,5)],[0,0]])
Q=s.Matrix([[s.Rational(3,5),-4*s.I/5],[s.Rational(4,5),3*s.I/5]])
assert L0.conjugate().T*L0+L1.conjugate().T*L1==I and Q.conjugate().T*Q==I
ends={};coord_ends={}
for name,initial in [('true',rhot),('fit',rhof)]:
    Omega=physical_step(s.kronecker_product(initial,Bell))
    xx=coordinate_step([Bell,s.zeros(4)],name)
    ends[name]={};coord_ends[name]={}
    for record,L in enumerate([L0,L1]):
        A=s.kronecker_product(I,L,I);R=s.kronecker_product(L,I)
        phys=clean(A*Omega*A.conjugate().T)
        coords=[clean(R*x*R.conjugate().T) for x in xx]
        if record==0:
            A=s.kronecker_product(I,Q,I);R=s.kronecker_product(Q,I)
            phys=physical_step(clean(A*phys*A.conjugate().T))
            coords=coordinate_step([clean(R*x*R.conjugate().T) for x in coords],name)
        assert extract(phys,name)==coords and traceM(phys)==readout(coords,name)
        ends[name][record]=traceM(phys);coord_ends[name][record]=coords
    assert sum(tr(A) for A in ends[name].values())==1
E_length=1+tr(ends['true'][0]);assert E_length==s.Rational(91,50)
# Identical quotient maps mean every complete endpoint difference is exactly the terminal mass term.
for record in range(2):
    assert coord_ends['true'][record]==coord_ends['fit'][record]
    xs=coord_ends['true'][record]
    mass=clean(sum(((ms['true'][j]-ms['fit'][j])*xs[j] for j in range(2)),s.zeros(4)))
    assert mass==clean(ends['true'][record]-ends['fit'][record])
delta_m=max(abs(x) for x in ms['true']-ms['fit']);assert delta_m==s.Rational(1,300)
eta=50*delta_m/2;assert eta==s.Rational(1,12)
endpoint_upper=sum(en(ends['true'][r]-ends['fit'][r]) for r in range(2))/2
assert 0<endpoint_upper<eta
# One Bell probe exactly attains the pointer-weight difference 1/100.
one_true=traceM(physical_step(s.kronecker_product(rhot,Bell)))
one_fit=traceM(physical_step(s.kronecker_product(rhof,Bell)))
DD=clean(one_true-one_fit)
exact_D=sum(abs(v)*mult for v,mult in DD.eigenvals().items())/2
assert exact_D==s.Rational(1,100)
# Complete conditional-pointer channel decomposition holds on every input matrix unit.
p_true=s.Rational(1,2);p_fit=s.Rational(51,100)
for initial,p in [(rhot,p_true),(rhof,p_fit)]:
    for a,b in product(range(2),repeat=2):
        expected=p*unit(a,b)+(1-p)*Z*unit(a,b)*Z
        assert traceM(U*s.kronecker_product(initial,unit(a,b))*U)==expected

out={'status':'PASS exact author low-rank complete-quotient diagnostics',
 'source_sha256':sha256((HERE/'LOW_RANK_COMPLETE_QUOTIENT_CP_SUFFIX.md').read_bytes()).hexdigest(),
 'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
 'source_candidate_rank_certificates':rank_data,'memory_dimension':2,'observable_rank':2,
 'IC_scalar_maps_per_model':36,'identical_quotient_map_checks':36,
 'source_H':[[str(x) for x in Hs['true'].row(i)] for i in range(2)],
 'fit_H':[[str(x) for x in Hs['fit'].row(i)] for i in range(2)],
 'noninvariant_physical_section_residuals':physical_section_failures,
 'full_input_matrix_kernel_invariance_checks':full_kernel_checks,
 'qutrit_reference_complete_quotient_checks':complete_checks,
 'retained_record_adaptive_stopping_branches':2,'expected_native_calls':str(E_length),
 'native_coefficient_residual':'0','K_core':'50','mass_row_difference':str(delta_m),'certificate_eta':str(eta),
 'adaptive_endpoint_half_trace_norm_certified_upper':str(endpoint_upper),
 'single_Bell_endpoint_half_trace_distance_exact':str(exact_D),
 'rank_inferred_from_samples':False,'source_calls':0,'episode_starts':0,'RNG_calls':0,'hardware_executions':0,
 'generic_physical_search_executed':False,'generic_QE_executed':False,'decoder_SDP_executed':False,
 'compiler_executed':False,'floating_point_used':False}
(HERE/'low_rank_complete_quotient_check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
