"""Generate exact native benchmark inputs; does not run any solver."""
from fractions import Fraction as F
from pathlib import Path
import json

def add(A, B):
    return [[A[i][j]+B[i][j] for j in range(3)] for i in range(3)]
def scale(a, A):
    return [[a*x for x in row] for row in A]
def diag(a,b,c):
    return [[F(a),F(0),F(0)],[F(0),F(b),F(0)],[F(0),F(0),F(c)]]
D2=diag(1,0,-1)
D1=diag(0,F(1,3),F(-1,3))
D0=[[F(-1),F(1),F(1,3)],[F(1),F(0),F(2)],[F(1,3),F(2),F(1)]]
rows={}
def row(B,f,s,label):
    key=(B,f,s)
    if key in rows:
        rows[key]['sweeps'].append(label)
        return
    eta=F(1,2**B)
    exponent=3*B+f
    omega=F(2**exponent) if exponent>=0 else F(1,2**(-exponent))
    coeff=[add(add(scale(F(1,4),D2),scale(-eta/2,D1)),scale(eta*eta,D0)),
           add(scale(F(-1),D2),scale(eta,D1)),D2]
    rows[key]={
      'id':f'B{B}_f{f}_s{s}', 'B':B, 'frequency_offset':f,
      'precision_bits':s, 'eta':str(eta), 'omega':str(omega),
      'operator_tolerance':str(F(1,2**s)), 'sweeps':[label],
      'coefficients_ascending_t':[[[str(x) for x in r] for r in A] for A in coeff],
      'interval':['0','1'], 'initial_matrix':'I_3',
      'phase_alignment_allowed':False,
      'status':'not_run'}
row(2,0,12,'prerequisite')
for f in (-2,0,2,4): row(3,f,20,'frequency')
for s in (12,20,28,36): row(3,0,s,'precision')
for B in (2,4,8,16): row(B,0,20,'coalescence')
result={'specification':'BENCHMARK_SPEC_v1.md','solver_row_wall_limit_seconds':30,
 'total_native_solver_limit_seconds':180,'solver_status':'not_implemented',
 'rows':list(rows.values())}
out=Path(__file__).with_name('benchmark_manifest.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(f'Wrote {len(rows)} exact-input rows; no solver executed.')
