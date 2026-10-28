#!/usr/bin/env python3
"""Actual ordinary feedback with effect-positive, nonpositive signed tag maps."""
import itertools,json
from pathlib import Path
import sympy as s
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
PS=[I,X,Y,Z]
def k(*xs):
    r=s.ones(1,1)
    for a in xs:r=s.kronecker_product(r,a)
    return r
def clean(A):return A.applyfunc(s.expand)
def ptrace_last(A,dout,dm):return s.Matrix(dout,dout,lambda i,j:sum(A[dm*i+a,dm*j+a] for a in range(dm)))
def reduce_wire(A,wire):
    if wire==0:return s.Matrix(2,2,lambda i,j:sum(A[2*i+a,2*j+a] for a in range(2)))
    return s.Matrix(2,2,lambda i,j:sum(A[2*a+i,2*a+j] for a in range(2)))
K=[s.diag(s.Rational(3,5),s.Rational(4,5)),s.Matrix([[0,s.Rational(3,5)],[s.Rational(4,5),0]])]
assert sum((A.H*A for A in K),s.zeros(2))==I
rates=[(s.Rational(1,10),s.Rational(1,5)),(s.Rational(3,10),s.Rational(2,5))]
weights=[[((p if f&2 else 1-p)*(q if f&1 else 1-q)) for f in range(4)] for p,q in rates]
patterns=[k(X if f&2 else I,Z if f&1 else I) for f in range(4)]
updates=[I,X,s.diag(1,s.I),s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])]
assert all(clean(A.H*A)==I for A in updates)
V1=(3*I-4*s.I*Y)/5
V2=clean((3*I-4*s.I*Z)*(5*I-12*s.I*X)/65)
V=k(V1,V2);assert clean(V.H*V)==s.eye(4)
generators=[k(X,I),k(Z,I),k(I,X),k(I,Z)]
def fmap(f,M):
    core=sum((weights[a][f]*updates[(f+a)%4]*K[a]*M*K[a].H*updates[(f+a)%4].H for a in range(2)),s.zeros(2))
    flag=s.zeros(4);flag[f,f]=1
    return clean(k(core,flag))
effects=[]
for f in range(4):
    # Compute directly from the error-dependent unitary Kraus, not by assertion.
    eff=sum((weights[a][f]*K[a].H*updates[(f+a)%4].H*updates[(f+a)%4]*K[a] for a in range(2)),s.zeros(2))
    target=sum((weights[a][f]*K[a].H*K[a] for a in range(2)),s.zeros(2))
    assert clean(eff)==target;effects.append(target)
assert sum(effects,s.zeros(2))==I
signs=[];bias_effects=[]
for G in generators:
    chi=[1 if P*G==G*P else -1 for P in patterns]
    assert all(P*G==z*G*P for P,z in zip(patterns,chi))
    A=sum((z*E for z,E in zip(chi,effects)),s.zeros(2))
    assert A==A.H and A[0,0]>0 and A[1,1]>0 and A.det()>0
    signs.append(chi);bias_effects.append(A)

entries=0;local_entries=0
for a,b in itertools.product(range(2),repeat=2):
    M=s.zeros(2);M[a,b]=1;fs=[fmap(f,M) for f in range(4)]
    total=sum(fs,s.zeros(8))
    unsigned=sum((k(clean(V*P*(s.eye(4)/4)*P.H*V.H),F) for P,F in zip(patterns,fs)),s.zeros(32))
    assert unsigned==k(s.eye(4)/4,total);entries+=1024
    for v,G in enumerate(generators):
        H=sum((z*F for z,F in zip(signs[v],fs)),s.zeros(8))
        actual=sum((k(clean(V*P*(G/4)*P.H*V.H),F) for P,F in zip(patterns,fs)),s.zeros(32))
        target=k(clean(V*G*V.H)/4,H)
        assert clean(actual)==clean(target);entries+=1024
        reduced=clean(ptrace_last(actual,4,8))
        theta=s.trace(bias_effects[v]*M)
        assert reduced==clean(V*G*V.H*theta/4)
        own=v//2;other=1-own
        assert clean(reduce_wire(reduced,other))==s.zeros(2)
        expected=(V1 if own==0 else V2)*([X,Z][v%2])*(V1.H if own==0 else V2.H)*theta/2
        assert clean(reduce_wire(reduced,own))==clean(expected);local_entries+=8

# Actual ordinary labels and all product-Pauli Born events, not just ideal means.
omega=s.Matrix([[s.Rational(3,5),s.I/5],[-s.I/5,s.Rational(2,5)]])
assert omega.det()>0
fs=[fmap(f,omega) for f in range(4)];probs=[s.trace(F) for F in fs]
acc=[s.zeros(4) for _ in range(5)];events=0
for axes,sgns in itertools.product(itertools.product([1,3],repeat=2),itertools.product([-1,1],repeat=2)):
    inp=k(*[(I+sgn*PS[axis])/2 for axis,sgn in zip(axes,sgns)])
    out=clean(sum((prob*V*P*inp*P.H*V.H for P,prob in zip(patterns,probs)),s.zeros(4)))
    for readaxes,bits in itertools.product(itertools.product([1,2,3],repeat=2),itertools.product([-1,1],repeat=2)):
        pi=[(I+bit*PS[axis])/2 for axis,bit in zip(readaxes,bits)]
        prob=s.expand(s.trace(k(*pi)*out));assert s.im(prob)==0 and prob>=0
        shadow=k(*[3*p-I for p in pi])
        acc[0]+=prob*shadow/(16*9)
        for wire in range(2):
            for j,axis in enumerate([1,3]):
                if axes[wire]==axis:acc[1+2*wire+j]+=2*sgns[wire]*prob*shadow/(16*9)
        events+=1
assert clean(acc[0])==s.eye(4)/4
theta=[]
for v,G in enumerate(generators):
    t=s.trace(bias_effects[v]*omega);theta.append(t)
    assert clean(acc[1+v])==clean(V*G*V.H*t/4)
    # Exact containing and padded gap values; no unknown memory-map positivity.
    assert clean((V*G*V.H)**2)==s.eye(4) and t>0

# Nonpositive signed output blocks really occur despite positive input effects.
negative_tag_traces=[]
for v in [1,2]:
    H=sum((z*F for z,F in zip(signs[v],fs)),s.zeros(8))
    f=next(i for i,z in enumerate(signs[v]) if z<0)
    tag=s.zeros(4);tag[f,f]=1
    neg=s.trace(k(I,tag)*H);assert neg<0;negative_tag_traces.append(neg)

# The relaxation cannot be transplanted to an emitted nontrivial gauge.
p=s.Rational(1,4);gauge_signed=s.diag(1-p,-p)
Delta=k(Z/2,gauge_signed);rawsign=s.diag(*[s.sign(x) for x in Delta.diagonal()])
assert s.trace(gauge_signed)==1-2*p>0 and rawsign!=k(Z,I)
out={'status':'PASS_EFFECT_POSITIVE_TAGGED_MEMORY_ACTUAL_ORDINARY_FEEDBACK_AND_GAUGE_BOUNDARY',
     'source_outcomes':0,'rng_draws':0,'physical_qubits':2,'incoming_memory_dimension':2,
     'outgoing_core_and_error_flag_dimension':8,'error_dependent_TP_updates':True,
     'complete_output_memory_entries':entries,'containing_and_disjoint_local_entries':local_entries,
     'actual_product_preparation_readout_Born_events':events,
     'positive_bias_effects':[str(A) for A in bias_effects],
     'actual_conditional_biases':[str(t) for t in theta],
     'containing_single_wire_gaps':[str(t/2) for t in theta],
     'padded_two_wire_gaps':[str(t/4) for t in theta],
     'signed_memory_map_negative_tag_traces':[str(x) for x in negative_tag_traces],
     'nontrivial_emitted_gauge_counterexample':{'positive_total_signed_effect':'1/2','raw_sign_is_true_logical_generator':False,'covered_by_relaxation':False},
     'sampled_finite_learner_or_hardware_executed':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
