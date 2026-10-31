#!/usr/bin/env python3
"""Small CQ diagnostic only: NOT a certified diamond error or gate backend."""
import json, math
import numpy as np
from scipy.linalg import expm, eig
from fractions import Fraction

def trace_norm_hermitian(x):return float(np.abs(np.linalg.eigvalsh((x+x.conj().T)/2)).sum())
n=4; D=1<<n; q=21/20
weights=np.array([q**sum(((x>>i)&1)==((x>>(i+1))&1) for i in range(n-1)) for x in range(D)])
pi=weights/weights.sum(); Q=np.zeros((D,D))
for x in range(D):
 for i in range(n):
  y=x^(1<<i); rate=weights[y]/(weights[x]+weights[y]);Q[y,x]+=rate;Q[x,x]-=rate
z=np.array([1-2*(x&1) for x in range(D)],dtype=float)
w=np.linalg.solve(-Q.T+np.ones((D,1))*pi.reshape(1,D),z)
corr=float(pi@(z*w))
X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]).astype(complex);I=np.eye(2)
def comm(H):return np.kron(I,H)-np.kron(H.T,I)
rho=np.array([[1,0],[0,0]],complex);v0=np.kron(pi,rho.reshape(4,order='F'))
Leff=-1j*comm(X)-corr*(comm(Z)@comm(Z))
reff=(expm(Leff)@rho.reshape(4,order='F')).reshape((2,2),order='F')
rows=[]
threshold=math.ceil(Fraction(4096)*Fraction(20,19)**2*Fraction(39*n,19)**2)
for lam in [threshold,10**6,10**8]:
 A=np.kron(lam*Q,np.eye(4)).astype(complex)
 for x in range(D):A[4*x:4*x+4,4*x:4*x+4]+=-1j*comm(X+math.sqrt(lam)*z[x]*Z)
 E=expm(A);v=E@v0
 val,V=eig(A);v_eig=V@(np.exp(val)*np.linalg.solve(V,v0))
 blocks=[v[4*x:4*x+4].reshape((2,2),order='F') for x in range(D)]
 red=sum(blocks)
 rows.append(dict(lambda_value=lam,global_generator_matrix_dimension=4*D,
  expm_eig_output_vector_disagreement=float(np.linalg.norm(v-v_eig)),eigenvector_condition=float(np.linalg.cond(V)),
  trace_defect=float(abs(np.trace(red)-1)),min_block_eigenvalue=float(min(np.linalg.eigvalsh((a+a.conj().T)/2).min() for a in blocks)),
  finite_vs_white_system_trace_norm=trace_norm_hermitian(red-reff),
  finite_vs_white_retained_CQ_trace_norm=sum(trace_norm_hermitian(blocks[x]-pi[x]*reff) for x in range(D)),
  source_marginal_l1=float(sum(abs(np.trace(blocks[x])-pi[x]) for x in range(D))),
  scopes='One stationary-CQ input, H0=X, K=Zsys Zsource0, T=1; white reduced generator inferred from Poisson equation; numerical diagnostic, no uniform error theorem.'))
out=dict(n=n,edge_ratio='21/20',initial_system='|0><0|',source='exact stationary pi',integrated_unit_rate_correlation=corr,
         arithmetic='SciPy double expm plus independent eig reconstruction; disagreement not certified error',rows=rows)
open('native_resource_audit_20261031/small_cq_dense_check.json','w').write(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
