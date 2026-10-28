"""Exact general-ray receiver and fresh qutrit CMI-index replay.
Synthetic matrices; ordinary entropy numbers are separate floating controls.
"""
import sympy as s
import numpy as np
from pathlib import Path
import json,time
OUT=Path(__file__).resolve().parent/'outputs';OUT.mkdir(exist_ok=True)
start=time.perf_counter()
def rec(A):return [[str(x) for x in row] for row in A.tolist()]
def ceil_log2(x):
 x=s.Rational(x);n=int(s.numer(x));d=int(s.denom(x));k=max(0,n.bit_length()-d.bit_length())
 while (1<<k)*d<n:k+=1
 while k and (1<<(k-1))*d>=n:k-=1
 return k
def ta(A,d):return s.Matrix(d,d,lambda i,j:sum(A[a*d+i,a*d+j] for a in range(3)))
def chan(A,d):
 pt=s.Matrix(3*d,3*d,lambda i,j:A[(j//d)*d+i%d,(i//d)*d+j%d])
 return (s.kronecker_product(s.eye(3),ta(A,d))-pt)/2
def ef(A,d):return s.kronecker_product(s.eye(3)/3,ta(A,d))
def entropy_f(A):
 v=np.linalg.eigvalsh(np.array(A.tolist(),dtype=float));assert min(v)>-1e-12
 v=v[v>1e-15];return float(v@np.log(v))
om=s.Matrix([int(i==j) for i in range(3) for j in range(3)]);p=om*om.T/3
rows=[]
S=s.zeros(3);S[0,1]=S[1,0]=1;T=s.diag(1,-1,0)
Hstar=(s.eye(9)+s.kronecker_product(S,T)/4)/9
assert Hstar.eigenvals()=={s.Rational(1,12):2,s.Rational(1,9):5,s.Rational(5,36):2}
u=s.Matrix(range(1,19));Hgeneral=(s.eye(18)+u*u.T)/(18+(u.T*u)[0])
for r,C,H,label in [(1,s.eye(1),Hstar,'outside_reset_closure'),(2,s.diag(1,2),Hgeneral,'general_non_TP_direction')]:
 d=3*r;assert s.trace(H)==1
 m=s.Rational(1);M=s.Rational(r);ell=s.trace((s.eye(9*r)-s.kronecker_product(p,s.eye(r)))*H)
 assert 0<ell<=1
 L=ceil_log2(24*r/ell);K=ceil_log2(4*M/m);j=int(s.ceiling(4*K/ell));k=2*L+j+1;eps=m/s.Integer(2)**k
 X=s.kronecker_product(om*om.T,C)+eps*H
 raw=eps*ell/3;normalized=raw/s.trace(X)
 assert s.Rational(ell,2)*k-ell*L-2*K>=ell/2
 marg=s.Matrix(3,3,lambda i,j:sum(H[i*d+a,j*d+a] for a in range(d)))
 block=X[:d,d:2*d];square=block*block
 assert square!=s.zeros(d)
 if r==1:
  assert ell==s.Rational(8,9) and k==20
  assert normalized==s.Rational(8,84934683)
  assert square==s.diag(1,1,0)/(1296*s.Integer(2)**40)
 else:assert marg!=s.eye(3)/3
 numbers=list(C)+list(H)+[eps,raw,normalized]
 row={'label':label,'r':r,'C':rec(C),'H':rec(H),'trace_H':str(s.trace(H)),'leakage':str(ell),
  'L':L,'K':K,'j':j,'k':k,'epsilon':str(eps),'raw_Delta_lower':str(raw),'normalized_CMI_excess_lower':str(normalized),
  'H_physical_marginal':rec(marg),'physical_marginal_uniform':marg==s.eye(3)/3,
  'source_offdiagonal_square':rec(square),'outside_declared_reset_bath_closure':True,
  'reference_dimension_before_twirl':d,'reference_dimension_after_twirl':d if r==1 else 9*d,
  'max_numerator_bits':max(abs(int(s.numer(x))).bit_length() for x in numbers),
  'max_denominator_bits':max(int(s.denom(x)).bit_length() for x in numbers),
  'input_scalar_entries_C_H':r*r+(9*r)**2,'input_scope':'synthetic exact matrices; no physical acquisition'}
 (OUT/f'POSITIVE_RAY_INPUT_R{r}.json').write_text(json.dumps(row,indent=2)+'\n')
 ctrl=time.perf_counter();delta=entropy_f(X)+entropy_f(ef(X,d))-2*entropy_f(chan(X,d))
 rows.append({key:val for key,val in row.items() if key not in ['C','H','H_physical_marginal','source_offdiagonal_square']}|
  {'ordinary_Delta_numeric':delta,'ordinary_normalized_excess_numeric':delta/float(s.trace(X)),
   'ordinary_scope':'floating eigvalsh, not an entropy enclosure','ordinary_seconds':time.perf_counter()-ctrl})
def levi(i,j,k):
 if len({i,j,k})<3:return 0
 p=[int(i),int(j),int(k)];return (-1)**sum(p[a]>p[b] for a in range(3) for b in range(a+1,3))
V=s.Matrix(9,3,lambda row,col:levi(col,row//3,row%3))
swap=s.Matrix(9,9,lambda i,j:int(i//3==j%3 and i%3==j//3));anti=(s.eye(9)-swap)/2
assert V.T*V==2*s.eye(3) and V*V.T/2==anti
components=0
for i in range(3):
 for j in range(3):
  z=s.zeros(3);z[i,j]=1;full=V*z*V.T/2;expected=(int(i==j)*s.eye(3)-z.T)/2
  first=s.Matrix(3,3,lambda a,b:sum(full[3*a+h,3*b+h] for h in range(3)))
  second=s.Matrix(3,3,lambda a,b:sum(full[3*h+a,3*h+b] for h in range(3)))
  assert first==second==expected;components+=2
  tw=s.zeros(3)
  for aa in range(3):
   counts=[sum((bb*(i-j))%3==q for bb in range(3)) for q in range(3)]
   if i==j:phase_sum=3
   else:assert counts==[1,1,1];phase_sum=0
   tw[(i+aa)%3,(j+aa)%3]+=s.Rational(phase_sum,9)
  assert tw==int(i==j)*s.eye(3)/3
assert chan((s.eye(9)+swap)/2,3)==s.Rational(3,4)*(s.eye(9)-p)
result={'status':'EXACT_GENERAL_RAY_RECEIVER_ACQUIRED; independent analytic root derivation separate',
 'rows':rows,'antisymmetric_isometry_channel_components_exact':components,'Weyl_twirl_matrix_units_exact':9,
 'adjoint_leakage_identity_exact':True,'CMI_entropy_offset':'log3 nats, not log9r; Delta raw divided by source trace',
 'elapsed_seconds_excluding_imports':time.perf_counter()-start,
 'global_contraction':'NOT_ESTABLISHED in this programme','historical_priority':'UNKNOWN','physical_implementation':'NOT_ACQUIRED'}
(OUT/'POSITIVE_RAY_ACQUISITION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
