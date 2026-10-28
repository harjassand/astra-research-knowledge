"""Compile exact rational inputs with the independently strengthened radius.
The theorem belongs to quantum_boundary_review; this is a consuming operation.
"""
from pathlib import Path
import sympy as s
import numpy as np
import json,time
OUT=Path(__file__).resolve().parent/'outputs';start=time.perf_counter()
def rec(A):return [[str(x) for x in row] for row in A.tolist()]
def loadmat(rows):return s.Matrix([[s.Rational(v) for v in row] for row in rows])
def psd(A):
 assert A==A.T;B=A.copy();bits=0
 for i in range(A.rows):
  assert B[i,i]>=0
  if B[i,i]==0:assert all(B[i,j]==0 for j in range(i+1,A.rows));continue
  pivot=B[i,i]
  for j in range(i+1,A.rows):
   for k in range(j,A.rows):B[j,k]-=B[j,i]*B[i,k]/pivot;B[k,j]=B[j,k]
  bits=max(bits,max(max(abs(int(s.numer(v))).bit_length(),int(s.denom(v)).bit_length()) for v in B))
 return bits
def ta(A,d):return s.Matrix(d,d,lambda i,j:sum(A[a*d+i,a*d+j] for a in range(3)))
def chan(A,d):
 pt=s.Matrix(3*d,3*d,lambda i,j:A[(j//d)*d+i%d,(i//d)*d+j%d])
 return (s.kronecker_product(s.eye(3),ta(A,d))-pt)/2
def ef(A,d):return s.kronecker_product(s.eye(3)/3,ta(A,d))
def ff(A):
 e=np.linalg.eigvalsh(np.array(A.tolist(),dtype=float));assert min(e)>-1e-12
 e=e[e>1e-15];return float(e@np.log(e))
om=s.Matrix([int(i==j) for i in range(3) for j in range(3)]);p=om*om.T/3
rows=[]
for r in [1,2]:
 case_start=time.perf_counter();old=json.loads((OUT/f'POSITIVE_RAY_INPUT_R{r}.json').read_text())
 C=loadmat(old['C']);H=loadmat(old['H']);m=s.Rational(1);d=3*r
 matrix_bits=max(psd(H),psd(C-m*s.eye(r)));assert s.trace(H)==1
 ell=s.trace((s.eye(9*r)-s.kronecker_product(p,s.eye(r)))*H);assert ell>0
 eps=m*ell**2/(2**14*r*r);X=s.kronecker_product(om*om.T,C)+eps*H
 raw=eps*ell/2;normalized=raw/s.trace(X);square=X[:d,d:2*d]**2
 assert square!=s.zeros(d)
 if r==1:
  assert eps==s.Rational(1,20736) and raw==s.Rational(1,46656)
  assert normalized==s.Rational(4,559881)
 numbers=list(C)+list(H)+list(X)+list(square)+[eps,raw,normalized]
 record={'r':r,'C':rec(C),'H':rec(H),'source_X':rec(X),'leakage':str(ell),'m':str(m),
  'epsilon':str(eps),'source_trace':str(s.trace(X)),'raw_Delta_lower':str(raw),
  'normalized_CMI_excess_lower':str(normalized),'physical_marginal_uniform':old['physical_marginal_uniform'],
  'reference_dimension_after_twirl':old['reference_dimension_after_twirl'],
  'outside_declared_reset_bath_closure':True,'source_offdiagonal_square':rec(square),
  'max_recorded_numerator_bits':max(abs(int(s.numer(v))).bit_length() for v in numbers),
  'max_recorded_denominator_bits':max(int(s.denom(v)).bit_length() for v in numbers),
  'max_Schur_reduced_rational_bits':matrix_bits,'input_matrix_entries':r*r+(9*r)**2,
  'exact_input_verification_and_receiver_seconds':time.perf_counter()-case_start,
  'theorem_authority':'../quantum_boundary_review/ polynomial-radius proof; not producer novelty',
  'physical_input':'synthetic supplied rational matrices; no hardware acquisition'}
 (OUT/f'QUADRATIC_RAY_INPUT_R{r}.json').write_text(json.dumps(record,indent=2)+'\n')
 control=time.perf_counter();delta=ff(X)+ff(ef(X,d))-2*ff(chan(X,d))
 rows.append({k:v for k,v in record.items() if k not in ['C','H','source_X','source_offdiagonal_square']}|
  {'ordinary_Delta_numeric':delta,'ordinary_normalized_excess_numeric':delta/float(s.trace(X)),
   'ordinary_entropy_scope':'floating eigvalsh, not an enclosure','ordinary_seconds':time.perf_counter()-control})
result={'status':'EXACT_QUADRATIC_RAY_RECEIVER_ACQUIRED; theorem reviewed separately',
 'rows':rows,'elapsed_seconds_excluding_imports':time.perf_counter()-start,
 'arithmetic_scope':'rational Schur PSD and scalar radius; maxima exclude unreduced Fraction temporaries',
 'global_contraction':'NOT_ESTABLISHED in this programme','priority':'UNKNOWN','physical_implementation':'NOT_ACQUIRED'}
(OUT/'QUADRATIC_RAY_ACQUISITION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
