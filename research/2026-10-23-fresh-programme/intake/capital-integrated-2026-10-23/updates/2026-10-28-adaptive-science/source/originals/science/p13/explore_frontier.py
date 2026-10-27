"""Owned numerical exploration; the accompanying proof owns global claims."""
import math, json
from pathlib import Path
import numpy as np
from attainable_design_owned import endpoints, bose, band_integral

HERE=Path(__file__).resolve().parent

def one(k):
    r=math.sqrt(2*k); p,s,_=endpoints(r,4.,2.)
    ends=[p,r,s]
    lam,mu,eta=np.linalg.solve(np.array([[w*w,2*w**4,-1.] for w in ends]),
                              -np.array([w**3*bose(w,.5) for w in ends]))
    return dict(k=k,C=1/k,lambda_=float(lam),mu=float(mu),eta=float(eta),
                bands=[[0.,p],[r,s]],J=band_integral(0,p,.5)+band_integral(r,s,.5))

def network(C,h,H):
    """Backbone=1, two side masses h and 1-h. Charges exact CM response."""
    b=1-h
    assert 0<h<1 and H>h*h/C
    k=b*b/(C-h*h/H)
    masses=np.array([1.,h,b]); springs=[H,k]
    L=np.zeros((3,3))
    for i,q in enumerate(springs,1):
        L[0,0]+=q; L[i,i]+=q; L[0,i]-=q; L[i,0]-=q
    im=1/np.sqrt(masses)
    D0=im[:,None]*L*im[None,:]
    Dpi=D0.copy();Dpi[0,0]+=4.
    alpha=np.linalg.eigvalsh(D0);beta=np.linalg.eigvalsh(Dpi)
    alpha[0]=0.
    bands=[[math.sqrt(max(0.,a)),math.sqrt(b)] for a,b in zip(alpha,beta)]
    J=sum(band_integral(a,b,.5) for a,b in bands)
    # Exact analytic identity is C=sum(m_i^2/k_i), side total=1.
    compliance=h*h/H+b*b/k
    return dict(C=C,h=h,H=H,k=k,masses=masses.tolist(),springs=springs,
                alpha=alpha.tolist(),beta=beta.tolist(),bands=bands,J=J,
                compliance=compliance,trace=float(sum(beta)-sum(alpha)))

def reduced(C,h):
    """H=infinity is only a limit, never a finite achieved network."""
    a=1+h;b=1-h;k=b*b/C
    r=math.sqrt(k*2/(a*b));p,s,_=endpoints(r,4/a,2)
    return band_integral(0,p,.5)+band_integral(r,s,.5)

def golden(fun,lo,hi):
    t=(math.sqrt(5)-1)/2
    x=hi-t*(hi-lo); y=lo+t*(hi-lo); fx=fun(x);fy=fun(y)
    for _ in range(90):
        if fx<fy:hi,y,fy=y,x,fx;x=hi-t*(hi-lo);fx=fun(x)
        else:lo,x,fx=x,y,fy;y=lo+t*(hi-lo);fy=fun(y)
    h=(lo+hi)/2
    return h,fun(h)

def main():
    lo,hi=10.,16.
    for _ in range(70):
        mid=(lo+hi)/2
        if one(mid)['mu']>0:lo=mid
        else:hi=mid
    threshold=one((lo+hi)/2)
    print('CRITICAL',json.dumps(threshold,indent=2))
    rows=[]
    for C in [.25,.1,.08,.075,.07,.06,.05,.025,.01,.001]:
        h,Jinf=golden(lambda h:reduced(C,h),1e-10,1-1e-9)
        finite=network(C,h,1000.)
        row=dict(C=C,ordinary=one(1/C),h=h,J_limit=Jinf,finite=finite)
        rows.append(row)
        print('C',C,'h',h,'J1',row['ordinary']['J'],'Jlim',Jinf,
              'Jfinite',finite['J'],'saving',row['ordinary']['J']-finite['J'])
    (HERE/'frontier_exploration.json').write_text(json.dumps(dict(threshold=threshold,rows=rows),indent=2)+'\n')

if __name__=='__main__':main()
