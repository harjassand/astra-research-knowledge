#!/usr/bin/env python3
"""Finite population checks; no acquired data, apparatus or hydrodynamic claim.
Run with Python + NumPy: python3 check_event_memory.py
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib, json, math, platform
import numpy as np

N, MASS = 5, 2
EDGES = [(0,1,F(1),0),(1,2,F(1),0),(2,0,F(1),0),
         (0,3,F(2),1),(3,4,F(2),1),(4,0,F(2),1)]
OCCS = [sum(1 << i for i in cc) for cc in combinations(range(N), MASS)]

def delta(mask,x,y):
    return ((mask >> x)&1)-((mask >> y)&1)

def swapped(mask,x,y):
    return mask ^ (1 << x) ^ (1 << y)

def build(alpha,mode,hidden_prefactor,force=0.):
    nb=2 if mode=='separate' else 1
    states=list(product(OCCS,product((-1,1),repeat=nb)))
    index={x:i for i,x in enumerate(states)}
    events=[[] for _ in states]; activity=np.zeros(len(states))
    for ix,(mask,bits) in enumerate(states):
        for x,y,c,ch in EDGES:
            d=delta(mask,x,y)
            if not d: continue
            sign=-1 if mode=='opposed' and ch==1 else 1
            ib=ch if mode=='separate' else 0
            u=bits[ib]; bn=list(bits); bn[ib]*=-1
            to=index[(swapped(mask,x,y),tuple(bn))]
            rate=float(c)*(1+alpha*u*sign*d)*math.exp(force*sign*d)
            inc=np.zeros(2); inc[ch]=d
            if rate>0: events[ix].append((to,rate,inc,True))
            activity[ix]+=float(c)
        # Arbitrary-to-the-controller rates on unselected reversible channels.
        for x,y in [(1,3),(2,4)]:
            if not delta(mask,x,y): continue
            other=swapped(mask,x,y)
            code=(min(mask,other)*13+max(mask,other)*7)%11
            rate=hidden_prefactor*(1+code)/7.
            if rate: events[ix].append((index[(other,bits)],rate,np.zeros(2),False))
    L=np.zeros((len(states),len(states)))
    for ix,row in enumerate(events):
        for jx,rate,_,_ in row: L[ix,jx]+=rate; L[ix,ix]-=rate
    pi=np.ones(len(states))/len(states)
    if force:
        pi=np.array([np.prod([1-alpha*u*math.tanh(force) for u in bits])
                     /len(states) for _,bits in states])
    return states,L,pi,events,activity

def diffusion(L,pi,events):
    drift=np.array([sum((r*d for _,r,d,_ in row),start=np.zeros(2)) for row in events])
    f=np.linalg.lstsq(np.vstack((L,pi)),
                      np.vstack((-drift,np.zeros((1,2)))),rcond=1e-12)[0]
    C=np.zeros((2,2))
    for ix,row in enumerate(events):
        for jx,rate,inc,_ in row:
            d=inc+f[jx]-f[ix]; C+=pi[ix]*rate*np.outer(d,d)
    return C,float(np.max(np.abs(L@f+drift)))

def exact_checks():
    count=0
    for mask,u,alpha in product(OCCS,(-1,1),(F(0),F(3,5),F(1))):
        balance=a=drift=bracket=F(0)
        for x,y,c,_ in EDGES:
            d=delta(mask,x,y); balance+=c*d
            if not d: continue
            a+=c; rate=c*(1+alpha*u*d); corr=d-alpha*u
            drift+=rate*corr; bracket+=rate*corr*corr
            assert rate==c*(1+alpha*(-u)*(-d))
            assert d==corr+alpha*F(u-(-u),2)
            if alpha==1 and rate>0: assert corr==0
        assert balance==drift==0
        assert bracket==(1-alpha*alpha)*a
        count+=1
    return count

def cell_check(alpha,h,k):
    states,L,pi,events,activity=build(alpha,'shared',17.,h)
    B=np.array([[-math.cosh(h)+alpha*math.sinh(h),
                 math.cosh(h+k)-alpha*math.sinh(h+k)],
                [math.cosh(h+k)+alpha*math.sinh(h+k),
                 -math.cosh(h)-alpha*math.sinh(h)]])
    eig,vec=np.linalg.eig(B); v=vec[:,int(np.argmax(eig.real))].real
    v*=np.sign(v.sum()); v/=v.min()
    lifted=np.array([v[0 if bits[0]==-1 else 1] for _,bits in states])
    Lk=L.copy()
    for ix,row in enumerate(events):
        for jx,rate,inc,selected in row:
            if selected: Lk[ix,jx]+=rate*math.expm1(k*float(inc.sum()))
    b=-math.cosh(h)+math.sqrt(alpha**2*math.cosh(h)**2
                            +(1-alpha**2)*math.cosh(h+k)**2)
    response=sum(pi[ix]*sum(rate*inc.sum() for _,rate,inc,_ in row)
                 for ix,row in enumerate(events))
    expected=(1-alpha**2)*float(pi@activity)*math.sinh(h)
    return {'alpha':alpha,'h':h,'k':k,
            'stationary_residual':float(np.max(np.abs(pi@L))),
            'cell_identity_residual':float(np.max(np.abs(Lk@lifted-b*activity*lifted))),
            'response':response,'response_formula':expected,'response_error':abs(response-expected)}

def main():
    out={'scope':'Population generators, not acquired data or physical experiments.',
         'python':platform.python_version(),'numpy':np.__version__,'sites':N,'particles':MASS,
         'exact_rational_states':exact_checks(),'covariance_cases':[],'spectral_cell_cases':[]}
    for alpha,mode,hidden in product((0.,.6,1.),('shared','opposed','separate'),(0.,.03125,32.)):
        states,L,pi,events,activity=build(alpha,mode,hidden)
        C,res=diffusion(L,pi,events)
        v=np.array([1.,-1. if mode=='opposed' else 1.]); measured=float(v@C@v)
        expected=(1-alpha**2)*float(pi@activity)
        eig=np.linalg.eigvalsh(L); nz=-eig[eig < -1e-9]
        case={'alpha':alpha,'mode':mode,'hidden_prefactor':hidden,'joint_states':len(states),
              'covariance':C.tolist(),'controlled_combination_variance':measured,
              'exact_combination_formula':expected,'formula_error':abs(measured-expected),
              'detailed_balance_residual':float(np.max(np.abs(L-L.T))),
              'poisson_residual':res,'nullity':int(np.sum(np.abs(eig)<=1e-9)),
              'smallest_positive_relaxation_rate':float(nz.min())}
        assert case['formula_error'] < 1e-9 and res < 1e-9
        assert case['detailed_balance_residual'] < 1e-12
        out['covariance_cases'].append(case)
    for alpha,h,k in product((0.,.6,1.),(-.4,0.,.7),(-.6,.3)):
        case=cell_check(alpha,h,k)
        assert case['stationary_residual'] < 1e-12
        assert case['cell_identity_residual'] < 1e-10 and case['response_error'] < 1e-12
        out['spectral_cell_cases'].append(case)
    out['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    dest=Path(__file__).with_name('EVENT_MEMORY_CHECK.json')
    dest.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'exact_rational_states':out['exact_rational_states'],
                      'covariance_cases':len(out['covariance_cases']),
                      'spectral_cell_cases':len(out['spectral_cell_cases']),
                      'max_variance_error':max(x['formula_error'] for x in out['covariance_cases']),
                      'output':str(dest)},indent=2))

if __name__=='__main__': main()
