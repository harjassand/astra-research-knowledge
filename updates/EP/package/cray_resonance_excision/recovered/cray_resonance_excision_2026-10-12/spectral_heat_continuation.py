"""Local exact resonance cancellation and a finite Taylor remainder majorant.

F(h) = h^(-1/2) J_g(d + J^2/h)
     = |J|^(-1) [ exp(h/(2 J^2) d^2/dx^2) f ](0),
 f(x)=exp(-d*x^2/2 - g*x^4/4), Re d >= 0, Re h >= 0.

The heat formula is exact. The polynomial/error functions below are floating
implementations of explicit mathematical bounds; not interval certified.
"""
import math, json
from pathlib import Path
import numpy as np
from numpy.polynomial import Polynomial
import mpmath as mp

def derivative_poly(order,g,d):
    p=Polynomial([1.])
    drift=Polynomial([0.,d,0.,g])
    for _ in range(order): p=p.deriv()-drift*p
    return p

def even_moment(power,g):
    if power%2:return 0.
    return .5*(2/g)**((power+1)/4)*math.gamma((power+1)/4)

def l2_majorant(p,g):
    q=p*Polynomial(np.conjugate(p.coef))
    return sum(abs(a)*even_moment(k,g) for k,a in enumerate(q.coef))

def evaluate(h,J=1.,g=1.,d=.2-.7j,order=2):
    if g<=0 or J==0 or d.real<0 or h.real<0:
        raise ValueError('Require g>0, J != 0, Re d>=0 and Re h>=0')
    value=0j
    for k in range(order+1):
        coeff=derivative_poly(2*k,g,d)(0.)
        value+=(h/(2*J*J))**k*coeff/math.factorial(k)
    value/=abs(J)
    r=2*order+2
    B=l2_majorant(derivative_poly(r,g,d),g)+l2_majorant(derivative_poly(r+1,g,d),g)
    error=(abs(h)/(2*J*J))**(order+1)*math.sqrt(B/2)/(abs(J)*math.factorial(order+1))
    return value,error

def special_reference(h,J=1.,g=1.,d=.2-.7j):
    mp.mp.dps=70
    hh=mp.mpc(h); dd=mp.mpc(d); gg=mp.mpf(g); jj=mp.mpf(J)
    s=dd+jj*jj/hh
    u=s*s/(8*gg)
    I=mp.sqrt(s/(2*gg))*mp.exp(u)*mp.besselk(mp.mpf(1)/4,u)
    return complex(I/mp.sqrt(2*mp.pi*hh))

def main():
    rows=[]
    for radius in [1e-1,1e-2,1e-3,1e-4,1e-6,1e-8]:
        for direction in [1+0j,(1+10j)/math.sqrt(101)]:
            h=radius*direction
            value,bound=evaluate(h)
            ref=special_reference(h)
            error=abs(value-ref)
            # For tiny h the bound can be below double precision; compare
            # with an explicit 1e-14 floating diagnostic floor, NOT a proof.
            assert error<=bound+1e-14
            rows.append(dict(h=[h.real,h.imag],bare_pivot_magnitude=abs(h)**-.5,
                regularized_value=[ref.real,ref.imag],heat_polynomial=[value.real,value.imag],
                observed_absolute_error=error,analytic_remainder_majorant=bound))
    out={'status':'Exact identity and derived analytic bound; 70-digit special-function diagnostic, not interval proof',
         'g':1,'J':1,'d':[.2,-.7],'taylor_order':2,'cases':rows,
         'missing_coupling_counterexample':'J=0 leaves h^(-1/2) J_g(d); no resonance cancellation',
         'rank_extension':'An invertible real coupling block B removes all covered zero modes with cost containing |det B|^-1 and the block Fourier L1 norm.'}
    root=Path(__file__).parent
    (root/'spectral_heat_results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
