import numpy as np
from sdp_objective import Bs,sv,sm
from fractions import Fraction
import sympy as S

def feasible(p, margin=.001,steps=30000):
 Q0=sum(B*p for B,p in zip(Bs[:9],p))
 B=np.column_stack([sv(x) for x in Bs[9:]]);pin=np.linalg.pinv(B);P=B@pin
 x0=(np.eye(36)-P)@sv(Q0)
 y=x0.copy();z=np.zeros(36)
 for it in range(steps):
  x=x0+P@(y-z)
  d,v=np.linalg.eigh(sm(x+z));yp=sv((v*np.maximum(d,margin))@v.T)
  z+=x-yp;pr=np.linalg.norm(x-yp);du=np.linalg.norm(yp-y);y=yp
  if it%100==0 and pr<1e-11 and du<1e-11:break
 k=pin@(x-sv(Q0));return k,sm(x),pr,du,it
if __name__=='__main__':
 p=np.array([1,1,3.5,.5,0,0,-2.9,-2.9,0])
 k,Q,pr,du,it=feasible(p,.01)
 print('k=',k, 'res',pr,du,it, 'eigenvalues',np.linalg.eigvalsh(Q))
 krat=[S.Rational(round(x*10000),10000) for x in k]
 prat=[S.Rational(str(x)) for x in p]
 Qr=sum((S.Matrix(B.astype(int))*v for B,v in zip(Bs,prat+krat)), S.zeros(8))
 print('rational K coefficients',krat)
 print('Qr',Qr)
 print('leading principal minors', [S.factor(Qr[:i,:i].det()) for i in range(1,9)])
 np.savez('/mnt/data/astra_meta_genesis/rational_gram_candidate.npz',p=p,k=np.array(krat,float).flatten(),Q=np.array(Qr,float))
 open('/mnt/data/astra_meta_genesis/rational_gram_certificate.txt','w').write(str(Qr)+'\nK='+str(krat)+'\nleading_minors='+str([S.factor(Qr[:i,:i].det()) for i in range(1,9)]))
