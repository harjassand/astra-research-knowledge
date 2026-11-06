"""Additional exact full-family sustaining-supply certificate."""
import json
from fractions import Fraction as Q
from exact import exp_minus, require
from plan import ROOT, save


def main():
    p=json.loads((ROOT/'results/PLAN.json').read_text())
    q=lambda k:Q(p[k])
    theta=q('source_only_equilibrium_relative_error')
    target=list(map(Q,p['target_amplitudes']))
    lower_sq=(1-theta)**2*sum((x*x for x in target),Q(0))
    qbar=(1+theta)*q('target_norm_upper')
    delta=q('retention_radius_about_true_equilibrium')
    lo,hi,cost=exp_minus(q('settling_time_after_switch')/q('actuator_time_constant'),96)
    dhold=q('actuator_tracking_error_at_switch')*hi+q('continuing_actuator_tracking_error')
    power=Q(p['source_priors']['a'])*lower_sq-delta*Q(p['source_priors']['A0'])*qbar
    power-=(qbar+delta)*(q('local_feedback_Lipschitz')*delta+dhold)
    require(power>Q(3744,1000))
    result={'status':'PASS','actual_disturbed_retention_source_supply_rate_lower':power,
      'retention_source_supplied_work_lower':power*q('retention_duration_after_settling'),
      'complete_program_absolute_source_supply_upper':q('source_absolute_supply_integral_bound'),
      'ideal_equilibrium_supply_lower':q('source_steady_pattern_supply_lower'),
      'actuator_tracking_error_after_settling':dhold,
      'extra_offline_exponential_enclosures':1,'extra_offline_exponential_cost':cost,
      'scope':'all declared source/initial/error family during the requested final retention interval; physical watts/joules require the warranted port power calibration',
      'device_energy':'add actual driver, reader, processor, preparation and calibration costs under THEOREM equation 29; no unmeasured electrical-energy number is claimed'}
    save(ROOT/'results/POWER_CERTIFICATE.json',result)
    print('Continuous disturbed-retention supply rate >=',float(power))


if __name__=='__main__':main()
