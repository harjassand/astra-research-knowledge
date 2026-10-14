"""Two-load source-aware certificate for equilibrium and a point preparation."""
from fractions import Fraction as F
import math,time,json
import numpy as np
import scipy.sparse as ss
import scipy.sparse.linalg as sla
from collective_sector import CollectiveRing

def sqrt_up(x,digits=30):
    if x<0:raise ValueError('negative square root')
    den=10**digits
    z=math.isqrt((x.numerator*den*den)//x.denominator)
    if F(z*z,den*den)<x:z+=1
    return F(z,den)

def run(n,t,nu=F(1),kappa=F(1),bits=32):
    start=time.perf_counter();R=CollectiveRing(n,F(t),nu,kappa);S=R.states();idx={x:i for i,x in enumerate(S)}
    rows=[];cols=[];vals=[]
    for row,x in enumerate(S):
        diag=kappa*(x&1)
        for i in range(n):
            rt=R.rate(x,i);diag+=rt;y=x^(1<<i)
            if y in idx:rows.append(row);cols.append(idx[y]);vals.append(-float(rt))
        rows.append(row);cols.append(row);vals.append(float(diag))
    K=ss.csc_matrix((vals,(rows,cols)),shape=(len(S),len(S)));factor=sla.splu(K)
    rhs=np.ones((len(S),2));rhs[:,1]=0;rhs[idx[0],1]=1/float(R.prob(0))
    v0=factor.solve(rhs);vs=[{x:F(round(float(v0[j,c])*2**bits),2**bits) for j,x in enumerate(S)} for c in range(2)]
    Kvs=[]
    for v in vs:
        Kv={}
        for x,vx in v.items():
            diag=kappa*(x&1)
            for i in range(n):
                diag+=R.rate(x,i);y=x^(1<<i)
                Kv[y]=Kv.get(y,F(0))-R.rate(y,i)*vx
            Kv[x]=Kv.get(x,F(0))+diag*vx
        Kvs.append(Kv)
    dr=[{x:-a for x,a in Kv.items()} for Kv in Kvs]
    dr[1][0]=dr[1].get(0,F(0))+1/R.prob(0)
    constants=[F(1),F(0)];Z=[]
    for c,d in zip(constants,dr):
        z0=c*R.da;z1=c*R.db*R.s
        for x,dx in d.items():
            wt=R.prob(x)/(R.gamma+kappa*(x&1));z0+=wt*dx
            z1+=wt*dx*F(2*x.bit_count()-n,n)
        Z.append((z0,z1))
    Gamma=[[F(0) for _ in range(2)] for _ in range(2)]
    G0=[[F(0) for _ in range(2)] for _ in range(2)]
    def load(i,v):return sum(R.prob(x)*a for x,a in v.items()) if i==0 else v.get(0,F(0))
    for i in range(2):
        for j in range(2):
            ci,cj=constants[i],constants[j]
            E=ci*cj*R.da
            for x in set(dr[i])|set(dr[j]):
                a=dr[i].get(x,F(0));b=dr[j].get(x,F(0))
                E+=R.prob(x)/(R.gamma+kappa*(x&1))*(ci*b+cj*a+a*b)
            zi,zj=Z[i],Z[j]
            E-=R.W00*zi[0]*zj[0]+R.W01*(zi[0]*zj[1]+zi[1]*zj[0])+R.W11*zi[1]*zj[1]
            Gamma[i][j]=E
            G0[i][j]=load(i,vs[j])+load(j,vs[i])-sum(R.prob(x)*a*Kvs[j][x] for x,a in vs[i].items())
    assert Gamma[0][1]==Gamma[1][0] and G0[0][1]==G0[1][0]
    assert Gamma[0][0]>=0 and Gamma[1][1]>=0 and Gamma[0][0]*Gamma[1][1]>=Gamma[0][1]**2
    center=G0[0][1]+Gamma[0][1]/2;radius=sqrt_up(Gamma[0][0]*Gamma[1][1])/2
    lo=center-radius;hi=center+radius
    return {'n':n,'t':str(t),'nu':str(nu),'kappa':str(kappa),'point_initial':'all spins closed',
            'point_lo':float(lo),'point_hi':float(hi),'point_ratio':float(hi/lo),
            'point_lo_exact':str(lo),'point_hi_exact':str(hi),
            'equilibrium_lo':float(G0[0][0]),'equilibrium_hi':float(G0[0][0]+Gamma[0][0]),
            'Gamma':[[str(a) for a in row] for row in Gamma],'G0':[[str(a) for a in row] for row in G0],
            'witnesses':[{str(x):str(a) for x,a in v.items()} for v in vs],
            'total_s':time.perf_counter()-start}
if __name__=='__main__':
    import sys
    out=run(int(sys.argv[1]),F(sys.argv[2]));json.dump(out,open(sys.argv[3],'w'))
    print(json.dumps({k:v for k,v in out.items() if k not in ['witnesses','Gamma','G0','point_lo_exact','point_hi_exact']}))
