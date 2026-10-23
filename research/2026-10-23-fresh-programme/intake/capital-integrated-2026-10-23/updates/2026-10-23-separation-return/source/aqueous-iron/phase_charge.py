from fractions import Fraction as F
from pathlib import Path
import json,time,resource
s=time.perf_counter()
xm,xh,xf=F('.340'),F('.648'),F('.012'); eta=F('.76')
assert xm+xh+xf==1
red=xm/3+xh+3*xf
# Independent valence calculation.
val=xm*F(8,3)+xh*2
assert red==3-val
q=red/eta
metal=3*xf/q
out={'source_table_1_assumed_total_Fe_fractions':[str(xm),str(xh),str(xf)],'reduction_electrons_per_initial_Fe':float(red),'source_inferred_total_electrons_per_initial_Fe':float(q),'conditional_metal_only_charge_efficiency':float(metal),'exact_metal_only_charge_efficiency':str(metal),'fraction_reduction_charge_in_final_metal':float(3*xf/red),'remaining_reduction_electrons_per_initial_Fe_for_all_metal':float(3-red),'remaining_fraction_of_full_reduction_charge':float((3-red)/3),'interpretation':'Reported 76% mixture-reduction efficiency is not metal-production efficiency. Conditional reconstruction, not raw current integration or absolute recovered product assay. No cell energy claim. Amorphous inventory and phase quantification uncertainty unresolved.','checks':'two exact independent valence and reaction-count expressions agree','seconds':time.perf_counter()-s,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
Path(__file__).with_name('phase_charge_result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
