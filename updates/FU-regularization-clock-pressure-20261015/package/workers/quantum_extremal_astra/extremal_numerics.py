import json, math
import numpy as np
from scipy.integrate import quad
from scipy.special import exp1
from scipy.optimize import minimize_scalar, linprog
from scipy.sparse import lil_matrix
GAMMA=0.5772156649015328606
Q=math.sqrt(2*math.pi)*math.exp(GAMMA/2)
def invd(t):
    if t==0:return 1.
    return math.exp((GAMMA+math.log(2*t)+exp1(2*t))/2)
def K(a):
    if a==1:return 0.
    b=1-a
    def f(t):
        return .5*(-math.expm1(-b*t))*(-math.expm1(-(2-b)*t))*invd(t)/t**2 if t else .5*b*(2-b)
    return quad(f,0,np.inf,epsabs=2e-10,epsrel=2e-10,limit=300)[0]
K0=K(0)
def right_step(a):
    if a==1:return 23/9
    c=1/(4*(K(a)+(1-a*a)/2))
    return 23/9-2*c*(1-a*a)**2/9

def left_step(a):
    c=1/(4*(Q*math.sqrt(1-a)+K0-K(a)+a*a/2))
    return 23/9-(8/9)*c*(a*a/2-a**4/4)

res={'K0':K0,'Q':Q,'constant_c':1/(4*K0+2),'constant_variance':right_step(0)}
res['steps']=[{'a':a,'right_variance':right_step(a),'left_variance':left_step(a)} for a in [0,.1,.2,.3,.4,.5,.6,.7,.8,.9,.95,.99,1]]
opt=minimize_scalar(left_step,bounds=(1e-6,1),method='bounded',options={'xatol':1e-12})
res['left_optimum']={'a':float(opt.x),'variance':float(opt.fun)}

def lp(dx=.02,L=16.):
    n=int(round(L/dx)); x=(np.arange(n)+.5)*dx
    rows=lil_matrix((n,n))
    def add_interval(j,a,b,scale):
        for i in range(max(0,int(a/dx)),min(n,int(b/dx)+1)):
            length=max(0.,min((i+1)*dx,b)-max(i*dx,a))
            if length: rows[j,i]+=scale*length
    for j,s in enumerate(x):
        if s>1:
            rows[j,j]-=2*(s-1)
            add_interval(j,abs(s-2),s,1.)
        else:
            rows[j,j]+=2*(1-s)
            add_interval(j,s,2-s,-1.)
    lo=np.arange(n)*dx; hi=lo+dx
    eq=(hi**2-lo**2)
    obj=(hi**4-lo**4)/6
    sol=linprog(obj,A_ub=rows.tocsr(),b_ub=np.zeros(n),A_eq=eq[None,:],b_eq=[1.],bounds=(0,None),method='highs')
    if not sol.success:return {'dx':dx,'error':str(sol.message)}
    h=sol.x
    residual=np.array(rows@h).flatten()
    support=[{'s':float(s),'h':float(hh)} for s,hh in zip(x,h) if hh>1e-4 and s<2.1]
    data={'dx':dx,'L':L,'variance':float(sol.fun),'max_constraint_residual':float(max(residual)),'eq_residual':float(eq@h-1),'central':support,'central_mass':float(np.sum(h[x<1])*dx),'tail_mass_last_2':float(np.sum(h[x>L-2])*dx)}
    np.savez(f'lp_dx_{dx}.npz',x=x,h=h,residual=residual,dual=sol.ineqlin.marginals)
    return data
res['lp']=[lp(dx) for dx in [.08,.04,.02,.01]]
with open('extremal_numerics.json','w') as f:json.dump(res,f,indent=2)
print(json.dumps({k:v for k,v in res.items() if k!='lp'},indent=2))
print(json.dumps([{k:v for k,v in r.items() if k!='central'} for r in res['lp']],indent=2))
