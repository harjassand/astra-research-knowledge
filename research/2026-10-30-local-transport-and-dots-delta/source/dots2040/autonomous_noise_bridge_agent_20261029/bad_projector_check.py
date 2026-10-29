# Reuse the nonunitary x-y-z physical model from hardcore_test.py.
exec(open('autonomous_noise_bridge_20261029/hardcore_test.py').read())
from itertools import combinations
Id=np.eye(dim);B=[];Ls=[]
for x in range(3):
    Q=kron([np.eye(4)]+[(I3-P0) if j==x else I3 for j in range(3)])
    G=kron([np.eye(4)]+[P0 if j in neigh[x] else I3 for j in range(3)])
    B.append(Q-V[x]@V[x].conj().T@G)
    for s in [1,2]:
        aa=np.zeros((3,3));aa[0,s]=1
        Ls.append(kron([np.eye(4)]+[aa if j==x else I3 for j in range(3)]))
def dual(O):
    return 1j*(H@O-O@H)+sum(L.conj().T@O@L-(L.conj().T@L@O+O@L.conj().T@L)/2 for L in Ls)
for x in range(3):
    assert np.linalg.norm(B[x]@B[x]-B[x])<1e-12
    assert np.linalg.norm(H@B[x]-B[x]@H)<1e-12
    for y in range(3):assert np.linalg.norm(B[x]@B[y]-B[y]@B[x])<1e-12
bounds=[]
for r in [1,2,3]:
 for S in combinations(range(3),r):
    P=np.eye(dim)
    for x in S:P=P@B[x]
    A=dual(P)+r*P
    lam=np.linalg.eigvalsh((A+A.conj().T)/2).max()
    assert lam<1e-12
    bounds.append((S,float(lam)))
print('All B projector / commutator checks pass.')
print('Largest eigenvalue of L*(product B)+|S| product B:',bounds)
