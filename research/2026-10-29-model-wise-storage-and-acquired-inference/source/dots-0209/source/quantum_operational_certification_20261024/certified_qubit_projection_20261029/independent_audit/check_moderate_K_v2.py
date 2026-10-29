from pathlib import Path
import sys,json,time
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P))
from certified_projection_v2 import *
rows=[]
Y=[[F(4,5),F(1,5),F(1,4),F(0)],[F(7,10),F(-1,6),F(1,5),F(1,7)],[F(1,5),F(0),F(0),F(0)]]
for power in [10,20,30,39]:
 start=time.time()
 try:
  E,c=project_certified(Y,[1,1,1<<power],F(1,10**12));row={'K_power':power,'status':'certified','gap':c['gap_float'],'iterations':c['iterations']}
 except RuntimeError as ex:row={'K_power':power,'status':'failed_closed','reason':str(ex)}
 row['seconds']=time.time()-start;rows.append(row)
Path(__file__).with_suffix('.json').write_text(json.dumps(rows,indent=2)+'\n');print(rows)
