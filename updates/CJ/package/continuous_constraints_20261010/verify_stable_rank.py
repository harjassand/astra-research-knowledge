"""Exact integer/rational checks of the stable-rank family; no Monte Carlo proof."""
import json
from pathlib import Path
from fractions import Fraction as Q
import numpy as np
from math import prod
N=64; m=4
I=np.eye(N,dtype=np.int64)
X1=np.zeros((N,N),dtype=np.int64); X2=X1.copy(); Z1=I.copy()
for j in range(N):
    X1[j^1,j]=1
    X2[j^2,j]=1
    Z1[j,j]=1 if (j&1)==0 else -1
A=[I,X1,Z1,X2]
H=[[int(np.trace(a@b.T)) for b in A] for a in A]
assert H==[[N*int(i==j) for j in range(m)] for i in range(m)]
assert all(np.array_equal(a@a.T,I) for a in A)
assert np.array_equal(sum(a@a.T for a in A),m*I)
assert np.array_equal(sum(a.T@a for a in A),m*I)
assert not np.array_equal(X1@Z1,Z1@X1)
# Exact rank of I+X1: identical pairs of rows, disjoint pair supports.
assert np.array_equal((I+X1)@(I+X1),2*(I+X1))
rank_singular=int(np.trace(I+X1)//2)
assert rank_singular==32
r=N//m
alpha=prod((Q(1)-Q(2*j,r)) for j in range(1,m//2+1))
K2=prod(Q(1)/(Q(1)-Q(2*j,r)) for j in range(1,m+1))
assert alpha==Q(21,32)
# Determinants from exact eigenvalues at two norm-one lambda vectors.
det_axis=Q(2)**N
det_angle=((1+Q(7,5)**2)*(1+Q(1,5)**2))**(N//2)
assert det_angle==Q(1924,625)**32 and det_angle!=det_axis
# Squared acceptance rationality checked at one rational vector.
s=Q(N)
ratio_axis=(1+s/r)**r/det_axis
ratio_angle=(1+s/r)**r/det_angle
assert 0<ratio_axis<=1 and 0<ratio_angle<=1
results={
 'all_integer_rational_assertions_passed':True,
 'N':N,'m':m,'raw_Gram_H':H,
 'matrix_descriptions':['I','X on bit 0','Z on bit 0','X on bit 1'],
 'native_Mp_and_Mn':'(1/16) I_64',
 'certified_r':r,
 'noncommuting_pair':['X on bit 0','Z on bit 0'],
 'rank_at_lambda_1_1_0_0':rank_singular,
 'det_at_lambda_1_0_0_0':'2^64',
 'det_at_lambda_3over5_4over5_0_0':'(1924/625)^32',
 'success_lower_bound':str(alpha),
 'L2_squared_bound':str(K2),
 'squared_acceptance_axis':str(ratio_axis),
 'squared_acceptance_angle':str(ratio_angle),
 'growing_even_m_family':[
   {'m':d,'N':n,'r':n//d,'success_lower_bound':str(prod(Q(1)-Q(2*j,n//d) for j in range(1,d//2+1)))}
   for d,n in [(4,512),(8,4096),(16,32768)]
 ]
}
p=Path(__file__).with_name('STABLE_RANK_EXACT_CHECKS.json')
p.write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
