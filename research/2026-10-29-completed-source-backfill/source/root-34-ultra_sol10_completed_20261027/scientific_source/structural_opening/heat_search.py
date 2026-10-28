#!/usr/bin/env python3
"""Compatible Fourier dissipation diagnostic; not a QC test/certificate.

Quartic products use alias-free periodic quadrature. Backgrounds are
eliminated by their literal positive quadratic form. No producer imports.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
from pathlib import Path
import itertools,json,math,time,argparse
import numpy as np
import sympy as s
from scipy.optimize import minimize

ROOT=Path(__file__).resolve().parent
a,b,c,d=s.symbols('a b c d')
u,v=a*a+c*c,b*b+d*d
q=a*d-b*c
beta=s.Rational(197**2-1,197**2+1)
F=s.expand((u+v)**2+12*q*q+4*beta*q*(u-v))
poly=s.Poly(F,a,b,c,d)
coef=dict(poly.terms())
T=np.zeros((4,4,4,4))
for inds in itertools.product(range(4),repeat=4):
    ee=tuple(inds.count(i) for i in range(4))
    T[inds]=float(coef.get(ee,0))*math.prod(math.factorial(x) for x in ee)/24
J=np.array([[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]],float)

class Problem:
 def __init__(self,frequencies):
    self.freq=np.array(frequencies,int);m=len(frequencies)
    n=4*int(np.max(np.abs(self.freq)))+1
    xy=np.array(list(np.ndindex(n,n)))*2*np.pi/n
    phase=xy@self.freq.T
    pro=np.stack([np.cos(phase),np.sin(phase)],axis=2)
    dpro=np.stack([-np.sin(phase),np.cos(phase)],axis=2)
    self.D=np.zeros((len(xy),m,2,2,4))
    self.H=np.zeros((len(xy),2,m,2,2,4))
    for ii,k in enumerate(self.freq):
      for out in range(2):
        self.D[:,ii,:,out,2*out:2*out+2]=pro[:,ii,:,None]*k
        for jj in range(2):
          self.H[:,jj,ii,:,out,2*out:2*out+2]=dpro[:,ii,:,None]*k*k[jj]
    self.D=self.D.reshape(len(xy),4*m,4)
    self.H=self.H.reshape(len(xy),2,4*m,4)
    self.n=n

 def evaluate(self,p,details=False):
    norm=np.linalg.norm(p)
    pp=p/norm
    G=np.einsum('npa,p->na',self.D,pp)
    H=np.einsum('njpa,p->nja',self.H,pp)
    V=np.einsum('abcd,njc,njd->nab',T,H,H,optimize=True)
    M=V.mean(axis=0)
    cc=np.einsum('nab,nb->na',V,G).mean(axis=0)
    A=-np.linalg.solve(M,cc)
    Y=G+A
    W=np.einsum('abcd,na,nb->ncd',T,Y,Y,optimize=True)
    numerator=12*np.einsum('na,nab,nb->n',Y,V,Y).mean()
    gG=24*np.einsum('nab,nb->na',V,Y)
    gH=24*np.einsum('nab,njb->nja',W,H)
    G2=np.sum(G*G,axis=1);H2=np.sum(H*H,axis=(1,2))
    den=np.mean(G2*H2)
    objective=numerator/den
    gG=(gG-objective*(2*G*H2[:,None]))/den
    gH=(gH-objective*(2*H*G2[:,None,None]))/den
    gp=(np.einsum('npa,na->p',self.D,gG)
        +np.einsum('njpa,nja->p',self.H,gH))/len(G)
    gp=(gp-pp*np.dot(pp,gp))/norm
    if not details:return objective,gp
    JH2=H[:,1]@J.T
    cross=24*np.einsum('nab,na,nb->n',W,H[:,0],JH2).mean()
    return {'objective':float(objective),'dissipation':float(numerator),
      'normalization':float(den),'chiral_dissipation':float(cross),
      'background':A.tolist(),'parameters':pp.tolist(),
      'frequencies':self.freq.tolist(),'grid':self.n,
      'background_matrix_eigenvalues':np.linalg.eigvalsh(M).tolist(),
      'gradient_norm':float(np.linalg.norm(gp))}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--starts',type=int,default=10)
 parser.add_argument('--iterations',type=int,default=800);args=parser.parse_args()
 sets=[[(1,0),(0,1),(1,1)],[(1,0),(0,1),(1,1),(1,-1)],
       [(1,0),(0,1),(1,1),(1,-1),(2,0),(0,2),(2,1),(1,2),(2,-1),(1,-2)]]
 rng=np.random.default_rng(301028)
 results=[]
 for ii,freqs in enumerate(sets):
    prob=Problem(freqs)
    p=rng.normal(size=4*len(freqs));vv,gg=prob.evaluate(p)
    step=1e-6;fd=[]
    for jj in range(len(p)):
      e=np.zeros_like(p);e[jj]=step
      fd.append((prob.evaluate(p+e)[0]-prob.evaluate(p-e)[0])/(2*step))
    error=float(np.max(np.abs(np.array(fd)-gg)))
    assert error<2e-5,error
    for jj in range(args.starts):
      start=time.perf_counter()
      fit=minimize(prob.evaluate,rng.normal(size=len(p)),jac=True,method='L-BFGS-B',
                   options={'maxiter':args.iterations,'ftol':1e-13,'gtol':1e-9,'maxls':40})
      result=prob.evaluate(fit.x,True)
      result.update(set=ii,start=jj,success=bool(fit.success),iterations=int(fit.nit),
                    derivative_check=error,seconds=time.perf_counter()-start)
      results.append(result)
      print(ii,jj,result['objective'],result['chiral_dissipation'],result['seconds'],flush=True)
      (ROOT/'HEAT_DIAGNOSTIC.json').write_text(json.dumps({'scope':'NUMERICAL_COMPATIBLE_HEAT_DIAGNOSTIC_NOT_QC',
            'target':'T^2+12q^2+4*((197^2-1)/(197^2+1))*q*x','runs':results},indent=2)+'\n')
if __name__=='__main__':main()
