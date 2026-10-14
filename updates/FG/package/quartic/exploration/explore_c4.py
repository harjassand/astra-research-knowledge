import sympy as s
r,lam,L,x,y=s.symbols('r lam L x y', real=True)
M11=s.Matrix([[12,0,0,3*L],[0,4*r,-L,0],[0,-L,4,0],[3*L,0,0,2*lam]])
M12=s.Matrix([[0,4*r,-L,0],[4*r,0,0,L],[-L,0,0,2*r-lam],[0,L,2*r-lam,0]])
M22=s.Matrix([[4*r,0,0,L],[0,12,-3*L,0],[0,-3*L,2*lam,0],[L,0,0,4]])
M=x*x*M11+2*x*y*M12+y*y*M22
print('det=',s.factor(M.det()))
for k in range(1,5):
 print('minor',k,s.factor(M[:k,:k].det()))
print('diagonal eigenblock=',M.subs({x:1,y:1}))
