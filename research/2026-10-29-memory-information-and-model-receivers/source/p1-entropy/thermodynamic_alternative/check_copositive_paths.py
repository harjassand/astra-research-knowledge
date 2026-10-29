"""Independent directed-generator checks of root's path-affinity bounds.

Matrix exponentials are floating numerical controls, not formal certificates.
All statements and constants are reconstructed in the companion ordinary proof.
"""
from pathlib import Path
from fractions import Fraction as F
import json
import hashlib
import numpy as np
import scipy
from scipy.linalg import expm
from check_thermodynamic_completion import zero, cycle, gen


def family(d, hidden_cycle=F(0)):
    w=[F(1)]*5+[1/(1-d*d)]*10
    a=zero(15); p=(1+d)/2; q=(1-d)/2
    for e in range(5):
        i,j=e,(e+1)%5
        for b in [0,1]:
            x=5+2*e+b; v=p if b==0 else q
            a[i][x]=w[x]*v; a[j][x]=w[x]*(1-v)
            a[x][i]=w[x]*(1-v); a[x][j]=w[x]*v
    if hidden_cycle:
        cycle(a,list(range(5,15)),hidden_cycle,hidden_cycle/3)
    return a,w


def general():
    a=zero(8); w=[1+F(i,10) for i in range(8)]
    for i in range(8):
        for j in range(i): a[i][j]=a[j][i]=F(1,5)
    cycle(a,list(range(8)),F(4),F(1))
    cycle(a,[0,2,5,1,6],F(7,10),F(1,5))
    return a,w


def entropy(a):
    E=0.0
    for i in range(len(a)):
        for j in range(i+1,len(a)):
            x,y=float(a[i][j]),float(a[j][i])
            if x: E+=(x-y)*np.log(x/y)
    return float(E)


def test(a,w,name):
    q=np.array(gen(a,w),dtype=float)
    f=np.array(a,dtype=float); w=np.array(w,dtype=float)
    n=len(w); m=5; b=np.arange(m); ii=np.arange(m,n)
    E=entropy(a); W=float(w.sum()); sigma=E/W
    fg=np.sqrt(f*f.T)
    qg=fg/w[:,None]; np.fill_diagonal(qg,np.diag(q))
    assert np.max(qg.sum(axis=1))<1e-10
    assert np.max(abs(w[:,None]*qg-(w[:,None]*qg).T))<1e-10
    H=np.ones((m,m))
    for i in range(m): H[i,(i+1)%m]=H[(i+1)%m,i]=-1
    A=f[np.ix_(b,ii)]; B=q[np.ix_(ii,b)]; G=-q[np.ix_(ii,ii)]
    Ag=fg[np.ix_(b,ii)]; Bg=qg[np.ix_(ii,b)]; Gg=-qg[np.ix_(ii,ii)]
    M=A@np.linalg.solve(G,np.linalg.solve(G,B))
    Mg=Ag@np.linalg.solve(Gg,np.linalg.solve(Gg,Bg))
    c=float((A@np.linalg.solve(G,np.linalg.solve(G,np.linalg.solve(G,B)))).sum())
    assert abs(M.sum()-w[ii].sum())<1e-9
    D1=float(((M+M.T)/2-Mg).sum())
    assert D1>=-1e-9 and D1*D1<=c*E/2+1e-9
    gamma_M=max(0.0,float(-(H*M).sum()))
    assert E>=2*gamma_M*gamma_M/c-1e-9
    R=float(-w[b]@np.diag(q)[b])
    mu_geo=float(fg[np.ix_(b,b)].sum()+(Ag@np.linalg.solve(Gg,Bg)).sum())
    Dfull=R-mu_geo
    assert E>=4*Dfull-1e-9
    bin_checks=[]
    nodes,weights=np.polynomial.legendre.leggauss(32)
    sq=np.sqrt(w[ii]); Hg=sq[:,None]*Gg/sq[None,:]
    assert np.max(abs(Hg-Hg.T))<1e-10
    for lo,hi in [(0.0,1.0),(0.3,1.7)]:
        C=A@np.linalg.solve(G,expm(-G*lo)-expm(-G*hi))@B
        Cg=Ag@np.linalg.solve(Gg,expm(-Gg*lo)-expm(-Gg*hi))@Bg
        delta=(C+C.T)/2-Cg
        assert delta.min()>-1e-9
        D=float(delta.sum()); gamma=max(0.0,float(-(H*C).sum()))
        assert E>=4*D-1e-9 and gamma<=D+1e-9
        gram=np.zeros((m,m))
        for node,wt in zip(nodes,weights):
            t=(lo+hi)/2+(hi-lo)*node/2
            V=(Ag/sq[None,:])@expm(-Hg*t/2)
            assert V.min()>-1e-10
            gram+=(hi-lo)*wt/2*(V@V.T)
        assert np.max(abs(gram-Cg))<1e-9
        assert float((H*Cg).sum())>-1e-9
        bin_checks.append(dict(lo=lo,hi=hi,gamma=gamma,deficit=D,
                               entropy_lower=4*gamma,gram_error=float(np.max(abs(gram-Cg)))))
    emission=np.zeros((n,5))
    for i in range(n): emission[i,i%5]=1
    lag_checks=[]
    pi=w/W
    for t in [0.2,1.0,3.0]:
        C=emission.T@(pi[:,None]*expm(t*q))@emission
        Cg=emission.T@(pi[:,None]*expm(t*qg))@emission
        delta=(C+C.T)/2-Cg
        assert delta.min()>-1e-9
        D=float(delta.sum()); gamma=max(0.0,float(-(H*C).sum()))
        assert sigma*t>=4*D-1e-9
        assert gamma<=D+1e-9
        assert float((H*Cg).sum())>-1e-9
        lag_checks.append(dict(t=t,deficit=D,gamma=gamma,entropy_lower=4*gamma/t))
    return dict(name=name,states=n,entropy_unnormalized=E,normalized_rate=sigma,
                native_departure_flux=R,full_path_deficit=Dfull,
                first_moment_gap=gamma_M,first_moment_deficit=D1,c=c,
                first_moment_lower=2*gamma_M*gamma_M/c,
                bins=bin_checks,lags=lag_checks)


def main():
    results=[]
    for eps in [F(0),F(1,1000),F(1,100),F(1,10),F(1)]:
        a,w=family(F(1,4),eps)
        results.append(test(a,w,'five_port_hidden_cycle_'+str(eps)))
    a,w=general(); results.append(test(a,w,'general_directed_eight_state'))
    sharp=[]
    for d in [F(1,4),F(1,8),F(1,16),F(1,64),F(1,256)]:
        a,w=family(d)
        E=entropy(a); gamma=float(10*d*d/(1-d*d))
        sharp.append(dict(d=str(d),E_over_gamma=E/gamma))
        assert E/gamma>4
    root=Path(__file__).parent.parent/'COPOSITIVE_PATH_CERTIFICATES.md'
    data=dict(status='PASS',scope='independent numerical controls; ordinary proof reviewed separately',
              numpy_version=np.__version__,scipy_version=scipy.__version__,
              reviewed_root_sha256=hashlib.sha256(root.read_bytes()).hexdigest(),
              source_observations=0,source_preparations=0,random_draws=0,
              models=len(results),positive_time_bins=2*len(results),lag_checks=3*len(results),
              results=results,constant_four_sharpness=sharp,
              script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    Path(__file__).with_name('COPOSITIVE_PATH_CHECKS.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:data[k] for k in ['status','models','positive_time_bins','lag_checks','source_observations','constant_four_sharpness']},indent=2))


if __name__=='__main__': main()
