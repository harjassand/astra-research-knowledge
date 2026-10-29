"""Finite one-port preparation/readout/reset and nonperturbative energy fit.

Independent of root_nonlinear_port. Synthetic classical coherent model;
floating integration/noise is diagnostic, not a physical acquisition or a
validated ODE solver. The learner never receives physical K or its axes.
"""
from pathlib import Path
from fractions import Fraction as F
import itertools,json,math,time
import numpy as np
from scipy.linalg import expm,svd
from scipy.integrate import solve_ivp
from scipy.optimize import linear_sum_assignment


def rational_source():
    n=5;v=[F(1),F(-2),F(-3),F(-4),F(-5)]
    # Rational unit vector c; rational Householder B has first row c.
    c=[F(53,55),F(4,55),F(6,55),F(8,55),F(10,55)]
    w=[F(int(j==0))-c[j] for j in range(n)];ww=sum(x*x for x in w)
    B=[[F(int(i==j))-2*w[i]*w[j]/ww for j in range(n)] for i in range(n)]
    R=[[F(int(i==j)) for j in range(n)] for i in range(n)]
    for i,j,co,si in ((1,2,F(3,5),F(4,5)),(2,3,F(5,13),F(12,13)),
                       (3,4,F(8,17),F(15,17)),(1,4,F(7,25),F(24,25))):
        G=[[F(int(a==b)) for b in range(n)] for a in range(n)]
        G[i][i]=G[j][j]=co;G[i][j]=-si;G[j][i]=si
        R=[[sum(G[a][k]*R[k][b] for k in range(n)) for b in range(n)] for a in range(n)]
    Q=[[sum(R[a][k]*B[k][b] for k in range(n)) for b in range(n)] for a in range(n)]
    assert all(sum(Q[k][i]*Q[k][j] for k in range(n))==int(i==j) for i in range(n) for j in range(n))
    lam=[F(2,5),F(9,10),F(3,2),F(11,5),F(3)]
    K=[[sum(Q[i][k]*lam[k]*Q[j][k] for k in range(n)) for j in range(n)] for i in range(n)]
    return Q,K,lam,c


class SyntheticPort:
    def __init__(self):
        self.qr,self.kr,self.lr,self.cr=rational_source()
        self.Q=np.array(self.qr,float);self.K=np.array(self.kr,float)
        self.lam=np.array(self.lr,float);self.c=np.array(self.cr,float)
        self.n=5;self.ode_calls=0;self.ode_evaluations=0
    def U(self,t):return (self.Q*np.exp(-1j*self.lam*t))@self.Q.T
    def prepare_matrix(self,h,L):
        t=(np.arange(L)+.5)*h
        return self.Q@(self.c[:,None]*np.exp(-1j*self.lam[:,None]*(L*h-t))*h*np.sinc(self.lam[:,None]*h/(2*np.pi)))
    def readout_matrix(self,times):return np.exp(-1j*np.asarray(times)[:,None]*self.lam)*self.c@self.Q.T
    def calibration(self,dt,length,amplitude=1.,pulse=.2):
        f=pulse*np.sinc(self.lam*pulse/(2*np.pi))*np.exp(-1j*self.lam*pulse/2)
        return np.exp(-1j*np.arange(length)[:,None]*dt*self.lam)@(amplitude*self.c**2*f)
    def nonlinear(self,z,t,g):
        def rhs(_,x):return -1j*(self.K@x+g*np.abs(x)**2*x)
        r=solve_ivp(rhs,(0,t),z,method='DOP853',rtol=2e-12,atol=2e-14)
        assert r.success
        self.ode_calls+=1;self.ode_evaluations+=r.nfev
        return r.y[:,-1]


def calibration(y,dt,n,pulse=.2):
    L=(len(y)-1)//2
    H0=np.array([[y[i+j] for j in range(L)] for i in range(L)])
    H1=np.array([[y[i+j+1] for j in range(L)] for i in range(L)])
    U,s,Vh=svd(H0,full_matrices=False);U=U[:,:n];V=Vh[:n].conj().T
    pole=np.linalg.eigvals((U.conj().T@H1@V)/s[:n][None,:])
    lam=np.sort(-np.angle(pole)/dt)
    A=np.exp(-1j*np.arange(len(y))[:,None]*dt*lam)
    coeff=np.linalg.lstsq(A,y,rcond=None)[0]
    f=pulse*np.sinc(lam*pulse/(2*np.pi))*np.exp(-1j*lam*pulse/2)
    weights=(coeff/f).real
    assert np.min(weights)>0
    c=np.sqrt(weights/weights.sum())
    return lam,c,{'hankel_nonzero_sigma_min':float(s[n-1]),'hankel_sigma_next':float(s[n]),
                  'Vandermonde_sigma_min':float(np.linalg.svd(A,compute_uv=False)[-1]),
                  'spectral_gap':float(np.diff(lam).min()),'minimum_port_overlap':float(c.min()),
                  'fit_residual':float(np.linalg.norm(A@coeff-y))}


def features(X):
    """Orthonormal real Sym4 coefficient convention; X columns are states."""
    n=X.shape[0];keys=list(itertools.combinations_with_replacement(range(n),4))
    out=[];perms=[]
    for key in keys:
        pp=sorted(set(itertools.permutations(key)));perms.append(pp)
        out.append(sum((X[a]*X[b].conj()*X[c]*X[d].conj()).real for a,b,c,d in pp)/math.sqrt(len(pp)))
    return np.array(out).T,keys,perms


def tensor_from(theta,n,perms):
    T=np.zeros((n,n,n,n))
    for value,pp in zip(theta,perms):
        for indices in pp:T[indices]=value/math.sqrt(len(pp))
    return T


def recover_axes(T,seed=917):
    rng=np.random.default_rng(seed);attempts=[];best=None
    for _ in range(16):
        w=rng.normal(size=T.shape[0]);w/=np.linalg.norm(w)
        A=np.einsum('abcd,c,d->ab',T,w,w)
        val,V=np.linalg.eigh(A);gap=float(np.diff(val).min())
        attempts.append(gap)
        if best is None or gap>best[0]:best=(gap,V,w)
    return best,attempts


def gauge_error(Qhat,Khat,oracle):
    overlap=np.abs(Qhat@oracle.Q.T)
    row,col=linear_sum_assignment(-overlap)
    signs=np.sign(np.sum(Qhat[row]*oracle.Q[col],axis=1))
    aligned=np.empty_like(Qhat);aligned[col]=Qhat[row]*signs[:,None]
    return {'axes_frobenius':float(np.linalg.norm(aligned-oracle.Q)),
            'K_frobenius':float(np.linalg.norm(aligned@Khat@aligned.T-oracle.K)),
            'signed_permutation':[[int(a),int(b),int(s)] for a,b,s in zip(row,col,signs)]}


def run():
    root=Path(__file__).parent;start=time.perf_counter();oracle=SyntheticPort()
    rng=np.random.default_rng(202610299700);n=5
    # Actual finite rectangular linear pulse and64 scalar complex samples.
    dt=.5;linear=oracle.calibration(dt,65)
    linnoise=1e-13*np.exp(2j*np.pi*rng.random(len(linear)))
    lam,c,cal=calibration(linear+linnoise,dt,n)
    Khat=np.diag(lam);Tprep=16.;L=32;h=Tprep/L
    Bhat=c[:,None]*np.exp(-1j*lam[:,None]*(Tprep-(np.arange(L)+.5)*h))*h*np.sinc(lam[:,None]*h/(2*np.pi))
    Bphys=oracle.prepare_matrix(h,L);Bpin=np.linalg.pinv(Bhat)
    times=np.arange(32)*.5;Tread=times[-1]
    Chat=np.exp(-1j*times[:,None]*lam)*c;Cphys=oracle.readout_matrix(times)
    Cpin=np.linalg.pinv(Chat);evolve_read=np.exp(-1j*lam*Tread)
    rngx=np.random.default_rng(202610299701)
    m=math.comb(n+3,4);directions=rngx.normal(size=(n,m))+1j*rngx.normal(size=(n,m))
    directions/=np.linalg.norm(directions,axis=0)
    durations=rngx.uniform(.7,1.3,size=m);g=.35;radii=(1.,1.5);noise=1e-9
    X=[];Y=[];raw_pre=[];raw_post=[];taus=[];drive_energy=[];peak=[];reset_residual=[];energy_defects=[]
    residue=np.zeros(n,complex);ode_initial=[];ode_final=[]
    tick=time.perf_counter()
    for j in range(m):
        for radius in radii:
            target=radius*directions[:,j];command=Bpin@target
            pre=oracle.U(Tprep)@residue+Bphys@command
            yp=Cphys@pre+noise*np.exp(2j*np.pi*rng.random(len(times)))
            x=evolve_read*(Cpin@yp)
            initial=oracle.U(Tread)@pre
            final=oracle.nonlinear(initial,float(durations[j]),g)
            yo=Cphys@final+noise*np.exp(2j*np.pi*rng.random(len(times)))
            y=Cpin@yo
            # Coherent reset through the SAME finite linear control frame.
            reset=-Bpin@(np.exp(-1j*lam*Tprep)*evolve_read*y)
            residue=oracle.U(Tprep+Tread)@final+Bphys@reset
            X.append(x);Y.append(y);raw_pre.append(yp);raw_post.append(yo);taus.append(durations[j])
            peak.append(max(np.abs(command).max(),np.abs(reset).max()))
            drive_energy.append(h*(np.vdot(command,command).real+np.vdot(reset,reset).real))
            reset_residual.append(np.linalg.norm(residue))
            ein=np.vdot(initial,oracle.K@initial).real+g/2*np.sum(np.abs(initial)**4)
            eout=np.vdot(final,oracle.K@final).real+g/2*np.sum(np.abs(final)**4)
            energy_defects.append(eout-ein);ode_initial.append(initial);ode_final.append(final)
    acquire_seconds=time.perf_counter()-tick
    X=np.array(X).T;Y=np.array(Y).T
    fi,keys,perms=features(X);fo,_,_=features(Y);A=fo-fi
    b=2/g*(np.sum(lam[:,None]*np.abs(X)**2,axis=0)-np.sum(lam[:,None]*np.abs(Y)**2,axis=0))
    tick=time.perf_counter();theta=np.linalg.lstsq(A,b,rcond=None)[0]
    T=tensor_from(theta,n,perms);fit_seconds=time.perf_counter()-tick
    (gap,V,w),gaps=recover_axes(T);Qhat=V.T
    sv=np.linalg.svd(A,compute_uv=False)
    trueT=np.einsum('ja,jb,jc,jd->abcd',oracle.Q,oracle.Q,oracle.Q,oracle.Q)
    err=gauge_error(Qhat,Khat,oracle)
    np.savez(root/'DATA.npz',X=X,Y=Y,A=A,b=b,theta=theta,T=T,lam=lam,c=c,
             raw_pre=np.array(raw_pre),raw_post=np.array(raw_post),taus=np.array(taus),
             Qtruth=oracle.Q,Ktruth=oracle.K,lambda_truth=oracle.lam,c_truth=oracle.c,
             ode_initial=np.array(ode_initial),ode_final=np.array(ode_final),w=w,
             Bhat=Bhat,Chat=Chat)
    source={'Q_exact':[[str(x) for x in r] for r in oracle.qr],
            'K_exact':[[str(x) for x in r] for r in oracle.kr],
            'lambda_exact':[str(x) for x in oracle.lr],'port_overlap_exact':[str(x) for x in oracle.cr]}
    (root/'SYNTHETIC_SOURCE.json').write_text(json.dumps(source,indent=2)+'\n')
    result={'status':'EXECUTED_FINITE_PORT_MODEL_DIAGNOSTIC_NOT_PHYSICAL',
            'independent_before_reading_root_code':True,'n':n,'tensor_coefficients':m,
            'experiments':2*m,'g':g,'radii':radii,'pulse_duration_range':[float(min(taus)),float(max(taus))],
            'linear_calibration':cal,'linear_calibration_bound_is_auditor_truth_only':True,
            'linear_lambda_error':float(np.max(np.abs(lam-oracle.lam))),
            'linear_port_overlap_error':float(np.linalg.norm(c-oracle.c)),
            'control_sigma_min':float(np.linalg.svd(Bhat,compute_uv=False)[-1]),
            'readout_sigma_min':float(np.linalg.svd(Chat,compute_uv=False)[-1]),
            'complex_readout_noise_bound':noise,'linear_readout_noise_bound':1e-13,
            'scalar_complex_snapshots':65+4*m*len(times),
            'reset_max_residual_norm':float(max(reset_residual)),
            'largest_coherent_drive_amplitude':float(max(peak)),
            'total_integrated_drive_power':float(sum(drive_energy)),
            'total_normalized_control_readout_pulse_time':float(2*m*(2*Tprep+2*Tread)+sum(taus)+32.2),
            'design_sigma_min':float(sv[-1]),'design_condition':float(sv[0]/sv[-1]),
            'energy_equation_residual':float(np.linalg.norm(A@theta-b)),
            'tensor_frobenius_error':float(np.linalg.norm(T-trueT)),
            'offline_contraction_gap':gap,'offline_gap_candidates':gaps,'reconstruction':err,
            'maximum_observed_ODE_energy_defect':float(max(map(abs,energy_defects))),
            'ODE_error_rigorously_qualified':False,'acquisition_seconds':acquire_seconds,
            'linear_tensor_solve_seconds':fit_seconds,'ODE_calls':oracle.ode_calls,
            'ODE_evaluations':oracle.ode_evaluations,'seconds_total':time.perf_counter()-start,
            'finite_noise_physical_model_or_advantage_claim':False}
    (root/'ENERGY_EXECUTION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':run()
