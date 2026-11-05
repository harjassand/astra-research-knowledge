"""Replay the complete minimum-19 proof without invoking an optimizer."""
from pathlib import Path
from fractions import Fraction
import json,subprocess,sys,tempfile,shutil,time
root=Path(__file__).resolve().parent
started=time.perf_counter()
def run(script,*args):
 result=subprocess.run([sys.executable,str(script),*map(str,args)],cwd=root,capture_output=True,text=True)
 if result.returncode:
  print(result.stdout);print(result.stderr,file=sys.stderr);raise SystemExit(result.returncode)
 return result.stdout
run(root/'audit_independent'/'check_certificates.py')
records=json.loads((root/'exact_lp_certificates.json').read_text())
assert {x['n']for x in records if Fraction(x['upper_a0'])<1}==set(range(9,18))
print('PASS: exact lower-bound certificates for n=9,...,17; Singleton excludes n<9.')
run(root/'audit_positive19'/'replay_certificate.py')
print('PASS: exact algebraic 19-qubit code, all 50 reduced KL identities, and distance exactly five.')
with tempfile.TemporaryDirectory(prefix='_proof_replay_',dir=root)as tmp:
 tmp=Path(tmp);checker=tmp/'verify_interval_dual.py'
 shutil.copy2(root/'audit_residual'/'verify_interval_dual.py',checker)
 run(checker,root/'audit_residual'/'dual_witness_corrected.json')
 receipt=json.loads((tmp/'interval_certificate.json').read_text())
 margin=Fraction(receipt['strict_contradiction_margin_lower_exact'])
 assert receipt['status']=='CERTIFIED EXCLUSION' and margin>Fraction(690847,10**10)
 print(f'PASS: n=18 excluded with exact certified margin greater than 690847/10^10 ({float(margin):.15g}).')
print(f'PASS: minimum length is exactly 19 under the fully symmetric rank-two distance-at-least-five definition. Replay seconds: {time.perf_counter()-started:.3f}.')
