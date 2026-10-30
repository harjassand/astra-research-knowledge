# Test the entire real covariant cubic heat-correction family for Cplus.
from pathlib import Path
HERE=Path(__file__).resolve().parent
exec((HERE/'heat_probe.py').read_text().split('E=s.factor')[0])
exec((HERE/'cubic_heat.py').read_text().split('\n',1)[1].split('f1,f2,f3=')[0])
cs=s.symbols('c0:5',real=True)
terms=[cc(X)*QQ*RR,cc(Y)*RR**2,X*RR*cc(P),Y*QQ*cc(P),Y*RR*cc(QQ)]
expr=s.Poly(s.expand(EC-16*sum(k*re(term) for k,term in zip(cs,terms))),realvars)
eqs=list(expr.coeffs())
for i,j,k in combinations(range(4),3):eqs.append(s.diff(omega[j,k],A[i])-s.diff(omega[i,k],A[j])+s.diff(omega[i,j],A[k]))
sol=s.linsolve(eqs,unknown+cs)
print(sol)
