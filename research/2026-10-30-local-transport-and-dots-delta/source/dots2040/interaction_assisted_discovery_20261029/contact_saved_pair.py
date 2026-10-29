import sympy as s, json
from finite_boundary_tests import q_r, first_diff
from scipy.linalg import expm
import numpy as np

def contact(Q,kappa=1):
 n=Q.rows;C=s.Matrix(s.kronecker_product(Q,s.eye(n))+s.kronecker_product(s.eye(n),Q))
 C=C.row_join(s.zeros(n*n,1)).col_join(s.zeros(1,n*n+1))
 for i in range(n):j=i*n+i;C[j,j]-=kappa;C[j,n*n]=kappa
 return C
C0=contact(q_r(0));C1=contact(q_r(s.Rational(1,10)))
a=s.zeros(1,17);a[0,0]=1;b=s.Matrix([int(i==0)+int(j==0) for i in range(4) for j in range(4)]+[0])
out={'first_boundary_mean_count_difference':first_diff(C1,C0,a,b),'observations':[]}
for t in [.1,.5,1,2,4]:
 p0=float((np.array(a,float)@expm(t*np.array(C0,float))@np.array(b,float))[0,0]);p1=float((np.array(a,float)@expm(t*np.array(C1,float))@np.array(b,float))[0,0]);out['observations'].append({'t':t,'equilibrium':p0,'r_01':p1,'difference':p1-p0})
print(json.dumps(out,indent=2))
