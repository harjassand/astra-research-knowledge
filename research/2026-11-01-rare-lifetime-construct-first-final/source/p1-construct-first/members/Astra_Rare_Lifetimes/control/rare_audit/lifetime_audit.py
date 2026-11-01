"""Independent exact-complex and phase-type CDF checks for lifetime upgrade."""
from fractions import Fraction as F
from pathlib import Path
import math,random,json
import numpy as np
from scipy.linalg import expm,eigvalsh
from scipy.special import gammainc
from exact_audit import solve,zeros,stats


def rare_generator(n,p,rng):
    weights=[rng.randint(1,7) for _ in range(n-1)]
    pi=[p]+[(1-p)*F(w,sum(weights)) for w in weights]
    g=F(1,2)
    q=zeros(n)
    for i in range(n):
        for j in range(n):
            if i!=j:q[i][j]=g*pi[j]
    # Strong nonreversible B currents; rare target need not be the mixing route.
    for _ in range(n):
        cyc=rng.sample(range(1,n),rng.randint(2,n-1))
        flow=F(rng.randint(1,5),7)
        for i,j in zip(cyc,cyc[1:]+cyc[:1]):q[i][j]+=flow/pi[i]
    # Nonreversible current through the target at a finite conditional exit rate.
    for _ in range(2):
        cyc=[0]+rng.sample(range(1,n),2)
        flow=g*p*F(rng.randint(1,3),2)
        for i,j in zip(cyc,cyc[1:]+cyc[:1]):q[i][j]+=flow/pi[i]
    for i in range(n):q[i][i]=-sum(q[i][j] for j in range(n) if j!=i)
    for j in range(n):assert sum(pi[i]*q[i][j] for i in range(n))==0
    return q,pi,g


def imaginary_resolvent_h(q,pi,a,omega):
    b=[i for i in range(len(q)) if i not in a]
    k=len(b)
    l=[[-q[i][j] for j in b] for i in b]
    block=zeros(2*k)
    for i in range(k):
        for j in range(k):block[i][j]=l[i][j];block[k+i][k+j]=l[i][j]
        block[i][k+i]=-omega;block[k+i][i]=omega
    xy=solve(block,[F(1)]*k+[F(0)]*k)
    return (sum(pi[x]*xy[i] for i,x in enumerate(b)),
            sum(pi[x]*xy[k+i] for i,x in enumerate(b)))


def d_bound(delta):
    return min(1.0,4*delta/math.pi*math.log1p(1/(4*delta*delta))+48*delta/math.pi)


def main():
    rng=random.Random(161803)
    exact_disk=0;exact_characteristic=0;rows=[]
    for n in [4,5,7,9]:
        for p in [F(1,1000),F(1,100),F(1,50)]:
            q,pi,g=rare_generator(n,p,rng)
            st=stats(q,pi,[0],g/F(10))
            r0=st['b']*st['M'];delta=1/(g*r0)
            assert delta<=F(1,4)
            assert delta>=p/(1-p)
            for ratio in [F(0),F(1,10),F(1,4),F(1,2),F(3,4),F(2)]:
                omega=g*ratio
                hr,hi=imaginary_resolvent_h(q,pi,[0],omega)
                denom=hr*hr+hi*hi
                zr=r0*hr/denom
                zi=r0*(-hi/denom-omega)
                deviation=(zr-1)**2+zi**2
                assert deviation<=ratio*ratio*zr
                exact_disk+=1
                if ratio<=F(1,2):
                    assert zr>=F(1,2)
                    assert deviation<=4*ratio*ratio
                    t=omega*r0
                    assert zr*zr+(zi+t)**2>=F(1,4)*(1+t*t)
                    phi_r=1+omega*hi;phi_i=-omega*hr
                    diff2=(phi_r-1/(1+t*t))**2+(phi_i+t/(1+t*t))**2
                    assert diff2<=16*delta*delta*t**4/(1+t*t)**2
                    exact_characteristic+=1
            qn=np.array([[float(z) for z in row]for row in q])
            pn=np.array([float(z)for z in pi])
            ds=np.sqrt(pn)
            lweighted=-ds[:,None]*qn/ds[None,:]
            gap=float(eigvalsh((lweighted+lweighted.T)/2)[1])
            assert gap>=float(g)-1e-9
            tgrid=np.concatenate(([0.0],np.geomspace(1e-5,30,180)))
            fv=[];fb=[]
            for t in tgrid:
                survival=pn[1:]@(expm(qn[1:,1:]*(float(r0)*t))@np.ones(n-1))
                fv.append(1-survival)
                fb.append(1-survival/float(1-p))
            ref=1-np.exp(-tgrid)
            error=float(np.max(np.abs(np.array(fv)-ref)))
            error_b=float(np.max(np.abs(np.array(fb)-ref)))
            bound=d_bound(float(delta))
            bound_b=min(1.0,(bound+float(p))/float(1-p))
            assert error<=bound+1e-10
            assert error_b<=bound_b+1e-10
            rows.append(dict(N=n,p=float(p),M=float(st['M']),bM=float(r0),
                certified_g=float(g),actual_symmetric_gap=gap,delta=float(delta),
                numerical_unconditional_cdf_error=error,
                numerical_conditional_cdf_error=error_b,
                proposed_unconditional_bound=bound,
                proposed_conditional_bound=bound_b))
    n=128
    r0=(n-1)/2
    g=1-math.cos(2*math.pi/n)
    tgrid=np.linspace(0,4,4001)
    erlangs=np.arange(1,n)[:,None]
    cdfs=gammainc(erlangs,tgrid[None,:]*r0)
    fpi=(1+cdfs.sum(axis=0))/n
    expcdf=1-np.exp(-tgrid)
    cycle=dict(N=n,delta=1/(g*r0),
        numerical_cdf_error=float(np.max(np.abs(fpi-expcdf))),
        note='Rare A alone is insufficient: this directed-cycle delta exceeds1/4.')
    result=dict(exact_complex_disk_checks=exact_disk,
        exact_characteristic_checks=exact_characteristic,
        cdf_rows=rows,no_mixing_separation_counterexample=cycle,
        scope='Exact rational complex checks plus floating phase-type CDF diagnostics; not a proof of Esseen constants or physical qualification.')
    path=Path(__file__).with_name('lifetime_audit_results.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
