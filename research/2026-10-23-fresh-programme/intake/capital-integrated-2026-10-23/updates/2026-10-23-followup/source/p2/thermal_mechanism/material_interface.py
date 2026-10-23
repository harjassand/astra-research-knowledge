"""Energy-normalized nonlinear thermal interface; calculations, not measurements.

Run: python thermal_mechanism/material_interface.py
All susceptibility outputs are explicit model extrapolations. Loss normalizations
in the conditional envelope are reference variables, not a measured device.
"""
from pathlib import Path
import json
import numpy as np
from scipy.constants import c, h, hbar, k, epsilon_0, pi
from scipy.optimize import minimize, minimize_scalar

OUT = Path(__file__).resolve().parent


def bose(f, temperature):
    return float(1 / np.expm1(h * f / (k * temperature)))


def thermal_gate(fc, fh, tc, th):
    nc = bose(fc, tc)
    ncl_hot = bose(fc, th)
    nh = bose(fh, th)
    d0, da = nc - nh, ncl_hot - nc
    return dict(fc_THz=fc/1e12, fh_THz=fh/1e12,
                fp_THz=(fh-fc)/1e12, Tc_K=tc, Th_K=th,
                nc=nc, n_cold_frequency_at_Th=ncl_hot, nh=nh,
                Delta0=d0, Delta_a=da,
                ideal_COP=fc/(fh-fc), Carnot_COP=tc/(th-tc),
                x_over_B_max=d0/da,
                Xi_over_A_infimum=da/(4*d0) if d0 > 0 else None)


def flytzanis(frequencies_THz, chi_e_pm_per_V, c_values,
              f_to_THz=8.05, gamma_THz=0.29):
    ds = [1-(f/f_to_THz)**2-1j*f*gamma_THz/f_to_THz**2
          for f in frequencies_THz]
    terms = [sum(1/d for d in ds),
             sum(1/(ds[i]*ds[j]) for i,j in [(0,1),(0,2),(1,2)]),
             1/np.prod(ds)]
    val = chi_e_pm_per_V*(1+sum(cc*t for cc,t in zip(c_values, terms)))
    return dict(real_chi14_pm_per_V=float(val.real),
                imag_chi14_pm_per_V=float(val.imag),
                real_chieff_211_pm_per_V=float(2/np.sqrt(3)*val.real),
                imag_chieff_211_pm_per_V=float(2/np.sqrt(3)*val.imag))


def conditional_envelope(gate):
    # Chosen reference values ONLY. No claim these coexist in a measured device.
    chi = 60e-12             # chi_eff = 2*d_eff, real coherent part
    nc, nh, ng_h, npump = 3.28, 3.28, 3.28, 3.61
    alpha_c = 0.006*100      # INTENSITY attenuation coefficient, m^-1
    rate_a = 2*pi*1e9        # energy damping rate, s^-1
    wc, wh = 2*pi*gate['fc_THz']*1e12, 2*pi*gate['fh_THz']*1e12
    eps_c_im = nc*c*alpha_c/wc
    xi = rate_a*gate['Xi_over_A_infimum']
    ep2 = 4*nh*ng_h*eps_c_im*xi/(chi**2*wh)
    ip = 0.5*epsilon_0*c*npump*ep2
    return dict(status='CONDITIONAL_REFERENCE_ENVELOPE_NOT_MEASURED_PERFORMANCE',
                assumed_real_chieff_pm_per_V=chi/1e-12,
                assumed_n_c=nc, assumed_n_h=nh, assumed_ng_h=ng_h,
                assumed_n_p=npump, assumed_alpha_c_cm_inv=alpha_c/100,
                assumed_A_over_2pi_Hz=rate_a/(2*pi),
                E_peak_infimum_kV_per_cm=float(np.sqrt(ep2)/1e5),
                I_p_infimum_W_per_m2=float(ip),
                q_p_abs_4nm_W_per_m2_per_alpha_p_cm_inv=float(ip*4e-9*100),
                full_overlap_x_over_2pi_MHz=float(wc*eps_c_im/(nc*nc)/(2*pi)/1e6),
                caution='Zero-useful-power infimum. Finite cooling, B material floor, '
                        'imperfect overlap, pump deposition and unwanted modes raise requirements. '
                        'alpha_p at 2.94607 THz and alpha_h at 9.6 um are UNKNOWN.')


def independent_normalization_check():
    # Direct equations for classical peak fields versus photon normalization,
    # with random energy indices, volumes and signal overlaps.
    rng=np.random.default_rng(202610233)
    largest=0.
    largest_loss_ratio=0.
    for _ in range(100):
        fc, fp = rng.uniform(10,35)*1e12, rng.uniform(1,6)*1e12
        wc, wp = 2*pi*fc, 2*pi*fp
        wh=wc+wp
        dc, dh, dp=rng.uniform(2,20,3)
        vol=10**rng.uniform(-23,-14)
        chi=10**rng.uniform(-12,-9)
        ep=10**rng.uniform(3,7)
        zc, zh=rng.uniform(.01,1,2)
        ec_im, eh_im, ep_im=10**rng.uniform(-6,-1,3)
        npump=epsilon_0*dp*vol*ep**2/(2*hbar*wp)
        g0=zc*zh*chi*np.sqrt(hbar*wc*wh*wp/(2*epsilon_0*vol*dc*dh*dp))
        g_classical=zc*zh*chi*np.sqrt(wc*wh/(4*dc*dh))*ep
        largest=max(largest,abs(g0*np.sqrt(npump)/g_classical-1))
        x=zc**2*wc*ec_im/dc
        bh=zh**2*wh*eh_im/dh
        lhs=4*g_classical**2/(x*bh)
        rhs=chi**2*ep**2/(ec_im*eh_im)
        largest_loss_ratio=max(largest_loss_ratio,abs(lhs/rhs-1))
    assert largest < 1e-12
    assert largest_loss_ratio < 1e-12
    return dict(cases=100, max_relative_field_vs_photon_error=largest,
                max_relative_overlap_cancellation_error=largest_loss_ratio)


def pump_absorption_bound_audit():
    """Audit the root branch's contact-optimized bound independently.

    One-dimensional optimization follows analytic elimination of pump and
    linewidth ratios at fixed low-mode hot-contact fraction r. The second
    calculation directly optimizes the independently derived B=2g expression.
    The material values are a mixed-source REFERENCE SCENARIO, not a device.
    """
    def hcrit_1d(d):
        def objective(r):
            gap=np.cbrt(1+d*r)-np.cbrt(d*r)
            return r*(1-r)*gap**3
        opt=minimize_scalar(lambda r:-objective(r), bounds=(1e-10,1-1e-10),
                            method='bounded', options={'xatol':1e-14})
        return float(-opt.fun),float(opt.x)

    def hcrit_2d(d):
        # u=sqrt(x/A), v_drive=sqrt(Xi/A); B=2g was eliminated exactly.
        def objective(loguv):
            u,v_drive=np.exp(loguv)
            f=u*u*(4*v_drive*v_drive-d*(1+u*u+4*u*v_drive)) / \
                (1+u*u+2*u*v_drive)**2
            return f/(4*v_drive*v_drive)
        opt=minimize(lambda q:-objective(q),np.log([.5,np.sqrt(1+d)]),
                     method='Nelder-Mead',
                     options={'xatol':1e-11,'fatol':1e-14,'maxiter':5000})
        return float(-opt.fun),[float(x) for x in np.exp(opt.x)]

    audit=[]
    for d in [1e-3,1e-2,1e-1,1.,10.,100.,1000.]:
        one,_=hcrit_1d(d)
        two,_=hcrit_2d(d)
        error=abs(two/one-1)
        assert error < 1e-10
        audit.append(dict(d=d,Hcrit_1d=one,Hcrit_direct_2d=two,
                          relative_difference=error))

    fc,fp=c/10.6e-6,c/110e-6
    fh=fc+fp
    gate=thermal_gate(fc,fh,300,315)
    wc,wp,wh=2*pi*np.array([fc,fp,fh])
    d=gate['Delta_a']/gate['Delta0']
    hcrit,r=hcrit_1d(d)
    direct,uv=hcrit_2d(d)
    nc,nh,npump,ngh=3.28,3.28,3.61,3.28
    chi=100e-12
    alpha_c,alpha_p=.006*100,2*100
    ec_im=nc*c*alpha_c/wc
    ep_im=npump*c*alpha_p/wp
    dh=nh*ngh
    volume_per_pair=(10.6e-6/nc)**3
    h0=epsilon_0*volume_per_pair*dh*ec_im*ep_im*wp / \
        (2*chi**2*hbar*wc*wh*gate['Delta0'])
    ratio=hcrit/h0
    critical_volume=volume_per_pair*ratio
    return dict(status='MIXED_SOURCE_CONDITIONAL_SCENARIO_NOT_GaAs_PERFORMANCE',
                assumptions='Identical independent mode pairs, uniform common pump, '
                'saturated spatial overlap, independently tunable contacts, weak loss, '
                'linear local thermal baths, no extra parasitic modes or pump loss.',
                gate=gate, d=d, Hcrit=hcrit,Hcrit_direct_2d=direct,
                optimal_low_mode_hot_contact_fraction=r,
                optimal_u_vdrive=uv,
                assumed_chieff_pm_per_V=chi/1e-12,
                assumed_alpha_c_cm_inv=alpha_c/100,
                assumed_alpha_p_cm_inv=alpha_p/100,
                loss_provenance='alpha_c from other-crystal calorimetry, with unresolved '
                'incident/internal-intensity convention; alpha_p fitted from 2007 DFG at '
                '110 um, not independent direct absorption; chi_eff is model input.',
                reference_volume_per_pair_m3=volume_per_pair,
                H0=float(h0), Qcold_over_Pabs_upper_bound=float(ratio),
                required_volume_per_pair_for_COPabs_gt1_m3=float(critical_volume),
                critical_volume_cube_side_nm=float(critical_volume**(1/3)*1e9),
                required_volume_for_positive_cooling_with_cold_deposition_fraction_point1_m3=
                    float(critical_volume/.1),
                independent_optimization_checks=audit)


def main():
    fc, fh=c/10.6e-6, c/9.6e-6
    gates=[thermal_gate(fc,fh,300,th) for th in (315,330)]
    candidate_gates=[thermal_gate(20e12,24e12,300,330),
                     thermal_gate(30e12,35e12,300,330)]
    parameter_sets=[
        ('2003 old parameters',134,[-.59,.14,-.07]),
        ('2003 revised example as tabulated by Roman 2006',134,[-.59,.16,-.13]),
        ('2006 rescaled ab initio alternative',277,[-.59,-.041,-.20])]
    dispersions=[]
    for label,fs in [('GaAs proposed 20/24/4 THz',[20,24,4]),
                     ('GaAs nearby 10.6/9.6 um',[fc/1e12,fh/1e12,(fh-fc)/1e12])]:
        for name,ce,cs in parameter_sets:
            dispersions.append(dict(trio=label, frequencies_THz=fs,
                model=name, chi_e_pm_per_V=ce, C1_C2_C3=cs,
                f_TO_THz=8.05, gamma_THz=.29,
                status='MODEL_EXTRAPOLATION_NOT_TARGET_MEASUREMENT',
                **flytzanis(fs,ce,cs)))
    result=dict(status='PHYSICAL_INTERFACE_GATE_DERIVED_MATERIAL_CLOSURE_UNKNOWN',
                acquired_measurement='NONE', usage_receipts='UNKNOWN',
                normalization_checks=independent_normalization_check(),
                pump_absorption_bound_audit=pump_absorption_bound_audit(),
                nearby_trio_gates=gates, original_candidate_gates=candidate_gates,
                conditional_envelopes=[conditional_envelope(g) for g in gates],
                susceptibility_model_scenarios=dispersions,
                complete_matched_three_frequency_loss_and_chi_dataset='UNKNOWN')
    (OUT/'material_interface_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
