from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import sys,json
A=Path(__file__).resolve().parent;sys.path.insert(0,str(A/'replay/matched_energy_clock_constructor_20261101'));import positive_integrals as p;import acquire_derivative as ac
checks=0;details=[]
def ok(a,s):
 global checks
 assert a,s
 checks+=1;details.append(s)

def no(fn,s):
 try:fn()
 except p.Unknown as e:ok(True,s+': '+str(e))
 else:raise AssertionError('false admission '+s)
kw=dict(alpha=4,beta=F(2,3),kappa=F(1),H=F(100),dmin=F(1,7),Nt=4,Ny=4,L=F(0),T=F(8),precision_bits=256)
ref=p.Price(**kw).run();limit=ref['work']['largest_root_operand_bound_bits'];got=p.Price(**kw,max_integer_bits=limit).run();ok(got['P_total_upper']==ref['P_total_upper'],'exact complete root/product integer ceiling admits');no(lambda:p.Price(**kw,max_integer_bits=limit-1).run(),'one below true root precheck ceiling refuses')
got=p.Price(**kw,max_nodes=25).run();ok(got['P_total_upper']==ref['P_total_upper'],'exact25 tensor-node budget admits');no(lambda:p.Price(**kw,max_nodes=24),'one below complete tensor-node budget refuses')
lo,hi=1,128
while lo<hi:
 mid=(lo+hi)//2
 try:p.Price(**kw,max_exp_terms=mid).run()
 except p.Unknown:lo=mid+1
 else:hi=mid
z=p.Price(**kw,max_exp_terms=lo).run();ok(z['P_total_upper']==ref['P_total_upper'],'minimal positive-exp Taylor/scaling budget admits');no(lambda:p.Price(**kw,max_exp_terms=lo-1).run(),'one below actual exp budget refuses')
small=p.Price(4,F(1),F(1),F(1),F(1),Nt=1,Ny=1,L=F(0),T=F(1),precision_bits=32)
ok(small.analytic_J_lower(F(1,1<<100))==0,'underresolved analytic root safely returns only zero lower')
no(lambda:p.Price(4,F(1),F(1),F(1),F(1),Nt=1,Ny=1,L=F(0),T=F(1000),precision_bits=32).run(),'underresolved positive transverse denominator refuses')
fx=p.Intervals(64,1000,1000,100,1)
for pair in [((0,0),(0,1)),((1,2),(0,0))]:no(lambda pair=pair:fx.div(*pair),'division requires strict positive lower')
for iv in [(-1,1),(2,1)]:no(lambda iv=iv:fx.keep(iv),'positive interval storage refuses negative/reversed')
raw=p.old.fixture(16);m=[]
for key,val in [('dimension',True),('dimension',15),('dimension',18),('energy_terms',[]),('mobility_program',None)]:r=deepcopy(raw);r[key]=val;m.append(r)
for coeff in ['-1','00','01','1.0','1/0','1/01',True,1]:r=deepcopy(raw);r['energy_terms'][-1]['coefficient']=coeff;m.append(r)
for ex in [True,1,-2,6,2.0]:r=deepcopy(raw);r['energy_terms'][-1]['powers'][-1]=ex;m.append(r)
r=deepcopy(raw);r['energy_terms'].pop(15);m.append(r)
r=deepcopy(raw);r['energy_terms'][15]['coefficient']='0';m.append(r)
r=deepcopy(raw);r['extra']='unread term';m.append(r)
r=deepcopy(raw);r['energy_terms'][-1]['extra']='unread field';m.append(r)
for mob in [{'kind':'constant_isotropic','value':'0'},{'kind':'constant_isotropic','value':'-1'},{'kind':'constant_diagonal','entries':['1']*15},{'kind':'constant_diagonal','entries':['1']*15+['0']},{'kind':'full_SPD','entries':['1']*16}]:r=deepcopy(raw);r['mobility_program']=mob;m.append(r)
for r in m:no(lambda r=r:ac.acquire(r),'full literal derivative raw grammar rejected')
for arg in ['max_dimension','max_terms','max_coefficient_bits','max_exponent_entries','max_total_coefficient_bits','max_rational_bits']:
 for value in [True,1]:no(lambda arg=arg,value=value:ac.acquire(raw,**{arg:value}),'raw derivative finite input/arithmetic budget')
r=p.old.fixture(16);r['energy_terms']=r['energy_terms'][:16]
for _ in range(7):r['energy_terms'].append(deepcopy(r['energy_terms'][0]))
no(lambda:ac.acquire(r,max_coefficient_bits=3),'sum of admitted literal atoms must pass aggregate coefficient bit budget')
report={'status':'PASS','checks':checks,'details':details,'small_grid_minimal_exp_terms':lo,'scope':'primitive finite resource and derivative parser, not final full consumer'};(A/'boundary_independent_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
