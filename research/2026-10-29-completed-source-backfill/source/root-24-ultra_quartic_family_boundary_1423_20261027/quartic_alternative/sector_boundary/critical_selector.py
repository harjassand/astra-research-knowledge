"""Exact quadratic-field consequences of the acoustic kernel."""
from pathlib import Path
import json
import sympy as s
from acoustic_boundary import acoustic


def main():
    z=s.symbols('z');r=s.sqrt(42);tau=89-12*r
    mc=-s.Rational(39,58)+s.Rational(15,29)*r
    domain=s.QQ.algebraic_field(r);p=s.Poly(z**4-mc*z*z+1,z,domain=domain)
    def reduce(e):return s.Poly(s.expand(e),z,domain=domain).rem(p).as_expr()
    Q=acoustic(tau,z)
    A=s.Matrix([reduce((-1)**(i+3)*Q.minor_submatrix(3,i).det()) for i in range(4)])
    assert all(reduce(t)==0 for t in Q*A)
    a,b,c,d=A;u=a*a+c*c;v=b*b+d*d;q=reduce(a*d-b*c);uv=reduce(u-v)
    def ratio(num,den):
        pp=s.Poly(reduce(num),z,domain=domain);qq=s.Poly(reduce(den),z,domain=domain)
        answer=s.simplify(pp.LC()/qq.LC());assert reduce(num-answer*den)==0
        return s.radsimp(answer)
    aa=s.symbols('a0:4');av,bv,cv,dv=aa
    U=av*av+cv*cv;V=bv*bv+dv*dv;W=av*bv+cv*dv;D=av*dv-bv*cv
    f=U*U+V*V+3*W*W+tau*D*D+4*D*(U-V)
    H=s.hessian(f,aa).subs(dict(zip(aa,A)));direction=s.Matrix([1,z,0,0]);cof=s.Matrix([0,0,-z,1])
    knum=reduce((cof.T*H*direction)[0]);kden=reduce((1+z*z)*q)
    R=ratio(uv,q);K=ratio(knum,kden)
    out={'status':'EXACT_NECESSARY_SELECTOR_CONSTRAINT',
         'tau':str(tau),'critical_m':str(mc),'critical_polynomial_z':str(p.as_expr()),
         'r_over_q':str(R),'forced_kappa_over_q':str(K),
         'selector_constraint':'delta = forced_kappa_over_q - alpha*r_over_q',
         'kernel_vector':[str(e) for e in A]}
    (Path(__file__).resolve().parent/'CRITICAL_SELECTOR.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
