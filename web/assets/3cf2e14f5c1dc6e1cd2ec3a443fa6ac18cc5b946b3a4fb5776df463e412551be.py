#!/usr/bin/env python3
"""Exact finite algebra audits for FULL_QUTRIT_TENSOR_THEOREM.txt."""
from pathlib import Path
from itertools import product
import hashlib
import json
import sympy as s

BASE = Path(__file__).resolve().parent
R = s.Rational
I = s.eye(3)
Ji = [s.Matrix(3, 3, lambda j,k: -s.I*s.LeviCivita(i,j,k)) for i in range(3)]
e = [I[:,i] for i in range(3)]
checks = []


def simp(m):
    return m.applyfunc(s.simplify)


def record(name, **details):
    checks.append({"name":name,"status":"PASS",**details})


def model(X,a,b):
    return (1-b)*s.trace(X)*I/3 + (a+b)*X/2 + (b-a)*X.T/2


# Choi CP decomposition on exact orthogonal projections.
omega = s.Matrix([1,0,0,0,1,0,0,0,1])/s.sqrt(3)
P = omega*omega.T
swap = s.zeros(9)
for i,j in product(range(3),repeat=2):
    swap[3*j+i,3*i+j]=1
P0=P; P1=(s.eye(9)-swap)/2; P2=(s.eye(9)+swap)/2-P
a,b=s.symbols("a b",real=True)
Ch=(1-b)*s.eye(9)/9+(a+b)*P/2+(b-a)*swap/6
eig = [(1+3*a+5*b)/9,(2+3*a-5*b)/18,(2-3*a+b)/18]
for proj,lam,rank in zip([P0,P1,P2],eig,[1,3,5]):
    assert proj*proj==proj and proj.trace()==rank
    assert simp(Ch*proj-lam*proj)==s.zeros(9)
assert P0+P1+P2==s.eye(9)
assert P0*P1==P0*P2==P1*P2==s.zeros(9)
assert s.simplify(Ch.trace())==1
record("exact_CP_spectrum", eigenvalues=[str(x) for x in eig],
       multiplicities=[1,3,5])

# Fixed real seven-state ensemble and coherent fourteen-state ensemble.
tetra_signs=[(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
real_atoms=[(R(2,15),v*v.T) for v in e]
for signs in tetra_signs:
    v=s.Matrix(signs)/s.sqrt(3)
    real_atoms.append((R(3,20),v*v.T))
directions=[(R(1,15),sign*v) for v in e for sign in [-1,1]]
directions += [(R(3,40),s.Matrix(signs)/s.sqrt(3))
               for signs in product([-1,1],repeat=3)]
coherent_atoms=[]
for q,n in directions:
    Jn=sum((n[i]*Ji[i] for i in range(3)),s.zeros(3))
    assert simp(Jn*Jn-(I-n*n.T))==s.zeros(3)
    pi=(I-n*n.T+Jn)/2
    coherent_atoms.append((q,pi))
for weight,pi in [*real_atoms,*coherent_atoms]:
    assert simp(pi.H-pi)==s.zeros(3)
    assert simp(pi*pi-pi)==s.zeros(3)
    assert pi.trace()==1
    assert weight>0
for atoms in [real_atoms,coherent_atoms]:
    assert sum(w for w,pi in atoms)==1
    assert simp(sum((w*pi for w,pi in atoms),s.zeros(3))-I/3)==s.zeros(3)
record("all_21_pure_atoms_and_barycenters", real_atoms=len(real_atoms),
       coherent_atoms=len(coherent_atoms), barycenter="I3/3")

# Exact second and fourth moments; all odd moments through degree three.
for i in range(3):
    assert s.simplify(sum(q*n[i] for q,n in directions))==0
for i,j in product(range(3),repeat=2):
    assert s.simplify(sum(q*n[i]*n[j] for q,n in directions))==R(int(i==j),3)
for i,j,k in product(range(3),repeat=3):
    assert s.simplify(sum(q*n[i]*n[j]*n[k] for q,n in directions))==0
for i,j,k,l in product(range(3),repeat=4):
    target=R(int(i==j)*int(k==l)+int(i==k)*int(j==l)+int(i==l)*int(j==k),15)
    assert s.simplify(sum(q*n[i]*n[j]*n[k]*n[l] for q,n in directions))==target
record("weighted_direction_design_moments", exact_degree=4,
       directions=14, fourth_moment_denominator=15)

def canonical(atoms,X):
    return simp(sum((3*w*pi*s.trace(pi*X) for w,pi in atoms),s.zeros(3)))

for i,j in product(range(3),repeat=2):
    E=s.zeros(3);E[i,j]=1
    real_out=canonical(real_atoms,E)
    coherent_out=canonical(coherent_atoms,E)
    assert simp(real_out-model(E,0,R(2,5)))==s.zeros(3)
    assert simp(coherent_out-model(E,R(1,2),R(1,10)))==s.zeros(3)
record("canonical_maps_on_full_matrix_space", basis_units=9,
       real_multipliers=["1","0","2/5"],
       coherent_multipliers=["1","1/2","1/10"])

mu=s.symbols("mu",real=True)
beta=(2-3*mu)/5
assert s.simplify(2*mu*R(1,2)+(1-2*mu)*0-mu)==0
assert s.simplify(2*mu*R(1,10)+(1-2*mu)*R(2,5)-beta)==0
assert s.simplify(R(2,5)-(2*b-1)-(7-10*b)/5)==0
assert s.simplify((2-3*(2*a-1))/5-(2*b-1)-R(2,5)*(5-3*a-5*b))==0
# Bounds follow from these exact nonnegative linear-combination identities.
n0=1+3*a+5*b; n1=2+3*a-5*b; n2=2-3*a+b
assert s.expand(n0+n1-(3+6*a))==0
assert s.expand(n0+n2-(3+6*b))==0
assert s.expand((5-3*a-5*b)+n1-(7-10*b))==0
record("scalar_comparator_regime_identities", mu="(2|a|-1)_+",
       quadrupole_low_a_slack="(7-10b)/5",
       quadrupole_high_a_slack="(2/5)(5-3a-5b)")

# Full traceless frame normalization and complete exact star spectrum.
H=[I,*[s.sqrt(R(3,2))*x for x in Ji]]
H += [s.sqrt(R(3,2))*s.diag(1,-1,0),s.diag(1,1,-2)/s.sqrt(2)]
for i,j in [(0,1),(0,2),(1,2)]:
    E=s.zeros(3);E[i,j]=E[j,i]=1
    H.append(s.sqrt(R(3,2))*E)
assert len(H)==9
for i,j in product(range(9),repeat=2):
    assert s.simplify(s.trace(H[i]*H[j])/3)==int(i==j)
assert simp(sum((s.kronecker_product(h.T,h) for h in H),s.zeros(9))-9*P)==s.zeros(9)
swap_BC=s.zeros(27)
for i,j,k in product(range(3),repeat=3):
    swap_BC[9*i+3*k+j,9*i+3*j+k]=1
PAB=s.kronecker_product(P,I)
PAC=swap_BC*PAB*swap_BC
assert PAB*PAC*PAB==PAB/9
W=sum((s.kronecker_product(h.T,h,I)+s.kronecker_product(h.T,I,h)
       for h in H[1:]),s.zeros(27))
assert simp(W-(9*(PAB+PAC)-2*s.eye(27)))==s.zeros(27)
t=s.Symbol("t")
cp=s.factor(W.charpoly(t).as_expr())
expected=(t-10)**3*(t-4)**3*(t+2)**21
assert s.expand(cp-expected)==0
record("full_frame_star_normalization", characteristic_polynomial=str(cp),
       maximum_eigenvalue="10", score="2(3a+5b)",
       exact_bound="3a+5b<=5")

# Reconstruct the supplied exact spin-sharp broadcaster, including all marginals.
R0=s.zeros(27)
for i in range(3):
    v=s.zeros(27,1)
    for j in range(3):
        v[9*i+3*j+j] += -2
        v[9*j+3*i+j] += 3
        v[9*j+3*j+i] += 3
    assert (v.T*v)[0]==60
    R0+=v*v.T/180
assert R0.trace()==1 and swap_BC*R0*swap_BC==R0
AB=s.Matrix(9,9,lambda r,c:sum(R0[3*r+k,3*c+k] for k in range(3)))
for axis in range(3):
    marginal=s.zeros(3)
    for i,j in product(range(3),repeat=2):
        for u,v in product(range(3),repeat=2):
            row=[u,v]; col=[u,v]
            row.insert(axis,i); col.insert(axis,j)
            rr=9*row[0]+3*row[1]+row[2]
            cc=9*col[0]+3*col[1]+col[2]
            marginal[i,j]+=R0[rr,cc]
    assert marginal==I/3
for i,j in product(range(3),repeat=2):
    E=s.zeros(3);E[i,j]=1
    reconstructed=s.Matrix(3,3,lambda u,v:3*AB[3*i+u,3*j+v])
    assert simp(reconstructed-model(E,R(3,4),R(7,20)))==s.zeros(3)
record("legal_sharp_R0_channel_reconstruction", a="3/4",b="7/20",
       all_single_marginals="I3/3",BC_symmetric=True,
       vector_frame_ratio="2",non_EB_witness="spin score3/2 exceeds k1")

result={
 "scope":"exact finite identity audits; analytic quantified proof separately supplied",
 "proof_sha256":hashlib.sha256((BASE/'FULL_QUTRIT_TENSOR_THEOREM.txt').read_bytes()).hexdigest(),
 "supplied_spin_theorem_sha256":hashlib.sha256((BASE.parents[1]/'spin1-proof/SPIN1_ALL_WEIGHTS_THEOREM.txt').read_bytes()).hexdigest(),
 "sympy_version":s.__version__,"tests":checks,"all_pass":True,
 "general_arbitrary_channel_status":"UNKNOWN"
}
(BASE/'full_qutrit_replay.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({"all_pass":True,"tests":len(checks),"proof_sha256":result['proof_sha256']},indent=2))
