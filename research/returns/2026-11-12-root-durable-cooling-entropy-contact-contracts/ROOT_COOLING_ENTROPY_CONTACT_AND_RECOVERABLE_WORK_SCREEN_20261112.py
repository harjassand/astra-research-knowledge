"""ROOT analytic screens; introduced properties, not a qualified material/device."""
import json, math
from pathlib import Path

Q=10000.0
cpw=4180.0
Tret,Tsupply,Tair=285.15,280.15,308.15
water_mdot=Q/(cpw*(Tret-Tsupply))
Scold=water_mdot*cpw*math.log(Tret/Tsupply)
air_rise=5.0
sink_entropy_per_J=math.log((Tair+air_rise)/Tair)/air_rise
Wrev_finite_air=Scold/sink_entropy_per_J-Q
pump=water_mdot/1000.0*100000.0/.5
controls=30.0
fan_a=50.0/(1.15*1000.0*air_rise*.5)
q_kJ,loading=5.0,3.0
material_mdot=Q/(1000*q_kJ)
eta_motor=.9

def wall(unloading,eta_return):
    drive=material_mdot*(loading-eta_return*unloading)*1000/eta_motor
    total=(drive+pump+controls+fan_a*Q)/(1-fan_a)
    return {'drive_W':drive,'pump_W':pump,'controls_W':controls,'fan_W':fan_a*(Q+total),'wall_W':total,'COP':Q/total}

ports=[]
for hot_C in [40.,42.,45.,47.,50.]:
    Tc,Th=277.15,hot_C+273.15
    wmin=q_kJ*(Th/Tc-1)
    unload_ceiling=loading-wmin
    drive_allowed=(Q/5)*(1-fan_a)-pump-controls-fan_a*Q
    eta_needed=(loading-drive_allowed*eta_motor/(material_mdot*1000))/unload_ceiling
    hpinch=Th-(Tair+air_rise)
    UA=None if hpinch<=0 else 12000*math.log((Th-Tair)/hpinch)/air_rise
    ports.append({'cold_C':4.,'hot_C':hot_C,'q_kJ_kg_cycle':q_kJ,'internal_reversible_net_work_kJ_kg':wmin,'max_unloading_at_3kJ_loading':unload_ceiling,'internal_work_shortfall_if_unloading_2_4':max(0.,wmin-.6),'minimum_eta_return_for_COP5_at_reversible_material_loop':eta_needed,'eta_le_1':eta_needed<=1.,'air_out_C':40.,'terminal_approach_K':hpinch,'UA_W_K_at_12kW_rejection':UA,'introduced_air_area_m2_at_U40':None if UA is None else UA/40,'eta_0_95_screen':wall(unload_ceiling,.95),'qualification':'Isothermal material-port specialization only; not a bound on distributed regenerative ports. Reversible material loop is an upper ceiling, not a supplied cycle.'})

# Linear apparent-capacity slab diagnostic with introduced constant properties.
# Average slab response to a fluid-temperature step with equal convection on both faces.
rho,k_s,cp_s,Lphase,phase_band=6450.,15.,500.,10000.,4.
cp_eff=cp_s+Lphase/phase_band
alpha=k_s/(rho*cp_eff)
def roots(Bi,n=24):
    rr=[]
    for j in range(n):
        lo=j*math.pi+1e-12;hi=(j+.5)*math.pi-1e-12
        for _ in range(70):
            mid=(lo+hi)/2
            if mid*math.tan(mid)<Bi:lo=mid
            else:hi=mid
        rr.append((lo+hi)/2)
    return rr

def mean_residual(t,half_thickness,h):
    if h is None:
        return sum(8/(math.pi**2*(2*j+1)**2)*math.exp(-((j+.5)*math.pi)**2*alpha*t/half_thickness**2)for j in range(24))
    Bi=h*half_thickness/k_s
    out=0.
    for mu in roots(Bi):
        coef=4*math.sin(mu)**2/(mu*(2*mu+math.sin(2*mu)))
        out+=coef*math.exp(-mu*mu*alpha*t/half_thickness**2)
    return out

thermal=[]
for thickness_mm in [.1,.5,1.43]:
    a=thickness_mm/2000
    for h in [None,5000.,10000.]:
        lo,hi=0.,100.
        for _ in range(70):
            mid=(lo+hi)/2
            if mean_residual(mid,a,h)>.1:lo=mid
            else:hi=mid
        t90=(lo+hi)/2
        thermal.append({'thickness_mm':thickness_mm,'h_W_m2K':h,'h_scope':'infinite limit'if h is None else'introduced constant film coefficient','alpha_m2_s':alpha,'time_to_90pct_mean_step_s':t90,'max_cycle_Hz_if_one_thermal_blow_is_quarter_cycle':1/(4*t90),'mean_response_at_0_25s':1-mean_residual(.25,a,h),'caveat':'Apparent cp surrogate, not a stress-driven phase front or measured transient heat-transfer model.'})

# Fixed 2kg active inventory geometry; steady fully-developed laminar estimates are diagnostics.
plates=[]
mass=2.;plate_length=.05;plate_width=.05;mu=.001;k_water=.6;rho_water=1000.
for t_mm in [.1,.5,1.43]:
    t=t_mm/1000
    for gap_rule in ['fixed_0.2mm','fixed_gap_over_thickness']:
        gap=.0002 if gap_rule=='fixed_0.2mm'else .0002*t/.00143
        count=mass/(rho*plate_length*plate_width*t)
        area=2*mass/(rho*t)
        volume=count*plate_length*plate_width*gap
        mdot_instant=water_mdot/.25
        v=(mdot_instant/rho_water)/(count*plate_width*gap)
        dp=12*mu*plate_length*v/gap**2
        Re=rho_water*v*(2*gap)/mu
        h_diag=7.54*k_water/(2*gap)
        hydraulic_avg=dp*(mdot_instant/rho_water)*.25
        raw_shuttle=volume*rho_water*cpw*36
        plates.append({'thickness_mm':t_mm,'gap_rule':gap_rule,'gap_mm':gap*1000,'plate_count_continuous_geometry':count,'two_face_area_m2':area,'fluid_inventory_L':volume*1000,'instant_velocity_m_s_at_quarter_cycle_blow':v,'instantaneous_laminar_diagnostic_dp_Pa':dp,'Reynolds_diagnostic':Re,'steady_Nu7_54_h_W_m2K':h_diag,'average_internal_hydraulic_W_before_pump_loss':hydraulic_avg,'unrecovered_full_36K_inventory_shuttle_J_cycle':raw_shuttle,'residual_shuttle_W_if_95pct_recovered_at_1Hz':.05*raw_shuttle,'caveat':'No manifold, transient, contact, phase, manufacture or stress-support closure. Shuttle is an alternative gross-to-net accounting diagnostic; never subtract it again from already-net q.'})

support=[]
for thickness_mm in [.1,.5,1.43]:
    # Introduced elastic Euler plate-strip screen; no phase-dependent modulus supplied.
    E,stress,K=50e9,500e6,1.
    thickness=thickness_mm/1000
    unsupported_max=math.pi*thickness*math.sqrt(E/(12*stress))/K
    support.append({'thickness_mm':thickness_mm,'E_Pa':E,'compression_stress_Pa':stress,'effective_length_factor':K,'maximum_unsupported_pitch_mm':unsupported_max*1000,'introduced_50mm_unbraced_Euler_stress_MPa':math.pi**2*E*(thickness/(K*.05))**2/12/1e6,'scope':'Weak-axis pinned elastic strip diagnostic only. Guides/contact, tension, curvature, different geometry or material can change it but their friction, heat and manufacturing are not free.'})

out={'scope':'New independent conditional conservation/interface screens, no producer execution, source navigation, physical test or qualified device. Every property/geometry except referenced 1.43mm stock thickness is introduced. No new lifetime or source claim.', 'whole_utility_entropy':{'cold_water_kg_s':water_mdot,'entropy_removed_W_K':Scold,'minimum_work_W_if_air_warms_35_to_40C':Wrev_finite_air,'ideal_COP_with_finite_air_rise':Q/Wrev_finite_air,'Carnot_material_COP_4C_40C':277.15/36,'unconstrained_old_power_example':wall(2.4,.95),'warning':'Earlier 3/2.4kJ work and net q5 with 4C/40C ports were separately introduced screens. This new specialization disallows silently treating all of them as a supplied thermodynamically consistent joint cycle. Distributed regenerative heat ports require their actual entropy integral.'},'isothermal_material_ports':ports,'apparent_capacity_slab':{'introduced':{'rho':rho,'k_W_mK':k_s,'base_cp_J_kgK':cp_s,'phase_heat_J_kg':Lphase,'phase_window_K':phase_band,'apparent_cp_J_kgK':cp_eff},'cases':thermal},'fluid_geometry_trade':plates,'compression_support':support}
for r in ports:
    assert abs((loading-r['max_unloading_at_3kJ_loading'])-r['internal_reversible_net_work_kJ_kg'])<1e-12
    s=r['eta_0_95_screen'];assert abs(s['wall_W']-s['drive_W']-s['pump_W']-s['controls_W']-s['fan_W'])<1e-9
assert Wrev_finite_air>0 and ports[0]['UA_W_K_at_12kW_rejection']is None
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'json':str(p),'finite_air_ideal_COP':out['whole_utility_entropy']['ideal_COP_with_finite_air_rise'],'ports':ports,'thermal_1_43mm':[r for r in thermal if r['thickness_mm']==1.43],'plate_trade':plates},indent=2))
