#!/usr/bin/env python3
"""Finite ADC resource receipt; does not materialize the raw record."""
import json, math
from pathlib import Path
P=Path(__file__).resolve().parent
d=json.loads((P/'physical_bridge_results.json').read_text())
a=d['acquisition'];c=d['finite_control']
n=a['force_bins_per_half_window'];w=a['half_bin_width']
nf=a['force_average_count'];nx=a['position_average_count']
alpha=1e-6
force_sd=a['sigma_force']/math.sqrt(w/n)
position_sd=a['sigma_position']/math.sqrt(w)
force_required=c['hold_force_bound']+force_sd*math.sqrt(2*math.log(4*nf/alpha))
position_required=d['amplitude']+c['tracking_allowance']+position_sd*math.sqrt(2*math.log(4*nx/alpha))
force_range,position_range=4,1
force_bits,position_bits=30,38
fq=2*force_range/(2**force_bits)
xq=2*position_range/(2**position_bits)
assert force_range>=force_required and position_range>=position_required
assert fq/2+5e-9<=1e-8 and xq/2+5e-12<=1e-11
out={'extra_overflow_failure_budget':alpha,
 'joint_valid_output_probability_lower_bound':1-.005-.005-alpha,
 'force_ADC':{'range_plus_minus':force_range,'bits':force_bits,
  'quantization_step':fq,'separate_calibration_error_budget':5e-9,
  'required_range_by_union_bound':force_required,'raw_bin_duration':w/n},
 'position_ADC':{'range_plus_minus':position_range,'bits':position_bits,
  'quantization_step':xq,'separate_calibration_error_budget':5e-12,
  'required_range_by_union_bound':position_required},
 'raw_record_bits_if_all_saved':nf*force_bits+nx*position_bits,
 'raw_record_bytes_if_all_saved':math.ceil((nf*force_bits+nx*position_bits)/8),
 'raw_records_materialized':False,
 'overrange_action':'emit explicit failure flag; do not issue an unqualified fit certificate',
 'scope':'Raw records may be streamed. Calibrated sensor transfer and actuator errors are additional declared bounded premises; no hidden noise-free meter is inferred.'}
(P/'finite_digitization_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
