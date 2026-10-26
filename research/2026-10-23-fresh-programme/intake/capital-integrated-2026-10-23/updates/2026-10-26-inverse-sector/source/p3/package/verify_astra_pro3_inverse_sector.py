"""Replay Astra Pro3 inverse-sector programmes independently and check byte hashes."""
from pathlib import Path
import tempfile,subprocess,shutil,hashlib,sys,os,json
ROOT=Path(__file__).resolve().parent
NAMES=[
 ('astra_pro3_sector_joint.py','astra_pro3_sector_joint_results.json'),
 ('astra_pro3_sparse_inverse_certificate.py','astra_pro3_sparse_inverse_certificate_results.json'),
 ('astra_pro3_sector_saturation.py','astra_pro3_sector_saturation_results.json'),
 ('astra_pro3_sector_constrained_vi.py','astra_pro3_sector_constrained_vi_results.json'),
]

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
 with tempfile.TemporaryDirectory(prefix='astra_sector_clean_') as t:
  t=Path(t)
  for source,result in NAMES:shutil.copy2(ROOT/source,t/source)
  out={}
  for script,result in NAMES:
   subprocess.run([sys.executable,str(t/script)],cwd=t,check=True,timeout=35,
                 stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,
                 env={**os.environ,'OPENBLAS_NUM_THREADS':'1'})
   assert sha(t/result)==sha(ROOT/result),(script,result)
   out[result]=sha(ROOT/result)
  print(json.dumps({'all_passed':True,'exact_result_sha256':out},indent=2))
if __name__=='__main__':main()
