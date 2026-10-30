"""Export the literal primitive and polynomial factorization certificate.

Includes a compact Hopf/Euler-gauge expression of the SAME exterior
derivative. The receiver uses rational sparse terms, not symbolic strings.
"""
from pathlib import Path
import hashlib,json,time
import sympy as S


def main():
    start=time.perf_counter();here=Path(__file__).parent
    family=json.loads((here/'ANGULAR_REDUCTION.json').read_text())
    candidate=json.loads((here/'PROFILE_CANDIDATE.json').read_text())
    A=S.symbols('a b c d',real=True);loc={str(v):v for v in A}
    loc.update({name:S.Rational(value)for name,value in candidate['parameters'].items()})
    P=S.Matrix([S.expand(S.sympify(text,locals=loc))for text in family['primitive_numerator']])
    T=sum(v*v for v in A);X=A[0]**2+A[2]**2-A[1]**2-A[3]**2
    Y=2*(A[0]*A[1]+A[2]*A[3]);Z=2*(A[0]*A[3]-A[1]*A[2])
    xi=S.Matrix([-A[2],-A[3],A[0],A[1]])
    R=(S.Matrix(A).T*P)[0]
    N=S.expand(T*P-S.Rational(1,4)*(T*S.Matrix([S.diff(R,v)for v in A])-R*S.Matrix([S.diff(T,v)for v in A])))
    grad=lambda f:S.Matrix([S.diff(f,v)for v in A])
    bx=Y*grad(X)-X*grad(Y);bz=Y*grad(Z)-Z*grad(Y)
    fs=[T*T*X,T*T*Z,X**3,X*X*Z,X*Z*Z,Z**3]
    ps=[T*T,X*X,X*Z,Z*Z]
    basis=[v*xi for v in fs]+[v*bx for v in ps]+[v*bz for v in ps]
    z=S.symbols('z:14');expr=sum((c*v for c,v in zip(z,basis)),S.zeros(4,1))-N
    equations=[v for e in expr for v in S.Poly(S.expand(e),A).coeffs()]
    M,rhs=S.linear_eq_to_matrix(equations,z);solution=next(iter(S.linsolve((M,rhs),z)))
    assert not any(v.free_symbols for v in solution)
    assert all(S.expand(e.subs(dict(zip(z,solution))))==0 for e in expr)
    def terms(expr,variables):return [[list(e),str(v)]for e,v in S.Poly(S.expand(expr),variables).terms()]
    b,d=A[1],A[3];factors=[]
    for row in candidate['leading_minors']:
        ff=[]
        for text,power in row['factors']:
            ff.append({'power':power,'terms':terms(S.sympify(text,locals={'b':b,'d':d}),(b,d))})
        factors.append({'k':row['k'],'constant':row['constant'],'factors':ff})
    out={'scope':'literal rational ordinary-heat primitive; independent algebraic/Sturm receiver required',
         'denominator':'T=a²+b²+c²+d²','primitive_coefficient_degree':3,
         'primitive_terms':[[i,e,c]for i,p in enumerate(P)for e,c in terms(p,A)],
         'P5_profile_parameters':candidate['parameters'],
         'canonical_Hopf_primitive':'T*f(X/T,Z/T)*xi + p(X/T,Z/T)*(Y dX-X dY) + r(X/T,Z/T)*(Y dZ-Z dY)',
         'Hopf_f_monomials':['x','z','x^3','x^2*z','x*z^2','z^3'],
         'Hopf_f_coefficients':[str(v)for v in solution[:6]],
         'Hopf_pr_monomials':['1','x^2','x*z','z^2'],
         'Hopf_p_coefficients':[str(v)for v in solution[6:10]],
         'Hopf_r_coefficients':[str(v)for v in solution[10:14]],
         'canonical_denominator':'T²; differs from P5/T by exact (−1/4)d(i_E alpha)',
         'leading_minor_factorizations':factors,
         'exceptional_slice':{'minor':6,'factor_index':1,'b2_power':1,
                              'repair':'p0+p1*u+p2*u²>0 from p2>0 and4p0p2−p1²>0; higher slices>=0'},
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'inputs':{name:hashlib.sha256((here/name).read_bytes()).hexdigest()for name in ['ANGULAR_REDUCTION.json','PROFILE_CANDIDATE.json']},
         'seconds_after_imports':time.perf_counter()-start}
    (here/'PRIMITIVE_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k]for k in ('Hopf_f_coefficients','Hopf_p_coefficients','Hopf_r_coefficients','seconds_after_imports')},indent=2))


if __name__=='__main__':main()
