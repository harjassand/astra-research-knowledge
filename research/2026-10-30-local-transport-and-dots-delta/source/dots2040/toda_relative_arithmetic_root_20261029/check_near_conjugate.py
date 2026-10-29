import numpy as np,json
from pathlib import Path
import mpmath as mp
mp.mp.dps=90
out=[]
for power in [1,2,3,4,6,8,12,20]:
 e=mp.mpf(10)**(-power);F=e**4-5*e**2+4;y=-mp.sqrt(F);yp=(4*e**3-10*e)/(2*y)
 a2=(2+y-e*yp)/(e*e);a1=-2*e*a2-yp
 A=mp.matrix([[1,e,e*e,y],[0,1,2*e,yp],[1,0,0,-2]])
 B=mp.matrix(A)
 for j in range(4):B[2,j]=(A[0,j]-A[2,j]-e*A[1,j])/(e*e)
 _,sa,_=mp.svd(A);_,sb,_=mp.svd(B)
 leading=a2*a2-1
 assert abs(a2+mp.mpf(5)/4)<mp.mpf('.01') if power>=2 else True
 out.append({'e':str(e),'raw_sigma_min':float(sa[2]),'confluent_sigma_min':float(sb[2]),'a1':float(a1),'a2':float(a2),'norm_leading_coefficient':float(leading)})
Path(__file__).with_suffix('.json').write_text(json.dumps({'precision_digits':90,'cases':out,'scope':'High-precision diagnostic of a regular physical kernel with singular raw evaluation rows; no general arithmetic theorem.'},indent=2)+'\n');print(json.dumps(out,indent=2))
