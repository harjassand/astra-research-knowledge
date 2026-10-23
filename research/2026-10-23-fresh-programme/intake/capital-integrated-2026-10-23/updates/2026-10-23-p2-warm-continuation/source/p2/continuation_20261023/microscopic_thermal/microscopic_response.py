"""Synthetic microscopic response checks; no material performance or measurements.

Two independently specified Hamiltonians are used:
1. Stable anharmonic coordinate + completed-square oscillator bath. Linear
   causal response is exact for its harmonic reference; chi2 is leading order
   in the cubic force. Bath damping, KK shift and FDT noise use the SAME J.
2. Exactly diagonalizable independent-boson two-level Hamiltonian. Its
   T=0 spectrum has an exact gap. The dipole response and chi2 below that gap
   are evaluated with the full Franck-Condon spectral measure.

All numerical values are DIMENSIONLESS DECLARED CONSTRUCTIONS, not data.
Run: python continuation_20261023/microscopic_thermal/microscopic_response.py
"""
from pathlib import Path
import json
import math
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad
from scipy.linalg import eigh, expm
from scipy.optimize import brentq

OUT=Path(__file__).resolve().parent


def bump(nu, center, width):
    u=(np.asarray(nu)-center)/width
    return np.where(np.abs(u)<1,(1-u*u)**2,0.)


class LorentzBath:
    """m=q=n=epsilon0=hbar=1; frequency units arbitrary."""
    w0=5.
    a=.5
    b4=.05
    center=5.
    width=1.
    peak=.4

    def j(self,w):
        return float(self.peak*bump(w,self.center,self.width))

    def dreal(self,w):
        lo,hi=self.center-self.width,self.center+self.width
        if w==0:
            return self.w0**2
        if lo<w<hi:
            val=quad(lambda nu:self.j(nu)/(nu*(nu+w)),lo,hi,
                     weight='cauchy',wvar=w,epsabs=1e-11,epsrel=1e-11)[0]
        else:
            val=quad(lambda nu:self.j(nu)/(nu*(nu*nu-w*w)),lo,hi,
                     epsabs=1e-11,epsrel=1e-11)[0]
        return self.w0**2-w*w-2*w*w/np.pi*val

    def d(self,w):
        return self.dreal(w)-1j*self.j(w)

    def dz(self,z):
        lo,hi=self.center-self.width,self.center+self.width
        fun=lambda nu:self.j(nu)/(nu*(nu*nu-z*z))
        val=quad(lambda nu:fun(nu).real,lo,hi,epsabs=1e-11)[0] \
            +1j*quad(lambda nu:fun(nu).imag,lo,hi,epsabs=1e-11)[0]
        return self.w0**2-z*z-2*z*z/np.pi*val

    def harmonic_hessian(self,n=128,global_convex_floor=False):
        z,w=leggauss(n)
        nu=self.center+self.width*z
        weights=self.width*w
        c2=2/np.pi*np.array([self.j(x) for x in nu])*nu*weights
        curvature=self.w0**2-self.a**2/(3*self.b4) \
            if global_convex_floor else self.w0**2
        mat=np.diag(np.r_[curvature+np.sum(c2/nu**2),nu**2])
        mat[0,1:]=mat[1:,0]=-np.sqrt(c2)
        return mat


def lorentz_checks():
    b=LorentzBath()
    ws=[1.,.2,1.2]
    ds=[b.d(w) for w in ws]
    chi1=[1/d for d in ds]
    chi2=-b.a/np.prod(ds)
    resonance=brentq(b.dreal,4.01,5.99)
    convex=b.w0*b.w0-b.a*b.a/(3*b.b4)
    eigen_harm=eigh(b.harmonic_hessian(),eigvals_only=True)
    eigen_floor=eigh(b.harmonic_hessian(global_convex_floor=True),eigvals_only=True)
    assert convex>0 and eigen_floor.min()>0
    assert max(b.j(w) for w in ws)==0.
    assert abs(chi2.imag)<1e-15 and abs(chi2.real)>0
    # Derive chi'(probe) again by integrating its absorption spectrum.
    # No undamped poles exist outside the bath band in this chosen reference.
    lo,hi=b.center-b.width,b.center+b.width
    kk=[]
    for w,d in zip(ws,ds):
        integral=2/np.pi*quad(
            lambda v:v*(1/b.d(v)).imag/(v*v-w*w),lo,hi,
            points=[resonance],epsabs=1e-11,epsrel=1e-10,limit=200)[0]
        direct=(1/d).real
        error=abs(integral/direct-1)
        assert error<1e-8
        kk.append(dict(probe=w,direct_chi1=direct,KK_from_absorption=integral,
                       relative_difference=error))
    sum_rule=2/np.pi*quad(lambda v:v*(1/b.d(v)).imag,lo,hi,
        points=[resonance],epsabs=1e-11,epsrel=1e-10,limit=200)[0]
    assert abs(sum_rule-1)<1e-8
    # Check the analytic upper-half-plane response, without interpreting the
    # regulator as an assigned physical linewidth.
    causal=[]
    for w in ws:
        z=w+1j*1e-7
        finite_eta=1/b.dz(z)
        causal.append(dict(probe=w,regulator=1e-7,
            real_at_upper_half_plane=float(finite_eta.real),
            imag_at_upper_half_plane=float(finite_eta.imag),
            physical_real_axis_absorption=float((1/b.d(w)).imag)))
    # Joint response/absorption identity in a lossy tuple within the same band.
    # This tuple is a mathematical normalization check, not a mixing proposal:
    # use arbitrary triplet for algebra; the identity holds if frequencies sum.
    rng=np.random.default_rng(202610231)
    errors=[]
    for _ in range(100):
        f=rng.uniform(4.1,5.9,3)
        dc,dh,dp=[b.d(w) for w in f]
        bc,bh,bp=[b.j(w) for w in f]
        ep=rng.uniform(.001,.01)
        xp=ep/dp
        chi=-b.a/(dc*dh*dp)
        loss_c=bc/abs(dc)**2
        loss_h=bh/abs(dh)**2
        lhs=abs(chi*ep)**2/(loss_c*loss_h)
        rhs=b.a**2*abs(xp)**2/(bc*bh)
        errors.append(abs(lhs/rhs-1))
        # Heat per oscillator from bath spectral density and optical theorem.
        heat=.5*f[2]*bp*abs(xp)**2
        heat_via_chi=.5*f[2]*(1/dp).imag*ep**2
        assert abs(heat/heat_via_chi-1)<1e-12
    return dict(status='HARMONIC_REFERENCE_EXACT_CHI2_LEADING_ANHARMONIC_ORDER',
        units='dimensionless m=q=n=epsilon0=hbar=1; not material parameters',
        parameters=dict(w0=b.w0,a=b.a,b4=b.b4,bath_band=[lo,hi],J_peak=b.peak),
        target_omega_c_p_h=ws,
        target_chi1_real=[float(x.real) for x in chi1],
        target_absorption=[float(x.imag) for x in chi1],
        target_chi2_real=float(chi2.real),
        target_chi2_imag=float(chi2.imag),
        resonance=float(resonance),J_at_resonance=b.j(resonance),
        global_potential_curvature_floor=convex,
        discretized_bath_min_normal_frequency=float(np.sqrt(eigen_harm.min())),
        discretized_global_Hessian_min_frequency=float(np.sqrt(eigen_floor.min())),
        no_pole_below_target_checked_min_D=float(min(b.dreal(w) for w in np.linspace(0,1.2,100))),
        linear_oscillator_strength_sum_rule=sum_rule,
        KK_checks=kk,upper_half_plane_checks=causal,
        same_response_algebra_checks=100,max_relative_identity_error=max(errors),
        warning='Hessian check proves classical stability of the discretized construction; '
        'it is not a proof of an exact finite-temperature anharmonic spectral gap. '
        'Finite-temperature nonlinear/Raman noise is not excluded by target linear J=0.')


def beta_kernel(delta,wc,wp):
    wh=wc+wp
    return (1/(delta-wh)*(1/(delta-wc)+1/(delta-wp))
            +1/(delta+wh)*(1/(delta+wc)+1/(delta+wp))
            +(1/(delta-wc)-1/(delta+wc)
              +1/(delta-wp)-1/(delta+wp))/wh)


def compound_poisson(n_grid):
    # Exact continuum's compound-Poisson measure discretized in energy.
    # Mean phonon count S=.4; wraparound needs at least 16 phonons.
    emax=128.
    energy=np.arange(n_grid)*emax/n_grid
    base=bump(energy,7.,1.)
    base/=base.sum()
    s=.4
    probs=np.fft.ifft(np.exp(s*(np.fft.fft(base)-1))).real
    return energy,probs


def second_order_density_matrix(energies,dipole,wc,wp):
    """Return beta_sum for real PEAK field phasors.

    E(t)=Re[Ec exp(-i wc t)+Ep exp(-i wp t)] and the output is
    Re[beta_sum Ec Ep exp(-i(wc+wp)t)]. The factor 1/2 below converts
    Fourier half-amplitudes to that real-peak output. In the joint static
    limit this beta equals the coefficient of E**2 in <D>(E), i.e. half
    its second derivative, not the second derivative itself.
    """
    rho0=np.zeros_like(dipole)
    rho0[0,0]=1
    comm=lambda a,b:a@b-b@a
    def r(w,x):
        return x/(w-(energies[:,None]-energies[None,:]))
    first_c=-r(wc,comm(dipole,rho0))
    first_p=-r(wp,comm(dipole,rho0))
    second=-.5*r(wc+wp,comm(dipole,first_c)+comm(dipole,first_p))
    return float(np.trace(dipole@second))


def quantum_gap_checks():
    delta,d,e=5.,.8,.3
    wc,wp=1.,.2
    rows=[]
    for ng in [8192,16384,32768]:
        ene,prob=compound_poisson(ng)
        trans=delta+ene
        alpha=[float(d*d*np.sum(prob*(1/(trans-w)+1/(trans+w))))
               for w in [wc,wp,wc+wp]]
        beta=float(e*d*d*np.sum(prob*beta_kernel(trans,wc,wp)))
        static=float(6*e*d*d*np.sum(prob/trans**2))
        rows.append(dict(grid=ng,total_probability=float(prob.sum()),
            minimum_numerical_probability=float(prob.min()),
            zero_phonon_weight=float(prob[0]),linear_alpha_real=alpha,
            beta_real=beta,beta_static=static))
    assert abs(rows[-1]['beta_real']/rows[-2]['beta_real']-1)<1e-8
    assert abs(rows[-1]['zero_phonon_weight']-np.exp(-.4))<1e-12
    # Each bath quantum has energy <=8 and the circular FFT period is 128.
    # Wrapping requires at least 16 quanta (this includes a measure-zero edge
    # and is deliberately conservative). Bound the Poisson tail by a geometric
    # series: subsequent probability ratios are <= S/(16+1).
    tail_bound=math.exp(-.4)*.4**16/math.factorial(16)/(1-.4/17)
    kernel_max=e*d*d*float(beta_kernel(delta,wc,wp))
    # Independent exact response calculation for a SINGLE explicit bath mode,
    # using its displaced-basis dipole, versus the Franck-Condon sum formula.
    single=[]
    for n in [12,20,28]:
        destroy=np.diag(np.sqrt(np.arange(1,n)),1)
        displacement=expm(np.sqrt(.4)*(destroy.T-destroy))
        dip=np.block([[np.zeros((n,n)),d*displacement],
                      [d*displacement.T,2*e*np.eye(n)]])
        energies=np.r_[np.arange(n)*7.,delta+np.arange(n)*7.]
        exact=second_order_density_matrix(energies,dip,wc,wp)
        poisson=np.array([math.exp(-.4)*.4**j/math.factorial(j) for j in range(n)])
        spectral=float(e*d*d*np.sum(poisson*beta_kernel(delta+7*np.arange(n),wc,wp)))
        error=abs(exact/spectral-1)
        assert error<1e-9
        single.append(dict(bath_cutoff=n,density_matrix_beta=exact,
            spectral_measure_beta=spectral,relative_difference=error))
    return dict(status='EXACT_GAPPED_HAMILTONIAN_T0_RESPONSE_WITH_NUMERICAL_QUADRATURE',
        units='dimensionless hbar=1; dipole and energy scales declared, not material data',
        parameters=dict(Delta=delta,d=d,e=e,bath_support=[6.,8.],Huang_Rhys_S=.4),
        exact_full_system_gap=5.,
        target_omega_c_p_h=[wc,wp,wc+wp],
        exact_target_intrinsic_linear_absorption=[0.,0.,0.],
        exact_target_T0_internal_equilibrium_dipole_noise=[0.,0.,0.],
        response_boundary='Matter plus specified internal bath before propagating '
        'electromagnetic-port dressing; not total extinction of a radiating dipole.',
        FFT_wrap_probability_upper_bound=tail_bound,
        FFT_wrap_beta_absolute_error_upper_bound=tail_bound*kernel_max,
        continuum_Franck_Condon_quadrature=rows,
        independent_single_bath_density_matrix_checks=single,
        qualifications=['Ground-state pointwise response counterexample, not room-temperature performance.',
            'Diagonal bath coupling does not guarantee population thermalization.',
            'Finite-temperature subgap Raman processes and finite-pump multiphoton excitation remain possible.',
            'No fixed oscillator-strength, number-density, geometric-size or source-efficiency budget imposed.',
            'Radiative reaction and useful converted/scattered output must be included when EM ports are added.',
            'No added-noise statement for arbitrary amplification; passive number-conserving RWA only.'])


def main():
    out=dict(status='THEOREM_COUNTEREXAMPLE_AND_CONDITIONAL_MODEL_BOUND',
        acquired_measurements='NONE',executed_physical_experiments='NONE',
        actual_backend_model_usage='UNKNOWN',usage_receipts='UNKNOWN',
        lorentz=lorentz_checks(),independent_boson=quantum_gap_checks())
    (OUT/'microscopic_response_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()
