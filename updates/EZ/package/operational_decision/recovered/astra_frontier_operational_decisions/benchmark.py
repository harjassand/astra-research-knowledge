"""Fresh finite-device response construction plus sensor/decision checking."""
from __future__ import annotations
import time
START=time.perf_counter()
import json,platform,sys,resource
from pathlib import Path
import numpy,scipy
from finite_certificates import run_case
from decision_certificate import produce
from experiment_compiler import compile_probe

def main(out='results'):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    start=time.perf_counter()
    rows=[run_case(kind,k,6,out) for k in [2,4,8] for kind in ['bad','good']]
    (out/'all_cases.json').write_text(json.dumps(rows,indent=2))
    response_seconds=time.perf_counter()-start
    st=time.perf_counter();compile_probe(out);produce(out);decision_seconds=time.perf_counter()-st
    ledger={'response_discovery_and_rational_verification_seconds':response_seconds,
            'decision_and_information_certificate_seconds':decision_seconds,
            'process_clock_including_imports_seconds':time.perf_counter()-START,
            'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'cases':6,'neutral_operator_dimension':70,'trial_degree':6,
            'polynomial_coefficients_per_case':924,'all_case_trial_complex_scalars':6*924*70,
            'reference_inverse_complex_scalars':6*70*70,
            'python':sys.version,'numpy':numpy.__version__,'scipy':scipy.__version__,
            'platform':platform.platform(),
            'timing_scope':'fresh six coefficient-family solves, rounding, exact response verification, payoff order, POVM, risk and all-adaptive information bounds; includes imports in process clock; excludes prior model/experiment selection, code development, searches and physical characterization',
            'input':'four-site Hamiltonian family, specified action menu and selected probe; no precomputed response coefficients or many-body gaps',
            'lab_experiment_performed':False}
    (out/'resource_ledger.json').write_text(json.dumps(ledger,indent=2))
    print(json.dumps(ledger,indent=2))
if __name__=='__main__':main()
