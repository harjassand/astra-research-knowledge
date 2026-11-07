from exact_matrix import *
from mediation import *
from pathlib import Path
from itertools import product
from scipy.linalg import expm
import json, time, random

started=time.perf_counter(); checks=0
def check(condition):
    global checks
    checks+=1
    assert condition, f"Check {checks} failed"


def initial_derivative(C,U,A):
    d=len(A[0]); out=zeros(d); H=hamiltonian(U,A)
    out[:,0] += H[:,0]*(-I); out[0,:] += H[0,:]*I
    for a in range(len(A)):
        for b in range(len(A)):
            if C[a,b]:
                out += np.outer(A[a][:,0],A[b][0,:])*C[a,b]
                ba=A[b]@A[a][:,0]
                # All A are Hermitian, but BA need not be Hermitian.
                abrow=A[b][0,:]@A[a]
                out[:,0] -= ba*C[a,b]/2
                out[0,:] -= abrow*C[a,b]/2
    return out


def numeric_generator(C,U,A):
    C,U=numeric(C),numeric(U); A=[numeric(a) for a in A]
    d=len(A[0]); Id=np.eye(d); H=sum((U[a,b]*A[a]@A[b] for a in range(len(A))
                                   for b in range(a+1,len(A))),np.zeros((d,d),complex))
    L=-1j*(np.kron(Id,H)-np.kron(H.T,Id))
    for a in range(len(A)):
        for b in range(len(A)):
            BA=A[b]@A[a]
            L += C[a,b]*(np.kron(A[b].T,A[a])-(np.kron(Id,BA)+np.kron(BA.T,Id))/2)
    return L


def numeric_channel(V,F,G,n,h):
    V,F,G=[numeric(a).real for a in [V,F,G]]
    A=[numeric(a) for a in site_ops(n)]; d=2**n; Id=np.eye(d)
    q=V.shape[1]; r=G.shape[1]; K=3*n
    B=[sum((V[a,k]*A[a] for a in range(K)),np.zeros((d,d),complex)) for k in range(q)]
    b2=[np.trace(b@b).real/d for b in B]; Ch=np.zeros((d*d,d*d),complex)
    for signs in product([-1,1],repeat=q+r):
        xi=np.array(signs[:q]); eta=np.array(signs[q:]); y=F@xi+G@eta
        Kr=Id.copy()
        for k,b in enumerate(B): Kr=(Id+np.sqrt(h)*xi[k]*b)@Kr/np.sqrt(1+h*b2[k])
        for i in range(n):
            yi=sum((y[a]*A[a] for a in range(3*i,3*i+3)),np.zeros((d,d),complex))
            Kr=(Id+.5j*np.sqrt(h)*yi)@np.linalg.inv(Id-.5j*np.sqrt(h)*yi)@Kr
        Ch += np.kron(Kr.conj(),Kr)/2**(q+r)
    return Ch


n=2; K=6
V=eye(K)/3
# Noncommuting local measurements, asymmetric feedback, complex noise and
# several different noncommuting interaction terms are all present.
F=mat([[Q(((a*7+b*3)%9)-4,17) for b in range(K)] for a in range(K)])
G=mat([[Q((-1)**a,19)] for a in range(K)])
data=from_factors(V,F,G,n)
for key in ['D','R','Sigma','C']: check(psd(data[key]))
for bad in [mat([[0,1],[1,0]]),mat([[1,2],[2,1]]),mat([[0,I],[-I,0]])]:
    good,separator,value=psd_or_separator(bad)
    check(not good and value<0)
    check(real_scalar((adj(separator)@bad@separator)[0,0])==value)
check(psd_or_separator(data['Sigma'])[0])
check(equal(block_parts(data['D'],n)[1],zeros(K)))
check(equal(block_parts(data['S'],n)[1],zeros(K)))
check(equal(data['Sigma'],np.block([[data['D'],-(data['U']+data['S']+data['J'])/2],
                                  [-(data['U']+data['S']-data['J'])/2,data['R']-data['D']]])))

A=site_ops(n)
Qdrift=zeros(4)
for a in range(K):
    for b in range(K):
        Qdrift += (A[a]@A[b])*(-data['R'][a,b]/2+I*data['B'][b,a])
target=hamiltonian(data['U'],A)*(-I)
for a in range(K):
    for b in range(K): target -= (A[b]@A[a])*data['C'][a,b]/2
check(equal(Qdrift+eye(4)*I*trace(data['S'])/2,target))

Ar=site_ops(n,True)
d0=initial_derivative(data['C'],data['U'],Ar)
single=[4*(a+1) for a in range(3)]+[a+1 for a in range(3)]
for a in range(K):
    for b in range(K): check(d0[single[a],single[b]]==data['C'][a,b])
for a in range(3):
    for b in range(3):
        check(d0[4*(a+1)+b+1,0]==-data['R'][a,b+3]-I*data['U'][a,b+3])
check(equal(d0,adj(d0))); check(trace(d0)==0)

# Audit the full dual formula, including imaginary normal correlations and
# unequal off-site P,T blocks, rather than only the simple Ising witness.
E=zeros(K); Qgeneral=zeros(K)
for a in range(K):
    for b in range(K):
        if a//3!=b//3:
            E[a,b]=Z(Q((a+b)%3-1,17))
            Qgeneral[a,b]=Z(Q((2*a+b)%5-2,13))
        elif a<b:
            Qgeneral[a,b]=Z(Q(a+b+1,23)); Qgeneral[b,a]=-Qgeneral[a,b]
Ygeneral=np.block([[eye(K)*10+E,Qgeneral],[Qgeneral.T,eye(K)*10-E]])
valid_general,kappa_general=dual(Ygeneral,data['R'],data['J'],data['U'],n)
check(valid_general)
Wgeneral=dual_witness(Ygeneral,n)
check(equal(Wgeneral,adj(Wgeneral)))
check(Wgeneral[0,0]==0)
check(real_scalar(trace(Wgeneral@d0))==-kappa_general)

# Exactly rational binary-instrument and Cayley identities at one site.
s=Q(1,32); b=[Q(1,3),Q(-2,7),Q(3,11)]
Bs=sum((paulis()[a]*b[a] for a in range(3)),zeros(2))
check(equal(Bs@Bs,eye(2)*sum(x*x for x in b)))
sum_k=zeros(2)
for sign in [-1,1]:
    N=eye(2)+Bs*(s*sign)
    sum_k += adj(N)@N/(2*(1+s*s*sum(x*x for x in b)))
check(equal(sum_k,eye(2)))
y=[Q(2,5),Q(-1,2),Q(1,7)]; y2=sum(x*x for x in y)
Yop=sum((paulis()[a]*y[a] for a in range(3)),zeros(2))
Uc=(eye(2)*(1-s*s*y2/4)+Yop*(I*s))/(1+s*s*y2/4)
check(equal(adj(Uc)@Uc,eye(2)))
r=[Q(1,5),Q(-2,7),Q(1,3)]
rho=(eye(2)+sum((paulis()[a]*r[a] for a in range(3)),zeros(2)))/2
rot=cayley_bloch(r,y,s)
rho_rot=(eye(2)+sum((paulis()[a]*rot[a] for a in range(3)),zeros(2)))/2
check(equal(Uc@rho@adj(Uc),rho_rot))

# The analytic threshold-separation family, including an exact finite witness.
gamma=Q(3,4); U=zeros(K); U[2,5]=U[5,2]=Z(1); R=eye(K)*gamma; J=zeros(K)
Yd=zeros(2*K)
for a in [2,5]: Yd[a,a]=Yd[a+K,a+K]=Z(Q(1,2))
for a,b in [(2,5),(5,2)]: Yd[a,b+K]=Yd[b+K,a]=Z(Q(1,2))
valid,kappa=dual(Yd,R,J,U,n)
check(valid); check(kappa==Q(1,4)); check(trace(Yd)==2)
dt=initial_derivative(R,U,Ar)
Wdual=dual_witness(Yd,n)
check(real_scalar(trace(Wdual@dt))==-kappa)
vproj=zeros(16)
vproj[12,12]=vproj[3,3]=Z(Q(1,2))
vproj[12,3]=I/2; vproj[3,12]=-I/2
W=pt(vproj,[4,4],1)
check(equal(W,adj(W))); check(W[0,0]==0)
check(real_scalar(trace(W@dt))==Q(-1,4))
# W has eigenvalues 1/2,1/2,1/2,-1/2 and twelve zeroes.
check(equal(W@W@W,W/4)); check(real_scalar(trace(W@W))==1)
tau=Q(1,256); Lambda=Q(11); normW=Q(1,2)
upper=-kappa*tau+normW*Lambda*Lambda*tau*tau/2
check(upper==Q(-135,262144)); check(upper<Q(-1,2048))

# An explicitly paid trusted-measurement witness acquisition contract.
omega=mat([[1],[0],[0],[1]])
bell=np.hstack([omega]+[np.kron(p,eye(2))@omega for p in paulis()])
bell2=np.kron(bell,bell)
Wphysical=bell2@W@adj(bell2)/4
pauli_list=[eye(2)]+paulis(); expansion=[]; score_bound=Q(0)
for setting in product(range(4),repeat=4):
    P=tensor([pauli_list[j] for j in setting])
    coefficient=real_scalar(sum((P[i,j]*Wphysical[j,i] for i in range(16) for j in range(16)
                                 if P[i,j]),Z())/16)
    if coefficient:
        expansion.append({"setting":"".join('IXYZ'[j] for j in setting),"coefficient":str(coefficient)})
        score_bound+=abs(coefficient)
rebuilt=zeros(16)
for term in expansion:
    rebuilt+=tensor([pauli_list['IXYZ'.index(j)] for j in term['setting']])*Q(term['coefficient'])
check(equal(rebuilt,Wphysical))
gap=-upper
shot_expression=48*score_bound*score_bound/(gap*gap) # ln(2/.01)<6
shot_count=(shot_expression.numerator+shot_expression.denominator-1)//shot_expression.denominator
Path(__file__).with_name('REFERENCE_WITNESS.json').write_text(json.dumps({
    "qubit_order":["system_A","reference_A","system_B","reference_B"],
    "pauli_expansion":expansion,"score_bound":str(score_bound),
    "evolution_time":"1/256","expectation_upper_bound":str(upper),
    "conservative_iid_trials_each_error_below_0_01":shot_count,
    "requires":"Trusted Bell preparation and Pauli measurements, valid stated Markovian model, fresh trials. No physical acquisition performed."},indent=2))

# Feasible certificate at the complete-mediation endpoint gamma=|J|=1.
Sep=np.block([[eye(K)/2,-U/2],[-U/2,eye(K)/2]])
check(psd(Sep))

# Ordinary system-only thresholds: exact tangent block for |++>.
plus=mat([[Q(1,2),Q(1,2)],[Q(1,2),Q(1,2)]])
rho_plus=np.kron(plus,plus)
for ga in [Q(1,4),Q(1,2),Q(3,4),Q(1)]:
    dp=pt(generator(rho_plus,eye(K)*ga,U,A),[2,2],1)
    # |+-> and |-+> vectors, each represented with denominator 2.
    v1=mat([[1],[-1],[1],[-1]])/2; v2=mat([[1],[1],[-1],[-1]])/2
    T=np.hstack([v1,v2]); B2=adj(T)@dp@T
    check(real_scalar(B2[0,0])==2*ga)
    check(real_scalar(B2[1,1])==2*ga)
    check(B2[0,1]*B2[1,0]==1)
    check(psd(B2)==(ga>=Q(1,2)))

# Floating diagnostics are expressly not exact proof or production simulation.
L=numeric_generator(data['C'],data['U'],A)
diagnostics=[]
for h in [1/32,1/64,1/128,1/256]:
    Ch=numeric_channel(V,F,G,n,h)
    err=np.linalg.norm(Ch-expm(h*L),2)
    trvec=np.eye(4).reshape(-1,order='F')
    tp=np.linalg.norm(trvec@Ch-trvec)
    diagnostics.append(dict(h=h,operator_error=float(err),error_over_h2=float(err/h**2),trace_preservation_residual=float(tp)))
    check(tp<1e-12)
check(diagnostics[-1]['error_over_h2']<5)

# Run the fixed-budget rational trajectory kernel as a software smoke check.
# A short run is NOT assigned the global continuum tolerance from the theorem.
to_fraction=lambda M:[[real_scalar(x) for x in row] for row in M]
sample,states=trajectory_z_sample(to_fraction(V),to_fraction(F),to_fraction(G),2,
                                 [[Q(1),Q(0),Q(0)],[Q(0),Q(0),Q(1)]],
                                 [[Q(0)]*3]*2,Q(1,32),12,36,random.Random(20261107))
for rr in states: check(dot(rr,rr)<=1)
check(len(sample)==2)

output={"exact_and_diagnostic_assertions":checks,"wall_seconds":time.perf_counter()-started,
        "finite_witness":{"J":"1","gamma":"3/4","time":"1/256","expectation_upper_bound":str(upper),
                          "ordinary_separability_threshold":"1/2","complete_mediation_threshold":"1",
                          "pauli_terms":len(expansion),"score_bound":str(score_bound),"iid_trial_bound":shot_count},
        "floating_small_channel_diagnostics":diagnostics,
        "rational_trajectory_smoke_check":{"steps":12,"precision_bits":36,"sample":sample,
            "scope":"Software algebra/positivity check only; no continuum-accuracy or physical experiment claim."},
        "conservative_budget_example":compiler_budget(2,"6","0","1/100","1/100"),
        "not_executed":"Full conservative compiler budgets, physical instruments, reference preparations and witness acquisitions."}
Path(__file__).with_name('VALIDATION.json').write_text(json.dumps(output,indent=2))
print(json.dumps(output,indent=2))
