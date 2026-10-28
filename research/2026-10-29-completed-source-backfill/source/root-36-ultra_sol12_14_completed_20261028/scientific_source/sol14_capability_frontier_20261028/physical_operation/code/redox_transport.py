"""Two-interface liquid-Ga Al-transfer anode: flux/purity screening.

The primary sources provide observations in DIFFERENT media and regimes.
This program explicitly supplies its missing kinetic/activity parameters.
Its countermodel is not a forecast or a qualified physical material law.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
from pathlib import Path
import json,math,time
import numpy as np
from scipy.integrate import solve_bvp

ROOT=Path(__file__).resolve().parents[1]
F=96485.33212331002
R=8.31446261815324
MAL=.0269815385
MGA=.069723

def flux_coefficients(D,length,pe,ka=math.inf,kc=math.inf):
    # N=K_A c(0)-K_C c(L), for N=-D c'+v c and Pe=vL/D.
    ratio=1. if abs(pe)<1e-12 else pe/(-math.expm1(-pe))
    left=D/length*ratio
    right=left*math.exp(-pe)
    effective=left/(1+left/ka+right/kc)
    return left,right,effective

def run():
    begin=time.monotonic()
    # Ga diffusion is source-reported for 60/40 AlCl3/EMIMCl.
    # Al2Cl7 diffusion is source-reported in a DIFFERENT BMIM liquid.
    # T, concentrations, activity convention, interface equilibrium,
    # effective layers and zero migration below are supplied assumptions.
    T=303.15;RTF=R*T/F;EG=.437;cstar=1000.;Dga=9.12e-11
    D_al_complex=3.25e-12;c_al_complex=3000.
    delta=1e-5;Lga=2*delta;bulk_drop=0.
    _,_,kg=flux_coefficients(Dga,Lga,0.)
    # 4 Al2Cl7^- +3e -> Al +7 AlCl4^-.
    j_al_max=3*F/4*D_al_complex*c_al_complex/delta
    j_al=j_al_max
    mol_al=j_al/(3*F)
    al_rate=MAL*mol_al*3600
    rows=[]
    for ea in (0.,.05,.10,.15,.20,.25):
        c_eq=cstar*math.exp((ea-EG)/RTF)
        mol_ga=kg*c_eq
        ratio=MGA*mol_ga/(MAL*mol_al)
        rows.append({'anode_V_vs_model_Al':ea,'Ga_equilibrium_mol_m3':c_eq,
                     'Ga_flux_mol_m2_s':mol_ga,'Ga_mass_fraction':ratio/(1+ratio),
                     'Ga_ppm':1e6*ratio/(1+ratio)})
    gates=[]
    for allowed in (1e-6,1e-4,1e-3):
        ratio=allowed/(1-allowed)
        emax=EG+RTF*math.log(ratio*MAL*mol_al/(MGA*kg*cstar))
        gates.append({'declared_Ga_mass_fraction_gate':allowed,
                      'largest_anode_V_fast_equilibrium_model':emax,
                      'positive_Al_anode_overpotential_available':emax>0})
    leakage_recovery=[]
    high_ratio=rows[4]['Ga_mass_fraction']/(1-rows[4]['Ga_mass_fraction'])
    for allowed in (1e-6,1e-4,1e-3):
        suppression=high_ratio/(allowed/(1-allowed))
        leakage_recovery.append({
            'Ga_mass_fraction_gate':allowed,
            'required_transport_or_activity_suppression_at_Ea_point2':suppression,
            'maximum_source_Robin_ka_m_s_with_fast_sink':kg/(suppression-1)})
    assert gates[0]['largest_anode_V_fast_equilibrium_model']<0
    assert rows[4]['Ga_mass_fraction']>1e-3
    # A more informed ordinary hydrodynamic comparator does not force equal
    # diffusion-layer thickness for species with different diffusivities.
    # Grant both routes the same ideal Levich k(D) scaling, not actual hardware.
    nu=1e-5;omega=100.
    def levich(D):return .62*D**(2/3)*nu**(-1/6)*math.sqrt(omega)
    kal=levich(D_al_complex);kga=levich(Dga)/2
    jlev=3*F/4*kal*c_al_complex
    rlev=MGA*kga*rows[4]['Ga_equilibrium_mol_m3']/(MAL*jlev/(3*F))
    assert rlev/(1+rlev)>1e-3
    levich_gates=[]
    for allowed in (1e-6,1e-4,1e-3):
        emax=EG+RTF*math.log((allowed/(1-allowed))*MAL*jlev/(3*F*MGA*kga*cstar))
        levich_gates.append({'Ga_mass_fraction_gate':allowed,'max_anode_V':emax})
    # Same layer thickness cancels at Al mass-transfer capacity.
    for layer in (1e-6,1e-5,1e-4):
        k=Dga/(2*layer)
        ja=3*F/4*D_al_complex*c_al_complex/layer
        val=MGA*k*rows[4]['Ga_equilibrium_mol_m3']/(MAL*ja/(3*F))
        ref=rows[4]['Ga_mass_fraction']/(1-rows[4]['Ga_mass_fraction'])
        assert abs(val/ref-1)<1e-12
    # Independent ordinary boundary-value solver of the constant-field
    # trace species, including finite source/sink transfer coefficients.
    controls=[]
    for pe in (-3.,0.,3.):
        length=2e-5;D=Dga;ka=2e-5;kc=1e-5;ceq=rows[4]['Ga_equilibrium_mol_m3']
        a,b,k=flux_coefficients(D,length,pe,ka,kc);expected=k*ceq
        # Dimensionless x. y[0]=c/ceq, y[1]=N/(D ceq/L).
        vel=pe
        def ode(x,y):return np.vstack((vel*y[0]-y[1],np.zeros_like(y[0])))
        source=ka*length/D;sink=kc*length/D
        def bc(ya,yb):return np.array([ya[1]-source*(1-ya[0]),yb[1]-sink*yb[0]])
        xx=np.linspace(0,1,21);guess=np.vstack((1-xx,np.full_like(xx,.5)))
        sol=solve_bvp(ode,bc,xx,guess,tol=1e-10,max_nodes=2000)
        assert sol.success
        measured=float(sol.y[1,0])*D*ceq/length
        assert abs(measured/expected-1)<1e-9
        assert np.min(sol.y[0])>=-1e-10
        controls.append({'Pe':pe,'closed_flux':expected,'BVP_flux':measured,
                         'relative_error':abs(measured/expected-1),'mesh_nodes':sol.x.size})
    # Ga-side transport/inventory, deliberately assumed favorable to host.
    rho_ga=6000.;w_al=.01;Dmetal=1e-9;thickness=1e-4
    cmetal=rho_ga*w_al/MAL
    jmetal=3*F*Dmetal*cmetal/thickness
    inventory_al=rho_ga*thickness*w_al
    turnover_h=inventory_al/al_rate
    # Electrical cell-energy identity: no sonication/heat energy is included.
    reference_V=.65;eta=.989
    cell_kwh=reference_V*3*F/(MAL*3.6e6*eta)
    assert abs(cell_kwh-1.958)<.003
    # Conditional pulse-control comparison. This uses a supplied Tafel law,
    # NOT a measured Al-Ga exchange-current or transfer coefficient.
    Tpulse=343.;tafel=.09031
    p=tafel/(math.log(10)*R*Tpulse/F)
    pulse_j=np.array([.2,1.8]);pulse_w=np.array([.5,.5])
    pulse_leak=float(pulse_w@(pulse_j**p))
    assert p>1 and pulse_leak>1
    out={
      'status':'CANDIDATE_FAST_REVERSIBLE_GA_COUNTERMODEL_FAILS_DECLARED_PURITY_GATES; NO_PHYSICAL_CAPABILITY_ACQUIRED',
      'model_inputs':{'T_K':T,'Ga_formal_V_parameter':EG,'Ga_cstar_mol_m3':cstar,
       'Ga_D_m2_s':Dga,'Ga_diffusion_source_regime':'60/40 AlCl3-EMIMCl; source temperature/activity convention not fully acquired',
       'Al_complex_D_m2_s':D_al_complex,'Al_complex_diffusion_source_regime':'different BMIM liquid at343K; NOT SAME-BATH VALIDATION',
       'Al_complex_concentration_mol_m3_assumed':c_al_complex,'layer_each_m_assumed':delta,
       'Ga_surface_equilibrium_assumed':True,'Ga_cathode_perfect_sink_assumed':True,
       'Ga_activity_conversion_and_reference_assumed':True,'migration_assumed_Pe':0},
      'Al_charge_stoichiometry':'3 electrons and4 Al2Cl7 complexes per Al atom',
      'Al_current_density_A_m2':j_al,'Al_kg_m2_h':al_rate,
      'Ga_leakage_rows':rows,'purity_potential_gates':gates,
      'conditional_rescue_thresholds':leakage_recovery,
      'ordinary_independent_BVP_controls':controls,
      'mass_transfer_layer_cancellation':'PASS; thinning both layers raises flux without repairing purity ratio',
      'equally_informed_Levich_control':{
       'status':'SUPPLIED_HYDRODYNAMIC_MODEL; no actual liquid-Ga rotating disk qualified',
       'nu_m2_s_assumed':nu,'omega_rad_s_assumed':omega,
       'Al_current_density_A_m2':jlev,'Al_kg_m2_h':MAL*jlev/(3*F)*3600,
       'Ga_ppm_at_anode_point2V':1e6*rlev/(1+rlev),
       'purity_gates':levich_gates,
       'scope':'Common rotation factor cancels from impurity ratio; unequal species layer thickness reduces the earlier leakage forecast.'},
      'favorable_Ga_host_scenario':{
       'rho_kg_m3_assumed':rho_ga,'Al_mass_fraction_assumed':w_al,'Dmetal_m2_s_assumed':Dmetal,
       'thickness_m_assumed':thickness,'Ga_side_current_ceiling_A_m2':jmetal,
       'ratio_to_same_scenario_Al_ionic_ceiling':jmetal/j_al,
       'ratio_to_Levich_Al_ionic_ceiling':jmetal/jlev,
       'metal_host_inventory_kg_m2':rho_ga*thickness,
       'Al_inventory_kg_m2':inventory_al,'Al_inventory_turnover_seconds':turnover_h*3600,
       'active_area_for_1t_per_h_m2':1000/al_rate,
       'host_inventory_for_1t_per_h_kg':rho_ga*thickness*1000/al_rate,
       'hundred_Al_inventory_turnovers_hours':100*turnover_h,
       'Levich_Al_inventory_turnover_seconds':inventory_al/(MAL*jlev/(3*F)),
       'Levich_active_area_for_1t_per_h_m2':1000/(MAL*jlev/(3*F)*3600),
       'Levich_host_inventory_for_1t_per_h_kg':
           rho_ga*thickness*1000/(MAL*jlev/(3*F)*3600),
       'illustrative_feed_Al_fraction':.9,
       'nonAl_mass_per_kg_product_before_any_separation':1/.9-1,
       'hours_to_host1pct_debris_if_all_nonAl_enters_host':
           (.01*rho_ga*thickness)/(al_rate*(1/.9-1)),
       'dirty_scrap_to_host_admission_rate_acquired':False},
      'ordinary_reference':{'cell_V':reference_V,'cathodic_current_efficiency':eta,
       'cell_only_kWh_kg_computed':cell_kwh,'reported_kWh_kg':1.958,
       'meaning':'Numerical equality identifies a cell-charge-compatible figure. It does not prove paper excluded auxiliaries; full energy accounting not acquired.'},
      'conditional_pulse_control':{'T_K':Tpulse,'supplied_Tafel_V_dec':tafel,
       'Ga_leakage_power_in_Al_current':p,'constant_same_mean_current_normalized_leakage':1.,
       'two_level_same_mean_current_normalized_leakage':pulse_leak,
       'scope':'Jensen control under supplied fast-Ga/Tafel laws; not an experimentally qualified Al-Ga pulse result.'},
      'decision':'Do not advance liquid-Ga anode as acquired feasible scrap upgrader. Direct low-temperature solid-anode electrorefining remains the stronger source-reported alternative. Full-cycle superiority is UNKNOWN.',
      'seconds':time.monotonic()-begin}
    (ROOT/'results/REDOX_TRANSPORT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':run()
