"""Exact-moment polynomial subspace tests for the normalized chord form."""
from fractions import Fraction as F
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eigvalsh

out=[]
for n in [2,3,4,5,10,20,50,100,1000]:
    C=[[F(1,n+2),F(1,n+4)],[F(1,n+4),F(1,n+6)]]
    A=[[F(1,n),F(5*n+4,5*n*(n+2))],[F(5*n+4,5*n*(n+2)),F(35*n*n+154*n+36,35*n*(n+2)*(n+4))]]
    scaled=np.array([[float(z*F(n,n+2)) for z in row] for row in A])
    eig=eigvalsh(scaled,np.array(C,dtype=float))
    out.append({'dimension':n,'normalized_subspace_eigenvalues':eig.tolist()})
# Disk f=x_1(1-r^2/2):
v=[F(1),F(-1,2)]
C=[[F(1,4),F(1,6)],[F(1,6),F(1,8)]]
A=[[F(1,2),F(7,20)],[F(7,20),F(121,420)]]
var=sum(v[i]*C[i][j]*v[j] for i in range(2) for j in range(2))
q=sum(v[i]*A[i][j]*v[j] for i in range(2) for j in range(2))
assert var==F(11,96) and q==F(373,1680) and q/(2*var)==F(373,385)
result={'ball_polynomial_subspace':out,'explicit_disk_test':{'variance':str(var),'Q':str(q),'normalized_ratio':str(q/(2*var))}}
print(json.dumps(result,indent=2))
Path(__file__).with_name('ball_exact_results.json').write_text(json.dumps(result,indent=2)+'\n')
