exec((__import__('pathlib').Path(__file__).parent/'leading_psd.py').read_text().split("q,z=s.symbols")[0])
rho=s.symbols('rho',real=True)
Ored=s.simplify(Osol.subs(dict(zip(params,ss)),simultaneous=True).subs({ww[55]:24-12*rho,ww[59]:36-18*rho}))
theta=s.Matrix([-c,-d,a,b]);zeta=s.Matrix([-b,a,-d,c]);u=s.symbols('u:4',real=True)
alpha=(u[0]*T+u[1]*D)*theta+(u[2]*T+u[3]*D)*zeta
OM=s.Matrix(4,4,lambda i,j:s.diff(alpha[j],A[i])-s.diff(alpha[i],A[j]))
eq=[]
for i,j in combinations(range(4),2):eq.extend(s.Poly(s.expand(Ored[i,j]-OM[i,j]),*A).coeffs())
print('PRIMITIVE',s.linsolve(eq,u),flush=True)
