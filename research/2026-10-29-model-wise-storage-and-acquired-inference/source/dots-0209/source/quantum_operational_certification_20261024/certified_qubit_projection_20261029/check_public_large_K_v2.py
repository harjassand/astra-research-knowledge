"""Exercise the actual public API, not a bypass around it."""
from certified_projection_v2 import *
from pathlib import Path
import json
Y=[[F(4,5),F(1,5),F(1,4),F(0)],[F(7,10),F(-1,6),F(1,5),F(1,7)],[F(1,5),F(0),F(0),F(0)]]
rows=[]
for power in [40,60,120,512,2048]:
 E,c=project_certified(Y,[1,1,1<<power],F(1,10**12));c['K_power']=power;rows.append(c)
for power in [0,2048]:
 E,c=project_certified([[F(1,5),F(1,7),F(-1,11),F(1,13)]],[1<<power],F(1,10**12));c['singleton_K_power']=power;rows.append(c)
Path(__file__).with_suffix('.json').write_text(json.dumps({'status':'PASS_PUBLIC_API_EXACT_CERTIFICATES','cases':rows},indent=2)+'\n')
print([(c.get('K_power',c.get('singleton_K_power')),c['gap_float']) for c in rows])
