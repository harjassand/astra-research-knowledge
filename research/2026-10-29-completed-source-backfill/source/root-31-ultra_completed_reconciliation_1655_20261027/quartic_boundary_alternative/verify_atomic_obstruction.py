#!/usr/bin/env python3
"""Independent standard-library Fraction replay of the literal finite atoms.

No scientific generator, SymPy, NumPy, SciPy, or parent/peer code is imported.
"""
from fractions import Fraction as Q
from pathlib import Path
import json,hashlib,time

HERE=Path(__file__).resolve().parent

def det(a):return a[0]*a[3]-a[1]*a[2]

def energy_and_direction(a,x,p):
 aa,b,c,d=a;xa,xb,xc,xd=x
 u=aa*aa+c*c;v=b*b+d*d;w=aa*b+c*d;q=aa*d-b*c
 du=2*(aa*xa+c*xc);dv=2*(b*xb+d*xd)
 dw=xa*b+aa*xb+xc*d+c*xd
 dq=xa*d+aa*xd-xb*c-b*xc
 values=(u*u,v*v,u*v,w*w,u*w,v*w,q*u,q*v,q*w)
 deriv=(2*u*du,2*v*dv,du*v+u*dv,2*w*dw,
        du*w+u*dw,dv*w+v*dw,dq*u+q*du,dq*v+q*dv,dq*w+q*dw)
 return sum(z*c for z,c in zip(values,p)),sum(z*c for z,c in zip(deriv,p))

def main():
 started=time.perf_counter()
 path=HERE/'EXACT_POLYNOMIAL_SELECTOR_OBSTRUCTION.json'
 raw=path.read_bytes(); data=json.loads(raw)
 p=list(map(Q,data['coefficients']))
 source=HERE/'external_inputs/EXACT_SYMMETRIC_TARGET.json'
 assert hashlib.sha256(source.read_bytes()).hexdigest()==data['source_sha256']
 assert list(map(Q,json.loads(source.read_text())['coefficients']))==p
 assert p[0]==p[1] and p[4]==p[5]==p[8]==0 and p[6]==-p[7]

 # Independent exact continuum ROC check in the aligned Hopf sector.
 k1=p[0];k2=(p[0]+p[1]+p[2]+p[3])/4
 coupling=(p[6]-p[7])/8;radius=(p[0]+p[1]+p[2])/4
 assert k1>0 and k2>0
 assert k1*radius-coupling*coupling>0
 n10=2*k1*k2-k2*k2
 n11=-(k1*k1-k2*k2+coupling*coupling)
 n20=2*k2*radius-k2*k2
 n21=2*(k1-k2)*radius-(k1*k1-k2*k2+3*coupling*coupling)
 assert n10>0 and n10+n11>0
 # detN(s) = A*s²+B*s+C, s in [0,1].
 A=n11*n21
 B=n10*n21+n11*n20+4*coupling*coupling*k2*k2
 C=n10*n20-4*coupling*coupling*k2*k2
 assert A>0
 stationary=-B/(2*A)
 candidates=[C,A+B+C]
 if 0<stationary<1:candidates.append(A*stationary*stationary+B*stationary+C)
 continuum_minimum=min(candidates)
 assert continuum_minimum>0

 # Literal evaluation of the atomic functional on all support selectors.
 total=Q(0);annihilators={(i,j):Q(0) for i in range(4) for j in range(i,4)}
 for atom in data['atoms']:
  a=list(map(Q,atom['A']));x=list(map(Q,atom['X']));weight=Q(atom['weight'])
  assert weight>0
  f,dfx=energy_and_direction(a,x,p)
  ax=[v+w for v,w in zip(a,x)]
  fx,_=energy_and_direction(ax,[Q(0)]*4,p)
  total+=weight*(fx-f-dfx)
  for i,j in annihilators:annihilators[i,j]+=weight*a[i]*a[j]*det(x)
 assert len(data['atoms'])==data['atomic_count']==24
 assert all(v==0 for v in annihilators.values())
 assert total==Q(data['negative_Bregman_pairing'])<0
 assert total<Q(-1,100000)
 out={
  'status':'PASS',
  'scope':'strict ROC and no polynomial globally nonnegative minor support; true PC unresolved',
  'certificate_sha256':hashlib.sha256(raw).hexdigest(),
  'source_sha256':data['source_sha256'],
  'strict_ROC_detN_minimum':str(continuum_minimum),
  'atomic_count':24,'all_ten_quadratic_annihilators_zero':True,
  'literal_Bregman_pairing':str(total),
  'strict_pairing_bound':'< -1/100000',
  'elapsed_seconds':time.perf_counter()-started,
 }
 (HERE/'ATOMIC_OBSTRUCTION_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))

if __name__=='__main__':main()
