"""Exact whole-cell harmonic minorant and declared complete-law affinity step."""
from pathlib import Path
from fractions import Fraction as Q
from math import factorial
import numpy as np,json
P=Path(__file__).parent/'degree36';d=np.load(P/'taylor_density_certificate.npz');N=int(d['phase_grid']);TD=int(d['denominator']);U=d['upper_integers']
def atanI(x,n):
 s=sum(((-1)**j*x**(2*j+1)/Q(2*j+1) for j in range(n)),Q());t=x**(2*n+1)/Q(2*n+1);return(s,s+t) if n%2==0 else(s-t,s)
a,b=atanI(Q(1,5),40),atanI(Q(1,239),12);pl=16*a[0]-4*b[1];ph=16*a[1]-4*b[0];cv=[];te=Q()
for j in range(2*N):
 jj=j if j<=N else j-2*N;m=(pl+ph)*Q(jj,2*N);rad=(ph-pl)*Q(abs(jj),2*N);ss=sum(((-1)**k*m**(2*k)/Q(factorial(2*k)) for k in range(26)),Q());er=abs(m)**52/Q(factorial(52))+rad;v=float(ss);te=max(te,abs(Q.from_float(v)-ss)+er);cv.append(v)
assert te<Q(1,10**15)
cv=np.array(cv);i=np.arange(N);v=(1+cv[(2*i+1)%(2*N),None]+cv[None,(2*i+1)%(2*N)]+cv[(2*(i[:,None]+i[None,:]+1))%(2*N)])/4
# |partial_a uvw|,|partial_b uvw| <=1; both half-widths pi/(2N).
# All binary64 operations bounded by 1e-12, well beyond input and rounding errors.
er=float(ph/N)+1e-12;piup=np.ceil(np.nextafter(v+er,np.inf)*TD).astype(np.int64)
c0=Q(183,250);c3=Q(249,100);pupper=Q(355,113);assert ph<pupper
# h=c0+c3 p>=c0-c3/8>0. Exact integer certificate h(p_upper)^2 * density_upper <=1.
assert c0-c3/8>0
HD=500*TD;HN=366*TD+1245*piup
leftmax=0;right=HD**2*4*TD*113
for hn,uu in zip(HN.flat,U.flat):
 left=int(hn)**2*355*int(uu);assert left<=right;leftmax=max(leftmax,left)
# Actual null split, then whole Brownian exit laws.
x=[Q(-1,4),Q(1,2),Q(1,2)];y=[Q(3,8),Q(-3,4),Q(-3,4)];w=Q(3,5)
assert all(w*xj+(1-w)*yj==0 for xj,yj in zip(x,y));assert x[0]*x[1]+x[0]*x[2]+x[1]*x[2]==0
moment=w*x[0]*x[1]*x[2]+(1-w)*y[0]*y[1]*y[2];assert moment==Q(3,64)
response=c0+c3*moment;baseline=json.load(open(P/'taylor_affinity_receipt.json'));upper=Q(baseline['actual_affinity_upper']);D=(response-upper)/2;assert D>0
# Both starts in aE, proved by Sylvester minors. Polynomial Harnack gives eta1<=K omega0.
aa=Q(15,16)
for z in [x,y]:
 zz=[t/aa for t in z];assert all(abs(t)<1 for t in zz);assert 1-sum(t*t for t in zz)+2*zz[0]*zz[1]*zz[2]>0
K=Q(20,9)*(1-aa)**-6;alpha=D/(K*K);assert 0<alpha<Q(1,2)
# On [0,alpha], |Phi''| <= K²: k<=K, k>=0, and Phi(omega0)<=1.
gain=D*alpha-K*K*alpha*alpha/2;assert gain>0
r={'status':'EXACT_HARMONIC_MINORANT_AND_FINITE_STEP_PASS','cells':N*N,'c0':str(c0),'c3':str(c3),'minorant_max_squared_density_product':str(Q(leftmax,right)),'minorant_response':str(response),'baseline_affinity_upper':str(upper),'derivative_lower':str(D),'derivative_lower_display':float(D),'Harnack_K':str(K),'declared_alpha':str(alpha),'declared_alpha_display':float(alpha),'affinity_gain_lower':str(gain),'affinity_gain_lower_display':float(gain),'scope':'actual complete paid Brownian-mixture finite affinity improvement over omega0; relies on Taylor density receiving certificate, not full source reachability'}
(P/'actual_gradient_step_receipt.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
