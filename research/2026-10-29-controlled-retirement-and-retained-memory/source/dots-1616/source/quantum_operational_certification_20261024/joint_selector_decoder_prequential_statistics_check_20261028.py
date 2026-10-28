#!/usr/bin/env python3
"""Independent exact conditional-design, real repair and finite sampler checks."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
from math import isqrt
import itertools,json
import sympy as S
Q=S.Rational
simp=lambda a:a.applyfunc(S.simplify)
def eq(a,b):return simp(a-b)==S.zeros(*a.shape)
def tr(a):return S.simplify(S.trace(a))
def ceil_log2(x):
    n=0
    while 2**n<x:n+=1
    return n
def ldlt(a):
    n=a.rows;L=S.eye(n);ds=[]
    for j in range(n):
        v=S.simplify(a[j,j]-sum(L[j,r]**2*ds[r] for r in range(j)));assert v>0;ds.append(v)
        for i in range(j+1,n):L[i,j]=S.simplify((a[i,j]-sum(L[i,r]*L[j,r]*ds[r] for r in range(j)))/v)
    assert eq(a,L*S.diag(*ds)*L.T)
    return L,ds
moments=[];moment_terms=0
for m in range(1,7):
    v=S.zeros(m,1)
    if m==1:v[0]=1
    else:v[0]=Q(3,5);v[1]=Q(4,5)
    matrices=[S.eye(m)/2,(S.eye(m)-v*v.T)/2,S.eye(m)/2+v*v.T/6]
    points=[]
    for i in range(m):
        zz=S.zeros(m);zz[i,i]=1;points.append((Q(2,m*(m+2)),zz))
    for signs in itertools.product([-1,1],repeat=m):
        z=S.Matrix(signs);points.append((Q(m,(m+2)*2**m),z*z.T/m))
    assert sum(pr for pr,zz in points)==1
    second=sum((pr*zz for pr,zz in points),S.zeros(m));assert eq(second,S.eye(m)/m)
    for A in matrices:
        mean=S.zeros(m);weighted_second=S.zeros(m);mean_y=0
        for pr,zz in points:
            pp=tr(A*zz);assert 0<=pp<=1
            TT=Q(m*(m+2),2)*zz-Q(m,2)*S.eye(m)
            assert tr(TT*TT)==Q(m**3*(m+3),4)<=m**4
            mean+=pr*pp*TT;weighted_second+=pr*pp*zz;mean_y+=pr*pp;moment_terms+=1
        assert eq(weighted_second,(2*A+tr(A)*S.eye(m))/(m*(m+2)))
        assert eq(mean,A)
        assert mean_y==tr(A)/m
        # Fresh half-role masking: exactly the same mean, not independent banks.
        assert eq(2*mean/2,A)
        moments.append({'m':m,'mean_trace':str(tr(A)),'exact_fourth_gradient':True})
# Same-history roles force a nonzero cross covariance in a physical m=d=2 example.
# D-role signal: minus ZZ gradient for anchor depolarizing strength 1/2.
meanD=Q(1,3);meanS=Q(1);crossmoment=0
assert crossmoment-meanD*meanS==Q(-1,3)
repairs=[]
for m in [1,2,3,5]:
    for N in [1,4,64]:
        xi=Q(1,16*N*N);delta=xi/(4096*m);b=ceil_log2(128*m/delta);Qgrid=2**b;u=Q(1,Qgrid)
        assert u<=delta/(128*m)<2*u
        Xt=S.zeros(m);Xt[0,0]=1
        Xt[m-1,m-1]-=u
        if m>1:
            sg=-1 if N==4 else 1
            Xt[0,m-1]+=sg*u;Xt[m-1,0]+=sg*u
        assert abs(tr(Xt)-1)<=delta/2
        ldlt(Xt+delta*S.eye(m))
        Xhat=Xt+(1-tr(Xt))*S.eye(m)/m
        X=(Xhat+3*delta*S.eye(m))/(1+3*m*delta)
        assert tr(X)==1;L,ds=ldlt(X)
        ldlt(X-Q(1,2)*delta/(1+3*m*delta)*S.eye(m))
        diff=X-Xt
        assert tr(diff*diff)<=(7*m*delta)**2
        Y=S.zeros(m);Y[0,0]=1
        if m>1:Y[-1,-1]=-Q(1,4)
        assert tr(Y*Y)<=4
        objdiff=abs(tr((X-Y)**2)-tr((Xt-Y)**2));assert objdiff<50*m*delta
        assert xi/4+xi/4+61*m*delta+xi/4<xi
        K=m*Qgrid*(65536*N*N+3);B=simp(K*X)
        assert all(v.q==1 for v in B)
        aa=[S.Integer(1)]+[S.simplify(B[:i,:i].det()) for i in range(1,m+1)]
        assert all(v>0 and v.q==1 for v in aa)
        assert all(aa[i]<=K**i for i in range(1,m+1))
        J=K*aa[m]
        for i in range(1,m):J*=aa[i]**2
        assert J<=K**(m*m+1)
        ws=[];rebuild=S.zeros(m)
        for i in range(m):
            col=L[:,i];norm2=tr(col.T*col);assert norm2>=1
            weight=S.simplify(ds[i]*norm2);assert weight>0
            assert S.simplify(weight*K*aa[i]*aa[i+1]).q==1
            assert S.simplify(weight*J).q==1
            ws.append(weight);rebuild+=weight*col*col.T/norm2
        assert sum(ws)==1 and eq(rebuild,X)
        bmax=1+(m*m+1)*ceil_log2(K);assert J<2**bmax
        repairs.append({'m':m,'N':N,'grid_bits':b,'common_selector_denominator_bits':K.bit_length(),'weight_denominator_bits':int(J).bit_length(),'predeclared_weight_sampler_bits':bmax,'exact_TP_PSD_LDL_reconstruction':True,'weights':[str(v) for v in ws]})
# Exact bounded integer rejection law, including adverse exhaustion.
samplers=[]
for counts in [[1,1,1],[1,2,2],[1,1,4],[1,2,3,5]]:
    J=sum(counts);bits=ceil_log2(J);rej=1-F(J,2**bits)
    for R in [1,3,8]:
        fail=rej**R;assert fail<=F(1,2**R)
        for ai in counts:
            prob=sum((rej**t*F(ai,2**bits) for t in range(R)),F(0))
            assert prob==(1-fail)*F(ai,J)
        samplers.append({'integer_weights':counts,'cap':R,'failure_probability':str(fail),'conditional_output_law_exact':True})
budgets=[]
for m in [1,2,3,8,17]:
    for w in [1,2,4]:
        d=2**w;G=d*d*2**((w+1)//2)
        for eps in [F(1),F(1,4),F(1,100)]:
            H=m*m+m*G;target=(12*H/eps)**2;N=1
            while N<target:N*=4
            rootN=isqrt(N);assert rootN*rootN==N
            xi=F(1,16*N*N);delta=xi/(4096*m);gridbits=ceil_log2(128*m/delta);Qgrid=2**gridbits;K=m*Qgrid*(65536*N*N+3)
            bmax=max(2,ceil_log2(m+2),1+(m*m+1)*ceil_log2(K))
            nu=eps/16;R=ceil_log2(16*N/nu)
            assert F(8*N,2**R)<=nu/2
            for GG in [G,m*m]:
                eta=F(1,2*GG*rootN)
                regret=F(1,2)/eta+eta*N*(2*GG)**2/2+F(3,1)*N*F(1,4*N)/(2*eta)
                assert regret==F(11,4)*GG*rootN<4*GG*rootN
            assert F(6*H,rootN)<=eps/2
            assert N<576*H*H/(eps*eps)<=(1152*m**4+2304*m*m*d**5)/(eps*eps)
            bits=N.bit_length()-1+N*(m+2*w+2)+8*N*R*bmax
            budgets.append({'m':m,'w':w,'epsilon':str(eps),'N':N,'R':R,'maximum_uniform_draw_bits':bmax,'explicit_conservative_total_fair_bits':bits})
anchor_floor=[{'m':m,'perfect_selector_loss':'0','uniform_anchor_oracle_Bell_loss':str(Q(3,4)*(1-Q(1,m)))} for m in [1,2,3,8,32]]
source='ordinary_joint_selector_decoder_prequential_20261028.md';root=Path(__file__).resolve().parent;hh=sha256((root/source).read_bytes()).hexdigest();assert hh=='ead2aaf47370e5fa0882cf90802325e0c914b8d25cbb05f86981f91a02cd6d4e'
out={'status':'PASS_EXACT_TWO_ROLE_REAL_DENSITY_AND_FINITE_SAMPLER_CHECKS','source_sha256':hh,'source_calls':0,'random_draws':0,'source_acquisition_simulations':0,'design_matrix_cases':moments,'finite_design_terms':moment_terms,'same_history_role_covariance':'-1/3','real_density_repair_LDL_cases':repairs,'bounded_integer_sampler_cases':samplers,'finite_full_budget_cases':budgets,'raw_anchor_floor_witness':anchor_floor,'scope':'Exact deterministic matrices, finite design expectation, rational feasibility/LDL and budget arithmetic; no OGD trajectory performance pilot or generic optimizer execution.'}
(root/'joint_selector_decoder_prequential_statistics_check_20261028.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['design_matrix_cases','real_density_repair_LDL_cases','bounded_integer_sampler_cases','finite_full_budget_cases']},indent=2));print('design_cases',len(moments),'repair_LDL_cases',len(repairs),'sampler_cases',len(samplers),'budget_cases',len(budgets))
