"""Run exact upstream epitaxy formulas without importing unused implant tables.

The downloaded upstream source files remain unchanged. Namespace package loading
selects the epitaxy, elasticity and noise modules, avoiding unrelated optional
h5py/data and installed-distribution metadata requirements. No stub changes the
sensor physics. These are model predictions, not experimental validation.
"""
from pathlib import Path
import hashlib
import json
import os
import sys
import types

here=Path(__file__).resolve().parent
os.environ.setdefault('MPLBACKEND', 'Agg')
os.environ.setdefault('MPLCONFIGDIR', str(here/'mpl_cache'))
root=here/'public_code'/'PiezoD'
src=root/'python'/'src'/'piezod'
provenance=json.loads((root/'PROVENANCE.json').read_text())
for f in provenance['files']:
    p=root/f['path'].replace('README.md','README.txt')
    data=p.read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert blob==f['git_blob_sha1'], (p,blob,f['git_blob_sha1'])

for name, path in [('piezod',src),('piezod.optimization',src/'optimization')]:
    mod=types.ModuleType(name)
    mod.__path__=[str(path)]
    sys.modules[name]=mod

from piezod.cantilever_epitaxy import CantileverEpitaxy

def run_case(name, **kwargs):
    c=CantileverEpitaxy(**kwargs)
    c.fluid='vacuum'
    vals=dict(name=name,parameters=kwargs,
        stiffness_N_per_m=c.stiffness(),
        frequency_Hz=c.omega_vacuum_hz(),
        resistance_ohm=c.resistance(),
        sensing_resistor_Joule_power_W=c.power_dissipation(),
        nominal_number_of_piezoresistors=c.number_of_piezoresistors,
        nominal_amplifier=c.amplifier,
        force_sensitivity_V_per_N=c.force_sensitivity(),
        total_force_noise_rms_N=c.force_resolution(),
        displacement_noise_rms_m=c.displacement_resolution(),
        piezoresistor_temperature_K=c.piezoresistor_temp(),
        thermal_modeling_flag=c.thermal_modeling,
        constant_property_estimated_peak_temperature_rise_K=c.approxTempRise()[0],
        constant_property_estimated_mean_resistor_temperature_K=c.approxPRTemp())
    return {k:float(v) if isinstance(v,(float,int)) else v for k,v in vals.items()}

result=dict(
    upstream_commit=provenance['commit'],
    source_git_blob_verification='All fetched upstream files verified exactly.',
    scope='Unmodified upstream model, finite stated bandwidth, no new optimization or measured device claim. Noise predictions use upstream default ambient-temperature model; constant-property self-heating estimate separately exposes when that assumption fails. The reported Joule power is ONE sensing resistor, not the full bridge, amplifier, controller, wiring or thermal management.',
    cases=[run_case('nominal_1um_sensor',l=524e-6,w=2e-6,t=1e-6,
                    l_pr_ratio=.29,v_bridge=10,doping_type='boron',
                    dopant_concentration=4.4e19,t_pr_ratio=.33,
                    freq_min=1,freq_max=1000),
           run_case('same_sensor_lower_bias',l=524e-6,w=2e-6,t=1e-6,
                    l_pr_ratio=.29,v_bridge=1,doping_type='boron',
                    dopant_concentration=4.4e19,t_pr_ratio=.33,
                    freq_min=1,freq_max=1000)]
)
(here/'piezod_benchmark_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
