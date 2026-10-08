"""Fresh sharp-step diagnostics and exact finite optimizer counterexamples.

No target verification code is read or imported. Exact rational identities and
new 4x4 matrix checks complement the proof; they do not prove a supremum.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import comb
import json
import numpy as np

OUT = Path(__file__).parent


def sectors(N):
    for twoj in range(N % 2, N + 1, 2):
        k = (N - twoj) // 2
        mult = comb(N, k) - (comb(N, k - 1) if k else 0)
        p = Q((twoj + 1) * mult, 2 ** N)
        yield twoj, mult, p


def add(A, B):
    return [[a+b for a, b in zip(x, y)] for x, y in zip(A, B)]


def scale(a, A):
    return [[a*x for x in row] for row in A]


def mul(A, B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]


def tr(A):
    return sum(A[i][i] for i in range(len(A)))


I = [[Q(int(i==j)) for j in range(4)] for i in range(4)]
XX = [[Q(int(i+j==3)) for j in range(4)] for i in range(4)]
YY = [[Q(0),0,0,-1],[0,0,1,0],[0,1,0,0],[-1,0,0,0]]
ZZ = [[Q((1,-1,-1,1)[i] if i==j else 0) for j in range(4)] for i in range(4)]
XI_IX = [[Q(int((i^j) in (1,2))) for j in range(4)] for i in range(4)]


def exact_pair_chi(C, t):
    delta = scale(Q(1,4), add(add(scale(C[0],XX),scale(C[1],YY)),scale(C[2],ZZ)))
    sigma = scale(Q(1,4),add(add(I,scale(t,XI_IX)),scale(t*t,XX)))
    inv = scale(4/(1-t*t)**2,add(add(I,scale(-t,XI_IX)),scale(t*t,XX)))
    assert mul(sigma,inv) == I
    value = tr(mul(mul(delta,delta),inv))
    gram = (sum(z*z for z in C)-2*t*t*C[1]*C[2])/(1-t*t)**2
    assert value == gram
    return value


exact_examples=[]
for N in [256,257,512,513]:
    tab=list(sectors(N))
    assert sum(p for _,_,p in tab)==1
    casimir=sum(p*Q(j2*(j2+2),4) for j2,_,p in tab)
    assert casimir==Q(3*N,4)
    a=sum(p*Q(j2,2) for j2,_,p in tab)
    v=(1-2*a/N)/(N-1)
    assert v>0
    baseline=6*v*v
    assert exact_pair_chi([-v,-v,2*v],Q(0))==baseline
    if N%2==0:
        p1=next(p for j2,_,p in tab if j2==2)
        shift=2*p1/(N*(N-1))
        improved=exact_pair_chi([-v+shift,-v-shift,2*v],Q(0))
        difference=2*shift*shift
        description='Replace spin1 mixture by (|1,+1>+|1,-1>)/sqrt2; b stays zero.'
        t=Q(0)
    else:
        p_half=next(p for j2,_,p in tab if j2==1)
        t=p_half/N
        improved=exact_pair_chi([-v-t*t,-v,2*v],t)
        difference=t*t*(2*v+16*v*v+t*t*(1-6*v*v))/(1-t*t)**2
        description='Replace spin1/2 mixture by its pure +x state; other sectors unchanged.'
    assert improved-baseline==difference>0
    exact_examples.append({'N':N,'r':2,'baseline':str(baseline),'improved':str(improved),
                           'strict_difference':str(difference),'difference_float':float(difference),
                           'baseline_float':float(baseline),'b_magnitude':str(t),
                           'legal_sector_modification':description})

# Exact algebra in the new tail bound.
derivative_bound=Q(105*265,256)*Q(128,119)**6
assert derivative_bound<180
assert 4*Q(9,8)**5<8
assert 24**2*3<42**2
assert 9720*Q(9,2)**3==885735<900000
f=[Q(1)]
aa=[Q(1)]
bb=[Q(1)]
for k in range(1,25):
    f.append(f[-1]*Q(2*k+1,k))
    aa.append(aa[-1]*Q(2*k+5,k))
    bb.append(bb[-1]*Q(2*k+9,k))
g=[aa[k]+(3*aa[k-1] if k else 0) for k in range(25)]
assert g[0]==1 and g[1]==10
for k in range(3,25):
    assert 36*k*k*f[k]==108*g[k-1]
for k in range(23):
    assert (k+2)*(k+1)*g[k+2]==105*(bb[k]+(bb[k-1] if k else 0))

# Fresh noncommuting covariance and Parseval checks from valid white-sector vectors.
P=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1,-1])]
I2=np.eye(2)
eps=np.zeros((3,3,3))
eps[0,1,2]=eps[1,2,0]=eps[2,0,1]=1
eps[1,0,2]=eps[0,2,1]=eps[2,1,0]=-1
rng=np.random.default_rng(481913)
numeric=[]
for N in [256,257,384,385,512,513]:
    for mode in ['biased_complex','haar']:
        mu=np.zeros(3)
        S=np.zeros((3,3))
        for j2,_,p in sectors(N):
            j=j2/2
            dim=j2+1
            if mode=='haar':
                psi=rng.normal(size=dim)+1j*rng.normal(size=dim)
            else:
                psi=np.zeros(dim,complex)
                psi[0]=1
                if dim>1: psi[1]=.37j*np.exp(.31j*j)
                if dim>2: psi[-1]+=.11*np.exp(.17j*j)
            psi/=np.linalg.norm(psi)
            m=j-np.arange(dim)
            jp=np.zeros(dim,complex); jm=np.zeros(dim,complex)
            if dim>1:
                jp[:-1]=np.sqrt(j*(j+1)-m[1:]*(m[1:]+1))*psi[1:]
                jm[1:]=np.sqrt(j*(j+1)-m[:-1]*(m[:-1]-1))*psi[:-1]
            acts=[(jp+jm)/2,(jp-jm)/(2j),m*psi]
            for a in range(3):
                mu[a]+=float(p)*np.vdot(psi,acts[a]).real
                for b in range(3): S[a,b]+=float(p)*np.vdot(acts[a],acts[b]).real
        b=2*mu/N
        V=S-np.outer(mu,mu)
        X=4*V/N; Z=X+np.outer(b,b)
        c=(4*S-N*np.eye(3))/(N*(N-1))
        C=c-np.outer(b,b)
        assert np.linalg.eigvalsh(V)[0]>-1e-9
        assert np.linalg.eigvalsh(Z)[0]>-1e-10
        assert abs(np.trace(Z)-(3-(N-1)*np.dot(b,b)))<1e-10
        assert np.linalg.norm(C-(Z-np.eye(3))/(N-1))<1e-12
        assert np.sum(C*C)<=6/(N-1)**2+1e-13
        rho=np.eye(4,dtype=complex)
        for a in range(3):
            rho+=b[a]*(np.kron(P[a],I2)+np.kron(I2,P[a]))
            for z in range(3): rho+=c[a,z]*np.kron(P[a],P[z])
        rho/=4
        tau=(I2+sum(b[a]*P[a] for a in range(3)))/2
        sigma=np.kron(tau,tau); delta=rho-sigma
        assert np.linalg.eigvalsh(rho)[0]>-1e-10
        chi=np.trace(delta@delta@np.linalg.inv(sigma)).real
        G=np.eye(3)-np.outer(b,b)+1j*np.einsum('abc,c->ab',eps,b)
        gram=np.vdot(C.ravel(),np.kron(np.linalg.inv(G),np.linalg.inv(G))@C.ravel()).real
        wrongG=np.eye(3)-np.outer(b,b)
        wrong=np.vdot(C.ravel(),np.kron(np.linalg.inv(wrongG),np.linalg.inv(wrongG))@C.ravel()).real
        assert abs(chi-gram)<1e-12
        t=np.linalg.norm(b)
        assert chi<=6/((N-1)**2*(1-t)**2)+1e-12
        numeric.append({'N':N,'mode':mode,'chi':chi,'parseval_residual':abs(chi-gram),
                        'commutator_norm':float(np.linalg.norm(rho@sigma-sigma@rho)),
                        'invalid_real_Gram_discrepancy':abs(wrong-chi),
                        'minimum_covariance_eigenvalue':float(np.linalg.eigvalsh(V)[0])})

N_rare=10**8
r_rare=4
alpha=Q(3,N_rare+2)
pair_norm=Q(6,(N_rare+2)**2)
d4=Q(3*(N_rare-2),(N_rare+2)*(N_rare-3))
rare_lower=6*pair_norm+d4*d4
rare_target=Q(36,N_rare**2)
rare_error=Q(42*16,N_rare**2*10000)+Q(900000*64,N_rare**3)
assert rare_lower-rare_target>rare_error
assert alpha*Q(N_rare*(N_rare+2),4)==Q(3*N_rare,4)
rare={'N':N_rare,'r':r_rare,'maximal_spin_weight':str(alpha),
      'spin0_weight':str(1-alpha),'exact_Casimir':str(Q(3*N_rare,4)),
      'd_zzzz':str(d4),'chi_lower_bound':str(rare_lower),
      'would_be_white_target':str(rare_target),'would_be_white_remainder':str(rare_error),
      'strict_violation':str(rare_lower-rare_target-rare_error),
      'N_squared_chi_lower_float':float(N_rare**2*rare_lower),
      'claim_refuted':'Replace exactly white Schur weights by mean Casimir only.'}

result={'status':'PASS exact and numerical finite diagnostics; not a supremum proof',
        'candidate_code_read':False,'exact_finite_optimizer_counterexamples':exact_examples,
        'exact_mean_Casimir_premise_counterexample':rare,
        'g_second_derivative_rational_bound':str(derivative_bound),
        'coefficient_identity_checks':45,'numeric_valid_white_sector_cases':numeric}
(OUT/'independent_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'counterexample_count':len(exact_examples),
                  'counterexample_differences':[z['difference_float'] for z in exact_examples],
                  'numeric_cases':len(numeric),
                  'maximum_Parseval_residual':max(z['parseval_residual'] for z in numeric),
                  'maximum_noncommutator':max(z['commutator_norm'] for z in numeric),
                  'maximum_invalid_real_Gram_discrepancy':max(z['invalid_real_Gram_discrepancy'] for z in numeric)},indent=2))
