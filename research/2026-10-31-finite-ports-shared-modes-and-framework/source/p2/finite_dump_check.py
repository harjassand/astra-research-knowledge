"""Full one-excitation simulation: local taps and finite fresh drains.

All retained-memory amplitudes are propagated. No bath state is sampled.
The two data atoms have levels 0,1,e. Optical locations are vacuum,
safe, risky, followed by a distinct outgoing location for every drain.
The state is an isometry from the initial M to data x optics x M.
"""
import math
import numpy as np
from scipy.linalg import eigh
from finite_ports import tap, norm, finite_dump_bell_bound

def hermitian(rng,d):
    z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
    h=(z+z.conj().T)/2
    return h/max(norm(h),1e-12)

def positive(rng,d,lo=1.,hi=2.):
    h=hermitian(rng,d)
    vals,vec=eigh(h)
    vals=np.linspace(lo,hi,d) if d>1 else np.array([lo])
    return (vec*vals)@vec.conj().T

def drain_map(collisions):
    """Residual R, emitted E, free V and the normalized emitted map."""
    d=len(collisions[0][0]); r=np.eye(d,dtype=complex)
    free=r.copy(); emitted=[]
    for v,a,b in collisions:
        emitted=[v@e for e in emitted]
        emitted.append(b@r)
        r=a@r; free=v@free
    e=np.vstack(emitted)
    vals,vec=eigh(np.eye(d)-r.conj().T@r)
    inverse_root=(vec*(1/np.sqrt(vals)))@vec.conj().T
    normalized=e@inverse_root
    actual=np.vstack([r,e]); ideal=np.vstack([np.zeros_like(r),normalized])
    return {'free':free,'residual':r,'emitted':e,'normalized':normalized,
            'isometry_error':norm(actual-ideal),
            'isometry_defect':norm(actual.conj().T@actual-np.eye(d))}

def memory_action(state,v):
    return np.einsum('ab,ijkbc->ijkac',v,state,optimize=True)

def rotate(state,theta):
    old_s=state[:,:,1].copy(); old_r=state[:,:,2].copy()
    state[:,:,1]=math.cos(theta)*old_s-math.sin(theta)*old_r
    state[:,:,2]=math.sin(theta)*old_s+math.cos(theta)*old_r
    return state

def apply_tap(state,which,v,a,b):
    old=state; out=memory_action(old,v)
    for other in range(3):
        photo=(1,other,2) if which==0 else (other,1,2)
        excited=(2,other,0) if which==0 else (other,2,0)
        p=old[photo]; x=old[excited]
        out[photo]=a@p+b@x
        out[excited]=b@p+a@x
    return out

def apply_drain(state,which,dm,first_location,ideal=False):
    old=state; out=memory_action(old,dm['free'])
    d=state.shape[-2]
    emit=dm['normalized'] if ideal else dm['emitted']
    for other in range(3):
        exc=(2,other,0) if which==0 else (other,2,0)
        x=old[exc]
        out[exc]=np.zeros_like(x) if ideal else dm['residual']@x
        for j in range(len(emit)//d):
            loc=(0,other,first_location+j) if which==0 else (other,0,first_location+j)
            # Every newly supplied drain mode is initially vacuum.
            assert np.linalg.norm(old[loc])<1e-13
            out[loc]+=emit[j*d:(j+1)*d]@x
    return out

def simulate(n=16,m=6,d=2,bath_scale=30.,seed=915):
    rng=np.random.default_rng(seed); tau=math.pi/3
    shape=(3,3,3+2*n*m,d,d)
    actual=np.zeros(shape,complex)
    for i in range(2):
        for j in range(2): actual[i,j,1]=np.eye(d)/2
    ideal=actual.copy(); location=3; max_dm_error=0.; max_dm_defect=0.
    for which in range(2):
        for step in range(n):
            h=bath_scale*hermitian(rng,d); g=positive(rng,d)
            v,a,b=tap([(tau,h,g)])
            # Fresh collisions, with arbitrary common forward memory motion.
            collisions=[]
            for k in range(m):
                hd=bath_scale*hermitian(rng,d); gd=positive(rng,d)
                collisions.append(tap([(tau,hd,gd)]))
            dm=drain_map(collisions)
            max_dm_error=max(max_dm_error,dm['isometry_error'])
            max_dm_defect=max(max_dm_defect,dm['isometry_defect'])
            actual=apply_tap(rotate(actual,math.pi/(2*n)),which,v,a,b)
            ideal=apply_tap(rotate(ideal,math.pi/(2*n)),which,v,a,b)
            actual=apply_drain(actual,which,dm,location,False)
            ideal=apply_drain(ideal,which,dm,location,True)
            location+=m
    a=actual.reshape(-1,d); i=ideal.reshape(-1,d)
    accepted=actual[:2,:2,1].reshape(4*d,d)
    success=accepted.conj().T@accepted
    target=(-actual[0,0,1]+actual[1,1,1])/math.sqrt(2)
    bad=success-target.conj().T@target
    bad=(bad+bad.conj().T)/2
    quality=float(eigh(bad,success,eigvals_only=True)[-1])
    bound=finite_dump_bell_bound(n,.5,.5,m)
    result={'n':n,'m':m,'memory_dimension':d,'bath_scale':bath_scale,
            'full_isometry_error':norm(a-i),
            'weighted_dump_bound':bound['dump_stinespring_error'],
            'actual_isometry_defect':norm(a.conj().T@a-np.eye(d)),
            'ideal_isometry_defect':norm(i.conj().T@i-np.eye(d)),
            'maximum_one_drain_isometry_error':max_dm_error,
            'maximum_one_drain_isometry_defect':max_dm_defect,
            'success_min':float(np.linalg.eigvalsh(success)[0]),
            'success_bound':bound['finite_dump_success_lower'],
            'worst_conditional_bell_infidelity':quality,
            'bell_infidelity_bound':bound['finite_dump_bell_infidelity_bound']}
    assert result['full_isometry_error']<=result['weighted_dump_bound']+1e-11
    assert result['success_min']>=result['success_bound']-1e-11
    assert quality<=result['bell_infidelity_bound']+1e-11
    assert result['actual_isometry_defect']<1e-9
    return result

if __name__=='__main__':
    import json
    print(json.dumps(simulate(),indent=2))
