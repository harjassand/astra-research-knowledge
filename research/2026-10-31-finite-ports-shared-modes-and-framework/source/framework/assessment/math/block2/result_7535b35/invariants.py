exec((__import__('pathlib').Path(__file__).parent/'leading_psd.py').read_text().split("q,z=s.symbols")[0])
X=x1+s.I*x2;Y=y1+s.I*y2;P=P1+s.I*P2;Q=Q1+s.I*Q2;R=R1+s.I*R2
cc=s.conjugate;ab=lambda z:s.expand(z*cc(z));re=lambda z:s.expand((z+cc(z))/2)
terms=[ab(X)*ab(P),ab(Y)*ab(P),ab(X)*ab(Q),ab(Y)*ab(Q),ab(X)*ab(R),ab(Y)*ab(R),re(cc(X)*Y*P*cc(Q)),re(cc(X)*cc(Y)*Q*Q),re(cc(X)*Y*Q*cc(R)),re(cc(Y)**2*Q*R),re(cc(X)*cc(Y)*P*R)]
k=s.symbols('k:11');eqs=s.Poly(s.expand(Ered/16-s.Add(*(ki*ti for ki,ti in zip(k,terms)))),*V).coeffs();sol=s.linsolve(eqs,k)
print('Invariant coefficients:',sol,flush=True)
(BASE/'invariant_coeffs.txt').write_text(str(list(sol)[0])+'\n')
