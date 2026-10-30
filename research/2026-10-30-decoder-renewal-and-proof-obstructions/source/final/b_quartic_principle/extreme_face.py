"""Exact full35 quartic face exposed by a fixed accepted Hopf endpoint.

Unknown coefficients are not restricted to objective/even quartics. This
is a symbolic necessary-face computation, not a sampled ROC test.
"""
from pathlib import Path
import json
import time
import hashlib
import sympy as S


def exponents(total, n):
    if n == 1:
        yield (total,)
    else:
        for j in range(total+1):
            for tail in exponents(total-j, n-1):
                yield (j,)+tail


def main():
    start=time.perf_counter()
    A=S.symbols('a b c d', real=True)
    e=S.symbols('e0:2', real=True)
    z=S.symbols('z0:2', real=True)
    C,D=S.symbols('C D', real=True)
    coeff=S.symbols('p0:35')
    powers=list(exponents(4,4))
    monomials=[S.prod(x**k for x,k in zip(A,p)) for p in powers]
    f=sum(x*y for x,y in zip(coeff,monomials))
    H=S.hessian(f,A)
    R=S.Matrix([e[0]*z[0],e[0]*z[1],e[1]*z[0],e[1]*z[1]])
    acoustic=S.expand((R.T*H*R)[0])
    equations=[]
    for base,xi in [([-D,C,C,D],(1,0)),([C,-D,D,C],(0,1))]:
        sub=dict(zip(A,base))|dict(zip(e,(C,D)))|dict(zip(z,xi))
        for variable in (*A,*e,*z):
            p=S.Poly(S.expand(S.diff(acoustic,variable).subs(sub,simultaneous=True)),C,D)
            equations.extend(p.coeffs())
    matrix,_=S.linear_eq_to_matrix(equations,coeff)
    matrix=S.Matrix(sorted(set(tuple(row) for row in matrix.tolist())))
    basis=matrix.nullspace()
    basis_polys=[S.factor(sum(x*y for x,y in zip(v,monomials))) for v in basis]
    q=A[0]*A[3]-A[1]*A[2]
    t=sum(x*x for x in A)
    x=A[0]**2+A[2]**2-A[1]**2-A[3]**2
    target=S.expand(t*t+12*q*q+4*q*x)
    target_coeff=S.Matrix([S.Poly(target,*A).coeff_monomial(m) for m in monomials])
    assert matrix*target_coeff==S.zeros(matrix.rows,1)
    report={
        'scope':'exact necessary face in all35 homogeneous quartic coefficients',
        'coefficient_exponents':[list(p) for p in powers],
        'constraint_matrix':[[str(x) for x in row] for row in matrix.tolist()],
        'matrix_shape':list(matrix.shape),'rank':matrix.rank(),
        'nullity':len(basis),'basis_polynomials':[str(p) for p in basis_polys],
        'target_coefficients':[str(x) for x in target_coeff],
        'elapsed_after_imports':time.perf_counter()-start,
        'random_draws':0,'ROC_samples':0,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    Path(__file__).with_name('EXTREME_FACE.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('matrix_shape','rank','nullity','basis_polynomials','elapsed_after_imports')},indent=2))


if __name__=='__main__':
    main()
