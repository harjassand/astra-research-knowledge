"""Independent 19-qubit PI positive control, from AAB Prop. 7.1.

Original arithmetic only; no downloaded research code.  This constructs the
published real root, proves a unique zero exists in a rational box using a
Banach contraction, verifies that all 4-qubit reduced KL polynomials lie in the
span of the nine defining equations, and checks degree <=4 spin KL numerically.
"""
import json
from math import comb
from pathlib import Path
import mpmath as mp
import numpy as np
import sympy as s

OUT = Path(__file__).resolve().parent
mp.mp.dps = 100
q = s.symbols('q0 q2 q4 q6 q8 q10 q12 q14 q16 q18')
def Q(w):
    assert 0 <= w <= 18 and w % 2 == 0
    return q[w//2]
F = []
labels = []
for a in [0,2,4]:
    for b in [1,3]:
        F.append(s.expand(sum(comb(15,2*k)*Q(2*k+a)*Q(19-2*k-b) for k in range(8))))
        labels.append(['D1',a,b])
for a,b in [(0,0),(0,2)]:
    F.append(s.expand(sum(comb(15,2*k)*(Q(2*k+a)*Q(2*k+b)-Q(2*k+4-a)*Q(2*k+4-b)) for k in range(8))))
    labels.append(['D2',a,b])
a=b=1
F.append(s.expand(sum(comb(15,2*k)*(Q(19-2*k-a)*Q(19-2*k-b)-Q(19-2*k-4+a)*Q(19-2*k-4+b)) for k in range(8))))
labels.append(['D3',a,b])
X = s.Matrix(q[1:])
f = s.Matrix(F).subs(q[0],1)
J = f.jacobian(X)
fn = s.lambdify(tuple(X), f, 'mpmath')
jn = s.lambdify(tuple(X), J, 'mpmath')
seed = list(map(mp.mpf, ['0.0477572','-0.0267249','-0.00506367','0.00332914','0.00527235','-0.000947223','0.0152707','0.00888631','0.32678']))
root = mp.findroot(fn, seed, J=jn, tol=mp.mpf('1e-95'), maxsteps=20)
print('Root refined:', [mp.nstr(z,25) for z in root], flush=True)

# Exact rational contraction certificate, in the closed sup-norm ball B(x,r).
# T(z)=z-R f(z), with R a rounded rational approximation of J(x)^-1.
# sup_B ||DT||_infty <= L, ||T(x)-x||_infty <= b.
# b+L*r<r and L<1 prove existence/uniqueness by Banach.  R nonsingular
# follows from ||I-R*J(x)||<1, so the fixed point is a zero of f.
def rat(v, digits=50):
    return s.Rational(mp.nstr(v,digits))
x = s.Matrix([rat(v) for v in root])
sub = dict(zip(X,x))
J0 = J.subs(sub)
Rmp = jn(*root)**-1
R = s.Matrix(9,9,lambda i,j:rat(Rmp[i,j]))
r = s.Rational(1,10**40)
bvec = R*f.subs(sub)
bmax = max(abs(v) for v in bvec)
M = s.eye(9)-R*J0
Mnorm = max(sum(abs(M[i,j]) for j in range(9)) for i in range(9))
Hs = [s.hessian(fi,X) for fi in f]
# A_jk = derivative in x_k of the jth column of R*J; exact constants.
Hrow = max(sum(abs(sum(R[i,l]*Hs[l][j,k] for l in range(9))) for j in range(9) for k in range(9)) for i in range(9))
L = Mnorm + r*Hrow
margin = r-bmax-L*r
assert L < 1 and margin > 0
print('Exact contraction PASS:', 'b/r=',s.N(bmax/r,8),'L=',s.N(L,8), flush=True)

# Independent symbolic verification of every 4-qubit reduced KL condition.
# Remove the harmless sqrt(C(4,a)C(4,b)) factor from each matrix entry.
# For a code vector with coefficient sqrt(C(19,w))*z_w, the resulting
# reduced matrix entry is sum_k C(15,k) z_(k+a) z_(k+b).
def z(logical,w):
    if logical == 0:
        return Q(w) if w % 2 == 0 else s.Integer(0)
    return Q(19-w) if w % 2 else s.Integer(0)
def red(a,b,la,lb):
    return s.expand(sum(comb(15,k)*z(la,k+a)*z(lb,k+b) for k in range(16)))
mons = [q[i]*q[j] for i in range(10) for j in range(i,10)]
def vec(poly):
    p=s.Poly(poly,*q)
    return s.Matrix([p.coeff_monomial(m) for m in mons])
B=s.Matrix.hstack(*[vec(fi) for fi in F])
assert B.rank()==9
decompositions=[]
for kind in ['cross','difference']:
    for a in range(5):
        for b in range(5):
            polynomial = red(a,b,0,1) if kind=='cross' else red(a,b,0,0)-red(a,b,1,1)
            coeff,params=B.gauss_jordan_solve(vec(polynomial))
            assert params.rows==0 and B*coeff==vec(polynomial)
            decompositions.append({'kind':kind,'a':a,'b':b,'linear_combination':[str(v) for v in coeff]})
print('All 50 reduced KL polynomial identities PASS',flush=True)

qs=[mp.mpf(1)]+list(root)
N=sum(mp.mpf(comb(19,2*i))*qs[i]**2 for i in range(10))
c0=[mp.mpf(0)]*20
for i in range(10):c0[2*i]=qs[i]*mp.sqrt(comb(19,2*i)/N)
c1=list(reversed(c0))
V=np.array([[float(c0[w]),float(c1[w])] for w in range(20)])
Jz=np.diag(np.arange(20)-9.5)
Jp=np.diag([np.sqrt((19-w)*(w+1)) for w in range(19)],-1)
Jm=Jp.T
norm_error=float(np.max(np.abs(V.T@V-np.eye(2))))
errors=[]
for a in range(5):
    for b in range(5-a):
        for c in range(5-a-b):
            E=np.linalg.matrix_power(Jp,a)@np.linalg.matrix_power(Jz,b)@np.linalg.matrix_power(Jm,c)
            C=V.T@E@V
            raw=float(np.max(np.abs(C-np.trace(C)*np.eye(2)/2)))
            errors.append({'a':a,'b':b,'c':c,'raw':raw,'relative_frobenius':raw/max(1,float(np.linalg.norm(E)))})
assert norm_error<1e-14
assert max(e['relative_frobenius'] for e in errors)<1e-14
# A five-site Z string has Dicke diagonal K_5(w)/binomial(19,5).
# Certify a nonzero logical diagonal difference, so the distance is exactly 5.
def kraw5(w):
    return sum((-1)**j*comb(w,j)*comb(19-w,5-j) for j in range(6) if j<=w and 5-j<=19-w)
g=s.expand(2*sum(comb(19,2*i)*kraw5(2*i)*q[i]**2 for i in range(10))).subs(q[0],1)
g0=g.subs(sub)
# Exact quadratic Taylor bound on |g(y)-g(x)| throughout the box.
g_error=r*sum(abs(s.diff(g,xi).subs(sub)) for xi in X)+r*r*sum(abs(s.diff(g,xi,xj)) for xi in X for xj in X)/2
assert abs(g0)>g_error
z5diff=2*sum(comb(19,2*i)*kraw5(2*i)*qs[i]**2 for i in range(10))/(comb(19,5)*N)
out={
 'n':19,'dimension':2,'distance_at_least':5,'distance_exactly':5,
 'source':{'title':'A family of permutationally invariant quantum codes','authors':'Aydin, Alekseyev, Barg','journal':'Quantum 8, 1321 (2024)','doi':'10.22331/q-2024-04-30-1321','url':'https://arxiv.org/html/2310.05358v3#S7','definition':'Equation (32), Proposition 7.1, final example of Section 7'},
 'exact_amplitude_definition':'Let q0=1 and let (q2,...,q18) be the unique real zero in the certified box of the nine polynomials. Let N=sum_i binomial(19,2i)*q_(2i)^2. Then c0[2i]=sqrt(binomial(19,2i)/N)*q_(2i), c0[odd]=0, and c1[w]=c0[19-w].',
 'polynomial_labels':labels,'polynomials':[str(fi) for fi in F],
 'rational_box_center':[str(v) for v in x],'rational_box_radius':str(r),
 'contraction':{'preconditioner':[[str(R[i,j]) for j in range(9)] for i in range(9)],'b_exact':str(bmax),'Mnorm_exact':str(Mnorm),'Hrow_exact':str(Hrow),'L_exact':str(L),'margin_exact':str(margin),'b_over_r_approx':str(s.N(bmax/r,15)),'L_approx':str(s.N(L,15)),'proved':True},
 'q_80_digits':[mp.nstr(v,80) for v in qs],
 'normalization_N_80_digits':mp.nstr(N,80),
 'dicke_c0_80_digits':[mp.nstr(v,80) for v in c0],
 'dicke_c1_80_digits':[mp.nstr(v,80) for v in c1],
 'numerical_gram_error':norm_error,
 'all_50_reduced_KL_symbolic_identities_proved':True,
 'reduced_KL_decompositions':decompositions,
 'spin_monomial_tests':errors,
 'max_spin_KL_raw':max(e['raw'] for e in errors),
 'max_spin_KL_relative_frobenius':max(e['relative_frobenius'] for e in errors),
 'distance5_witness':{'operator':'Z on any fixed five physical qubits','difference_numerator_polynomial':str(g),'center_value_exact':str(g0),'box_error_bound_exact':str(g_error),'logical_diagonal_difference_80_digits':mp.nstr(z5diff,80),'nonzero_proved':True},
}
(OUT/'positive19_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
np.savez(OUT/'positive19_dicke.npz',V=V,P=V@V.T,n=np.array(19),d=np.array(5))
print(json.dumps({k:out[k] for k in ['n','dimension','distance_at_least','numerical_gram_error','max_spin_KL_raw','max_spin_KL_relative_frobenius']},indent=2))
