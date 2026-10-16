"""Original fixed finite-window matrix checks; no optimization or acquired code."""
import numpy as np
import json

def evolve(h):
    w,v=np.linalg.eigh(h)
    return (v*np.exp(-1j*w))@v.conj().T

def F(a,b,eta):
    p=np.sin(min(a,np.pi/2))**2;q=np.sin(min(b,np.pi/2))**2
    z=eta*np.sqrt(p*q*(1-p)*(1-q));Q=p+q-p*q
    x=1. if p*q==0 else min(1.,z/(p*q))
    return Q-p*q*x*x+2*z*x

z=np.diag([1.,-1.,-1.]);v0=np.array([1.,0.,0.])
Hpre=np.array([[0,0,1],[0,0,0],[1,0,0]],complex)
Hpost=np.array([[0,1,0],[1,0,0],[0,0,0]],complex)
Hw=np.array([[0,1,1j],[1,0,0],[-1j,0,0]],complex)/np.sqrt(2)
assert abs(np.linalg.norm(Hw,2)-1)<1e-14
cases=[(np.pi/6,np.pi/6,0.,[0.,np.pi]),
       (np.pi/6,np.pi/6,.05,[0.,np.pi]),
       (.2,.4,.3,[0.,np.pi]),
       (.3,.2,.08,[0.,np.pi/2]),
       (.7,.6,.8,[0.,np.pi]),
       (0.,0.,.1,[0.,np.pi])]
rows=[]
for a,b,c,phases in cases:
    pre=evolve(a*Hpre);post=evolve(b*Hpost)
    actual=np.concatenate([post@evolve(c*Hw+phi*z/2)@pre@v0 for phi in phases])/np.sqrt(len(phases))
    ref=np.concatenate([post@evolve(phi*z/2)@pre@v0 for phi in phases])/np.sqrt(len(phases))
    actual=actual/np.linalg.norm(actual);ref=ref/np.linalg.norm(ref)
    overlap=np.vdot(ref,actual)
    chord=np.linalg.norm(actual-np.exp(1j*np.angle(overlap))*ref)
    angle=2*np.arcsin(min(chord/2,1.))
    pa=sum(abs(actual[k])**2 for k in range(len(actual)) if k%3!=0)
    pr=sum(abs(ref[k])**2 for k in range(len(ref)) if k%3!=0)
    eta=abs(np.mean(np.exp(-1j*np.array(phases))))
    single=F(a,b,eta)
    bound=np.sin(min(np.arcsin(np.sqrt(single))+c,np.pi/2))**2
    assert angle<=c+1e-12
    assert pr<=single+1e-12
    assert pa<=bound+1e-12
    rows.append(dict(a=a,b=b,c=c,eta=eta,p_actual=float(pa),p_reference=float(pr),reference_F=float(single),angle=float(angle),bound=float(bound)))
print(json.dumps({'fixed_cases':rows,'maximum_angle_minus_charge':max(r['angle']-r['c'] for r in rows),
                  'maximum_probability_minus_bound':max(r['p_actual']-r['bound'] for r in rows)},indent=2))
