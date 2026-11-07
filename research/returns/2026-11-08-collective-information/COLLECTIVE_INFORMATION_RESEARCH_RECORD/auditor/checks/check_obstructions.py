import math, json
from pathlib import Path
import numpy as np

# Independent 4x4 generator construction, spectral propagation, and direct
# observable-generator closure. Diagnostics supplement the proofs.
states=[(-1,-1),(-1,1),(1,-1),(1,1)]
index={s:i for i,s in enumerate(states)}
x=np.array([s[0] for s in states],float)
z=np.array([s[1] for s in states],float)
xz=x*z

def generator(gamma,u,hidden=True):
    Q=np.zeros((4,4))
    for i,(a,b) in enumerate(states):
        Q[i,index[(-a,b)]]=1+(u*b if hidden else 0)
        Q[i,index[(a,-b)]]=gamma
        Q[i,i]=-sum(Q[i])
    return Q

def exp_symmetric(Q,t):
    vals,vecs=np.linalg.eigh(Q)
    return (vecs*np.exp(vals*t))@vecs.T

rows=[]
for gamma in [0.0,0.1,1.0,4.0]:
    for u in [-.75,0,.5,.75]:
        Q=generator(gamma,u)
        assert np.max(np.abs(Q-Q.T))<1e-14
        assert np.max(np.abs(Q@np.ones(4)))<1e-14
        assert np.max(np.abs(Q@x-(-2*x-2*u*xz)))<1e-14
        assert np.max(np.abs(Q@xz-(-2*u*x-2*(1+gamma)*xz)))<1e-14
        p0=np.array([0,0,.5,.5])
        for t in [.01,.1,1,3,10]:
            p=p0@exp_symmetric(Q,t)
            s=math.sqrt(gamma*gamma+4*u*u)
            expected=math.exp(-(2+gamma)*t)*(math.cosh(s*t)+(gamma/s)*math.sinh(s*t)) if s else math.exp(-2*t)
            assert abs(p@x-expected)<2e-14
            assert np.min(p)>-1e-14
        rows.append({'gamma':gamma,'u':u,'symmetric':True,'closure':True})
Q=generator(.1,.75)
p0=np.array([0,0,.5,.5])
p=p0@exp_symmetric(Q,1)
gap=float(p@x-math.exp(-2))
assert gap>.17

# Positive-model robustness for long growing duration and changing controls.
rng=np.random.default_rng(20261107)
gamma=.4; gamma_hat=.401; ustar=.75; lam=2*(1-ustar)
y0=np.array([1.,.2]); y=y0.copy(); yh=y0.copy()
max_err=0.
for j in range(1000):
    u=float(rng.uniform(-ustar,ustar)); dt=float(rng.uniform(0,2))
    A=-2*np.array([[1,u],[u,1+gamma]])
    Ah=-2*np.array([[1,u],[u,1+gamma_hat]])
    assert np.max(np.linalg.eigvalsh(A))<=-lam+1e-14
    y=exp_symmetric(A,dt)@y
    yh=exp_symmetric(Ah,dt)@yh
    max_err=max(max_err,float(np.linalg.norm(y-yh)))
assert max_err<=2*math.sqrt(2)*abs(gamma-gamma_hat)/lam

# Detector parity formula by exhaustive finite models, including count law.
parity_rows=[]
for n in range(1,9):
    v=.6; err=(1-v)/2
    count=1<<n
    labels=np.array([(-1)**i.bit_count() for i in range(count)])
    pplus=(1+labels)/count
    pminus=(1-labels)/count
    channel=np.zeros((count,count))
    for i in range(count):
        for j in range(count):
            d=(i^j).bit_count()
            channel[i,j]=err**d*(1-err)**(n-d)
    op=pplus@channel; om=pminus@channel
    predicted=(1+(v**n)*labels)/count
    assert max(abs(op-predicted))<1e-14
    tv=float(np.sum(abs(op-om))/2)
    cp=np.zeros(n+1); cm=np.zeros(n+1)
    for i in range(count): cp[i.bit_count()]+=op[i]; cm[i.bit_count()]+=om[i]
    ctv=float(np.sum(abs(cp-cm))/2)
    assert abs(tv-v**n)<1e-14 and abs(ctv-tv)<1e-14
    parity_rows.append({'n':n,'tv':tv,'count_tv':ctv,'predicted':v**n})

thermo_gap=3/8*4**(-1/3)
rare_gap=math.exp(-2)-math.exp(-4)
result={'status':'PASS','four_state_cases':len(rows),'four_state_gap':gap,'thermodynamic_gap':thermo_gap,'rare_clock_gap':rare_gap,'positive_lift_max_error':max_err,'positive_lift_bound':2*math.sqrt(2)*abs(gamma-gamma_hat)/lam,'parity_cases':parity_rows,'scope':'Exact finite diagnostics supplement the analytic proofs; no physical experiment or novelty claim.'}
out=Path(__file__).with_name('check_obstructions_result.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
