import sympy as s
r,lam,L,k,h,l=s.symbols('r lam L k h l', real=True)
M11=s.Matrix([[12,0,0,3*L],[0,4*r,-L,0],[0,-L,4,0],[3*L,0,0,2*lam]])
M12=s.Matrix([[0,4*r,-L,0],[4*r,0,0,L],[-L,0,0,2*r-lam],[0,L,2*r-lam,0]])
M22=s.Matrix([[4*r,0,0,L],[0,12,-3*L,0],[0,-3*L,2*lam,0],[L,0,L*0,4]])
K=s.Matrix([[0,k,h,0],[-k,0,0,h],[-h,0,0,l],[0,-h,-l,0]])
Q=M11.row_join(M12+K).col_join((M12-K).row_join(M22))
# sx a,b,c,d ; tx a,b,c,d.
B=s.Matrix([[1,0,0,0,0,1,0,0], # pparallel
[0,0,0,-1,0,0,1,0], # zperp=ct-ds
[0,-1,0,0,1,0,0,0],# pperp
[0,0,1,0,0,0,0,1],# zparallel
[1,0,0,0,0,-1,0,0],# ptilde1
[0,0,0,1,0,0,1,0],# ztilde2
[0,1,0,0,1,0,0,0],# ptilde2
[0,0,1,0,0,0,0,-1]])# ztilde1
T=s.simplify(B*Q*B.T/4)
for i in range(4): print('block',i,T[2*i:2*i+2,2*i:2*i+2])
print('offdiag',s.simplify(T-s.diag(*[T[2*i:2*i+2,2*i:2*i+2] for i in range(4)])))
