"""ROOT independent balances. Introduced surrogates are not qualified devices."""
import json,math
from pathlib import Path

# Available returned construction; rounding remains the producer's.
A0,P0=778.538,186.462
Ac,Af,Pf=524.026,242.432,7.804
fine_needed=.95*A0-Ac
paste_ceiling=Af*.03/.97
old={'fine_aggregate_fraction_needed_after_passing_coarse':fine_needed/Af,'fine_paste_removal_for_97pct_purity_if_no_aggregate_lost_kg_t':max(0,Pf-paste_ceiling),'nominal_extra_paste_removal_if_absorption_excess_scales_with_retained_paste_kg_t':Pf*(1-1/1.2),'disposal_removed_but_no_quality_repair_USD_t':41.79-12.69,'free_all_initial_replacement_decommissioning_then_USD_t':41.79-12.69-10.28,'free_all_electricity_then_USD_t':41.79-12.69-1.86,'warning':'Removing a cost line does not construct accepted sand or a free machine. Absorption scaling is newly introduced, not measured.'}

# Different PV operation screen, not a qualified whole refinery.
area_t=100.;G=1000.;width=1.;theta=math.pi/2
pv={'introduced_module_area_m2_t':area_t,'introduced_fracture_G_J_m2':G,'ideal_90deg_peel_force_N':G*width/(1-math.cos(theta)),'ideal_interface_work_kWh_t':G*area_t/3.6e6,'front_speed_m_s_at_1t_h_1m_width':area_t/(3600*width),'whole_tonne_sensible_heat_kWh_at_0_8kJkgK_115K':1000*.8*115/3600,'scope':'No fracture path, surface purity, component recovery, heat loss, installed machine or novel advantage supplied. Commercial heated knife and brush scraper are credited from actual manufacturer-page exposure.'}

# Standalone co-located industrial wet-cake to dry-product operation.
feed=1000.;si=.7;so=.98;solid=feed*si
product=solid/so;removed=feed-product;retained=product-solid
rho_s,rho_w=2740.,1000.
porosity=.47
void_per_kgsolid=porosity/(1-porosity)/rho_s
S_required=(retained/rho_w)/(solid*void_per_kgsolid)
Srem=.25
water_at_Srem=solid*void_per_kgsolid*Srem*rho_w
wrem=water_at_Srem/(solid+water_at_Srem)
phi_required=(.02/.98*rho_s/(rho_w*Srem))/(1+.02/.98*rho_s/(rho_w*Srem))
water={'feed_kg':feed,'input_solid_mass_fraction':si,'dry_solid_kg':solid,'product_kg_at_98pct':product,'removed_water_kg':removed,'retained_water_kg':retained,'saturated_input_porosity':(feed-solid)/rho_w/((feed-solid)/rho_w+solid/rho_s),'required_S_if_phi_0_47':S_required,'water_wet_fraction_at_fixed_phi_0_47_Srem_0_25':wrem,'phi_needed_at_fixed_Srem_0_25_for_2pct_water':phi_required,'qualification':'Input slurry must first be formed/consolidated with its liquid paid. Source epsilon0.47/density2740/Srem0.25 belong to that limestone/50kPa fitted case. Do not extrapolate its Srem to all materials or pressures.'}

# Paid compression: one gas void-volume charge, ideal isothermal, no vent leakage yet.
P0abs=1e5;T=298.15;Rsp=287.
end_void=solid*void_per_kgsolid
end_gas_volume=end_void-retained/rho_w
liquid_volume=removed/rho_w
pressure=[]
for MPa in [1.,5.,15.,20.]:
    P=MPa*1e6; ratio=P/P0abs
    r=2*.072/P
    water_work=P*liquid_volume/3.6e6
    gas_ideal=P*end_gas_volume*math.log(ratio)/3.6e6
    gas_mass=P*end_gas_volume/(Rsp*T)
    pressure.append({'pressure_MPa':MPa,'wetting_radius_capillary_scale_nm':r*1e9,'pressure_times_all_removed_liquid_volume_kWh_t_feed':water_work,'end_gas_volume_m3_t_feed':end_gas_volume,'one_end_gas_inventory_charge_isothermal_kWh_t_feed':gas_ideal,'compressor_0_65_kWh_t_feed':gas_ideal/.65,'gas_inventory_kg_t_feed':gas_mass,'thinwall_t_over_r_at_allowable150MPa':P/150e6,'warning':'Single-charge surrogate excludes breakthrough gas, cycling, preparation, real gas, heat and depressurization. P*dV includes initial slurry-formation drainage here only as an alternative overinclusive scale. Do not add it to compressor work as an independent paid drive if compressor already supplies displacement.'})

# A two-path toy exhibits gas short circuit; not a calibrated material model.
paths=[]
L=.002;A=1.;k=1e-16;mu_l=.001;mu_g=1.8e-5;deltaP=15e6
for wet_fraction in [1.,.1,.01,.001]:
    # introduced wet relative permeability collapses cubically;
    # an already open dry patch maintains a gas path.
    krl=wet_fraction**3;open_gas=.01
    Ql=k*krl*deltaP/(mu_l*L)*A
    Qg=k*open_gas*deltaP/(mu_g*L)*A
    gas_std=Qg*(15e6/1e5)
    paid=(15e6*Qg*math.log(150)/.65)/3.6e6
    paths.append({'introduced_effective_wet_fraction':wet_fraction,'liquid_L_m2_h':Ql*3.6e6,'gas_highP_L_m2_h':Qg*3.6e6,'gas_standard_m3_m2_h':gas_std*3600,'gas_compression_kWh_m2_h':paid*3600,'gas_per_removed_water_highP_volume':Qg/Ql,'scope':'Two-path introduced Darcy/isothermal surrogate only. No claim these k/relative-permeability functions hold for a real paste.'})

# Final trim if a fixed residual saturation persists.
trim=max(0,water_at_Srem-retained)
thermal_trim={'trim_water_kg_t_feed_if_source_fixed_saturation_persists':trim,'trim_share_of_total_removed_water':trim/removed,'introduced_0_55kWh_kg_trim_per_total_removed_kg':trim*.55/removed,'introduced_0_20kWh_kg_trim_per_total_removed_kg':trim*.20/removed,'warning':'Do not use source residual saturation at untested pressure as a universal bound. Heat-pump figures are introduced, not measured quotes.'}

# Whole-cycle desorption bound: supplied energy goes somewhere even without vaporizing.
adsorption=[]
Rwater=461.5
for aw in [.9,.5,.1]:
    # Work per kg water for reversible extraction from activity aw to pure water.
    w=Rwater*T*math.log(1/aw)/3.6e6
    adsorption.append({'introduced_water_activity':aw,'minimum_reversible_separation_kWh_kgwater_at25C':w,'qualification':'Only that water at that activity; integrate over the measured sorption path, do not apply the last-drop activity to all removed water.'})

rate_feed=10000.;annual_feed_t=rate_feed/1000*8760*.9
annual_removed_t=annual_feed_t*removed/feed
crf=.08/(1-(1.08)**-20)
fin={'wet_feed_t_y':annual_feed_t,'water_removed_t_y':annual_removed_t,'initial_capital_USD':1e6,'capital_recovery_USD_twater':crf*1e6/annual_removed_t,'introduced_electric_80kWh_twater_at40_USD_MWh':3.2,'remaining_USD_twater_below40_before_all_other_labor_renewal_maintenance_waste':40-crf*1e6/annual_removed_t-3.2,'capital_is_not_a_quote':True}

# Phase-blocking drain as an OPTIONAL construction; clean capillary membrane only.
mem=[]
for pore_nm in [2.,5.,10.]:
    r=pore_nm*1e-9;eps=.3;tortuosity=2.;thickness=1e-6
    kk=eps*r*r/(8*tortuosity)
    cap=2*.072/r
    flux=kk/(.001*thickness)*15e6
    mem.append({'introduced_pore_radius_nm':pore_nm,'clean_entry_pressure_MPa':cap/1e6,'clean_ideal_flux_L_m2_h_at15MPa':flux*3.6e6,'scope':'No actual membrane strength, wetting, defects, support, fouling, chemical compatibility or trapped-water contact is supplied. Tiny drain pores do not reconnect isolated water inside cake.'})

out={'scope':'Own analytic calculations only. No physical test or producer execution. New properties/functions explicitly introduced, source fits retain exact selected scope.','concrete_reassessment':old,'PV_comparison':pv,'drying_mass':water,'pressure_budget':pressure,'gas_bypass':paths,'thermal_trim':thermal_trim,'sorption_work':adsorption,'full_cost':fin,'optional_phase_blocking_drain':mem}
assert abs(solid+retained+removed-feed)<1e-10
assert 0<S_required<Srem<1
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'concrete':old,'water':water,'pressure':pressure,'trim':thermal_trim,'finance':fin,'bypass':paths},indent=2))
