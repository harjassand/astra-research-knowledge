#!/usr/bin/env python3
"""Coherent multi-J quantum-frame receiver on the actual tracial stream.

The full regular-representation frame and its right reference are retained.
Distinct J blocks share the SAME carrier Kraus indices, so their coherences
are not dephased. These are finite diagnostics, not an asymptotic theorem.
"""
import math,json,argparse
from pathlib import Path
import numpy as np
from scipy import sparse
from spin_frame_probe import source_receiver_kraus,petz_fe

def rotor_data(jmax,theta,ratio,kind,weights):
    js=list(range(jmax+1));D=sum((2*j+1)**2 for j in js)
    entries=[([],[],[]) for _ in range(4)]
    eta=np.zeros(D,complex);offset=0
    for j in js:
        d=2*j+1
        if weights=='dimension':w=math.sqrt(d)
        elif weights=='sine':w=math.sin(math.pi*(j+1)/(jmax+2))/math.sqrt(d)
        else:w=1/math.sqrt(d)
        for m in range(d):eta[offset+m*d+m]=w
        v=ratio/math.tan(theta)
        angle=theta*ratio if kind=='exponential' else None
        ks=source_receiver_kraus(j,theta,v,angle)
        for ki,K in enumerate(ks):
            ii,jj=np.where(abs(K)>1e-14)
            rr,cc,vv=entries[ki]
            for r0 in range(2):
                for right in range(d):
                    rr.extend(((r0*2+ii//d)*D+offset+right*d+ii%d).tolist())
                    cc.extend(((r0*2+jj//d)*D+offset+right*d+jj%d).tolist())
                    vv.extend(K[ii,jj].tolist())
        offset+=d*d
    eta/=np.linalg.norm(eta)
    Ks=[sparse.csr_matrix((v,(r,c)),shape=(4*D,4*D)) for r,c,v in entries]
    err=sparse.linalg.norm(sum(K.conj().T@K for K in Ks)-sparse.eye(4*D))
    assert err<1e-10,err
    return D,eta,Ks

def run(jmax,theta,ratio,n,kind='exponential',weights='sine'):
    D,eta,Ks=rotor_data(jmax,theta,ratio,kind,weights)
    bell=np.array([1,0,0,1],complex)/math.sqrt(2)
    psi=np.kron(bell,eta);rho=np.outer(psi,psi.conj())
    rows=[];best=(0.0,0)
    times=set(range(1,min(n,10)+1))|set(range(20,n+1,20))|{n}
    for t in range(1,n+1):
        out=np.zeros_like(rho)
        for K in Ks:
            z=K@rho;out+=(K@z.conj().T).conj().T
        rho=out
        if t in times:
            fe=petz_fe(rho,1,D)
            rows.append([t,fe])
            if fe>best[0]:best=(fe,t)
    return {'source_theta':theta,'Jmax':jmax,'memory_dimension':D,
            'interaction':kind,'ratio':ratio,'initial_weights':weights,'N':n,
            'best_sampled_petz_fe':best[0],'best_sampled_time':best[1],
            'final_trace':float(np.trace(rho).real),'samples':rows}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--jmax',type=int,default=3)
    p.add_argument('--theta',type=float,default=.3);p.add_argument('--ratio',type=float,default=1)
    p.add_argument('--n',type=int,default=600);p.add_argument('--kind',choices=['exponential','lax'],default='exponential')
    p.add_argument('--weights',choices=['dimension','sine','flat'],default='sine')
    a=p.parse_args();r=run(a.jmax,a.theta,a.ratio,a.n,a.kind,a.weights)
    path=Path(__file__).with_name(f'rotor_J{a.jmax}_theta{a.theta}_{a.kind}_{a.ratio}_{a.weights}.json')
    path.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='samples'},indent=2))
