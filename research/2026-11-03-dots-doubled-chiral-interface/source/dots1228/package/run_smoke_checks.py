"""Run small reproducible checks in a temporary, relocatable copy.
Requires Python, NumPy and SciPy. Does not run the astronomical construction.
"""
from pathlib import Path
import os, shutil, subprocess, sys, tempfile

OLD_PREFIX = 'producer-workspace/chiral_hamiltonian_interface_20261102'
CHECKS = [
    'core_phase_rule.py',
    'joint_gap/root_disentangler_cocycle_check.py',
    'joint_gap/root_gaussian_purification_check.py',
    'joint_gap/check_tree_gauss_compiler.py',
]

def main():
    source = Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory(prefix='astra-chiral-checks-') as temp:
        root = Path(temp) / 'research'
        shutil.copytree(source, root, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        for script in root.rglob('*.py'):
            body = script.read_text()
            script.write_text(body.replace(OLD_PREFIX, str(root)))
        env = dict(os.environ, OPENBLAS_NUM_THREADS='2', OMP_NUM_THREADS='2')
        for relative in CHECKS:
            print('\n=== '+relative+' ===', flush=True)
            subprocess.run([sys.executable, str(root / relative)], cwd=root,
                           env=env, check=True, timeout=180)
        print('\nAll selected smoke checks completed. See individual proof qualifications.')

if __name__ == '__main__':
    main()
