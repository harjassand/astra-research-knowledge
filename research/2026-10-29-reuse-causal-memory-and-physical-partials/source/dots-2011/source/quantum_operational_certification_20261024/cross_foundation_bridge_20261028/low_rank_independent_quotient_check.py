#!/usr/bin/env python3
"""Independent exact rank-three quotient fixture on qutrit memory.
No author-code imports, samples, generic rank search, QE, decoder or compiler.
"""
from pathlib import Path
from hashlib import sha256
from itertools import product
import sympy as s
import json
P=Path(__file__).resolve().parent
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
z=(I+Z)/2;n=(I-Z)/2;xp=(I+X)/2;yp=(I+Y)/2
states=[z,n,xp,yp];effects=[r/4 for r in states]+[I-sum(states,s.zeros(2))/4]
Us=[I,X,Z];U=s.diag(*Us);assert U.H*U==s.eye(6)
rho=s.ones(3)/3;t=s.Rational(1,50)
sigma=(1-t)*rho+t*s.diag(s.Rational(1,2),s.Rational(1,3),s.Rational(1,6))
assert sigma==sigma.H and s.trace(sigma)==1
assert all(v>0 for v in [sigma[:k,:k].det() for k in range(1,4)])

def clean(A):return A.applyfunc(s.expand)
def tr(A):return s.expand(s.trace(A))
def vec(A):return s.Matrix(list(A))
def en(A):return sum(abs(s.re(v))+abs(s.im(v)) for v in A)
def E(d,i,j):
    a=s.zeros(d);a[i,j]=1;return a

def f(F,A):
    d=F.rows;k=A.rows//d
    return clean(sum((F[j,i]*A[i*k:(i+1)*k,j*k:(j+1)*k] for i,j in product(range(d),repeat=2)),s.zeros(k)))
def cb(T,r,e):
    return clean(s.Matrix([[T[i,j]*tr(e*Us[i]*r*Us[j].H) for j in range(3)] for i in range(3)]))
Gram=s.Matrix([[tr(a*b) for b in states] for a in states])
D=[clean(sum((Gram.inv()[u,v]*states[v] for v in range(4)),s.zeros(2))) for u in range(4)]
B=[4*d for d in D]+[s.zeros(2)]
for i,j in product(range(2),repeat=2):
    a=E(2,i,j)
    assert sum((r*tr(d*a) for r,d in zip(states,D)),s.zeros(2))==a
    assert sum((b*tr(e*a) for b,e in zip(B,effects)),s.zeros(2))==a
assert sum(effects,s.zeros(2))==I
# Actual one-word prefixes isolate X and the I/X pair respectively.
cores={name:[initial,cb(initial,z,n/4),cb(initial,xp,xp/4)] for name,initial in [('true',rho),('fit',sigma)]}
Fs=[s.eye(3),s.diag(0,s.Rational(1,4),0),s.diag(s.Rational(1,4),s.Rational(1,4),0)]
Hs={name:s.Matrix([[tr(F*T) for T in core] for F in Fs]) for name,core in cores.items()}
assert all(H.det()!=0 for H in Hs.values())
assert Hs['true'][:2,:2].det()!=0 # An invertible smaller minor does not prove rank two.
fake_c=Hs['true'][:2,:2].inv()*Hs['true'][:2,2]
fake_null=clean(cores['true'][2]-sum((cores['true'][j]*fake_c[j] for j in range(2)),s.zeros(3)))
assert all(tr(F*fake_null)==0 for F in Fs[:2])
missing_future_signal=tr(Fs[2]*fake_null)
assert missing_future_signal!=0
assert tr(cb(fake_null,xp,xp/4))==missing_future_signal
inv={name:H.inv() for name,H in Hs.items()};mass={name:H[0,:] for name,H in Hs.items()}
Ws=[E(3,i,j) for i,j in product(range(3),repeat=2) if i!=j]
W=s.Matrix.hstack(*map(vec,Ws));assert W.rank()==6
rank={};Cs={};section_witnesses={};witness_checks=0
for name,initial in [('true',rho),('fit',sigma)]:
    reached=[initial]+[cb(initial,r,e) for r,e in product(states,effects)]
    rr=s.Matrix.hstack(*map(vec,reached)).rank()
    assert rr==9
    futures=[s.eye(3)]
    for r,e in product(states,effects):
        F=s.diag(*[tr(e*u*r*u.H) for u in Us]);futures.append(F)
    oo=s.Matrix.hstack(*map(vec,futures)).rank();assert oo==3
    rank[name]={'reachable_dimension':rr,'observable_rank':oo,'invisible_dimension':rr-oo}
    G=s.Matrix.hstack(*map(vec,cores[name]))
    assert G[:,0]==vec(initial)
    for u,v in product(range(4),range(5)):
        r,e=states[u],effects[v]
        table=s.Matrix([[tr(F*cb(T,r,e)) for T in cores[name]] for F in Fs])
        C=clean(inv[name]*table);Cs[name,u,v]=C
        residual=clean(s.Matrix.hstack(*[vec(cb(T,r,e)) for T in cores[name]])-G*C)
        # Explicit Eq. (9) witnesses, complex Liouville coordinates; no tolerance.
        Bz=s.Matrix([[residual[3*i+j,k] for k in range(3)] for i,j in product(range(3),repeat=2) if i!=j])
        assert W*Bz==residual
        images=s.Matrix.hstack(*[vec(cb(w,r,e)) for w in Ws])
        Az=s.Matrix([[images[3*i+j,k] for k in range(6)] for i,j in product(range(3),repeat=2) if i!=j])
        assert W*Az==images and all(tr(w)==0 for w in Ws)
        assert Hs[name]*C==table
        witness_checks+=1
        if residual!=s.zeros(9,3) and name not in section_witnesses:
            section_witnesses[name]={'input':u,'effect':v,'nonzero_entry':next(str(v) for v in residual if v!=0)}
    assert name in section_witnesses
assert all(Cs['true',u,v]==Cs['fit',u,v] for u,v in product(range(4),range(5)))
# Every full port input matrix entry preserves the six-dimensional invisible subspace.
full_kernel=0
for w in Ws:
    for i,j in product(range(2),repeat=2):
        a=clean(U*s.kronecker_product(w,E(2,i,j))*U.H)
        assert all(a[2*k:2*k+2,2*k:2*k+2]==s.zeros(2) for k in range(3))
        assert f(s.eye(3),a)==s.zeros(2);full_kernel+=1

def extract(A,name):
    ys=[f(F,A) for F in Fs]
    return [clean(sum((inv[name][j,i]*ys[i] for i in range(3)),s.zeros(ys[0].rows))) for j in range(3)]
def lift(xs,name):return clean(sum((s.kronecker_product(T,x) for T,x in zip(cores[name],xs)),s.zeros(3*xs[0].rows)))
def read(xs,row):return clean(sum((row[j]*xs[j] for j in range(3)),s.zeros(xs[0].rows)))
def step(xs,name):
    ff={(j,u):f(D[u],xs[j]) for j,u in product(range(3),range(4))}
    return [clean(sum((Cs[name,u,v][i,j]*s.kronecker_product(B[v],ff[j,u]) for j,u,v in product(range(3),range(4),range(5))),s.zeros(xs[0].rows))) for i in range(3)]
def physical(A):
    r=A.rows//6;a=s.kronecker_product(U,s.eye(r));return clean(a*A*a.H)
# Explicit IC identity including memory, input and qutrit reference indices.
q=s.zeros(6,1);q[0]=s.Rational(3,5);q[5]=4*s.I/5;payload=q*q.H
complete_checks=0;nonzero_kernel_insertions=0
for name,initial in [('true',rho),('fit',sigma)]:
    om=s.kronecker_product(initial,payload)
    for depth in range(2):
        xx=extract(om,name);direct=physical(om);pred=step(xx,name)
        assert pred==extract(direct,name)
        invisible=clean(direct-lift(pred,name))
        assert all(invisible[6*k:6*k+6,6*k:6*k+6]==s.zeros(6) for k in range(3))
        assert read(pred,mass[name])==f(s.eye(3),direct)
        assert f(s.eye(3),physical(invisible))==s.zeros(6)
        if invisible!=s.zeros(18):nonzero_kernel_insertions+=1
        om=direct;complete_checks+=1
assert nonzero_kernel_insertions==2 # U squared is identity, so depth two returns to the chosen initial section.
# Finite adaptive stopping with retained local record and a coherent recycled input.
b=s.Matrix([1,0,0,1]);bell=b*b.H/2
Q=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
Ls=[s.diag(1,s.Rational(3,5))*Q,s.Matrix([[0,s.Rational(4,5)],[0,0]])*Q]
assert sum((L.H*L for L in Ls),s.zeros(2))==I
end={};coord={}
for name,initial in [('true',rho),('fit',sigma)]:
    om=physical(s.kronecker_product(initial,bell));xs=step([bell,s.zeros(4),s.zeros(4)],name)
    end[name]={};coord[name]={}
    for record,L in enumerate(Ls):
        a=s.kronecker_product(s.eye(3),L,I);c=s.kronecker_product(L,I)
        yy=clean(a*om*a.H);cc=[clean(c*x*c.H) for x in xs]
        if record==0:yy=physical(yy);cc=step(cc,name)
        assert cc==extract(yy,name) and read(cc,mass[name])==f(s.eye(3),yy)
        end[name][record]=f(s.eye(3),yy);coord[name][record]=cc
    assert sum(tr(a) for a in end[name].values())==1
for record in range(2):
    assert coord['true'][record]==coord['fit'][record]
    assert end['true'][record]-end['fit'][record]==read(coord['true'][record],mass['true']-mass['fit'])
K=sum(abs(v) for v in inv['true']);dm=max(abs(v) for v in mass['true']-mass['fit']);eta=K*dm/2
upper=sum(en(end['true'][r]-end['fit'][r]) for r in range(2))/2
assert 0<upper<eta<1
one_diff=f(s.eye(3),physical(s.kronecker_product(rho-sigma,bell)))
bell_distance=sum(abs(v)*multiplicity for v,multiplicity in one_diff.eigenvals().items())/2
assert bell_distance==s.Rational(1,300)
report={
 'status':'PASS_INDEPENDENT_EXACT_LOW_RANK_QUOTIENT_CERTIFICATES',
 'source_sha256':sha256((P/'LOW_RANK_COMPLETE_QUOTIENT_CP_SUFFIX.md').read_bytes()).hexdigest(),
 'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
 'independent_code_imports_author_code':False,'memory_dimension':3,'observable_rank':3,
 'input_settings':4,'output_POVM_outcomes':5,'source_candidate_exact_rank_data':rank,
 'kernel_witness_columns':6,'exact_candidate_source_witness_checks':witness_checks,
 'full_input_matrix_kernel_invariance_checks':full_kernel,
 'source_H':[[str(v) for v in Hs['true'].row(i)] for i in range(3)],
 'source_H_determinant':str(Hs['true'].det()),'smaller_invertible_minor_does_not_certify_rank':True,
 'omitted_future_detects_fake_rank_two_kernel':str(missing_future_signal),
 'raw_prefix_and_future_max_depth':1,'example_shifted_pool_depth':3,'theorem_bound_2r_minus_1':5,
 'noninvariant_source_and_candidate_sections':section_witnesses,
 'qutrit_reference_complete_transfer_checks':complete_checks,'nonzero_invisible_insertions':nonzero_kernel_insertions,
 'retained_adaptive_stop_branches':2,'true_expected_native_calls':str(1+tr(end['true'][0])),
 'native_coordinate_residual':'0','K':str(K),'mass_debit':str(dm),'eta':str(eta),
 'adaptive_endpoint_half_trace_norm_upper':str(upper),'single_Bell_half_trace_distance_exact':str(bell_distance),
 'rank_inferred_from_counts':False,'source_calls':0,'episode_starts':0,'random_draws':0,'sampled_outcomes':0,
 'hardware_executions':0,'generic_physical_fit_executed':False,'generic_QE_executed':False,
 'generic_decoder_SDP_executed':False,'compiler_executed':False,'floating_point_used':False}
(P/'low_rank_independent_quotient_check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
