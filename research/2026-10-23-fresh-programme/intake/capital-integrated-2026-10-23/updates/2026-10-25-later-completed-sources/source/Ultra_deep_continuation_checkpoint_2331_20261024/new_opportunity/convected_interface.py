"""Bounded proofs/replay for the rotation-only extension of the ionic skin.

Original frozen-axis files are imported without editing. Rational inequalities
certify the declared operators, not unknown material coefficients.
"""
from fractions import Fraction as F
import json
import math
from pathlib import Path

import elastic_interface as base


def shared_bounds(p):
    qbar = F(22500)
    kpl, kpu, hb = base.kp_bounds(qbar, p["b"], p["ce"])
    km0 = 2/(p["b"]*p["ce"])
    mlo = (km0-kpu)/(km0+kpu+2*p["kw"])
    sl, _, _, cu = hb
    ell = qbar*p["b"]/2
    cb = sl/(ell*cu**3)/(1+kpu/km0)
    bend = p["young"]*p["b"]**3/(12*(1-p["poisson"]**2))
    (_, c_hi), (_, sx_hi) = base.hyperbolic_bounds(p["rho"]*p["b"]**2*qbar**2)
    assert p["gamma"]*qbar**2+p["nu_m"]*kpl > p["j0"]/p["kn"]
    return qbar, kpu, km0, mlo, cb, bend, c_hi, sx_hi


def ordinary_global_certificate(p):
    qb, kpu, km0, mlo, cb, bend, c_hi, sx_hi = shared_bounds(p)
    delta = 2*(kpu+p["kw"])/km0
    abar = p["b"]/p["kn"]*sx_hi
    jbar = p["j0"]*delta/p["b"]*(abar+p["lmax"]*(c_hi-1))
    g2 = p["j0"]*p["b"]/2*(abar+p["lmax"]*(c_hi+1))
    chi0 = p["nu_m"]*p["kw"]*mlo**2
    c4 = p["nu_m"]*cb*bend
    bound = jbar-chi0+max(g2-p["gamma"], F(0))**2/(4*c4)
    assert bound < 0
    return {"scope": "rational C6 ordinary rotating-skin all-q certificate, mu=1MPa",
            "low_q_N_upper_V_per_m": base.ratio_record(bound),
            "qbar_per_m": int(qb), "high_q_certificate_shared_with_E7": True,
            "pass": True}


def weak_support_witness(p):
    q = F(4000)
    _, kpu, _ = base.kp_bounds(q, p["b"], p["ce"])
    chi_hi = p["gamma"]*q*q+p["nu_m"]*(2*kpu+p["kw"])
    (cs_lo, cs_hi), (sx_lo, sx_hi) = base.hyperbolic_bounds(p["rho"]*p["b"]**2*q*q)
    h_hi = cs_hi+p["lmax"]*p["kn"]*p["rho"]*p["b"]*q*q*sx_hi
    ell = q*p["b"]/2
    (_, cu), (slx, _) = base.hyperbolic_bounds(ell*ell)
    tanh_lo = ell*slx/cu
    llower = p["resistance"]+p["bulk_depth"]/p["bulk_kappa"]*(1-(q*p["bulk_depth"])**2/3)
    geo_lo = p["j0"]*q*tanh_lo*(p["b"]/p["kn"]*sx_lo+llower*(cs_lo+1))
    witness = geo_lo-chi_hi*h_hi
    assert p["rho"] >= 1 and witness > 0
    return {"scope": "rational same-skin ordinary instability, weak support mu=10kPa",
            "q_per_m": int(q), "N_lower_V_per_m": base.ratio_record(witness),
            "N_over_G_lower": base.ratio_record(witness/(p["j0"]/p["kn"])),
            "pass": True}


def response(p, q, rho, with_rv=True):
    x = {k: float(v) for k, v in p.items()}
    _, m, ke = base.elastic_twoport(q, x["b"], x["young"], x["poisson"], x["kw"])
    ll = x["resistance"]+math.tanh(q*x["bulk_depth"])/(x["bulk_kappa"]*q)
    aa = q*x["b"]
    cc, ss = math.cosh(aa*math.sqrt(rho)), math.sinh(aa*math.sqrt(rho))
    pp = x["kn"]*q*math.sqrt(rho)
    hh = cc+ll*pp*ss
    g = x["j0"]/x["kn"]
    chi = x["gamma"]*q*q+x["nu_m"]*ke
    r0 = q*(m-math.cosh(aa))/math.sinh(aa)
    rb = q*(m*math.cosh(aa)-1)/math.sinh(aa)
    rv = x["rv"] if with_rv else 0.
    nr = -chi*hh-x["j0"]*m*rv-x["j0"]*((ss/pp+ll*cc)*r0-ll*rb)
    nf = (g-chi)*hh-m*(g+x["j0"]*rv)
    den = x["r"]*cc+ss/pp+ll*(cc+x["r"]*pp*ss)
    return nr, nf, den


def rate(p):
    x = {k:float(v) for k,v in p.items()}
    mm = 1/(1+x["kw"]*x["b"]*x["ce"])
    g = x["j0"]/x["kn"]
    n_ordinary = g*(1-mm)-x["nu_m"]*x["kw"]*mm
    n_response = n_ordinary-mm*x["j0"]*x["rv"]
    den = x["r"]+x["b"]/x["kn"]+x["lmax"]
    lo = x["j0"]*den/(-n_ordinary)
    lr = x["j0"]*den/(-n_response)
    return {"ordinary_leveling_mean_height_m":lo,
            "responsive_leveling_mean_height_m":lr,
            "longwave_leveling_gain":lo/lr,
            "electrical_force_equivalent_Pa_per_m":x["j0"]*x["rv"]/x["nu_m"],
            "electrical_to_real_foundation_ratio":x["j0"]*x["rv"]/(x["nu_m"]*x["kw"])}


def main():
    p = base.declared_parameters()
    weak = dict(p)
    weak["mu"] /= 100
    weak["kw"] /= 100
    weak["p0"] /= 100
    ordinary = ordinary_global_certificate(p)
    witness = weak_support_witness(weak)
    responsive_weak = base.rational_certificate(weak)
    # Independent algebraic consistency in finite parameter cases, not the all-q proof.
    max_iso, max_order = 0., -float("inf")
    for q in (1000.,4000.,10000.,22500.,50000.):
        nr, nf, _ = response(p,q,1.)
        max_iso = max(max_iso,abs(nr-nf)/max(1.,abs(nf)))
        for rho in (1.,2.,10.,100.):
            nr,nf,_=response(p,q,rho)
            max_order=max(max_order,(nr-nf)/max(1.,abs(nf)))
    normal_rows = []
    weak_rows = []
    for q in (2000.,4000.,10000.):
        a,_,_=response(p,q,10.,False)
        b,_,_=response(p,q,10.,True)
        c,_,_=response(weak,q,10.,False)
        d,_,_=response(weak,q,10.,True)
        g=float(p["j0"]/p["kn"])
        normal_rows.append(dict(q=q,ordinary_N_over_G=a/g,responsive_N_over_G=b/g))
        weak_rows.append(dict(q=q,ordinary_N_over_G=c/g,responsive_N_over_G=d/g))
    out={"ordinary_all_q":ordinary,"weak_support_ordinary_witness":witness,
         "weak_support_responsive_all_q":responsive_weak,
         "original_support_rate":rate(p),"weak_support_rate":rate(weak),
         "finite_diagnostics":{"rho1_reduction_relative_error":max_iso,
             "maximum_relative_Nrot_minus_Nfrozen_rho_ge1":max_order,
             "original_support":normal_rows,"weak_support":weak_rows},
         "physical_scope":{"intrinsic_eigenvalues_strain_independent":True,
             "unstressed_incremental_operator_prescribed":True,
             "loaded_tangent_error_bounded":False,"same_film_material_acquired":False,
             "nonlinear_skin_basin_proved":False,"cycling_stability_proved":False}}
    Path(__file__).with_name("CONVECTED_INTERFACE_RESULTS.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"ordinary_all_q_N_upper":ordinary["low_q_N_upper_V_per_m"]["value"],
                      "weak_support_ordinary_N_lower":witness["N_lower_V_per_m"]["value"],
                      "weak_responsive_all_q_pass":responsive_weak["all_q_certificate_pass"],
                      "rate":out["original_support_rate"],"diagnostics":out["finite_diagnostics"]},indent=2))


if __name__=="__main__":
    main()
