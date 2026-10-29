"""Exact dyadic matrix-ball verification; infinity norm throughout."""
import json,time,numpy as np,sympy as sp,sys
from pathlib import Path
from fractions import Fraction as F
P=Path(__file__).parent;SRC=Path('producer-workspace/grevlex_value_oracle_20261029');j=json.loads((SRC/'quotient.json').read_text());f=json.loads((P/'left_eigenvector_finder.json').read_text());n=40;S=1<<f['dyadic_bits'];st=time.time();I=np.eye(n,dtype=object)*S

def norm(A):return F(max(sum(abs(int(x)) for x in row) for row in A),S)
def add(a,b):return a[0]+b[0],a[1]+b[1]
def scale(a,c):
 c=F(c);return np.array([[int(x)*c.numerator//c.denominator for x in row] for row in a[0]],dtype=object),abs(c)*a[1]+F(n,S)
def mul(a,b):
 return (a[0]@b[0])//S,norm(a[0])*b[1]+norm(b[0])*a[1]+a[1]*b[1]+F(n,S)
def sub(a,b):return a[0]-b[0],a[1]+b[1]
def bound(a):return norm(a[0])+a[1]
def saved(key):return np.array([[int(x) for x in row] for row in f[key]],dtype=object),F(0)
M=[]
for cols in j['multiplication_columns']:
 M.append((np.array([[int(F(cols[c][r])*S) for c in range(n)] for r in range(n)],dtype=object),F(n,S)))
powers=[];Q=(I.copy(),F(0))
for A in M:
 A2=mul(A,A);powers.append([(I,F(0)),A,A2,mul(A2,A)]);Q=add(Q,A2)
N=(np.zeros((n,n),dtype=object),F(0))
for e,c in j['f0_terms']:
 v=(I,F(0))
 for k,a in enumerate(e):
  if a:v=mul(v,powers[k][a])
 N=add(N,scale(v,F(c)))
CQ=saved('approximate_Q_inverse_integer');rq=bound(sub((I,F(0)),mul(CQ,Q)));assert rq<1
invQ=norm(CQ[0])/(1-rq);L=saved('approximate_L_integer');res=bound(sub(mul(Q,L),scale(N,F(1,4))));errL=invQ*res
mid=F(f['midpoint']);lb,ub=map(F,f['root_interval']);assert lb<mid<ub
cs=list(map(int,json.loads((SRC/'candidate.json').read_text())['integer_coefficients_low_to_high']));t=sp.Symbol('t');poly=sp.Poly.from_list(cs[::-1],t);old_iv=json.loads((SRC/'root_candidate_certificate.json').read_text())['least_real_value_interval'];verified_iv=sp.refine_root(poly,sp.Rational(old_iv[0]),sp.Rational(old_iv[1]),eps=sp.Rational(1,2**100),fast=True);assert list(map(str,verified_iv))==f['root_interval']
rad=max(mid-lb,ub-mid)
A=L[0].T.copy();diag=int(mid*S)
for k in range(n):A[k,k]-=diag
A[0,:]=0;A[0,0]=S
Aball=(A,n*errL+rad+F(1,S));CA=saved('approximate_A_inverse_integer');ra=bound(sub((I,F(0)),mul(CA,Aball)));assert ra<1
w=[F(int(x),S) for x in CA[0][:,0]];errw=ra/(1-ra)*max(map(abs,w));assert w[0]-errw<=1<=w[0]+errw
out={'status':'EXACT_INTERVAL_LEFT_EIGENVECTOR_CERTIFICATE','seconds':time.time()-st,'Q_inverse_residual_bound':str(rq),'L_infinity_error_bound':str(errL),'A_inverse_residual_bound':str(ra),'evaluation_vector_infinity_error_bound':str(errw),'coordinate_intervals':[[str(w[i]-errw),str(w[i]+errw)] for i in [3,2,1]],'root_interval':f['root_interval'],'error_float':float(errw),'scope':'Conditional only on already exactly verified simple value polynomial and its exact isolated least root. Every matrix-ball operation and inverse-residual inequality here is rational exact.'};(P/'left_interval_certificate.json').write_text(json.dumps(out,indent=2)+'\n');print('rq',float(rq),'ra',float(ra),'errw',float(errw),'seconds',time.time()-st)

sys.path.insert(0,str(SRC/'received'));from quartic_sos_oracle import rational_candidate,exact_eval
q=rational_candidate([1]+[float(w[i]) for i in [3,2,1]],bits=36);assert sum(x*x for x in q)==1
inp=json.loads((SRC/'received/input.json').read_text());orig={tuple(e):F(v) for e,v in zip(inp['exponents'],inp['original'])};upper=exact_eval(orig,q);lower=lb-F(inp['objective_bias_bound']);gap=upper-lower;assert gap<F(inp['target_gap'])
(P/'left_feasible_certificate.json').write_text(json.dumps({'status':'EXACT_GLOBAL_GAP_FROM_CERTIFIED_LEFT_EIGENVECTOR','rational_unit_quaternion':list(map(str,q)),'exact_original_upper':str(upper),'exact_original_lower':str(lower),'exact_gap':str(gap),'gap_float':float(gap),'scope':'No local optimizer and no coordinate numerator polynomial used. Depends on exact grevlex value-polynomial proof plus exact interval residual certificate.'},indent=2)+'\n')
print('exactgap',float(gap))
