"""Acquire a literal strong coherent source and rational CMI receiver."""
from fractions import Fraction as Q
from pathlib import Path
import json,time
import certify_sic_sparse as cert
import replay_sic_exact as exact
def enc(x):return str(x.numerator)+'/'+str(x.denominator)
def composition_receiver(labels,weights):
 assert 1<=len(weights)<=5 and len(labels)==len(weights)
 assert all(isinstance(p,(int,Q)) for p in weights)
 weights=[Q(p) for p in weights]
 assert all(p>=0 for p in weights) and sum(weights)==1
 probabilities={}
 for label,p in zip(labels,weights):
  assert len(label)==2 and all(isinstance(v,int) and v in range(3) for v in label)
  label=tuple(label);probabilities[label]=probabilities.get(label,Q(0))+p
 return (1-sum(p*p for p in probabilities.values()))/128
def epsilon(i,j,k):
 if len({i,j,k})<3:return 0
 return 1 if (i,j,k) in [(0,1,2),(1,2,0),(2,0,1)] else -1
def extension_replay(rho):
 ext=exact.zeros(27)
 for j in range(3):
  for k in range(3):
   for r in range(3):
    for l in range(3):
     for m in range(3):
      for s in range(3):
       ext[9*j+3*k+r][9*l+3*m+s]=exact.sumq(exact.scale(rho[3*i+r][3*t+s],Q(epsilon(i,j,k)*epsilon(t,l,m),2)) for i in range(3) for t in range(3))
 checks=0
 for j in range(3):
  for r in range(3):
   for l in range(3):
    for s in range(3):
     expected=exact.sub(exact.q(Q(int(j==l and r==s),6)),exact.scale(rho[3*l+r][3*j+s],Q(1,2)))
     assert exact.sumq(ext[9*j+3*k+r][9*l+3*k+s] for k in range(3))==expected
     assert exact.sumq(ext[9*k+3*j+r][9*k+3*l+s] for k in range(3))==expected
     checks+=2
 for j in range(3):
  for k in range(3):
   for l in range(3):
    for m in range(3):
     assert exact.sumq(ext[9*j+3*k+r][9*l+3*m+r] for r in range(3))==exact.q(Q(int(j==l and k==m)-int(j==m and k==l),6))
     checks+=1
 return checks
def run():
 start=time.perf_counter();labels=[(0,0),(0,1),(0,2),(1,0),(1,1)]
 assert composition_receiver([(0,0),(0,0)],[Q(1,2),Q(1,2)])==0
 assert composition_receiver([(0,0),(0,1)],[Q(1,2),Q(1,2)])==Q(1,256)
 weights=[Q(v,79) for v in [64,8,4,2,1]];assert sum(weights)==1
 rho=exact.zeros(9)
 for (a,b),p in zip(labels,weights):
  bb=exact.bell(a,b)
  for i in range(9):
   for j in range(9):rho[i][j]=exact.add(rho[i][j],exact.scale(bb[i][j],p))
 for i in range(3):
  for k in range(3):
   assert exact.sumq(rho[3*i+j][3*k+j] for j in range(3))==exact.q(Q(int(i==k),3))
 extension_checks=extension_replay(rho)
 s=sum(p*p for p in weights);q=(1+3*s)/4
 universal=composition_receiver(labels,weights);assert universal>0
 lower=2*cert.lmin3(q)[0]-cert.hmax5(s)[1];assert lower>0
 coarse=Q((lower*1000).numerator//(lower*1000).denominator,1000)
 assert lower>=coarse>0
 maxbits=max(max(v.numerator.bit_length(),v.denominator.bit_length()) for row in rho for x in row for v in x)
 result={'labels':labels,'weights':[enc(p) for p in weights],
 'exact_rho_Qomega':[[[enc(a),enc(b)] for a,b in row] for row in rho],
 'rho_rank':5,'reference_dimension':3,'antisymmetric_extension_dimension':27,
 'exact_extension_partial_trace_components':extension_checks,
 'purity_weights':enc(s),'purity_SIC_output':enc(q),
 'raw_Delta_equals_CMI_excess':True,'CMI_excess_lower_exact':enc(coarse),
 'uniform_composition_receiver':enc(universal),
 'receiver_lower_exact':enc(lower),'receiver_lower_display':float(lower),
 'reduction_criterion_fails':max(weights)>Q(1,3),
 'Schmidt_number_three_witness':enc(max(weights)),
 'all_positive_eigenvalues_distinct':len(set(weights))==5,
 'source_field_entry_bit_length':maxbits,
 'receiver_rational_bit_length':max(lower.numerator.bit_length(),lower.denominator.bit_length()),
 'elapsed_seconds':time.perf_counter()-start}
 path=Path(__file__).resolve().parent/'outputs'/'SPARSE_BELL_SOURCE.json';path.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ['exact_rho_Qomega','receiver_lower_exact']},indent=2))
if __name__=='__main__':run()
