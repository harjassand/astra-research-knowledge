"""Transport the strongest acquired boundary primitive into the generic gauge."""
from pathlib import Path
import json,sympy as S,numpy as np,time
here=Path(__file__).parent;start=time.perf_counter();case=here/'general_ray'
old=json.loads((here.parent/'outputs/angular_boundary/seed_299_301.json').read_text());ray=json.loads((here/'generic_nonpc_ray.json').read_text())
raw=json.loads((here/'general_angular_basis.json').read_text());A=S.symbols('a b c d',real=True);a,b,c,d=A;v=[S.Symbol(n,real=True) for n in raw['variables']]
co=np.array(list(map(float,map(S.Rational,ray['K_coefficients']))));B=np.array([[co[0],co[1]],[co[1],co[3]]]);val,V=np.linalg.eigh(B)
e=V[:,0]
if e@co[[2,4]]<0:e=-e
theta=np.arctan2(-e[1],e[0]);ps,pt=np.cos(theta/2),np.sin(theta/2)
L=S.Matrix([[ps,-pt,0,0],[pt,ps,0,0],[0,0,ps,-pt],[0,0,pt,ps]])
Pold=S.Matrix([sum(S.Rational(row[4],row[5])*S.prod(x**e for x,e in zip(A,row[:4])) for row in rows) for rows in old['P']])
Pold=(float(val[0])*L.T*Pold.subs(dict(zip(A,L*S.Matrix(A))),simultaneous=True)).applyfunc(S.expand)
loc={str(x):x for x in (*A,*v)};P=S.Matrix([S.sympify(x,locals=loc) for x in raw['P']])
T=sum(x*x for x in A)
def omega(P):
    out=[]
    for i in range(4):
        for j in range(i+1,4):out.append(S.expand(T*(S.diff(P[j],A[i])-S.diff(P[i],A[j]))-2*(A[i]*P[j]-A[j]*P[i])))
    return out
W,Wo=omega(P),omega(Pold);powers=set()
for x in W+Wo:powers.update(S.Poly(x,*A).monoms())
powers=sorted(powers);rows=[];target=[]
for ww,oo in zip(W,Wo):
    pp,qq=S.Poly(ww,*A),S.Poly(oo,*A)
    for power in powers:
        cc=pp.coeff_monomial(power);rows.append([float(S.diff(cc,x)) for x in v]);target.append(float(qq.coeff_monomial(power)))
M=np.array(rows);bb=np.array(target);fit,res,rank,sv=np.linalg.lstsq(M,bb,rcond=None)
out={'parameters':dict(zip(map(str,v),fit.tolist())),'density_fit_error':float(np.linalg.norm(M@fit-bb)),'rank':int(rank),'seconds':time.perf_counter()-start,
     'scope':'Numerical reference derived by an actual orthogonal-domain transport of the previously certified primitive. Not a certificate for the perturbed quartic.'}
(case/'reference.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
