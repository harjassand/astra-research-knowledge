#!/usr/bin/env python3
"""Independent standard-library exact replay. No source author's code imported."""
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement
from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parent
SRC=ROOT/'certificate_as_received.json'
b=SRC.read_bytes(); data=json.loads(b)
N=10; zero=(0,)*N

def add(*ps):
 r={}
 for p in ps:
  for e,c in p.items(): r[e]=r.get(e,F(0))+c
 return {e:c for e,c in r.items() if c}
def scale(p,c): return {e:c*v for e,v in p.items() if c*v}
def mul(p,q):
 r={}
 for e,c in p.items():
  for f,d in q.items():
   g=tuple(x+y for x,y in zip(e,f));r[g]=r.get(g,F(0))+c*d
 return {e:c for e,c in r.items() if c}
def deriv(p,i):
 r={}
 for e,c in p.items():
  if e[i]:
   f=list(e);f[i]-=1;r[tuple(f)]=c*e[i]
 return r
def var(i):
 e=list(zero);e[i]=1;return {tuple(e):F(1)}
x=[var(i) for i in range(4)]; z=[var(i) for i in range(4,10)]
a,b,c,d=x
u=add(mul(a,a),mul(c,c));v=add(mul(b,b),mul(d,d));j=add(mul(a,d),scale(mul(b,c),-1));s=add(u,v,scale(j,-2))
G=add(scale(mul(s,s),3),scale(mul(u,u),F(35,24)),mul(j,j),scale(mul(j,u),F(-5,2)))
C=[[F(v) for v in row] for row in data['basis']]; S=[[F(v) for v in row] for row in data['reduced_gram']];Q=[[F(v) for v in row] for row in data['gram']]
assert len(C)==24 and all(len(r)==18 for r in C)
assert len(S)==18 and all(len(r)==18 for r in S)
assert len(Q)==24 and all(len(r)==24 for r in Q)
assert all(S[i][k]==S[k][i] for i in range(18) for k in range(18))
CS=[[sum(C[i][k]*S[k][l] for k in range(18)) for l in range(18)] for i in range(24)]
assert all(Q[i][j]==sum(CS[i][k]*C[j][k] for k in range(18)) for i in range(24) for j in range(24))
# Derive LDL ourselves, compare all entries, not merely diagonal signs.
L=[[F(i==j) for j in range(18)] for i in range(18)]; piv=[]
for k in range(18):
 p=S[k][k]-sum(L[k][r]**2*piv[r] for r in range(k));assert p>0;piv.append(p)
 for i in range(k+1,18): L[i][k]=(S[i][k]-sum(L[i][r]*L[k][r]*piv[r] for r in range(k)))/p
assert all(S[i][j]==sum(L[i][k]*piv[k]*L[j][k] for k in range(18)) for i in range(18) for j in range(18))
assert piv==[F(t) for t in data['ldl_diagonal']]
# Exact elimination for column rank of C.
R=[r[:] for r in C];rank=0
for col in range(18):
 p=next((i for i in range(rank,24) if R[i][col]),None)
 if p is None:continue
 R[rank],R[p]=R[p],R[rank];q=R[rank][col];R[rank]=[v/q for v in R[rank]]
 for i in range(rank+1,24):
  q=R[i][col];R[i]=[a-q*b for a,b in zip(R[i],R[rank])]
 rank+=1
assert rank==18
assert data['matrix_entry_order']==['a','b','c','d']
assert data['omega_pair_order']==[list(t) for t in combinations(range(4),2)]
assert data['quadratic_coefficient_order']==[list(t) for t in combinations_with_replacement(range(4),2)]
W={}
for pair,row in zip(data['omega_pair_order'],data['omega_coefficients']):
 W[tuple(pair)]=add(*(scale(mul(x[i],x[k]),F(c)) for (i,k),c in zip(data['quadratic_coefficient_order'],row)))
def omega(i,j):return W[i,j] if i<j else scale(W[j,i],-1) if j<i else {}
closed=[]
for i,j,k in combinations(range(4),3):
 p=add(deriv(omega(j,k),i),scale(deriv(omega(i,k),j),-1),deriv(omega(i,j),k));assert not p;closed.append([i,j,k])
alpha=[scale(add(*(mul(x[i],omega(i,k)) for i in range(4))),F(1,4)) for k in range(4)]
assert all(add(deriv(alpha[k],i),scale(deriv(alpha[i],k),-1),scale(omega(i,k),-1))=={} for i,k in combinations(range(4),2))
B1=[z[0],z[1],z[3],z[4]];B2=[z[1],z[2],z[4],z[5]]
D=[[F(v) for v in row] for row in data['diffusion']];assert D==[[F(4897,5000),0],[0,F(5103,5000)]]
H=[[deriv(deriv(G,i),k) for k in range(4)] for i in range(4)]
heat=add(*(scale(mul(H[i][k],mul(B[i],B[k])),weight) for weight,B in [(D[0][0],B1),(D[1][1],B2)] for i in range(4) for k in range(4)))
corr=add(*(mul(W[i,k],add(mul(B1[i],B2[k]),scale(mul(B1[k],B2[i]),-1))) for i,k in combinations(range(4),2)))
Z=[mul(xx,zz) for xx in x for zz in z]
lhs=add(*(scale(mul(Z[i],Z[k]),Q[i][k]) for i in range(24) for k in range(24)))
res=add(lhs,scale(heat,-1),scale(corr,-1)); assert not res
# Enumerate the full bihomogeneous coefficient space independently.
coefs=[]
for i,k in combinations_with_replacement(range(4),2):
 for r,t in combinations_with_replacement(range(4,10),2):
  e=[0]*10
  for ix in [i,k,r,t]:e[ix]+=1
  coefs.append(tuple(e));assert lhs.get(tuple(e),0)==add(heat,corr).get(tuple(e),0)
assert len(coefs)==210 and len(set(coefs))==210
receipt={'certificate_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'expected_hash_matches':hashlib.sha256(SRC.read_bytes()).hexdigest()=='4004e6144335150a5b3569dfb7b4d0b836f2776497c271e7f31b2faf52830000','exact_identity_coefficients_checked':210,'closedness_triples_checked':closed,'primitive_components_checked':6,'basis_rank':rank,'gram_factorization_entries_checked':576,'ldl_reconstruction_entries_checked':324,'positive_ldl_pivots':[str(p) for p in piv],'diffusion':[str(D[0][0]),str(D[1][1])],'residual_terms':len(res),'all_checks_passed':True,'arithmetic':'Python standard-library fractions.Fraction; independently authored polynomial and matrix routines'}
receipt['single_final_newline_sha256']=hashlib.sha256(SRC.read_bytes().rstrip()+b'\n').hexdigest()
receipt['quoted_hash_matches_after_removing_one_extra_final_newline']=receipt['single_final_newline_sha256']=='4004e6144335150a5b3569dfb7b4d0b836f2776497c271e7f31b2faf52830000'
assert receipt['quoted_hash_matches_after_removing_one_extra_final_newline']
(ROOT/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
