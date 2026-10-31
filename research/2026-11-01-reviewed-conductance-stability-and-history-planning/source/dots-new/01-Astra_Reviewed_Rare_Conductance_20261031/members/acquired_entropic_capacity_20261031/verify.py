"""Separate receiving entry point: bind exact certificate to raw task input.

It reconstructs coefficients/coordinate and all integer integral bounds. It
does not authenticate a physical polynomial or prove the mathematical theorem.
"""
from fractions import Fraction as F
from capacity import acquire, Integrator, Unknown, strict_positive_int


def canonical_fraction(x):
    if type(x) is not str:
        raise Unknown("fraction must be canonical string")
    try:
        y=F(x)
    except (ValueError,ZeroDivisionError) as exc:
        raise Unknown("invalid rational string") from exc
    if str(y)!=x:
        raise Unknown("noncanonical fraction")
    return y


def receiving_verify(raw,cert,*,beta=F(1),max_quad_ratio=F(101,100),
                     max_grid=131072,max_precision=16384,max_points=524288,
                     max_cutoff=65536,max_product_bits=2000000):
    if type(cert) is not dict or type(beta) is not F or beta<=0:
        raise Unknown("task/certificate schema")
    if type(max_quad_ratio) is not F or max_quad_ratio<1:
        raise Unknown("quadrature ratio must be an exact Fraction at least one")
    for name,value in [("grid budget",max_grid),("point budget",max_points),
                       ("cutoff budget",max_cutoff),("precision budget",max_precision),
                       ("product-bit budget",max_product_bits)]:
        strict_positive_int(value,name)
    acquired=acquire(raw)
    n,m=acquired["n"],acquired["m"]
    if cert.get("schema")!="entropic_capacity.v1":
        raise Unknown("certificate schema version")
    if type(cert.get("n")) is not int or type(cert.get("m")) is not int or cert["n"]!=n or cert["m"]!=m:
        raise Unknown("dimension binding")
    if cert.get("ell")!=acquired["ell"] or canonical_fraction(cert.get("beta"))!=beta or cert.get("b")!="1/2":
        raise Unknown("coordinate/beta/basin binding")
    if cert.get("direction_rational")!=acquired["direction_rational"] or cert.get("direction_norm_squared")!=acquired["direction_norm_squared"]:
        raise Unknown("exact radical direction binding")
    if cert.get("basins")!="ell.x <= -b and ell.x >= b" or cert.get("observable")!="cap_mu(A,B)/mu(A)":
        raise Unknown("task meaning changed")
    N,p=cert.get("grid_N"),cert.get("precision_bits")
    if type(N) is not int or N<=0 or N>max_grid or N&(N-1):
        raise Unknown("grid admission budget")
    if type(p) is not int or p<=0 or p>max_precision:
        raise Unknown("precision admission budget")
    T=canonical_fraction(cert.get("cutoff_T"))
    if T.denominator!=1 or T<2 or T>max_cutoff or T.numerator&(T.numerator-1):
        raise Unknown("cutoff admission budget")
    # Guard the actual expanded number of grid evaluations, not only N.
    if N*(2*int(T)+1)>max_points:
        raise Unknown("total-grid admission budget")
    ks=[F(k) for k in acquired["kappa"]] if acquired["kappa"] is not None else None
    coeff=[F(c) for c in acquired["determinant_coefficients"]] if acquired["determinant_coefficients"] is not None else None
    ii=Integrator(ks,p,coeff,max_points,max_product_bits)
    left=ii.monotone_integral(F(1,2),F(1),N,0)
    right=ii.monotone_integral(F(1),T,N*int(2*(T-1)),0)
    mass=(left[0]+right[0],left[1]+right[1]+ii.tail(T))
    rr=ii.monotone_integral(F(0),F(1,2),N,1)
    resistance=(2*rr[0],2*rr[1])
    if min(mass+resistance)<=0:
        raise Unknown("nonpositive numerical lower bound")
    if mass[1]*resistance[1]>max_quad_ratio*mass[0]*resistance[0]:
        raise Unknown("requested quadrature accuracy not met")
    factor=1+F(8,9)/beta
    free=(1/(beta*mass[1]*resistance[1]),1/(beta*mass[0]*resistance[0]))
    full=(free[0]/factor,free[1])
    pairs={"mass_A_unnormalized":mass,"resistance":resistance,
           "free_energy_rate":free,"full_diffusion_rate":full}
    for name,pair in pairs.items():
        got=cert.get(name)
        if type(got) is not dict or canonical_fraction(got.get("lower"))!=pair[0] or canonical_fraction(got.get("upper"))!=pair[1]:
            raise Unknown("wrong exact interval: "+name)
    if canonical_fraction(cert.get("universal_factor"))!=factor or canonical_fraction(cert.get("tail_upper"))!=ii.tail(T):
        raise Unknown("wrong loss factor or omitted tail")
    return {"status":"PASS","n":n,"grid_points":len(ii.cache),
            "max_integer_bits":ii.max_integer_bits,
            "receiving_scope":"exact raw polynomial, acquired full-fiber basins, stated beta, capacity/mass only"}
