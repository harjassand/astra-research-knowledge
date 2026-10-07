"""Independent exact connection check for the sheared Sol counterexample."""
from pathlib import Path
import json
import sympy as sp

x,y,t=sp.symbols('x y t',real=True)
a,eps,omega,nu=sp.symbols('a eps omega nu',positive=True)
h=sp.Function('h')(t)
c=sp.diff(h,t)-2*a*h
coords=(x,y,t)
g=sp.Matrix([[sp.exp(2*a*t),h,0],[h,sp.exp(-2*a*t)*(1+h*h),0],[0,0,1]])
gi=g.inv()
U=sp.Matrix([[sp.exp(-a*t),-h*sp.exp(-a*t),0],[0,sp.exp(a*t),0],[0,0,1]])
checks={}
simp=lambda z:sp.simplify(sp.trigsimp(z))
def check(name,z):
    checks[name]=all(simp(v)==0 for v in z) if isinstance(z,(sp.MatrixBase,list,tuple)) else simp(z)==0

check('constant_volume',g.det()-1)
check('orthonormal_frame',U.T*g*U-sp.eye(3))
Gamma=[[[simp(sum(gi[i,l]*(sp.diff(g[l,k],coords[j])+sp.diff(g[l,j],coords[k])-sp.diff(g[j,k],coords[l])) for l in range(3))/2) for k in range(3)] for j in range(3)] for i in range(3)]
D=sp.Matrix(3,3,lambda i,j:Gamma[i][j][2])
S=simp((D+gi*D.T*g)/2)
B=U.inv()*S*U
check('strain_from_connection',B-sp.Matrix([[a,c/2,0],[c/2,-a,0],[0,0,0]]))
check('divergence_X',sum(Gamma[i][i][2] for i in range(3)))
check('zero_advection',sp.Matrix([Gamma[i][2][2] for i in range(3)]))
Scov=g*S
divcov=sp.Matrix(3,1,lambda i,_:simp(sum(gi[j,k]*(sp.diff(Scov[k,i],coords[j])-sum(Gamma[l][j][k]*Scov[l,i]+Gamma[l][j][i]*Scov[k,l] for l in range(3))) for j in range(3) for k in range(3))))
check('stress_divergence',gi*divcov-sp.Matrix([0,0,-2*a*a-c*c/2]))
coframe=U.inv()[:2,:2]
check('normal_growth_generator',sp.diff(coframe,t)*coframe.inv()-sp.Matrix([[a,c],[0,-a]]))
hpert=eps*(omega*sp.sin(omega*t)-2*a*sp.cos(omega*t))/(omega**2+4*a*a)
check('periodic_shear_solution',sp.diff(hpert,t)-2*a*hpert-eps*sp.cos(omega*t))
p=-nu*eps*eps/(4*omega)*sp.sin(2*omega*t)
check('constant_force_with_pressure',nu*(4*a*a+(eps*sp.cos(omega*t))**2)+sp.diff(p,t)-nu*(4*a*a+eps*eps/2))
cc,theta=sp.symbols('cc theta',real=True)
xi=sp.Matrix([sp.cos(theta),sp.sin(theta)])
perp=sp.Matrix([-sp.sin(theta),sp.cos(theta)])
skew=sp.Matrix([[0,cc/2],[-cc/2,0]])
check('strain_eigenline_spin', (perp.T*skew*xi)[0]+cc/2)
z=sp.Function('z')(t)
check('angle_derivative',sp.diff(sp.atan(z/(2*a))/2,t)-a*sp.diff(z,t)/(4*a*a+z*z))
check('rotation_cross_term_is_derivative',a*z*sp.diff(z,t)/(4*a*a+z*z)-sp.diff(a*sp.log(4*a*a+z*z)/2,t))
report={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'scope':'Exact smooth sheared metric, strain/stress, cocycle generator, force and angular formulas. No entropy acquisition or external analytic certification.','sympy_version':sp.__version__}
Path(__file__).with_name('shear_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
assert all(checks.values())
