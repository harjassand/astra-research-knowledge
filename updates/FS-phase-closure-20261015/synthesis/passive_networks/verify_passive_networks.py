"""Exact graph/static certificates plus numerical complex-envelope checks.

No material coefficients or physical measurements are inferred by this script.
"""
from pathlib import Path
from fractions import Fraction as F
import datetime
import hashlib
import json
import math
import platform
import numpy as np

BASE=Path(__file__).resolve().parent

def transpose(a): return [list(row) for row in zip(*a)]
def matmul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]
def add(a,b,sign=1):
    return [[a[i][j]+sign*b[i][j] for j in range(len(a[0]))]
            for i in range(len(a))]
def scale(a,c): return [[c*x for x in row] for row in a]
def block(a,ii,jj): return [[a[i][j] for j in jj] for i in ii]
def inv(a):
    n=len(a)
    w=[[F(x) for x in a[i]]+[F(i==j) for j in range(n)]
       for i in range(n)]
    for j in range(n):
        pivot=next(k for k in range(j,n) if w[k][j])
        w[j],w[pivot]=w[pivot],w[j]
        p=w[j][j];w[j]=[x/p for x in w[j]]
        for i in range(n):
            if i!=j:
                p=w[i][j];w[i]=[w[i][k]-p*w[j][k] for k in range(2*n)]
    return [row[n:] for row in w]
def quad(v,a): return matmul(transpose(v),matmul(a,v))[0][0]
def graph(n,edges,shunts):
    a=[[F(0) for _ in range(n)] for _ in range(n)]
    for i,g in enumerate(shunts):a[i][i]+=g
    for i,j,k in edges:
        a[i][i]+=k;a[j][j]+=k;a[i][j]-=k;a[j][i]-=k
    return a
def kron(a,tt):
    ii=[i for i in range(len(a)) if i not in tt]
    if not ii:return block(a,tt,tt)
    return add(block(a,tt,tt),matmul(matmul(block(a,tt,ii),
        inv(block(a,ii,ii))),block(a,ii,tt)),sign=-1)
def strings(a):return [[str(x) for x in row] for row in a]

# Exact mediator graph with multiple paths and three terminal ports.
edges=[(0,3,F(2)),(1,4,F(3)),(2,5,F(4)),(3,4,F(1)),
       (4,5,F(2)),(3,5,F(1)),(0,2,F(1,3))]
gamma=[F(1,5),F(1,5),F(1,5),F(1,2),F(2,3),F(3,4)]
R=graph(6,edges,gamma);tt=[0,1,2];ii=[3,4,5]
Hinv=inv(block(R,ii,ii));RTI=block(R,tt,ii);Sterm=kron(R,tt)
leak=add([[gamma[i]] for i in tt],matmul(matmul(RTI,Hinv),
    [[gamma[i]] for i in ii]),sign=-1)
assert [[sum(row)] for row in Sterm]==leak
assert all(leak[i][0]>=gamma[tt[i]] for i in range(len(tt)))
assert all(Sterm[i][j]<=0 for i in range(3) for j in range(3) if i!=j)

# Exact positive-output envelope, load realization and power balance.
x=[[F(1)]]; A=[[Sterm[0][0]]]
C=block(Sterm,[1,2],[1,2]);Cinv=inv(C)
b=[[-Sterm[i][0]] for i in [1,2]];yy0=matmul(Cinv,b)
strength=quad(b,Cinv);D0=A[0][0]-strength;t=F(3,4)
y=scale(yy0,t);v=x+y
P=matmul(transpose(b),y)[0][0]-quad(y,C)
D=quad(v,Sterm)
assert P==t*(1-t)*strength
assert D==D0+strength*(1-t)**2
f=matmul(Sterm,v);Pin=f[0][0]
assert Pin-P==D
Lload=scale(C,1/t-1)
assert matmul(Lload,y)==scale(f[1:],-1)
assert quad(y,Lload)==P

# Exact ground-leakage perturbation, retaining nonnegative physical leakage.
delta=F(1,6); idx=4; local=ii.index(idx)
assert 0<=delta<=gamma[idx]
Rnew=[row[:] for row in R];Rnew[idx][idx]-=delta
w=matmul(RTI,[[Hinv[i][local]] for i in range(len(ii))])
den=1-delta*Hinv[local][local];assert den>0
prediction=add(Sterm,scale(matmul(w,transpose(w)),delta/den),sign=-1)
assert kron(Rnew,tt)==prediction

# A concrete two-fluid matched-loss replacement and its add-only failure.
c1,c2,k,cb,u,y2=F(1,2),F(1),F(1),F(2),F(1),F(2,5)
f1=(c1+k)*u-k*y2;fL=k*u-(c2+k)*y2
P2=fL*y2;D2=f1*u-P2
assert (P2,f1,D2)==(F(2,25),F(11,10),F(51,50))
assert D2<cb*u*u and D2>c1*u*u

# Exact mediator leakage-replacement condition with one concrete rational case.
l1,l2,c2r,gb,gn=F(2),F(3),F(1),F(4),F(1)
gr=l2*c2r/(l2+c2r)
base_l=l1*gb/(l1+gb);new_l=l1*(gn+gr)/(l1+gn+gr)
assert (new_l<base_l)==(gn+gr<gb)
assert new_l==F(14,15) and base_l==F(4,3)

# Exact layered harmonic-velocity bound: path 0--1--2--3, source fixed 1.
RR=graph(4,[(0,1,F(1)),(1,2,F(1)),(2,3,F(1))],
    [F(0),F(2),F(2),F(1)])
hh=scale(matmul(inv(block(RR,[1,2,3],[1,2,3])),
    block(RR,[1,2,3],[0])),-1)
# All non-source rows have sum edges/(sum edges+ground)=1/2.
assert 0<=hh[2][0]<=F(1,8)

# Passive reactive example, exact real/imaginary output checks via fractions.
yr,yi=F(-1,4),F(-1,4)
yabs=yr*yr+yi*yi
Pout=F(1,2)*yabs
Pinreact=F(1,2)*(1-yi)
Dreact=F(1,2)*(1+yabs)
assert (Pout,Pinreact,Dreact)==(F(1,16),F(5,8),F(9,16))
gain_re,gain_im=F(-2,5),F(-1,5)
gain_product=(gain_re**2-gain_im**2,2*gain_re*gain_im)
assert gain_product==(F(3,25),F(4,25))

# Complex multi-source/multi-receiver envelope: passive Z(s)=R+sM.
rng=np.random.default_rng(20261015)
worst_power=0.;worst_loss=0.;worst_lower=0.
cases=60
for _ in range(cases):
    ns=int(rng.integers(1,4));nr=int(rng.integers(1,5));n=ns+nr
    U=rng.normal(size=(n,n));Rnum=U.T@U+np.eye(n)
    V=rng.normal(size=(n,n));M=V.T@V+np.eye(n)
    Z=Rnum+1j*M
    xx=rng.normal(size=ns)+1j*rng.normal(size=ns)
    Cn=Rnum[ns:,ns:];ev,W=np.linalg.eigh(Cn)
    Ci=(W*(1/ev))@W.T;Cih=(W*(1/np.sqrt(ev)))@W.T
    bb=-Z[ns:,:ns]@xx;cc=Rnum[ns:,:ns]@xx
    Dbase=(np.vdot(xx,Rnum[:ns,:ns]@xx).real-np.vdot(cc,Ci@cc).real)/2
    K=np.vdot(bb,Ci@bb).real/4
    center=Cih@bb/2;uncon=-Cih@cc
    separation=np.linalg.norm(uncon-center)
    for frac in [0.,.13,.5,.91,1.]:
        target=frac*K/2;radius=math.sqrt(max(K-2*target,0.))
        if separation>1e-14:
            uopt=center+radius*(uncon-center)/separation
        else:
            direction=np.zeros(nr,dtype=complex);direction[0]=1.
            uopt=center+radius*direction
        yy=Cih@uopt;vv=np.concatenate([xx,yy])
        actualP=-np.vdot(yy,Z[ns:,:ns]@xx+Z[ns:,ns:]@yy).real/2
        actualD=np.vdot(vv,Rnum@vv).real/2
        predicted=Dbase+(separation-radius)**2/2
        worst_power=max(worst_power,abs(actualP-target)/(1+abs(target)))
        worst_loss=max(worst_loss,abs(actualD-predicted)/(1+abs(predicted)))
        assert abs(actualP-target)<=1e-9*(1+abs(target))
        assert abs(actualD-predicted)<=1e-9*(1+abs(predicted))
        # Unrestricted random points on the same output sphere cannot improve it.
        for j in range(5):
            direction=rng.normal(size=nr)+1j*rng.normal(size=nr)
            direction/=np.linalg.norm(direction)
            yrand=Cih@(center+radius*direction)
            vrand=np.concatenate([xx,yrand])
            Drand=np.vdot(vrand,Rnum@vrand).real/2
            worst_lower=max(worst_lower,predicted-Drand)
            assert Drand>=predicted-1e-9*(1+abs(predicted))
        ua=uncon if separation<=radius else uopt
        ya=Cih@ua;va=np.concatenate([xx,ya])
        Pa=-np.vdot(ya,Z[ns:,:ns]@xx+Z[ns:,ns:]@ya).real/2
        Da=np.vdot(va,Rnum@va).real/2
        lower=Dbase+max(separation-radius,0.)**2/2
        assert Pa>=target-1e-9*(1+abs(target))
        assert abs(Da-lower)<=1e-9*(1+abs(lower))

# Check explicit one-frequency passive optimal load for the reactive fixture.
zload=3+2*math.sqrt(2)-2j
yc=-1j/(1+2j+zload)
Pc=zload.real*abs(yc)**2/2
Dc=(1+abs(yc)**2)/2
Dstar=.5+(.5-1/math.sqrt(8))**2/2
assert math.isclose(Pc,1/16,rel_tol=1e-12)
assert math.isclose(Dc,Dstar,rel_tol=1e-12)

out={
 'status':'PASS_CONDITIONAL_ALGEBRA_AND_MODEL_CHECKS',
 'scope':'No material acquisition, physical task advantage, or novelty certification.',
 'generated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'python':platform.python_version(),'numpy':np.__version__,'seed':20261015,
 'exact_graph_terminal_matrix':strings(Sterm),
 'exact_inherited_terminal_leakage':[str(a[0]) for a in leak],
 'exact_static_multireceiver':{'S':str(strength),'D0':str(D0),'P':str(P),
     'D':str(D),'Pin':str(Pin),'load_scale':str(1/t-1)},
 'exact_ground_leak_reduction':{'delta':str(delta),'denominator':str(den),
     'rank_one_identity':True},
 'exact_loss_replacement_witness':{'old_loss':'2','new_loss':'51/50',
     'useful_power':'2/25','input':'11/10','add_only_baseline_loss':'1/2'},
 'exact_mediator_replacement':{'old':'4/3','new':'14/15',
     'receiver_branch_loss':str(gr),'condition':str(gn+gr)+' < '+str(gb)},
 'exact_layered_receiver_velocity':str(hh[2][0]),
 'exact_layered_velocity_upper_bound':'1/8',
 'exact_reactive_counterexample':{'Pout':'1/16','Pin':'5/8','loss':'9/16',
     'unloaded_gain_product_real':'3/25','unloaded_gain_product_imag':'4/25',
     'real_complex_Schur':'6/5','Schur_real_part':'1'},
 'reactive_fixture_optimal_loss':Dstar,
 'complex_envelope_networks':cases,'complex_envelope_power_targets':5*cases,
 'comparison_points_on_power_spheres':25*cases,
 'worst_normalized_power_residual':worst_power,
 'worst_normalized_loss_residual':worst_loss,
 'largest_lower_bound_violation_before_tolerance':worst_lower,
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
(BASE/'CHECK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
