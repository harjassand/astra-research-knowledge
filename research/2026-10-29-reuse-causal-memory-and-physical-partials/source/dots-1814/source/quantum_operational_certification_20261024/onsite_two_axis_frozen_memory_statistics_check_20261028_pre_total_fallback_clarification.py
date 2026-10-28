#!/usr/bin/env python3
"""Independent exact on-site Born laws, proper rotations and finite fits; no samples."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
import itertools,json
import sympy as S
import mpmath as mp
mp.mp.dps=100
Q=S.Rational;ii=S.I
I=S.eye(2);P=[S.Matrix([[0,1],[1,0]]),S.Matrix([[0,-ii],[ii,0]]),S.diag(1,-1)]
def simp(a):return a.applyfunc(S.simplify)
def eq(a,b):return simp(a-b)==S.zeros(*a.shape)
def tr(a):return S.simplify(S.trace(a))
def fro2(a):return tr(a.H*a)
def psd(a):
    a=simp(a);assert eq(a,a.H)
    while a.rows:
        z=S.simplify(a[0,0]);assert z>=0
        if z==0:
            assert all(a[0,j]==0 and a[j,0]==0 for j in range(a.rows));a=a[1:,1:]
        else:a=simp(a[1:,1:]-a[1:,0:1]*a[0:1,1:]/z)
    return True

def quat(ts):
    z=sum(t*t for t in ts);return S.Matrix([(1-z)/(1+z)]+[2*t/(1+z) for t in ts])
def V(u):return u[0]*I-ii*sum((u[j+1]*P[j] for j in range(3)),S.zeros(2))
def rot(u):
    v=V(u);assert eq(v.H*v,I) and S.simplify(v.det())==1
    r=S.Matrix(3,3,lambda a,j:tr(P[a]*v*P[j]*v.H)/2)
    assert eq(r.T*r,S.eye(3)) and S.simplify(r.det())==1
    return r

def KM(m):
    a=S.zeros(4);a[0,0]=m[0,0]+m[1,1]+m[2,2]
    a[1,1]=m[0,0]-m[1,1]-m[2,2];a[2,2]=-m[0,0]+m[1,1]-m[2,2];a[3,3]=-m[0,0]-m[1,1]+m[2,2]
    a[0,1]=m[2,1]-m[1,2];a[0,2]=m[0,2]-m[2,0];a[0,3]=m[1,0]-m[0,1]
    a[1,2]=m[0,1]+m[1,0];a[1,3]=m[0,2]+m[2,0];a[2,3]=m[1,2]+m[2,1]
    for i in range(4):
        for j in range(i+1,4):a[j,i]=a[i,j]
    return a
us=[S.Matrix([1,0,0,0]),S.Matrix([0,1,0,0]),quat([Q(1,3),Q(-1,4),Q(1,5)]),quat([Q(1,20),Q(1,31),Q(-1,23)]),quat([Q(1,2**12),0,Q(1,2**13)])]
rs=[rot(u) for u in us]
# Exact full product records for q=2,n=3, unknown matching pi=(2,0), spectator at1.
# Two conditional memory populations of a non-reset weak instrument K0,K1.
# K0=diag(3/5,4/5), K1=diag(4/5,3/5); branch-dependent positive Pauli weights.
# The marginal weights below arise from actual coherent memory states with those populations.
RR=[[[F(x) for x in row] for row in r.tolist()] for r in [rs[2],rs[3]]]
pi=[2,0];pp=[[F(2,5),F(3,10),F(3,10)],[F(3,4),F(1,8),F(1,8)]]
# Errors are I, X tensor X, Z tensor Z; branch0 has negative Y contrast -1/5.
chi=[[1,1,1],[1,-1,-1],[-1,-1,1]]
gauge_bloch=[[1,0,0],[0,1,0]]
born_cases=[];terms=0
for mem00 in [F(1,2),F(4,5)]:
    wr=[F(9,25)*mem00+F(16,25)*(1-mem00),F(16,25)*mem00+F(9,25)*(1-mem00)]
    assert sum(wr)==1
    lam=[sum(wr[r]*sum(pp[r][a]*chi[a][j] for a in range(3)) for r in range(2)) for j in range(3)]
    assert lam[0]>=F(2,5) and lam[2]>=F(2,5)
    means=[[[F(0) for j in range(3)] for a in range(3)] for i in range(2)]
    coarse=[[[F(0) for a in range(3)] for site in range(3)] for i in range(2)]
    totals=F(0)
    for js in itertools.product([0,2],repeat=2):
        for signs in itertools.product([-1,1],repeat=2):
            for axes in itertools.product(range(3),repeat=3):
                for bs in itertools.product([-1,1],repeat=3):
                    prob=F(0)
                    for r in range(2):
                        for alpha in range(3):
                            v=wr[r]*pp[r][alpha]*F(1+bs[1]*gauge_bloch[r][axes[1]],2)
                            for i in range(2):
                                signal=signs[i]*chi[alpha][js[i]]*RR[i][axes[pi[i]]][js[i]]
                                v*= (1+bs[pi[i]]*signal)/2
                            prob+=v
                    prob/=16*27;assert prob>=0;totals+=prob;terms+=1
                    for i in range(2):
                        means[i][axes[pi[i]]][js[i]]+=prob*6*signs[i]*bs[pi[i]]
                    if js==(0,0):
                        for i in range(2):
                            for site in range(3):coarse[i][site][axes[site]]+=4*prob*3*signs[i]*bs[site]
    assert totals==1
    for i in range(2):
        for a in range(3):
            for j in range(3):assert means[i][a][j]==(RR[i][a][j]*lam[j] if j in [0,2] else 0)
        for site in range(3):
            for a in range(3):assert coarse[i][site][a]==(RR[i][a][0]*lam[0] if site==pi[i] else 0)
        moment=sum(means[i][a][j]**2 for a in range(3) for j in range(3))
        assert 0<=36-moment<=36
    born_cases.append({'memory_00':str(mem00),'instrument_branch_weights':[str(w) for w in wr],'X_contrast':str(lam[0]),'Z_contrast':str(lam[2]),'proper_two_column_means_and_matching':True})
# Symbolic K identity and proper two-axis curvature, including actual unitary Bell loss.
k_cases=[];curvature=[]
matrices=[S.zeros(3),S.Matrix([[1,Q(1,3),Q(-1,4)],[Q(1,7),Q(-1,2),Q(2,5)],[Q(1,9),Q(-3,8),Q(1,4)]])]
for a in range(3):
    for j in [0,2]:
        for sign in [-1,1]:
            m=S.zeros(3);m[a,j]=6*sign;matrices.append(m)
for m in matrices:
    kk=KM(m);assert fro2(kk)==4*fro2(m)
    if fro2(m)<=36:psd(12*S.eye(4)-kk);psd(12*S.eye(4)+kk)
    for u,r in zip(us,rs):assert S.simplify((u.T*kk*u)[0]-tr(r.T*m))==0
    k_cases.append({'norm_squared_M':str(fro2(m)),'K_identity_for_quaternions':len(us)})
for ia,ra in enumerate(rs):
    for ib,rb in enumerate(rs):
        rel=simp(ra.T*rb);squared=fro2(ra-rb)
        assert 1-rel[1,1]<=2-rel[0,0]-rel[2,2]
        for kappa,lx,lz in [(Q(1,4),Q(2,5),Q(2,5)),(Q(1,2),Q(1,2),Q(3,4))]:
            D=S.diag(lx,0,lz);gap=tr((ra-rb).T*ra*D)
            assert gap>=kappa*squared/4
            loss=1-tr(V(us[ib]).H*V(us[ia]))**2/4
            assert S.simplify(loss-squared/8)==0
            curvature.append({'true_index':ia,'fit_index':ib,'kappa':str(kappa),'Bell_loss':str(loss)})
improper=S.diag(1,-1,1);assert improper.det()==-1
assert tr((S.eye(3)-improper)*S.diag(1,0,1))==0 and fro2(S.eye(3)-improper)==4
# Finite exactly rational real Jacobi. Floating two-by-two angles are proposals only;
# every unitarity/energy/residual/Rayleigh/control assertion below is exact rational.
def embed(r,i,j):
    out=S.eye(4)
    for a,x in enumerate([i,j]):
        for b,y in enumerate([i,j]):out[x,y]=r[a,b]
    return out

def energy(a):return S.simplify(sum(a[i,j]**2 for i in range(4) for j in range(4) if i!=j))

def ceil_log2(x):
    k=0
    while 2**k<x:k+=1
    return k
fits=[]
known_m=[S.zeros(3),S.Matrix([[6,0,0],[0,0,0],[0,0,0]]),rs[2]*S.diag(Q(2,5),0,Q(3,5)),rs[3]*S.diag(Q(3,4),0,Q(1,2))+S.Matrix([[Q(1,100),0,Q(-1,150)],[Q(1,120),0,0],[0,0,Q(1,170)]])]
for m in known_m:
    kk=KM(m);delta=Q(1,32);zeta=delta/24
    rho=kk/48+S.eye(4)/4;psd(rho);psd(S.eye(4)/2-rho)
    current=rho;QQ=S.eye(4);steps=0;k=4;cap=k*k*ceil_log2(32*k/zeta**2)
    while energy(current)>zeta*zeta/16:
        assert steps<cap
        i,j=max(((i,j) for i in range(k) for j in range(i+1,k)),key=lambda pair:abs(current[pair[0],pair[1]]))
        oldE=energy(current)
        aa=mp.matrix([[mp.mpf(str(S.N(current[x,y],95))) for y in [i,j]] for x in [i,j]])
        vals,rot2=mp.eigh(aa)
        if mp.det(rot2)<0:rot2[:,1]=-rot2[:,1]
        c,s=rot2[0,0],rot2[1,0]
        if c<0:c,s=-c,-s
        tt=Q(int(mp.nint((s/(1+c))*2**90)),2**90)
        c0=(1-tt*tt)/(1+tt*tt);s0=2*tt/(1+tt*tt)
        rr=S.Matrix([[c0,-s0],[s0,c0]]);assert eq(rr.T*rr,S.eye(2)) and rr.det()==1
        whole=embed(rr,i,j);nextm=simp(whole.T*current*whole)
        assert energy(nextm)<=(1-Q(2,k*k))*oldE+zeta*zeta/(64*k*k)
        current=nextm;QQ=simp(QQ*whole);steps+=1
    assert eq(QQ.T*QQ,S.eye(4))
    diag=S.diag(*[(QQ.T*kk*QQ)[i,i] for i in range(4)])
    residual=kk-QQ*diag*QQ.T;assert fro2(residual)<=delta*delta/4
    im=max(range(4),key=lambda i:diag[i,i]);u=QQ[:,im];label=diag[im,im]
    assert S.simplify((u.T*u)[0])==1 and S.simplify((u.T*kk*u)[0]-label)==0
    psd((label+delta/2)*S.eye(4)-kk)
    vv=V(u);assert eq(vv.H*vv,I) and S.simplify(vv.det())==1
    rr=rot(u);assert S.simplify(tr(rr.T*m)-label)==0
    fits.append({'M_Y_column_zero':all(m[i,1]==0 for i in range(3)),'steps':steps,'cap':cap,'exact_residual_Rayleigh_and_SU2':True,'zero_matrix':bool(m==S.zeros(3))})
# Explicit non-iid martingale second moment, two adaptive rounds with real Born bits.
# Fix one coordinate F_X,X: it is +6/-6 with probabilities (1+lambda)/12,(1-lambda)/12,
# and zero with probability5/6. Let next contrast depend on that first coordinate.
mean1=Q(2,5);second=0;total=0
for f1,p1 in [(6,(1+mean1)/12),(-6,(1-mean1)/12),(0,Q(5,6))]:
    lam2=Q(3,4) if f1>0 else Q(1,2)
    for f2,p2 in [(6,(1+lam2)/12),(-6,(1-lam2)/12),(0,Q(5,6))]:
        z1=f1-mean1;z2=f2-lam2;pr=p1*p2;total+=pr;second+=pr*(z1+z2)**2/4
assert total==1
expected=(6-mean1**2+sum(p*(6-(Q(3,4) if f>0 else Q(1,2))**2) for f,p in [(6,(1+mean1)/12),(-6,(1-mean1)/12),(0,Q(5,6))]))/4
assert S.simplify(second-expected)==0 and second<=Q(36,2)
# Record-TV transfer: exact finite weights can move memory arbitrarily, while good-record loss is uniform.
transfer=[]
for eps in [Q(1),Q(1,8),Q(1,100)]:
    beta=eps/8;nc=eps/16;ns=3*eps/16;b=9*eps/32
    ideal=[1-beta,beta];actual=[1-beta-nc,beta+nc]
    assert sum(abs(a-bb) for a,bb in zip(ideal,actual))/2==nc
    worst=actual[0]*b+actual[1]+ns
    assert worst<=b+beta+nc+ns==21*eps/32<eps
    transfer.append({'epsilon':str(eps),'actual_good_record_lower_bound':str(actual[0]),'worst_average_excess_bound':str(worst)})
budgets=[]
for n,q in [(1,1),(3,2),(32,8),(1000,10)]:
    for kappa in [Q(1),Q(2,5),Q(1,100)]:
        for eps in [Q(1),Q(1,8),Q(1,1000)]:
            beta=eps/8;L0=ceil_log2(8*q*n/beta);N0=int(S.ceiling(3072*L0/kappa**2))
            L1=ceil_log2(24*q/beta);N1=int(S.ceiling(4096*q*L1/(kappa**2*eps)))
            assert N0*kappa**2/(3072)>=L0
            assert Q(4*q*n,2**L0)<=beta/2
            ex=N1*kappa**2*eps/(3456*q);assert ex>=Q(32,27)*L1>=L1
            assert Q(12*q,2**L1)<=beta/2
            delta=kappa*eps/(32*q);err=kappa*kappa*eps/(8*q)
            assert 2*err/kappa**2+delta/kappa==9*eps/(32*q)
            B=N0+N1;nr=eps/32;r=ceil_log2(4*n*B/nr)
            assert Q(n*B,4**r)<=nr
            bits=q*N0+2*q*N1+2*n*B*r
            budgets.append({'n':n,'q':q,'kappa':str(kappa),'epsilon':str(eps),'N0':N0,'N1':N1,'total_calls_including_service':B+1,'calibration_bit_cap':bits})
root=Path(__file__).resolve().parent;source='ordinary_onsite_two_axis_frozen_memory_recovery_20261028.md'
h=sha256((root/source).read_bytes()).hexdigest()
assert h=='c2691ea45067c5dda9d3ee19b5c94ccfaa4de8d23d46f01f1bbbf69ecb32feba'
out={'status':'PASS_SOURCE_DISABLED_ONSITE_TWO_AXIS_STATISTICS','source':source,'source_sha256':h,'source_calls':0,'random_draws':0,'source_acquisition_simulations':0,'generic_optimizer_executed':False,'rational_Jacobi_fixture_executed':True,'floating_proposals_accepted_only_by_exact_rational_certificates':True,
 'summary':{'actual_three_site_Born_terms':terms,'conditional_two_logical_memory_cases':len(born_cases),'K_matrix_cases':len(k_cases),'quaternion_K_identities':len(k_cases)*len(us),'two_axis_curvature_Bell_cases':len(curvature),'finite_exact_rational_Jacobi_fits':len(fits),'adaptive_scalar_martingale_histories':9,'record_TV_transfer_cases':len(transfer),'full_budget_cases':len(budgets),'negative_Y_contrast':str(Q(-1,5)),'improper_reflection_failure_preserved':True},
 'Born_cases':born_cases,'K_matrix_cases':k_cases,'curvature':curvature,'finite_fits':fits,'record_transfer':transfer,'budgets':budgets}
(root/'onsite_two_axis_frozen_memory_statistics_check_20261028.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out['summary'],indent=2));print(out['status'])
