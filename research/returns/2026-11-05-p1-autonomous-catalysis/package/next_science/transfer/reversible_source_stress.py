"""Stress test rapid reversible adsorption, distinct from strong binding.
This is a synthetic model comparison, not parameters inferred from Liang.
"""
from pathlib import Path
import json
import catalytic_reversible_source as model
from catalytic_poisson_audit import thermal_certificate,comparator_change


def main():
    states=['0','0','-0.1','-0.1','-0.1','0']
    out=[]
    for mode in ('modulate','consume'):
        for ads in ('1e4','1e8'):
            a=model.solve_case(mode=mode,capture='0',fast='100',
                  energies=states,adsorption=ads,internal=True)
            b=model.solve_case(mode=mode,capture='1',fast='100',
                  energies=states,adsorption=ads,internal=True)
            result={'mode':mode,'adsorption_rate_s':float(ads),
                    'capture_off':a['output'],'capture_on':b['output'],
                    'comparison':comparator_change(a,b),
                    'thermal_certificate':thermal_certificate(b)}
            J=b['output']['net_adsorptions_pair_per_s']
            result['gross_ads_per_net_turnover']=b['output']['gross_adsorptions_pair_per_s']/J
            out.append(result)
            print(json.dumps({'mode':mode,'ads':ads,'gross/net':result['gross_ads_per_net_turnover'],
                 'J0':result['comparison']['J0'],'J1':result['comparison']['J1'],
                 'capture_flux':b['output']['net_mode_capture_pair_per_s'],
                 'thermalJ':result['thermal_certificate']['Jth'],
                 'bound':result['thermal_certificate']['gain_bound_max']}),flush=True)
    Path(__file__).with_name('reversible_source_stress_results.json').write_text(json.dumps(out,indent=2))

if __name__=='__main__':main()
