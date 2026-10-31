"""Whole-graph calibration of the finite-U gate after the naive pulse failed.

Exact symmetry reduction of the4900-state Hubbard Hilbert space, not a spin
projection. All charge states in the chosen pair-permutation/global-singlet
sector remain. Two pulse parameters are optimized; reported finite checks do
not claim proof of a global optimum or a perfect finite-U recurrence.
"""
import sys,time,json
from pathlib import Path
from itertools import combinations
from math import pi,sqrt
import numpy as np
from scipy.sparse import csr_matrix,diags
from scipy.linalg import eigh
from scipy.optimize import minimize,brentq
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from phase4_hubbard.check_finite_hubbard import fock_basis,hopping_matrix,hop
from phase4_exact_spin.check_hubbard_entangler import code

def permutation_basis(basis,characters):
    lookup={w:k for k,w in enumerate(basis)};seen=set();rows=[];cols=[];vals=[];col=0
    permutations=[]
    for g in range(16):
        p=list(range(8));char=1
        for j in range(4):
            if (g>>j)&1:p[2*j],p[2*j+1]=p[2*j+1],p[2*j];char*=characters[j]
        permutations.append((p,char))
    for word in basis:
        if word in seen:continue
        v={}
        occupied=[m for m in range(16) if (word>>m)&1]
        for p,char in permutations:
            moved=[2*p[m//2]+m%2 for m in occupied]
            w=sum(1<<m for m in moved);seen.add(w)
            inversions=sum(a>b for j,a in enumerate(moved) for b in moved[j+1:])
            v[w]=v.get(w,0)+char*((-1)**inversions)
        n=sqrt(sum(a*a for a in v.values()))
        if n==0:continue
        for w,a in v.items():
            if a:rows.append(lookup[w]);cols.append(col);vals.append(a/n)
        col+=1
    return csr_matrix((vals,(rows,cols)),shape=(len(basis),col),dtype=float)

def setup():
    basis=fock_basis(8,4,4);lookup={w:k for k,w in enumerate(basis)}
    bplus=fock_basis(8,5,3);lp={w:k for k,w in enumerate(bplus)}
    rows=[];cols=[];vals=[]
    for c,w in enumerate(basis):
        for i in range(8):
            h=hop(w,2*i,2*i+1)
            if h is not None:ww,sign=h;rows.append(lp[ww]);cols.append(c);vals.append(sign)
    plus=csr_matrix((vals,(rows,cols)),shape=(len(bplus),len(basis)),dtype=float)
    pb=permutation_basis(basis,[-1]*4)
    y=plus@pb;S2=(y.T@y).toarray();ev,E=eigh(S2)
    Q=pb@E[:,abs(ev)<1e-8]
    doubles=np.array([sum(((w>>(2*i))&3)==3 for i in range(8)) for w in basis])
    h0=diags(doubles,dtype=complex)
    hi=hopping_matrix(basis,list(combinations(range(4),2))+list(combinations(range(4,8),2)))
    hx=hopping_matrix(basis,[(i,j) for i in [0,1] for j in [4,5]])
    load=np.zeros(len(basis),complex);bc=code()[:,3]
    for n in range(256):
        if n.bit_count()!=4:continue
        w=sum(1<<(2*i+((n>>(7-i))&1)) for i in range(8));load[lookup[w]]=bc[n]
    v=Q.T@load
    assert np.linalg.norm(Q@v-load)<1e-12
    return dict(Q=Q,v=v,h0=np.real_if_close(Q.T@(h0@Q)),
                hi=np.real_if_close(Q.T@(hi@Q)),hx=np.real_if_close(Q.T@(hx@Q)),
                residual=float(np.linalg.norm(plus@Q)),permutation_dimension=pb.shape[1],
                singles=doubles==0)

def apply_exp(H,t,v):
    e,B=eigh(H,check_finite=False)
    return B@(np.exp(-1j*t*e)*(B.T@v))

def ramp_apply(v,h0,V,duration,steps,down=False):
    a1=(3-2*sqrt(3))/12;a2=(3+2*sqrt(3))/12
    c1=.5-sqrt(3)/6;c2=.5+sqrt(3)/6;dt=duration/steps
    for k in range(steps):
        f=lambda c:(np.cos(pi*(k+c)/(2*steps)) if down else np.sin(pi*(k+c)/(2*steps)))**2
        g1,g2=f(c1),f(c2)
        v=apply_exp(.5*h0+(a2*g1+a1*g2)*V,dt,v)
        v=apply_exp(.5*h0+(a1*g1+a2*g2)*V,dt,v)
    return v

def evaluate(m,ratio,plateau,steps=24,return_state=False):
    t=.5/sqrt(50);V=t*(m['hi']+sqrt(ratio)*m['hx'])
    v=ramp_apply(m['v'].copy(),m['h0'],V,40.,steps)
    v=apply_exp(m['h0']+V,plateau,v)
    v=ramp_apply(v,m['h0'],V,40.,steps,True)
    amp=np.vdot(m['v'],v)
    if return_state:return amp,v
    return max(0.,1-abs(amp)**2)

def main():
    begin=time.time();m=setup();t=.5/sqrt(50)
    def spectral_ratio(r):
        es=np.linalg.eigvalsh(m['h0']+t*(m['hi']+sqrt(r)*m['hx']))
        return (es[2]-es[0])/(es[1]-es[0])
    root=brentq(lambda r:spectral_ratio(r)-2,.4,1.8)
    initial=[root,100.]
    calls=[]
    def objective(x):
        if not(.2<x[0]<2 and 20<x[1]<220):return 10.+sum(x*x)
        z=evaluate(m,x[0],x[1]);calls.append((x.tolist(),z));return z
    opt=minimize(objective,initial,method='Nelder-Mead',
                 options={'xatol':1e-9,'fatol':2e-12,'maxiter':180})
    rows=[]
    for steps in [24,48,96]:
        a,v=evaluate(m,*opt.x,steps=steps,return_state=True)
        full=m['Q']@v
        rows.append(dict(steps=steps,code_reject=float(1-abs(a)**2),
                         charge_probability=float(1-np.vdot(full[m['singles']],full[m['singles']]).real),
                         amplitude=[float(a.real),float(a.imag)]))
    result=dict(full_dimension=4900,pair_permutation_dimension=m['permutation_dimension'],
                exact_reduced_dimension=len(m['v']),spin_projector_residual=m['residual'],
                U_over_J_nominal=50.,t_intra_over_U=t,
                static_low_spectral_ratio_two_cross_J_ratio=float(root),
                optimized_cross_J_ratio=float(opt.x[0]),optimized_plateau=float(opt.x[1]),
                t_cross_over_U=float(t*sqrt(opt.x[0])),ramp_time=40.,
                total_gate_duration=float(opt.x[1]+80),optimization_success=bool(opt.success),
                optimization_message=str(opt.message),objective_calls=len(calls),
                refinement=rows,wall_seconds=time.time()-begin)
    Path(__file__).with_name('hubbard_entangler_calibration_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
