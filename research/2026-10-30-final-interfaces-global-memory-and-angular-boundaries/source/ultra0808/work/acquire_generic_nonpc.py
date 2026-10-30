"""Acquire an exact non-aligned exposed ray using the five-jet normal form."""
from pathlib import Path
import sympy as S,numpy as np,json,time
from scipy.optimize import minimize_scalar
here=Path(__file__).parent;start=time.perf_counter()
raw=json.loads((here/'hopf_cone_geometry.json').read_text());nf=json.loads((here/'exposed_normal_form.json').read_text())
vv=S.symbols('u l p n q r',real=True);loc={str(x):x for x in vv};t=S.Symbol('t',real=True)
H=[S.Matrix([[S.sympify(x,locals=loc) for x in row] for row in mat]) for mat in raw['H_coefficients']]
hf=[S.lambdify(vv,x,'numpy',cse=True) for x in H]
a,b,c=S.symbols('a b c',real=True);co=[S.sympify(x,locals={'a':a,'b':b,'c':c}) for x in nf['coefficient_polynomials']]
z=S.Symbol('z')
def F(A,k):
    aa,bb,cc,dd=A;X=aa*aa+cc*cc-bb*bb-dd*dd;Y=2*(aa*bb+cc*dd);Z=2*(aa*dd-bb*cc)
    u,l,p,n,q,r=k
    return u*X*X+2*l*X*Y+2*p*X*Z+n*Y*Y+2*q*Y*Z+r*Z*Z
def support_gap(k,base,Rs):
    vals=[]
    for R in Rs:
        pp=S.Poly(S.expand(F(tuple(x+y*z for x,y in zip(R,base)),k)),z)
        c0,c1,c2=[pp.nth(i) for i in range(3)]
        vals.append(S.factor((c2-c1*c1/(4*c0))/(R[0]*R[3]-R[1]*R[2])))
    return vals,vals[1]-vals[0]
for nn,pp,qq in [(1.001,299/301,.001),(1.01,299/301,.01),(1.0001,299/301,.0001)]:
    B=np.diag([1.,nn]);dd=np.array([pp,qq]);HH=2*nn*np.eye(2)-B@B-np.outer(dd,dd);tt=np.array([qq,-nn*pp])
    def threshold(theta):
        e=np.array([np.cos(theta),np.sin(theta)])
        return (e@(B@B+3*np.outer(dd,dd))@e+4*(e@tt)**2/(e@HH@e))/(2*e@B@e)
    grid=np.linspace(0,np.pi,2001,endpoint=False);center=max(grid,key=threshold)
    fit=minimize_scalar(lambda x:-threshold(x),bounds=(center-.01,center+.01),method='bounded',options={'xatol':1e-15})
    theta=fit.x;k0=[1.,0.,pp,nn,qq,-fit.fun]
    ps=np.cos(theta/2);pt=np.sin(theta/2);ht=np.array(hf[0](*k0))*ps*ps+np.array(hf[1](*k0))*ps*pt+np.array(hf[2](*k0))*pt*pt
    val,vec=np.linalg.eigh(ht);AR=vec[:,0].reshape(2,2)@np.array([[ps,-pt],[pt,ps]])
    AR/=AR[1,1];av=[S.Rational(float(x)).limit_denominator(1000000) for x in (AR[0,0],AR[0,1],AR[1,0])]
    k=[S.factor(x.subs(dict(zip((a,b,c),av)))) for x in co]
    if k[0]<0:k=[-x for x in k]
    k=[S.factor(x/k[0]) for x in k]
    rotation=np.array([[ps,-pt],[pt,ps]])
    def ratmat(x):return [S.Rational(float(y)).limit_denominator(1000000) for y in (np.array(x)@rotation).reshape(-1)]
    cutA=ratmat([[36,0],[0,35]]);cutR=[ratmat([[0,55],[-4,0]]),ratmat([[1,0],[0,-2]])]
    bounds,gap=support_gap(k,cutA,cutR)
    print('candidate',list(map(str,av)),'gap',float(gap),flush=True)
    if gap<=0:continue
    mat=H[0].subs(dict(zip(vv,k)))+t*H[1].subs(dict(zip(vv,k)))+t*t*H[2].subs(dict(zip(vv,k)))
    minors=[S.factor(mat[:j,:j].det(method='domain-ge')) for j in range(1,5)];checks=[];good=True
    for j,poly in enumerate(minors,1):
        poly=S.Poly(poly,t);power=0
        while poly.nth(0)==0:poly=poly.exquo(S.Poly(t,t));power+=1
        roots=S.polys.polytools.count_roots(poly,-S.oo,S.oo)
        passed=power%2==0 and roots==0 and poly.eval(0)>0
        checks.append([j,power,poly.degree(),int(roots),bool(passed)]);good &= bool(passed)
    print('ROC',good,checks,flush=True)
    if not good:continue
    A0=av+[S.Integer(1)];s2=av[1]**2+1
    bc=S.factor(-(av[2]+av[0]*av[1])/s2);dc=S.factor((av[1]*av[2]-av[0])/s2)
    out={'parameters':list(map(str,av)),'A0':list(map(str,A0)),'K_coefficients':list(map(str,k)),
         'canonical_zero':[str(bc),str(dc)],'canonical_kernel':['0','0',str(av[1]),'0','0','1'],
         'support_upper':str(bounds[0]),'support_lower':str(bounds[1]),'nonpc_gap':str(gap),
         'support_A':list(map(str,cutA)),'support_Rplus':list(map(str,cutR[0])),'support_Rminus':list(map(str,cutR[1])),
         'principal_minors':list(map(str,minors)),'checks':checks,'seconds':time.perf_counter()-start,
         'scope':'Exact global ROC and non-PC; exposed extremality follows from rank five. QC has not been established by this acquisition.'}
    (here/'generic_nonpc_ray.json').write_text(json.dumps(out,indent=2)+'\n')
    print('saved generic non-PC exposed ray',out['seconds'],flush=True);break
else:raise ValueError('No exact candidate admitted')
