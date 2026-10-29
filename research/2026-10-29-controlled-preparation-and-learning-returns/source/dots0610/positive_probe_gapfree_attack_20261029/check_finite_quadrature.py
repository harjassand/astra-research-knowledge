# Small-dimensional diagnostic of ACTUAL-discrete-moment inversion, not a35D implementation.
import numpy as np,json,math
from fractions import Fraction as F
from pathlib import Path
from numpy.polynomial.legendre import leggauss
p=Path(__file__).parent;T=8;d=2;r=F(1,8);gamma=4*math.ceil(math.log2(10*d*T))
# K={(a,y):1/2<=a<=1, |y|<=a}; p proportional exp(-b·x).
b=np.array([4.,-3.]);g,w=leggauss(128);aa=(g+3)/4;wa=w/4;zz=g;wz=w
Z=0.;mu=np.zeros(2);S=np.zeros((2,2))
for a,aw in zip(aa,wa):
 for z,zw in zip(zz,wz):
  x=np.array([a,a*z]);mass=aw*zw*a*np.exp(-b@x);Z+=mass;mu+=mass*x;S+=mass*np.outer(x,x)
mu/=Z;S/=Z
rows=[]
for n in [4,8,16,32,64]:
 records=[];den=1<<50
 for i in range(n):
  a=F(2*n+2*i+1,4*n)
  for j in range(n):
   z=F(2*j+1-n,n);x=(a,a*z);mass=max(1,round(math.exp(-float(b[0])*float(x[0])-float(b[1])*float(x[1]))*float(a)*den));records.append((x,mass))
 total=sum(m for x,m in records);mean=[sum((x[i]*m for x,m in records),F(0))/total for i in range(2)];M=[[sum((x[i]*x[j]*m for x,m in records),F(0))/total for j in range(2)] for i in range(2)]
 det=M[0][0]*M[1][1]-M[0][1]*M[1][0];assert det>0
 inv=[[M[1][1]/det,-M[0][1]/det],[-M[1][0]/det,M[0][0]/det]]
 ell=[F(2,5),F(2,5)] # physical +arm failure.8, -armfailure0; Z=aY.
 ExZ=[sum((x[i]*sum(x[j]*ell[j] for j in range(2))*m for x,m in records),F(0))/total for i in range(2)]
 recovered=[sum(inv[i][j]*ExZ[j] for j in range(2)) for i in range(2)];assert recovered==ell
 Mn=np.array(M,float);err=float(np.linalg.norm(np.array(mean,float)-mu));min_cov=float(np.linalg.eigvalsh(Mn-S/2).min());maxlev=max(float(np.array(x,float)@np.linalg.solve(S,np.array(x,float))) for x,m in records)
 rows.append({'mesh_per_axis':n,'finite_support_points':n*n,'mean_error_vs_high_order_numeric_integral':err,'target_mean_tolerance':float(r/(4*T*T)),'covariance_M_minus_S_over2_min_eigenvalue':min_cov,'maximum_support_leverage':maxlev,'leverage_limit':2*d*gamma*gamma,'exact_rational_estimator_unbiased':True,'M_determinant_positive_exact':True})
assert rows[-1]['mean_error_vs_high_order_numeric_integral']<float(r/(4*T*T)) and min_cov>0 and maxlev<2*d*gamma*gamma
out={'scope':'2D rational finite quadrature diagnostic; covariance inversion and unbiasedness are EXACT Fraction algebra. Continuous comparison is high-order floating quadrature, NOT an interval certificate. No35D controller or learning run claimed.','rows':rows};(p/'finite_quadrature_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
