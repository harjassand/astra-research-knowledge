import sys
sys.set_int_max_str_digits(0)
from pathlib import Path
import runpy,numpy as np,json,hashlib,sys
P=Path('morrey_law_first_stress_20261026/cube_brownian_completion').resolve();O=P/'fully_corrective141_half_K48';sys.path.insert(0,str(P));files=list(O.glob('*.json'))+list(O.glob('*.npy'))+list(O.glob('*.npz'));hs={p:hashlib.sha256(p.read_bytes()).hexdigest()for p in files};sv=np.save;sz=np.savez_compressed;wr=Path.write_text;seen=[]
def save(p,a,*args,**kw):assert Path(p).parent==O and np.array_equal(np.load(p),a);seen.append(Path(p).name)
def savez(p,*args,**kw):
 assert Path(p).parent==O and not args
 with np.load(p)as z:
  assert set(z.files)==set(kw)
  for k,v in kw.items():assert np.array_equal(z[k],v),k
 seen.append(Path(p).name)
def write(p,data,*args,**kw):
 assert p.parent==O;old=json.loads(p.read_text());new=json.loads(data);assert old.keys()==new.keys()
 for k in old:
  if k!='seconds':assert old[k]==new[k],k
 seen.append(p.name);return len(data)
np.save=save;np.savez_compressed=savez;Path.write_text=write
try:
 runpy.run_path(str(P/'receive_corrective141_half_root_proxy.py'),run_name='__main__')
 runpy.run_path(str(P/'receive_corrective141_half_arithmetic_plan.py'),run_name='__main__')
 runpy.run_path(str(P/'receive_corrective141_half_full_Gram.py'),run_name='__main__')

finally:np.save=sv;np.savez_compressed=sz;Path.write_text=wr
assert all(hashlib.sha256(p.read_bytes()).hexdigest()==h for p,h in hs.items());print('NONMUTATING CORRECTIVE122 EXPORT/FULL-GRAM CANDIDATE REPLAY PASS',seen)
