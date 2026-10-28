"""Independent algebra/numerical checks for private framed recovery.
No collective quantum circuit is executed, no numerical SDP optimality is assumed.
"""
from pathlib import Path
import json
import numpy as np
import sympy as sp

ROOT=Path(__file__).parent
rng=np.random.default_rng(202610271929)
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1.,-1.]).astype(complex)
P=[I,X,Y,Z]

def kraus(di,do,r):
    a=rng.normal(size=(do*r,di))+1j*rng.normal(size=(do*r,di))
    q,_=np.linalg.qr(a)
    return list(q.reshape(r,do,di))

def choi(ks):
    # Input first, output second; vec(K) = K.T.reshape(-1).
    return sum(np.outer(k.T.reshape(-1), k.T.reshape(-1).conj()) for k in ks)

def hcost(ks):
    d=ks[0].shape[1]
    return sum(np.outer(k.conj().reshape(-1),k.reshape(-1)) for k in ks)/d**2

def fe(e,ds):
    d=e[0].shape[1]
    return sum(abs(np.trace(l@k))**2 for l in ds for k in e)/d**2

def channel_matrix(ks):
    d=ks[0].shape[1]
    out=[]
    for a in range(d):
        for b in range(d):
            e=np.zeros((d,d),complex); e[a,b]=1
            out.append(sum(k@e@k.conj().T for k in ks).reshape(-1))
    return np.array(out).T

errs=[]
key_inv=[]
twirl_diag=[]
for output_dim in [2,3,4]:
  for _ in range(10):
    e=kraus(2,output_dim,3)
    d=kraus(output_dim,2,output_dim)
    h=hcost(e); c=choi(d)
    errs.append(abs(np.trace(h@c).real-fe(e,d)))
    errs.append(abs(np.trace(h).real-.5))
    errs.append(np.linalg.norm(sum(l.conj().T@l for l in d)-np.eye(output_dim)))
    for p in P:
        rotated=[p.conj().T@l@k@p for l in d for k in e]
        key_inv.append(abs(fe([I],rotated)-fe(e,d)))
    twirled=[p.conj().T@l@k@p/2 for p in P for l in d for k in e]
    j=choi(twirled)/2
    bell=np.array([p.T.reshape(-1)/np.sqrt(2) for p in P]).T
    bj=bell.conj().T@j@bell
    twirl_diag.append(np.linalg.norm(bj-np.diag(np.diag(bj))))
    errs.append(abs(bj[0,0].real-fe(e,d)))
    # Bell-test trace norm equals 2(1-Fe), and triangle upper bound matches.
    phi=np.outer(bell[:,0],bell[:,0].conj())
    errs.append(abs(np.linalg.eigvalsh(j-phi).sum()))
    errs.append(abs(np.sum(abs(np.linalg.eigvalsh(j-phi)))-2*(1-fe(e,d))))

# Exact rational Pauli primal/dual optimality certificates, including tensors.
spI=sp.eye(2)
spP=[spI,sp.Matrix([[0,1],[1,0]]),sp.Matrix([[0,-sp.I],[sp.I,0]]),sp.diag(1,-1)]
probabilities=[list(map(sp.Rational,['1/2','1/4','1/8','1/8'])),
               list(map(sp.Rational,['1/10','1/5','3/5','1/10'])),
               [sp.Rational(1,4)]*4]
certs=[]
for probs in probabilities:
    h=sp.zeros(4)
    for p,v in zip(probs,spP):
        w=sp.Matrix([sp.conjugate(v[i,j]) for i in range(2) for j in range(2)])
        h+=p*w*w.conjugate().T/4
    jmax=max(range(4),key=lambda i:probs[i])
    l=spP[jmax].conjugate().T
    v=sp.Matrix([l[a,b] for b in range(2) for a in range(2)])
    c=v*v.conjugate().T
    y=probs[jmax]*spI/2
    slack=sp.kronecker_product(y,spI)-h
    assert all(e>=0 for e in slack.eigenvals())
    objective=sp.simplify(sp.trace(h*c))
    assert objective==sp.trace(y)==max(probs)
    certs.append({'probabilities':list(map(str,probs)),'fopt_exact':str(objective),
                  'dual_eigenvalues':list(map(str,slack.eigenvals()))})
    # Tensor product ordering here is (B1,A1,B2,A2), permutation immaterial.
    for m in [2,3]:
        hh=h; cc=c; yy=sp.kronecker_product(y,spI)
        for _ in range(m-1):
            hh=sp.kronecker_product(hh,h)
            cc=sp.kronecker_product(cc,c)
            yy=sp.kronecker_product(yy,sp.kronecker_product(y,spI))
        assert sp.simplify(sp.trace(hh*cc))==objective**m
        # Known Bell-product diagonalization gives every slack eigenvalue explicitly.
        from itertools import product
        vals=[max(probs)**m/2**m-sp.prod(t)/2**m for t in product(probs,repeat=m)]
        assert all(v>=0 for v in vals)

# Tangent bound, multiplicative-regret reduction, arbitrary latent mixtures.
scalar_violation=0.0
count=0
for m in [1,2,3,8,32,127]:
  for a in np.linspace(.25,1,101):
    gamma=float(rng.uniform(.001,1))
    f=rng.uniform(0,a,size=20)
    weights=rng.dirichlet(np.ones(20))
    r=a-f
    lhs=a**m-f**m
    rhs=m*a**(m-1)*r
    scalar_violation=max(scalar_violation,float(np.max(lhs-rhs)))
    delta=float(weights@r)
    eps0=max(0.,delta-gamma*(1-a))
    global_regret=float(a**m-weights@(f**m))
    bound=gamma*(1-a**m)+m*eps0
    scalar_violation=max(scalar_violation,global_regret-bound)
    count+=1

# Exposed-key / fixed unframed channel counterexample: residual coherent rotation.
theta=.12
u=np.diag([np.exp(-1j*theta),np.exp(1j*theta)])
f=abs(np.trace(u))**2/4
private_diamond=2*(1-f)
unframed_diamond=2*np.sin(theta)
# With the key flagged at output, input |+> attains 2 sin(theta) in every
# branch (U_theta or U_minus_theta), so the flagged trace norm has that value.
assert unframed_diamond>private_diamond*5

# Symbolic amplitude-damping certificate for the strict unframed optimum gap.
t=sp.symbols('t', positive=True)
vec=sp.Matrix([1,0,0,t])
h_ad=(vec*vec.T+(1-t**2)*sp.diag(0,1,0,0))/4
y_ad=sp.diag((1+t)/4,t*(1+t)/4)
s_ad=sp.kronecker_product(y_ad,sp.eye(2))-h_ad
expected_slack=sp.Matrix([[t/4,0,0,-t/4],[0,t*(1+t)/4,0,0],
                          [0,0,t*(1+t)/4,0],[-t/4,0,0,t/4]])
assert sp.simplify(s_ad-expected_slack)==sp.zeros(4)
v_id=sp.Matrix([1,0,0,1]); x_id=v_id*v_id.T
f_ad=(1+t)**2/4
assert sp.simplify(sp.trace(h_ad*x_id)-f_ad)==0
assert sp.simplify(sp.trace(y_ad)-f_ad)==0
assert s_ad.nullspace()==[v_id]
assert sp.simplify((1-t**2)-(1-f_ad)-(1-t)*(1+3*t)/4)==0
ad_certificate={'slack_eigenvalues':['0','t/2','t*(1+t)/4 (twice)'],
                'kernel':'span{(1,0,0,1)} for 0<t<1',
                'fopt':'(1+t)^2/4',
                'unframed_identity_lower_bound_minus_framed_optimum':'(1-t)*(1+3*t)/2 > 0',
                'unique_fe_optimal_decoder':'identity; kernel support plus TP'}

out={'status':'PASS','seed':202610271929,
     'random_channel_objective_tp_trace_max_residual':float(max(errs)),
     'key_conjugation_fidelity_max_residual':float(max(key_inv)),
     'pauli_twirl_off_diagonal_max_residual':float(max(twirl_diag)),
     'exact_pauli_optimality_certificates':certs,
     'scalar_mixture_cases':count,'scalar_max_violation':scalar_violation,
     'coherent_residual_counterexample':{'theta':theta,'entanglement_fidelity':float(f),
       'private_framed_diamond':float(private_diamond),'unframed_or_key_flagged_diamond':float(unframed_diamond)},
     'amplitude_damping_symbolic_certificate':ad_certificate,
     'scope':'Exact rational certificates only for stated Pauli examples; random residual/scalar checks do not prove the general theorem. No Schur/tomography/decoder circuit is executed.'}
assert max(errs)<1e-12 and max(key_inv)<1e-12 and max(twirl_diag)<1e-12
assert scalar_violation<1e-12
(ROOT/'private_framed_independent_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
