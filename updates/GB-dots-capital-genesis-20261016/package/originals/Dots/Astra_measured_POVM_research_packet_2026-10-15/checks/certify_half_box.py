import numpy as np,sympy as s,json
from pathlib import Path
root=Path(__file__).resolve().parent.parent/'certificates';raw=np.load(Path(__file__).resolve().parent.parent/'data'/'huang_theta_pi_over_4_printed.npy');A=np.load(root/'half_millibox_interior_candidate.npy');den=10**8
inds=[(i,i,0)for i in range(4)]+[(i,j,0)for i in range(4)for j in range(i+1,4)]+[(i,j,1)for i in range(4)for j in range(i+1,4)]
F=[s.zeros(4)for _ in range(4)]
for i,j,im in inds:
 vals=np.array([a[i,j].imag if im else a[i,j].real for a in A]);lo=[];hi=[]
 for e in raw:
  xs=[e[i,j].imag,-e[j,i].imag]if im else[e[i,j].real,e[j,i].real]
  lo.append(round((max(xs)-.0005)*den));hi.append(round((min(xs)+.0005)*den))
 v=np.clip(np.rint(vals*den).astype(np.int64),lo,hi);target=den if i==j else 0;err=int(target-v.sum())
 for k in range(4):
  change=min(err,hi[k]-v[k]) if err>=0 else max(err,lo[k]-v[k]);v[k]+=change;err-=change
 assert err==0
 for k,x in enumerate(v):
  x=s.Rational(int(x),den)
  if im:F[k][i,j]+=s.I*x;F[k][j,i]-=s.I*x
  elif i==j:F[k][i,i]=x
  else:F[k][i,j]+=x;F[k][j,i]+=x
E=[s.Matrix(np.rint(e.real*1000).astype(int))/1000+s.I*s.Matrix(np.rint(e.imag*1000).astype(int))/1000 for e in raw]
for f,e in zip(F,E):
 assert f==f.conjugate().T
 assert all(f[:k,:k].det()>0 for k in range(1,5))
 for x in f-e:assert abs(s.re(x))<=s.Rational(1,2000) and abs(s.im(x))<=s.Rational(1,2000)
assert sum(F,s.zeros(4))==s.eye(4)
obj={'denominator':den,'meaning':'existence witness inside componentwise 0.0005 box, not actual apparatus POVM','effects':[{'real_numerators':[[int(s.re(x)*den)for x in row]for row in f.tolist()],'imag_numerators':[[int(s.im(x)*den)for x in row]for row in f.tolist()]}for f in F],'all_exact_checks':'PASS'}
(root/'physical_half_box_candidate.json').write_text(json.dumps(obj,indent=2));print('PASS: rational positive-definite complete POVM inside componentwise real/imag +/-0.0005 box.')
