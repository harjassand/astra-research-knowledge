"""Finite-matrix audits for the physical admission note.

This checks algebra and exposes a local-bath failure.  It does not certify a
finite-band electromagnetic reservoir or a continuum interacting device.
"""
from pathlib import Path
import json
import numpy as np
from numpy.linalg import norm, eigh, svd
from scipy.linalg import expm

I2=np.eye(2)
X=np.array([[0.,1.],[1.,0.]])
Z=np.diag([1.,-1.])

def opnorm(a):
    return float(norm(a,2))

def isometry_for_band(h, bare, inds):
    energies, vecs=eigh(h)
    v=vecs[:,inds]
    u, _, vh=svd(bare.conj().T@v)
    polar=u@vh
    w=v@polar.conj().T
    return w, energies[inds]

def make_system(omega=1., csum=4., source_band=.001,
                t0=.00008, t1=.00002, gc=.00001, nmax=5):
    ne=nmax+1
    a=np.diag(np.sqrt(np.arange(1,ne)),1)
    n=a.T@a
    hop=np.zeros((3,3))
    # Charge ordering S, D_R, D_L.
    hop[0,1]=hop[1,0]=np.sqrt(2)
    hop[0,2]=hop[2,0]=np.sqrt(2)
    charge=np.diag([0.,-omega,csum+omega])
    he=source_band*X/2
    gain=t0*I2+t1*Z
    h=np.kron(np.kron(charge,np.eye(ne)),I2)
    h+=np.kron(np.kron(np.eye(3),omega*n),I2)
    h+=np.kron(np.eye(3*ne),he)
    h+=np.kron(np.kron(hop,np.eye(ne)),gain)
    h+=np.kron(np.kron(hop,gc*(a+a.T)),I2)
    ann=np.kron(np.kron(np.eye(3),a),I2)
    xpos=ann+ann.T
    def bare(columns):
        v=np.zeros((h.shape[0],len(columns)*2))
        for j,(q,photons) in enumerate(columns):
            for e in range(2):
                v[(q*ne+photons)*2+e,j*2+e]=1
        return v
    return h,ann,xpos,bare,gain,he

def lyapunov(g, h, kappa, d):
    mu=np.sqrt(2)*g
    nu=np.sqrt(2)*h
    c=kappa/2+d
    alpha=min(1., kappa/(2*(nu+c*c/(2*mu))))
    m=min(alpha*mu/2,kappa/2)
    rate=m/(1+alpha/2)
    return {'alpha':alpha,'rate':rate,'initial_a_prefactor':1/(1-alpha/2)}

def run():
    p=dict(omega=1.,csum=4.,source_band=.001,t0=.00008,
           t1=.00002,gc=.00001,nmax=5)
    h,a,x,bare,gain,he=make_system(**p)
    plow=bare([(1,0),(0,0),(1,1)])
    psink=bare([(1,0)])
    pactive=bare([(0,0),(1,1)])
    wlow,eval_low=isometry_for_band(h,plow,np.arange(6))
    wsink,eval_sink=isometry_for_band(h,psink,np.arange(2))
    wa,eval_a=isometry_for_band(h,pactive,np.arange(2,6))
    heff=wlow.T@h@wlow
    ac=wsink.T@x@wa
    acideal=np.column_stack([np.zeros((2,2)),np.eye(2)])
    ha=wa.T@h@wa
    kappa=4*p['gc']
    knojump=ha-0.5j*kappa*(ac.T@ac)
    worst=[]
    ell=lyapunov(p['gc'],p['gc'],kappa,0.)
    in_a=np.vstack([np.eye(2),np.zeros((2,2))])
    for scaled_time in [0,5,10,20,40,80]:
        t=scaled_time/p['gc']
        z=expm(-1j*knojump*t)@in_a
        worst.append({'t_times_gain':scaled_time,
                      'dressed_band_worst_no_jump':opnorm(z)**2,
                      'ideal_lyapunov_bound':min(1.,ell['initial_a_prefactor']*
                                               np.exp(-ell['rate']*t))})
    # A full non-RWA local D[a] jump excites the exact dressed ground state.
    es,vs=eigh(h)
    ground=vs[:,0]
    bare_jump=a@ground
    local_heat=kappa*(np.vdot(bare_jump,h@bare_jump).real-
                     es[0]*np.vdot(bare_jump,bare_jump).real)
    passive_jump=wsink@ac@wa.T
    passive_ground_norm=norm(passive_jump@ground)
    hh=p['t0']+p['t1']
    vbound=2*hh+np.sqrt(10)*p['gc']
    gapbound=.5*p['omega']-p['source_band']-4*hh-4*p['gc']-16*p['gc']**2/p['omega']
    report={'parameters':p,'source_gain_commutator_norm':opnorm(he@gain-gain@he),
            'low_band_eigenvalues':eval_low.tolist(),
            'first_omitted_eigenvalue':float(es[6]),
            'actual_low_band_gap':float(es[6]-es[5]),
            'conservative_infinite_mode_gap_bound':gapbound,
            'offblock_norm_bound':vbound,
            'conservative_exact_dressing_bound':4*vbound/gapbound,
            'conservative_retained_hamiltonian_correction_bound':8*vbound*vbound/gapbound,
            'canonical_low_isometry_change':opnorm(wlow-plow),
            'actual_low_hamiltonian_correction':opnorm(heff-plow.T@h@plow),
            'band_lowering_operator_change':opnorm(ac-acideal),
            'active_block_offdiagonal_singular_values':svd(ha[:2,2:],compute_uv=False).tolist(),
            'coarse_band_no_jump_survival':worst,
            'local_bare_annihilator_ground_heating_rate':float(local_heat),
            'passive_band_lowering_ground_action_norm':float(passive_ground_norm),
            'lyapunov_constants':ell,
            'meaning':'Finite-system algebra only; bath approximation and material spin/orbital admission are separate.'}
    assert report['source_gain_commutator_norm']>0
    assert report['actual_low_band_gap']>gapbound>0
    assert report['canonical_low_isometry_change']<report['conservative_exact_dressing_bound']
    assert report['actual_low_hamiltonian_correction']<report['conservative_retained_hamiltonian_correction_bound']
    assert local_heat>0
    assert passive_ground_norm<1e-10
    Path(__file__).with_name('resonant_valve_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    run()
