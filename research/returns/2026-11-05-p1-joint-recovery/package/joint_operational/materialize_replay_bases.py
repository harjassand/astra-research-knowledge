"""Anchor saved multiplicity coefficients to explicit physical Kraus bases."""
import json
from pathlib import Path
import numpy as np
import scipy.linalg as la
from spin_gauge_control import setup
from rotor_control import rotor_setup
from cascade_control import cascade_setup

root=Path(__file__).resolve().parent
manifest=json.loads((root/'numerical_summary.json').read_text());checks=[]
for run in manifest['runs']:
 path=Path(run['policy_path']);path=path if path.is_absolute() else root/path
 metadata=Path(run['metadata_path']);metadata=metadata if metadata.is_absolute() else root/metadata
 meta=json.loads(metadata.read_text())
 with np.load(path) as z:data={k:z[k] for k in z.files}
 data['source_theta']=np.array(meta['theta']);data['memory_dimension']=np.array(meta['m']);data['initial_joint_state']=data['states'][0]
 if 'policy_block_0' in data:
  if path.name.startswith('gauge_'):
   model,chan,dec,_=setup(meta['j'],meta['theta'],all_env=meta.get('all_env',False),gauge_state=meta.get('gauge_state','tracial'),gauge_seed=meta.get('gauge_seed',123))
  elif path.name.startswith('cascade_'):
   model,chan,dec,_=cascade_setup(meta['k'],meta['theta'],meta['initial'],'CLARABEL',1e-8)
  elif path.name.startswith('rotor_'):
   model,chan,dec,_=rotor_setup(meta['cutoff'],meta['theta'],meta['initial'])
  else:raise ValueError(path.name)
  for k,b in enumerate(chan.bases):data['channel_base_'+str(k)]=b
  if hasattr(dec,'bases'):
   for k,b in enumerate(dec.bases):data['decoder_base_'+str(k)]=b
  residual=0.;n=len(data['states'])-1
  for j in sorted(set([0,min(3,n-1),n-1])):
   coeff=[data['policy_block_'+str(k)][j] for k in range(len(chan.blocks))]
   out=chan.apply(model.source(data['states'][j]),coeff)
   residual=max(residual,float(la.norm(out-data['states'][j+1])))
  if residual>1e-8:raise RuntimeError('Basis mismatch '+path.name+' '+str(residual))
  checks.append(dict(file=path.name,physical_basis_stage_residual=residual))
 np.savez_compressed(path,**data)
(root/'replay_basis_checks.json').write_text(json.dumps(checks,indent=2))
print('Anchored',len(checks),'representation policies; maximum checked state residual',max(x['physical_basis_stage_residual'] for x in checks))
