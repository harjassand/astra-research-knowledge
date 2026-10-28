"""Exact all-nine/Bell/common-bath controls, with no eigensolver premise.

Three eigenvalues of a rational Q[sqrt(-3)] matrix are isolated by a
rational Sturm sequence. Scalar log enclosures are from the independent
arith.py module. The general all-nine inequality is analytic, not inferred
from these controls.
"""
from fractions import Fraction as Q
from pathlib import Path
from time import perf_counter
import itertools,json,sys
import frame as f
import arith as a
sys.set_int_max_str_digits(0)
HERE=Path(__file__).resolve().parent

def trim(p):
 while len(p)>1 and p[-1]==0:p.pop()
 return p
def poly_value(p,x):
 value=Q(0)
 for c in reversed(p):value=value*x+c
 return value
def poly_remainder(p,q):
 p=p[:]
 while len(p)>=len(q)and p!=[0]:
  factor=p[-1]/q[-1];shift=len(p)-len(q)
  for j,c in enumerate(q):p[j+shift]-=factor*c
  trim(p)
 return p
def sturm(p):
 seq=[p,[i*p[i]for i in range(1,len(p))]]
 while len(seq[-1])>1:
  r=poly_remainder(seq[-2],seq[-1]);assert r!=[0]
  seq.append([-x for x in r])
 return seq
def variation(seq,x):
 signs=[1 if v>0 else-1 for p in seq if(v:=poly_value(p,x))!=0]
 return sum(x!=y for x,y in zip(signs,signs[1:]))
def isolate(p,bits=76):
 seq=sturm(p)
 def count(lo,hi):return variation(seq,lo)-variation(seq,hi)
 assert poly_value(p,0)!=0 and poly_value(p,1)!=0 and count(Q(0),Q(1))==3
 todo=[(Q(0),Q(1),3)];roots=[];steps=0
 while todo:
  lo,hi,n=todo.pop()
  if n==1 and hi-lo<=Q(1,2**bits):roots.append((lo,hi));continue
  split=next(lo+(hi-lo)/d for d in range(2,6)if poly_value(p,lo+(hi-lo)/d)!=0)
  left=count(lo,split);right=count(split,hi);assert left+right==n
  if left:todo.append((lo,split,left))
  if right:todo.append((split,hi,right))
  steps+=1
 roots.sort();assert len(roots)==3
 return roots,steps

def entropy_source(weights):
 total=Q(sum(weights));p=[Q(x)/total for x in weights]
 m=f.linear_combination(p,f.SICS)
 trace=f.trace(m);purity=f.trace(f.mm(m,m));det=f.determinant3(m)
 assert trace==f.z(1)and purity[1]==det[1]==0
 s=sum(x*x for x in p);assert purity[0]==(1+3*s)/4
 polynomial=[-det[0],(1-purity[0])/2,-Q(1),Q(1)]
 roots,steps=isolate(polynomial)
 sm=a.entropy(roots);hp=a.entropy([a.iv(x)for x in p]);delta=a.sub(a.scale(sm,2),hp)
 assert delta[0]>0
 relaxation=a.sub(a.scale(a.lower_entropy3(purity[0]),2),a.upper_entropy(s,9))
 # A matched ordinary purity relaxation may fail without a negative Delta.
 return {'raw_weights':weights,'trace':a.serial(total),'input_purity':a.serial(s),
         'output_purity':a.serial(purity[0]),'characteristic_polynomial_ascending':[a.serial(x)for x in polynomial],
         'eigenvalue_intervals':[a.record(x)for x in roots],'Sturm_splits':steps,
         'source_Delta_per_trace':a.record(delta),'scalar_purity_lower_envelope':a.record(relaxation)},p,delta

def bath_fixture(weights,p,delta):
 total=Q(sum(weights));x=f.linear_combination(weights,f.BELLS)
 u=[[Q(1,2)]*2 for _ in range(2)];v=[[Q(1),Q(0)],[Q(0),Q(0)]]
 z=f.zeros(18)
 for i in range(9):
  for j in range(9):
   for r in range(2):
    for s in range(2):
     z[2*i+r][2*j+s]=f.add(f.scale(x[i][j],u[r][s]),f.z(int(i==j)*v[r][s]))
 assert f.trace(z)==f.z(total+9)
 for i in range(3):
  for j in range(3):
   marginal=f.total(z[2*(3*i+b)+r][2*(3*j+b)+r]for b in range(3)for r in range(2))
   assert marginal==f.z((total+9)/3 if i==j else 0)
 for i in range(9):
  for j in range(9):assert z[2*i+1][2*j+1]==f.scale(x[i][j],Q(1,2))
 # q'(0+)=1/2 for U=|+><+|, V=|0><0|. The remaining positive
 # spectral-mixture measure can be discarded because the whole white ray
 # is paid by the all-nine theorem.
 rawgap=a.scale(delta,total/2);cmigap=a.scale(rawgap,1/(total+9))
 assert cmigap[0]>Q('0.02874184987290896')
 off=[[x[i][3+j]for j in range(3)]for i in range(3)]
 off2=f.mm(off,off);assert any(t!=f.z()for row in off2 for t in row)
 assert len(set(weights))==9 and Q(max(weights),min(weights))>24 and max(p)>Q(2,3)
 # The singlet eigenvector for the largest Bell weight tests the reduction
 # inequality X<=I tensor Tr_A X=(T/3)I exactly.
 assert max(weights)>total/3
 return{'dimension':18,'reference_dimension':6,'antisymmetric_extension_dimension':54,
         'source_trace':a.serial(total+9),'scalar_TP_normalization':a.serial(Q(3)/(total+9)),
         'common_bath_U':[[a.serial(t)for t in row]for row in u],
         'common_bath_V':[[a.serial(t)for t in row]for row in v],
         'noncommuting_singular_bath':True,'white_ray':'all a>=0, analytic all-nine theorem',
         'bath_atom_weight':'1/2','raw_Delta_lower':a.record(rawgap),'CMI_excess_lower':a.record(cmigap),
         'lower_expression_interval_convention':'Actual bath Delta and CMI exceed the lower endpoints. The displayed upper endpoints bound only the discarded-mass lower expressions, not the actual bath quantities.',
         'matched_literal_exclusions':{'scalar_at_most_two_spectral_levels':True,
          'condition_number_at_most_24':True,'reduction_region':True,
          'Schmidt_number_at_most_two':True,'fixed_physical_block_square_zero':True},
         'scope_limit':'These exclude only the named literal premises, not every positive source or operator-bath theorem.'}

def main():
 start=perf_counter();near,p,d=entropy_source([44,1,2,3,4,5,6,7,8])
 # The exact sign assertion is independent of the display-only conversion.
 assert Q(near['scalar_purity_lower_envelope']['upper'])<0
 robust,p,delta=entropy_source([1000,1,2,3,4,5,6,7,8])
 bath=bath_fixture(robust['raw_weights'],p,delta)
 # Rational universal inequalities underlying fourth partial-sum bounds.
 assert Q(16,5)**2>=10 and Q(11,6)**2>=Q(10,3)
 result={'status':'PASS','proof':'ALL_NINE_PROOF.md','purity_relaxation_control':near,
 'nine_distinct_bath_seed':robust,'common_bath_receiver':bath,
 'acquisition':'No numerical eigensolver/SDP; exact field products, cubic Sturm isolation and rational log intervals.',
 'seconds':perf_counter()-start,'priority':'UNKNOWN','unrestricted_WH3_or_CLR_claim':False}
 (HERE/'ALL_NINE_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'status':result['status'],'seconds':result['seconds'],
 'matched_purity_relaxation':near['scalar_purity_lower_envelope']['display_only'],
 'actual_purity_control_Delta':near['source_Delta_per_trace']['display_only'],
 'robust_Bell_Delta':robust['source_Delta_per_trace']['display_only'],
 'bath_CMI_excess_lower':bath['CMI_excess_lower']['display_only']},indent=2))
if __name__=='__main__':main()
