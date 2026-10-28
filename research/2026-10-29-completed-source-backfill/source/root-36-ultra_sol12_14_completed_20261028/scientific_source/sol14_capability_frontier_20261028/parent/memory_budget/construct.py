"""Exact genuinely noncommuting Bell weights and information-budget receiver.

Reuses the accepted sol12 scalar entropy arithmetic, explicitly charged.
This is a construction, not an independent replay of that prior theorem.
"""
from fractions import Fraction as F
from pathlib import Path
import importlib.util, json, sys, time
sys.set_int_max_str_digits(0)
START=time.perf_counter()
HERE=Path(__file__).resolve().parent
PRIOR=HERE.parents[2]/'sol12_structural_capability_20261028'/'quantum_independent'
sys.path.insert(0,str(PRIOR))
import frame as f
import arith as a
import compile_all_nine as prior
weights=[1000,1,2,3,4,5,6,7,8];T=F(sum(weights))
I=[[F(1),F(0)],[F(0),F(1)]]
PX=[[F(1,2),F(1,2)],[F(1,2),F(1,2)]]
MX=[[F(1,2),F(-1,2)],[F(-1,2),F(1,2)]]
PZ=[[F(1),F(0)],[F(0),F(0)]]
MZ=[[F(0),F(0)],[F(0),F(1)]]
states=[[[v/2 for v in row]for row in I],PX,MX,PZ,MZ,MZ,PZ,MX,PX]
A=[[[weights[k]*v for v in row]for row in states[k]]for k in range(9)]
C=[[sum(m[i][j]for m in A)for j in range(2)]for i in range(2)]
assert C==[[F(518),F(0)],[F(0),F(518)]]
def add_tensor(dest,left,right):
 for i in range(len(left)):
  for j in range(len(left)):
   for u in range(len(right)):
    for v in range(len(right)):
     dest[len(right)*i+u][len(right)*j+v]=f.add(dest[len(right)*i+u][len(right)*j+v],f.scale(left[i][j],right[u][v]))
X=f.zeros(18);M=f.zeros(6)
for bell,sic,aa in zip(f.BELLS,f.SICS,A):
 add_tensor(X,bell,aa);add_tensor(M,sic,aa)
assert f.trace(X)==f.z(T)and f.trace(M)==f.z(T)
assert all(X[j][i]==f.conj(X[i][j])for i in range(18)for j in range(18))
# Original physical qutrit is the first factor, reference is B3 x L2.
pt=[[X[6*(j//6)+i%6][6*(i//6)+j%6]for j in range(18)]for i in range(18)]
ref=[[f.total(X[6*k+i][6*k+j]for k in range(3))for j in range(6)]for i in range(6)]
assert all(ref[i][j]==f.z(T/6 if i==j else 0)for i in range(6)for j in range(6))
NX=[[f.scale(f.sub(f.z(T/6 if i//6==j//6 and i%6==j%6 else 0),pt[i][j]),F(1,2))for j in range(18)]for i in range(18)]
perm=[]
for u in range(3):
 for d in range(3):
  for l in range(2):perm.append(2*(3*((u+d)%3)+(u+2*d)%3)+l)
assert all(NX[perm[i]][perm[j]]==(f.scale(M[i%6][j%6],F(1,3))if i//6==j//6 else f.z())for i in range(18)for j in range(18))
off=[row[6:12]for row in X[:6]]
assert any(z!=f.z()for row in f.mm(off,off)for z in row)
scalar,p,gap=prior.entropy_source(weights)
chi=a.scale(a.LOG2,F(36,1036));budget=a.sub(gap,chi)
assert budget[0]>F(33,1000)
# Ai span I,X,Z, whereas one fixed-basis common bath spans at most two.
comm=f.mm([[f.z(v)for v in row]for row in A[1]],[[f.z(v)for v in row]for row in A[3]])
back=f.mm([[f.z(v)for v in row]for row in A[3]],[[f.z(v)for v in row]for row in A[1]])
assert comm!=back
def serialmatrix(mat):return [[[str(z[0]),str(z[1])]for z in row]for row in mat]
out={'status':'EXACT_NONCOMMUTING_MATRIX_WEIGHT_ADMISSION','weights':weights,
 'scalar_defect':a.record(gap),'memory_Holevo_information':a.record(chi),
 'CMI_excess_lower_expression':a.record(budget),
 'scope_of_upper_endpoint':'It bounds the budget expression, not the actual source CMI.',
 'source_trace':str(T),'density_normalization':'1/1036','TP_Choi_normalization':'6/1036',
 'reference_dimension':6,'extension_dimension':54,'source_rank':10,
 'exact_Bell_to_SIC_identity':True,'reference_marginal':'I6/6 after normalization',
 'memory_marginal':'I2/2 after normalization','matrix_weight_span_dimension':3,
 'noncommuting_weights':True,'condition_number_24_premise':False,
 'reduction_premise':False,'Schmidt_number_at_most_2_premise':False,
 'fixed_physical_offblock_square_zero_premise':False,
 'proof_inputs':'Accepted scalar cubic entropy certificate; entropy chain rule and mutual-information data processing.',
 'whole_white_curve':'NOT_YET_ACQUIRED','arbitrary_matrix_weight_theorem':False,
 'seconds_including_upstream_imports':time.perf_counter()-START}
(HERE/'SOURCE.json').write_text(json.dumps({'field':'Q[sqrt(-3)]','Ai_unnormalized':[[[str(v)for v in row]for row in aa]for aa in A], 'X':serialmatrix(X),'M':serialmatrix(M)},indent=2)+'\n')
(HERE/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'CMI_excess_budget_display':out['CMI_excess_lower_expression']['display_only'],'seconds':out['seconds_including_upstream_imports']},indent=2))
