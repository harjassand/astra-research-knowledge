"""Find positivity restrictions on the complete symmetry reduced leading family."""
exec((__import__('pathlib').Path(__file__).parent/'leading_symmetry.py').read_text().split("sol=s.linsolve")[0])
ss=s.sympify((BASE/'residual_solution.txt').read_text(),locals={str(z):z for z in ww})
Ered=s.expand(Ecx.subs(dict(zip(params,ss)),simultaneous=True))
q,z=s.symbols('q z',real=True)
Ediag=s.factor(Ered.subs({x1:q,x2:0,y1:z,y2:0}))
plus=[P1,Q1,R1];minus=[P2,Q2,R2]
Hp=s.simplify(s.hessian(Ediag,plus)/2);Hm=s.simplify(s.hessian(Ediag,minus)/2)
print('Real block:',Hp,flush=True);print('Imag block:',Hm,flush=True)
print('Real determinant:',s.factor(Hp.det()),flush=True);print('Imag determinant:',s.factor(Hm.det()),flush=True)
print('At x=0:',s.factor(Hp.subs(q,0)),s.factor(Hm.subs(q,0)),flush=True)
print('At y=0:',s.factor(Hp.subs(z,0)),s.factor(Hm.subs(z,0)),flush=True)
theta=s.Matrix([-c,-d,a,b]);zeta=s.Matrix([-b,a,-d,c]);alpha=(3*T+14*D)*theta+(9*T-6*D)*zeta
OP=s.Matrix(4,4,lambda i,j:s.diff(alpha[j],A[i])-s.diff(alpha[i],A[j]))
print('Primary params:',s.Poly(OP[2,3],*A).coeff_monomial(b*c),s.Poly(OP[2,3],*A).coeff_monomial(d*d),flush=True)
