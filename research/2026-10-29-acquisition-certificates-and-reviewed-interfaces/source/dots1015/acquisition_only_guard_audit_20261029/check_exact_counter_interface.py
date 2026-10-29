from pathlib import Path
import importlib.util,random,json,copy
from fractions import Fraction as F
r=Path('producer-workspace/acquisition_only_quantum_certificate_20261029');sp=importlib.util.spec_from_file_location('cert',r/'exact_data_certificate.py');mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod);rng=random.Random(19)
for _ in range(500):
 v=F(rng.randrange(10**15),rng.randrange(1,10**10));bits=rng.randrange(0,70);u=mod.root_upper(v,bits);assert u*u>=v;assert u==0 or (u-F(1,2**bits))**2<v
T=2**200;J=T//3
edge={'quaternion':['1','0','0','0'],'coefficients':[],'reported_gap_sum':'0','squared_feedback_sum':'0'}
rec={'horizon':T,'service_target':J,'correction_radius':J//256,'services_completed':J,'probe_count':0,'active_calls':J,'probe_probability':'1/3','perturbation_amplitude':2**100,'midpoint_bank_size':2**410,'raw_transfer_factor':8,'failure_budget_exponents':[20,20,20],'edges':[copy.deepcopy(edge) for _ in range(3)],'verified_code':True,'resource_abort':False}
a=mod.certify(rec);assert a['accept'];b=copy.deepcopy(rec);b['resource_abort']=True;assert not mod.certify(b)['accept'];b=copy.deepcopy(rec);b['services_completed']-=1;b['active_calls']-=1;assert not mod.certify(b)['accept']
b=copy.deepcopy(rec);b['edges'][0]['reported_gap_sum']='1';assert F(mod.certify(b)['virtual_bad_count_upper'])>=F(a['virtual_bad_count_upper'])
b=copy.deepcopy(rec);b['edges'][0]['quaternion']=['1','1','0','0']
try:mod.certify(b);raise AssertionError('nonunit accepted')
except ValueError:pass
for mutation in ['alpha','odd_port','impossible_feedback']:
 b=copy.deepcopy(rec)
 if mutation=='alpha':b['raw_transfer_factor']='1'
 elif mutation=='odd_port':b['edges'].pop()
 else:b['edges'][0]['coefficients']=[([4,0,0,0],'1')]
 try:mod.certify(b);raise AssertionError('invalid contract accepted: '+mutation)
 except ValueError:pass
out={'public_transfer_and_feedback_hardening':True,'upper_roots_checked':500,'synthetic_large_counter_accepts':True,'abort_and_shortage_reject':True,'monotone_gap_bound':True,'nonunit_candidate_rejected':True,'scope':'Arithmetic/interface checks on synthetic counters only; no physical provenance, feasible workload or positive-yield evidence.'}
Path(__file__).with_name('counter_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
