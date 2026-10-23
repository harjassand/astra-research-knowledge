import json
from decimal import Decimal, getcontext
getcontext().prec=35
D=Decimal
r=D('2186.6299335')
out={'diagnostic_collision_ratio':str(r),'five_percent_first_order_gamma':str(D('.05')/r),'one_percent_first_order_gamma':str(D('.01')/r),'avco_alumina_mol_per_m2_s':[str(D(x)*D(10000)) for x in ['6.6e-9','7.0e-9']],'avco_inlet_bed_K':[str((D(x)-32)*D(5)/9+D('273.15')) for x in ['3050','3500']],'is_measured_zirconia_bound':False,'is_trajectory':False}
print(json.dumps(out,indent=2))
