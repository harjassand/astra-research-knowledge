"""Independent finite-matrix audit of commutator-sensitive admission.

Checks the exact BCH bound, arbitrary-state propagator norm, large extensive
diagonal source energies, a source-powered resonance, and piecewise time-
dependent source dynamics with a single fixed dressing generator.
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm, eigh

I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],dtype=complex)
Y=np.array([[0,-1j],[1j,0]],dtype=complex)
Z=np.diag([1.,-1.]).astype(complex)
lower=np.array([[0,1],[0,0]],dtype=complex)

def on_site(a,i,n):
    out=np.array([[1.]],dtype=complex)
    for j in range(n): out=np.kron(out,a if i==j else I)
    return out

def annihilator(i,n):
    out=np.array([[1.]],dtype=complex)
    for j in range(n):
        out=np.kron(out,Z if j<i else lower if j==i else I)
    return out

def opnorm(a):
    return float(np.linalg.norm(a,2))

def comm(a,b):
    return a@b-b@a

def unitary_function(h):
    es,vs=eigh(h)
    return lambda t:(vs*np.exp(-1j*es*t))@vs.conj().T

def density_source(n,scale=0.,hopping=.2,phase=0.):
    ds=2**n
    annih=[annihilator(i,n) for i in range(n)]
    occupations=[a.conj().T@a for a in annih]
    diagonal=np.zeros((ds,ds),complex)
    for i,ni in enumerate(occupations):
        diagonal+=(.7+.11*i)*((-1)**i)*ni
    for i in range(n):
        for j in range(i+1,n):
            diagonal+=(.4/(j-i))*occupations[i]@occupations[j]
    h=scale*diagonal
    for i in range(n-1):
        z=np.exp(1j*phase*(i+1))*annih[i].conj().T@annih[i+1]
        h+=hopping*(z+z.conj().T)
    return h,occupations

def two_band_data(he,gain,delta,w=None):
    ds=len(he)
    eye=np.eye(ds)
    hc=np.kron(np.diag([0.,delta]),eye)
    source=np.kron(I,he)
    v=np.kron(X,gain)
    s=np.kron(-1j*Y,gain/delta)
    if w is None: w=np.zeros_like(v)
    href=hc+source+w
    h=href+v
    sn=opnorm(s); vn=opnorm(v); wn=opnorm(w)
    cn=opnorm(comm(s,source))
    bound=np.exp(2*sn)*(cn+2*sn*wn+sn*vn)
    rotation=expm(s)
    remainder=rotation@h@rotation.conj().T-href
    return {'h':h,'href':href,'hc':hc,'source':source,'v':v,'s':s,
            'sn':sn,'vn':vn,'wn':wn,'cn':cn,'bound':float(bound),
            'rnorm':opnorm(remainder),'cancellation_error':opnorm(comm(s,hc)+v)}

def audit_static(n,scale,delta=100.):
    he,_=density_source(n,scale=scale)
    gain=np.eye(2**n)+.3*on_site(Z,0,n)
    w=.15*np.kron(Z,on_site(Z,n-1,n))
    d=two_band_data(he,gain,delta,w)
    uf=unitary_function(d['h']); rf=unitary_function(d['href'])
    times=[]
    for t in [.5,2.,5.]:
        actual=opnorm(uf(t)-rf(t))
        bound=2*d['sn']+t*d['bound']
        assert actual<=bound+1e-7
        times.append({'time':t,'unitary_norm_error':actual,'bound':bound})
    assert d['rnorm']<=d['bound']+1e-7
    return {'source_sites':n,'diagonal_energy_scale':scale,
            'source_norm':opnorm(he),
            'source_spectral_diameter':float(np.linalg.eigvalsh(he)[-1]-np.linalg.eigvalsh(he)[0]),
            'gain_eigenvalue_interval':[.7,1.3],
            'source_gain_commutator_norm':opnorm(comm(he,gain)),
            'expected_source_gain_commutator_norm':.12,
            's':d['sn'],'c':d['cn'],'w':d['wn'],'v':d['vn'],
            'exact_bch_remainder_norm':d['rnorm'],'bch_remainder_bound':d['bound'],
            'cancellation_error':d['cancellation_error'],'times':times}

def resonant_counterexample():
    delta=1000.
    he=delta*X/2
    gain=2*I+Z
    d=two_band_data(he,gain,delta)
    t=np.pi/2
    u=unitary_function(d['h'])(t)
    uref=unitary_function(d['href'])(t)
    inp=np.kron(np.array([1.,0.]),np.array([1.,1.])/np.sqrt(2))
    out=u@inp
    leakage=float(np.vdot(out[2:],out[2:]).real)
    actual=opnorm(u-uref)
    bound=2*d['sn']+t*d['bound']
    false_gap_bound=2*d['sn']+t*np.exp(2*d['sn'])*d['sn']*d['vn']
    assert leakage>.99
    assert actual>10*false_gap_bound
    assert actual<=bound+1e-10
    return {'delta':delta,'time':t,'gain_eigenvalue_interval':[1.,3.],
            'source_gain_commutator_norm':opnorm(comm(he,gain)),
            'c':d['cn'],'orbital_leakage_from_explicit_input':leakage,
            'unitary_norm_error':actual,'correct_bound':bound,
            'incorrect_bound_omitting_source_commutator':false_gap_bound,
            'message':'A positive unknown gain can use a resonant quantum source to bridge the bare gap.'}

def time_dependent_example():
    n=3; delta=100.; ds=2**n; steps=16; duration=3.; dt=duration/steps
    gain=np.eye(ds)+.3*on_site(Z,0,n)
    actual=np.eye(2*ds,dtype=complex)
    reference=actual.copy()
    integral=0.; maxsource=0.; maxc=0.; s0=None
    for j in range(steps):
        he,_=density_source(n,scale=(1+j%3)*1e4,hopping=.2,
                            phase=.71*j)
        w=.15*np.cos(.37*j)*np.kron(Z,on_site(X,n-1,n))
        d=two_band_data(he,gain,delta,w)
        if s0 is None: s0=d['s']
        assert opnorm(d['s']-s0)==0
        actual=unitary_function(d['h'])(dt)@actual
        reference=unitary_function(d['href'])(dt)@reference
        integral+=dt*d['bound']
        maxsource=max(maxsource,opnorm(he)); maxc=max(maxc,d['cn'])
    error=opnorm(actual-reference)
    bound=2*opnorm(s0)+integral
    assert error<=bound+1e-8
    return {'steps':steps,'duration':duration,'maximum_source_norm':maxsource,
            'maximum_c':maxc,'unitary_norm_error':error,'integrated_bound':bound,
            'message':'Piecewise source Hamiltonians do not commute with one another; S stays fixed.'}

def multiblock_example():
    rng=np.random.default_rng(3102026)
    energies=np.array([-7.,0.,0.,7.])
    ds=2; nc=len(energies)
    he=11.3*X+3.7*Z
    raw=rng.normal(size=(nc*ds,nc*ds))+1j*rng.normal(size=(nc*ds,nc*ds))
    raw=(raw+raw.conj().T)/2
    v=np.zeros_like(raw); w=np.zeros_like(raw); s=np.zeros_like(raw)
    for a in range(nc):
        for b in range(nc):
            sl=(slice(a*ds,(a+1)*ds),slice(b*ds,(b+1)*ds))
            if energies[a]==energies[b]:
                w[sl]=.07*raw[sl]
            else:
                v[sl]=.11*raw[sl]
                s[sl]=v[sl]/(energies[a]-energies[b])
    hc=np.kron(np.diag(energies),I)
    source=np.kron(np.eye(nc),he)
    href=hc+source+w; h=href+v
    sn=opnorm(s); cn=opnorm(comm(s,source)); wn=opnorm(w); vn=opnorm(v)
    r=expm(s)@h@expm(-s)-href
    bound=np.exp(2*sn)*(cn+2*sn*wn+sn*vn)
    assert opnorm(s+s.conj().T)<1e-14
    assert opnorm(comm(s,hc)+v)<1e-14
    assert opnorm(r)<=bound+1e-12
    return {'s':sn,'c':cn,'w':wn,'v':vn,'remainder_norm':opnorm(r),
            'remainder_bound':float(bound),
            'antihermiticity_error':opnorm(s+s.conj().T),
            'cancellation_error':opnorm(comm(s,hc)+v)}

if __name__=='__main__':
    result={'static_density_sources':[audit_static(4,l) for l in [0.,1e2,1e4,1e6]],
            'source_size_scaling':[audit_static(n,1e4) for n in [2,4,6]],
            'resonant_source_counterexample':resonant_counterexample(),
            'time_dependent_source':time_dependent_example(),
            'multiple_energy_blocks':multiblock_example(),
            'scope':'Independent matrix checks support the analytic proof; they are not the proof.'}
    Path(__file__).with_name('local_admission_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
