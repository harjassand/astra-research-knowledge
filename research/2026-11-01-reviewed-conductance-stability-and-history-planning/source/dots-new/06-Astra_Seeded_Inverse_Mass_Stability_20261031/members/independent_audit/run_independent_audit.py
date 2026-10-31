#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product,permutations
from pathlib import Path
from math import isqrt
import importlib.util,json,copy,hashlib
import independent_seeded_receiver as v
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
spec=importlib.util.spec_from_file_location('candidate',HERE/'frozen_seeded_inverse_mass.py');s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)

def hard_raw(rates=(1,1,1,1,1,1,2,1)):
 l,m,a,b,c,d,e,f=map(F,rates)
 return [((0,0,0),(1,0,0),l),((1,0,0),(0,0,0),m),((2,1,0),(1,1,1),a),((1,1,1),(2,1,0),b),((2,0,1),(1,2,0),c),((1,2,0),(2,0,1),d),((1,1,1),(1,0,2),e),((1,0,2),(1,1,1),f)]
def comps(N,n):
 if n==1:yield(N,)
 else:
  for a in range(N+1):
   for z in comps(N-a,n-1):yield(a,)+z

def exercise(label,raw,cert,limit=14):
 t=F(cert['t']);weights=tuple(map(F,cert['weights']));rec,c,check=v.generator_checker(raw,t,weights,cert);n=rec['n'];A=rec['a'];J=rec['satellites'];count=0;expanded=0
 for N in range(limit+1):
  for x in comps(N,n):
   q=check(x);count+=1
   if N<=5:
    def value(y):return t**sum(y)*(c['h0'] if y[A]==0 else 1+c['c']/(y[A]+sum(w*y[j]for w,j in zip(weights,J))))
    actual=F(0)
    for u,z,k in rec['channels']:
     rate=k*v.ff(x,u)
     if rate:actual+=rate*(value(tuple(a-b+d for a,b,d in zip(x,u,z)))-value(x))
    assert actual/value(x)==q;expanded+=1
 points=[]
 for a in [0,1,2,c['A_cut']-1,c['A_cut']]:
  for j,cut in zip(J,c['B_cuts']):
   for b in [cut-1,cut,cut+1,10**50]:
    x=[0]*n;x[A]=a;x[j]=b;points.append(tuple(x))
 points += [(10**6,)*n,(10**50,)*n]
 for x in points:check(x)
 return {'label':label,'dimension':n,'ordinary_exact_states':count,'targeted_exact_states':len(points),'expanded_small_W_checks':expanded,'S':str(c['S']),'ell':str(c['ell']),'K1':str(c['K1']),'c':str(c['c']),'cutoffs':[c['A_cut']]+list(c['B_cuts'])}

def main():
 original=json.loads((HERE/'frozen_hard_demo.json').read_text());x=json.loads((HERE/'frozen_exercise_results.json').read_text());raw=hard_raw();v.hard_audit(raw,F(2),original);assert v.receive_structural(raw,original['qualitative'])
 invalid_audit_t=[]
 for bad_t in [F(1),F(0),F(1,2),F(-1),1.0,True]:
  try:v.hard_audit(raw,bad_t,original)
  except (AssertionError,ValueError):invalid_audit_t.append(repr(bad_t))
  else:raise AssertionError('invalid audit t accepted')
 heter=hard_raw((F(2,3),F(7,5),F(1,2),F(3,4),F(5,7),F(2,9),F(11,3),F(13,5)))
 zero=[((0,0),(1,0),1),((1,0),(0,0),1),((3,0),(1,2),2),((1,2),(3,0),3)]
 star=[((0,0,0,0),(1,0,0,0),1),((1,0,0,0),(0,0,0,0),1)]
 for j in range(1,4):
  u=tuple(2*int(i==0)+int(i==j)for i in range(4));z=tuple(int(i==0)+2*int(i==j)for i in range(4));star += [(u,z,F(j,2)),(z,u,F(j+1,3))]
 unary=raw+[((2,0,0),(1,1,0),F(3,5)),((1,1,0),(2,0,0),F(7,4))]
 rawcases=[raw,raw,raw,heter,zero,star,unary];rows=[]
 for row,rr in zip(x['cases'],rawcases):
  cert=row['certificate'];bundle={'status':'CERTIFIED','certificate':cert,'acquisition':row['acquisition']};route=row['acquisition']['route']
  if route=='recognized mediated triangle halving':v.hard_audit(rr,F(cert['t']),bundle)
  elif route=='rational grid':v.grid_audit(rr,F(cert['t']),bundle)
  else:
   eta=F(1,8);tries=0
   while True:
    c=v.derive(v.recognize(rr),F(2),(eta,F(0)));tries+=1
    if c['status']=='CERTIFIED_REQUESTED_T_MOMENT':break
    eta/=2
   assert tries==row['acquisition']['profiles'] and v.canonical(c)==v.canonical(cert)
  rows.append(exercise(row['label'],rr,cert,10 if len(rr[0][0])==4 else 14))
 # Additional hard-family branch coverage from candidate proposals, independently received.
 for label,rr in [('hard_c_cap_one',hard_raw((1,10**8,1,1,1,1,2,1))),('hard_initial_eta_passes',hard_raw((1,1,1,F(1,10**6),1,1,2,1)))]:
  b=v.wire(s.hard_search(rr,F(2),100));v.hard_audit(rr,F(2),b);rows.append(exercise(label,rr,b['certificate'],10))
  if label=='hard_c_cap_one':assert F(b['certificate']['c'])==1
  else:assert b['acquisition']['profiles']==1
 # Same fixed profile is NOT an all-t numerical certificate.
 w=tuple(map(F,original['certificate']['weights']));old_at_large=v.derive(v.recognize(raw),F(100),w)
 assert old_at_large['status']=='PROFILE_REJECTED' and old_at_large['reasons']==['finite-head compatibility failed']
 assert not v.receive(raw,F(100),w,original['certificate'])
 assert x['cases'][2]['certificate']['status']=='CERTIFIED_REQUESTED_T_MOMENT' and tuple(map(F,x['cases'][2]['certificate']['weights']))!=w
 # All six raw coordinate permutations with rate splitting/null normalization.
 metamorphic=[]
 for perm in permutations(range(3)):
  rr=[(tuple(u[i]for i in perm),tuple(z[i]for i in perm),k)for u,z,k in reversed(raw)];u,z,k=rr.pop();rr += [(u,z,k/3),(u,z,2*k/3),((0,0,0),(0,0,0),F(1))]
  b=v.wire(s.hard_search(rr,F(2),100));v.hard_audit(rr,F(2),b);assert v.receive_structural(rr,b['qualitative']);metamorphic.append({'permutation':perm,'A':b['certificate']['open_coordinate'],'profiles':b['acquisition']['profiles']})
 # Both capped routes and the analytic opposing-profile obstruction.
 v.hard_audit(raw,F(2),x['capped_quantitative_preserves_qualitative']);assert v.receive_structural(raw,x['capped_quantitative_preserves_qualitative']['qualitative'])
 v.grid_audit(raw,F(2),x['generic_capped'])
 opposing=raw[:2]
 for u,z in [((1,2,0),(1,1,1)),((1,1,1),(1,0,2)),((1,1,1),(2,1,0))]:opposing += [(u,z,F(1)),(z,u,F(1))]
 v.grid_audit(opposing,F(2),x['opposing_profile_class_obstruction']['budgeted_result'])
 cap4=v.wire(s.generic_search(opposing,F(2),4));v.grid_audit(opposing,F(2),cap4);assert cap4['acquisition']['last_denominator']==2
 signs=0
 for weights in product([F(0),F(1,4),F(1,2),F(1)],repeat=2):
  d=v.derive(v.recognize(opposing),F(2),weights);assert d['status']=='PROFILE_REJECTED' and not all(u>0 for u in d['pure']);signs+=1
 # Fully independent semantic mutations, not mere candidate re-derivation.
 cert=original['certificate'];mutations=[]
 for key in ['raw_sha256','dimension','open_coordinate','satellite_coordinates','t','weights','ell','source_coefficients','pure','K1','K2','K','D','c','C','zeta','S','head_strength','A_cut','B_cuts','tail_threshold','exception_states_not_enumerated','N_max','h0','foster_prefactor','foster_base','foster_exponent','foster_bits','guarantee','extra']:
  q=copy.deepcopy(cert)
  if key=='raw_sha256':q[key]='0'*64
  elif key in ['dimension','open_coordinate','A_cut','exception_states_not_enumerated','N_max']:q[key]+=1
  elif key=='satellite_coordinates':q[key]=list(reversed(q[key]))
  elif key in ['weights','pure']:q[key][0]=str(F(q[key][0])+1)
  elif key=='B_cuts':q[key][0]=1
  elif key=='source_coefficients':q[key][0][1]=str(F(q[key][0][1])+1)
  elif key=='foster_prefactor':q['foster_constant_factored']['prefactor']='0'
  elif key=='foster_base':q['foster_constant_factored']['base']='1'
  elif key=='foster_exponent':q['foster_constant_factored']['exponent']=0
  elif key=='foster_bits':q['foster_constant_factored']['expanded_numerator_bits_upper']=0
  elif key=='guarantee':q[key]='all bases follow from every fixed profile'
  elif key=='extra':q['oracle']='trusted'
  else:q[key]=str(F(q[key])+1)
  assert not v.receive(raw,F(2),w,q) and not s.receive(raw,F(2),w,q);mutations.append(key)
 # Search-accounting corruptions: independent replay rejects every one.
 accounting=[]
 for key in ['profiles','source_term_evaluations','trials_eta','trials_status','trials_strength','guaranteed_trials','guarantee_bound_halvings','eta0','eta_required_sufficient','Kbar','c0','retained_rational_peak_bits','recognition_input_rows','recognition_graph_edge_visits','cap_scope','all_t_qualitative','route','extra']:
  b=copy.deepcopy(original);ac=b['acquisition']
  if key=='trials_eta':ac['trials'][0]['eta']='0'
  elif key=='trials_status':ac['trials'][0]['certificate_status']='CERTIFIED_REQUESTED_T_MOMENT'
  elif key=='trials_strength':ac['trials'][0]['head_strength']='0'
  elif key in ['cap_scope','all_t_qualitative','route']:ac[key]='unsupported claim'
  elif key=='extra':ac['unpaid_oracle']=True
  elif key in ['eta0','eta_required_sufficient','Kbar','c0']:ac[key]=str(F(ac[key])+1)
  else:ac[key]+=1
  try:v.hard_audit(raw,F(2),b)
  except (AssertionError,KeyError):accounting.append(key)
  else:raise AssertionError('accounting mutation accepted '+key)
 structural=[]
 for key,value in [('profile_evaluations',1),('mediator_coordinate',2),('numerical_foster_constants_provided',True),('recognition_input_rows',0),('recognition_graph_edge_visits',0),('guarantee','all weakly reversible networks')]:
  q=copy.deepcopy(x['structural']);q[key]=value;assert not v.receive_structural(raw,q) and not s.receive_structural(raw,q);structural.append(key)
 huge=hard_raw((10**100,F(1,10**100),1,1,1,1,2,1));assert v.receive_structural(huge,x['structural_huge_rates'])
 # Guard numerical constructors in both implementations during qualitative use.
 def deny(*a,**k):raise AssertionError('qualitative invoked quantitative work')
 saved=(s.derive,s.hard_search,s.generic_search,v.derive)
 s.derive=s.hard_search=s.generic_search=v.derive=deny
 try:
  assert v.receive_structural(huge,v.wire(s.hard_structural(huge)))
 finally:s.derive,s.hard_search,s.generic_search,v.derive=saved
 # Independently check exact rational entropy lower bounds, without log evaluation.
 ent=json.loads((ROOT/'entropy_exact_controls.json').read_text())
 for e in ent['checks']:
  n=e['n'];root=isqrt(n);assert root*root==n
  lower=F(2*n**3,n+1)-n*root;assert lower==F(e['exact_lower_using_log_n_le_sqrt_n'])>0 and e['positive']
 print(json.dumps({'candidate_source_sha256':hashlib.sha256((HERE/'frozen_seeded_inverse_mass.py').read_bytes()).hexdigest(),
 'independent_raw_semantic_and_search_receiving':True,'cases':rows,'metamorphic_permutations':metamorphic,
 'invalid_hard_audit_t_rejected_before_bound_loop':invalid_audit_t,
 'fixed_t_profile_rejected_at_t100_but_separate_acquisition_succeeds':True,
 'semantic_tampers_rejected':mutations,'halving_accounting_tampers_rejected':accounting,'structural_tampers_rejected':structural,
 'capped_quantitative_preserves_qualitative':True,'generic_grid_cap_replay_verified':True,
 'generic_last_denominator_is_cap_check_cursor_not_necessarily_last_tested':{'cap4_only_denominator1_profiles_tested':True,'reported_cursor':cap4['acquisition']['last_denominator']},
 'opposing_pure_sign_controls':signs,'guarded_qualitative_huge_rate_receiving':True,'entropy_rational_lower_bounds_verified':len(ent['checks']),
 'finite_tests_supplement_proof':True},indent=2))
if __name__=='__main__':main()
