from pathlib import Path
HERE=Path(__file__).resolve().parent
exec((HERE / 'cascade_scalar_limit.py').read_text().split('B=[np.eye')[0])
from itertools import combinations
for n in [2,3,4,5]:
 d=2**n;W=[np.eye(2*d,dtype=complex)]+[np.zeros((2*d,2*d),complex) for _ in range(4)]
 for j in range(1,n+1):
  P=swap(n+1,0,j);V=[(1j**p)*np.linalg.matrix_power(P,p)/factorial(p) for p in range(5)]
  W=[sum(V[q]@W[p-q] for q in range(p+1)) for p in range(5)]
 O=W[4]-(W[1]@W[3]+W[2]@W[2]+W[3]@W[1])/2+(W[1]@W[1]@W[2]+W[1]@W[2]@W[1]+W[2]@W[1]@W[1])/3-np.linalg.matrix_power(W[1],4)/4
 H=(O[:d,:d]+O[d:,d:])/(2j)
 terms=[chir(n,*q) for q in combinations(range(n),3)]
 coef=[np.vdot(X,H).real/np.vdot(X,X).real for X in terms]
 res=H-sum((z*X for z,X in zip(coef,terms)),start=np.zeros_like(H))
 print('n',n,'coeff',coef,'resnorm',np.linalg.norm(res),'Hnorm',np.linalg.norm(H),flush=True)
