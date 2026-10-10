#!/usr/bin/env python3
"""Seven scoped diagnostics in a disposable copy; no source checkout or network.

Requires Python 3, numpy and mpmath. This does not validate the general proofs,
historical priority, laboratory feasibility, or foundational significance.
The slow raw-data fits/forecasts retain separate reproduction commands in
reports/s45_realization.txt and are not silently counted as replayed here.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time

CASES = [
    ('exact_closure', 's43_proof/check_exact.py'),
    ('exact_node_census', 'root_nonlinear_tomography/node_census.py'),
    ('ambient_rank', 'root_nonlinear_tomography/rank_test.py'),
    ('supplied_kernel_conditioning', 's41_primitive/check_recovery.py'),
    ('supplied_kernel_residues', 's41_primitive/check_residue_recovery.py'),
    ('independent_interpolation', 's46_adversary/independent_checks.py'),
    ('simulated_phase_interface', 'h09_gate/phase_cycle_check.py'),
]

def check_result(name, result):
    if name == 'exact_closure':
        assert len(result) == 11
        return {'exact_cases': len(result), 'scope': 'polynomial identities and selected rational examples'}
    if name == 'exact_node_census':
        assert result['status'] == 'EXACT_SCOPED_ALGEBRA_CHECK_PASS'
        assert len(result['rows']) == 6
        return {'exact_cases': 6, 'largest_hidden_count': 1000, 'physical_acquisition': False}
    if name == 'ambient_rank':
        assert [r['rank_mod_prime'] for r in result] == [5,15,35,69,121]
        return {'finite_field_ranks': [5,15,35,69,121], 'universal_rank_proof': False}
    if name == 'supplied_kernel_conditioning':
        rows = result['conditioning']
        a = next(r for r in rows if r['n']==8 and not r['oscillator'])
        b = next(r for r in rows if r['n']==8 and r['oscillator'])
        assert a['condV'] > 1e10 and b['exact_B_K_error'] < 1e-7
        return {'first_order_n8_condition': a['condV'],
                'oscillator_n8_supplied_B_K_error': b['exact_B_K_error'], 'acquired_H1_H3': False}
    if name == 'supplied_kernel_residues':
        good = next(r for r in result['moderate_damping'] if r['n']==8 and r['gamma']==.03)
        assert good['K_error'] < 1e-7
        assert all(r['maximum_input_frequency'] <= 3.1 for r in result['reconstructions'])
        return {'n8_gamma_003_K_error': good['K_error'], 'acquired_H1_H3': False}
    if name == 'independent_interpolation':
        p = result['paired_first_order']
        assert p['finite_interpolation_relative_error'] < 1e-60
        assert all(r['close_pair_grid_min_singular'] >= .16 for r in result['oscillator_pole_clusters'])
        return {'mpmath_interpolation_error': p['finite_interpolation_relative_error'],
                'physical_measurements': False}
    if name == 'simulated_phase_interface':
        err = result['richardson_rho_0.05_0.10']['relative_error']
        assert err < 1e-4
        assert result['results'][-1]['relative_error'] < result['results'][0]['relative_error']/8
        return {'RK4_Richardson_relative_error': err, 'sensor_noise_tested': False}
    raise ValueError(name)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt',type=Path,help='Optional receipt destination; otherwise stdout only')
    args=parser.parse_args()
    import numpy
    import mpmath
    base=Path(__file__).resolve().parent
    result={'status':'RUNNING','scope_disclosure':__doc__.strip(),
            'python':sys.version,'platform':platform.platform(),
            'numpy':numpy.__version__,'mpmath':mpmath.__version__,'checks':[]}
    environment=os.environ.copy()
    environment.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    started=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='astra04-replay-') as temporary:
        root=Path(temporary)
        shutil.copytree(base/'reports',root/'reports',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        for name,relative in CASES:
            script=root/'reports'/relative
            t=time.monotonic()
            proc=subprocess.run([sys.executable,str(script)],cwd=root,env=environment,
                                text=True,capture_output=True,timeout=300)
            if proc.returncode:
                raise RuntimeError(f'{name} failed: {proc.stderr[-6000:]}\n{proc.stdout[-3000:]}')
            parsed=json.loads(proc.stdout)
            evidence=check_result(name,parsed)
            result['checks'].append({'name':name,'script':'reports/'+relative,'status':'PASS',
                                    'seconds':time.monotonic()-t,
                                    'source_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),
                                    'stdout_sha256':hashlib.sha256(proc.stdout.encode()).hexdigest(),
                                    'evidence':evidence})
            print(f'{name}: PASS',file=sys.stderr,flush=True)
    result['status']='SEVEN_SCOPED_DIAGNOSTICS_PASS'
    result['seconds']=time.monotonic()-started
    serialized=json.dumps(result,indent=2)+'\n'
    if args.receipt:
        args.receipt.parent.mkdir(parents=True,exist_ok=True)
        args.receipt.write_text(serialized)
    print(serialized)

if __name__=='__main__':
    main()
