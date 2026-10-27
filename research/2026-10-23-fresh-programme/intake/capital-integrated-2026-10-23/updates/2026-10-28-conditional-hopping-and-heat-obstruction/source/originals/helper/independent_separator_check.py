#!/usr/bin/env python3
"""Independent exact checker: sparse polynomial algebra + Fraction LDL only.
Does not import or execute principal code or numerical maps.
"""
from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import json, hashlib

BASE=Path('/Users/harjas/Documents/ChatGPT/coordination/work/astra-opportunity-retrieval-20261027/ultra')
cert_path=BASE/'principal/EXACT_HEAT_SEPARATOR.json'
raw=cert_path.read_bytes(); cert=json.loads(raw)
xpairs=list(combinations_with_replacement(range(4),2))
zpairs=list(combinations_with_replacement(range(6),2))
formpairs=list(combinations(range(4),2))
xindex={v:i for i,v in enumerate(xpairs)};zindex={v:i for i,v in enumerate(zpairs)}
lam=[Q(v) for v in cert['lambda_xpair_zpair']]
assert len(lam)==210

def plus(*polys):
 out={}
 for p in polys:
  for e,c in p.items():out[e]=out.get(e,Q(0))+c
 return {e:c for e,c in out.items() if c}
def scale(p,c):return {e:v*c for e,v in p.items() if v*c}
def times(p,r):
 out={}
 for e,c in p.items():
  for f,d in r.items():
   g=tuple(a+b for a,b in zip(e,f));out[g]=out.get(g,Q(0))+c*d
 return {e:c for e,c in out.items() if c}
def deriv(p,i):
 out={}
 for e,c in p.items():
  if e[i]:
   f=list(e);f[i]-=1;out[tuple(f)]=c*e[i]
 return out

def variable(i):
 e=[0]*4;e[i]=1;return {tuple(e):Q(1)}
x=[variable(i) for i in range(4)];a,b,c,d=x
u=plus(times(a,a),times(c,c));v=plus(times(b,b),times(d,d))
w=plus(times(a,b),times(c,d));det=plus(times(a,d),scale(times(b,c),-1))
basis=[times(u,u),times(v,v),times(u,v),times(w,w),times(u,w),times(v,w),times(det,u),times(det,v),times(det,w)]
p=[Q(t) for t in cert['p']]
assert p==list(map(Q,[1,1,16,-13,0,0,4,-4,0]))
F=plus(*(scale(poly,c) for poly,c in zip(basis,p)))
Fd=times(det,det)
J1=[0,1,3,4];J2=[1,2,4,5]
def eval_coefficient(ex,zi,zj):
 indices=[]
 for i,k in enumerate(ex):indices.extend([i]*k)
 assert len(indices)==2
 return lam[21*xindex[tuple(indices)]+zindex[tuple(sorted((zi,zj)))]]
def diss_pair(poly):
 out=Q(0)
 for i,j in product(range(4),repeat=2):
  h=deriv(deriv(poly,i),j)
  for ex,c in h.items():
   out+=c*(eval_coefficient(ex,J1[i],J1[j])+eval_coefficient(ex,J2[i],J2[j]))
 return out
pair_F=diss_pair(F);pair_det=diss_pair(Fd)
assert pair_F==Q(cert['pair_F'])==Q(-4049717,6250000)
assert pair_det==Q(cert['pair_det2'])==Q(80001,25000000)
assert pair_F<0<pair_det

# All closed quadratic two-forms are exterior derivatives of homogeneous
# cubic one-forms by Cartan's identity. Verify all 4*20=80 generators.
cubic_ex=[]
for ids in combinations_with_replacement(range(4),3):
 e=[0]*4
 for j in ids:e[j]+=1
 cubic_ex.append(tuple(e))
def form_pullback_pair(forms):
 out=Q(0)
 for (i,j),poly in forms.items():
  for ex,c in poly.items():
   out+=c*(eval_coefficient(ex,J1[i],J2[j])-eval_coefficient(ex,J1[j],J2[i]))
 return out
columns=[]
for component in range(4):
 for ex in cubic_ex:
  alpha={ex:Q(1)};forms={}
  for i,j in formpairs:
   pos=deriv(alpha,i) if j==component else {}
   neg=deriv(alpha,j) if i==component else {}
   forms[(i,j)]=plus(pos,scale(neg,-1))
  assert form_pullback_pair(forms)==0
  col=[]
  for ij in formpairs:
   poly=forms[ij]
   for k,l in xpairs:
    e=[0]*4;e[k]+=1;e[l]+=1;col.append(poly.get(tuple(e),Q(0)))
  columns.append(col)

def rank_columns(columns):
 pivots={}
 for column in columns:
  vec=column[:]
  for i in sorted(pivots):
   if vec[i]:
    t=vec[i];vec=[a-t*b for a,b in zip(vec,pivots[i])]
  nz=next((i for i,a in enumerate(vec) if a),None)
  if nz is not None:
   t=vec[nz];pivots[nz]=[a/t for a in vec]
 return len(pivots)
closed_rank=rank_columns(columns)
assert closed_rank==45

# Moment matrix for the 24 independent bilinear coordinates x_i z_j.
M=[[lam[21*xindex[tuple(sorted((i//6,j//6)))]+zindex[tuple(sorted((i%6,j%6)))]] for j in range(24)] for i in range(24)]
def exact_ldl(mat):
 n=len(mat);L=[[Q(int(i==j)) for j in range(n)] for i in range(n)];D=[]
 for i in range(n):
  pivot=mat[i][i]-sum(L[i][k]*L[i][k]*D[k] for k in range(i))
  assert pivot>0,('nonpositive pivot',i,str(pivot));D.append(pivot)
  for j in range(i+1,n):L[j][i]=(mat[j][i]-sum(L[j][k]*L[i][k]*D[k] for k in range(i)))/pivot
 assert all(mat[i][j]==sum(L[i][k]*D[k]*L[j][k] for k in range(n)) for i,j in product(range(n),repeat=2))
 return D
DD=exact_ldl(M)
assert DD==[Q(t) for t in cert['dual_ldl_diagonal']]

def quadratic_matrix(poly):
 out=[[Q(0) for j in range(4)] for i in range(4)]
 for ex,c in poly.items():
  ids=[]
  for i,k in enumerate(ex):ids.extend([i]*k)
  assert len(ids)==2
  i,j=ids
  if i==j:out[i][i]+=c
  else:out[i][j]+=c/2;out[j][i]+=c/2
 return out
M11=quadratic_matrix(deriv(deriv(F,0),0))
M12=quadratic_matrix(deriv(deriv(F,0),1))
M22=quadratic_matrix(deriv(deriv(F,1),1))
K=[[Q(0) for j in range(4)] for i in range(4)]
assert [Q(t) for t in cert['acoustic_skew']]==list(map(Q,[1,0,0,0,0,15]))
for (i,j),t in zip(formpairs,cert['acoustic_skew']):K[i][j]=Q(t);K[j][i]=-Q(t)
A=[[Q(0) for j in range(8)] for i in range(8)]
for i,j in product(range(4),repeat=2):
 A[i][j]=M11[i][j];A[i][j+4]=M12[i][j]+K[i][j]
 A[i+4][j]=M12[i][j]-K[i][j];A[i+4][j+4]=M22[i][j]
AD=exact_ldl(A)
assert AD==[Q(t) for t in cert['acoustic_ldl_diagonal']]
report={
 'status':'EXACT_PASS',
 'checker':'Independent sparse polynomial and Fraction LDL reconstruction; no principal modules/maps executed',
 'certificate_sha256':hashlib.sha256(raw).hexdigest(),
 'coefficient_convention':{'x_pairs':xpairs,'z_pairs':zpairs,'jet1':J1,'jet2':J2,'lambda_order':'x_pair major, z_pair minor'},
 'closed_form_generators_checked':80,
 'closed_form_span_exact_rank':closed_rank,
 'dual_moment_matrix_shape':[24,24],
 'dual_moment_matrix_exact_reconstruction':True,
 'dual_moment_matrix_ldl_all_positive':True,
 'dual_moment_matrix_ldl_matches_certificate':True,
 'pair_F':str(pair_F),'pair_det2':str(pair_det),
 'acoustic_matrix_exact_reconstruction':True,
 'acoustic_ldl_all_positive':True,
 'acoustic_ldl_matches_certificate':True,
 'acoustic_ldl_diagonal':[str(t) for t in AD],
 'scope':'Excludes all identity-diffusion closed homogeneous-quadratic-two-form bilinear-SOS certificates for F-gamma det^2, gamma>=0; symmetry then excludes all constant-SPD spatial diffusion certificates in the same class. Does not establish QC failure.'
}
(BASE/'helper/INDEPENDENT_HEAT_SEPARATOR_CHECK.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='coefficient_convention'},indent=2))
