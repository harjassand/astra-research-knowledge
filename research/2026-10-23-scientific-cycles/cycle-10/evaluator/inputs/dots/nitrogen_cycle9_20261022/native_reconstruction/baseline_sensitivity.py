from pathlib import Path
import csv,json
from fractions import Fraction as F
p=Path(__file__).parent;src=p.parent/'nitrite_finishing/dataset/Figure_4.csv';rows=list(csv.reader(src.open()))
out=[]
for j in [0,2,4]:
 vals={F(r[j]):F(r[j+1]) for r in rows[1:] if len(r)>j+1 and r[j] and r[j+1]}
 y0=vals[F(0)];yf=vals[F(2700)];increment=(yf-y0)/1000
 out.append({'label':rows[0][j+1],'first_record_mM':float(y0),'value_2700s_mM':float(yf),'first_record_subtracted_increment_per_1M_initial_nitrite':float(increment),'min_external_acceptor_e_per_initial_N_if_other_N_ge_minus3':float(max(F(0),8*increment-6))})
r={'scope':'Stress test, not assertion that first sample is chemical background. Initial transient/calibration needs source interpretation; do not silently discard or treat as physical imported nitrate.','rows':out,'air_over_N2_increment_ratio':out[0]['first_record_subtracted_increment_per_1M_initial_nitrite']/out[2]['first_record_subtracted_increment_per_1M_initial_nitrite']}
(p/'baseline_sensitivity.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
