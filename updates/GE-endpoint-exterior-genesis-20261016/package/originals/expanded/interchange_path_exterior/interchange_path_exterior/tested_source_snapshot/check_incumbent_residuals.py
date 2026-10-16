"""Bounded diagnostic of CRAM sparse shifted solves on the SAME 20-site case.
Published numeric coefficient data from Pusa (2012), Table 2, transcribed here.
Own execution code. This is NOT a certified exponential algorithm: scalar
CRAM approximation and coefficient truncation are not validated here.
Exact Fraction residuals ARE a rigorous check of the computed linear solves.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from fractions import Fraction as F
import sys,json,time,math
from pathlib import Path
import numpy as np
from scipy.sparse import csc_matrix,eye
from scipy.sparse.linalg import splu
sys.path.insert(0,'/workspace/shared/interchange_local_saturation')
from rigorous_pair_certificate import pair_H
from exterior_certificate import PathSurvival
TH=[(-10.843917078696988026,19.277446167181652284),(-5.2649713434426468895,16.220221473167927305),(5.9481522689511774808,3.5874573620183222829),(3.5091036084149180974,8.4361989858843750826),(6.4161776990994341923,1.1941223933701386874),(1.4193758971856659786,10.925363484496722585),(4.9931747377179963991,5.9968817136039422260),(-1.4139284624888862114,13.497725698892745389)]
AL=[(-5.090152186522491565e-7,-2.422001765285228797e-5),(2.115174218246603091e-4,4.389296964738067392e-3),(113.39775178483930527,101.94721704215856450),(15.059585270023467528,-5.751405277642181998),(-64.500878025539646595,-224.59440762652096056),(-1.479300711355799972,1.768658832378293791),(-62.518392463207918892,-11.190391094283228480),(4.102313683541002127e-2,-1.574346617345546819e-1)]
n=20;ed=[(i,i+1) for i in range(n-1)];sets={'original':[10**i for i in range(n-1)],'boost':[1,10]+[10**n]*(n-3)};results=[]
for name,rates in sets.items():
 H,ei=pair_H(n,ed,rates);d=len(H);t=F(1,2)
 rows=[[(j,int(x)) for j,x in enumerate(row) if x] for row in H]
 A=csc_matrix(np.array(H,dtype=float))*float(t);v=np.ones(d);y=np.full(d,2.1248537104952237488e-16);checks=[];begin=time.perf_counter()
 for th,al in zip(TH,AL):
  theta=complex(*th);alpha=complex(*al);lu=splu(A+theta*eye(d,format='csc'));z=lu.solve(v);y-=2*np.real(alpha*z)
  zr=[F.from_float(float(x.real)) for x in z];zi=[F.from_float(float(x.imag)) for x in z];a,b=map(F.from_float,th);maxres=F(0)
  for i,row in enumerate(rows):
   re=t*sum((w*zr[j] for j,w in row),F(0))+a*zr[i]-b*zi[i]-1
   im=t*sum((w*zi[j] for j,w in row),F(0))+a*zi[i]+b*zr[i]
   maxres=max(maxres,abs(re)+abs(im))
  # |complex residual| <= |Re|+|Im|. Positive real shift: M-matrix max principle.
  # Other shifts: spectral 2-norm resolvent, then norm equivalence.
  bound=maxres/a if a>0 else maxres*(math.isqrt(d)+1)/abs(b)
  checks.append(dict(theta=[float(a),float(b)],residual_complex_l1_upper_exact=str(maxres),residual_complex_l1_upper_float=float(maxres),linear_solution_infinity_error_bound_exact=str(bound),linear_solution_infinity_error_bound_float=float(bound),LU_nnz=lu.L.nnz+lu.U.nnz))
 ob=PathSurvival(rates,90);lo,hi=ob.at(t)
 results.append(dict(name=name,pair_states=d,pair_nnz=sum(len(x) for x in rows),seconds_including_exact_residuals=time.perf_counter()-begin,
  exact_residual_checks=checks,CRAM_output_min=float(y.min()),CRAM_output_max=float(y.max()),
  adjacent_CRAM_float=[float(y[i]) for i in ei],
  adjacent_integer_certificate_midpoints=[float(F(l+h,2*ob.D)) for l,h in zip(lo,hi)],
  largest_adjacent_diagnostic_discrepancy=max(abs(float(y[i])-float(F(l+h,2*ob.D))) for i,l,h in zip(ei,lo,hi))))
out=dict(source='https://arxiv.org/html/1206.2880#S2',scope='same graph and t=1/2 only; eight sparse complex shifts per generator, double precision proposals with exact rational residual verification; not an exponential certificate',results=results)
Path(__file__).with_name('incumbent_residual_receipt.json').write_text(json.dumps(out,indent=2))
for r in results: print(r['name'],r['largest_adjacent_diagnostic_discrepancy'],max(q['linear_solution_infinity_error_bound_float'] for q in r['exact_residual_checks']))
