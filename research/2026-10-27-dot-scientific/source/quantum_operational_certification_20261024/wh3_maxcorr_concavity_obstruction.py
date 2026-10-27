from fractions import Fraction as F
from pathlib import Path
import json
I=((F(1),F(0)),(F(0),F(1)))
def add(A,B):return tuple(tuple(A[i][j]+B[i][j] for j in range(2))for i in range(2))
def scale(A,s):return tuple(tuple(x*s for x in row)for row in A)
def mul(A,B):return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2))for j in range(2))for i in range(2))
def inv(A):
 d=A[0][0]*A[1][1]-A[0][1]*A[1][0]
 return ((A[1][1]/d,-A[0][1]/d),(-A[1][0]/d,A[0][0]/d))
def log_scalar(x,n=30):
 y=(x-1)/(x+1);p=2*sum((y**(2*k+1)/F(2*k+1)for k in range(n)),F(0));e=2*abs(y)**(2*n+1)/(F(2*n+1)*(1-y*y));return p,e
def log_matrix(A,n=30):
 Y=mul(add(A,scale(I,-1)),inv(add(A,I)));rho=max(sum(abs(x)for x in row)for row in Y);assert rho<1
 Y2=mul(Y,Y);power=Y;total=scale(I,0)
 for k in range(n):total=add(total,scale(power,F(2,2*k+1)));power=mul(power,Y2)
 e=2*rho**(2*n+1)/(F(2*n+1)*(1-rho*rho));return total,e
def g(b):
 a=F(3,10);x0=F(2,3)+b/3;x1=F(1,6)+a/2+b/3;off=F(1,3)-b/3
 K=((x1/2,-off/2),(-off/2,x0/2));L,e=log_matrix(scale(K,4))
 # vv^T=[[1,-2],[-2,4]]/6; squared norm=5/6.
 pair=(L[0][0]-4*L[0][1]+4*L[1][1])/6
 l0,e0=log_scalar(4*x0/3);l1,e1=log_scalar(4*x1/3);lk,ek=log_scalar(4*(1+2*b)/6)
 return F(2,3)*l0+l1/3-2*pair-lk/3,F(2,3)*e0+e1/3+F(5,3)*e+ek/3
p,ep=g(F(4,5));m,em=g(F(3,5));c,ec=g(F(7,10));v=p+m-2*c;e=ep+em+2*ec
assert v-e>F(1,2000)
out={'status':'EXACT PASS','midpoint_second_difference':float(v),'error_bound':float(e),'certified_lower':'1/2000','scope':'Nonconcavity only, not an entropy-target counterexample','parameters':'u=(2,1,1)/sqrt6; X=P+0.3 qq^T+b ww^T; b=0.6,0.7,0.8; q=(0,1,-1)/sqrt2; w=(-1,1,1)/sqrt3'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
