"""Finite local-port construction and state-uniform Zeno bounds.

New resource setting: a local qutrit |0>,|1>,|e> couples |1,1_b>
to |e,0_b> with a positive, unknown operator G on retained M.  A
fresh drain removes |e> between visits.  No native two-data-qubit
parity coupling is supplied.  Sources, drains, and meter-only beam
splitters are explicitly separate resources from the old spin handles.
"""
import math
import numpy as np
from scipy.linalg import expm, block_diag, eigh

def norm(a): return float(np.linalg.norm(a,2))

def opacity_bound(gmin,gmax,tau=None):
    if tau is None: tau=math.pi/(gmin+gmax)
    assert gmin>0 and gmax>=gmin and gmax*tau<math.pi
    return max(abs(math.cos(gmin*tau)),abs(math.cos(gmax*tau)))

def tap(pieces):
    """Exact piecewise-constant finite tap: [(dt,H_M,G),...].

    Returned A is the amplitude to remain in the risky photon mode;
    B transfers the excitation to the auxiliary level. The latter is
    removed into a fresh outgoing drain before the next visit.
    """
    dim=len(pieces[0][1]); eye=np.eye(dim,dtype=complex)
    plus=eye.copy(); minus=eye.copy(); free=eye.copy()
    for dt,h,g in pieces:
        plus=expm(-1j*(h+g)*dt)@plus
        minus=expm(-1j*(h-g)*dt)@minus
        free=expm(-1j*h*dt)@free
    return free,(plus+minus)/2,(plus-minus)/2

def node(taps,angle=math.pi/2):
    """Chronological weak rotations followed by local taps.

    'bright' acts on safe/risky optical rails and M, conditioned on
    the stationary logical qubit being |1>.  'dark' is transparent
    and consists of the same free-memory history and the optical
    rotation. This routine retains every memory matrix element.
    """
    n=len(taps); dim=len(taps[0][0]); eye=np.eye(dim,dtype=complex)
    c=math.cos(angle/n); s=math.sin(angle/n)
    rot=np.kron(np.array([[c,-s],[s,c]]),eye)
    bright=np.eye(2*dim,dtype=complex); free=eye.copy()
    r_actual=0.
    for v,a in taps:
        bright=block_diag(v,a)@rot@bright
        free=v@free
        r_actual=max(r_actual,norm(a))
    dark=np.kron(np.array([[math.cos(angle),-math.sin(angle)],
                          [math.sin(angle),math.cos(angle)]]),free)
    return {'bright':bright,'dark':dark,'free':free,'r_actual':r_actual,
            'u':bright[:dim,:dim], 'v':bright[:dim,dim:],
            'w':bright[dim:,:dim], 'z':bright[dim:,dim:]}

def node_bounds(n,r,angle=math.pi/2):
    assert n>=2 and 0<=r<1 and 0<angle/n<=math.pi/2
    theta=angle/n; c=math.cos(theta); s=math.sin(theta); q=r*c
    geometric=(1-q**n)/(1-q)
    delta=n*(1-c)+(r*s*s/(1-q))*(n-geometric)
    alpha=s*geometric
    beta=r*alpha
    gamma=q**n+r*s*s*(1-q**n)/(1-q)**2
    return {'n':n,'r':r,'angle':angle,'delta':delta,'alpha':alpha,
            'beta':beta,'gamma':gamma,
            'leading_delta_constant':angle*angle*(1+r)/(2*(1-r))}

def bell_bounds(n,r):
    b=node_bounds(n,r,math.pi/2)
    d=2*b['delta']+b['alpha']*b['beta']
    bad=(b['alpha']**2+b['beta']**2)/4+d*d/8
    success=(1+max(0.,1-d)**2)/4
    return {**b,'even_sector_deviation':d,'bad_effect_bound':bad,
            'success_lower':success,'conditional_bell_infidelity_bound':min(1.,bad/success)}

def bell_filter(first,second):
    """Two pi/2 nodes, input safe rail, accept final safe rail.

    For |++> stationary inputs, ideal accepted state is
    ( -|00> + |11> ) / sqrt(2). No Pauli correction pulse is assumed.
    """
    f00=-second['free']@first['free']
    f01=second['v']@first['free']
    f10=-second['free']@first['w']
    f11=second['u']@first['u']+second['v']@first['w']
    blocks=[f00,f01,f10,f11]
    success=sum(f.conj().T@f for f in blocks)/4
    bell=(-f00+f11)/(2*math.sqrt(2))
    bad=(success-bell.conj().T@bell)
    bad=(bad+bad.conj().T)/2
    vals=eigh(bad,success,eigvals_only=True)
    # Initial |++> factor is a physical logical-source assumption.
    return {'blocks':blocks,'success_effect':success,'bad_effect':bad,
            'success_min':float(np.linalg.eigvalsh(success)[0]),
            'success_max':float(np.linalg.eigvalsh(success)[-1]),
            'worst_conditional_bell_infidelity':max(0.,float(vals[-1]))}

def parity_bounds(n,r):
    b=node_bounds(n,r,math.pi); d=2*b['delta']
    fail=1. if d>=1 else d-d*d/2
    return {**b,'signal_operator_error':d,
            'herald_failure_upper':min(1.,fail),
            'accepted_branch_operator_error':d/2,
            'half_diamond_instrument_upper':min(1.,d/math.sqrt(2)+fail/2)}

def parity_instrument(first,second):
    """Full two-outcome parity instrument from two pi-winding nodes.

    A reference rail bypasses both controlled taps but experiences the
    same free evolution of M. A residual risky-rail photon is rejected
    after each node. Only the final photon needs to be detected.
    """
    common=second['free']@first['free']; dim=len(common)
    blocks=[common,-second['u']@first['free'],
            -second['free']@first['u'],second['u']@first['u']]
    signal=block_diag(*blocks); ref=np.kron(np.eye(4),common)
    plus=(ref+signal)/2; minus=(ref-signal)/2
    q=np.diag([1,-1,-1,1]); ident=np.eye(4)
    ideal_plus=np.kron((ident+q)/2,common)
    ideal_minus=np.kron((ident-q)/2,common)
    success=plus.conj().T@plus+minus.conj().T@minus
    return {'plus':plus,'minus':minus,'success_effect':success,
            'accepted_branch_operator_error':max(norm(plus-ideal_plus),norm(minus-ideal_minus)),
            'herald_failure_max':max(0.,float(np.linalg.eigvalsh(np.eye(4*dim)-success)[-1]))}

def dump_bound(n,r,r_dump,m,angle=math.pi/2,nodes=2,risky_input_nodes=0):
    """Weighted Stinespring error for m imperfect dump collisions.

    Dump error acts only on the short-lived excited level. The ideal
    prefix excited amplitude for a safe input is at most
    sin(theta)/(1-r cos(theta)). A node that may start in the risky
    rail also has a geometrically decaying transient. In the Bell
    factory this occurs at the second node, and MUST be counted.
    A bound without this support information would incorrectly pay
    a full-sized source error on every cycle.
    """
    theta=angle/n; c=math.cos(theta); s=math.sin(theta); q=r*c
    exposure=nodes*n*s/(1-q)+risky_input_nodes*c*(1-q**n)/(1-q)
    return math.sqrt(2)*exposure*r_dump**m

def finite_dump_bell_bound(n,r,r_dump,m):
    b=bell_bounds(n,r); e=dump_bound(n,r,r_dump,m,risky_input_nodes=1)
    p=(max(0.,math.sqrt(b['success_lower'])-e))**2
    bad=(math.sqrt(b['bad_effect_bound'])+e)**2
    return {**b,'dump_stinespring_error':e,'finite_dump_success_lower':p,
            'finite_dump_bell_infidelity_bound':min(1.,bad/p) if p else 1.}

def scalar_taps(n,a):
    return [(np.ones((1,1),complex),np.array([[a]],complex)) for _ in range(n)]
