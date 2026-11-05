"""Exact original sine-arm intervention, without a second meter or pin.

Uses finite canonical position-pointer measurements, additive C1 force pulses,
and fresh tilted-Gaussian randomness. The endpoint position shift is chosen
to cancel its residual covariance with momentum and its initial-position
gain. This avoids a hidden 1/k displacement-action divergence.
"""
import argparse
import json
from decimal import Decimal
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from p2_general_reset import reduced_meter, reset, iv_fixture


def direct_arm(k, eta=.5, D0=1., duration=.1):
    base=reset(k,tau_control=duration,D0=D0)
    w=np.array(base['weights']); G,S,cross,Cm,Hm=reduced_meter(k)
    A=np.array([[0.,1.],[-k,-1.]])
    E=expm(A*duration); crossf=cross@E.T
    B=np.array([[0.],[1.]])
    VL=np.block([[A,2*B@B.T],[np.zeros((2,2)),-A.T]])
    ev=expm(VL*duration)
    Cf=E@Cm@E.T+ev[:2,2:]@ev[:2,:2].T
    q=crossf[:,1]-S@w
    c=base['residual_px_covariance']; v=base['residual_p_variance']
    ix=[0,7]
    mat=np.array([G[ix,0],q[ix]])
    s=np.zeros(8); s[ix]=np.linalg.solve(mat,np.array([0.,-c]))
    gain_s=s@G; gain_w=w@G
    r=1-v; amplitude=eta*np.exp(v/(2*r))
    assert amplitude<1
    # Across fair arms, the tilted dither has exactly N(0,r) marginal.
    # A conditional arm has mean +/- eta exp(-1/2), second moment r.
    final_gain=np.array(base['final_initial_gains_x_p_force'])
    final_gain[0]+=gain_s
    xnoise=Cf[0,0]+2*s@crossf[:,0]+s@S@s
    cross_residual=c+s@q
    # Original hard fixture: E x0^2=1/k, E p0^2=1+m^2,
    # E F^2=f^2, E p0 F=mf, with x0 independent conditional sector.
    lam=base['lambda']; m=np.sqrt(2*D0*lam); f=(1-lam)*m
    T=np.array([[0.,0.,0.],[0.,1+m*m,m*f],[0.,m*f,f*f]])
    d_gain=np.vstack([gain_s,-gain_w])
    # Exact construction has zero first component of gain_s. Do not charge
    # numerical cancellation residual times a divergent 1/k coordinate.
    d_gain[0,0]=0.
    displacement_cov=np.vstack([s,-w])@S@np.vstack([s,-w]).T
    displacement_cov+=d_gain@T@d_gain.T
    if k>0: displacement_cov[1,1]+=gain_w[0]**2/k
    displacement_cov[1,1]+=r
    pulseH=np.array(base['finite_pulse_endpoint_matrix'])
    invH=np.linalg.inv(pulseH)
    force_action=3*duration/16*np.trace(invH@displacement_cov@invH.T)
    return {'k':float(k),'lambda':lam,'eta':eta,'D0_for_action':D0,
        'meter_duration':1.,'control_duration':duration,
        'nominal_intervention_duration':1+duration,
        'momentum_feedback_weights':w.tolist(),
        'position_feedback_weights':s.tolist(),
        'position_feedback_gains_x_p_force':gain_s.tolist(),
        'position_feedback_constraint_determinant':float(np.linalg.det(mat)),
        'residual_momentum_variance':v,'residual_position_momentum_covariance':c,
        'dither_gaussian_variance':r,'dither_sine_amplitude':float(amplitude),
        'dither_density':'G_r(d) [1 +/- A sin(d/r)] (normalized sigma=1)',
        'dither_proposal_acceptance_probability':float(1/(1+amplitude)),
        'final_initial_gains_x_p_force':final_gain.tolist(),
        'final_x_gaussian_noise_variance':float(xnoise),
        'final_x_residual_momentum_covariance':float(cross_residual),
        'final_arm_mean_momentum_magnitude':float(eta*np.exp(-.5)),
        'final_arm_momentum_second_moment':1.,
        'expected_squared_endpoint_displacement':displacement_cov.tolist(),
        'finite_pulse_endpoint_matrix':pulseH.tolist(),
        'expected_force_squared_integral':float(force_action),
        'girsanov_control_action':float(force_action/4),
        'scope':'Exact nominal linear-Gaussian plant equations and tilted '
        'dither identity. Finite range, calibration, pointer preparation, '
        'recycling and smooth meter edges are separate physical costs.'}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--interval',action='store_true')
    parser.add_argument('--pieces',type=int,default=100)
    args=parser.parse_args()
    if args.interval:
        rows=[]
        for j in range(args.pieces):
            lo=str(Decimal(j)/(4*Decimal(args.pieces)))
            hi=str(Decimal(j+1)/(4*Decimal(args.pieces)))
            r=iv_fixture([lo,hi],duration=(1,10),direct_arm=True)
            rows.append(r)
            print(json.dumps({'piece':j,'k':[lo,hi],
                'variance_upper':r['variance_upper'],
                'amplitude_upper':r['dither_sine_amplitude_upper'],
                'det_upper':r['position_feedback_determinant_upper'],
                'strict':r['strict_direct_arm_feasible']}),flush=True)
            assert r['strict_direct_arm_feasible']
        out={'arithmetic':'mpmath interval, 40 decimal digits',
            'domain':'0 <= k <= 1/4','all_strict':True,
            'uniform_variance_upper':max(r['variance_upper'] for r in rows),
            'uniform_amplitude_upper':max(r['dither_sine_amplitude_upper'] for r in rows),
            'determinant_upper':max(r['position_feedback_determinant_upper'] for r in rows),
            'pieces':rows}
        path=Path(__file__).with_name('p2_direct_sine_arm_interval.json')
    else:
        out={'construction':'Original eta=.5 sine arms; no second meter, no pin.',
            'rows':[direct_arm(k) for k in (0.,.01,.1,.25)]}
        for r in out['rows']:
            assert abs(r['position_feedback_gains_x_p_force'][0])<1e-12
            assert abs(r['final_x_residual_momentum_covariance'])<1e-12
        path=Path(__file__).with_suffix('.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(path)
