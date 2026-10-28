#!/usr/bin/env python3
"""Independent exact finite checks for the full-port CP-suffix certificate.
Different IC frame and variable stopping fixture; no author-code imports or samples.
"""
from pathlib import Path
from hashlib import sha256
from itertools import product, combinations
import json
import sympy as s
ROOT=Path(__file__).resolve().parent
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Y=s.Matrix([[0,-s.I],[s.I,0]])
Z=s.diag(1,-1); z=(I+Z)/2; n=(I-Z)/2; xp=(I+X)/2; yp=(I+Y)/2
states=[z,n,xp,yp]
effects=[r/4 for r in states]+[I-sum(states,s.zeros(2))/4]

def simp(a): return a.applyfunc(s.expand)
def tr(a): return s.expand(s.trace(a))
def en(a): return sum(abs(s.re(v))+abs(s.im(v)) for v in a)
def am(a): return a.applyfunc(abs)
def unit(d,i,j):
    a=s.zeros(d);a[i,j]=1;return a

def part(a,d):
    k=a.rows//d
    return simp(sum((a[i*k:(i+1)*k,i*k:(i+1)*k] for i in range(d)),s.zeros(k)))
def func(f,a):
    d=f.rows;k=a.rows//d
    return simp(sum((f[j,i]*a[i*k:(i+1)*k,j*k:(j+1)*k] for i,j in product(range(d),repeat=2)),s.zeros(k)))
G=s.Matrix([[tr(a*b) for b in states] for a in states])
D=[simp(sum((G.inv()[u,v]*states[v] for v in range(4)),s.zeros(2))) for u in range(4)]
B=[4*d for d in D]+[s.zeros(2)]
f=[en(d) for d in D];g=[en(b) for b in B]
for a in [unit(2,i,j) for i,j in product(range(2),repeat=2)]:
    assert sum((r*tr(d*a) for r,d in zip(states,D)),s.zeros(2))==a
    assert sum((b*tr(e*a) for b,e in zip(B,effects)),s.zeros(2))==a
assert sum(effects,s.zeros(2))==I
assert all(all(val>=0 for val in e.eigenvals()) for e in effects)
SW=s.zeros(4);CN=s.zeros(4)
for m,a in product(range(2),repeat=2):
    SW[2*a+m,2*m+a]=1
    CN[2*m+(a^m),2*m+a]=1
ports={'swap':SW,'control':CN}
assert all(u.H*u==s.eye(4) for u in ports.values())
t=s.Rational(1,10**12);tau0=z;sig0=(1-t)*z+t*n
cores={'true':[tau0,n/4,xp/4,yp/4], 'fit':[sig0,(1-t)*n/4,(1-t)*xp/4,(1-t)*yp/4]}
Fs=[I,z/4,xp/4,yp/4]

def cb(u,mem,inp,e):
    a=simp(u*s.kronecker_product(mem,inp)*u.H)
    return simp(s.Matrix([[sum(e[l,k]*a[2*i+k,2*j+l] for k,l in product(range(2),repeat=2)) for j in range(2)] for i in range(2)]))
for label,start in [('true',tau0),('fit',sig0)]:
    for j,r in enumerate([n,xp,yp],start=1): assert cb(SW,start,r,z/4)==cores[label][j]
Hs={label:s.Matrix([[tr(e*r) for r in core] for e in Fs]) for label,core in cores.items()}
assert all(h.det()!=0 for h in Hs.values())
inv={label:h.inv() for label,h in Hs.items()};mass={label:h[0,:] for label,h in Hs.items()}

def extract(a,label):
    ys=[func(e,a) for e in Fs]
    return [simp(sum((inv[label][j,i]*ys[i] for i in range(4)),s.zeros(ys[0].rows))) for j in range(4)]
def lift(xs,label):
    return simp(sum((s.kronecker_product(r,x) for r,x in zip(cores[label],xs)),s.zeros(2*xs[0].rows)))
def read(xs,row):return simp(sum((row[j]*xs[j] for j in range(4)),s.zeros(xs[0].rows)))
for label in cores:
    for i,j in product(range(2),repeat=2): assert lift(extract(unit(2,i,j),label),label)==unit(2,i,j)
Cs={};Hz={}
for label,core in cores.items():
    for name,u in ports.items():
        for a,b in product(range(4),range(5)):
            table=s.Matrix([[tr(e*cb(u,r,states[a],effects[b])) for r in core] for e in Fs])
            Hz[label,name,a,b]=table;Cs[label,name,a,b]=simp(inv[label]*table)

def step(xs,label,name):
    ys=[]
    ff={(j,a):func(D[a],xs[j]) for j,a in product(range(4),range(4))}
    for i in range(4):
        ys.append(simp(sum((Cs[label,name,a,b][i,j]*s.kronecker_product(B[b],ff[j,a])
          for j,a,b in product(range(4),range(4),range(5))),s.zeros(xs[0].rows))))
    return ys
# A positive entangled prefix with a retained qutrit reference tests amplification,
# and the first four source-to-candidate coordinate lift matrix units test non-CPness.
v=s.Matrix([1,0,0,0,1,0]);ent=v*v.H/2
omega=s.kronecker_product(tau0,ent)
post=simp(s.kronecker_product(SW,s.eye(3))*omega*s.kronecker_product(SW.H,s.eye(3)))
xx=extract(post,'true');assert lift(xx,'true')==post
neg=None
for j,x in enumerate(xx):
    for size in range(1,4):
        for inds in combinations(range(x.rows),size):
            det=s.factor(x.extract(inds,inds).det())
            if det<0:neg={'block':j,'indices':inds,'determinant':str(det)};break
        if neg:break
    if neg:break
assert neg
noncomm=any(simp(xx[i]*xx[j]-xx[j]*xx[i])!=s.zeros(xx[0].rows) for i,j in combinations(range(4),2))
assert noncomm
ref_checks=0
for label in cores:
    for name,u in ports.items():
        actual=simp(s.kronecker_product(u,s.eye(3))*post*s.kronecker_product(u.H,s.eye(3)))
        assert lift(step(extract(post,label),label,name),label)==actual;ref_checks+=1
Jl=s.zeros(4)
for i,j in product(range(2),repeat=2): Jl[2*i:2*i+2,2*j:2*j+2]=lift(extract(unit(2,i,j),'true'),'fit')
neg_lift=None
for size in range(1,5):
    for inds in combinations(range(4),size):
        det=s.factor(Jl.extract(inds,inds).det())
        if det<0:neg_lift={'indices':inds,'determinant':str(det)};break
    if neg_lift:break
assert neg_lift
# Exact synthetic bands, not confidence counts. Candidate need not be in them.
w=s.Rational(1,10**20);H=Hs['true'];DH=s.ones(4)*w;DH[0,0]=0
A=am(inv['true'])*DH
assert max(sum(A[i,j] for j in range(4)) for i in range(4))<1
M=(s.eye(4)-A).inv()*am(inv['true']);K=max(1,sum(M));res={}
for name in ports:
    for a,b in product(range(4),range(5)):
        cf=Cs['fit',name,a,b]
        E=M*(s.ones(4)*w+DH*am(cf)+am(H*cf-Hz['true',name,a,b]))
        assert all(e>=0 for e in E-am(Cs['true',name,a,b]-cf));res[name,a,b]=E
errors={name:max(sum(f[a]*g[b]*res[name,a,b][i,j] for i,a,b in product(range(4),range(4),range(5))) for j in range(4)) for name in ports}
eps=max(errors.values());dm=max(DH[0,j]+abs(mass['true'][j]-mass['fit'][j]) for j in range(4))
assert sum(en(x) for x in xx)<=K
# Actual variable-length controller: SWAP; retained two-outcome local instrument;
# outcome 1 stops, outcome 0 recycles output through CONTROL. Reference is a qubit.
bell=s.Matrix([1,0,0,1]);bell=bell*bell.H/2
Q=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
Ls=[s.diag(1,s.Rational(3,5))*Q,s.Matrix([[0,s.Rational(4,5)],[0,0]])*Q]
assert sum((L.H*L for L in Ls),s.zeros(2))==I

def caller(xs,L):
    a=s.kronecker_product(L,I);return [simp(a*x*a.H) for x in xs]
def phys(label):
    init=cores[label][0];big=s.kronecker_product(SW,I)
    om=simp(big*s.kronecker_product(init,bell)*big.H);out={}
    for r,L in enumerate(Ls):
        a=s.kronecker_product(I,L,I);p=simp(a*om*a.H)
        if r==0:
            a=s.kronecker_product(CN,I);p=simp(a*p*a.H)
        out[r]=p
    assert sum(tr(v) for v in out.values())==1
    return out

def coord(first,second):
    prefix=step([bell]+[s.zeros(4) for _ in range(3)],first,'swap');out={}
    for r,L in enumerate(Ls):
        x=caller(prefix,L)
        out[r]=step(x,second,'control') if r==0 else x
    return out
ht=coord('true','true');hf=coord('fit','fit');hm=coord('true','fit')
pt=phys('true');pf=phys('fit')
for r in [0,1]:
    assert lift(ht[r],'true')==pt[r] and lift(hf[r],'fit')==pf[r]
    insertion1=read([hm[r][j]-hf[r][j] for j in range(4)],mass['fit'])
    insertion2=read([ht[r][j]-hm[r][j] for j in range(4)],mass['fit'])
    debit=read(ht[r],mass['true']-mass['fit'])
    assert simp(insertion1+insertion2+debit)==part(pt[r],2)-part(pf[r],2)
    if r==1: assert insertion2==s.zeros(4)
expected_L=1+tr(pt[0]);assert expected_L==s.Rational(994,625)
actual_upper=sum(en(part(pt[r],2)-part(pf[r],2)) for r in [0,1])/2
eta=K*(expected_L*eps+dm)/2;assert 0<actual_upper<eta<1
mass_upper=sum(en(read(ht[r],mass['true']-mass['fit'])) for r in [0,1])/2
assert 0<mass_upper<=K*dm/2
# Independent scalar-CP / complete-port counterexample, with different frame.
pp=[[tr(e*r.T) for e in effects] for r in states]
assert all(p>=0 for row in pp for p in row) and all(sum(row)==1 for row in pp)
assert SW.eigenvals()=={1:3,-1:1}
# Direct-service Choi reconstruction orientation, independently at p=2 k=2.
U=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
JN=sum((tr(e*U*r*U.H)*s.kronecker_product(d.T,b) for r,d in zip(states,D) for e,b in zip(effects,B)),s.zeros(4))
vec=s.Matrix([U[j,i] for i,j in product(range(2),repeat=2)])
assert simp(JN)==vec*vec.H
report={
 'status':'PASS_INDEPENDENT_EXACT_COMPLETE_PORT_CP_SUFFIX_FIXTURES',
 'source_sha256':sha256((ROOT/'COMPLETE_PORT_PHYSICAL_RESIDUAL_SIMULATOR.md').read_bytes()).hexdigest(),
 'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
 'independent_code_imports_author_code':False,'IC_inputs':4,'IC_POVM_outcomes':5,
 'IC_frame_gram_determinant':str(G.det()),'H_determinant':str(H.det()),
 'raw_true_masses':[str(x) for x in mass['true']], 'raw_fit_masses':[str(x) for x in mass['fit']],
 'qutrit_reference_complete_actions':ref_checks,'nonpositive_coordinate_witness':neg,
 'noncommuting_coordinate_blocks':noncomm,'non_CP_core_lift_witness':neg_lift,
 'retained_adaptive_stop_branches':2,'maximum_native_calls':2,'true_expected_native_calls':str(expected_L),
 'exact_stopping_telescope_branches':2,'K_exact':str(K),'epsilon_exact':str(eps),'mass_debit_exact':str(dm),
 'complete_endpoint_half_trace_norm_upper':str(actual_upper),'bound_using_expected_length':str(eta),
 'strict_actual_upper_below_bound_below_one':True,'mass_term_nonzero':True,
 'transpose_nonnegative_scalar_branches':20,'transpose_TP_sums':4,'transpose_negative_Bell_eigenvalue':'-1/2',
 'direct_service_Choi_transpose_orientation_verified':True,
 'source_calls':0,'episode_starts':0,'random_draws':0,'sampled_outcomes':0,'hardware_executions':0,
 'generic_physical_fit_executed':False,'generic_QE_executed':False,'generic_decoder_SDP_executed':False,
 'compiler_or_gate_synthesis_executed':False,'floating_point_used_for_assertions':False,
 'scope':'Exact supplied finite fixtures plus separate analytic audit; not model acquisition or generic solver execution.'}
(ROOT/'complete_port_independent_suffix_check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
