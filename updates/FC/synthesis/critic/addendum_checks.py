"""Independent fixtures for FC synthesis. No producer/other-worker imports."""
from fractions import Fraction as F
from itertools import product
from math import factorial as fac
from pathlib import Path
import json, math
import numpy as np
from scipy.linalg import eigh, expm
from scipy.integrate import quad
from scipy.special import expit
from scipy.stats import norm

result={"status":"PASS","scope":"Exact finite rational and double-precision diagnostic fixtures, not external proof validation"}

def ebeta(n,s,p):
    return F(fac(s)*fac(n-s),fac(n+1))/(p**s*(1-p)**(n-s))

beta_checks=0
for p in (F(1,7),F(2,5),F(1,2),F(4,5)):
    for n in range(11):
        for s in range(n+1):
            assert p*ebeta(n+1,s+1,p)+(1-p)*ebeta(n+1,s,p)==ebeta(n,s,p)
            beta_checks+=1
    # Exact probability of first crossing up to a finite horizon.
    alpha=F(1,4); live={0:F(1)}; crossed=F(0)
    for n in range(1,13):
        next_live={}
        for s,w in live.items():
            for x,px in ((0,1-p),(1,p)):
                ss=s+x; ww=w*px
                if ebeta(n,ss,p)>=1/alpha: crossed+=ww
                else: next_live[ss]=next_live.get(ss,F(0))+ww
        live=next_live
        assert crossed<=alpha and crossed+sum(live.values())==1
result['exact_beta_martingale_cases']=beta_checks

def edir(counts,p):
    n=sum(counts); k=len(counts)
    return F(fac(k-1)*math.prod(fac(x) for x in counts),fac(n+k-1))/math.prod(x**y for x,y in zip(p,counts))

p=(F(1,7),F(2,7),F(4,7)); dirs=0
for counts in product(range(7),repeat=3):
    if sum(counts)>6: continue
    expected=F(0)
    for i,pp in enumerate(p):
        cc=list(counts);cc[i]+=1;expected+=pp*edir(cc,p)
    assert expected==edir(counts,p);dirs+=1
result['exact_dirichlet_martingale_cases']=dirs

opt=0
grid=[F(i,6) for i in range(7)]
for l in grid:
    for h in grid:
        if l>h:continue
        for mass in grid[1:]:
            feasible=[]
            for p1 in grid:
                if not l<=p1<=h:continue
                for w1 in grid:
                    w0=mass-w1
                    if 0<=w0<=1-p1 and 0<=w1<=p1:feasible.append(w1)
            left=max(F(0),l-(1-mass));right=min(mass,h)
            assert min(feasible)==left and max(feasible)==right
            for u0,u1 in ((F(1),F(3)),(F(3),F(1)),(F(2),F(2))):
                direct=min((mass-w1)*u0+w1*u1 for w1 in feasible)
                endpoint=left if u1>=u0 else right
                assert direct==mass*u0+endpoint*(u1-u0);opt+=1
result['exact_binary_latent_optimization_cases']=opt

rare=[]
for m in range(2,21):
    theta=F(1,2**m);A0=2-theta;A1=3-2*theta
    assert A1/A0>=F(10,7)
    q0=1/A0;q1=2/A1
    assert q1-q0==1/(A0*A1) and q1-q0>=F(1,6)
    for cap in (1,3,9):
        def stopped(p):
            return [(1-p)**(j-1)*p for j in range(1,cap+1)]+[(1-p)**cap]
        a,b=stopped(theta),stopped(2*theta)
        tv=sum(abs(x-y) for x,y in zip(a,b))/2
        en=(1-(1-theta)**cap)/theta
        assert tv<=theta*en
    rare.append({"m":m,"theta_denominator":theta.denominator,"ratio_lower_holds":True,"tilted_separation_lower_holds":True})
result['exact_rare_overlap_cases']=rare

rng=np.random.default_rng(31854)
def gibbs(H,beta):
    E,U=eigh(H);x=np.exp(-beta*(E-E[0]));rho=(U*(x/x.sum()))@U.conj().T
    return rho,-beta*E[0]+math.log(x.sum())
def logmat(A):
    e,u=eigh(A);assert e.min()>0
    return (u*np.log(e))@u.conj().T
def rel(A,B):
    return np.trace(A@(logmat(A)-logmat(B))).real
def f(x):
    return .5*(1+x)*math.log1p(x)+(.5*(1-x)*math.log1p(-x) if x<1 else 0.)

activity=[]
for t in range(80):
    k=2+t%3;n=2*k+1;labels=np.arange(n)%k;beta=float(rng.uniform(.1,1.4))
    A=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));H=(A+A.conj().T)/3
    D=H*(labels[:,None]==labels[None,:]);T=H-D
    rho,lz=gibbs(H,beta);rhoD,ld=gibbs(D,beta)
    sigma=rho*(labels[:,None]==labels[None,:]);a=-np.trace(rho@T).real;K=np.linalg.norm(T,2)
    entropy1=rel(rho,sigma);entropy2=rel(sigma,rhoD)
    identity=beta*a-entropy1-entropy2
    upper=beta*a-f(a/K)
    assert abs(identity-(lz-ld))<2e-11
    assert entropy1+1e-11>=f(a/K)
    assert -1e-11<=lz-ld<=upper+1e-11
    assert upper<=min(beta*a,math.log(math.cosh(beta*K)))+1e-11
    activity.append({"test":t,"identity_error":abs(identity-(lz-ld)),"activity_bound_slack":upper-(lz-ld),"entropy_POVM_slack":entropy1-f(a/K)})
result['activity_entropy_diagnostics']=activity
for x in (.1,.5,1.,3.):
    aa=math.tanh(x)
    assert abs(x*aa-f(aa)-math.log(math.cosh(x)))<1e-12
result['resonant_activity_equalities']=4

def h2(p):
    return -(p*math.log(p) if p>0 else 0)-((1-p)*math.log1p(-p) if p<1 else 0)
compression=[]
for t in range(48):
    n=3+t%5;labels=np.arange(n)%2;beta=float(rng.uniform(.1,1.3))
    A=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
    H=(A+A.conj().T)/4+np.diag((2*labels-1)*rng.uniform(-2,2))
    mask=labels[:,None]==labels[None,:];D=H*mask;T=H-D
    B=T*((labels[:,None]==0)&(labels[None,:]==1));K=np.linalg.norm(T,2)
    P0=np.diag(labels==0);P1=np.eye(n)-P0
    choi=np.block([[P0,B/K],[B.conj().T/K,P1]])
    assert eigh(choi,eigvals_only=True).min()>-1e-12
    rho,lz=gibbs(H,beta);sigma=rho*mask;_,ld=gibbs(D,beta)
    p=float(np.trace(rho@P0).real);a=-float(np.trace(rho@T).real);x=a/K
    w=np.trace(rho@B)/K
    compressed=np.array([[p,np.conj(w)],[w,1-p]])
    assert abs(2*w.real+a/K)<1e-12 and eigh(compressed,eigvals_only=True).min()>-1e-12
    assert x<=2*math.sqrt(p*(1-p))+1e-12
    radius=min(1.,math.sqrt((2*p-1)**2+x*x));dp=h2(p)-h2((1+radius)/2)
    assert rel(rho,sigma)+1e-11>=rel(compressed,np.diag([p,1-p]))
    assert rel(compressed,np.diag([p,1-p]))+1e-11>=dp
    assert dp+1e-11>=f(x)
    assert lz-ld<=beta*a-dp+1e-11
    compression.append({'test':t,'p':p,'activity_scaled':x,'penalty':dp,'older_penalty':f(x),'partition_slack':beta*a-dp-(lz-ld)})
result['binary_UCP_compression_models']=compression
bias_cases=0
for x in (.001,.01,.1,.2,.5,.9):
    values=[]
    for b in np.linspace(0,math.sqrt(1-x*x),17):
        p=(1+b)/2;r=min(1.,math.sqrt(b*b+x*x));values.append(h2(p)-h2((1+r)/2))
    assert np.diff(values).min()>-1e-12 and values[0]+1e-12>=f(x)
    bias_cases+=len(values)
result['binary_bias_order_cases']=bias_cases

# Exact rational sign proof for the shared-latent control; no LP optimum used.
assert sum(F(16)**j/fac(j) for j in range(30))>10**6
ratio_upper=F(100,103)+F(8,10**6)
assert F(101,100)*ratio_upper<1
coef_gap=F(97,400)-(F(1,4)-F(1,101))
assert coef_gap*10**6>F(3,4)
graph=(math.exp(F(3,25))+3*math.exp(F(-1,25)))/4
assert graph<1.01
v0=np.array([8.,8.,-8.,8.]);v1=np.array([7.5,8.5,-7.97,9.]);cap=1.01/4
vertices=[]
for free in range(4):
    for fixed in product((0.,cap),repeat=3):
        q=np.zeros(4);q[np.arange(4)!=free]=fixed;q[free]=1-sum(fixed)
        if -1e-12<=q[free]<=cap+1e-12:vertices.append(q)
ratios=[(q@np.exp(-v1))/(q@np.exp(-v0)) for q in vertices]
low=-math.log(1.01*max(ratios));high=-math.log(min(ratios)/1.01)
def interval(v):
    u=np.exp(-v);p=np.full(4,.25);mass=1/1.01;kept=0.
    for i in np.argsort(u):
        take=min(p[i],mass);kept+=take*u[i];mass-=take
    return -math.log(p@u),-math.log(kept)
l0,h0=interval(v0);l1,h1=interval(v1)
assert low>0 and l1-h0<0<h1-l0
result['shared_latent_control']={'exact_rational_strict_sign':True,'vertex_count':len(vertices),'contrast_interval_float':[low,high],'independent_subtraction_float':[l1-h0,h1-l0]}

# Collision overlap and quartic moment: raw-output testing contract only.
collision=[]
for a,b,p in ((1.,1.1,.5),(1.,1.4,.25),(1.,3.,.5),(1.,2.,.8)):
    mu=(1-p)*a+p*b;variance=p*(1-p)*(b-a)**2;D=max(mu-a,b-mu);q=(D/mu)**2
    assert q<1
    overlap=lambda s,u:(1-(s-mu)*(u-mu)/mu**2)**-1.5
    chi=(1-p)**2*overlap(a,a)+2*p*(1-p)*overlap(a,b)+p*p*overlap(b,b)-1
    A=((1-q)**-1.5-1-1.5*q)/(q*q);bound=A*(variance/mu**2)**2
    assert chi<=bound+1e-12 and chi>0
    gaussian=lambda s,x:(2*math.pi*s)**-1.5*math.exp(-x*x/(2*s))
    integrand=lambda x:4*math.pi*x*x*((1-p)*gaussian(a,x)+p*gaussian(b,x)-gaussian(mu,x))**2/gaussian(mu,x) if x<25 else 0.
    numeric,err=quad(integrand,0,25,epsabs=1e-12)
    assert abs(numeric-chi)<1e-10
    collision.append({'a':a,'b':b,'p':p,'chi2':chi,'bound':bound,'quadrature_error':abs(numeric-chi)})
mom=lambda j:math.prod(3+2*i for i in range(j))
assert sum(coef*mom(j) for j,coef in enumerate((225,-300,130,-20,1)))==120
result['collision_information_checks']=collision

# Independent conditional Gaussian response tests; no Te covariance asserted.
roc=[]
for d in (.1,.5,1.,3.):
    for slope,bias in ((.5,-2),(1.,0),(4.,2),(7.,-4)):
        g=lambda x:expit(slope*x+bias)
        pt=quad(lambda x:norm.pdf(x-d)*g(x),-12,12,epsabs=1e-12)[0]
        pu=quad(lambda x:norm.pdf(x)*g(x),-12,12,epsabs=1e-12)[0]
        lower=norm.cdf(norm.ppf(pt)-d)
        assert pu+1e-10>=lower
        roc.append({'d':d,'target':pt,'unwanted':pu,'lower':lower})
result['Gaussian_smooth_response_checks']=roc

bellman=0
for n in range(1,13):
    for m in (1,2,5):
        for R in (F(1,2),F(1),F(10),F(2291053,5000)):
            values=[F(1)]
            for k in range(1,n+1):values.append(values[-1]*k*R/(k*R+m))
            for relative in (F(0),F(1,3),F(1)):
                ru=F(3,7);rt=relative*R*ru
                gen=n*rt*(values[n-1]-values[n])-m*ru*values[n]
                assert gen<=0 and (gen==0)==(relative==1)
                bellman+=1
result['exact_global_write_generator_cases']=bellman
T,a=F(2),F(1,10)
actual=((T+a)**3-(T-a)**3)/2
linear=3*T*T*a
assert actual-linear==a**3
result['finite_angle_scope_falsifier']={'nonlinear_response':'g(T)=T^3','exact_odd_difference':str(actual),'first_order_only':str(linear),'missing_cubic_term':str(actual-linear),'repair':'Declare linearized coefficients or retain the odd/even remainders; does not refute first-order kinematic benchmark.'}

Path('addendum_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','beta_martingale_cases':beta_checks,'dirichlet_cases':dirs,'latent_optimization_cases':opt,'rare_family_cases':len(rare),'activity_models':len(activity),'binary_UCP_models':len(compression),'binary_bias_cases':bias_cases,'shared_control_exact_sign':True,'collision_information_fixtures':len(collision),'Gaussian_response_fixtures':len(roc),'exact_global_write_generator_fixtures':bellman,'finite_angle_scope_falsifier':True},indent=2))
