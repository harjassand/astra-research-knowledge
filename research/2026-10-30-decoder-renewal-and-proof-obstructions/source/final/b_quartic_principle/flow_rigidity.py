"""Exact acoustic determinant in the symmetry-reduced constant-flow class."""
from pathlib import Path
import hashlib,json,time
import sympy as S


def main():
    start=time.perf_counter()
    a,b,c,d=S.symbols('a b c d',real=True)
    u,v,t,ell,nu=S.symbols('u v t ell nu',real=True)
    A=(a,b,c,d)
    q=a*d-b*c;T=sum(x*x for x in A);x=a*a+c*c-b*b-d*d
    f=T*T+12*q*q+4*q*x
    H=S.hessian(f,A).subs({a:0,b:1,c:1,d:0})
    R=S.Matrix([u,u*t,v,v*t])
    acoustic=S.expand((R.T*H*R)[0])
    B=S.hessian(acoustic,(u,v))/2
    assert B==S.Matrix([[64*t*t,32*t],[32*t,16*(1+t*t)]])
    J=S.Matrix([[0,-1],[1,0]])
    L=ell*(1+t*t)*S.eye(2)+2*nu*t*J
    Q=S.expand((B*L+L.T*B)/2)
    determinant=S.factor(Q.det())
    assert S.expand(determinant).coeff(t,2)==-256*nu*nu
    assert S.factor(determinant.subs(nu,0))==1024*ell*ell*t**4*(1+t*t)**2
    out={'scope':'all real ell,nu,t; exact acoustic obstruction, no sampled flow',
         'acoustic_matrix':[[str(x) for x in row] for row in B.tolist()],
         'det_sym_BL':str(determinant),'t2_coefficient':str(S.expand(determinant).coeff(t,2)),
         'consequence':'nonnegative for all real t forces nu=0',
         'seconds_after_imports':time.perf_counter()-start,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Path(__file__).with_name('FLOW_RIGIDITY.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
