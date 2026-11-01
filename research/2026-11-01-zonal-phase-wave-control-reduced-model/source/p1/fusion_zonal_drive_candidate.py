"""Exploratory, conditional slab-model fusion zonal-shear design.

Source: local wave momentum / absorbed-power identity in Gallaro & Dodin,
arXiv:2609.36299 (2026). The effective damping/diffusion/shear requirement,
actuator efficiency, spatial blur and heat payoff are MODEL INPUTS, not measured.
Runs: python fusion_zonal_drive_candidate.py
"""
from dataclasses import dataclass
import math
import numpy as np
from scipy.optimize import minimize_scalar, brentq
from scipy.special import i0e, ive
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

@dataclass(frozen=True)
class Scenario:
    n_m3: float = 5e19
    ion_mass_kg: float = 3.34358372e-27
    damp_s: float = 3000.
    radial_momentum_diff_m2_s: float = 0.4
    omega_rad_s: float = 2 * math.pi * 120000.
    ky_m_inv: float = 50.
    smear_m: float = 0.012
    radial_period_m: float = 0.5
    zonal_layer_volume_m3: float = 50.
    target_rms_shear_s: float = 1e5
    eta_momentum_transfer: float = 0.10
    rf_absorption_fraction: float = 0.70
    

def absorbed_power_density(sc, k, sigma=None):
    """Minimum mean absorbed-wave power (W/m^3) for exactly sinusoidal u.

    In an ideal continuously steerable signed-wave-absorption profile, positive
    and negative launches have independent controllable shapes. Momentum
    delivery is eta (ky/omega) times gaussian-smoothed differential absorption.
    Positive decomposition of the inverse sinusoidal force realizes the bound.
    """
    if sigma is None: sigma=sc.smear_m
    rho=sc.n_m3 * sc.ion_mass_kg
    w_over_k=sc.omega_rad_s / abs(sc.ky_m_inv)
    return (2*math.sqrt(2)/math.pi) * (rho*w_over_k / sc.eta_momentum_transfer) * (sc.target_rms_shear_s / k) * (sc.damp_s + sc.radial_momentum_diff_m2_s*k*k) * math.exp((k*sigma)**2/2)


def optimal_k_correct(sc):
    """Solve sigma² D z² +(D+sigma² gamma)z - gamma=0 for z=k²."""
    D=sc.radial_momentum_diff_m2_s
    g=sc.damp_s
    q=sc.smear_m**2
    b=D+q*g
    z=(2*g)/(b+math.sqrt(b*b+4*q*D*g)) # This expression equals k²? check algebra below
    # Equation positive root is 2g/(b+sqrt(...)), actually factor should be 2g/(b+sqrt(...))? Evaluate at q=0 gives g/D correct.
    return math.sqrt(z)


def build_discrete_drive(sc, n_port=64, n_eval=4096, m=7):
    """Finite equally-spaced source positions approximating the signed drive.

    Point-per-port weights are obtained by sampling the exact unconvolved
    sinusoidal injection and separately decomposing into nonnegative +/-.
    Each fixed-width Gaussian coupling transports the wave momentum. Aliases
    are included in the output. This is NOT an acquired RF deposition map.
    """
    L=sc.radial_period_m
    k=2*math.pi*m/L
    x=np.arange(n_eval)*L/n_eval
    source_x=np.arange(n_port)*L/n_port
    rho=sc.n_m3*sc.ion_mass_kg
    uamp=math.sqrt(2)*sc.target_rms_shear_s/k
    target_force_amp=rho*(sc.damp_s+sc.radial_momentum_diff_m2_s*k*k)*uamp
    input_amp=target_force_amp*math.exp((k*sc.smear_m)**2/2)*sc.omega_rad_s/(sc.eta_momentum_transfer*sc.ky_m_inv)
    signed_density=input_amp*np.cos(k*source_x)
    pos=np.maximum(signed_density,0)
    neg=np.maximum(-signed_density,0)
    # Fourier-space periodic Gaussian smearing plus discrete equal-spaced quadrature.
    p_signed=np.zeros(n_eval)
    if n_eval%n_port!=0: raise ValueError('n_eval must be a multiple of n_port')
    p_signed[np.arange(n_port)*(n_eval//n_port)] = (pos-neg)*(n_eval/n_port)
    # A periodic Gaussian is equivalent to multiplier exp(-0.5*sigma^2*k_n^2).
    k_grid=2*math.pi*np.fft.fftfreq(n_eval,d=L/n_eval)
    force=np.fft.ifft(np.fft.fft(p_signed)*np.exp(-.5*(sc.smear_m*k_grid)**2)).real *sc.eta_momentum_transfer*sc.ky_m_inv/sc.omega_rad_s
    U=np.fft.ifft(np.fft.fft(force)/(rho*(sc.damp_s+sc.radial_momentum_diff_m2_s*k_grid**2))).real
    S=np.fft.ifft(1j*k_grid*np.fft.fft(U)).real
    Uideal=uamp*np.cos(k*x)
    Sideal=np.gradient(Uideal,L/n_eval,edge_order=2)
    source_absorb=np.mean(pos+neg)
    # Fraction of output shear not explained by its desired Fourier pair.
    exact_shear=-uamp*k*np.sin(k*x)
    error=np.linalg.norm(S-exact_shear)/np.linalg.norm(exact_shear)
    modal_amp = np.dot(S,exact_shear)/np.dot(exact_shear,exact_shear)
    return dict(n_port=n_port,m=m,k=k,pabs_Wm3=source_absorb, shear_relative_error=error,desired_shear_fraction=modal_amp,unwanted_shear_rms=np.sqrt(np.mean((S-modal_amp*exact_shear)**2)), net_momentum_source=np.mean(pos-neg))



def locked_fraction(concentration, half_width=math.pi/6):
    """Exact stationary von Mises phase-mass in target window at zero detuning."""
    phase=np.linspace(-half_width,half_width,12001)
    p=np.exp(concentration*(np.cos(phase)-1))/(2*math.pi*i0e(concentration))
    return float(np.trapezoid(p,phase))


def phase_concentration_for_target(p=0.95, half_width=math.pi/6):
    return float(brentq(lambda x:locked_fraction(x,half_width)-p,0,250))


def stationary_phase_fv(kappa, Dphi, detuning, ngrid=1024):
    """Periodic finite-volume upwind CTMC approximation to Adler phase SDE.

    dtheta=(detuning-kappa*sin(theta))dt+sqrt(2 Dphi)dW.
    Generator is conservative. Returns phase-grid probability mass.
    """
    from scipy.sparse import csr_matrix
    theta=np.linspace(-math.pi,math.pi,ngrid,endpoint=False)
    h=2*math.pi/ngrid
    b=detuning-kappa*np.sin(theta)
    diff=Dphi/h**2
    right=diff+np.maximum(b,0)/h
    left=diff+np.maximum(-b,0)/h
    rows=np.concatenate([np.arange(ngrid),np.arange(ngrid),np.arange(ngrid)])
    cols=np.concatenate([np.arange(ngrid),(np.arange(ngrid)+1)%ngrid,(np.arange(ngrid)-1)%ngrid])
    vals=np.concatenate([-(right+left),right,left])
    from scipy.sparse import coo_matrix
    Q=coo_matrix((vals,(rows,cols)),shape=(ngrid,ngrid)).tocsr()
    A=Q.T.tolil()
    A[-1,:]=np.ones(ngrid)
    rhs=np.zeros(ngrid);rhs[-1]=1
    prob=spsolve(A.tocsr(),rhs)
    assert np.min(prob)>-1e-10
    prob=np.maximum(prob,0)/np.maximum(np.sum(np.maximum(prob,0)),1e-300)
    return theta,prob


def phase_scenario(sc, Dphi=5., detuning=0., confidence=.95, window=math.pi/6, m=7):
    c=phase_concentration_for_target(confidence,window)
    # kappa=c*Dphi is sufficient at zero detuning; for detuning find exact FV required kappa.
    if abs(detuning)>1e-15:
        def mass(kappa):
            th,p=stationary_phase_fv(kappa,Dphi,detuning,ngrid=512)
            return p[np.abs(th)<window].sum()
        lo,hi=0,max(c*Dphi,abs(detuning))*1.2
        while mass(hi)<confidence:
            hi*=1.5
            if hi>1e6: raise ValueError('phase-lock requirement too large')
        kappa=brentq(lambda x:mass(x)-confidence,lo,hi,xtol=1e-7)
    else:
        kappa=c*Dphi
    k=2*math.pi*m/sc.radial_period_m
    A=math.sqrt(2)*sc.target_rms_shear_s/k
    F0=sc.n_m3*sc.ion_mass_kg*A*kappa
    pabs=2/math.pi*F0*(sc.omega_rad_s/(sc.eta_momentum_transfer*sc.ky_m_inv))*math.exp((sc.smear_m*k)**2/2)
    plaunched=pabs*sc.zonal_layer_volume_m3/sc.rf_absorption_fraction/1e6
    plocal=0.5*(1+ive(2,c)/ive(0,c)) if detuning==0 else float('nan')
    return dict(kappa=kappa,kappa_over_damping=kappa/(sc.damp_s+sc.radial_momentum_diff_m2_s*k*k),radial_phase_locking_power_MW=plaunched,amplified_local_shear_sq_relative_to_unpinned=plocal/.5)

def checks():
    sc=Scenario()
    # analytic optimum checked by direct scalar minimization
    analytic=optimal_k_correct(sc)
    numeric=minimize_scalar(lambda z: absorbed_power_density(sc,z),bounds=(5,300),method='bounded').x
    assert abs(analytic-numeric)/numeric < 1e-5, (analytic,numeric)
    k=2*math.pi*7/sc.radial_period_m
    values=[build_discrete_drive(sc,n_port=n,m=7) for n in (16,32,64,128)]
    assert values[-1]['shear_relative_error'] < 1e-9
    assert abs(values[-1]['net_momentum_source']) < 1e-6
    optimum=absorbed_power_density(sc,analytic)
    chosen=absorbed_power_density(sc,k)
    rho=sc.n_m3*sc.ion_mass_kg
    uamp=math.sqrt(2)*sc.target_rms_shear_s/k
    p_mech_density=rho*(sc.damp_s+sc.radial_momentum_diff_m2_s*k*k)*uamp*uamp/2
    print('Model-only! No demonstrated plasma actuator or heat savings.\n')
    print(f'Unblurred optimum wavenumber = {math.sqrt(sc.damp_s/sc.radial_momentum_diff_m2_s):.6f} /m')
    print(f'Width-costed continuous optimum = {analytic:.6f} /m; radial period {2*math.pi/analytic:.4f} m')
    print(f'Ideal continuous minimum absorbed wave power density = {optimum:.2f} W/m3')
    print(f'Chosen m=7: k={k:.4f} /m, U_amp={uamp:.2f} m/s, shear_RMS={sc.target_rms_shear_s:.2e}/s')
    print(f'Chosen absorbed = {chosen:.2f} W/m3, volume cost={chosen*sc.zonal_layer_volume_m3/1e6:.3f} MW')
    print(f'Launched RF, conditional eta and absorption = {chosen*sc.zonal_layer_volume_m3/sc.rf_absorption_fraction/1e6:.3f} MW')
    print(f'Mechanical dissipation = {p_mech_density*sc.zonal_layer_volume_m3/1e6:.3f} MW; mechanical/absorbed = {p_mech_density/chosen:.3%}')
    for v in values:
        print(f"nport={v['n_port']:3d}, Pabs={v['pabs_Wm3']:.2f} W/m3, target response={v['desired_shear_fraction']:.6f}, relative shear error={v['shear_relative_error']:.6f}, RMS spurious={v['unwanted_shear_rms']:.2f} /s, net wave imbalance={v['net_momentum_source']:.2e}")
    print('eta sweep:')
    for eta in (1.,.3,.1,.03,.01):
        s=Scenario(eta_momentum_transfer=eta)
        pp=absorbed_power_density(s,k)*s.zonal_layer_volume_m3/s.rf_absorption_fraction/1e6
        print(f' eta={eta:.2f} -> launched MW {pp:.3f}')
    print('phase-pinning scenario (spontaneously sustained amplitude REQUIRED, not proven):')
    lam=phase_concentration_for_target()
    print(f'  Required stationary phase concentration lambda=kappa/Dphi for 95% within +/-30 degrees: {lam:.5f}')
    for df in (1,5,50,500):
        d=phase_scenario(sc,Dphi=df)
        print(f"  Dphi={df:4.0f}/s -> kappa={d['kappa']:8.2f}/s, RF launched {d['radial_phase_locking_power_MW']:.3f} MW, ratio to amplitude-drive {d['kappa_over_damping']:.4f}")
    print('Detuned phase locking (finite-volume stationary diffusion):')
    for det in (0,20,100):
        d=phase_scenario(sc,Dphi=5,detuning=det)
        print(f" detuning={det:3.0f}/s -> kappa={d['kappa']:9.2f}/s, launched {d['radial_phase_locking_power_MW']:.3f} MW")
    th,pm=stationary_phase_fv(lam*5,5,0)
    mass=pm[np.abs(th)<math.pi/6].sum()
    assert abs(mass-.95)<.003, mass
    return values

if __name__=='__main__': checks()

# Additional finite-startup check: stationary concentration does not imply that
# freshly selected, uniformly random phases immediately meet a target coverage.
def finite_startup_check():
    from scipy.sparse import coo_matrix
    from scipy.sparse.linalg import expm_multiply
    n=256; D=5.; kappa=100.;det=0.
    h=2*math.pi/n
    theta=np.linspace(-math.pi,math.pi,n,endpoint=False)
    drift=det-kappa*np.sin(theta)
    plus=D/h**2 + np.maximum(drift,0)/h
    minus=D/h**2 + np.maximum(-drift,0)/h
    ind=np.arange(n)
    Q=coo_matrix((np.r_[-plus-minus,plus,minus],(np.r_[ind,ind,ind],np.r_[ind,(ind+1)%n,(ind-1)%n])),shape=(n,n)).tocsr()
    p=np.ones(n)/n
    print('  Finite startup from uniform phase, kappa=100/s Dphi=5/s, 30deg window:')
    for t in (0.0,0.02,0.05,0.10,0.20):
        q=expm_multiply(Q.T*t,p) if t>0 else p
        mass=q[np.abs(theta)<math.pi/6].sum()
        print(f'   t={t:.2f}s, phase-in-window mass={mass:.6f}')

if __name__=='__main__':
    finite_startup_check()

def amplitude_phase_falsifier(ntraj=5000, dt=2e-5, T=.1, seed=1407):
    """Noise-driven Stuart-Landau amplitude/phase test, NOT gyrokinetics.
    Same wave-force phase projection, but amplitude can change, invalidating
    the phase-only approximation when kappa is not small compared to mu.
    """
    rng=np.random.default_rng(seed)
    A=1.0; Dphi=5.; kappa=100.; N=round(T/dt)
    outputs=[]
    for mu in (3000.,100.,30.):
        z=np.exp(1j*rng.uniform(-math.pi,math.pi,ntraj))
        for _ in range(N):
            dW=rng.standard_normal(ntraj)+1j*rng.standard_normal(ntraj)
            z+=dt*(mu*z*(1-abs(z)**2)+kappa)+math.sqrt(2*Dphi*dt)*dW
        ang=np.angle(z)
        inside=np.mean(abs(ang)<math.pi/6)
        amp=np.mean(abs(z))
        outputs.append((mu,inside,amp))
    print('  Full noisy Stuart-Landau test (n=5000, time=0.1s; all synthetic):')
    for mu,inside,amp in outputs:
        print(f'   mu={mu:6.0f}/s, |phase|<30deg fraction={inside:.4f}, mean amplitude / unforced A={amp:.4f}')
    return outputs

if __name__=='__main__':
    amplitude_phase_falsifier()
