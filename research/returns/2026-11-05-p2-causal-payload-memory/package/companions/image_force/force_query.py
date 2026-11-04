"""Executed checks for a Stokes-adjoint raw-image force query.

This is algebra and deterministic quadrature, not an optical experiment and not
a simulated certification of a statistical confidence interval.
"""
from pathlib import Path
import json
import numpy as np
import sympy as sp
from numpy.polynomial.legendre import leggauss

OUT = Path(__file__).resolve().parent
x, y, B, C, D = sp.symbols("x y B C D", real=True)
s = x*x+y*y
q = C-B/s**2+D/(2*s)
q1 = 2*B/s**3-D/(2*s**2)
S = sp.Matrix([[2*x*(q+2*y*y*q1), 2*y*(q+(y*y-x*x)*q1)],
               [2*y*(q+(y*y-x*x)*q1), -2*x*(q+2*y*y*q1)]])
pressure = 8*C*x-2*D*x/s
gradp = sp.Matrix([sp.diff(pressure, z) for z in (x,y)])
Hp = sp.hessian(pressure, (x,y))
lap = lambda f: sp.diff(f,x,2)+sp.diff(f,y,2)
symbolic_checks = {
    "trace_S": sp.simplify(sp.trace(S)) == 0,
    "div_S_minus_half_grad_pressure": all(sp.simplify(sum(sp.diff(S[i,j],(x,y)[j]) for j in range(2))-gradp[i]/2)==0 for i in range(2)),
    "lap_S_minus_hessian_pressure": all(sp.simplify(lap(S[i,j])-Hp[i,j])==0 for i in range(2) for j in range(2)),
    "lap_pressure": sp.simplify(lap(pressure))==0,
}
assert all(symbolic_checks.values())

a, R = 1., 2.
den = (R*R+a*a)*np.log(R/a)-(R*R-a*a)
cn = 1/(2*den)
bn = -cn*a*a*R*R
dn = -2*cn*(R*R+a*a)
an = cn*(a*a-R*R)-dn*np.log(R)

def fields(z):
    xx, yy = np.asarray(z)[...,0], np.asarray(z)[...,1]
    ss = xx*xx+yy*yy
    qq = cn-bn/ss**2+dn/(2*ss)
    qq1 = 2*bn/ss**3-dn/(2*ss**2)
    h1 = 2*xx*(qq+2*yy*yy*qq1)
    h2 = 2*yy*(qq+(yy*yy-xx*xx)*qq1)
    matrix = np.stack([h1,h2,h2,-h1],axis=-1).reshape(xx.shape+(2,2))
    gp = np.stack([8*cn+2*dn*(xx*xx-yy*yy)/ss**2,
                   4*dn*xx*yy/ss**2],axis=-1)
    ph1 = 4*dn*xx*(-xx*xx+3*yy*yy)/ss**3
    ph2 = -4*dn*yy*(3*xx*xx-yy*yy)/ss**3
    hp = np.stack([ph1,ph2,ph2,-ph1],axis=-1).reshape(xx.shape+(2,2))
    return matrix,gp,hp

def query(z, end, mu=0.):
    ss,gp,hp=fields(z)
    displacement=np.asarray(end)-np.asarray(z)
    value=np.einsum("...i,...ij,...j->...",displacement,ss-mu*hp,displacement)
    return value+2*mu*np.einsum("...i,...i->...",gp,displacement)

def lap_query(z,end):
    _,gp,hp=fields(z)
    displacement=np.asarray(end)-np.asarray(z)
    return np.einsum("...i,...ij,...j->...",displacement,hp,displacement)-2*np.einsum("...i,...i->...",gp,displacement)

theta=2*np.pi*np.arange(512)/512
unit=np.stack([np.cos(theta),np.sin(theta)],axis=-1)
z=np.array([1.35,.25]); end=np.array([1.47,.20])
radial_profiles=[("ring",[(1.,.2)]),
                 ("two_rings",[(.625,.1),(.375,.3)]),
                 ("different_second_moment",[(1.,.3)])]
blur_checks=[]
for name,profile in radial_profiles:
    mu=sum(p*r*r for p,r in profile)/4
    blurred=sum(p*np.mean(query(z+r*unit,end,0.)) for p,r in profile)
    corrected=sum(p*np.mean(query(z+r*unit,end,mu)) for p,r in profile)
    actual=query(z,end)
    predicted=actual+mu*lap_query(z,end)
    blur_checks.append(dict(profile=name,mu=mu,true=float(actual),blurred=float(blurred),corrected=float(corrected),unadjusted_bias=float(blurred-actual),correction_error=float(corrected-actual),pizzetti_error=float(blurred-predicted)))
    assert abs(corrected-actual)<1e-11
    assert abs(blurred-predicted)<1e-11

# A manufactured steady incompressible flow, with fully specified body force.
# It vanishes at both circular walls, so its reciprocal boundary term is zero.
F=(s-1)**2*(4-s)**2
amplitude=sp.Rational(3,100)
alpha=sp.Rational(3,10)
beta=sp.Rational(2,5)
psi=amplitude*F*(1+alpha*x+beta*y)
u=sp.Matrix([sp.diff(psi,y),-sp.diff(psi,x)])
Ju=u.jacobian((x,y))
lapu=sp.Matrix([lap(u[i]) for i in range(2)])
rho=1.2; viscosity=.7
bodyforce=Ju*u-sp.Rational(7,12)*lapu
ufun=sp.lambdify((x,y),list(u),"numpy")
bfun=sp.lambdify((x,y),list(bodyforce),"numpy")
def velocity(z):
    return np.stack(ufun(z[...,0],z[...,1]),axis=-1)

rr,wr=leggauss(80)
rr=(R-a)*rr/2+(R+a)/2
wr=wr*(R-a)/2
ang=2*np.pi*np.arange(512)/512
grid=np.stack([rr[:,None]*np.cos(ang),rr[:,None]*np.sin(ang)],axis=-1)
weights=wr[:,None]*rr[:,None]*(2*np.pi/len(ang))
ug=velocity(grid)
sg,_,_=fields(grid)
local=np.einsum("...i,...ij,...j->...",ug,sg,ug)
inertial=float(np.sum(local*weights))
ss=grid[...,0]**2+grid[...,1]**2
gg=an+bn/ss+cn*ss+dn*np.log(ss)/2
qq=cn-bn/ss**2+dn/(2*ss)
virtual=np.stack([gg+2*grid[...,1]**2*qq,-2*grid[...,0]*grid[...,1]*qq],axis=-1)
bg=np.stack(bfun(grid[...,0],grid[...,1]),axis=-1)
forcing_work=float(np.sum(np.einsum("...i,...i->...",virtual,bg)*weights))
force_from_volume=rho*(inertial+forcing_work)
force_from_wall=float(72*np.pi*viscosity*float(amplitude)*float(beta))
assert abs(force_from_volume-force_from_wall)<1e-9

finite_lag=[]
for delta in [.008,.004,.002,.001]:
    final=grid.copy()
    dt=delta/8
    for _ in range(8):
        k1=velocity(final)
        k2=velocity(final+dt*k1/2)
        k3=velocity(final+dt*k2/2)
        k4=velocity(final+dt*k3)
        final+=dt*(k1+2*k2+2*k3+k4)/6
    acquired=float(np.sum(query(grid,final)*weights)/delta**2)
    finite_lag.append(dict(lag=delta,quadratic_current=acquired,instantaneous_current=inertial,error=acquired-inertial))

receipt=dict(
    scope="Symbolic identities, deterministic radial quadrature, and manufactured-flow mechanics; no observed images or experiment.",
    symbolic_checks=symbolic_checks,
    annulus=dict(a=a,R=R,A=an,B=bn,C=cn,D=dn,virtual_drag_on_body=4*np.pi*dn),
    blur_checks=blur_checks,
    manufactured_flow=dict(rho=rho,viscosity=viscosity,amplitude=float(amplitude),alpha=float(alpha),beta=float(beta),inertial_current=inertial,body_force_virtual_work=forcing_work,force_from_volume=force_from_volume,force_from_wall=force_from_wall,error=force_from_volume-force_from_wall),
    finite_lag=finite_lag,
)
(OUT/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))
