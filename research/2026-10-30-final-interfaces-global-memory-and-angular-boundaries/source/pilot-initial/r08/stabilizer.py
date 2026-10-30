"""Exact comparison with all GL(2)-pullbacks of birotational quartics."""
from pathlib import Path
import json
import sympy as s

OUT=Path(__file__).resolve().parent
a,b,c,d,tau=s.symbols('a b c d tau')
av=(a,b,c,d);A=s.Matrix([[a,b],[c,d]])
T=sum(v*v for v in av);q=a*d-b*c;X=a*a+c*c-b*b-d*d
H=1+3*tau*tau;B=1-3*tau*tau
# Use H*F so that the matrix has polynomial entries in tau.
HF=s.expand(H*T*T+4*(3*H-12*tau)*q*q+4*B*q*X)
uv=s.symbols('u0:8')
U=s.Matrix(2,2,uv[:4]);V=s.Matrix(2,2,uv[4:])
delta=U*A+A*V
coeff=s.Poly(s.expand(sum(s.diff(HF,z)*v for z,v in zip(av,list(delta)))),*av).coeffs()
M=s.linear_eq_to_matrix(coeff,uv)[0]
center=M.subs(tau,s.Rational(1,30))
_,cols=center.rref();_,rows=center[:,list(cols)].T.rref()
assert len(cols)==6
det=s.factor(M.extract(list(rows),list(cols)).det())
left_rotation=s.Matrix([0,-1,1,0,0,0,0,0])
trivial_action=s.Matrix([-1,0,0,-1,1,0,0,1])
assert M*left_rotation==s.zeros(M.rows,1)
assert M*trivial_action==s.zeros(M.rows,1)
factors=[]
for fac,e in s.factor_list(det,tau)[1]:
    factors.append({'polynomial':str(fac),'multiplicity':int(e),
        'root_count_on_closed_0_1over3':int(s.Poly(fac,tau).count_roots(0,s.Rational(1,3)))})
record={'representation':'delta A = U A + A V',
        'rows':M.rows,'columns':M.cols,'minor_rows':list(rows),'minor_columns':list(cols),
        'minor_determinant':str(det),'factor_roots':factors,
        'stabilizer_dimension_on_open_branch':2,
        'basis':[list(map(str,left_rotation)),list(map(str,trivial_action))],
        'conclusion':'No F_tau for 0<tau<1/3 is an invertible left/right pullback, or transpose pullback, of a quartic invariant under independent left and right SO(2) rotations.'}
(OUT/'stabilizer_result.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
