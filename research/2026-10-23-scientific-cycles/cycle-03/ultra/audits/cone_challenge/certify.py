"""Exact integer certificate for a genuinely physical q=8 Gram cone separation.
Generation mode --generate reads the numerical proposal only. Replay uses only
standard-library exact arithmetic and the saved integer inputs JSON.
"""
import os,sys,json,time,itertools,hashlib,resource
from fractions import Fraction
from pathlib import Path
BASE=Path(__file__).resolve().parent
st=time.perf_counter();cpu=time.process_time()
P=10**10
if '--generate' in sys.argv:
 import numpy as np
 a=np.load(BASE/'q8_alternating_best.npz');U=a['U'];Z=a['Z'];I=np.eye(8)
 A=(U-I)@np.linalg.inv(U+I);A=(A-A.conj().T)/2
 Ar=np.rint(P*A.real).astype(np.int64);Ai=np.rint(P*A.imag).astype(np.int64)
 # Impose exact skew-Hermitian symmetry after independent rounding.
 for i in range(8):
  Ar[i,i]=0
  for j in range(i):Ar[i,j]=-Ar[j,i];Ai[i,j]=Ai[j,i]
 Ur=np.rint(P*U.real).astype(np.int64);Ui=np.rint(P*U.imag).astype(np.int64)
 w,v=np.linalg.eigh(Z);Y=v[:,-4:]@np.diag(np.sqrt(np.maximum(w[-4:],0)));Yi=np.rint(P*Y).astype(np.int64)
 data={'P':P,'Ar':Ar.tolist(),'Ai':Ai.tolist(),'Ur':Ur.tolist(),'Ui':Ui.tolist(),'Y':Yi.tolist()}
 (BASE/'EXACT_INPUTS.json').write_text(json.dumps(data,indent=2)+'\n')
data=json.loads((BASE/'EXACT_INPUTS.json').read_text());P=data['P'];Ar,Ai,Ur,Ui,Y=[data[k] for k in ['Ar','Ai','Ur','Ui','Y']]
q=8
assert all(Ar[i][j]==-Ar[j][i] and Ai[i][j]==Ai[j][i] for i in range(q) for j in range(q))
# R=(I-A)Uhat-(I+A), with denominator P^2.
Rr=[[P*Ur[i][j]-sum(Ar[i][k]*Ur[k][j]-Ai[i][k]*Ui[k][j] for k in range(q))-P*Ar[i][j]-(P*P if i==j else 0) for j in range(q)]for i in range(q)]
Ri=[[P*Ui[i][j]-sum(Ar[i][k]*Ui[k][j]+Ai[i][k]*Ur[k][j] for k in range(q))-P*Ai[i][j] for j in range(q)]for i in range(q)]
delta=Fraction(sum(abs(v) for R in [Rr,Ri] for row in R for v in row),P*P)
assert delta<1
# For each one-site erasure, reduce rank-one projectors on its complement.
# Numerators are exact complex integers; all reduced matrices denominator P^2.
Gs=[[0]*q for _ in range(q)]
for bit in range(3):
 idx=[[v for v in range(q) if (v>>bit)&1==s] for s in range(2)]
 rr=[];ri=[]
 for j in range(q):
  R=[[sum(Ur[idx[s][a]][j]*Ur[idx[s][b]][j]+Ui[idx[s][a]][j]*Ui[idx[s][b]][j] for s in range(2)) for b in range(4)]for a in range(4)]
  I=[[sum(Ui[idx[s][a]][j]*Ur[idx[s][b]][j]-Ur[idx[s][a]][j]*Ui[idx[s][b]][j] for s in range(2)) for b in range(4)]for a in range(4)]
  rr.append(R);ri.append(I)
 for j in range(q):
  for k in range(q):Gs[j][k]+=sum(rr[j][a][b]*rr[k][b][a]-ri[j][a][b]*ri[k][b][a] for a in range(4) for b in range(4))
# Ghat=Gs/(2 P^4). A normalized rational PSD test matrix Z=YY^T/tr(YY^T).
Zn=[[sum(Y[i][k]*Y[j][k] for k in range(4)) for j in range(q)]for i in range(q)]
tr=sum(Zn[i][i] for i in range(q));assert tr>0
# Exactly enumerate every distinct relabelled 3-cube, 840=8!/48.
edges=[(i,i^(1<<b)) for i in range(q) for b in range(3) if i<(i^(1<<b))]
graphs=set();maxs=None;maxperm=None
for perm in itertools.permutations(range(q)):
 edge=tuple(sorted(tuple(sorted((perm[i],perm[j]))) for i,j in edges))
 if edge in graphs:continue
 graphs.add(edge);s=sum(Zn[i][j] for i,j in edge)
 if maxs is None or s>maxs:maxs=s;maxperm=perm
assert len(graphs)==840
actual=Fraction(sum(Zn[i][j]*Gs[i][j] for i in range(q) for j in range(q)),2*P**4*tr)
support=Fraction(3*tr+2*maxs,2*tr)
gap=actual-support;lower=gap-45*delta
assert lower>Fraction(1,500)
result={'status':'EXACT_INTEGER_PASS','dimension':8,'D':2,'r':3,'N':1,'unique_reference_graphs':840,'enumerated_permutations':40320,'basis':'U=(I-A)^(-1)(I+A), A exact rational skew-Hermitian','dual':'Z=YY^T/tr(YY^T), exact rational PSD trace one','gap_hat':{'numerator':str(gap.numerator),'denominator':str(gap.denominator),'decimal_diagnostic':float(gap)},'residual_l1_bound':{'numerator':str(delta.numerator),'denominator':str(delta.denominator),'decimal_diagnostic':float(delta)},'rigorous_gap_lower':{'numerator':str(lower.numerator),'denominator':str(lower.denominator),'decimal_diagnostic':float(lower)},'certified_claim':'kappa > (ln 2)/500 is necessary for the total common-DS-congruence cone on this actual basis','max_reference_permutation':list(maxperm),'wall_seconds':time.perf_counter()-st,'cpu_seconds':time.process_time()-cpu,'maxrss_raw':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'python':sys.version,'inputs_sha256':hashlib.sha256((BASE/'EXACT_INPUTS.json').read_bytes()).hexdigest()}
(BASE/'EXACT_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
