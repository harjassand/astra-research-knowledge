"""Private final source/result binding; not a scientific audit substitute."""
from pathlib import Path
import ast,hashlib,json,platform


def main():
    root=Path(__file__).parent;manifest=[]
    for p in sorted(root.rglob('*')):
        if not p.is_file() or p.name=='FINAL_RECEIPT.json' or '__pycache__' in p.parts:continue
        raw=p.read_bytes()
        if p.suffix=='.py':ast.parse(raw,filename=str(p))
        manifest.append({'path':str(p.relative_to(root)),'bytes':len(raw),
                         'sha256':hashlib.sha256(raw).hexdigest()})
    d=json.loads((root/'ENERGY_EXECUTION.json').read_text())
    c=json.loads((root/'ENERGY_CERTIFICATE.json').read_text())
    f=json.loads((root/'ORDINARY_FIT.json').read_text())
    out={'status':'CONSTRUCTED_CONDITIONAL_FINITE_PULSE_ENERGY_OPERATION',
         'new_energy_theorem_independent_whole_review':'PENDING',
         'all_size_scope':'connected n>=2, real symmetric known-metric network; cyclic qualified linear port; globally switchable known onsite Kerr; coherent complex port',
         'whole_analytic_family_injectivity':True,
         'finite_design':'generic paired two-radius existence; measured conditioning still mandatory',
         'uniform_noisy_or_physical_identification':'NOT_ACQUIRED',
         'n1_isolated_vertices':'ambient energy identification exception explicitly retained',
         'actual_experiments':d['experiments'],'raw_complex_records':d['scalar_complex_snapshots'],
         'normalised_protocol_time':d['total_normalized_control_readout_pulse_time'],
         'actual_K_error':d['reconstruction']['K_frobenius'],
         'finite_DATA_tensor_error_upper':c['tensor_error_certified_upper_from_actual_source_contract'],
         'new_acquisition_seconds':d['acquisition_seconds'],
         'new_inverse_seconds':d['linear_tensor_solve_seconds'],
         'ordinary_training_experiments':12,
         'ordinary_K_errors':[r['reconstruction']['K_frobenius'] for r in f['rows']],
         'ordinary_initial_and_same_data_serialization_replay_both_retained':True,
         'ordinary_fit_replay_seconds':f['seconds_total'],
         'ordinary_wins_model_acquisition_accuracy_discriminator':True,
         'practical_advantage_or_historical_novelty':'UNKNOWN',
         'apparatus_or_actual_source_qualification':'NOT_PERFORMED',
         'bootstrap_zero_calibration':'idealized in prototype; later coherent reset does not pay it',
         'ODE_accuracy':'not validated; finite stored source energy defects separately bounded',
         'root_pulse_package_whole_review':'ACCEPTED at corrected mathematical/model scope; see ROOT_REVIEW.md',
         'frozen_kinetic_package':'unchanged, no rerun; current evidence does not displace it',
         'runtime_python':platform.python_version(),
         'manifest':manifest,'file_count':len(manifest),
         'total_bytes':sum(x['bytes'] for x in manifest)}
    (root/'FINAL_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('manifest','finite_DATA_tensor_error_upper')},indent=2))


if __name__=='__main__':main()
