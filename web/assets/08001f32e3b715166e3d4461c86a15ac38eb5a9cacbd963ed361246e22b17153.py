"""Exact finite congruence checks and identity controls; not a Hardy verifier."""
from pathlib import Path
from fractions import Fraction
import json
import numpy as np
import sympy as sp

base=Path(__file__).parent
u,v=sp.symbols('u v',positive=True)
alpha,beta,kappa=sp.symbols('alpha beta kappa',real=True)
A=(u+1/u)/2;B=(u-1/u)/2
c=(u**2+u**-2)/2;h=(u**2-u**-2)/2
C=(v**2+v**-2)/2;sb=(v**2-v**-2)/2
tanhb=sb/C
m=2*beta*tanhb;n=1-1/C
da=2*alpha*h/c-kappa*(1-1/c)
P=h*beta+(alpha*c-kappa*h/2)*tanhb
Q=2*B*beta+(alpha-kappa*B)*tanhb/A
M=sp.Matrix([[A*A*m-kappa*n+B*B*da,-P,A*m-kappa*n],
             [-P,B*B*m+A*A*da,-Q],
             [A*m-kappa*n,-Q,m-kappa*n]])
S=sp.Matrix([[1,1,0],[1,-1,0],[0,0,1]])
nodes=[(beta-alpha,v/u),(beta+alpha,v*u),(beta,v)]
def kernel(i,j):
    x,ex=nodes[i];y,ey=nodes[j]
    sx=(ex**2-ex**-2)/2;sy=(ey**2-ey**-2)/2
    hx=(ex-ex**-1)/2;hy=(ey-ey**-1)/2
    return (x*sy+y*sx-2*kappa*hx*hy)/(ex/ey+ey/ex)
gram=sp.Matrix(3,3,kernel)
checks=[]
for i in range(3):
    for j in range(i,3):
        residual=sp.cancel((C*S.T*M*S/2-gram)[i,j])
        assert residual==0,(i,j,residual)
        checks.append({'name':f'congruence_{i}_{j}','residual':str(residual)})
extras={
 'stationary_constant':c*da-(2*alpha*h-kappa*(c-1)),
 'physical_Im_XY':4*A*B*beta+(2*alpha*c-kappa*h)*tanhb-2*P,
 'physical_a_Im_ZY':4*B*beta+2*(alpha-kappa*B)*tanhb/A-2*Q,
}
for name,expression in extras.items():
    residual=sp.cancel(expression)
    assert residual==0,(name,residual)
    checks.append({'name':name,'residual':str(residual)})

controls=json.loads((base/'DESIGNED_CONTROLS.json').read_text())['rows']
paulis=[np.kron(np.eye(2),p) for p in [np.array([[0.,1.],[1.,0.]]),np.array([[0.,-1j],[1j,0.]]),np.diag([1.,-1.])]]
results=[]
for row in controls:
    rho=np.array(row['rho_real_float'],dtype=complex)
    p=float(Fraction(row['exact_parameters']['p']))
    al=.5*np.log(p/(1-p))
    aa=np.cosh(al/2);bb=np.sinh(al/2);cc=np.cosh(al);hh=np.sinh(al)
    dd=2*al*np.tanh(al)-np.pi*(1-1/cc)
    vals,vec=np.linalg.eigh(rho)
    vals=vals[::-1];vec=vec[:,::-1]
    rotated=[vec.conj().T @ p @ vec for p in paulis]
    for noise_a in [0.,1.,-2.]:
        energy=dd*sum(vals[i]*(bb*bb*abs(rotated[0][i,i])**2+aa*aa*abs(rotated[1][i,i])**2) for i in range(4))
        for i in range(4):
            for j in range(i+1,4):
                w=vals[i]+vals[j];be=.5*np.log(vals[i]/vals[j])
                mm=2*be*np.tanh(be);nn=1-1/np.cosh(be)
                pp=hh*be+(al*cc-np.pi*hh/2)*np.tanh(be)
                qq=2*bb*be+(al-np.pi*bb)*np.tanh(be)/aa
                mat=np.array([[aa*aa*mm-np.pi*nn+bb*bb*dd,-pp,aa*mm-np.pi*nn],
                              [-pp,bb*bb*mm+aa*aa*dd,-qq],
                              [aa*mm-np.pi*nn,-qq,mm-np.pi*nn]])
                xyz=np.array([rotated[0][i,j],1j*rotated[1][i,j],noise_a*rotated[2][i,j]])
                energy+=w*np.vdot(xyz,mat @ xyz).real
        jm=np.array(row['J_matrix']);em=np.array(row['E_matrix'])
        co=np.array([1.,0.,noise_a])
        direct=float(co @ (jm-np.pi*em) @ co)
        results.append({'exact_parameters':row['exact_parameters'],'noise_a':noise_a,
                        'spectral_M_value':float(energy),'direct_value':direct,
                        'absolute_residual':float(abs(energy-direct))})
report={'status':'9 exact rational-function identities, plus finite physical identity diagnostics; no universal Hardy/operator verifier',
        'symbolic_exponential_parameters':'u=exp(alpha/2), v=exp(beta/2); identities are rational in u,v and linear in alpha,beta,kappa',
        'sympy_version':sp.__version__,'numpy_version':np.__version__,
        'exact_checks':checks,'number_of_control_checks':len(results),
        'maximum_control_absolute_residual':max(r['absolute_residual'] for r in results),
        'controls':results}
(base/'EXPOSED_KERNEL_REPLAY.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps({key:report[key] for key in ['status','sympy_version','number_of_control_checks','maximum_control_absolute_residual']},indent=2))
