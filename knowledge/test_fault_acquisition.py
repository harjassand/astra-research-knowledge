"""Independent exact checks of the selected saved P3 acquisition certificates.

No producer module, NetworkX routine or full scientific replay is executed.
"""
from fractions import Fraction as F
from math import isqrt
import hashlib,json,subprocess,sys,unittest
from pathlib import Path
from knowledge.model import ROOT,Inputs
from knowledge.retrieve import Library
UPDATE='research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-fault-acquisition'
SRC=ROOT/UPDATE/'source/p3'
IDS=['U1032-edge-fault-relative-recovery','U1032-group-fault-observation-cost','U1032-offset-free-equilibrium-reuse']
PROOF='ASTRA_PRO3_FAULT_TOLERANT_REUSABLE_ACQUISITION.md'
NOTICE='SN-N1032-CUT-COUNT-SCOPE-20261026'
N=12;A=F(1,10);M=F(2);ETA=F(1,10000)

def data(name):return json.loads((SRC/'originals'/name).read_bytes())
def edges():return {tuple(sorted((u,(u+d)%N)))for u in range(N)for d in (1,2,6)}
def value(i,t):
 t=F(t);v=F(1,16)+t/30+t*(1-t)/40
 return v+[0,F(1,80)+t/100,-F(1,40)+t*(1-t)/60,F(1,100)+t/40][i]
def nodes():return [value(i//3,F(i%3,2))for i in range(N)]
def upper_sqrt(x):
 scale=2**36;k=isqrt(x.numerator*scale*scale//x.denominator)
 if F(k,scale)**2<x:k+=1
 return F(k,scale)
def project(z):
 total=F(0);threshold=None
 for j,v in enumerate(sorted(z,reverse=True),1):
  total+=v;t=(total-1)/j
  if v>t:threshold=t
 assert threshold is not None
 x=[max(F(0),v-threshold)for v in z];assert sum(x)==1
 return x
def matrices():
 return [
 [[0,F(1,15),-F(1,24),0],[-F(1,20),0,F(1,25),0],[F(1,24),-F(1,18),0,F(1,25)],[0,F(1,26),-F(1,22),0]],
 [[0,-F(1,20),0,F(1,30)],[F(1,24),0,-F(1,28),0],[0,F(1,25),0,-F(1,30)],[-F(1,28),0,F(1,25),0]],
 [[0,F(1,25),F(1,25),F(1,25)],[F(1,25),0,0,0],[F(1,25),0,0,0],[F(1,25),0,0,0]],[[0]*4 for _ in range(4)]]
def envelope(centers,radii,i,t):
 pairs=[(F(centers[3*i+j]),F(radii[3*i+j]),F(j,2))for j in range(3)]
 return max(c-r-A*abs(t-s)for c,r,s in pairs),min(c+r+A*abs(t-s)for c,r,s in pairs)
def map_at(x,K,p,response):
 return project([(p[i]+sum(K[i][j]*x[j]for j in range(4))-response(i,x[i]))/M for i in range(4)])
def audit_portfolio(obj,centers,radii):
 assert obj['count']==len(obj['cases'])==60 and obj['new_native_calls']==0
 maxima=list(map(F,obj['uniform_module_error_limits']));E=F(obj['joint_E'])
 for i in range(4):
  grid=max((lambda b:(b[1]-b[0])/2)(envelope(centers,radii,i,F(j,256)))for j in range(257))
  assert maxima[i]>=grid+A/512
 assert E*E>=sum(r*r for r in maxima)
 rho_sum=F(0);largest=F(0)
 for case in obj['cases']:
  K=matrices()[int(case['network'])];p=list(map(F,case['load']));x=list(map(F,case['estimate']));ref=list(map(F,case['source_aware_reference']))
  assert all(0<=v<=1 for v in x+ref)
  q=(upper_sqrt(sum(v*v for row in K for v in row))+A)/M;assert q<1
  surrogate=lambda i,t:sum(envelope(centers,radii,i,t))/2
  after=map_at(x,K,p,surrogate);epsilon=upper_sqrt(sum((u-v)**2 for u,v in zip(after,x)))
  rho=F(case['guaranteed_position_radius']);assert rho>=(epsilon+E/M)/(1-q)
  truth=lambda i,t:value(i,t)-value(0,0)
  truth_after=map_at(ref,K,p,truth);rr=F(case['reference_iteration_residual'])
  assert rr*rr>=sum((u-v)**2 for u,v in zip(truth_after,ref))
  discrepancy=F(case['reference_discrepancy']);assert discrepancy*discrepancy>=sum((u-v)**2 for u,v in zip(x,ref))
  assert discrepancy<=rho+rr/(1-q)
  rho_sum+=rho;largest=max(largest,discrepancy)
 assert F(obj['mean_certified_radius'])==rho_sum/60
 assert F(obj['max_checked_discrepancy'])==largest
 assert obj['source_aware_reference_function_evaluations']==60*4*56
 return 60,60*4*56
def audit_paths(certificates,noisy=False):
 es=edges();zs=nodes();rr={e:zs[e[1]]-zs[e[0]]for e in es};rr[(0,1)]+=7;rr[(4,6)]-=11
 if noisy:
  for j,e in enumerate(sorted(es)):rr[e]+=ETA*F((-1)**j,2)
 assert set(certificates)==set(map(str,range(1,N)))
 for target,cert in certificates.items():
  paths=cert['paths'];assert len(paths)==5;used=set();sums=[]
  for path in paths:
   assert path[0]==0 and path[-1]==int(target);seen=set();total=F(0)
   for u,v in zip(path,path[1:]):
    e=tuple(sorted((u,v)));assert e in es and e not in seen and e not in used;seen.add(e);total+=rr[e]if u<v else-rr[e]
   used.update(seen);sums.append(total)
  assert sums==list(map(F,cert['path_sums']))
  center=sorted(sums)[2];assert center==F(cert['median'])
  radius=max(len(p)-1 for p in paths)*ETA if noisy else F(0)
  assert F(cert['certified_radius'])==radius and abs(center-zs[int(target)]+zs[0])<=radius
def complete_cuts():
 es=edges();sizes=[]
 for mask in range(2**11):
  subset={0}|{j+1 for j in range(11)if mask>>j&1}
  if len(subset)<N:sizes.append(sum((u in subset)!=(v in subset)for u,v in es))
 assert len(es)==30 and all(sum(v in e for e in es)==5 for v in range(N))
 assert len(sizes)==2047 and min(sizes)==5
 return len(sizes),min(sizes)
def audit_selected():
 cuts,minimum=complete_cuts();scalar=data('fault_tolerant_acquisition_results.json');group=data('group_fault_acquisition_results.json');op=group['group_robust_operation']
 assert scalar['graph']['nontrivial_cuts_exhaustively_checked']==2046
 assert data('independent_verification_results.json')['min_cut_cuts']==2047
 audit_paths(scalar['path_decoding_certificates']);audit_paths(scalar['nonzero_honest_noise']['path_decoding_certificates'],True)
 zs=nodes();relative=[v-zs[0]for v in zs];assert relative==list(map(F,scalar['decoded_exact_values_relative_to_node0']))
 assert {tuple(r['edge']):F(r['residual'])for r in scalar['corrupted_edge_residuals_exact']}=={(0,1):F(7),(4,6):F(-11)}
 reports=[[F(v)for v in row]for row in op['synthetic_report_groups']];assert len(reports)==5 and all(len(row)==11 for row in reports)
 decoded=[F(0)]+[sorted(row[j]for row in reports)[2]for j in range(11)];assert decoded==relative==list(map(F,op['exact_recovered_relative_values']))
 assert op['physical_instrument_group_calls']==5 and op['total_returned_scalars']==55
 exact=audit_portfolio(scalar['exact_later_operations'],relative,[0]*N)
 noisy=scalar['nonzero_honest_noise'];no=audit_portfolio(noisy['later_operations'],noisy['decoded_centers'],noisy['certified_node_radii'])
 groups=audit_portfolio(op['future_tasks'],decoded,[0]*N)
 return dict(proper_rooted_cuts=cuts,mincut=minimum,certificate_labels=sum(x[0]for x in [exact,no,groups]),reference_component_evaluations=sum(x[1]for x in [exact,no,groups]))

class FaultAcquisition(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.library=Library()

 def test_complete_cuts_preserve_original_count_discrepancy(self):
  self.assertEqual(complete_cuts(),(2047,5));self.assertEqual(data('fault_tolerant_acquisition_results.json')['graph']['nontrivial_cuts_exhaustively_checked'],2046)
  self.assertEqual(data('independent_verification_results.json')['min_cut_cuts'],2047)
  scalar=(SRC/'originals/fault_tolerant_acquisition.py').read_text();verifier=(SRC/'originals/verify_fault_tolerant_research.py').read_text()
  self.assertIn('range(1,1<<(N-1))',scalar);self.assertIn('range(0,2**11)',verifier)

 def test_all_exact_noisy_paths_and_robust_medians(self):
  scalar=data('fault_tolerant_acquisition_results.json');audit_paths(scalar['path_decoding_certificates']);audit_paths(scalar['nonzero_honest_noise']['path_decoding_certificates'],True)

 def test_29_edge_indistinguishability(self):
  witness=data('fault_tolerant_acquisition_results.json')['deleted_edge_lower_bound'];es=edges()-{(0,1)}
  z0=[F(0)]*N;z1=[F(0)]*N;z1[0]=F(witness['alternative_difference_at_node_0'])
  bad0={tuple(e)for e in witness['faults_required_for_first_source']};bad1={tuple(e)for e in witness['faults_required_for_second_source']}
  rr={e:z1[e[1]]-z1[e[0]]if e in bad0 else F(0)for e in es}
  self.assertEqual({e for e in es if rr[e]!=z0[e[1]]-z0[e[0]]},bad0)
  self.assertEqual({e for e in es if rr[e]!=z1[e[1]]-z1[e[0]]},bad1);self.assertEqual((len(es),len(bad0),len(bad1)),(29,2,2));self.assertLessEqual(abs(z1[0]),A/2)

 def test_one_group_failure_does_not_invalidate_edge_theorem(self):
  obj=data('group_fault_acquisition_results.json');c=obj['edge_connectivity_insufficient_for_group_faults'];owned={tuple(e)for e in c['one_bad_group_edges']};z0=list(map(F,c['first_source_zero_vector']));z1=list(map(F,c['second_source_shifted_root_vector']))
  changed={e for e in edges()if z0[e[1]]-z0[e[0]]!=z1[e[1]]-z1[e[0]]};self.assertEqual(changed,owned);self.assertEqual(len(changed),5);self.assertGreater(len(changed),2)
  self.assertEqual(obj['minimum_scalar_readings_for_exactly_five_independent_groups'],55)

 def test_global_gauge_invariance_and_separate_offset_failure(self):
  z=[F(-1,3),F(4,7),F(8,9),F(3,5)];self.assertEqual(project(z),project([v+F(17,5)for v in z]))
  self.assertNotEqual(project([F(0),F(0)]),project([F(1),F(0)]))
  # Derivatives of the declared scalar synthetic polynomial sources are affine.
  for i in range(4):
   for t in [F(0),F(1)]:
    d=F(1,30)+(1-2*t)/40+[0,F(1,100),(1-2*t)/60,F(1,40)][i];self.assertLessEqual(abs(d),A)
  self.assertIn('q<1',self.library.resolve(IDS[2])['contract']['requires'][1])

 def test_selected_180_saved_equilibrium_certificates_and_costs(self):
  self.assertEqual(audit_selected(),dict(proper_rooted_cuts=2047,mincut=5,certificate_labels=180,reference_component_evaluations=40320))

 def test_actual_source_ranges_review_versions_and_support_failure(self):
  index=json.loads((ROOT/UPDATE/'source/INDEX.json').read_bytes());self.assertEqual(len(index['files']),8);self.assertEqual(sum(r['bytes']for r in index['files']),203129)
  for row in index['files']:self.assertEqual(hashlib.sha256((ROOT/UPDATE/row['path']).read_bytes()).hexdigest(),row['sha256'])
  for identifier,lines,phrase in [(IDS[0],[13,43],'2f+1'),(IDS[1],[77,85],'55'),(IDS[2],[45,75],'common scalar')]:
   source=self.library.source(identifier,0);self.assertEqual(source['source']['lines'],lines);self.assertIn(phrase,source['text'])
  for identifier in ['N1032',*IDS]:
   record=self.library.resolve(identifier);review=next(r for r in record['review_overlays']if r['id']=='A1052-fault-acquisition');self.assertEqual(review['decision'],'accepted_internally_verified');self.assertIn({'id':record['id'],'content_version':record['content_version']},review['subjects']);self.assertEqual(review['working_device'],'not established')
   self.assertTrue(any(n['notice_id']==NOTICE and not n['whole_claim_invalidated']for n in record['notices']))
  with self.assertRaisesRegex(ValueError,'INGESTION FAILED: required source bytes missing'):
   Inputs(ROOT).source(dict(path=UPDATE+'/source/p3/required_but_missing.json',sha256='0'*64,lines=[1,1]))

 def test_bridges_endpoint_versions_and_default_packets(self):
  for b,state in [(IDS[2],'ESTABLISHED COMPATIBLE INTERFACE'),(IDS[1],'REFUTED TRANSFER')]:
   transfer=self.library.bridge(IDS[0],b)['transfers'][0];self.assertEqual(transfer['state'],state)
   for e in ['from','to']:self.assertEqual(transfer[e+'_version'],self.library.resolve(transfer[e])['content_version'])
  for args in [('packet',i)for i in ['N1032',*IDS]]+[('bridge',IDS[0],i)for i in IDS[1:]]:
   p=subprocess.run([sys.executable,'knowledge/retrieve.py',*args],cwd=ROOT,capture_output=True);self.assertEqual(p.returncode,0,p.stderr);self.assertLessEqual(len(p.stdout),32768)

if __name__=='__main__':unittest.main()
