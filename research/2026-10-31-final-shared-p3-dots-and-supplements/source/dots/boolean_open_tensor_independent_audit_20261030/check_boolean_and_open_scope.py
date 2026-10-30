"""Independent finite algebra diagnostics; no autonomous hardware simulation."""
import itertools, json, math
import numpy as np
rng=np.random.default_rng(20261030)

def subsets(mask):
    s=mask
    while True:
        yield s
        if not s: break
        s=(s-1)&mask

def mobius(values,n):
    out=list(values)
    for i in range(n):
        for s in range(1<<n):
            if s>>i&1: out[s]-=out[s^(1<<i)]
    return out

def poly_mul(a,b):
    out={}
    for s,c in a.items():
        for t,d in b.items(): out[s|t]=out.get(s|t,0)+c*d
    return {s:c for s,c in out.items() if c}

# Exhaustive threshold polynomials (including every Boolean input).
threshold_cases=0
for n in range(1,10):
    for d in range(1,n+1):
        vals=[int(s.bit_count()>=d) for s in range(1<<n)]
        cs=mobius(vals,n)
        exp=[0 if s.bit_count()<d else (-1)**(s.bit_count()-d)*math.comb(s.bit_count()-1,d-1) for s in range(1<<n)]
        assert cs==exp
        assert sum(abs(c) for c in cs)==sum(math.comb(n,j)*math.comb(j-1,d-1) for j in range(d,n+1))
        threshold_cases+=len(vals)

# Nonfactorized signed global superoperators: choose inclusive maps, then invert.
n=8; eps=.023
B=[]
for s in range(1<<n):
    if not s: U=np.eye(2); sign=1
    else:
        z=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)); U,_=np.linalg.qr(z)
        sign=rng.choice([-1,1])
    B.append(sign*eps**s.bit_count()*np.kron(U.conj(),U))
E=[]
full=(1<<n)-1
for s in range(1<<n):
    E.append(sum(((-1)**t.bit_count()*B[s|t] for t in subsets(full^s)),np.zeros((4,4),complex)))
reconstruction=max(float(np.linalg.norm(sum((E[r] for r in range(1<<n) if r&s==s),np.zeros((4,4),complex))-B[s])) for s in range(1<<n))
assert reconstruction<1e-12
supports=[0b00001111,0b00111100,0b11110000,0b11000011]
R0=max(sum(bool(s>>i&1) for s in supports) for i in range(n)); d=3
polys=[]; bools=[]
for j,supp in enumerate(supports):
    # Include nonmonotone exact-three predicates to test no monotonicity assumption.
    vals=[int((r&supp).bit_count()>=3) if j%2==0 else int((r&supp).bit_count()==3) for r in range(1<<n)]
    cs=mobius(vals,n); polys.append({s:c for s,c in enumerate(cs) if c}); bools.append(vals)
C=max(sum(abs(c) for c in p.values()) for p in polys)
coarse_max_res=0.; coarse_cert_max_ratio=0.; min_degree_tests=[]
for f in range(1,1<<len(supports)):
    p={0:1}
    for j in range(len(supports)):
        if f>>j&1:p=poly_mul(p,polys[j])
    actual=sum((E[r] for r in range(1<<n) if all(bools[j][r] for j in range(len(supports)) if f>>j&1)),np.zeros((4,4),complex))
    via_poly=sum((c*B[s] for s,c in p.items()),np.zeros((4,4),complex))
    coarse_max_res=max(coarse_max_res,float(np.linalg.norm(actual-via_poly)))
    assert all(s.bit_count()*R0>=d*f.bit_count() for s in p)
    cert=sum(abs(c)*eps**s.bit_count() for s,c in p.items())
    cap=(C*eps**(d/R0))**f.bit_count()
    assert cert<=cap*(1+1e-12)
    coarse_cert_max_ratio=max(coarse_cert_max_ratio,cert/cap)
assert coarse_max_res<1e-12

# Signed OR bound is sharp already for scalar multiples of the identity channel.
L=5; p=.03
or_scalar=sum(p**s.bit_count() for s in range(1,1<<L))
assert abs(or_scalar-((1+p)**L-1))<1e-14
assert or_scalar>L*p
# Overlap loss: R0 identical AND_d coarse predicates has joint mass eps^d.
d0=3; R00=2; p0=.07
assert abs((p0**(d0/R00))**R00-p0**d0)<1e-15

# Explicit factor map with arbitrary ancillary input, two open legs and
# operator-valued acausal boundary coefficients. No CP/Hermiticity assumed.
dl,da,db,de=2,2,3,2
z=rng.normal(size=(dl,dl))+1j*rng.normal(size=(dl,dl)); U,_=np.linalg.qr(z)
W=[rng.normal(size=(db,da))+1j*rng.normal(size=(db,da)) for _ in range(4)]
T=[np.kron(U,w) for w in W]
Cmat=rng.normal(size=(4,4,de,de))+1j*rng.normal(size=(4,4,de,de))
# Joint logical+ancillary input is deliberately entangled; output should equal
# (Ad_U tensor Gamma) on it, NOT in general a product state.
psi=rng.normal(size=dl*da)+1j*rng.normal(size=dl*da); psi/=np.linalg.norm(psi)
rho=np.outer(psi,psi.conj())
actual=sum((np.kron(T[a]@rho@T[b].conj().T,Cmat[a,b]) for a in range(4) for b in range(4)),np.zeros((dl*db*de,dl*db*de),complex))
expected=np.zeros_like(actual)
for i,j in itertools.product(range(dl),repeat=2):
    e=np.zeros((dl,dl),complex);e[i,j]=1
    aij=rho[i*da:(i+1)*da,j*da:(j+1)*da]
    gamma=sum((np.kron(W[a]@aij@W[b].conj().T,Cmat[a,b]) for a in range(4) for b in range(4)),np.zeros((db*de,db*de),complex))
    expected+=np.kron(U@e@U.conj().T,gamma)
open_res=float(np.linalg.norm(actual-expected)); assert open_res<1e-10

# Weaker-premise counterexamples.
# Correct for auxiliary |0> does not imply correctness with that auxiliary open.
X=np.array([[0,1],[1,0]],complex); I=np.eye(2)
F=np.kron(I,np.diag([1,0]))+np.kron(X,np.diag([0,1]))
ket0=np.array([1,0]);ket1=np.array([0,1])
assert np.allclose(F@np.kron(ket0,ket0),np.kron(ket0,ket0))
assert np.allclose(F@np.kron(ket0,ket1),np.kron(ket1,ket1))
# Same classical Z-measurement probabilities do not imply channel identity:
# complete dephasing destroys |+><+| off diagonals.
rhop=np.ones((2,2))/2; deph=np.diag(np.diag(rhop))
assert np.allclose(np.diag(rhop),np.diag(deph))
measurement_only_error=float(np.linalg.norm(rhop-deph,ord='nuc'))
# For a non-isometric reset target, a dilation stores all logical input in env;
# selecting env |0> gives a logical-input-dependent success probability.
reset_dilation=np.column_stack([np.kron(ket0,ket0),np.kron(ket0,ket1)])
p0_effect=reset_dilation.conj().T@np.kron(I,np.outer(ket0,ket0))@reset_dilation
assert np.allclose(p0_effect,np.diag([1,0]))

result={
 'scope':'Finite exact algebra diagnostics only; not a physical open-DAG or threshold proof.',
 'threshold_boolean_inputs_checked':threshold_cases,
 'global_superoperator_dimension':[4,4],
 'global_mobius_residual':reconstruction,
 'coarse_maps_checked':15,
 'coarse_min_degree':d,'coarse_overlap':R0,'coarse_coefficient_bound':C,
 'coarse_boolean_map_residual':coarse_max_res,
 'max_certified_coefficient_bound_ratio':coarse_cert_max_ratio,
 'signed_OR_value':or_scalar,'naive_probability_union_bound':L*p,
 'overlap_exponent_saturation':{'d':d0,'R0':R00,'joint':p0**d0},
 'signed_operator_valued_open_contraction_residual':open_res,
 'fixed_ancilla_counterexample':'controlled-X preserves logical input for A=0 and flips it for A=1',
 'measurement_only_counterexample_trace_distance_norm':measurement_only_error,
 'general_channel_postselection_effect':p0_effect.real.tolist()
}
print(json.dumps(result,indent=2))
