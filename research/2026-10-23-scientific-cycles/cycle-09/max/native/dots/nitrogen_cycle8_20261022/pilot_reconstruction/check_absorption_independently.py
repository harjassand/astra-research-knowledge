"""Principal-owner independent 60-digit quadrature, original extent variable.
Does not import the serial-bound solver or run its finite-stage calculation.
"""
import mpmath as m,json,time,resource,hashlib
from pathlib import Path
start=time.perf_counter();m.mp.dps=60;p=Path(__file__).parent;root=p.parent
raw=(root/'absorption_bound/inputs/input.json').read_bytes();i=json.loads(raw);r=json.loads((root/'absorption_bound/result.json').read_text())
assert hashlib.sha256(raw).hexdigest()=='75de794a26ecaac2e8c4c938249bea1af08fa4fa7e563407962e9ecb58f10a34'
M=m.mpf;f=M(i['standard_flow_L_min'])/M(i['declared_standard_molar_volume_L_mol'])/60
k=M(i['event_k_cm6_molecule2_s'])*M(i['Avogadro'])**2/M('1e12');c=M(i['pressure_Pa'])/(M(i['R_J_mol_K'])*M(i['T_K']))
results=[]
for row in r['rows']:
 ip=next(x for x in i['points'] if x['configuration']==row['configuration']);a=M(ip['initial_NO_fraction']);b=M('.21')-a/2
 Y=M('.99') if row['target']=='99_percent_capture' else (a-M('.0001'))/(a*(1-M('1.75')*M('.0001')))
 E=M('1.5')*a*Y;g=E/3
 def serial(e):return (1-M(7)*e/6)**3/((a-M(2)*e/3)**2*(b-e/2))
 def recycle(e):return (1+g-e/2)**3/((a+g-e)**2*(b-e/2))
 pts=[M(0),E/2,E*M('.9'),E*M('.99'),E]
 v=f/(2*k*c**3)*m.quad(serial,pts)*1000
 vr=f/(2*k*c**3)*m.quad(recycle,pts)*1000
 assert abs(v-M(str(row['ideal_lower_bound_reaction_volume_L'])))/v<M('1e-10')
 assert abs(vr-M(str(row['selective_regenerated_NO_recycle_monomer_reaction_volume_L'])))/vr<M('1e-10')
 assert vr<v
 # Exact algebraic pointwise bounds checked on rational-looking mp states; the proof is symbolic, not this grid.
 for frac in [M('.1'),M('.5'),M('.99')]:
  e=E*frac
  for fraction_s in [M(0),M('.4'),M(1)]:
   s=e*fraction_s
   for fraction_d in [M(0),M('.7'),M(1)]:
    d=(e-s)/2*fraction_d
    t=1-e/2-M(2)*s/3-d;tstar=1-M(7)*e/6
    n=a-e+s/3;nstar=a-M(2)*e/3
    assert t+M('1e-55')>=tstar and n<=nstar+M('1e-55')
    assert n/t<=nstar/tstar+M('1e-55')
 results.append({'configuration':row['configuration'],'target':row['target'],'serial_L':str(v),'selective_recycle_L':str(vr),'same_product_tail':True,'native_agreement_relative_tolerance':'1e-10'})
out={'scope':'Independent numerical corroboration, not physical validation or universal train optimum','input_sha256':hashlib.sha256(raw).hexdigest(),'rows':results,'elapsed_s':time.perf_counter()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(p/'independent_absorption_result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
