"""Independent governing-equation check; no producer imports.

Exact Sturm roots replace the producer's Bernstein implementation. Full
external/internal equations also retain the source short circuit and connectors.
The internal-motion family is a constructed passive countermodel, not hardware.
"""
from pathlib import Path
import json
import math
import numpy as np
import sympy as s

OUT=Path(__file__).resolve().parent
x,w=s.symbols('x w', positive=True, real=True)
m0,m,k,c,g,R,L=map(s.Rational,['4.971','1.21','42992','4.56','12.5','1.7','.009'])
h=k+s.I*w*c+s.I*w*g*g/(R+s.I*w*L)
condensed=-w*w*m0+h-h*h/(h-m*w*w)
expected=-w*w*(m0+m*h/(h-m*w*w))
assert s.cancel(condensed-expected)==0
d=R*R+L*L*x
A=k*d+g*g*L*x
B=c*d+g*g*R
T=s.expand((A-m*x*d)**2+x*B**2)
N=s.expand(m0*T+m*(A*(A-m*x*d)+x*B**2))
J=s.expand(m*m*x*x*B*d)
identity=s.cancel(expected-(-x*N/T+s.I*w*J/T).subs(x,w*w))
assert identity==0
# Cross-port reciprocity/power consequence for the fixed electrical short.
H=-g*m*w*w/((R+s.I*w*L)*(k-m*w*w+s.I*w*c)+s.I*w*g*g)
relative=m*w*w/(h-m*w*w)
abs_sq=lambda z:s.cancel(z*s.conjugate(z))
imag_a=s.cancel((expected-s.conjugate(expected))/(2*s.I))
assert s.cancel(imag_a-w*R*abs_sq(H)-w*c*abs_sq(relative))==0
lo=(s.Rational(333,106)*62)**2
hi=(s.Rational(355,113)*64)**2
D=s.Integer(50000)
edge_upper=s.Integer(25501)
beta=s.Integer(278000)
P=s.Poly((D*T-x*N)**2+x*(J+50*T)**2-(2*edge_upper+beta)**2*T*T,x)
loss=s.Poly(x*J*J-157000**2*T*T,x)
root_checks={}
for name,p in [('denominator',s.Poly(T,x)),('dominance',P),('loss',loss),('imaginary_numerator',s.Poly(J,x))]:
    roots=int(p.count_roots(lo,hi))
    left=p.eval(lo)
    assert roots==0 and left>0
    root_checks[name]={'degree':p.degree(),'roots_in_rational_band':roots,'left_sign':1}
assert D*D+hi*50**2<(2*edge_upper)**2
paid=beta-30000
den=(paid+2*edge_upper)*(paid+edge_upper)-edge_upper**2
two=edge_upper**2/den
assert two<s.Rational(1,100)

# Derive the rigid comparator from its two physical node equations.
mass2=s.symbols('mass2', real=True)
M=2*(m0+m)
ww=s.Integer(198);xx=ww*ww;z=25000+s.I*ww*25
rigid=s.Matrix([[z*2-xx*(M-mass2),-z],[-z,z-xx*mass2]])
det=s.expand(rigid.det())
assert s.expand(det-(xx**2*mass2*(M-mass2)-xx*z*(M+mass2)+z*z))==0
real=s.re(det)
vertex=s.solve(s.diff(real,mass2),mass2)[0]
assert 0<vertex<M and s.diff(real,mass2,2)<0
rmax=real.subs(mass2,vertex)
assert rmax>0 and abs(real.subs(mass2,0))<=rmax and abs(real.subs(mass2,M))<=rmax
imag=s.im(det)
imax=max(abs(imag.subs(mass2,0)),abs(imag.subs(mass2,M)))
lower_sq=s.cancel((s.re(z)**2+s.im(z)**2)**2/(rmax*rmax+imax*imax))
assert lower_sq>s.Rational(1,10000)

# Independent exact bound on nominal relative internal motion, |r-q|/|q|.
# h-m*w^2=(A-m*x*d+i*w*B)/d. A factor of 5 is sufficient.
stroke_poly=s.Poly(25*T-m*m*x*x*d*d,x)
assert stroke_poly.count_roots(lo,hi)==0 and stroke_poly.eval(lo)>0

diagnostic=[]
for f in [31,31.5,32]:
    ww=2*math.pi*f
    hh=complex(h.subs(w,ww));z=25000+1j*ww*25
    mat=np.zeros((4,4),complex)
    for j in range(2):
        q,p=2*j,2*j+1
        mat[q,q]=-ww*ww*float(m0)+hh+(2 if j==0 else 1)*z
        mat[p,p]=hh-ww*ww*float(m)
        mat[q,p]=mat[p,q]=-hh
    mat[0,2]=mat[2,0]=-z
    sol=np.linalg.solve(mat,np.array([z,0,0,0]))
    rel=sol[1::2]-sol[::2]
    current=-1j*ww*float(g)*rel/(float(R)+1j*ww*float(L))
    heat=.5*float(c)*ww**2*np.abs(rel)**2+.5*float(R)*np.abs(current)**2
    aa=complex(expected.subs(w,ww))
    port_heat=.5*ww*aa.imag*np.abs(sol[::2])**2
    assert np.allclose(heat,port_heat,rtol=2e-12,atol=1e-8)
    diagnostic.append(dict(frequency_Hz=f,
        displacement_per_unit_base=np.abs(sol[::2]).tolist(),
        relative_internal_stroke_per_unit_base=np.abs(rel).tolist(),
        short_circuit_current_A_per_m_base=np.abs(current).tolist(),
        mechanical_and_Joule_W_per_m2_base=heat.tolist(),
        base_reaction_N_per_m_base=float(abs(z*(1-sol[0])))))

# Exact passive family: redistribute mass mu from carrier to one hidden branch.
# Delta a=-mu*w^4/(w0^2-w^2+i*gamma*w), mu=eps*gamma/W^3.
# This gives |Delta a|<=mu*w^3/gamma<=eps over 0<w<=W.
gamma_values=[1,1e-2,1e-4,1e-6]
eps,W,w0=1000.,202.,198.
family=[]
for gamma in gamma_values:
    mu=eps*gamma/W**3
    delta=-mu*w0**4/(1j*gamma*w0)
    stroke=w0/gamma
    # Mean kinetic energy of hidden mass for harmonic port amplitude 1m.
    kinetic=.25*mu*w0*w0*(1+stroke*stroke)
    assert abs(delta)<=eps
    family.append(dict(gamma_per_s=gamma,branch_mass_kg=mu,
        relative_stroke_per_unit_port=stroke,
        port_discrepancy_at_w0_N_per_m=abs(delta),
        mean_hidden_kinetic_J_per_m2_port=kinetic))

result=dict(scope='Independent exact source-model identity/root checks, numerical internal-cost diagnostics, and a constructed passive hidden-motion family. No physical qualification or priority claim.',
    source_identity_exact=True,resistive_power_loss_identity_exact=True,
    source_margin_Sturm_checks=root_checks,
    paid_two_cell_bound_exact=str(two),nominal_internal_stroke_factor_bound=5,
    all_rigid_mass_allocations_lower_bound_squared_exact=str(lower_sq),
    full_matrix_diagnostics=diagnostic,
    hidden_motion_family=dict(epsilon_N_per_m=eps,wmax_rad_per_s=W,w0_rad_per_s=w0,
        static_mass_preserved=True,uniform_band_discrepancy_bound_proved=True,cases=family))
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
