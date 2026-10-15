"""Exact certificate for a full, infinitely supported, dependent scalar regularizer.

No truncated constraint grid is used in this certificate. The proof reduces the
infinite lattice to a finite core, finitely many strip types, and one tail type.
"""
from fractions import Fraction as F
import json
from pathlib import Path

D=Path(__file__).parent
C=[
 [1000000,149000,5200,14],
 [149000,48600,7120,72],
 [5200,7120,2450,420],
 [14,72,420,73],
]
N=3
q=F(11,64)
u=(1-q)/(1+q)
checks=[]
for i in range(N):
 for j in range(N):
  a,b,c,d=C[i][j],C[i+1][j],C[i][j+1],C[i+1][j+1]
  total=a+b+c+d;dx=a+c-b-d;dy=a+b-c-d
  det=total*total-dx*dx-dy*dy
  assert total>0 and det>0
  checks.append({'core_cell':[i,j],'S_squared_minus_dx_squared_minus_dy_squared':str(det)})
for j in range(N):
 x,y=C[N][j],C[N][j+1]
 det=(1-u*u)*(x+y)**2-(x-y)**2
 assert det>0
 checks.append({'strip_pair':[j,j+1],'reduced_determinant':str(det)})
assert 2*u*u<1
m=[F(1),F(2),F(2),2/(1-q)]
t=[F(0),F(2),F(8),2*(N*N/(1-q)+2*N*q/(1-q)**2+q*(1+q)/(1-q)**3)]
Z=sum(m[i]*m[j]*C[i][j] for i in range(N+1) for j in range(N+1))
T=4*sum((t[i]*m[j]+m[i]*t[j])*C[i][j] for i in range(N+1) for j in range(N+1))/Z
assert T<F(321,100)
assert T<F(4)
out={
 'status':'all exact rational positivity checks passed',
 'noise_law':'P(N=(2k,2l)) = C[min(abs(k),3),min(abs(l),3)] * q**(max(abs(k)-3,0)+max(abs(l)-3,0)) / Z',
 'q':str(q),'C':C,'Z':str(Z),
 'normalized_trace':str(T),'trace_decimal':float(T),
 'per_coordinate_variance':str(T/2),'variance_decimal':float(T/2),
 'cross_covariance':0,'all_tail_2u_squared':str(2*u*u),
 'checks':checks,
 'scope':'analytic infinite tail reduction and exact rational finite core certificate; not a floating point or truncated LP certificate',
}
(D/'exact_construction_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','q','Z','normalized_trace','trace_decimal','variance_decimal','all_tail_2u_squared']},indent=2))
