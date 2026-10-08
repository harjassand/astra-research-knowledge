#!/usr/bin/env python3
"""Exact rational counterexample to replacing the complex centered Gram."""
from fractions import Fraction as F
from pathlib import Path
import json

t=F(1,2)
epsilon=F(-1,4)
tau=[F(3,4),F(1,4)]
sigma=[a*b for a in tau for b in tau]
rho=[[F(0) for _ in range(4)] for _ in range(4)]
for i in range(4):
    rho[i][i]=sigma[i]
    rho[i][3-i]=epsilon/4
assert sum(rho[i][i] for i in range(4))==1
for a,b in ((0,3),(1,2)):
    assert rho[a][a]>0 and rho[b][b]>0
    assert rho[a][a]*rho[b][b]-rho[a][b]*rho[b][a]==F(1,32)>0
swap=[0,2,1,3]
assert all(rho[i][j]==rho[swap[i]][swap[j]] for i in range(4) for j in range(4))
marginal=[[sum(rho[2*i+k][2*j+k] for k in range(2)) for j in range(2)]
          for i in range(2)]
assert marginal==[[F(3,4),F(0)],[F(0),F(1,4)]]
singlet=(rho[1][1]+rho[2][2]-rho[1][2]-rho[2][1])/2
assert singlet==F(1,4)
delta=[[rho[i][j]-(sigma[i] if i==j else 0) for j in range(4)] for i in range(4)]
chi=sum(sum(delta[i][j]*delta[j][i] for j in range(4))/sigma[i] for i in range(4))
gram_value=epsilon**2/(1-t*t)**2
naive_value=epsilon**2
assert chi==gram_value==F(1,9)
assert naive_value==F(1,16) and chi-naive_value==F(7,144)
commutator=[[rho[i][j]*(sigma[j]-sigma[i]) for j in range(4)] for i in range(4)]
assert sum(x*x for row in commutator for x in row)==F(1,512)>0
record={
 'status':'exact rational assertions passed',
 'N':2,'r':2,'in_final_r_le_N_over_128_range':False,
 'permutation_invariant':True,'white_sector_weights':['1/4','3/4'],
 'reference_one_body_eigenvalues':['3/4','1/4'],
 'positive_block_determinants':['1/32','1/32'],
 'centered_d_xx':'-1/4','all_other_centered_degree2_coefficients':'0',
 'true_Petz_chi_square':str(chi),
 'complex_Gram_Parseval_value':str(gram_value),
 'invalid_real_Gram_value':str(naive_value),
 'exact_error_from_invalid_substitution':str(chi-naive_value),
 'commutator_HS_norm_squared':'1/512',
 'scope':'counterexample to invalid real-covariance substitution, not candidate theorem'
}
path=Path(__file__).with_name('exact_counterexamples.json')
path.write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
