from pathlib import Path
import json
import sympy as s
checks=[]
def ck(name,condition):
 assert condition,name
 checks.append(name)
# Incoming two-program arithmetic, exact supplied synthetic fixtures.
r1=s.Matrix([4,2,6]);r2=s.Matrix([-1,-2,-3]);lam=s.Rational(1,3)
ck('neutral_program_1',r1[0]+r1[1]==r1[2]);ck('neutral_program_2',r2[0]+r2[1]==r2[2])
ck('two_program_exchange',lam*r1+(1-lam)*r2==s.Matrix([s.Rational(2,3),-s.Rational(2,3),0]))
# Exact finite-zero countermodel, ordered edges: forward, backward, loop1, idle0.
B=s.Matrix([[-1,1,0,0],[1,-1,0,0]]);salt=s.Matrix([1,0,0,0]);exchange=s.Matrix([0,0,1,0]);time=s.ones(4,1)
f=s.Matrix([0,0,1,0]);ck('circulation_relaxation',B*f==s.zeros(2,1));ck('relaxed_salt_zero',(salt.T*f)[0]==0);ck('relaxed_unit_rate',(exchange.T*f)[0]==1 and(time.T*f)[0]==1)
# Dual tau=1,u=0,kappa=0 bounds every edge and certifies optimality1.
ck('dual_bound_one',all(exchange[i]<=time[i] for i in range(4)))
# Every restored path has equal forward/backward counts. Nonzero exchange from0
# requires a visit to1, hence a forward count>=1 and strictly positive salt.
for n in [1,2,5,100]:
 counts=s.Matrix([1,1,n,0]);ck('restored_'+str(n),B*counts==s.zeros(2,1));ck('positive_connector_salt_'+str(n),(salt.T*counts)[0]==1);ck('rate_'+str(n),(exchange.T*counts)[0]/(time.T*counts)[0]==s.Rational(n,n+2))
# Inventory gauge: different transient selectivities; exact cycle exchange0.
u=s.Matrix([0,3]);k=s.Rational(2,5);ss=s.Matrix([2,-2,1,0]);xx=k*ss+B.T*u
ck('different_edge_selectivities',xx[0]/ss[0]!=xx[2]/ss[2] and xx[2]/ss[2]==k)
cycle=s.Matrix([1,1,0,0]);ck('telescoping_inventory_gauge',(xx.T*cycle)[0]==k*(ss.T*cycle)[0]==0)
# Robust box support: all four vertices attain/check epsx+abs(kappa)*epss.
for kap in [-2,s.Rational(1,3),0]:
 ex=s.Rational(1,10);es=s.Rational(1,20)
 vals=[dx-kap*ds for dx in [-ex,ex] for ds in [-es,es]]
 ck('box_support_'+str(kap),max(vals)==ex+abs(kap)*es)
result={'schema':'astra.fy-cyclic-control-check.v1','status':'PASS','check_count':len(checks),'checks':checks,'scope':'Exact synthetic algebra only. The classical LP/closure proofs are written separately; no measured species response or physical separator acquired.'}
Path(__file__).with_name('CYCLIC_CONTROL_CHECK.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(checks)}))
