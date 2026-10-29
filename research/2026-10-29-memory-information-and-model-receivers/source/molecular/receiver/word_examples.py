"""Algebraic admitted molecular-word examples, not native CaOH parameters.

No ion propagation is replayed. The purpose is a non-null target check and
an explicit cross-word coefficient inaccessible from only kick diagonals.
"""
from pathlib import Path
from fractions import Fraction as F
import itertools,json,hashlib,time
import numpy as np

HERE=Path(__file__).resolve().parent
def dec(x):return np.array(x['real'])+1j*np.array(x['imag'])
def enc(x):return {'real':x.real.tolist(),'imag':x.imag.tolist()}

def coefficients(phases,qs,theta):
    c,s=np.cos(theta/2),np.sin(theta/2);M={0:np.eye(2,dtype=complex)}
    for phase,q in zip(phases,qs):
        terms={0:c*np.eye(2),q:np.array([[0,0],[-1j*s*np.exp(1j*phase),0]]),
               -q:np.array([[0,-1j*s*np.exp(-1j*phase)],[0,0]])}
        new={}
        for h,A in M.items():
            for j,B in terms.items():new[h+j]=new.get(h+j,0)+B@A
        M=new
    V=np.zeros((9,2),complex)
    for h,A in M.items():V[h+4]=A[:,0]
    return V@V.conj().T

def main():
    tic=time.perf_counter();data=(HERE/'inputs'/'HISTORY_KERNELS.json').read_bytes();root=json.loads(data)
    rb=json.loads((HERE/'KERNEL_BOUND.json').read_text())
    # Outward rational upper for the exact algebraic five-grid factor.
    kappa_upper=(1+F(22360679774998,10**13))/5
    for r in rb['reports']:
        rad=F(r['radius_exact'])
        if r['harmonic']:
            r['five_grid_probability_bound_rational_upper']=str(rad*kappa_upper/2)
            r['five_grid_probability_bound_numeric_display']=float(rad*kappa_upper/2)
        else:r['raw_probability_bound_exact']=str(rad/2)
    rb['numeric_display_scope']='Exact rational radius and rational upper for algebraic five-grid factor govern; binary64 displayed decimals are approximate.'
    (HERE/'KERNEL_BOUND.json').write_text(json.dumps(rb,indent=2)+'\n')
    rows=[];maxauto=0.;maxtrace=0.;saved=None
    for p in [.03,.5]:
        theta=2*np.arcsin(np.sqrt(p))
        for qs in [[1,1,1,1],[1,-1,1,1]]:
            Cbar=np.zeros((9,9),complex)
            for ks in itertools.product(range(5),repeat=3):
                phase=np.r_[2*np.pi*np.array(ks)/5,0.]
                C=coefficients(phase,qs,theta)
                maxtrace=max(maxtrace,abs(np.trace(C)-1))
                for lag in range(1,9):maxauto=max(maxauto,abs(np.diag(C,lag).sum()))
                Cbar+=C*np.exp(-1j*np.dot([-1,1,1],phase[:3]))/125
                if saved is None and qs==[1,-1,1,1]:saved=C
            for report in root['reports']:
                for name in ['Z_physical_bright','Y_analysis']:
                    d=report['observables'][name];A=dec(d['A']);B=dec(d['B']);target=dec(d['Ktarget'])
                    a=np.trace(Cbar@A);b=np.trace(Cbar@B);cc=np.trace(Cbar@B.conj().T)
                    # A rigorous structural triangle bound, evaluated in floats here.
                    rows.append({'pulse':report['pulse'],'axis':name,'p_per_pulse_model':p,'q':qs,
                        'target_mean_bright_coefficient':[float(np.trace(Cbar@target).real),float(np.trace(Cbar@target).imag)],
                        'target_probability_coefficient_abs':float(abs(np.trace(Cbar@target))/2),
                        'model_error_probability_triangle_all_Dphases':float((abs(a)+abs(b)+abs(cc))/2),
                        'no_native_CaOH_excitation_or_molecular_model_claim':True})
    # A literal small non-Toeplitz PSD, trace-one/autocorrelation example.
    V=np.array([[.5,0],[.5,-.5],[0,.5]],complex);C=V@V.conj().T
    N=np.array([[0,1,0],[1,0,0],[0,0,0]],complex)
    out={'kernel_sha256':hashlib.sha256(data).hexdigest(),'examples':rows,
         'coefficient_checks':{'max_trace_defect':float(maxtrace),'max_offlag_sum':float(maxauto)},
         'diagonal_only_information_counter':{'C':enc(C),'zero_diagonal_error_kernel':enc(N),
             'trace_CN':float(np.trace(C@N).real),
             'scope':'Coefficient/linear-measurement example; not a fabricated native instrument. It proves kick diagonals do not generally determine cross-word contraction.'},
         'seconds_after_imports':time.perf_counter()-tic,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'WORD_EXAMPLES.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'examples':rows,'coefficient_checks':out['coefficient_checks'],'seconds':out['seconds_after_imports']},indent=2))

if __name__=='__main__':main()
