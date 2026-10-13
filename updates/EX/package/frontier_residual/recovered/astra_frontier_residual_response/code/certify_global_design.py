"""Exact continuous-domain macroscopic design from complete response-jet certificates.
Numerical discovery is not used in this checker. All operations are rational except
outward-rounded displayed summaries. Source certificates require Pauli verification.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import json,sys,time,hashlib
from jet_design import ev,bernstein,tight_interval,gram_q_bounds,error_jet

def pair(x):return dict(exact=[str(a) for a in x],decimal=[float(a) for a in x])
def check_digest(path,rec):
 p=path.with_suffix('.npz')
 assert hashlib.sha256(p.read_bytes()).hexdigest()==rec['witness_sha256']
 assert rec['balance_exact'] and rec['zero_jet_gap_exact']

def check(root):
 start=time.perf_counter();mainpath=root/'fresh/witness.json'
 rec=json.loads(mainpath.read_text());check_digest(mainpath,rec)
 ctr=F(rec['parameters']['V']);assert ctr==F(1109,512)
 anchors=[]
 for name in ['V0','Vhalf','V1','V1half','V3','V2','V2half']:
  path=root/'anchors'/f'{name}.json';r=json.loads(path.read_text());check_digest(path,r)
  c=list(map(F,r['upper_D_polynomial_exact']));assert len(c)==3 and c[2]>=0
  anchors.append((F(r['parameters']['V']),c,r,path))
 low,up=map(F,rec['D_interval_exact'])
 def anchor_upper(a,b):
  return min(max(ev(c,a-v),ev(c,b-v)) for v,c,r,p in anchors)
 def domain_upper(a,b,n=1024):
  return max(anchor_upper(a+(b-a)*F(i,n),a+(b-a)*F(i+1,n)) for i in range(n))
 leftup=domain_upper(F(0),F(2));rightup=domain_upper(F(5,2),F(3))
 assert leftup<low and rightup<low
 big=(F(2),F(5,2));cbig=tight_interval(rec,*big,2);assert cbig[1]<0
 bracket=(F(2157,1000),F(87,40));dl=tight_interval(rec,bracket[0],bracket[0],1);dr=tight_interval(rec,bracket[1],bracket[1],1)
 assert dl[0]>0 and dr[1]<0
 small=(F(43,20),F(219,100));assert small[0]<=bracket[0]<ctr<bracket[1]<=small[1]
 csmall=tight_interval(rec,*small,2);mu=-csmall[1];M=-csmall[0];assert mu>0
 dctr=tight_interval(rec,ctr,ctr,1);g=max(abs(q) for q in dctr);regret=g*g/(2*mu)
 old=F(71,32);p=list(map(F,rec['corrected_D_polynomial_exact']));delta_hat=ev(p,F(0))-ev(p,old-ctr)
 e=(old-ctr)*error_jet(gram_q_bounds(rec,ctr,old),1)
 improve=(delta_hat-e,delta_hat+e);assert improve[0]>0
 lo_poly=list(map(F,rec['lower_D_polynomial_exact']));up_poly=list(map(F,rec['upper_D_polynomial_exact']))
 independent=(low-ev(up_poly,old-ctr),up-ev(lo_poly,old-ctr));assert independent[0]<0<independent[1]
 # A matched value-only global certificate using every identical response packet.
 n=1024
 value_middle=[]
 for i in range(n):
  a=big[0]+(big[1]-big[0])*F(i,n);b=big[0]+(big[1]-big[0])*F(i+1,n)
  central=bernstein(up_poly,a-ctr,b-ctr)[1]
  value_middle.append(min(central,anchor_upper(a,b)))
 value_global=max(leftup,rightup,max(value_middle));value_regret=value_global-low
 tol=F(1,1024);assert small[0]<ctr-tol and ctr+tol<small[1]
 tolerant_regret=regret+g*tol+M*tol*tol/2
 maxring=max([rec['min_finite_ring_size']]+[r['min_finite_ring_size'] for _,_,r,_ in anchors])
 out=dict(status='All displayed inequalities verified with exact rational arithmetic, conditional on the mathematical transport and response-jet theorems.',parameters=rec['parameters'],domain=['0','3'],chosen_control=str(ctr),D_chosen=pair((low,up)),unique_global_maximizer=True,optimizer_bracket=pair(bracket),positive_derivative_left=pair(dl),negative_derivative_right=pair(dr),global_exclusion=dict(left_domain=['0','2'],left_upper_exact=str(leftup),left_upper=float(leftup),right_domain=['5/2','3'],right_upper_exact=str(rightup),right_upper=float(rightup),chosen_lower_exact=str(low)),curvature_large=pair(cbig),curvature_large_domain=list(map(str,big)),curvature_small=pair(csmall),curvature_small_domain=list(map(str,small)),derivative_chosen=pair(dctr),g_upper_exact=str(g),strong_concavity_mu_exact=str(mu),global_regret_upper_exact=str(regret),global_regret_upper=float(regret),old_control=str(old),improvement_over_old=pair(improve),independent_value_difference=pair(independent),matched_value_only_global_upper_exact=str(value_global),matched_value_only_regret_exact=str(value_regret),matched_value_only_regret=float(value_regret),matched_regret_ratio=float(value_regret/regret),actuator_error=str(tol),regret_with_actuator_error_exact=str(tolerant_regret),regret_with_actuator_error=float(tolerant_regret),same_results_for_every_finite_ring_n_at_least=maxring,cells_per_envelope=1024,main_sha256=rec['witness_sha256'],anchor_sha256={p.stem:r['witness_sha256'] for _,_,r,p in anchors},seconds=time.perf_counter()-start)
 (root/'global_design.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));return out
if __name__=='__main__':check(Path(sys.argv[1]))
