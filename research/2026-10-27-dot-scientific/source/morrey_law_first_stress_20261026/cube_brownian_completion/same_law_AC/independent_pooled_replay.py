from pathlib import Path
import numpy as np,runpy,json,sys
p=Path('/workspace/scratch/57d8dd795b13/morrey_law_first_stress_20261026/cube_brownian_completion');sys.path.insert(0,str(p));old=Path.write_text;oldnp=np.savez_compressed

def write(self,data,*a,**k):
 x=json.loads(data);y=json.loads(self.read_text())
 for z in (x,y):
  for row in z.get('component_mass_checks',[]):row.pop('seconds',None)
 assert x==y,str(self)
 print('MATCH',self.name,flush=True);return len(data)
def save(path,**kw):
 z=np.load(path);assert set(z.files)==set(kw)
 for k,v in kw.items():assert np.array_equal(z[k],v),k
 print('MATCH npz',path,flush=True)
Path.write_text=write;np.savez_compressed=save
try:
 for name in ['scan_pooled_full_product_structure.py','receive_pooled_full_box_capacities.py','receive_pooled_box_flow_packing.py']:
  print('BEGIN',name,flush=True);runpy.run_path(str(p/name),run_name='__main__')
finally:Path.write_text=old;np.savez_compressed=oldnp
