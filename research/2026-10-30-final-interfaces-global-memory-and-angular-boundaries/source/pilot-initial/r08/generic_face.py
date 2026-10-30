"""Symbolic parameter version of the full quartic acoustic face."""
from pathlib import Path
import importlib.util
import json
import time
import sys
import sympy as s

OUT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("face",OUT/"extreme_face.py")
face=importlib.util.module_from_spec(spec); spec.loader.exec_module(face)
a,b,c,d,t,x,y=face.a,face.b,face.c,face.d,face.t,face.x,face.y
av=face.av
tau=s.symbols('tau')
B=1-3*tau*tau; H=1+3*tau*tau
domain=s.QQ.frac_field(tau)
mod=s.Poly(B**2*(1-t*t)**2-(1-4*tau+3*tau*tau)*H*(1+t*t)**2,t,domain=domain).monic()
K=[-B*(tau*(1-t*t)+H*t*t)*(1+t*t),
   B*t*(H-tau*(1-t*t))*(1+t*t),
   B*B*t*(1-t*t)-tau*H*t*(1+t*t)**2,
   B*B*t*t*(1-t*t)+tau*H*(1+t*t)**2]
K=[s.Poly(kk,t,domain=domain).rem(mod).as_expr() for kk in K]
Ku=s.Matrix([x*K[0]-y*K[2],x*K[1]-y*K[3],
             y*K[0]+x*K[2],y*K[1]+x*K[3]])
R=dict(zip(av,(x,x*t,y,y*t)))
start=time.perf_counter();columns=[]
for mon in face.monomials:
    hh=s.hessian(mon,av).subs(R,simultaneous=True)
    col=[]
    for v in hh*Ku:
        pp=s.Poly(s.expand(v),x,y)
        for ix in range(4):
            rem=s.Poly(pp.coeff_monomial(x**ix*y**(3-ix)),t,domain=domain).rem(mod)
            col.extend(rem.nth(j) for j in range(4))
    columns.append(col)
L=s.Matrix.hstack(*[s.Matrix(col) for col in columns])
print('matrix built',time.perf_counter()-start,flush=True)
center=L.subs(tau,s.Rational(1,30))
_,cols=center.rref()
reverse='--reverse' in sys.argv
exception='--pivot-exception' in sys.argv
if exception:
    # This only proposes row indices. The determinant below is exact.
    import numpy as np
    residual=np.array(L[:,list(cols)].subs(tau,0.201222525334277),dtype=float)
    scale=np.linalg.norm(residual,axis=1)
    scale[scale==0]=1
    residual/=scale[:,None]
    chosen=[]
    for _ in range(34):
        norms=np.linalg.norm(residual,axis=1)
        index=int(np.argmax(norms))
        assert norms[index]>1e-8 and index not in chosen
        chosen.append(index)
        vec=residual[index]/norms[index]
        residual-=np.outer(residual@vec,vec)
    rows=tuple(chosen)
elif reverse:
    _,positions=center[:,list(cols)][::-1,:].T.rref()
    rows=tuple(center.rows-1-i for i in positions)
else:
    _,rows=center[:,list(cols)].T.rref()
minor=L.extract(list(rows),list(cols))
# Clear every row's rational-function denominator first.
denoms=[]
for i in range(minor.rows):
    den=s.lcm_list([s.denom(s.cancel(v)) for v in minor.row(i)])
    denoms.append(den)
    for j in range(minor.cols):minor[i,j]=s.cancel(minor[i,j]*den)
print('minor denominators cleared',time.perf_counter()-start,flush=True)
from sympy.polys.matrices import DomainMatrix
dm=DomainMatrix.from_Matrix(minor).convert_to(s.QQ.poly_ring(tau))
det=s.factor(dm.det().as_expr())
print('minor determinant',det,'seconds',time.perf_counter()-start,flush=True)
T=sum(v*v for v in av);q=a*d-b*c;X=a*a+c*c-b*b-d*d
F=s.Poly(s.expand(T*T+4*(3-12*tau/H)*q*q+4*B/H*q*X),*av)
fv=s.Matrix([F.coeff_monomial(m) for m in face.monomials])
assert all(s.cancel(v)==0 for v in L*fv)
output={'minor_rows':list(rows),'minor_columns':list(cols),
        'row_denominators':list(map(str,denoms)),
        'cleared_minor_determinant':str(det),
        'F_in_generic_kernel':True,
        'generic_modulus':str(mod.as_expr()),
        'seconds':time.perf_counter()-start}
filename=('generic_face_exception_result.json' if exception else
          'generic_face_reverse_result.json' if reverse else 'generic_face_result.json')
(OUT/filename).write_text(json.dumps(output,indent=2)+'\n')
