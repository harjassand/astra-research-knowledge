import sympy as s
from itertools import combinations
pairs=list(combinations(range(4),2))
W=s.Matrix([[int(i==j)-int(i==3) for j in range(3)] for i in range(4)])
G=W.T*W
reps=[]
for a,b in pairs:
    P=s.eye(4);P.row_swap(a,b)
    reps.append(G.inv()*W.T*P*W)
K=s.zeros(27);T=s.zeros(27)
for f in reps:
    K+=s.kronecker_product(*([f-s.eye(3)/2]*3))/6
    T+=s.kronecker_product(*([f]*3))/6
V=s.Matrix.hstack(*((K+s.Rational(13,24)*s.eye(27)).col_join(T-s.eye(27)/3)).nullspace())
print('V shape',V.shape)
print('V=',V.tolist())
print('eigen identity',K*V==-s.Rational(13,24)*V)
for a,b in pairs:
    pass
