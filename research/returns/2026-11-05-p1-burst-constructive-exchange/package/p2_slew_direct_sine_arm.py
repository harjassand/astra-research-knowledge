"""Finite-slew canonical meter and exact original sine-arm preparation.

Every pointer uses a continuous trapezoidal coupling, with rise/fall duration
1/64, plateau 3/32, peak 1, and maximum slew 64 (gamma-normalized units).
Linear-ramp transition and Gaussian bath covariance are exact finite matrix
exponentials, not ODE sampling. --interval checks the continuum k in [0,1/4].
"""
import argparse
import json
from decimal import Decimal
from pathlib import Path
import mpmath as mp
import numpy as np
from scipy.linalg import expm
from scipy.integrate import quad


def ramp_piece(k,L,a,u,X):
    # Normalized clock v=t/L. J0'=x, J1'=J0.
    # g(v)=a+u*v, so integral g*x dt=L*((a+u)*J0-u*J1).
    # State x,p,J0,J1,P0,v*P0,F. P0 and F are constant inputs.
    A=X.zeros(7)
    A[0,1]=L
    A[1,0]=-k*L; A[1,1]=-L
    A[1,4]=-a*L; A[1,5]=-u*L; A[1,6]=L
    A[2,0]=1; A[3,2]=1; A[5,4]=1
    E=X.expm(A)
    D=X.matrix([[1,0,0,0,0,0,0],[0,1,0,0,0,0,0],
                [0,0,L*(a+u),-L*u,0,0,0]])
    T=D*E
    S=X.matrix([[T[0,0],T[0,1],0],
                [T[1,0],T[1,1],0],
                [T[2,0],T[2,1],1]])
    f=T[:,6]; p=T[:,4]
    # Only four dynamic states carry bath noise, so use an 8x8 Van Loan.
    A4=A[:4,:4]; VL=X.zeros(8)
    for i in range(4):
        for j in range(4):
            VL[i,j]=A4[i,j]; VL[i+4,j+4]=-A4[j,i]
    VL[1,5]=2*L
    EV=X.expm(VL); C4=EV[:4,4:]*EV[:4,:4].T
    D4=D[:,:4]
    C=D4*C4*D4.T
    return S,f,p,C


def cubic_ramp_piece(k,L,rising,X):
    # C1 smoothstep g=3v^2-2v^3 or its complement. Every coefficient is exact.
    coefficients=[0,0,3,-2] if rising else [1,0,-3,2]
    # x,p,J0,J1,J2,J3,P0,vP0,v^2P0,v^3P0,F.
    A=X.zeros(11)
    A[0,1]=L; A[1,0]=-k*L; A[1,1]=-L; A[1,10]=L
    for j in range(4): A[1,6+j]=-coefficients[j]*L
    A[2,0]=1
    for j in range(3,6): A[j,j-1]=1
    for j in range(1,4): A[6+j,5+j]=j
    E=X.expm(A)
    # Repeated integration by parts at v=1. Initial integrals are zero.
    qrow=[1,0,-6,12] if rising else [0,0,6,-12]
    D=X.zeros(3,11); D[0,0]=D[1,1]=1
    for j in range(4): D[2,2+j]=L*qrow[j]
    T=D*E
    S=X.matrix([[T[0,0],T[0,1],0],[T[1,0],T[1,1],0],
                [T[2,0],T[2,1],1]])
    f=T[:,10]; p=T[:,6]
    A6=A[:6,:6]; VL=X.zeros(12)
    for i in range(6):
        for j in range(6):
            VL[i,j]=A6[i,j]; VL[i+6,j+6]=-A6[j,i]
    VL[1,7]=2*L
    EV=X.expm(VL); C6=EV[:6,6:]*EV[:6,:6].T
    D6=D[:,:6]; C=D6*C6*D6.T
    return S,f,p,C


def slew_meter(k,X=mp.mp,profile='linear'):
    # The area of each trapezoid is 7/64; source backaction is included.
    rise=X.mpf(1)/64; plateau=X.mpf(3)/32
    Sw=X.eye(3); fw=X.zeros(3,1); pw=X.zeros(3,1); Cw=X.zeros(3)
    for L,a,u in ((rise,0,1),(plateau,1,0),(rise,1,-1)):
        if profile=='cubic' and u:
            S,f,p,C=cubic_ramp_piece(k,L,u>0,X)
        else:
            S,f,p,C=ramp_piece(k,L,a,u,X)
        Sw=S*Sw; fw=S*fw+f; pw=S*pw+p; Cw=S*Cw*S.T+C
    count=8; n=2+count; H=X.zeros(n,3+count); C=X.zeros(n)
    H[0,0]=H[1,1]=1
    for j in range(count):
        ix=[0,1,2+j]; S=X.eye(n)
        for a in range(3):
            for b in range(3): S[ix[a],ix[b]]=Sw[a,b]
        H=S*H
        for a in range(3):
            H[ix[a],2]+=fw[a]; H[ix[a],3+j]+=pw[a]
        C=S*C*S.T
        for a in range(3):
            for b in range(3): C[ix[a],ix[b]]+=Cw[a,b]
    Ho=H[2:,:].copy()
    for j in range(count): Ho[j,3+j]+=X.mpf(1)/100
    area=X.mpf(7)/64; Ho=Ho/area
    G=Ho[:,:3]; pvar=X.mpf(1)/100; qvar=X.mpf(1)/1000000
    S=C[2:,2:]/area**2+pvar*Ho[:,3:]*Ho[:,3:].T+qvar/area**2*X.eye(count)
    cross=C[2:,:2]/area+pvar*Ho[:,3:]*H[:2,3:].T
    Cm=C[:2,:2]+pvar*H[:2,3:]*H[:2,3:].T
    return G,S,cross,Cm,H[:2,:3]


def endpoint_matrices(k,X=mp.mp,profile='linear'):
    G,S,cross,Cm,Hm=slew_meter(k,X,profile=profile)
    duration=X.mpf(1)/10
    A=X.matrix([[0,1],[-k,-1]])
    A3=X.matrix([[0,1,0],[-k,-1,1],[0,0,0]])
    E3=X.expm(A3*duration); E=E3[:2,:2]
    hm=X.zeros(3)
    for i in range(2):
        for j in range(3): hm[i,j]=Hm[i,j]
    hm[2,2]=1; H=E3[:2,:]*hm
    VL=X.zeros(4)
    for i in range(2):
        for j in range(2):
            VL[i,j]=A[i,j]; VL[i+2,j+2]=-A[j,i]
    VL[1,3]=2
    EV=X.expm(VL*duration)
    C=E*Cm*E.T+EV[:2,2:]*EV[:2,:2].T
    crossf=cross*E.T
    return G,S,crossf,C,H


def as_numpy(a):
    return np.array([[float(a[i,j]) for j in range(a.cols)] for i in range(a.rows)])


def point(k,D0=1.,profile='linear'):
    mp.mp.dps=30
    G,S,cross,C,H=[as_numpy(a) for a in endpoint_matrices(mp.mpf(str(k)),profile=profile)]
    b=cross[:,1]
    SG=np.linalg.solve(S,G); sb=np.linalg.solve(S,b)
    w=sb+SG@np.linalg.solve(G.T@SG,H[1]-G.T@sb)
    v=float(C[1,1]-2*w@b+w@S@w)
    c=float(C[0,1]-w@cross[:,0]); q=b-S@w
    mat=np.array([G[[0,7],0],q[[0,7]]])
    s=np.zeros(8); s[[0,7]]=np.linalg.solve(mat,np.array([0.,-c]))
    r=1-v; amplitude=.5*np.exp(v/(2*r))
    gains=H.copy(); gains[0]+=s@G; gains[1]-=w@G
    xvar=C[0,0]+2*s@cross[:,0]+s@S@s
    lam=(1-np.sqrt(max(0.,1-4*k)))/2
    m=np.sqrt(2*D0*lam); f=(1-lam)*m
    TT=np.array([[0.,0.,0.],[0.,1+m*m,m*f],[0.,m*f,f*f]])
    d_gain=np.vstack([s@G,-w@G]); d_gain[0,0]=0.
    D=np.vstack([s,-w])@S@np.vstack([s,-w]).T+d_gain@TT@d_gain.T
    if k>0: D[1,1]+=(w@G)[0]**2/k
    D[1,1]+=r
    A=np.array([[0.,1.],[-k,-1.]]); B=np.array([[0.],[1.]])
    h=.1; pulse=np.zeros((2,2))
    for j in range(2):
        lo=j*h/2; hi=(j+1)*h/2
        for row in range(2):
            pulse[row,j]=quad(lambda t:(expm(A*(h-t))@B)[row,0]
                *np.sin(2*np.pi*(t-lo)/h)**2,lo,hi,epsabs=1e-13)[0]
    invpulse=np.linalg.inv(pulse)
    action=float(3*h/16*np.trace(invpulse@D@invpulse.T))
    return {'k':k,'lambda':float(lam),'eta':.5,'D0_for_action':D0,
        'meter_duration':1.,'control_duration':h,'nominal_duration':1.1,
        'coupling_profile':profile,'coupling_peak':1.,
        'coupling_maximum_slew':96. if profile=='cubic' else 64.,
        'pointer_rise_duration':1/64,'pointer_plateau_duration':3/32,
        'momentum_feedback_weights':w.tolist(),'position_feedback_weights':s.tolist(),
        'residual_momentum_variance':v,'dither_sine_amplitude':float(amplitude),
        'position_feedback_determinant':float(np.linalg.det(mat)),
        'position_feedback_initial_x_gain':float((s@G)[0]),
        'position_feedback_p_force_gains':(s@G)[1:].tolist(),
        'final_initial_gains_x_p_force':gains.tolist(),
        'final_x_residual_momentum_covariance':float(c+s@q),
        'final_x_gaussian_noise_variance':float(xvar),
        'expected_force_squared_integral':action,'girsanov_control_action':action/4,
        'finite_force_endpoint_matrix':pulse.tolist(),
        'scope':'Exact continuous piecewise-linear meter coupling, bounded slew. '
          'Classical Gaussian pointer preparation and calibrated parameters assumed; '
          'finite ranges, ADC/DAC precision, reuse and preparation costs separate.'}


def interval_piece(lo,hi,profile='linear'):
    X=mp.iv; X.dps=40; k=X.mpf([lo,hi])
    G,S,cross,C,H=endpoint_matrices(k,X,profile=profile)
    mid=(float(lo)+float(hi))/2
    base=[repr(float(z)) for z in point(mid,profile=profile)['momentum_feedback_weights']]
    w0=X.matrix([X.mpf(t) for t in base])
    hh=X.matrix([H[1,j] for j in range(3)])
    ix=[0,3,7]; small=X.matrix([[G[j,i] for j in ix] for i in range(3)])
    delta=small**-1*(hh-G.T*w0); w=w0.copy()
    for j,i in enumerate(ix): w[i]+=delta[j]
    b=cross[:,1]
    v=C[1,1]-2*(w.T*b)[0]+(w.T*S*w)[0]
    c=C[0,1]-(w.T*cross[:,0])[0]; q=b-S*w
    mat=X.matrix([[G[0,0],G[7,0]],[q[0],q[7]]])
    det=mat[0,0]*mat[1,1]-mat[0,1]*mat[1,0]
    s=mat**-1*X.matrix([0,-c])
    amplitude=X.mpf(1)/2*X.exp(v/(2*(1-v)))
    return {'k_interval':[lo,hi],'candidate_rational_weights':base,
       'gain_correction_indices':ix,'position_feedback_indices':[0,7],
       'residual_variance':str(v),'variance_upper':float(v.b),
       'position_feedback_determinant':str(det),'determinant_upper':float(det.b),
       'position_feedback_weights':[str(z) for z in s],
       'dither_sine_amplitude':str(amplitude),'amplitude_upper':float(amplitude.b),
       'strict':bool(v.b<1 and amplitude.b<1 and det.b<0)}


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
            r=interval_piece(lo,hi); rows.append(r)
            print(json.dumps({'piece':j,'k':[lo,hi],'upper':r['variance_upper'],
                'amplitude':r['amplitude_upper'],'det_upper':r['determinant_upper'],
                'strict':r['strict']}),flush=True)
            assert r['strict']
        result={'arithmetic':'mpmath directed interval, 40 decimal digits',
            'model':'Continuous trapezoidal canonical meter coupling; no step edges.',
            'domain':'0 <= k <= 1/4','all_strict':True,
            'uniform_variance_upper':max(r['variance_upper'] for r in rows),
            'uniform_amplitude_upper':max(r['amplitude_upper'] for r in rows),
            'determinant_upper':max(r['determinant_upper'] for r in rows),'pieces':rows}
        path=Path(__file__).with_name('p2_slew_direct_sine_arm_interval.json')
    else:
        result={'model':'Finite-slew meter and original eta=.5 sine arms',
                'rows':[point(k) for k in (0.,.01,.1,.25)]}
        for r in result['rows']:
            assert r['dither_sine_amplitude']<1
            assert abs(r['position_feedback_initial_x_gain'])<1e-12
            assert abs(r['final_x_residual_momentum_covariance'])<1e-12
        path=Path(__file__).with_suffix('.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(path)
