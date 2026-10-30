"""Numerical stress test of the positive-operator force theorem.

H_q(t) = H_M(t) + p^2/(2m) - q*x*G_M(t), q=+1 or -1.
The force operator G_M is positive and need not commute with H_M or
with its values in other intervals.  This script uses a convergent
Fourier/Strang discretization, not an interval certificate.  The support
theorem itself is proved by a spectral/Trotter argument in DERIVATION.md.

Only a prepared meter wave packet is supplied.  The entire internal
memory input basis is propagated, so the displayed measurement effects
are operators on the memory, not averages over selected memory states.
"""
import math
import numpy as np
from scipy.linalg import expm

def hermitian(rng,d):
    a = rng.normal(size=(d,d)) + 1j*rng.normal(size=(d,d))
    a = (a+a.conj().T)/2
    return a/np.linalg.norm(a,2)

def make_intervals(seed=1727, d=4, chunks=8):
    rng = np.random.default_rng(seed)
    out=[]
    for j in range(chunks):
        h=40*hermitian(rng,d)
        v,_=np.linalg.qr(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)))
        g=v@np.diag(np.linspace(.75,1.75,d))@v.conj().T
        out.append((.25,h,g))
    return out

def simulate(intervals, sign=1, grid=4096, halfwidth=8., substeps=16,
             pwidth=1., mass=3.):
    d=len(intervals[0][1]); dp=2*halfwidth/grid
    p=(np.arange(grid)-grid//2)*dp
    # Conjugate x values for scipy/numpy's Fourier convention.
    x=2*math.pi*np.fft.fftfreq(grid,d=dp)
    packet=np.zeros(grid)
    mask=np.abs(p)<pwidth
    packet[mask]=np.cos(math.pi*p[mask]/(2*pwidth))**4
    packet/=np.linalg.norm(packet)
    psi=np.einsum('ab,p->apb',np.eye(d),packet).astype(complex)
    for duration,h,g in intervals:
        dt=duration/substeps
        uh=expm(-.5j*dt*h)
        vals,v=np.linalg.eigh(g)
        kinetic=np.exp(-.25j*dt*p*p/mass)
        translation=np.exp(-1j*sign*vals[:,None]*x[None,:]*dt)
        for _ in range(substeps):
            psi=np.einsum('ab,bpc->apc',uh,psi)*kinetic[None,:,None]
            psi=np.einsum('ab,bpc->apc',v.conj().T,psi)
            psi=np.fft.fft(psi,axis=1)
            psi*=translation[:,:,None]
            psi=np.fft.ifft(psi,axis=1)
            psi=np.einsum('ab,bpc->apc',v,psi)
            psi=np.einsum('ab,bpc->apc',uh,psi)*kinetic[None,:,None]
    def effect(selection):
        w=psi[:,selection,:].reshape(-1,d)
        return w.conj().T@w
    wrong=effect(sign*p<=0)
    total=effect(np.ones(grid,dtype=bool))
    duration=sum(t for t,_,_ in intervals)
    gmin=min(np.linalg.eigvalsh(g)[0] for _,_,g in intervals)
    gmax=max(np.linalg.eigvalsh(g)[-1] for _,_,g in intervals)
    a,b=-pwidth+gmin*duration,pwidth+gmax*duration
    outside=effect((sign*p<a-2*dp)|(sign*p>b+2*dp))
    return {'sign':sign,'grid':grid,'substeps_per_interval':substeps,
            'duration':duration,'g_min':float(gmin),'g_max':float(gmax),
            'predicted_signed_momentum_interval':[float(a),float(b)],
            'worst_memory_wrong_readout_probability':float(np.linalg.eigvalsh(wrong)[-1]),
            'outside_predicted_support':float(np.linalg.eigvalsh(outside)[-1]),
            'isometry_residual':float(np.linalg.norm(total-np.eye(d),2)),
            'max_bath_norm':max(float(np.linalg.norm(h,2)) for _,h,g in intervals),
            'max_bath_force_commutator':max(float(np.linalg.norm(h@g-g@h,2)) for _,h,g in intervals)}

def failure_examples():
    # Positive expectation in one memory state cannot certify the operator gap.
    good=np.diag([1.,1.]); hidden_bad=np.diag([1.,-1.])
    safe=np.array([1.,0.]); hidden=np.array([0.,1.])
    return {'safe_state_good_mean':float(safe@good@safe),
            'safe_state_bad_mean':float(safe@hidden_bad@safe),
            'hidden_state_bad_mean':float(hidden@hidden_bad@hidden),
            'dark_state_velocity':0.0}

if __name__=='__main__':
    import json
    intervals=make_intervals()
    print(json.dumps([simulate(intervals,q) for q in [1,-1]],indent=2))
