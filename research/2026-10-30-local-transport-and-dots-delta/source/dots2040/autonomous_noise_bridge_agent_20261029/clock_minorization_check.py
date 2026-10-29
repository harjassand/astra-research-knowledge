import numpy as np
from itertools import combinations
for N in range(1,8):
    sets=[s for r in range(N+1) for s in combinations(range(N),r) if all(i+1 not in s for i in s)]
    ds=len(sets);I=np.eye(ds);b=[]
    for x in range(N):
        bx=np.zeros((ds,ds))
        for j,s in enumerate(sets):
            if x in s:bx[sets.index(tuple(y for y in s if y!=x)),j]=1
        b.append(bx)
    n=[a.T@a for a in b];H=sum(a+a.T for a in b)
    def dual(O):return 1j*(H@O-O@H)+sum(a.T@O@a-(a.T@a@O+O@a.T@a)/2 for a in b)
    for x in range(N):
        neighbors=[y for y in range(N) if abs(x-y)==1]
        A=np.eye(ds)
        for y in neighbors:A=A@(I-n[y])
        rhs=-b[x]/2-1j*(A-2*n[x])+1j*sum((b[y].T@b[x] for y in neighbors),np.zeros((ds,ds)))
        assert np.linalg.norm(dual(b[x])-rhs)<1e-12
        assert np.linalg.norm(dual(n[x])-(-n[x]+1j*(b[x]-b[x].T)))<1e-12
print('Exact operator equations verified on path graphs N=1,...,7.')
