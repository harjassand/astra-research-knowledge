"""Run pinned upstream PiezoD for a DC rocker readout with explicit costs.

No downloaded physics is modified. Only the namespace loader bypasses unused
implant tables and installed-package metadata. The primary model is not a
complete thermomechanical simulation of the proposed compound material.
"""
from pathlib import Path
import hashlib
import json
import os
import sys
import types
import math

HERE=Path(__file__).resolve().parent
OUT=HERE/'results';OUT.mkdir(exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR',str(OUT/'mpl-cache'))
os.environ.setdefault('MPLBACKEND','Agg')
SOURCE=HERE.parent/'materials_constraints'/'public_code'/'PiezoD'
prov=json.loads((SOURCE/'PROVENANCE.json').read_text())
for item in prov['files']:
    p=SOURCE/item['path'].replace('README.md','README.txt')
    data=p.read_bytes()
    digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert digest==item['git_blob_sha1']
src=SOURCE/'python'/'src'/'piezod'
for name,path in [('piezod',src),('piezod.optimization',src/'optimization')]:
    module=types.ModuleType(name);module.__path__=[str(path)];sys.modules[name]=module
from piezod.cantilever_epitaxy import CantileverEpitaxy


def run(bias,fmin=1.,fmax=1000.):
    c=CantileverEpitaxy(l=100e-6,w=10e-6,t=1e-6,l_pr_ratio=.3,
                        v_bridge=bias,doping_type='boron',dopant_concentration=4.4e19,
                        t_pr_ratio=.33,freq_min=fmin,freq_max=fmax)
    c.fluid='vacuum'
    delta_temp=c.approxTempRise()[0]
    total=c.integrated_noise()
    mechanical=c.thermo_integrated()
    actuator=c.actuator_noise_integrated()
    electronics=math.sqrt(max(0,total*total-mechanical*mechanical-actuator*actuator))
    sx=electronics/c.displacement_sensitivity()
    k=1.0 # declared stiffness of EACH load-bearing branch, independent of readout
    pivot=c.stiffness();gain=(2*k+pivot)/k
    return dict(bias_V=bias,frequency_band_Hz=[fmin,fmax],
        cantilever_geometry_m=[c.l,c.w,c.t],pivot_stiffness_N_per_m=pivot,
        free_cantilever_resonance_Hz=c.omega_vacuum_hz(),
        sensing_resistor_Joule_power_W=c.power_dissipation(),
        constant_property_peak_temperature_rise_K=delta_temp,
        upstream_electronic_voltage_noise_V=electronics,
        upstream_electronic_displacement_noise_m=sx,
        inferred_rocker_rest_difference_electronic_noise_m=gain*sx,
        ideal_thermal_equilibrium_rest_difference_sd_m=math.sqrt((2*k+pivot)*1.380649e-23*300)/k,
        full_band_rms_is_not_independent_sample_noise=True,
        limitations=['ambient-noise formulas; heating validity must be checked',
                     'free-cantilever resonance/damping not the coupled-rocker resonance/damping',
                     'full-band noise does not establish a static-offset floor or an OU spectrum',
                     'one sensing resistor power only; full bridge, electronics, motor and control omitted',
                     'no fabricated sensor, thermal packaging or mechanical reversal demonstrated'])


if __name__=='__main__':
    result=dict(upstream_commit=prov['commit'],source_files_verified=len(prov['files']),
                cases=[run(.1),run(1.),run(3.),run(1.,.1,100.)])
    (OUT/'finite_readout_cost_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
