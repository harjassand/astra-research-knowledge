import sys,json
sys.dont_write_bytecode=True
import numpy as np
from pathlib import Path
raw=json.loads((Path(__file__).parent/'all_free.json').read_text());groups={}
for m,c in raw:
 key=(m[0]+m[1],m[2]+m[3],m[4]+m[5])
 if min(key)==0:continue
 groups.setdefault(key,[]).append((m,float(c)))
rng=np.random.default_rng(18);ang=rng.uniform(0,2*np.pi,size=(3,3000));vals=np.array([np.cos(ang[0]),np.sin(ang[0]),np.cos(ang[1]),np.sin(ang[1]),np.cos(ang[2]),np.sin(ang[2])])
for key,terms in groups.items():
 pp=sum(c*np.prod(vals**np.array(m)[:,None],axis=0) for m,c in terms);ii=pp.argmin()
 print(key,'min',pp[ii], 'directions',vals[:,ii].tolist(),flush=True)
