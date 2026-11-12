"""ROOT conditional cost, mechanical recovery and cooling balances; no device data fit."""
import json
import math
from pathlib import Path

crf=.08*1.08**20/(1.08**20-1)
steam_nonpower=48.79-20.96
steam={
    "reported_heat_cost_USD_MWh":48.79,
    "reported_electricity_USD_MWh":20.96,
    "nonpower_cost_same_ledger_USD_MWh":steam_nonpower,
    "if_initial_capital_free_USD_MWh":48.79-17.89,
    "if_500k_capital_other_lines_unchanged_USD_MWh":48.79-17.89+17.89*500/1385.16,
    "if_reversible_COP_2point66615_no_age_effect_other_lines_unchanged":steam_nonpower+40/2.66615,
    "COP_required_to_make_35_if_nonpower_unchanged":40/(35-steam_nonpower),
    "25pct_less_than_introduced_31point88_comparator_USD_MWh":31.88*.75,
    "zero_service_COP_needed_at_500k_capital_for_that_comparator":
        40/(31.88*.75-500000*crf/7884),
}

# Finite cooling-stream reversible work; introduced constant-cp water.
cpw=4.18
Tc_out=280.15
Tc_in=285.15
Ta=308.15
Qperkg=cpw*(Tc_in-Tc_out)
entropy=cpw*math.log(Tc_in/Tc_out)
work=Ta*entropy-Qperkg
qcool=10.0
q_use=5.0  # INTRODUCED net useful kJ/kg/cycle at the required lift
mass_rate=qcool/q_use
motor=.9
wload=3.0
wunload=2.4
water_flow=qcool/(cpw*5)
water_pump=water_flow/1000*100000/.5/1000
control=.03
cases=[]
for dp_air in (50,100):
    fan_fraction=dp_air/(1.15*1000*5*.5)
    eta_needed=(wload-((qcool/5)*(1-fan_fraction)-water_pump-control-fan_fraction*qcool)*motor/mass_rate)/wunload
    for eta_recovery in (.8,.95,1.0):
        drive=mass_rate*(wload-eta_recovery*wunload)/motor
        # Fan heat and all purchased drive/auxiliary power end at the air sink.
        wall=(drive+water_pump+control+fan_fraction*qcool)/(1-fan_fraction)
        fan=fan_fraction*(qcool+wall)
        assert abs(wall-drive-water_pump-control-fan)<1e-10
        cases.append({
            "introduced_air_dp_Pa":dp_air,
            "introduced_mechanical_unloading_work_recovery":eta_recovery,
            "motor_grid_kW":drive,"water_pump_grid_kW":water_pump,
            "fan_grid_kW":fan,"control_grid_kW":control,
            "all_wall_kW":wall,"delivered_cooling_COP":qcool/wall,
            "mechanical_recovery_needed_for_COP5":eta_needed,
        })

geometry=[]
for freq in (.5,1,3.5):
    mass=mass_rate/freq
    volume=mass/6450  # INTRODUCED density
    area=volume/.05
    geometry.append({
        "introduced_Hz":freq,"active_kg":mass,
        "introduced_50mm_parallel_bed_500MPa_force_N":area*500e6,
        "introduced_4pct_strain_stroke_m":.05*.04,
        "cycles_year_4000h":freq*4000*3600,
        "cycles_20year_at_4000h":freq*4000*3600*20,
        "operating_hours_for_5million_cycles":5e6/freq/3600,
    })

renewal=[]
for price in (100,1000):
    for cycles in (5e6,2e7,1e8):
        renewal.append({"introduced_prepared_USD_kg":price,"introduced_cycles_between_renewal":cycles,
                        "active_material_only_USD_MWh_cooling":3_600_000*price/(cycles*q_use)})

annual_cooling=qcool*4000/1000
capital=300*qcool
electricity=annual_cooling/5*80
other_room=30*annual_cooling-electricity-capital*crf-capital*.03

# Surface-preparation time screen from declared fabrication dimensions and
# an INTRODUCED square raster interpretation; not actual factory throughput.
mass=mass_rate
sheet_plan_area=mass/(6450*.00143)
shots=sheet_plan_area/(.001**2)*3*2
treatment={
    "introduced_active_mass_kg":mass,
    "introduced_density_kg_m3":6450,
    "declared_sample_stock_thickness_m":.00143,
    "introduced_square_raster_pitch_m":.001,
    "introduced_three_passes_each_of_two_sides_shots":shots,
    "hours_at_1Hz":shots/3600,
    "optical_kWh_at_4point97J_shot":shots*4.97/3_600_000,
    "wall_kWh_at_introduced_5pct_laser_efficiency":shots*4.97/3_600_000/.05,
    "introduced_100USD_hour_processing_cost":shots/3600*100,
    "limits":"No validated raster equivalence, process-rate scaling, heat control, yield or sample-to-module fatigue transfer.",
}

result={
    "status":"INTRODUCED_COUPLED_OPERATION_SCREENS_NOT_A_COOLING_INVENTION",
    "steam_ledger_diagnostics_not_all_heat_pumps":steam,
    "cooling_12to7C_to_35C_air_reversible_screen":{
        "cp_kJ_kgK":cpw,"cooling_kJ_kg":Qperkg,"entropy_removed_kJ_kgK":entropy,
        "work_min_kJ_kg":work,"maximum_glide_COP":Qperkg/work,
        "introduced_4C_cold_40C_hot_two_level_Carnot_COP":277.15/(313.15-277.15)},
    "introduced_material_cycle":{
        "net_useful_kJ_kg_cycle":q_use,"loading_work_kJ_kg":wload,
        "recoverable_unloading_work_kJ_kg":wunload,"motor_efficiency":motor,
        "net_material_throughput_kg_s":mass_rate},
    "self_consistent_drive_fan_water_cases":cases,
    "force_inventory_fatigue_cases":geometry,
    "replacement_material_screens":renewal,
    "introduced_300USD_kW_5COP_80USD_MWh_4000h_cost":{
        "annual_cooling_MWh":annual_cooling,"initial_capital_USD":capital,
        "annual_electricity_USD":electricity,"annual_capital_recovery_USD":capital*crf,
        "introduced_3pct_capital_maintenance_USD_year":capital*.03,
        "remaining_USD_year_for_every_other_duty_at_30USD_MWh":other_room},
    "surface_treatment_screen":treatment,
    "limits":[
        "No fitted or measured simultaneous work/cooling/fatigue/cost point is supplied.",
        "Five million cycles are an illustrative replacement interval, not an observed failure or a new qualification gate.",
        "Lower bending force does not guarantee equal active transformed mass, work, heat-transfer area or useful lift.",
        "Material-only replacement cost cancels frequency when qualified life is cycle-count limited; installation and service do not.",
        "The paid old steam plant and the new chilled-water operation are different endpoints; neither is claimed achieved.",
        "No source/SI/artifact recovery, producer execution, purchase, installation, billing or physical test occurred."]}
p=Path(__file__).with_suffix('.json')
p.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
