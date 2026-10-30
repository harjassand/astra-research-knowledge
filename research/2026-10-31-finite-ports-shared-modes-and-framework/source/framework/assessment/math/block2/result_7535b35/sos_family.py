"""A complete acoustic-null bilinear SOS ansatz; solve its coefficient map."""
exec((__import__('pathlib').Path(__file__).parent/'invariants.py').read_text().split('k=s.symbols')[0])
L7=X*Q+2*Y*P;L5=X*R+2*Y*Q;L3=X*cc(R)+2*cc(Y)*P
A1=cc(X)*P+2*cc(Y)*Q;A2=Y*cc(R)+X*cc(Q)+cc(Y)*Q;A3=X*cc(Q)+2*cc(Y)*Q
ls=s.symbols('l7 l5 l3',real=True);gg=s.symbols('g11 g12 g13 g22 g23 g33',real=True)
G=s.Matrix([[gg[0],gg[1],gg[2]],[gg[1],gg[3],gg[4]],[gg[2],gg[4],gg[5]]]);AA=s.Matrix([A1,A2,A3])
SOS=sum(li*ab(Li) for li,Li in zip(ls,[L7,L5,L3]))+s.re((s.conjugate(AA).T*G*AA)[0]).expand(complex=True)
eqs=s.Poly(s.expand(Ered/16-SOS),*V).coeffs()
unks=[ww[55],ww[59]]+list(ls)+list(gg)
sol=s.linsolve(eqs,unks);print('SOS family:',sol,flush=True)
(BASE/'sos_solution.txt').write_text(str(list(sol)[0])+'\n')
