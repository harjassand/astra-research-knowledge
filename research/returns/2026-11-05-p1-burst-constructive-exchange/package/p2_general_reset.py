"""Original-plant reset: finite position pointers plus additive force only.

No harmonic pin and no observation of the hidden constant force are needed.
The construction is an affine Gaussian channel calculation.  --interval
certifies a uniform variance margin by interval arithmetic on k in [0,1/4].
"""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.integrate import quad
from gaussian_meter_probe import construct as full_meter


def reduced_meter(k, count=8, tau=1., qvar=1e-6, pvar=.01,
                  pointer_mass=100., gain=1.):
    # State source(x,p), accumulated coupling contributions to pointer Q_j.
    # Inputs initial x,p,force and independent initial pointer P_j.
    n=2+count
    inp=3+count
    H=np.zeros((n,inp)); H[0,0]=H[1,1]=1.
    C=np.zeros((n,n))
    A=np.array([[0.,1.,0.],[-k,-1.,0.],[gain,0.,0.]])
    D=np.zeros((3,3)); D[1,1]=2.
    VL=np.block([[A,D],[np.zeros((3,3)),-A.T]])
    E=expm(VL*(tau/count)); S3=E[:3,:3]
    Q3=E[:3,3:]@S3.T
    aug=np.zeros((4,4)); aug[:3,:3]=A; aug[1,3]=1.
    b=expm(aug*(tau/count))[:3,3]
    for j in range(count):
        ix=[0,1,2+j]; S=np.eye(n); S[np.ix_(ix,ix)]=S3
        H=S@H
        H[ix,2]+=b
        H[ix,3+j]-=gain*b
        C=S@C@S.T
        C[np.ix_(ix,ix)]+=Q3
    Hobs=H[2:,:].copy()
    for j in range(count): Hobs[j,3+j]+=tau/pointer_mass
    Hobs/=gain*tau/count
    G=Hobs[:,:3]
    V=C[2:,2:]/(gain*tau/count)**2+pvar*Hobs[:,3:]@Hobs[:,3:].T
    V+=qvar/(gain*tau/count)**2*np.eye(count)
    cross=C[2:,:2]/(gain*tau/count)+pvar*Hobs[:,3:]@H[:2,3:].T
    Cs=C[:2,:2]+pvar*H[:2,3:]@H[:2,3:].T
    return G,V,cross,Cs,H[:2,:3]


def reset(k, tau_control=.2, D0=1.):
    G,V,cross,Cm,Hm=reduced_meter(k)
    A=np.array([[0.,1.],[-k,-1.]])
    A3=np.array([[0.,1.,0.],[-k,-1.,1.],[0.,0.,0.]])
    E3=expm(A3*tau_control); E=E3[:2,:2]
    hm=np.vstack([Hm,np.array([0.,0.,1.])]); H=E3[:2,:]@hm
    B=np.array([[0.],[1.]])
    VL=np.block([[A,2*B@B.T],[np.zeros((2,2)),-A.T]])
    ev=expm(VL*tau_control)
    Cf=E@Cm@E.T+ev[:2,2:]@ev[:2,:2].T
    crossf=cross@E.T
    cp=crossf[:,1]
    Z=np.linalg.solve(V,G); z=np.linalg.solve(V,cp)
    w=z+Z@np.linalg.solve(G.T@Z,H[1]-G.T@z)
    residual_var=float(Cf[1,1]-2*w@cp+w@V@w)
    residual_cross=float(Cf[0,1]-w@crossf[:,0])
    slack=1-residual_var
    assert slack>0
    dither=np.array([[residual_cross**2/slack,-residual_cross],
                     [-residual_cross,slack]])
    final_gain=H.copy(); final_gain[1]-=w@G
    final_cov=Cf.copy()
    final_cov[1,1]=residual_var
    final_cov[0,1]=final_cov[1,0]=residual_cross
    final_cov+=dither
    # Two finite C1 pulse shapes; both vanish with zero derivative at edges.
    dur=tau_control
    pulseH=np.zeros((2,2))
    for j in range(2):
        lo=j*dur/2; hi=(j+1)*dur/2
        for row in range(2):
            pulseH[row,j]=quad(lambda s: (expm(A*(dur-s))@B)[row,0]
                *np.sin(2*np.pi*(s-lo)/dur)**2,lo,hi,epsabs=1e-13)[0]
    # Original hard fixture has k=lambda(1-lambda), gamma=M=sigma=1.
    lam=(1-np.sqrt(max(0.,1-4*k)))/2
    m=np.sqrt(2*D0*lam); f=(1-lam)*m
    h=H[1]
    mean_gain_second=(h[0]**2/k if k>0 else 0.)+h[1]**2*(1+m*m)+h[2]**2*f*f+2*h[1]*h[2]*m*f
    EY2=float(w@V@w+mean_gain_second)
    target_second=np.array([[dither[0,0],-residual_cross],
                            [-residual_cross,EY2+slack]])
    invH=np.linalg.inv(pulseH)
    coeff_second=invH@target_second@invH.T
    forceL2=float(3*dur/16*np.trace(coeff_second))
    return {'k':float(k),'lambda':float(lam),'D0_for_cost':D0,
      'meter_duration':1.,'control_duration':dur,'total_reset_duration':1+dur,
      'weights':w.tolist(),'initial_p_prediction_gains':h.tolist(),
      'predictor_noise_variance':float(w@V@w),
      'residual_p_variance':residual_var,'residual_px_covariance':residual_cross,
      'thermal_variance_slack':slack,'dither_covariance':dither.tolist(),
      'final_initial_gains_x_p_force':final_gain.tolist(),
      'final_noise_covariance':final_cov.tolist(),
      'gain_residual':float(np.max(np.abs(final_gain[1]))),
      'covariance_residual':float(max(abs(final_cov[1,1]-1),abs(final_cov[0,1]))),
      'finite_pulse_endpoint_matrix':pulseH.tolist(),
      'finite_pulse_matrix_determinant':float(np.linalg.det(pulseH)),
      'expected_force_squared_integral':forceL2,
      'girsanov_control_action':forceL2/4,
      'meter_parameters':{'count':8,'Q_variance':1e-6,'P_variance':.01,
                          'pointer_mass':100.,'coupling_gain':1.},
      'scope':'Finite classical Gaussian instrument and additive force model. '
              'No pin. Exact equations define the weights; numerical gains '
              'and covariances are checks, not experimental data.'}


def iv_fixture(k_interval, dps=40, duration=(1,5), direct_arm=False):
    import mpmath as mp
    I=mp.iv; I.dps=dps
    k=I.mpf(k_interval); count=8; n=2+count; inp=3+count
    H=I.zeros(n,inp); H[0,0]=H[1,1]=1
    C=I.zeros(n); width=I.mpf(1)/8
    A=I.matrix([[0,1,0],[-k,-1,0],[1,0,0]])
    VL=I.zeros(6)
    for r in range(3):
        for c in range(3): VL[r,c]=A[r,c]; VL[r+3,c+3]=-A[c,r]
    VL[1,4]=2
    ev=I.expm(VL*width); S3=ev[:3,:3]; Q3=ev[:3,3:]*S3.T
    aug=I.zeros(4)
    for r in range(3):
        for c in range(3): aug[r,c]=A[r,c]
    aug[1,3]=1
    b=I.expm(aug*width)[:3,3]
    for j in range(count):
        ix=[0,1,2+j]; S=I.eye(n)
        for r in range(3):
            for c in range(3): S[ix[r],ix[c]]=S3[r,c]
        H=S*H
        for r in range(3): H[ix[r],2]+=b[r]; H[ix[r],3+j]-=b[r]
        C=S*C*S.T
        for r in range(3):
            for c in range(3): C[ix[r],ix[c]]+=Q3[r,c]
    Ho=H[2:,:].copy()
    for j in range(count): Ho[j,3+j]+=I.mpf(1)/100
    Ho=Ho/width
    G=Ho[:,:3]
    pvar=I.mpf(1)/100; qvar=I.mpf(1)/1000000
    V=C[2:,2:]/width**2+pvar*Ho[:,3:]*Ho[:,3:].T+qvar/width**2*I.eye(count)
    cross=C[2:,:2]/width+pvar*Ho[:,3:]*H[:2,3:].T
    Cm=C[:2,:2]+pvar*H[:2,3:]*H[:2,3:].T
    dur=I.mpf(duration[0])/duration[1]
    A2=I.matrix([[0,1],[-k,-1]])
    A3=I.matrix([[0,1,0],[-k,-1,1],[0,0,0]])
    E3=I.expm(A3*dur); E=E3[:2,:2]
    hm=I.zeros(3)
    for r in range(2):
        for c in range(3): hm[r,c]=H[r,c]
    hm[2,2]=1
    HF=E3[:2,:]*hm
    vv=I.zeros(4)
    for r in range(2):
        for c in range(2): vv[r,c]=A2[r,c]; vv[r+2,c+2]=-A2[c,r]
    vv[1,3]=2
    ee=I.expm(vv*dur)
    CF=E*Cm*E.T+ee[:2,2:]*ee[:2,:2].T
    XF=cross*E.T
    cp=XF[:,1]
    hh=I.matrix([HF[1,j] for j in range(3)])
    # Do not interval-invert a highly correlated observation covariance.
    # Any exactly mean-correct candidate upper-bounds the optimal residual
    # variance. Start with a rational, fixed midpoint candidate and correct
    # only three coefficients using a uniformly nonsingular gain submatrix.
    lo=float(k_interval[0]); hi=float(k_interval[1])
    base=[repr(float(t)) for t in reset((lo+hi)/2,tau_control=float(duration[0])/duration[1])['weights']]
    w0=I.matrix([I.mpf(t) for t in base])
    indices=(0,3,7)
    small=I.matrix([[G[j,i] for j in indices] for i in range(3)])
    correction=small**-1*(hh-G.T*w0)
    w=w0.copy()
    for j,ix in enumerate(indices): w[ix]+=correction[j]
    vr=CF[1,1]-2*(w.T*cp)[0]+(w.T*V*w)[0]
    cc=CF[0,1]-(w.T*XF[:,0])[0]
    result={'k_interval':list(k_interval) if isinstance(k_interval,(list,tuple)) else str(k_interval),
            'residual_variance':str(vr),'residual_cross':str(cc),
            'variance_upper':float(vr.b),'variance_lower':float(vr.a),
            'candidate_rational_weights':base,'gain_correction_indices':list(indices),
            'certificate':'Exactly mean-correct candidate; constrained minimum variance is no larger.',
            'strict_slack':bool(vr.b<1)}
    if direct_arm:
        q=cp-V*w
        mat=I.matrix([[G[0,0],G[7,0]],[q[0],q[7]]])
        det=mat[0,0]*mat[1,1]-mat[0,1]*mat[1,0]
        sv=mat**-1*I.matrix([0,-cc])
        amplitude=I.mpf(1)/2*I.exp(vr/(2*(1-vr)))
        result.update({'control_duration':str(dur),
            'position_feedback_indices':[0,7],
            'position_feedback_determinant':str(det),
            'position_feedback_determinant_upper':float(det.b),
            'position_feedback_weights':[str(z) for z in sv],
            'eta':'.5','dither_sine_amplitude':str(amplitude),
            'dither_sine_amplitude_upper':float(amplitude.b),
            'strict_direct_arm_feasible':bool(amplitude.b<1 and det.b<0)})
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--interval',action='store_true')
    parser.add_argument('--pieces',type=int,default=100)
    args=parser.parse_args()
    if args.interval:
        # Directed decimal endpoints; exactly cover [0,1/4].
        from decimal import Decimal
        rows=[]
        for j in range(args.pieces):
            lo=str(Decimal(j)/(4*Decimal(args.pieces)))
            hi=str(Decimal(j+1)/(4*Decimal(args.pieces)))
            r=iv_fixture([lo,hi]); rows.append(r)
            print(json.dumps({'piece':j,'k':[lo,hi],'upper':r['variance_upper'],
                              'strict':r['strict_slack']}),flush=True)
            assert r['strict_slack']
        ans={'arithmetic':'mpmath interval, 40 decimal digits',
             'domain':'0 <= k <= 1/4','all_strict':True,
             'uniform_variance_upper':max(r['variance_upper'] for r in rows),
             'pieces':rows}
        path=Path(__file__).with_name('p2_general_reset_interval.json')
    else:
        # Independent reduced vs full canonical-pointer covariance check.
        for k in (0.,.1,.25):
            G,V,cross,Cs,H=reduced_meter(k)
            a=full_meter(k=k,tau=1.,count=8,qvar=1e-6,pvar=.01,
                         pointer_mass=100.,return_matrices=True)['matrices']
            f=a['total'].shape[0]-1
            assert np.max(np.abs(G-a['readout']@a['total'][:,[0,1,f]]))<1e-12
            assert np.max(np.abs(V-a['observation_covariance']))<1e-12
            assert np.max(np.abs(cross-a['readout']@a['covariance'][:,:2]))<1e-12
            assert np.max(np.abs(Cs-a['covariance'][:2,:2]))<1e-12
        rows=[reset(k) for k in (0.,.01,.1,.25)]
        assert max(r['gain_residual'] for r in rows)<1e-10
        assert max(r['covariance_residual'] for r in rows)<1e-12
        ans={'status':'reduced/full model and finite reset checks passed',
             'physical_trials':0,'results':rows}
        path=Path(__file__).with_suffix('.json')
    path.write_text(json.dumps(ans,indent=2)+'\n')
    print(json.dumps(ans,indent=2))
