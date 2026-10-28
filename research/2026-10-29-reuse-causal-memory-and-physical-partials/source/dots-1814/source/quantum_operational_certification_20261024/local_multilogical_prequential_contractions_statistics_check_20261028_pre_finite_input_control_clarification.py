#!/usr/bin/env python3
"""Independent exact finite-law/statistics checks. No source calls or RNG."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
from math import isqrt
import itertools,json
import sympy as S
Q=S.Rational; ii=S.I
I=S.eye(2); X=S.Matrix([[0,1],[1,0]]); Y=S.Matrix([[0,-ii],[ii,0]]); Z=S.diag(1,-1)
paulis=[X,Y,Z]
def simp(a):return a.applyfunc(S.simplify)
def eq(a,b):return simp(a-b)==S.zeros(*a.shape)
def tr(a):return S.simplify(S.trace(a))
def fro2(a):return tr(a.H*a)
def tensor(xs):
    out=S.ones(1,1)
    for x in xs:out=S.kronecker_product(out,x)
    return out

def psd(a):
    a=simp(a);assert eq(a,a.H)
    while a.rows:
        p=S.simplify(a[0,0]);assert p>=0
        if p==0:
            assert all(a[0,j]==0 and a[j,0]==0 for j in range(a.rows));a=a[1:,1:]
        else:a=simp(a[1:,1:]-a[1:,0:1]*a[0:1,1:]/p)
    return True

def partial(a,keep,n):
    rest=[j for j in range(n) if j not in keep];dk=2**len(keep);out=S.zeros(dk)
    def bits(v,k):return [(v>>(k-j-1))&1 for j in range(k)]
    def idx(kb,rb):
        bb=[0]*n
        for j,b in zip(keep,kb):bb[j]=b
        for j,b in zip(rest,rb):bb[j]=b
        return sum(b<<(n-j-1) for j,b in enumerate(bb))
    for x in range(dk):
        for y in range(dk):
            out[x,y]=sum(a[idx(bits(x,len(keep)),bits(r,len(rest))),idx(bits(y,len(keep)),bits(r,len(rest)))] for r in range(2**len(rest)))
    return simp(out)

def embed_local(a,keep,n):
    rest=[j for j in range(n) if j not in keep];out=S.zeros(2**n)
    def projected(v,js):
        return sum(((v>>(n-j-1))&1)<<(len(js)-k-1) for k,j in enumerate(js))
    for x in range(2**n):
        for y in range(2**n):
            if projected(x,rest)==projected(y,rest):out[x,y]=a[projected(x,keep),projected(y,keep)]
    return out

def meas(n):
    out=[]
    for aa in itertools.product(range(3),repeat=n):
        for ss in itertools.product([-1,1],repeat=n):
            pp=[(I+s*paulis[a])/2 for a,s in zip(aa,ss)]
            zz=[3*p-I for p in pp]
            out.append((aa,ss,tensor(pp),tensor(zz),Q(1,3**n)))
    return out
measurements={n:meas(n) for n in [1,2,3]}
shadow_cases=[];shadow_terms=0
for n in [1,2,3]:
    d=2**n;v=S.zeros(d,1);v[0]=1;v[-1]=ii
    rho_ent=v*v.H/2
    rho_prod=tensor([(I+paulis[j%3])/2 for j in range(n)])
    states=[rho_ent,rho_prod,(rho_ent+2*S.eye(d)/d)/3]
    for rho in states:
        EZ=S.zeros(d);EZ2=S.zeros(d);total=0
        for aa,ss,pp,zz,pa in measurements[n]:
            born=tr(rho*pp);assert 0<=born<=1;pr=pa*born;total+=pr
            assert fro2(zz)==5**n
            # Tensor eigenvalues are products of 2,-1; PSD certificates give exact operator bound.
            EZ+=pr*zz;EZ2+=pr*(zz*zz);shadow_terms+=1
        assert total==1 and eq(EZ,rho)
        target=S.zeros(d)
        for mask in range(2**n):
            keep=[j for j in range(n) if (mask>>j)&1]
            target+=2**(n-len(keep))*embed_local(partial(rho,keep,n),keep,n)
        assert eq(EZ2,target);psd(3**n*S.eye(d)-EZ2)
        shadow_cases.append({'n':n,'trace_second_moment':str(tr(EZ2)),'exact_correlated_Born_moments':True})
# Two different local records on one entangled output are not independent.
bell=S.zeros(4,1);bell[0]=1;bell[3]=1;rho=bell*bell.H/2
m0=m1=m01=0
for aa,ss,pp,zz,pa in measurements[2]:
    pr=pa*tr(rho*pp);v0=3*ss[0] if aa[0]==2 else 0;v1=3*ss[1] if aa[1]==2 else 0
    m0+=pr*v0;m1+=pr*v1;m01+=pr*v0*v1
assert m0==m1==0 and m01==1
# Actual input labels and actual whole-output Born records, for two different conditional histories.
U=S.diag(1,1,1,ii);ZZ=tensor([Z,Z]);fullI=S.eye(4)
B={(i,j):simp(U*tensor([paulis[j] if k==i else I for k in range(2)])*U.H) for i in range(2) for j in [0,2]}
roles=[];gradient_terms=0;coarse_terms=0
for p in [Q(7,8),Q(5,6)]:
    def channel(r):return simp(U*(p*r+(1-p)*ZZ*r*ZZ)*U.H)
    expected={(i,j):((2*p-1) if j==0 else 1)*B[i,j]/4 for i in range(2) for j in [0,2]}
    means={(i,j):S.zeros(4) for i in range(2) for j in [0,2]}
    coarse=[S.zeros(4),S.zeros(4)];coarse2=[S.zeros(4),S.zeros(4)]
    for aa in itertools.product([0,2],repeat=2):
        for ss in itertools.product([-1,1],repeat=2):
            rho=channel(tensor([(I+s*paulis[a])/2 for a,s in zip(aa,ss)]))
            for ma,bs,pp,zz,pa in measurements[2]:
                prob=pa*tr(rho*pp)/16;assert prob>=0
                for i in range(2):means[i,aa[i]]-=prob*ss[i]*zz
                gradient_terms+=1
                if aa==(0,0):
                    for i in range(2):
                        coarse[i]+=4*prob*ss[i]*zz;coarse2[i]+=4*prob*zz*zz
                    coarse_terms+=1
    for i in range(2):
        for j in [0,2]:
            assert eq(means[i,j],-expected[i,j]/2)
            roles.append({'conditional_p_I':str(p),'logical':i,'axis':j,'conditional_gradient_exact':True})
        assert eq(coarse[i],expected[i,0])
        variance=simp(coarse2[i]-expected[i,0]**2)
        psd(variance);psd(9*fullI-variance)
    # Conditioning on the other CURRENT sign destroys the asserted marginal mean.
    conditional=S.zeros(4)
    for s in [-1,1]:conditional+=Q(s,2)*channel(tensor([(I+s*X)/2,(I+X)/2]))
    assert not eq(conditional,expected[0,0])
# Coarse localization contrast under unknown unitary on one true two-site patch.
# Use logical+gauge inside sites0,1 and a spectator site2; exact disjoint partial trace vanishes.
B1=simp(U*tensor([X,I])*U.H)
localization=[]
for z in [Q(0),Q(1,3),Q(1,2**30)]:
    gauge=(I+z*Y)/2;rho=simp(U*tensor([I/2,gauge])*U.H)
    for kappa in [Q(1,2),Q(3,4),Q(1)]:
        Delta=kappa*B1*rho
        assert tr(B1*Delta)==kappa
        glob=tensor([Delta,(I+X)/2])
        assert eq(partial(glob,[2],3),S.zeros(2))
        localization.append({'kappa':str(kappa),'complex_gauge_z':str(z),'disjoint_mean_zero':True})
# Weighted excess and raw-sign residual with noncommuting gauge order, including tiny eigenweights.
Q2=S.Matrix([[Q(3,5),4*ii/5],[4*ii/5,Q(3,5)]]);assert eq(Q2.H*Q2,I)
Q4=tensor([Q2,Q2])*S.diag(1,ii,1,1);assert eq(Q4.H*Q4,fullI)
weighted=[]
for ratio in [Q(3,4),Q(1,2**25)]:
    gg=S.diag(ratio**2,1)/(1+ratio**2)
    vv=S.Matrix([[ratio**2,ratio],[ratio,1]])/(4*(1+ratio**2))
    for kappa in [Q(1,2),Q(3,4)]:
        hh=kappa*gg+(1-kappa)*vv;psd(hh-kappa*gg);psd(gg-hh)
        assert not eq(gg*hh,hh*gg)
        rho=tensor([I/2,gg]);R=tensor([I/2,hh]);BB=tensor([Z,I])
        for vals in [[-1,Q(-1,2),0,Q(3,4)],[Q(-1,8),0,Q(1,16),Q(1,2)]]:
            C=Q4*S.diag(*vals)*Q4.H;A=C;SS=Q4*S.diag(*[1 if v>=0 else -1 for v in vals])*Q4.H
            psd(fullI-A);psd(fullI+A);assert eq(SS*SS,fullI)
            P=fullI-(A*BB+BB*A)/2;psd(P)
            ee=tr(R*P)/2;ar=tr(rho*(A-BB)**2);ds=tr(rho*(BB-SS)**2)
            assert ee>=kappa*tr(rho*P)/2 and ar<=4*ee/kappa and ds<=4*ar
            weighted.append({'tiny_gauge':bool(ratio<Q(1,100)),'kappa':str(kappa),'excess':str(ee),'raw_sign_kernel_convention_exact':True})
# Finite entry rounding and exact contraction feasibility. Known spectral examples, not a Jacobi execution.
def rnd(x,u):return u*S.floor(x/u+Q(1,2))
def roundH(a,u):
    d=a.rows;b=S.zeros(d)
    for i in range(d):
        for j in range(i,d):
            b[i,j]=rnd(S.re(a[i,j]),u)+ii*rnd(S.im(a[i,j]),u);b[j,i]=S.conjugate(b[i,j])
    return b

def ceil_log2(x):
    j=0
    while 2**j<x:j+=1
    return j
clipping=[]
for W in [1,2]:
    d=2**W;R0=2**((W+1)//2);QQ=Q2 if W==1 else Q4
    for N in [4,64,1024]:
        u=Q(1,16*R0*N);tau=u/4;t0=u/(16*R0);v=Q(1,2**ceil_log2(64*R0*d/u))
        assert v<=u/(64*R0*d)<2*v
        vals=[Q(-3,2),Q(5,4)] if d==2 else [Q(-3,2),Q(-1,8),0,Q(5,4)]
        YY=QQ*S.diag(*vals)*QQ.H
        # Backward diagonalization tolerance uses a known tiny diagonal perturbation.
        cc=[a+tau/(2*d) for a in vals]
        CC=QQ*S.diag(*cc)*QQ.H;assert fro2(CC-YY)<=tau**2
        PP=QQ*S.diag(*[max(-1,min(1,a)) for a in cc])*QQ.H
        exact=QQ*S.diag(*[max(-1,min(1,a)) for a in vals])*QQ.H
        assert fro2(PP-exact)<=tau**2
        pt=roundH(PP,v);AA=pt/(1+t0)
        assert fro2(pt-PP)<=(2*d*v)**2
        psd(S.eye(d)+AA);psd(S.eye(d)-AA)
        assert fro2(AA-exact)<=u**2
        clipping.append({'W':W,'N':N,'mesh_bits':ceil_log2(1/v),'exact_feasibility_and_projection_slack':True})
# Deterministic pathwise OGD on possible diagonal record gradients, with actual finite repair.
ogd=[]
for N in [4,16,64]:
    W=1;d=2;R0=2;G0=3;root=isqrt(N);eta=Q(R0,G0*root);u=Q(1,16*R0*N);t0=u/(16*R0)
    mesh=Q(1,2**ceil_log2(64*R0*d/u));A=S.zeros(2)
    gradients=[S.diag(-2,1),S.diag(1,-2),S.zeros(2),S.diag(2,-1),S.diag(-1,2)]
    comparators=[Z,X];sums=[0,0]
    for t in range(N):
        g=gradients[(t*t+2*t)%len(gradients)];assert fro2(g)<=G0**2
        for j,B in enumerate(comparators):sums[j]+=tr(g*(A-B))
        YY=A-eta*g;P=S.diag(*[max(-1,min(1,YY[i,i])) for i in range(2)])
        A=roundH(P,mesh)/(1+t0);psd(I-A);psd(I+A)
        assert fro2(A-P)<=u*u
    for j,B in enumerate(comparators):
        assert sums[j]<=2*R0*G0*root
        ogd.append({'N':N,'comparator':'Z' if j==0 else 'X','exact_regret':str(sums[j])})
# Integer resource caps and exact rational confidence/accuracy arithmetic.
budgets=[]
for n,q,w in [(1,1,1),(3,2,1),(5,2,2),(16,8,2),(32,12,3),(7,4,7)]:
    for kappa in [Q(1),Q(1,3)]:
        for eps in [Q(1),Q(1,8),Q(1,1000)]:
            W=min(n,3*w-2);C=min(q,2*W-1);K=min(q,W+2*(C-1)*(W-1));Ag=min(q,K*K)
            R0=2**((W+1)//2);G0=isqrt(5**W)+(isqrt(5**W)**2<5**W)
            M0=n-w+1;d0=2**w;beta=eps/8
            L0=ceil_log2(2*d0*q*M0/beta)
            N0=int(S.ceiling(256*12**w*L0/kappa**2))
            target=(1152*Ag*q*R0*G0/(kappa*eps))**2;N=1
            while N<target:N*=4
            assert N<4*target and isqrt(N)**2==N
            a=kappa/(8*d0);den=2*(3**w+2*d0*a/3)
            exponent=Q(N0)*a*a/den
            assert exponent>=L0
            # e^L>=2^L; hence whole union <= 2*d*q*M / 2^L <= beta.
            assert Q(2*d0*q*M0,2**L0)<=beta
            u=Q(1,16*R0*N);eta=Q(R0,G0*isqrt(N));d=2**W
            # Use sqrt(d)<=R0 for an entirely rational conservative regret certificate.
            bound=Q(d,2)/eta+eta*N*G0**2/2+N*(4*R0*u+u*u)/(2*eta)
            assert bound<=2*R0*G0*isqrt(N)
            main=Q(288*Ag*q*R0*G0,kappa*isqrt(N));assert main<=eps/4
            b=Q(1,2**ceil_log2(S.sqrt(288*Ag*q/eps)))
            assert b*b<=eps/(288*Ag*q) and (2*b)**2>eps/(288*Ag*q)
            learned=main+36*Ag*q*b*b;assert learned<=3*eps/8
            total=learned+beta+eps/4;assert total<=3*eps/4
            Bcalls=N0+N;nu_rng=eps/16;Jrng=n*Bcalls;Rrng=ceil_log2(4*Jrng/nu_rng)
            assert Q(Jrng,4**Rrng)<=nu_rng
            bits=ceil_log2(N)+q*N0+2*q*N+2*n*Bcalls*Rrng+q
            assert bits>=ceil_log2(N)+q*N0+2*q*N+2*n*Bcalls+q
            assert N<32*1152**2*Ag**2*q*q*10**W/(kappa*kappa*eps*eps)
            budgets.append({'n':n,'q':q,'w':w,'epsilon':str(eps),'kappa':str(kappa),'N0':N0,'N':N,'random_bit_cap':bits})
root=Path(__file__).resolve().parent
source='ordinary_local_multilogical_prequential_contractions_20261028.md'
source_hash=sha256((root/source).read_bytes()).hexdigest()
assert source_hash=='c1505e16aa6c4222826ac69ba9c7ad6825d191648c383d0d8d4792db2a924202'
out={'status':'PASS_EXACT_SOURCE_DISABLED_STATISTICS_CHECK','source':source,'source_sha256':source_hash,'source_calls':0,'random_draws':0,'source_acquisition_simulations':0,'generic_Jacobi_or_optimizer_executed':False,
 'summary':{'correlated_snapshot_cases':len(shadow_cases),'snapshot_Born_terms':shadow_terms,'conditional_gradient_cases':len(roles),'fine_input_output_Born_terms':gradient_terms,'coarse_input_output_Born_terms':coarse_terms,'localization_cases':len(localization),'weighted_noncommuting_gauge_cases':len(weighted),'finite_clipping_repair_cases':len(clipping),'deterministic_pathwise_OGD_cases':len(ogd),'full_budget_cases':len(budgets),'same_output_local_record_covariance':str(m01-m0*m1)},
 'correlated_shadows':shadow_cases,'conditional_gradients':roles,'localization':localization,'weighted_excess_and_sign':weighted,'clipping':clipping,'pathwise_OGD':ogd,'budgets':budgets}
(root/'local_multilogical_prequential_contractions_statistics_check_20261028.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out['summary'],indent=2));print(out['status'])
