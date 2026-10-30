"""Conventional informed optimal control for the projected contact fixture.

This gives an ordinary controller the same occupation-dependent hopping
identified by orbital_remainder.py. Positive tunnelling and signed scalar
detuning are legal. It is a numerical controller, not a certified physical
program or a full multiorbital simulation.
"""
import json
import sys
import time
from pathlib import Path
import numpy as np
from scipy.linalg import eigh,expm,expm_frechet
from scipy.optimize import least_squares
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'p2_physical_bridge'))
from orbital_echo import fermion_ops


def run():
    c=fermion_ops(4); n=[a.conj().T@a for a in c];I=np.eye(16)
    D=n[0]@n[1]+n[2]@n[3]; Z=(n[0]+n[1]-n[2]-n[3])/2
    K=sum(c[s].conj().T@c[2+s]+c[2+s].conj().T@c[s] for s in range(2))
    ev,vec=eigh(np.array([[1.,.5],[.5,20.75]]));eta=float(abs(vec[0,0]))
    ce=[c[k]@(I+(eta-1)*n[k^1]) for k in range(4)]
    Ke=sum(ce[s].conj().T@ce[2+s]+ce[2+s].conj().T@ce[s] for s in range(2))
    target=expm(1j*np.pi*K/4)
    T=12*np.pi;segments=16;dt=T/segments
    cache={};calls=0
    def both(x):
        nonlocal calls
        if 'x' in cache and np.array_equal(x,cache['x']):return cache['r'],cache['j'],cache['u']
        calls+=1
        us=[];dug=[];dud=[]
        for k in range(segments):
            a=-1j*dt*(D-x[k]*Ke+x[segments+k]*Z)
            u=expm(a);us.append(u)
            dug.append(expm_frechet(a,1j*dt*Ke,compute_expm=False))
            dud.append(expm_frechet(a,-1j*dt*Z,compute_expm=False))
        before=[I]
        for u in us:before.append(u@before[-1])
        after=[None]*(segments+1);after[segments]=I
        for k in reversed(range(segments)):after[k]=after[k+1]@us[k]
        delta=before[-1]-target;r=np.r_[delta.real.ravel(),delta.imag.ravel()]
        cols=[]
        for deriv in [dug,dud]:
            for k in range(segments):
                v=after[k+1]@deriv[k]@before[k]
                cols.append(np.r_[v.real.ravel(),v.imag.ravel()])
        j=np.array(cols).T
        cache.update(x=x.copy(),r=r,j=j,u=before[-1])
        return r,j,before[-1]
    rng=np.random.default_rng(1847)
    records=[];best=None;start=time.perf_counter()
    for attempt in range(3):
        x0=np.r_[rng.uniform(.12,.45,segments),rng.uniform(-.4,.4,segments)]
        res=least_squares(lambda x:both(x)[0],x0,jac=lambda x:both(x)[1],
                          bounds=(np.r_[np.zeros(segments),-np.ones(segments)],
                                  np.r_[.7*np.ones(segments),np.ones(segments)]),
                          max_nfev=220,ftol=1e-13,xtol=1e-13,gtol=1e-13)
        error=float(np.linalg.norm(both(res.x)[2]-target,2))
        row=dict(attempt=attempt,nfev=res.nfev,operator_error=error,cost=float(res.cost),
                 hopping=res.x[:segments].tolist(),detuning=res.x[segments:].tolist())
        records.append(row)
        if best is None or error<best['operator_error']:best=row
        if error<1e-8:break
    result=dict(projected_eta=eta,segments=segments,duration_Ueff_over_hbar=T,
                seconds=time.perf_counter()-start,derivative_evaluations=calls,best=best,attempts=records,
                caveats=['Projected two-orbital contact matrix-element correction only; no remaining bands, ramps or hardware bandwidth are certified.',
                         'Controller acquires eta and charging/hopping/detuning values. The calibration information is supplied, not free.',
                         'A numerical pulse improvement is not an exact root or a device advantage.'])
    Path(__file__).with_name('retune_sorter_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':run()
