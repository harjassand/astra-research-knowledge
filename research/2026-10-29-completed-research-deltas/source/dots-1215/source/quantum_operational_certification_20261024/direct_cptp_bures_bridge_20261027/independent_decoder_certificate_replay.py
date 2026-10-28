"""Independent exact LDL replay; does not call the author's SDP solver/verifier."""
from pathlib import Path
import hashlib,json
import sympy as s
P=Path(__file__).parent
raw=(P/'finite_decoder_sdp_certificates.json').read_bytes()
obj=json.loads(raw)
def decode(xs):return s.Matrix([[s.Rational(z[0])+s.I*s.Rational(z[1]) for z in row] for row in xs])
def pd_ldl(A):
 assert A==A.conjugate().T
 n=A.rows;L=s.eye(n);d=[]
 for i in range(n):
  p=s.simplify(A[i,i]-sum(L[i,j]*s.conjugate(L[i,j])*d[j] for j in range(i)))
  assert p.is_real and p.is_positive
  d.append(p)
  for k in range(i+1,n):
   L[k,i]=s.simplify((A[k,i]-sum(L[k,j]*s.conjugate(L[i,j])*d[j] for j in range(i)))/p)
 assert s.simplify(L*s.diag(*d)*L.conjugate().T-A)==s.zeros(n)
 return {'count':n,'minimum_pivot':str(min(d))}
rows=[]
for rec in obj['certificates']:
 k=rec['k'];H=decode(rec['H']);C=decode(rec['C']);Y=decode(rec['Y'])
 for i in range(k):
  for j in range(k): assert C[2*i,2*j]+C[2*i+1,2*j+1]==int(i==j)
 slack=H-s.kronecker_product(Y,s.eye(2))
 tests=[pd_ldl(z) for z in [H,C,slack]]
 gap=s.simplify(s.trace(H*C)-s.trace(Y))
 assert 0<gap<s.Rational(1,10**6)
 assert gap==s.Rational(rec['exact_gap'])
 rows.append({'name':rec['name'],'k':k,'exact_tp':True,'exact_positive_LDL_for_H_C_and_dual_slack':tests,'exact_gap':str(gap),'gap_float':float(gap)})
result={'status':'PASS','certificate_sha256':hashlib.sha256(raw).hexdigest(),'checks':rows,'scope':'Independent exact LDL reconstruction, TP and primal/dual gap checks on the stated rounded SDP coefficient matrices only.'}
(P/'independent_decoder_certificate_replay.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'certificate_sha256':result['certificate_sha256'],'gaps':[r['gap_float'] for r in rows]},indent=2))
