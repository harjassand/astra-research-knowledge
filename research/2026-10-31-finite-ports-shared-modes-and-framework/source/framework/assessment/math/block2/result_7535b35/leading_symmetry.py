"""Reduce all closed acoustically admissible corrections by residual symmetry."""
exec((__import__('pathlib').Path(__file__).parent/'leading_null.py').read_text().split("print('Acoustic coefficient")[0])
solution=s.sympify((BASE/'leading_solution.txt').read_text(),locals={str(z):z for z in ww})
Osol=O.subs(dict(zip(ww,solution)),simultaneous=True)
Esol=E.subs(dict(zip(ww,solution)),simultaneous=True)
x1,x2,y1,y2,P1,P2,Q1,Q2,R1,R2=s.symbols('x1 x2 y1 y2 P1 P2 Q1 Q2 R1 R2',real=True)
V=[x1,x2,y1,y2,P1,P2,Q1,Q2,R1,R2]
sub={a:(x1+y1)/2,b:(y2-x2)/2,c:(x2+y2)/2,d:(x1-y1)/2,h[0]:P1+2*Q1+R1,h[1]:-P2+R2,h[2]:-P1+2*Q1-R1,h[3]:P2+2*Q2+R2,h[4]:P1-R1,h[5]:-P2+2*Q2-R2}
Ecx=s.expand(Esol.subs(sub,simultaneous=True))
rot=0
for re,im,weight in [(x1,x2,-4),(y1,y2,-2),(P1,P2,-5),(Q1,Q2,-3),(R1,R2,-1)]:
 rot+=weight*(-im*s.diff(Ecx,re)+re*s.diff(Ecx,im))
ref=Ecx-Ecx.subs({x2:-x2,y2:-y2,P2:-P2,Q2:-Q2,R2:-R2},simultaneous=True)
params=[ww[i] for i in [49,55,56,57,58,59]]
eqs=s.Poly(s.expand(rot),*V).coeffs()+s.Poly(s.expand(ref),*V).coeffs()
sol=s.linsolve(eqs,params);print('Residual family:',sol,flush=True)
ss=list(sol)[0];Ered=s.factor(Ecx.subs(dict(zip(params,ss)),simultaneous=True))
Ored=s.simplify(Osol.subs(dict(zip(params,ss)),simultaneous=True))
print('Residual parameters:',set().union(*(z.free_symbols for z in ss)),flush=True)
print('Ored:',Ored,flush=True)
print('Ered:',Ered,flush=True)
(BASE/'residual_solution.txt').write_text(str(ss)+'\n')
