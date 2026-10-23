"""Independent, bounded mathematical check, not a reacting or material-validated device.
One analytic axial-conduction counterexample, three FV resolutions, one finite blow.
No chemistry calculation and no design-parameter grid.
"""
from pathlib import Path
import json,time,resource,platform
import numpy as np
import scipy
from scipy.integrate import solve_bvp
from scipy.linalg import expm,solve
from scipy.sparse.linalg import expm_multiply
ROOT=Path(__file__).resolve().parent
START=time.monotonic(); HOT=3100.;COLD=300.;LIMIT=2500.

def analytic(n,D):
    lam=np.sqrt(n*(1+n*D)/D)
    R=n/(2*(1+n*D))*(1+2*n*D*np.tanh(lam/2)/lam)
    eps=R/(1+R);a=n*(1-eps)/(2*(1+n*D))
    sm=.5+a*(.5-np.tanh(lam/2)/lam)
    return dict(NTU=n,D=D,lambda_profile=lam,R=R,effectiveness=eps,solid_max_theta=sm,
                solid_max_K=COLD+(HOT-COLD)*sm,cold_out_K=COLD+(HOT-COLD)*eps,
                hotface_mean_conduction_export_dimensionless=n/2*(1+eps-2*sm))

def phase(N,nt,reverse=False,D=0.):
    """Integrate each plug-flow cell exactly against its cell-average solid T.
    Cell heat rates are inlet minus outlet enthalpy; conduction is conservative FV.
    Dimensionless time is Cdot*t/Csolid,total; D=k_eff*A/(Cdot*L).
    """
    a=np.exp(-nt/N);eye=np.eye(N)
    E=np.zeros((N,N));F=np.zeros(N)
    for i in range(N):
        E[i,i]=-N*(1-a)
        if i:E[i,:i]=N*(1-a)**2*a**np.arange(i-1,-1,-1)
        F[i]=N*(1-a)*a**i
    w=(1-a)*a**np.arange(N-1,-1,-1)
    if reverse:E=E[::-1,::-1];F=np.zeros(N);w=w[::-1]
    L=np.diag(np.r_[-1.,np.full(N-2,-2.),-1.])+np.diag(np.ones(N-1),1)+np.diag(np.ones(N-1),-1)
    E=E+D*N*N*L
    return E,F,w,(0. if reverse else a**N)

def fv_steady(N,nt=8.,D=.1):
    H,f,wh,bh=phase(N,nt,D=D);C,g,wc,bc=phase(N,nt,True,D)
    s=solve(-(H+C)/2,(f+g)/2)
    eps=float(wc@s+bc);ho=float(wh@s+bh)
    return dict(N=N,effectiveness=eps,solid_max_K=float(COLD+(HOT-COLD)*s.max()),
                energy_residual=1-ho-eps,steady_ODE_residual=float(np.max(abs((H+C)@s+f+g))))

def finite_blow(N=160,nt=8.,D=.1,b=.001):
    maps=[];gens=[]
    for rev in [False,True]:
        B,f,w,c=phase(N,nt,rev,D)
        E=np.zeros((N+2,N+2));E[:N,:N]=B;E[:N,N]=f;E[-1,:N]=w;E[-1,N]=c
        gens.append(E);maps.append(expm(E*b))
    H,C=maps
    P=C[:N,:N]@H[:N,:N];f=C[:N,:N]@H[:N,N]+C[:N,N]
    s0=solve(np.eye(N)-P,f);s1=H[:N,:N]@s0+H[:N,N];s2=C[:N,:N]@s1+C[:N,N]
    eps=(C[-1,:N]@s1+C[-1,N])/b;hout=(H[-1,:N]@s0+H[-1,N])/b
    maxima=[]
    # 101 samples per phase, labelled sampled rather than rigorously maximized.
    for E,s in zip(gens,[s0,s1]):
        ss=expm_multiply(E,np.r_[s,1.,0.],start=0.,stop=b,num=101)[:,:N]
        maxima.append(float(ss.max()))
    return dict(N=N,NTU=nt,D=D,blow_ratio=b,effectiveness=float(eps),cold_out_K=float(COLD+(HOT-COLD)*eps),
                solid_max_K_101_samples_per_phase=float(COLD+(HOT-COLD)*max(maxima)),
                solid_max_K_semidiscrete_upper_bound=float(COLD+(HOT-COLD)*(max(maxima)+nt*b/100)),
                peak_bound_note='At a spatial maximum the conduction term is nonpositive and d(theta_max)/dt <= NTU; add NTU times the 100-interval sample spacing. Bounds this finite-volume system, not continuum discretization error.',
                periodic_reset_max=float(abs(s2-s0).max()),energy_residual=float(1-hout-eps),
                caveat='Finite-volume and sampled peak; analytic continuum rapid-cycle result is the rigorous counterexample.')

r=analytic(8.,.1)
def fun(x,y):
    H,C,S,V=y
    return np.array([-8*(H-S),8*(C-S),V,-8/(2*.1)*(H+C-2*S)])
def bc(ya,yb):return np.array([ya[0]-1,yb[1],ya[3],yb[3]])
x=np.linspace(0,1,60);y=np.array([1-.3*x,.7*(1-x),.7-.4*x,np.full_like(x,-.4)])
bvp=solve_bvp(fun,bc,x,y,tol=1e-9,max_nodes=5000)
assert bvp.success,bvp.message
bvp_receipt=dict(success=bvp.success,message=bvp.message,nodes=len(bvp.x),max_rms_residual=float(max(bvp.rms_residuals)),
                 effectiveness=float(bvp.sol(0)[1]),solid_max_K=float(COLD+(HOT-COLD)*bvp.sol(0)[2]),
                 epsilon_disagreement=float(abs(bvp.sol(0)[1]-r['effectiveness'])))
assert bvp_receipt['epsilon_disagreement']<1e-10
fv=[fv_steady(N) for N in [100,200,400]]
f=finite_blow()
nh,nc=3.,12.;ueff=nh*nc/(nh+nc);epsu=ueff/(1+ueff);su=(nh+nc*epsu)/(nh+nc)
unequal=dict(NTU_hot=nh,NTU_cold=nc,NTU_combined=ueff,effectiveness=epsu,cold_out_K=COLD+(HOT-COLD)*epsu,
             solid_max_K=COLD+(HOT-COLD)*su,phase_hot_to_cold_conductance_ratio=nh/nc)
result=dict(scope=__doc__,hot_K=HOT,cold_K=COLD,solid_limit_K=LIMIT,
            no_axial_equal_h_bound=dict(cold_out_K=2*LIMIT-HOT,effectiveness=(2*LIMIT-HOT-COLD)/(HOT-COLD)),
            exact_axial_continuum=r,independent_BVP=bvp_receipt,FV_spatial_convergence=fv,finite_blow=f,
            unequal_h_continuum=unequal,
            symmetric_pure_radiation_necessary_peak_min_K=HOT/2**.25,
            symmetric_radiation_fourth_power_budget_K4=2*LIMIT**4-HOT**4,
            physical_example=dict(D=.1,mass_flux_kg_m2_s=1.,cp_J_kg_K=1200.,length_m=.1,k_effective_W_m_K=12.,status='Illustrative parameter translation, not a measured material property.'),
            receipts=dict(wall_s=time.monotonic()-START,max_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                          python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,time_UTC=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())))
(ROOT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
