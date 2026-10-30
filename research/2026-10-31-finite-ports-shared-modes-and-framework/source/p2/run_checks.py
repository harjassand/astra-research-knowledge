"""Reproduce the finite-port working checks and resource examples.

The proofs, rather than floating point samples, justify uniform claims.
All numerical results here are ordinary double precision, not interval
certificates. Run from any directory with numpy/scipy installed.
"""
import json, math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from fractions import Fraction
from finite_ports import *
from finite_dump_check import hermitian, positive, simulate

class NC:
    """Exact rational polynomials in noncommuting symbols."""
    def __init__(self,x=0):
        if isinstance(x,dict): self.terms={k:Fraction(v) for k,v in x.items() if v}
        elif isinstance(x,str): self.terms={(x,):Fraction(1)}
        else: self.terms={():Fraction(x)} if x else {}
    @staticmethod
    def cast(x): return x if isinstance(x,NC) else NC(x)
    def __add__(self,other):
        t=self.terms.copy()
        for k,v in self.cast(other).terms.items(): t[k]=t.get(k,0)+v
        return NC(t)
    __radd__=__add__
    def __neg__(self): return NC({k:-v for k,v in self.terms.items()})
    def __sub__(self,other): return self+-self.cast(other)
    def __rsub__(self,other): return self.cast(other)+-self
    def __mul__(self,other):
        t={}
        for k,v in self.terms.items():
            for l,w in self.cast(other).terms.items(): t[k+l]=t.get(k+l,0)+v*w
        return NC(t)
    def __rmul__(self,other): return self.cast(other)*self
    def __truediv__(self,other): return self*NC(Fraction(1,other))
    def __eq__(self,other): return self.terms==self.cast(other).terms

def symbolic_checks():
    v1,v2,u1,u2,a1,a2,w1,w2,z1,z2=[NC(x) for x in 'V1 V2 u1 u2 v1 v2 w1 w2 z1 z2'.split()]
    first=[[[0,-v1],[v1,0]],[[u1,a1],[w1,z1]]]
    second=[[[0,-v2],[v2,0]],[[u2,a2],[w2,z2]]]
    expected=[-v2*v1,a2*v1,-v2*w1,u2*u1+a2*w1]
    found=[sum(NC.cast(second[y][0][k])*first[x][k][0] for k in range(2))
           for x in range(2) for y in range(2)]
    assert all(x==y for x,y in zip(found,expected))
    f=[NC('f'+str(j)) for j in range(4)]
    fd=[NC('fd'+str(j)) for j in range(4)]
    success=sum(fd[j]*f[j] for j in range(4))/4
    target=(-fd[0]+fd[3])*(-f[0]+f[3])/8
    bad=(fd[1]*f[1]+fd[2]*f[2])/4+(fd[0]+fd[3])*(f[0]+f[3])/8
    assert success-target-bad==0
    return {'noncommuting_filter_blocks':4,'bell_bad_effect_identity':True}

def unitary(rng,d):
    q,r=np.linalg.qr(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)))
    return q

def arbitrary_contraction_checks():
    rng=np.random.default_rng(81733); cases=0; max_excess=-1.
    worst_parity_branch=0.; worst_bell=0.
    for d in [1,2,4]:
        for n in [2,3,8,32,128]:
            for r in [0.,.2,.6,.95]:
                banks=[]
                for k in range(2):
                    ts=[]
                    for j in range(n):
                        v=unitary(rng,d)
                        a=unitary(rng,d)@np.diag(r*rng.uniform(.1,1,d))@unitary(rng,d)
                        ts.append((v,a))
                    banks.append(ts)
                for angle in [math.pi/2,math.pi]:
                    ns=[node(ts,angle) for ts in banks]; bounds=node_bounds(n,r,angle)
                    for x in ns:
                        excess=max(norm(x['u']-x['free'])-bounds['delta'],
                                   norm(x['v'])-bounds['alpha'],
                                   norm(x['w'])-bounds['beta'],
                                   norm(x['z'])-bounds['gamma'])
                        max_excess=max(max_excess,excess)
                        assert excess<1e-11
                    if angle==math.pi/2:
                        got=bell_filter(*ns); b=bell_bounds(n,r)
                        assert got['success_min']>=b['success_lower']-1e-11
                        assert got['worst_conditional_bell_infidelity']<=b['conditional_bell_infidelity_bound']+1e-11
                        worst_bell=max(worst_bell,got['worst_conditional_bell_infidelity'])
                    else:
                        got=parity_instrument(*ns); b=parity_bounds(n,r)
                        assert got['accepted_branch_operator_error']<=b['accepted_branch_operator_error']+1e-11
                        assert got['herald_failure_max']<=b['herald_failure_upper']+1e-11
                        worst_parity_branch=max(worst_parity_branch,got['accepted_branch_operator_error'])
                    cases+=1
    return {'two_node_cases':cases,'maximum_block_bound_excess':max_excess,
            'note':'Includes deliberately poor small-N cases; no bath state is sampled.'}

def physical_opacity_checks():
    rng=np.random.default_rng(5011); cases=0; excess=-1.; max_comm=0.
    for d in [2,4,8]:
        for scale in [0.,1.,10.,100.,1000.]:
            for count in [1,7]:
                pieces=[]; tau=math.pi/3
                for k in range(count):
                    h=scale*hermitian(rng,d); g=positive(rng,d)
                    max_comm=max(max_comm,norm(h@g-g@h))
                    pieces.append((tau/count,h,g))
                v,a,b=tap(pieces)
                excess=max(excess,norm(a)-.5)
                assert norm(a)<=.5+1e-10
                assert norm(a.conj().T@a+b.conj().T@b-np.eye(d))<1e-9
                cases+=1
    return {'cases':cases,'maximum_opacity_bound_excess':excess,
            'maximum_H_G_commutator_norm':max_comm,'maximum_bath_norm':1000.}

def failure_witnesses():
    x=np.array([[0,1],[1,0]],complex); z=np.diag([1.,-1.]); eye=np.eye(2)
    rows=[]
    for omega in [0.,10.,100.]:
        v,a,b=tap([(math.pi/2,omega*z,x)])
        rows.append({'bath_strength':omega,'actual_transfer_probability':norm(b)**2,
                     'transfer_probability_upper':1/(1+omega*omega)})
        assert norm(b)**2<=1/(1+omega*omega)+1e-11
    # A singular-value gap is insufficient, even when every singular value is one.
    # Reusing the same perfectly coherent drain reverses a complete transfer.
    swap=expm(-1j*math.pi*x/2)
    returned=swap@swap@np.array([1.,0.])
    assert abs(abs(returned[0])**2-1)<1e-12
    # Common-factor dark/bright spectral-gap intuition is also insufficient.
    h=np.diag([0.,1.5]); g=np.array([[2.,1.],[1.,2.]])
    vals,vec=np.linalg.eigh(h+g)
    resonant_overlap=abs(vec[1,0])
    assert abs(vals[0]-1.5)<1e-12 and resonant_overlap>0
    return {'indefinite_coupling':rows,'coherent_drain_return_probability':float(abs(returned[0])**2),
            'adiabatic_warning':{'G_eigenvalues':np.linalg.eigvalsh(g).tolist(),
                                 'H_eigenvalues':np.linalg.eigvalsh(h).tolist(),
                                 'H_plus_G_eigenvalues':vals.tolist(),
                                 'resonant_dark_bright_overlap':float(resonant_overlap)}}

def sharpness():
    rows=[]; r=.5; phi=math.pi/2
    leading=phi**2*(1+r*r)/(2*(1-r)**2)+phi**4*(1+r)**2/(4*(1-r)**2)
    for n in [64,128,256,512,1024,2048]:
        nd=node(scalar_taps(n,r)); exact=bell_filter(nd,nd)
        rows.append({'n':n,'n_times_safe_block_error':n*norm(nd['u']-nd['free']),
                     'n_squared_bell_infidelity':n*n*exact['worst_conditional_bell_infidelity']})
    return {'r':r,'safe_block_asymptotic':node_bounds(2,r)['leading_delta_constant'],
            'bell_infidelity_asymptotic':leading,'samples':rows}

def resource_examples():
    rows=[]; r=.6; m=20; tau_max=1.05*math.pi/3
    for n in [32,64,128,256]:
        b=finite_dump_bell_bound(n,r,r,m)
        p=b['finite_dump_success_lower']; err=b['finite_dump_bell_infidelity_bound']
        # One finite source pulse, balanced optical loss per complete cycle,
        # a detector with no false accepts. These are stipulated resources.
        yield_lower=(1-r*r)*.9*.999**(2*n)*p
        total_error=b['dump_stinespring_error']+.02
        pcal=(max(0.,math.sqrt(b['success_lower'])-total_error))**2
        ecal=(math.sqrt(b['bad_effect_bound'])+total_error)**2/pcal
        yield_cal=(1-r*r)*.9*.999**(2*n)*pcal
        rows.append({'n_per_node':n,'finite_dump_success_lower':p,
                     'bell_infidelity_bound':err,'dump_error':b['dump_stinespring_error'],
                     'mean_attempts_upper':1/yield_lower,
                     'drain_windows_per_attempt':2*n*m,
                     'total_interaction_windows_per_attempt':1+2*n*(1+m),
                     'interaction_time_upper_per_attempt_gmin_units':tau_max*(1+2*n*(1+m)),
                     'with_rotation_error_002':{'success_lower':pcal,'bell_infidelity_bound':ecal,
                                               'mean_attempts_upper':1/yield_cal}})
    shots=math.ceil(4*math.log(200)/.01**2)
    n=64; detection=.64*.9*.999**(n/2)
    return {'assumptions':{'gmin':1.,'gmax':2.,'timing_relative_window':.05,
                           'conservative_r':r,'exact_r_with_timing':math.cos(.3*math.pi),
                           'drain_collisions_per_tap':m,'balanced_cycle_transmission':.999,
                           'source_emission_lower':.64,'readout_efficiency':.9,
                           'false_accepts':0.,'prep_and_holding_errors':'not included'},
            'rows':rows,'ordinary_meter_calibration':{
                'one_node_total_angle_precision':.01,'confidence_failure':.01,
                'detected_probes_sufficient':shots,'coupler_passes_per_detected_probe':n//2,
                'detected_probe_passes':shots*(n//2),
                'prepared_source_attempts_mean':shots/detection,
                'qualification':'known monotone phase branch; SPAM bias separately bounded; stable coupler'}}

def main():
    results={'symbolic':symbolic_checks(),'arbitrary_contractions':arbitrary_contraction_checks(),
             'physical_opacity':physical_opacity_checks(),'failures':failure_witnesses(),
             'sharpness':sharpness(),'finite_drains':simulate(),
             'resources':resource_examples(),
             'status':'Root working derivations. Floating point checks are not certified rounding enclosures.'}
    path=Path(__file__).with_name('results.json')
    path.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({k:v for k,v in results.items() if k not in ['resources','sharpness']},indent=2))
    print('Saved results.json; all checks passed.')

if __name__=='__main__': main()
