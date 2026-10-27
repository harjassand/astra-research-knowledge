#!/usr/local/bin/python3
"""Independent regulated scalar response, analytically integrating one coordinate.

The cross term uses a divided difference of the exact one-body transform.  This
does not replace a boundary proof and does not discretize the radiating shell.
"""
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from scipy.special import roots_legendre

from independent_checks import endpoint, quadrature_channel

OUT = Path(__file__).resolve().parent
g = .2
kp, km = 2*g*g, g*g


def grid(center, k, n, E):
    nodes, weights = quadrature_channel(center,k,n)
    cuts=[0.,math.pi]
    other_edges=[0.,2.] if center==5 else [4.,6.]
    for edge in other_edges:
        x=E-edge
        if center-1 < x < center+1:
            cuts.append(math.acos(x-center))
    cuts=sorted(set(cuts))
    t,w=roots_legendre(n)
    xs=[nodes[0:1]]; ws=[weights[0:1]]
    for a,b in zip(cuts[:-1],cuts[1:]):
        theta=a+(b-a)*(t+1)/2
        u,v=np.cos(theta),np.sin(theta)
        x=center+u
        weight=(b-a)*w/2*2*k*v*v/(math.pi*((3-x+2*k*u)**2+4*k*k*v*v))
        xs.append(x);ws.append(weight)
    return np.concatenate(xs),np.concatenate(ws)


def run(n):
    x,w=quadrature_channel(5,kp,256)
    y,v=quadrature_channel(1,km,256)
    pp=x[:,None]+x[None,:]; mm=y[:,None]+y[None,:]
    Wp=np.outer(w,w);Wm=np.outer(v,v)
    def pair_eq(E):return np.sum(Wp/(pp-E))+np.sum(Wm/(mm-E))
    E=brentq(pair_eq,2*x[0]+1e-8,2*y[0]-1e-8,xtol=5e-15)
    D=np.sum(Wp/(pp-E)**2)+np.sum(Wm/(mm-E)**2)
    C=math.sqrt(2/D)
    x,w=grid(5,kp,n,E);y,v=grid(1,km,n,E)
    a=endpoint(E-x,5,kp).real
    b=endpoint(E-y,1,km).real
    out=[]
    for epsilon in [1e-2,1e-3,1e-4,1e-5,1e-6,1e-7,1e-8]:
        z=E+1j*epsilon
        rm=endpoint(z-x,1,km)
        rp=endpoint(z-y,5,kp)
        M=np.sum(w*rm)
        B=C*(np.sum(w*a*rm)+np.sum(v*b*rp))
        # Integrating y in m_-(E-y)/(x+y-z) gives this divided difference.
        divided=(b[None,:]-rm[:,None])/((E-y[None,:])-(z-x[:,None]))
        cross=np.sum((w*a)[:,None]*v[None,:]*divided)
        A=C*C*(np.sum(w*a*a*rm)+np.sum(v*b*b*rp)+2*cross)
        reduced=A-B*B/M
        out.append({"epsilon":epsilon,"A":[A.real,A.imag],"B":[B.real,B.imag],
                    "M":[M.real,M.imag],"response":[reduced.real,reduced.imag],
                    "regularized_density":float(reduced.imag/math.pi)})
    return {"nodes_per_threshold_piece":n,"Ep":float(E),"rows":out}


if __name__=="__main__":
    results=[run(n) for n in [128,512,1024]]
    (OUT/'boundary_diagnostic.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))
