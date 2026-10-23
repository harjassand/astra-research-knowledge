"""Algebraic face checks only. No evolution, calibration, or physical D selection.
Normalized mobilities below are unit-test fixtures, not measured bed coefficients.
"""
from pathlib import Path
import hashlib, importlib.util, json, time, resource
import numpy as np
ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'nitrogen_finite_cycle_20261021/thermo_helper/helper.py'
spec = importlib.util.spec_from_file_location('pinned_continuous_thermo', SOURCE)
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
K = module.ThermoKernel()

def thermodynamics(T, Y, p):
    cpR, hRT, sR = (a[:, 0] for a in K.thermochemistry(T))
    ri = K.R / K.W
    x = (Y / K.W) / np.sum(Y / K.W)
    h = ri * T * hRT
    standard_mu_over_T = ri * (hRT - sR)
    mu_over_T = standard_mu_over_T + ri * np.log(x * p / K.P0)
    return h, standard_mu_over_T, mu_over_T

def normalized_face(TL, YL, pL, TR, YR, pR):
    """Return normalized dissipative fluxes; alpha=1, k/d=1 are algebra fixtures.
    A physical implementation MUST supply qualified coefficients and boundary data.
    Only strictly positive Y are admitted here; no clipping or log floors.
    """
    for Y in (YL, YR):
        assert np.all(Y > 0) and abs(Y.sum()-1) < 1e-12
    hL, aL, muTL = thermodynamics(TL, YL, pL)
    hR, aR, muTR = thermodynamics(TR, YR, pR)
    dbeta = 1/TR - 1/TL
    hface = (aR-aL)/dbeta if TR != TL else hL
    dv = -(muTR-muTL)
    z = dv + hface*dbeta
    ym = .5*(YL+YR)
    proj = np.eye(6)-np.outer(ym, np.ones(6))
    mobility = proj @ np.diag(K.W*ym) @ proj.T
    species = mobility @ z
    heat = TL*TR*dbeta
    energy = hface @ species + heat
    sigma_direct = species @ dv + energy*dbeta
    sigma_factored = z @ mobility @ z + TL*TR*dbeta**2
    xL=(YL/K.W)/sum(YL/K.W); xR=(YR/K.W)/sum(YR/K.W)
    z_ideal=-(K.R/K.W)*np.log(xR*pR/(xL*pL))
    return dict(species=species, heat=heat, energy=energy,
                sigma_direct=sigma_direct, sigma_factored=sigma_factored,
                z=z, z_ideal=z_ideal, hface=hface, dv=dv,
                sigma_without_enthalpy=species@dv+heat*dbeta,
                mobility=mobility)

def main():
    t=time.monotonic()
    YL=np.array([.73,.20,.01,.015,.04,.005])
    YR=np.array([.72,.21,.012,.013,.039,.006])
    f=normalized_face(2700,YL,110000,2300,YR,100000)
    mass_relative=abs(f['species'].sum())/np.linalg.norm(f['species'],1)
    sigma_relative=abs(f['sigma_direct']-f['sigma_factored'])/f['sigma_factored']
    ideal_relative=np.linalg.norm(f['z']-f['z_ideal'])/np.linalg.norm(f['z_ideal'])
    # Verify the continuum common-D mobility identity on a simplex tangent.
    ym=.5*(YL+YR); Wmix=1/sum(ym/K.W); b=1/K.W
    A=K.R*(np.diag(1/(K.W*ym))-Wmix*np.outer(b,b))
    tangent=np.array([1.,-2.,3.,-4.,5.,-3.])
    fick_identity=np.linalg.norm(f['mobility']@A@tangent/K.R-tangent)/np.linalg.norm(tangent)
    assert fick_identity < 1e-13
    # Closed two-cell conservative assembly. Volumes differ deliberately.
    VL,VR=.003,.007
    rateL=-np.r_[f['species'],f['energy']]/VL
    rateR=np.r_[f['species'],f['energy']]/VR
    balance=VL*rateL+VR*rateR
    ledger_relative=np.max(abs(balance))/max(np.max(abs(np.r_[f['species'],f['energy']])),1)
    assert mass_relative < 1e-13 and sigma_relative < 1e-12
    assert ideal_relative < 1e-12 and ledger_relative < 1e-14
    assert f['sigma_factored'] >= 0
    # LTE total-conductivity double count and opposing-gradient counterexample.
    kg,ks,gg,gs=1.,1.,1.,-1.
    ktotal=kg+ks
    correct=-kg*gg-ks*gs
    double_count=-ktotal*gg-ks*gs
    assert correct == 0 and double_count == -1
    # Constitutive identifiability: equal LTE total, unequal non-LTE fluxes.
    partitions=[(0.,2.),(.5,1.5),(1.,1.),(1.5,.5),(2.,0.)]
    off_lte=[dict(kg=a,ks=b,LTE_total=a+b,flux=-a*gg-b*gs) for a,b in partitions]
    # Existing code's solid face conductivity. No material-validation claim.
    KR=1.4161997074001969e-9*.2
    solid=[dict(T_K=T,k_s_existing_W_m_K=KR*T**3) for T in [300.,1000.,1700.,2500.,2700.]]
    # A common-D Fick flux is not generally entropy-safe in a pressure gradient.
    # Dimensionless binary example R1=1,R2=2; Y=(1/2,1/2), Y_x=(a,-a).
    # sigma/(eps*rho*D)=(16/3) a^2 - a * p_x/p. Set a=1, p_x/p=6.
    fick_binary=dict(R=[1.,2.],Y=[.5,.5],Y_x=[1.,-1.],log_p_x=6.,
                     composition_term=16./3.,pressure_term=-6.,entropy_normalized=-2./3.)
    # Compute rather than trust the displayed rational result.
    yi=np.array(fick_binary['Y']); yp=np.array(fick_binary['Y_x']); ri=np.array(fick_binary['R'])
    x=yi*ri/sum(yi*ri)
    logxprime=yp/yi-sum(yp*ri)/sum(yi*ri)
    comp=sum(ri*yp*logxprime); pterm=sum(ri*yp)*6
    assert abs(comp-16/3)<1e-14 and comp+pterm < 0
    fick_binary.update(composition_term=float(comp),pressure_term=float(pterm),entropy_normalized=float(comp+pterm))
    result=dict(scope=__doc__,
                face=dict(relative_mass_sum=mass_relative,relative_entropy_identity_residual=sigma_relative,
                          positive_entropy_production_normalized=float(f['sigma_factored']),
                          relative_ideal_force_identity_residual=ideal_relative,
                          relative_closed_inventory_balance=ledger_relative,
                          relative_common_D_tangent_identity=fick_identity,
                          species_enthalpy_transport_omission_entropy_normalized=float(f['sigma_without_enthalpy'])),
                total_conductivity_counterexample=dict(kg=kg,ks=ks,gas_gradient=gg,solid_gradient=gs,
                                                       correct_total_flux=correct,double_counted_total_flux=double_count,
                                                       units='Normalized algebra example, not a bed property fit'),
                nonidentifiable_LTE_partitions=off_lte,
                isothermal_pressure_gradient_Fick_counterexample=fick_binary,
                existing_conditional_solid_coefficient=solid,
                runtime_s=time.monotonic()-t,peak_rss_KiB_linux=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(__file__).with_name('face_diagnostics_result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__ == '__main__': main()
