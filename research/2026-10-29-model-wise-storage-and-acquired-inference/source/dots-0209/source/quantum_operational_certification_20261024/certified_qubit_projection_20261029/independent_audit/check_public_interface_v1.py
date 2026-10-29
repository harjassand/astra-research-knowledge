from pathlib import Path
from fractions import Fraction as F
import sys,runpy,json
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P))
from certified_projection_v2 import project_certified
ns=runpy.run_path(str(Path(__file__).with_name('check_exact_v1.py')));validate=ns['validate']
rows=[]
def case(name,Y,mult):
 try:
  E,c=project_certified(Y,mult,F(1,10**12));g=validate(c);assert g<=F(1,10**12)
  rows.append({'name':name,'outcome':'certified','gap':str(g),'gap_float':float(g),'certificate':c})
 except RuntimeError as ex:rows.append({'name':name,'outcome':'failed_closed','reason':str(ex)})
for power in [40,60,120,512,2048]:
 case('overloaded_'+str(power),[[F(4,5),F(1,5),F(1,4),F(0)],[F(7,10),F(-1,6),F(1,5),F(1,7)],[F(1,5),F(0),F(0),F(0)]],[1,1,1<<power])
case('singleton_indefinite',[[F(-3),F(1,3),F(-2),F(7)]],[1<<2048])
case('underloaded_boundary',[[F(1,10),F(0),F(0),F(0)],[F(4,5),F(0),F(0),F(0)]],[1,1<<2048])
case('rank_one_boundary',[[F(1,4),F(1,4),F(0),F(0)],[F(3,4),F(-1,4),F(0),F(0)]],[1,1<<2048])
Path(__file__).with_suffix('.json').write_text(json.dumps(rows,indent=2)+'\n')
print([(r['name'],r['outcome'],r.get('gap_float')) for r in rows])
