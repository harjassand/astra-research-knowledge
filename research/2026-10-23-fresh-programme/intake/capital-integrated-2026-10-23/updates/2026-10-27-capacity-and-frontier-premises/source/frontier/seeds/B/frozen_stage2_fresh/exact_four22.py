import sympy as s
from itertools import combinations,product
words=list(product(range(2),repeat=4))
weight2=[w for w in words if sum(w)==2]
def pairing(pairs):
    out=s.zeros(6,1)
    for j,w in enumerate(weight2):
        val=1
        for a,b in pairs:
            val*=int((w[a],w[b])==(0,1))-int((w[a],w[b])==(1,0))
        out[j]=val
    return out
W=s.Matrix.hstack(pairing([(0,1),(2,3)]),pairing([(0,2),(1,3)]))
G=W.T*W
reps=[]
for a,b in combinations(range(4),2):
    P=s.zeros(6)
    for j,w in enumerate(weight2):
        ww=list(w);ww[a],ww[b]=ww[b],ww[a]
        P[weight2.index(tuple(ww)),j]=1
    reps.append(G.inv()*W.T*P*W)
K=s.zeros(8);T=s.zeros(8)
for f in reps:
    K+=s.kronecker_product(*([f-s.eye(2)/2]*3))/6
    T+=s.kronecker_product(*([f]*3))/6
V=s.Matrix.hstack(*((K+s.Rational(9,8)*s.eye(8)).col_join(T)).nullspace())
print('words',weight2,'W',W.tolist(),'G',G.tolist(),'reps',[f.tolist() for f in reps], 'V',V.tolist())
