"""Independent exact reconstruction from the four-state rate definition.

No worker implementation is imported. This is an abstract CTMC counterfamily,
not physical measurements or a conclusion about the scope of a published proof.
"""
import json
from pathlib import Path
import sympy as s

e=s.symbols('e',positive=True)
a=2+e/3;b=1+e/3;h=1-e
Q=s.zeros(4)
for i in range(1,4):
    Q[0,i]=e/3
    Q[i,0]=h
    Q[i,1+(i%3)]=a
    Q[i,1+((i-2)%3)]=b
for i in range(4):Q[i,i]=-sum(Q[i,j] for j in range(4) if j!=i)
pi=s.Matrix([[h,e/3,e/3,e/3]])
assert s.simplify(pi*Q)==s.zeros(1,4)
X=s.Matrix(4,3,lambda i,j:s.Integer(i==j+1)-e/3)
A=s.Matrix([[-4,1,2],[2,-4,1],[1,2,-4]])
assert s.simplify(Q*X-X*A.T)==s.zeros(4,3)
Sigma=s.simplify(X.T*s.diag(*pi)*X)
assert s.simplify(Sigma-(e/3*s.eye(3)-e**2/9*s.ones(3)))==s.zeros(3)
assert s.simplify(A*Sigma-Sigma*A)==s.zeros(3)
assert s.simplify(pi*X)==s.zeros(1,3)
for i in range(1,4):assert s.simplify(pi[0]*Q[0,i]-pi[i]*Q[i,0])==0
ring_current=s.simplify(3*(e/3)*(a-b))
assert ring_current==e
D=-(A+A.T)/2;K=(A-A.T)/2
ou_rate=s.trace(K.T*D.inv()*K)
assert ou_rate==s.Rational(3,11)
norm_sq=[s.factor((X[i,:]*Sigma.inv()*X[i,:].T)[0]) for i in range(4)]
fourth=s.factor(sum(pi[i]*norm_sq[i]**2 for i in range(4)))
assert s.simplify(fourth-(9/e-6+e/(1-e)))==0

# Same positive-frequency covariance for the matched Gaussian OU.
R=(A+s.I*s.eye(3)).inv()
S=s.simplify(R*(2*D)*s.conjugate(R.T))
assert S[0,0]==S[1,1]==S[2,2]
C=s.simplify(S/S[0,0])
closure=s.simplify(C[0,1]*C[1,2]*C[2,0])
imag=s.im(closure)
assert imag!=0
result=dict(scope='Exact independent CTMC/rate/covariance identities. No experimental claim, historical-priority finding or published-SI conclusion.',
    parameter_scope='0<e<1',
    stationary_distribution=[str(z) for z in pi],
    centered_indicator_drift_constant=True,
    A=[[int(z) for z in A.row(i)] for i in range(3)],
    covariance_matrix=str(Sigma),
    drift_commutes_with_covariance=True,
    true_path_KL_rate='e*log((2+e/3)/(1+e/3))',
    matched_Gaussian_path_KL_rate_exact=str(ou_rate),
    whitened_fourth_moment=str(fourth),
    squared_whitened_norm_by_state=[str(z) for z in norm_sq],
    omega_1_normalized_closure_imaginary_exact=str(imag),
    omega_1_normalized_closure_imaginary_float=float(imag),
    universal_covariance_only_positive_rate_floor_for_this_fixed_whitened_covariance=False)
Path(__file__).with_name('results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
