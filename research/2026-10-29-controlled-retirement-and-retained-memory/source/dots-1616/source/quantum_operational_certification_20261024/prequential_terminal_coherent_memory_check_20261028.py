"""Exact finite CP-memory diagnostics, not sampled source acquisition.

Checks the NEW prequential candidate's physical record law, conditional gradient,
six-state/Bell conversion, and terminal-channel splicing. No RNG is used. The
adaptive two-decoder fixture is deliberately not advertised as an OGD pilot.
"""
import hashlib
import itertools
import json
from pathlib import Path
import sympy as s

I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Y=s.Matrix([[0,-s.I],[s.I,0]])
Z=s.diag(1,-1); H=s.Matrix([[1,1],[1,-1]])/s.sqrt(2); S=s.diag(1,s.I)
PAULI=[I,X,Y,Z]; AXES=[X,Y,Z]
zero=s.diag(1,0)
phi=s.Matrix([1,0,0,1])/s.sqrt(2); PHI=phi*phi.H

def kron(*xs):
    return s.kronecker_product(*xs)

def ptr(r,n,keep):
    keep=tuple(keep); gone=tuple(i for i in range(n) if i not in keep)
    out=s.zeros(2**len(keep))
    for a in itertools.product(range(2),repeat=len(keep)):
      for b in itertools.product(range(2),repeat=len(keep)):
        v=0
        for c in itertools.product(range(2),repeat=len(gone)):
          aa=[0]*n; bb=[0]*n
          for j,i in enumerate(keep): aa[i]=a[j]; bb[i]=b[j]
          for j,i in enumerate(gone): aa[i]=bb[i]=c[j]
          ai=sum(x*2**(n-1-i) for i,x in enumerate(aa))
          bi=sum(x*2**(n-1-i) for i,x in enumerate(bb))
          v+=r[ai,bi]
        aidx=sum(x*2**(len(a)-1-i) for i,x in enumerate(a))
        bidx=sum(x*2**(len(b)-1-i) for i,x in enumerate(b))
        out[aidx,bidx]=s.simplify(v)
    return out

def cnot(n,c,t):
    u=s.zeros(2**n)
    for x in range(2**n):
        y=x ^ ((1<<(n-1-t)) if x&(1<<(n-1-c)) else 0)
        u[y,x]=1
    return u

# Source first emits a gauge entangled with retained M, then applies one fixed
# complex hidden U to L,G. All logical Pauli noise is identity.
U=kron(S,I)*cnot(2,1,0)
V=cnot(3,1,2)*kron(I,H,I)
A=kron(U,I)*V
sigma=(I+Y)/2
assert A.H*A==s.eye(8)

def joint_source(r,m):
    return s.simplify(A*kron(r,zero,m)*A.H)

def channel(r,m):
    return ptr(joint_source(r,m),3,(0,1))

def bell_joint(m):
    B=kron(I,A)
    return s.simplify(B*kron(PHI,zero,m)*B.H)

def decode(r,Vd):
    return ptr(s.simplify(Vd*r*Vd.H),2,(0,))

def bell_decoded(m,Vd):
    B=kron(I,Vd,I)
    return ptr(s.simplify(B*bell_joint(m)*B.H),4,(0,1))

def choi(Vd):
    out=s.zeros(8)
    for a in range(4):
      for b in range(4):
        e=s.zeros(4); e[a,b]=1
        out+=kron(decode(e,Vd),e)/4
    return s.simplify(out)

decoders=[s.eye(4),kron(X,I),U.H]
Js=[choi(v) for v in decoders]
assert all(ptr(j,3,(1,2))==s.eye(4)/4 for j in Js)

words=[kron(a,b) for a in PAULI for b in PAULI]
branches=[]; post_by_b={-1:s.zeros(2),1:s.zeros(2)}
for ji,P in enumerate(AXES):
  for sign in (-1,1):
    rho=joint_source((I+sign*P)/2,sigma)
    for wi,W in enumerate(words):
      for b in (-1,1):
        eff=(s.eye(4)+b*W)/2
        post=ptr(kron(eff,I)*rho,3,(2,))/96
        prob=s.simplify(s.trace(post))
        assert prob>=0
        if prob:
            assert post==post.H and s.simplify(post.det())>=0
            branches.append((ji,sign,wi,b,post))
            post_by_b[b]+=post
assert s.simplify(sum(s.trace(z[-1]) for z in branches))==1

# Actual local product measurements, with individual outcomes discarded, induce
# the same memory instrument as the parity effect AFTER the output is discarded.
local_instrument_checks=0
rho=joint_source((I+X)/2,sigma)
for aidx in range(4):
 for bidx in range(4):
  W=kron(PAULI[aidx],PAULI[bidx])
  for parity in (-1,1):
   actual=s.zeros(2)
   for aout in ((1,) if aidx==0 else (-1,1)):
    for bout in ((1,) if bidx==0 else (-1,1)):
     if aout*bout!=parity: continue
     ea=I if aidx==0 else (I+aout*PAULI[aidx])/2
     eb=I if bidx==0 else (I+bout*PAULI[bidx])/2
     E=kron(ea,eb,I)
     actual+=ptr(E*rho*E,3,(2,))
   coarse=ptr(kron((s.eye(4)+parity*W)/2,I)*rho,3,(2,))
   assert s.simplify(actual-coarse)==s.zeros(2)
   local_instrument_checks+=1

unique=[]
for *_,post in branches:
    m=s.simplify(post/s.trace(post))
    if m not in unique: unique.append(m)
noncommuting=next((a,b) for a in unique for b in unique if a*b!=b*a)
assert noncommuting

gradient_checks=0; conversion_checks=0
for m in [sigma]+unique[:5]:
    empirical=s.zeros(8); exact=s.zeros(8); losses=[]
    for P in AXES:
      for sign in (-1,1):
        r=channel((I+sign*P)/2,m)
        exact-=s.Rational(1,3)*sign*kron(P,r.T)
        for W in words:
            # Sum of the TWO integer-outcome probabilities is performed exactly.
            for b in (-1,1):
                prob=(1+b*s.trace(W*r))/2
                g=-8*sign*b*kron(P,W.T)
                empirical+=prob*g/96
                assert s.trace(g.H*g)==512
    assert s.simplify(empirical-exact)==s.zeros(8)
    gradient_checks+=1
    for Vd,J in zip(decoders,Js):
        p=0
        for P in AXES:
          for sign in (-1,1):
            r=decode(channel((I+sign*P)/2,m),Vd)
            p+=(1-sign*s.trace(P*r))/12
        ell=1-s.trace(PHI*bell_decoded(m,Vd))
        assert s.simplify(p-s.Rational(2,3)*ell)==0
        assert s.simplify(p-(s.Rational(1,2)+s.trace(exact*J)))==0
        losses.append(s.simplify(ell)); conversion_checks+=1
    assert losses[-1]==0

# Two-slot adaptive terminal policy: D1=discard gauge; D2=X^[(b+1)/2] then
# discard gauge, where b is the actually acquired first parity. This checks an
# adaptive policy, not an OGD implementation and not a count-acquisition claim.
first=bell_decoded(sigma,decoders[0])
direct_second=s.zeros(4)
conditional_second=s.zeros(4)
for ji,sign,wi,b,post in branches:
    vd=decoders[1] if b==1 else decoders[0]
    prob=s.trace(post)
    direct_second+=bell_decoded(post,vd)
    conditional_second+=prob*bell_decoded(post/prob,vd)
assert s.simplify(direct_second-conditional_second)==s.zeros(4)
direct=(first+direct_second)/2
conditional=(first+conditional_second)/2
assert direct==conditional and s.trace(direct)==1 and direct==direct.H
assert all(v>=0 for v in direct.eigenvals())
ell=s.simplify(1-s.trace(PHI*direct))
occupation=(1-s.trace(PHI*first)+1-s.trace(PHI*conditional_second))/2
assert s.simplify(ell-occupation)==0

# The deterministic-cutoff obstruction has orthogonal Bell errors at a shared
# pure gauge. Their equal mixture is separable (qubit Bell diagonal max=1/2).
PHIX=kron(I,X)*PHI*kron(I,X)
timer_mix=(PHI+PHIX)/2
assert sorted(timer_mix.eigenvals().keys())==[0,s.Rational(1,2)]

path=Path(__file__)
result={
 "status":"PASS_EXACT_DIAGNOSTICS_NOT_AN_OGD_PILOT",
 "source_calls":0,"rng_draws":0,
 "arithmetic":"exact SymPy rational/complex matrices; no floating tolerances",
 "physical_output_qubits":2,"logical_qubits":1,"retained_memory_qubits":1,
 "positive_probe_instrument_branches":len(branches),
 "distinct_conditional_memory_states":len(unique),
 "noncommuting_conditional_memories":[str(z) for z in noncommuting],
 "local_record_parity_instrument_checks":local_instrument_checks,
 "conditional_gradient_checks":gradient_checks,
 "six_state_bell_and_choi_checks":conversion_checks,
 "gradient_frobenius_norm_squared":"512 = d^5/2 at d=4",
 "adaptive_two_slot_bell_loss":str(ell),
 "terminal_channnel_identity":"exact with complete Bell reference",
 "oracle_loss":"0 for the fixed hidden U inverse decoder at every tested memory",
 "timer_obstruction_equal_mixture_eigenvalues":["1/2","1/2","0","0"],
 "scope":"finite algebraic fixture; not proof of all processes, not sampled acquisition, not a performance pilot",
 "script_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
}
out=path.with_suffix('.json'); out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
