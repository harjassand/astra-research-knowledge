from pathlib import Path
from fractions import Fraction as F
import itertools,math,json,hashlib
import numpy as np
import sympy as s
ROOT=Path(__file__).parent
PA=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
def rat(x):return s.Rational(x.numerator,x.denominator)
def rotation(q):
 q=list(map(int,q));a,x,y,z=q;v=s.Matrix([x,y,z]);cross=s.Matrix([[0,-z,y],[z,0,-x],[-y,x,0]])
 return ((a*a-x*x-y*y-z*z)*s.eye(3)+2*v*v.T+2*a*cross)/sum(t*t for t in q)
def sqrt_upper(x,D):
 x=F(x);num=x.numerator*D*D;den=x.denominator;m=math.isqrt(num//den)
 while m*m*den<num:m+=1
 return F(m,D)
def bounds_for_N(N,design):
 D=design['rational_rounding_denominator'];t=F(design['Bernstein_log_upper_t']);eta=sqrt_upper(18*t/F(N),D)+F(20)*t/(3*N)
 h=F(3,4)*sqrt_upper(F(3),D)*eta
 return eta,h

def source_table():
 cfg=json.loads((ROOT/'SOURCE_ONLY.json').read_text());la=s.Rational(cfg['lambda']);ep=s.Rational(cfg['epsilon']);RL=rotation(cfg['logical_rotation_quaternion']);RG=rotation(cfg['gauge_rotation_quaternion'])
 assert RL.T*RL==s.eye(3) and RG.T*RG==s.eye(3)
 table={};den=1
 for j,si,a0,a1 in itertools.product(range(3),range(2),range(3),range(3)):
  sign=2*si-1;p=[]
  for og,ol in itertools.product([-1,1],repeat=2):
   p.append((1+ol*la*sign*RL[a1,j]+og*ep*sign*(1 if j==2 else 0)*RG[a0,2])/4)
  assert sum(p)==1 and min(p)>0
  table[j,si,a0,a1]=p
  for x in p:den=math.lcm(den,int(s.denom(x)))
 cdf=np.empty((3,2,3,3,4),dtype=np.int64)
 for key,p in table.items():cdf[key]=np.cumsum([int(x*den) for x in p])
 return cdf,den,cfg,RL,RG

def generate_bank(N,seed,cdf,den):
 rng=np.random.default_rng(seed);j=rng.integers(0,3,N);si=rng.integers(0,2,N);a0=rng.integers(0,3,N);a1=rng.integers(0,3,N);r=rng.integers(0,den,N)
 c=cdf[j,si,a0,a1];out=np.sum(r[:,None]>=c,axis=1)
 assert np.all(out<4)
 return np.column_stack([j,2*si-1,a0,a1,2*(out//2)-1,2*(out%2)-1]).astype(np.int8)

def exact_scores(count,N,design):
 # Receives only an observed integer contrast matrix, not source parameters.
 M=s.Matrix(3,3,lambda k,j:s.Rational(9*int(count[k,j]),N));m=np.array(M).astype(float)
 tr=np.trace(m);a=m
 K=np.array([[tr,a[2,1]-a[1,2],a[0,2]-a[2,0],a[1,0]-a[0,1]],
 [a[2,1]-a[1,2],a[0,0]-a[1,1]-a[2,2],a[0,1]+a[1,0],a[0,2]+a[2,0]],
 [a[0,2]-a[2,0],a[0,1]+a[1,0],a[1,1]-a[0,0]-a[2,2],a[1,2]+a[2,1]],
 [a[1,0]-a[0,1],a[0,2]+a[2,0],a[1,2]+a[2,1],a[2,2]-a[0,0]-a[1,1]]])
 _,v=np.linalg.eigh(K);qi=np.rint(v[:,-1]*design['candidate_quaternion_denominator']).astype(int);assert np.any(qi)
 Q=rotation(qi);assert Q.T*Q==s.eye(3) and Q.det()==1
 primal=s.trace(Q.T*M)
 H=sum((M[k,j]*s.kronecker_product(PA[j].T,PA[k])/2 for j in range(3) for k in range(3)),s.zeros(4))
 D=design['rational_rounding_denominator'];seed=float(np.linalg.eigvalsh(np.array(H).astype(complex))[-1]);y=s.Rational(math.ceil(seed*D)+2,D)
 def minors(y):
  W=y*s.eye(4)-H;out=[]
  for k in range(1,5):
   for inds in itertools.combinations(range(4),k):out.append(s.simplify(W.extract(inds,inds).det()))
  return out
 ms=minors(y);fallback=False
 if min(ms)<0:
  fallback=True;y=max(H[i,i]+sum(abs(s.re(H[i,j]))+abs(s.im(H[i,j])) for j in range(4) if j!=i) for i in range(4));ms=minors(y)
 assert all(x.is_real and x>=0 for x in ms)
 upper=2*y;assert primal<=upper
 return {'M_coefficients':[[str(M[k,j]) for j in range(3)] for k in range(3)],'candidate_quaternion_integers':list(map(int,qi)),'primal_objective_exact':str(primal),'dual_scalar_y_exact':str(y),'dual_objective_exact':str(upper),'all_15_dual_principal_minors_exact':list(map(str,ms)),'dual_PSD_exact':True,'primal_rotation_exact_SO3':True,'dual_fallback_used':fallback,'empirical_primal_dual_gap':float(upper-primal)},primal,upper

def learner(records,design):
 # This function has no source configuration, rotation, swap or generator access.
 N=len(records);counts=np.zeros((2,3,3),dtype=np.int64)
 for site in range(2):np.add.at(counts[site],(records[:,2+site],records[:,0]),records[:,1].astype(np.int64)*records[:,4+site])
 eta,h=bounds_for_N(N,design);out=[]
 for site in range(2):
  witness,p,u=exact_scores(counts[site],N,design)
  lo=max(s.Rational(0),(1+p)/4-rat(h));hi=min(s.Rational(1),(1+u)/4+rat(h));assert lo<=hi
  witness.update({'physical_site':site,'integer_signed_counts':counts[site].tolist(),'fidelity_lower_exact':str(lo),'fidelity_upper_exact':str(hi),'fidelity_interval':[float(lo),float(hi)]});out.append(witness)
 accepted=[i for i in range(2) if s.Rational(out[i]['fidelity_lower_exact'])>s.Rational(out[1-i]['fidelity_upper_exact'])]
 assert len(accepted)<=1
 return {'calls':N,'coefficient_radius_upper_exact':str(eta),'score_halfwidth_upper_exact':str(h),'score_halfwidth_upper':float(h),'accepted_site':accepted[0] if accepted else None,'guard_status':'ACCEPT' if accepted else 'ABSTAIN','site_witnesses':out},counts

def main():
 design=json.loads((ROOT/'PREDECLARED_DESIGN.json').read_text());design_hash=hashlib.sha256((ROOT/'PREDECLARED_DESIGN.json').read_bytes()).hexdigest()
 # Exact verification that chosen t upper bounds the required logarithm.
 e9lower=sum(F(9)**k/F(math.factorial(k)) for k in range(21));assert e9lower>2*design['coefficient_count_M']/F(design['confidence_beta_per_bank'])
 cdf,den,cfg,RL,RG=source_table();reports=[]
 for bank in design['banks']:
  records=generate_bank(bank['calls'],bank['seed'],cdf,den);r,counts=learner(records,design)
  np.savez_compressed(ROOT/(bank['name']+'_records.npz'),records=records,integer_signed_counts=counts)
  r.update({'name':bank['name'],'seed':bank['seed'],'records_sha256':hashlib.sha256(records.tobytes()).hexdigest(),'source_parameters_used_by_learner':False})
  (ROOT/(bank['name']+'_certificate.json')).write_text(json.dumps(r,indent=2)+'\n');reports.append(r)
 validation={'physical_source_parameters_for_validation_only':cfg,'exact_joint_probability_denominator':den,'all_settings_positive':True,'normalized_Choi_lower_bound':'1/80','global_normal_cone_gap':'3/4','logical_true_oracle_fidelity':'17/20','gauge_true_oracle_fidelity':'11/40','logical_rotation_exact':[[str(x) for x in row] for row in RL.tolist()],'gauge_rotation_exact':[[str(x) for x in row] for row in RG.tolist()]}
 (ROOT/'SOURCE_VALIDATION.json').write_text(json.dumps(validation,indent=2)+'\n')
 summary={'status':'EXECUTED_ORDINARY_COMMON_BANK_DEMO','design_sha256_before_sampling':design_hash,'actual_individually_sampled_source_calls':sum(x['calls'] for x in reports),'physical_Pauli_readouts':2*sum(x['calls'] for x in reports),'independent_banks':len(reports),'declared_total_failure_budget':design['total_union_failure_budget'],'exact_probability_denominator':den,'summary':[{'name':r['name'],'calls':r['calls'],'halfwidth':r['score_halfwidth_upper'],'guard':r['guard_status'],'accepted_site':r['accepted_site'],'intervals':[x['fidelity_interval'] for x in r['site_witnesses']]} for r in reports],'scope':'Stationary finite source simulation; exact rational empirical primal/dual and outward confidence radii. No hardware, compiler, generic future-memory or overall practical advantage claim.'}
 (ROOT/'RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
