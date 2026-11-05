"""Finite Gaussian measurement/feedforward reset certificate.

This checks a classical linear SDE and finite canonical-pointer model, not
hardware.  The source x,p and constant unknown force f are arbitrary inputs.
Fresh pointer and thermostat noises are Gaussian.  The meter calculation
follows the independently constructed gaussian_meter_probe.py in this folder.

Run normally for floating arithmetic checks; --interval encloses the key
positive variance slack with mpmath interval arithmetic for one rational
parameter fixture.  No simulation or asymptotic fit is used.
"""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm


def meter(k=1., tau=1., count=8, qvar=1e-6, pvar=.01,
          pointer_mass=100., gain=1., gamma=1., mass=1., sigma=1.):
    n=3+2*count
    f=n-1
    ps=slice(2,2+count)
    qs=slice(2+count,2+2*count)
    total=np.eye(n)
    cov=np.zeros((n,n))
    cov[ps,ps]=pvar*np.eye(count)
    cov[qs,qs]=qvar*np.eye(count)
    width=tau/count
    for j in range(count):
        A=np.zeros((n,n))
        A[0,1]=1/mass
        A[1,0]=-k
        A[1,1]=-gamma
        A[1,f]=1
        A[1,2+j]=-gain
        for l in range(count):
            A[2+count+l,2+l]=1/pointer_mass
        A[2+count+j,0]=gain
        D=np.zeros((n,n))
        D[1,1]=2*gamma*sigma*sigma
        V=np.block([[A,D],[np.zeros_like(A),-A.T]])
        E=expm(V*width)
        S=E[:n,:n]
        G=E[:n,n:]@S.T
        cov=S@cov@S.T+G
        total=S@total
    read=np.zeros((count,n))
    for j in range(count):
        read[j,2+count+j]=1/(gain*width)
    means=read@total[:,[0,1,f]]
    cross=read@cov[:,:2]
    constraints=np.column_stack([means,cross])
    V=read@cov@read.T
    rhs=np.array([0.,1.,0.,0.,0.])
    Z=np.linalg.solve(V,constraints)
    w=Z@np.linalg.solve(constraints.T@Z,rhs)
    return w, float(w@V@w), cov[:2,:2], constraints, means, cross


def construction(k=1., tau=1., count=8, qvar=1e-6, pvar=.01,
                 pointer_mass=100., gain=1., control_duration=1.,
                 initial_p_second_moment=1.):
    # The normalized fixture has mass=gamma=sigma=1.
    w,v,Cm,con,means,cross=meter(k,tau,count,qvar,pvar,pointer_mass,gain)
    A=np.array([[0.,1.],[-k,-1.]])
    B=np.array([[0.],[1.]])
    Sigma=np.diag([1/k,1.])
    omega=np.sqrt(k-.25)
    T=2*np.pi/omega
    attenuation=np.exp(-T/2)
    assert T>tau+control_duration
    Erem=expm(A*(T-tau))
    Cbase=Erem@Cm@Erem.T+Sigma-Erem@Sigma@Erem.T
    Cbase=(Cbase+Cbase.T)/2
    c=float(Cbase[0,1])
    Vp=float(Cbase[1,1]+attenuation**2*v)
    slack=1.-Vp
    assert slack>0
    dither=np.array([[c*c/slack,-c],[-c,slack]])
    final_cov=Cbase.copy()
    final_cov[1,1]+=attenuation**2*v
    final_cov+=dither
    # Exact mathematical base gain at the full damped-oscillator period.
    base_gain=np.array([[attenuation,0.,(1-attenuation)/k],
                        [0.,attenuation,0.]])
    final_gain=base_gain.copy()
    final_gain[1,:]-=attenuation*(w@means)
    transformed_meter_cross=(w@cross)@Erem.T
    # Finite minimum-L2 force on the final control interval: u(s)=
    # B^T exp(A^T(T-s)) W^{-1} d, where W is the controllability Gramian.
    D=B@B.T
    block=np.block([[A,D],[np.zeros_like(A),-A.T]])
    E=expm(block*control_duration)
    W=E[:2,2:]@E[:2,:2].T
    W=(W+W.T)/2
    desired_second=np.array([[c*c/slack,-c],[-c,
        attenuation**2*(initial_p_second_moment+v)+slack]])
    expected_force_L2=float(np.trace(np.linalg.solve(W,desired_second)))
    # Direct endpoint integration check for two basis displacements.
    nodes,weights=np.polynomial.legendre.leggauss(80)
    integral=np.zeros((2,2))
    for z,wt in zip(nodes,weights):
        remaining=(z+1)*control_duration/2
        e=expm(A*remaining)
        integral+=wt*(e@D@e.T)@np.linalg.inv(W)*control_duration/2
    # An independent backaction-only expression checks the variance margin.
    coeff=[]
    width=tau/count
    for j in range(count):
        q=-gain*np.linalg.solve(A,(expm(-A*(j+1)*width)-
                                  expm(-A*j*width))@B)
        coeff.append(q[:,0])
    backaction_over_a2=pvar*sum(np.outer(q,q) for q in coeff)
    delta_ratio=float(backaction_over_a2[1,1])
    return {
        'k_total':k,'meter_time':tau,'reset_total_time':float(T),
        'control_time':control_duration,'pointer_count':count,
        'pointer_q_variance':qvar,'pointer_p_variance':pvar,
        'pointer_mass':pointer_mass,'gain':gain,
        'meter_variance':v,'meter_weights':w.tolist(),
        'attenuation':float(attenuation),
        'meter_backaction_momentum_variance_over_a2':delta_ratio,
        'variance_budget_sum':v+delta_ratio,
        'variance_slack':slack,
        'uncontrolled_endpoint_covariance':Cbase.tolist(),
        'fresh_dither_covariance':dither.tolist(),
        'final_endpoint_covariance':final_cov.tolist(),
        'final_initial_gains_x_p_force':final_gain.tolist(),
        'meter_endpoint_noise_covariance':transformed_meter_cross.tolist(),
        'meter_constraint_residual':float(np.max(np.abs(con.T@w-
                                      np.array([0.,1.,0.,0.,0.])))),
        'endpoint_covariance_residual':float(max(abs(final_cov[1,1]-1),
                                               abs(final_cov[0,1]))),
        'endpoint_input_gain_residual':float(np.max(np.abs(final_gain[1]))),
        'controllability_eigenvalues':np.linalg.eigvalsh(W).tolist(),
        'pulse_endpoint_integral_residual':float(np.max(np.abs(integral-np.eye(2)))),
        'expected_force_squared_integral_for_Ep2':expected_force_L2,
        'girsanov_action_for_Ep2':expected_force_L2/4,
        'initial_p_second_moment_for_cost':initial_p_second_moment,
        'variance_identity_residual':float(abs(slack-
            attenuation**2*(1-v-delta_ratio))),
        'scope':'Classical finite linear SDE and canonical pointers. Algebraic '
                'reset, not a device test. Temporary fine readings and dither '
                'seeds must be isolated/discarded before launch.'
    }


def interval_certificate():
    import mpmath as mp
    I=mp.iv
    I.dps=45
    z=I.mpf(0)
    count=8
    n=3+2*count
    force=n-1
    pvar=I.mpf(1)/100
    qvar=I.mpf(1)/1000000
    width=I.mpf(1)/count
    total=I.eye(n)
    cov=I.zeros(n)
    for j in range(count):
        cov[2+j,2+j]=pvar
        cov[2+count+j,2+count+j]=qvar
    for j in range(count):
        A=I.zeros(n)
        A[0,1]=1
        A[1,0]=-1
        A[1,1]=-1
        A[1,force]=1
        A[1,2+j]=-1
        for l in range(count):
            A[2+count+l,2+l]=I.mpf(1)/100
        A[2+count+j,0]=1
        V=I.zeros(2*n)
        for r in range(n):
            for c in range(n):
                V[r,c]=A[r,c]
                V[r+n,c+n]=-A[c,r]
        V[1,n+1]=2
        E=I.expm(V*width)
        S=E[:n,:n]
        G=E[:n,n:] * S.T
        cov=S*cov*S.T+G
        total=S*total
    read=I.zeros(count,n)
    for j in range(count):
        read[j,2+count+j]=count
    means=I.zeros(count,3)
    for j,col in enumerate((0,1,force)):
        for r in range(count):
            means[r,j]=(read*total)[r,col]
    cross=read*cov[:,:2]
    D=I.zeros(count,5)
    for r in range(count):
        for c in range(3):
            D[r,c]=means[r,c]
        for c in range(2):
            D[r,c+3]=cross[r,c]
    V=read*cov*read.T
    rhs=I.matrix([0,1,0,0,0])
    Z=V**-1 * D
    w=Z*(D.T*Z)**-1*rhs
    v=(w.T*V*w)[0]
    A=I.matrix([[0,1],[-1,-1]])
    B=I.matrix([0,1])
    delta=z
    for j in range(count):
        q=-(A**-1)*(I.expm(-A*(j+1)*width)-I.expm(-A*j*width))*B
        delta+=pvar*q[1]**2
    budget=v+delta
    assert budget.b < 1
    return {'arithmetic':'mpmath interval, 45 decimal digits',
            'rational_fixture':{'k':1,'gamma':1,'M':1,'sigma':1,
              'tau':1,'count':8,'qvar':'1/1000000','pvar':'1/100',
              'pointer_mass':100,'gain':1},
            'meter_variance_enclosure':str(v),
            'backaction_over_a2_enclosure':str(delta),
            'variance_budget_enclosure':str(budget),
            'strict_slack_verified':True}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--interval',action='store_true')
    args=parser.parse_args()
    if args.interval:
        ans=interval_certificate()
        target=Path(__file__).with_name('p2_reset_interval.json')
    else:
        rows=[construction(k=k) for k in (1.,1.1,1.25)]
        for r in rows:
            assert r['meter_constraint_residual']<1e-8
            assert r['endpoint_input_gain_residual']<1e-9
            assert r['endpoint_covariance_residual']<1e-12
            assert r['pulse_endpoint_integral_residual']<1e-10
            assert r['variance_identity_residual']<1e-12
        ans={'status':'all Gaussian gain/covariance and finite-pulse checks passed',
             'physical_trials':0,'results':rows}
        target=Path(__file__).with_suffix('.json')
    target.write_text(json.dumps(ans,indent=2)+'\n')
    print(json.dumps(ans,indent=2))
