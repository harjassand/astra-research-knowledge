#!/usr/bin/env python3
"""Complete coherent-feedback/common-subchannel and retained-fault checks."""
import itertools,json
from pathlib import Path
import sympy as s
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
def kron(*xs):
    r=s.ones(1,1)
    for A in xs:r=s.kronecker_product(r,A)
    return r
def clean(A):return A.applyfunc(s.expand)
def E(d,a,b):
    z=s.zeros(d);z[a,b]=1;return z
def psd2(A):
    assert A==A.H and A[0,0]>=0 and A[1,1]>=0 and A.det()>=0

# Literal normalized Bell witness for failure of constant ideal CP domination.
phi=s.Matrix([[1,0,0,1],[0,0,0,0],[0,0,0,0],[1,0,0,1]])/2
p=s.Rational(1,4);tag0=s.diag(1,0);tag1=s.diag(0,1)
badphi=kron(I,X)*phi*kron(I,X)
J=(1-p)*kron(phi,tag0)+p*kron(badphi,tag1)
Jid=kron(phi,(1-p)*tag0+p*tag1)
witness=s.trace(kron(phi,tag1)*(J-(1-p)*Jid))
assert witness==-s.Rational(3,16)

# Two modules with state-dependent coherent memory and retained error flags.
K=[s.diag(1,s.Rational(12,13)),s.Matrix([[0,s.Rational(5,13)],[0,0]])]
eta=s.Rational(25,169)
assert sum((A.H*A for A in K),s.zeros(2))==I
psd2(eta*I-K[1].H*K[1])
rot0=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
rot1=s.Matrix([[s.Rational(5,13),-s.Rational(12,13)],[s.Rational(12,13),s.Rational(5,13)]])
CN=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
controller=clean(CN*(3*s.eye(4)-4*s.I*kron(Z,I))/5)
assert clean(controller.H*controller)==s.eye(4)
real={};ideal={};mem={}
for f1,f2 in itertools.product(range(2),repeat=2):
    # The second source uses the genuinely retained first error record.
    k2=(rot0 if f1==0 else rot1)*K[f2]*(I if f1==0 else rot0)
    A=k2*K[f1];mem[f1,f2]=A
    Ureal=(kron(I,Z) if f2 else s.eye(4))*controller*(kron(X,I) if f1 else s.eye(4))
    tag=s.zeros(4,1);tag[2*f1+f2,0]=1
    real[f1,f2]=kron(kron(Ureal,A),tag)
    ideal[f1,f2]=kron(kron(controller,A),tag)
assert real[0,0]==ideal[0,0]
assert clean(sum((A.H*A for A in real.values()),s.zeros(8)))==s.eye(8)
assert clean(sum((A.H*A for A in ideal.values()),s.zeros(8)))==s.eye(8)
G=real[0,0];geffect=clean(G.H*G);c=(1-eta)**2
assert geffect==kron(s.eye(4),s.diag(1,c))
breal=clean(sum((A.H*A for f,A in real.items() if f!=(0,0)),s.zeros(8)))
bideal=clean(sum((A.H*A for f,A in ideal.items() if f!=(0,0)),s.zeros(8)))
assert breal==bideal==s.eye(8)-geffect
assert breal==kron(s.eye(4),s.diag(0,1-c))

# Check complete output matrices of both real and comparison processes after
# subtracting the SAME all-clean map, on every joint logical/memory matrix unit.
entries=0
for a,b0 in itertools.product(range(8),repeat=2):
    M=E(8,a,b0);common=G*M*G.H
    full=sum((A*M*A.H for A in real.values()),s.zeros(32))
    base=sum((A*M*A.H for A in ideal.values()),s.zeros(32))
    rb=sum((A*M*A.H for f,A in real.items() if f!=(0,0)),s.zeros(32))
    ib=sum((A*M*A.H for f,A in ideal.items() if f!=(0,0)),s.zeros(32))
    assert clean(full-common)==clean(rb) and clean(base-common)==clean(ib)
    entries+=2*32*32
# Logical Bell probes and memory |1> attain the full bound in this fixture:
# within each nonzero recorded error string the real/ideal Bell vectors are
# orthogonal, while the retained core memory update is exactly the same.
badprob=0
for f,A in mem.items():
    state=A*s.Matrix([0,1]);weight=(state.H*state)[0]
    if f!=(0,0):
        f1,f2=f;Ureal=(kron(I,Z) if f2 else s.eye(4))*controller*(kron(X,I) if f1 else s.eye(4))
        assert s.trace(Ureal.H*controller)==0
        badprob+=weight
assert badprob==1-c

# Learned gauge effects plus a native tagged error instrument: only EFFECT
# domination is used. Current alpha is retained in the outgoing memory.
b=s.Rational(1,5);plus=s.ones(2)/2
Tg=[I-b*plus,b*plus]
assert Tg[0]+Tg[1]==I
psd2(Tg[0]-(1-b)*I);psd2(Tg[1])
Gkraus=[]
for alpha in range(2):
    B=s.zeros(8,2)
    for m in range(2):B[(m*2+m)*2+alpha,m]=1
    Gkraus.append(B*K[alpha])
def contract(T,A):
    return s.Matrix(4,4,lambda u,v:sum(T[h,g]*A[4*g+u,4*h+v] for g,h in itertools.product(range(2),repeat=2)))
fhat={};total={};learned_entries=0
for a,b0 in itertools.product(range(2),repeat=2):
    M=E(2,a,b0);outs=[A*M*A.H for A in Gkraus]
    maps=[sum((contract(Tg[beta^alpha],outs[alpha]) for alpha in range(2)),s.zeros(4)) for beta in range(2)]
    target=sum((contract(I,A) for A in outs),s.zeros(4))
    assert clean(maps[0]+maps[1])==clean(target)
    fhat[a,b0]=maps;total[a,b0]=target;learned_entries+=3*16
effect=s.Matrix(2,2,lambda a,b0:s.trace(fhat[b0,a][0]))
combined_eta=b+eta-b*eta
psd2(effect-(1-b)*(1-eta)*I)
psd2(combined_eta*I-(I-effect))

# Three sequential fault locations, memory-dependent updates, all fault tags
# retained. Uniform conditional fault EFFECT, not independent error sampling.
paths={}
for f in itertools.product(range(2),repeat=3):
    A=I;history=0
    for slot,bit in enumerate(f):
        U=rot0 if (slot+history)%2==0 else rot1
        V=I if history%2==0 else rot0
        A=U*K[bit]*V*A;history=2*history+bit
    paths[f]=A
effects={f:clean(A.H*A) for f,A in paths.items()}
assert clean(sum(effects.values(),s.zeros(2)))==I
pair_effects=[]
for i,j in itertools.combinations(range(3),2):
    pair=clean(sum((A for f,A in effects.items() if f[i] and f[j]),s.zeros(2)))
    psd2(eta**2*I-pair);pair_effects.append(pair)
bad=clean(sum((A for f,A in effects.items() if sum(f)>=2),s.zeros(2)))
psd2(sum(pair_effects,s.zeros(2))-bad)
psd2(3*eta**2*I-bad)
assert any(A.trace()>0 for f,A in effects.items() if sum(f)>=2)

out={'status':'PASS_COMPLETE_COHERENT_FEEDBACK_COMMON_SUBCHANNEL_AND_TAGGED_FAULT_EFFECTS',
     'source_calls':0,'random_draws':0,
     'negative_normalized_Choi_witness':str(witness),
     'adaptive_slots':2,'input_joint_dimension':8,'output_with_retained_flags_dimension':32,
     'complete_common_subchannel_matrix_entries':entries,
     'second_source_depends_on_first_retained_error_record':True,
     'common_controller':'non-Clifford rational logical rotation followed by coherent CNOT output1 to input2',
     'one_slot_uniform_bad_effect':str(eta),'all_clean_trace_lower_bound':str(c),
     'actual_Bell_memory_input_half_distance':str(badprob),'finite_process_upper_bound':str(1-c),
     'common_clean_map_not_constant_multiple_of_total':True,
     'learned_complete_gauge_memory_map_entries':learned_entries,
     'learned_native_combined_eta':str(combined_eta),
     'three_sequential_tagged_fault_patterns':8,'specified_fault_pairs_checked':3,
     'uniform_three_fault_union_effect_bound':str(3*eta**2),
     'acquisition_or_physical_hardware_executed':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
