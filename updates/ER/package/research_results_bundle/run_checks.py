"""Run the included finite checks; this does not validate the general theorems."""
from pathlib import Path
import subprocess, sys, time
root=Path(__file__).resolve().parent
logs=root/'check_outputs';logs.mkdir(exist_ok=True)
scripts=[
'controlled_noise/weighted_basis_peeling_check.py',
'controlled_noise/boolean_polynomial_xor_checks.py',
'controlled_noise/repeated_control_checks.py',
 'transport_continuation_cost/check_paid_bounds.py',
 'transport_continuation_cost/check_restart_response.py',
 'transport_projection_locality/check_projection_obstruction.py',
 'nonlocal_transport_compression/check_infinite_degree_coupling.py',
 'nonlocal_transport_compression/test_degree_ladder.py',
 'transport_excursion_resummation/check_excursion_reset.py',
 'front_scaling/calculate.py',
 'replica_recombination/check_recombination.py']
failed=[]
for rel in scripts:
    start=time.monotonic()
    p=subprocess.run([sys.executable,str(root/rel)],cwd=root,capture_output=True,text=True)
    msg=p.stdout + ('\nSTDERR\n'+p.stderr if p.stderr else '')
    (logs/(Path(rel).stem+'.txt')).write_text(msg)
    print(f'{rel}: exit {p.returncode}, {time.monotonic()-start:.2f} seconds',flush=True)
    if p.returncode: failed.append(rel)
if failed: raise SystemExit('Failed: '+', '.join(failed))
print('All included finite checks completed. They are not an end-to-end implementation or independent proof audit.')
