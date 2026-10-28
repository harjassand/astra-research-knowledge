"""Exact rational input/order/normalization receiver and ordinary entropy control.

All plants here are synthetic supplied matrices. Exact certificates establish
the scalar theorem's hypotheses and consequence. Ordinary eigensolver values
are separate diagnostics, not rigorous matrix-entropy enclosures or audits.
"""
from fractions import Fraction as F
from pathlib import Path
import json,time
import sympy as s
import numpy as np
HERE=Path(__file__).resolve().parent;OUT=HERE/'outputs';OUT.mkdir(exist_ok=True)
def hh(v):
 v=s.Matrix(v);return s.eye(len(v))-2*v*v.T/(v.T*v)[0]
def matrecord(A):return [[str(x) for x in row] for row in A.tolist()]
def trace_a(A,r):
 return s.Matrix(3*r,3*r,lambda i,j:sum(A[a*3*r+i,a*3*r+j] for a in range(3)))
def trans_a(A,r):
 return s.Matrix(9*r,9*r,lambda i,j:A[(j//(3*r))*(3*r)+i%(3*r),(i//(3*r))*(3*r)+j%(3*r)])
def N(A,r):return (s.kronecker_product(s.eye(3),trace_a(A,r))-trans_a(A,r))/2
def E(A,r):return s.kronecker_product(s.eye(3)/3,trace_a(A,r))
def ff(A):
 v=np.linalg.eigvalsh(np.array(A.tolist(),dtype=float));assert min(v)>-1e-11
 v=v[v>1e-14];return float(v@np.log(v))
def acquire(r,flat=False):
 start=time.perf_counter();d=3*r
 Q=hh(list(range(1,r+1)));cs=[s.Rational(1) if flat else s.Rational(j) for j in range(1,r+1)]
 C=Q*s.diag(*cs)*Q.T;m=min(cs);M=max(cs);kappa=M/m;b=m/(512*kappa**2)
 R=hh(list(range(1,d+1)))*hh([j*j+2*j+3 for j in range(1,d+1)])
 ys=[s.Rational(j,d) for j in range(1,d+1)]
 Y=b*R*s.diag(*ys)*R.T
 assert Q.T*Q==s.eye(r) and R.T*R==s.eye(d)
 assert C==Q*s.diag(*cs)*Q.T and Y==b*R*s.diag(*ys)*R.T
 assert min(cs)>0 and min(ys)>0 and max(ys)==1
 assert b<=m/(512*kappa**2)
 om=s.Matrix([int(i==j) for i in range(3) for j in range(3)])
 p=om*om.T/3;swap=s.zeros(9)
 for i in range(3):
  for j in range(3):swap[3*i+j,3*j+i]=1
 pm=(s.eye(9)-swap)/2;ps=s.eye(9)-pm
 A0=s.kronecker_product(om*om.T,C);H=s.kronecker_product(s.eye(3),Y);X=A0+H
 assert N(A0,r)==s.kronecker_product(pm,C)
 assert E(A0,r)==s.kronecker_product(s.eye(9)/3,C)
 assert N(H,r)==H and E(H,r)==H
 T=s.trace(Y);TC=s.trace(C)
 assert s.trace(s.kronecker_product(p,s.eye(r))*H)==T/3
 assert s.trace(s.kronecker_product(pm,s.eye(r))*H)==T
 assert s.trace(X)==3*(TC+T)
 margin=T/(9*(TC+T));rawmargin=T/3
 # Input-side physical marginal: this is an actual TP Choi family.
 marg=s.Matrix(3,3,lambda i,j:sum(X[i*d+k,j*d+k] for k in range(d)))
 assert marg==(TC+T)*s.eye(3)
 realign=s.Matrix(9,r*r,lambda i,j:Y[(i//3)*r+j//r,(i%3)*r+j%r])
 osr=realign.rank();comm=Y*s.kronecker_product(s.eye(3),C)-s.kronecker_product(s.eye(3),C)*Y
 if not flat:assert comm!=s.zeros(d)
 assert osr>2
 numbers=list(C)+list(Y)+list(Q)+list(R)
 exact={'r':r,'flat_C':flat,'m':str(m),'M':str(M),'b':str(b),'kappa':str(kappa),
  'C':matrecord(C),'C_orthogonal_factor':matrecord(Q),'C_spectrum':[str(x) for x in cs],
  'Y':matrecord(Y),'Y_orthogonal_factor':matrecord(R),'Y_spectrum_divided_by_b':[str(x) for x in ys],
  'trace_C':str(TC),'trace_Y':str(T),'reset_probability':str(T/(TC+T)),
  'certified_raw_Delta_lower':str(rawmargin),'certified_CMI_excess_nats':str(margin),
  'operator_Schmidt_rank_Y':osr,'Y_commutes_with_I_tensor_C':comm==s.zeros(d),
  'max_rational_numerator_bits':max(abs(int(s.numer(x))).bit_length() for x in numbers),
  'max_rational_denominator_bits':max(int(s.denom(x)).bit_length() for x in numbers),
  'explicit_C_Y_entries':r*r+d*d,'full_source_matrix_dimension':9*r,
  'operator_order_certificate':'exact rational orthogonal factors and ordered diagonal spectra',
  'physical_input':'synthetic matrices; no measured channel',
  'exact_receiver_and_input_seconds':time.perf_counter()-start}
 filename=f'WEAK_RESET_INPUT_R{r}'+('_FLAT' if flat else '')+'.json'
 (OUT/filename).write_text(json.dumps(exact,indent=2)+'\n')
 compare_start=time.perf_counter();delta=ff(X)+ff(E(X,r))-2*ff(N(X,r))
 row={k:v for k,v in exact.items() if k not in ['C','Y','C_orthogonal_factor','Y_orthogonal_factor','C_spectrum','Y_spectrum_divided_by_b']}
 row.update({'ordinary_dense_entropy_Delta_numeric':delta,
  'ordinary_dense_normalized_CMI_excess_nats_numeric':delta/float(3*(TC+T)),
  'numeric_control_scope':'numpy eigvalsh, not an interval certificate',
  'ordinary_dense_control_seconds':time.perf_counter()-compare_start})
 return row
if __name__=='__main__':
 start=time.perf_counter();rows=[acquire(2),acquire(3),acquire(5),acquire(3,flat=True)]
 om=s.Matrix([int(i==j) for i in range(3) for j in range(3)]);p=om*om.T/3
 sw=s.Matrix(9,9,lambda i,j:int(i//3==j%3 and i%3==j//3));ps=(s.eye(9)+sw)/2
 assert N(ps,1)==s.Rational(3,4)*(s.eye(9)-p)
 assert s.Rational(10,27)-s.Rational(1,256)-s.Rational(1,3)==s.Rational(229,6912)>0
 result={'status':'EXACT_SCALAR_RECEIVER_INPUTS_ACQUIRED; analytic theorem unreviewed',
  'rows':rows,'leakage_operator_identity_exact':True,'threshold_log_rational_reduction_exact':True,
  'elapsed_seconds_excluding_imports':time.perf_counter()-start,
  'historical_priority':'UNKNOWN','unrestricted_W3_contraction':'UNRESOLVED',
  'physical_channel_or_metrology':'NOT_ACQUIRED'}
 (OUT/'WEAK_RESET_ACQUISITION.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
