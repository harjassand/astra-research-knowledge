"""Reproduce the diagnostics in the documented dependency environment."""
import os,pathlib,subprocess,sys
root=pathlib.Path(__file__).resolve().parent
env=os.environ.copy();env['OPENBLAS_NUM_THREADS']='1';env['OMP_NUM_THREADS']='1'
for script in ('verify.py','verify_anchored.py','verify_star.py','verify_residual.py','make_figure.py'):
    subprocess.run([sys.executable,str(root/script)],cwd=root,env=env,check=True)
