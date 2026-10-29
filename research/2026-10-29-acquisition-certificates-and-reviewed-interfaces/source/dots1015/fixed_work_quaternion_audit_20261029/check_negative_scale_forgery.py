import sys,json
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,'producer-workspace/fixed_work_quaternion_kernel_20261029')
import bounded_sos_oracle as b
import fixed_work_oracle as fw
raw={(4,0,0,0):F(1)};G=[[F(fw.qdiag[i] if i==j else 0) for j in range(10)] for i in range(10)]
# Locate the square monomial q0^2 independently from Gram grouping of q0^4.
group=fw.groups[(4,0,0,0)];assert len(group)==1;i,j,a=group[0];assert i==j and a==1;G[i][i]-=1
c={'quaternion':['1','0','0','0'],'scale':'-1','lambda_proposal':'-1','repair_shift':'0','rational_gram':[[str(v) for v in row] for row in G],'rational_basis':[[str(int(i==j)) for j in range(10)] for i in range(10)],'upper':'1','lower':'1','gap':'0'}
accepted=b.verify(raw,c);assert accepted
out={'verifier_accepts_forged_certificate':accepted,'true_minimum':0,'claimed_lower':1,'generated_solve_outputs_not_impugned':True,'certificate':c}
Path(__file__).with_name('negative_scale_forgery.json').write_text(json.dumps(out,indent=2)+'\n');print('UNSOUND verifier accepts lower1 for q0^4, actual minimum0')
