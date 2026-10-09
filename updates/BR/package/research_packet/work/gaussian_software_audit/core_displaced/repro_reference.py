from pathlib import Path
import sys,json,hashlib,random
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'gaussian_transfer'))
from displaced_sampler import ParityEnvelope
from flint import ctx
rows=[]
for h in [100,10**10,10**20]:
 law=ParityEnvelope(F(0),F(1),F(1),h,F(1,1000))
 with ctx.workprec(1024):
  exactish=law._logweight_narrow(law.reference_k,100)
  gap=law.reference-exactish
  rows.append({'h':str(h),'reference_gap':str(gap),'reference_mass':str((exactish-law.reference).exp()),'reference_k':str(law.reference_k),'bounds':list(law.bounds(law.reference_k)),'grid_bits':law.bits})
 result=law.draw(random.Random(1))
 rows[-1].update({'output':str(result),'used_fallback':law.used_fallback,'attempts':law.last_attempts})
path=Path(__file__).resolve().parents[2]/'gaussian_transfer/displaced_sampler.py'
out={'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'cases':rows}
print(json.dumps(out,indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
