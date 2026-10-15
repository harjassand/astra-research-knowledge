"""Exploratory compatible Fourier diagnostic, not a universal certificate."""
import argparse, json, time
from pathlib import Path
import numpy as np

def basis(m):
    n=4*m+1
    xy=np.stack(np.meshgrid(np.arange(n)*2*np.pi/n,np.arange(n)*2*np.pi/n,indexing='ij'),axis=-1).reshape(-1,2)
    modes=[(i,j) for i in range(m+1) for j in range(-m,m+1) if i>0 or j>0]
    rows=[]
    labels=[]
    for out in range(2):
        for k in modes:
            k=np.array(k,dtype=float)
            ang=xy@k
            for phase in range(2):
                row=np.zeros((4,len(xy)))
                derivative=(np.cos(ang) if phase==0 else -np.sin(ang))/np.linalg.norm(k)
                row[2*out]=k[0]*derivative
                row[2*out+1]=k[1]*derivative
                rows.append(row)
                labels.append([out,int(k[0]),int(k[1]),'sin' if phase==0 else 'cos'])
    return np.array(rows),labels,n

def evaluate(x,B,grad=True):
    a,b,c,d=np.einsum('i,ijk->jk',x,B)
    u=a*a+c*c;v=b*b+d*d;S=u+v;j=a*d-b*c;delta=u-v;q=2*a+d
    J=S*S/8+1.5*j*j+.5*delta*j
    cubic=a**3+5*a*a*d+2*a*d*d+a*c*c+d*c*c-4*a*b*c-2*b*c*d
    A=float(np.mean(J));C=float(np.mean(cubic));Q=float(np.mean(q*q+c*c))
    ratio=C*C/(4*A*Q) if A*Q else 0.
    if not grad:return ratio,A,C,Q,float(np.mean(j)),[float(np.mean(z)) for z in (a,b,c,d)]
    cf=3*j+.5*delta
    dJ=np.array([S*a/2+j*a+cf*d,S*b/2-j*b-cf*c,S*c/2+j*c-cf*b,S*d/2-j*d+cf*a])
    dC=np.array([3*a*a+10*a*d+2*d*d+c*c-4*b*c,-4*a*c-2*c*d,2*c*(a+d)-2*b*(2*a+d),5*a*a+4*a*d+c*c-2*b*c])
    dQ=np.array([4*q,np.zeros_like(q),2*c,2*q])
    field=C/(2*A*Q)*dC-ratio/A*dJ-ratio/Q*dQ
    gx=np.einsum('ijk,jk->i',B,field)/B.shape[-1]
    return ratio,gx

def run(m,seed,steps):
    B,labels,n=basis(m)
    rng=np.random.default_rng(seed)
    x=rng.normal(size=len(B));x/=np.linalg.norm(x)
    # Projected Adam is a local diagnostic. No claim of global optimization.
    mom=np.zeros_like(x);var=np.zeros_like(x);best=(-1.,x.copy());lr=.02
    for t in range(1,steps+1):
        value,g=evaluate(x,B)
        if value>best[0]:best=(value,x.copy())
        g-=x*np.dot(g,x)
        mom=.9*mom+.1*g;var=.999*var+.001*g*g
        x+=lr*(mom/(1-.9**t))/(np.sqrt(var/(1-.999**t))+1e-9)
        x/=np.linalg.norm(x)
        if t%500==0:lr*=.8
    value,A,C,Q,jmean,means=evaluate(best[1],B,False)
    return {'bandwidth':m,'grid':n,'seed':seed,'steps':steps,'ratio_C2_over_4AQ':value,'A4':A,'C3':C,'Q2':Q,'determinant_mean':jmean,'gradient_means':means,'labels':labels,'coefficients':best[1].tolist()}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--bandwidth',type=int,default=3);ap.add_argument('--runs',type=int,default=8);ap.add_argument('--steps',type=int,default=2000);args=ap.parse_args()
    t=time.time();results=[]
    for seed in range(args.runs):
        r=run(args.bandwidth,seed,args.steps);results.append(r)
        print(json.dumps({k:r[k] for k in ['bandwidth','seed','ratio_C2_over_4AQ','A4','C3','Q2']}),flush=True)
    out={'scope':'specified compatible finite Fourier local searches only; no lower bound and no universal inequality certificate','elapsed_seconds':time.time()-t,'results':results}
    Path(f'FOURIER_DIAGNOSTIC_m{args.bandwidth}.json').write_text(json.dumps(out,indent=2)+'\n')
