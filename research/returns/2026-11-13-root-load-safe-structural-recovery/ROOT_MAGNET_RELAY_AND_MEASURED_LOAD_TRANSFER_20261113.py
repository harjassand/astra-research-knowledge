"""ROOT-owned introduced quasi-static relay and uncertainty screens only."""
import json


def run():
    # A common measured head load cannot generally certify all 24 pin loads.
    safe = [100.] * 24
    unsafe = [300.] + [(2400.-300.)/23] * 23
    assert abs(sum(safe)-sum(unsafe)) < 1e-9
    load, old_k, new_k = 1000., 1e6, 1e6
    equivalent_k = old_k*new_k/(old_k+new_k)
    steps=[]
    for fraction in [0., .25, .5, .75, .98, 1.]:
        actuator_after_contact = fraction*load/equivalent_k
        new_force = equivalent_k*actuator_after_contact
        old_force = load-new_force
        steps.append({"introduced_transfer_fraction": fraction,
                      "actuator_travel_after_contact_mm": actuator_after_contact*1000,
                      "old_force_N": old_force, "new_force_N": new_force,
                      "old_spring_energy_J": old_force**2/(2*old_k)})
    # Before contact an additional introduced 0.5mm clearance must be traversed.
    # Release at measured10N with +/-5N bias gives a worst-case15N residual.
    return {"common_head_observability": {
                "safe_individual_loads_N":safe,"unsafe_individual_loads_N":unsafe,
                "identical_head_load_N":sum(safe),"introduced_individual_limit_N":200},
            "one_dimensional_handoff": {
                "introduced_old_and_new_stiffness_N_m":[old_k,new_k],
                "introduced_total_load_N":load,"introduced_initial_gap_mm":.5,
                "quasi_static_after_contact_steps":steps,
                "measured_old_release_force_N":10.,"introduced_sensor_error_bound_N":5.,
                "worst_residual_force_N":15.,
                "worst_old_elastic_release_energy_J":15.**2/(2*old_k)},
            "magnet_force_screen": {
                "supplied_bar_width_thickness_slice_mm":[18.7,3.05,.28],
                "nominal_slice_area_mm2":2*(18.7+3.05)*.28,
                "introduced_10MPa_force_N":2*(18.7+3.05)*.28*10,
                "introduced_22MPa_force_N":2*(18.7+3.05)*.28*22},
            "same_unchanged_magnet_service_ledger": {
                "reported_conditional_service_USD_kg":88.30,
                "free_capital_and_major_renewal_plus_electricity_USD_kg":88.30-36.23-1.33,
                "reported_no_EDM_capital_USD":603750,
                "reported_no_EDM_service_USD_kg":39.73,
                "reported_conditional_campaign_kWh_kg":481.03/22.1487291,
                "population_to_annual_demand_diagnostic_years":42200/16681},
            "scope": "introduced scalar springs, known contact/no slip, bounded sensor bias and quasi-static motion only; no six-axis joint, hardware, fracture, fatigue, actuator access or procurement qualification"}


if __name__ == '__main__':
    print(json.dumps(run(),indent=2))
