"""Exact rational fringing/tolerance budget and FULL-pair energy diagnostic."""
from fractions import Fraction as F
from pathlib import Path
import json
import time
import numpy as np
from scipy.linalg import hadamard


def main():
    start=time.perf_counter()
    rho=F(1,6); a=F(1,20); q=F(1,10)
    shell=8*(sum((F(1,j*j) for j in range(1,6)),F(0))+F(1,5))
    assert shell<F(40,3)
    epsilon=F(20,3)*q**3/(1-a*q)**3
    general=1-5*rho-24*a*a-8*epsilon
    support=1-5*rho-6*a*a-8*epsilon
    assert general>0 and support>0
    H=hadamard(8).astype(int)
    xy=np.asarray([(i,j) for i in range(8) for j in range(8)],float)
    ss=H.ravel(); w=len(ss); h=float(q)
    S=2*w/h**3
    cases=[]
    # A standard source-generated Hadamard face, NOT a new/code-optimized
    # manufacturing palette. Include one out-of-tolerance pose explicitly.
    for name,angle,delta in [('aligned',0.,np.array([0.,0.])),
                             ('small_translation',0.,np.array([float(a*q),0.])),
                             ('small_angle',float(a*q)/(2*np.linalg.norm([3.5,3.5])),np.array([0.,0.])),
                             ('half_pixel_unqualified',0.,np.array([.5,0.]))]:
        centered=xy-3.5
        R=np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
        target=centered@R.T+3.5+delta
        disp=xy[:,None,:]-target[None,:,:]
        r2=np.einsum('ijk,ijk->ij',disp,disp)
        K=(r2-2*h*h)/(r2+h*h)**2.5
        energy=float(np.sum(ss[:,None]*ss[None,:]*K))
        maxpose=float(np.linalg.norm(target-xy,axis=1).max())
        allowed=maxpose<=float(a*q)*(1+1e-12)
        error=abs(-energy/S-1)
        cases.append({'name':name,'normalized_full_pair_attraction':-energy/S,
                      'actual_max_pixel_displacement':maxpose,
                      'allowed_max_pixel_displacement':float(a*q),
                      'inside_declared_pose_tolerance':allowed,
                      'deviation_from_ideal_mate_score':error,
                      'analytic_uniform_score_error_upper':float(3*a*a+epsilon) if allowed else None,
                      'inside_analytic_bound':bool(error<=float(3*a*a+epsilon)) if allowed else None})
    out={'scope':'Conditional fixed-normal-hard-dipole contact model; no physical calibration/assembly',
         'epsilon_exact':str(epsilon),'epsilon_display':float(epsilon),
         'general_signed_AND_gap_exact':str(general),'general_signed_AND_gap_display':float(general),
         'support_or_translation_AND_gap_exact':str(support),'support_or_translation_AND_gap_display':float(support),
         'exact_shell_bound':str(shell),'pairs_per_energy_sum':64**2,
         'float_full_pair_diagnostics':cases,'seconds_after_imports':time.perf_counter()-start,
         'source_Hadamard_face_claimed_to_meet_rho':False,
         'cross_face_remote_fields_or_native_commitment_acquired':False}
    Path(__file__).with_name('MAGNETOSTATIC_RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
