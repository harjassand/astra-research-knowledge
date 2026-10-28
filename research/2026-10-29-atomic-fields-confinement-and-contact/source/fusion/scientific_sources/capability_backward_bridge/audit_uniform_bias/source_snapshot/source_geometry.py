"""Lopez2610.29921v1 map, z=exp(i*phi), a=sqrt(lambda)."""
import sympy as s
def geometry():
    z=s.symbols('z',nonzero=True);a,b=s.symbols('a b',real=True,positive=True);I=s.I
    p=a*z;pb=a/z
    N=s.Matrix([1-p*p,I*(1+p*p),2*p]);Nb=s.Matrix([1-pb*pb,-I*(1+pb*pb),2*pb])
    A=(N+Nb)/2;C=(N-Nb)/(2*I)
    H=2*p*p+2*I*p**3;Hb=2*pb*pb-2*I*pb**3
    nv=s.Matrix([a*(z+1/z),a*(z-1/z)/I,a*a-1])/(1+a*a)
    k=2*a**3*(z+1/z)*(1-a*(z-1/z)/(2*I))/(1+a*a)**2
    X=(((H+Hb)/2*A+(H-Hb)/(2*I)*C)/(1+a*a)**2+(b-k)*nv).applyfunc(s.cancel)
    return z,a,b,X
