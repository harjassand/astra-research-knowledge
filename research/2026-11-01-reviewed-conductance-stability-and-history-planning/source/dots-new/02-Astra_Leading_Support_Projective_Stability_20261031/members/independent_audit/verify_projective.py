#!/usr/bin/env python3
"""Independent exact polynomial/cone/support verifier. Candidate code proposes only."""
from fractions import Fraction as F
from itertools import combinations,product
from math import factorial,comb,prod,ceil
from pathlib import Path
import importlib.util,json,copy,hashlib
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('candidate',HERE/'frozen_projective_mass.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
CACHE={}

def comps(N,n):
 if n==1:yield (N,)
 else:
  for a in range(N+1):
   for z in comps(N-a,n-1):yield(a,)+z

def poly(x):return {tuple(r['exponent']):F(r['coefficient']) for r in x} if isinstance(x,list) else {tuple(a):F(c) for a,c in x.items()}
def add(a,b):
 r=dict(a)
 for u,c in b.items():r[u]=r.get(u,F(0))+c
 return {u:c for u,c in r.items() if c}
def mul(a,b):
 r={}
 for u,c in a.items():
  for v,d in b.items():
   w=tuple(x+y for x,y in zip(u,v));r[w]=r.get(w,F(0))+c*d
 return {u:c for u,c in r.items() if c}
def scale(a,c):return {u:v*c for u,v in a.items() if v*c}
def ffpoly(u):
 n=len(u);r={(0,)*n:F(1)}
 for j,a in enumerate(u):
  e=tuple(int(i==j) for i in range(n))
  for k in range(a):r=mul(r,{e:F(1),(0,)*n:-F(k)} if k else {e:F(1)})
 return r
def shiftmono(u,nu):
 out={}
 for z in product(*(range(a+1) for a in u)):
  c=prod(F(comb(a,b))*v**(a-b) for a,b,v in zip(u,z,nu))
  if c:out[z]=c
 return out
def ff(x,u):
 if any(a<b for a,b in zip(x,u)):return 0
 return prod(prod(range(a-b+1,a+1)) for a,b in zip(x,u))
def ev(poly,x):return sum(c*prod(F(v)**a for v,a in zip(x,u)) for u,c in poly.items())
def solver(A,b):
 n=len(b);M=[list(map(F,r))+[F(y)] for r,y in zip(A,b)]
 for j in range(n):
  k=next((i for i in range(j,n) if M[i][j]),None)
  if k is None:return None
  M[j],M[k]=M[k],M[j]
  for i in range(j+1,n):
   fac=M[i][j]/M[j][j]
   if fac:M[i]=[x-fac*y for x,y in zip(M[i],M[j])]
 x=[F(0)]*n
 for i in range(n-1,-1,-1):x[i]=(M[i][-1]-sum(M[i][j]*x[j] for j in range(i+1,n)))/M[i][i]
 return x

def unpack(rec):
 assert rec['accepted'];n=len(rec['species']);A=rec['pivot'];J=list(rec['satellites'])
 assert n>=2 and J==[i for i in range(n) if i!=A]
 raw=[(tuple(u),tuple(v),F(k)) for u,v,k in rec['reactions']]
 assert all(len(u)==len(v)==n and all(type(z)==int and z>=0 for z in u+v) and k>0 for u,v,k in raw)
 adj={u:set() for u,v,k in raw}|{v:set() for u,v,k in raw}
 for u,v,k in raw:adj[u].add(v)
 for u,v,k in raw:
  seen={v};todo=[v]
  while todo:
   z=todo.pop()
   for w in adj[z]:
    if w not in seen:seen.add(w);todo.append(w)
  assert u in seen
 zero=(0,)*n;unit=tuple(int(i==A) for i in range(n));lam=death=F(0);internal=[]
 for u,v,k in raw:
  if (u,v)==(zero,unit):lam+=k
  elif (u,v)==(unit,zero):death+=k
  else:assert sum(u)==sum(v);internal.append((u,v,k))
 assert lam==F(rec['immigration'])>0 and death==F(rec['death'])>0
 assert internal==[(tuple(u),tuple(v),F(k)) for u,v,k in rec['internal']]
 order=max([2]+[sum(u) for u,v,k in internal]);assert order==rec['leading_order']
 return n,A,J,raw,internal,lam,death,order

def support(rec,sw):
 n,A,J,raw,internal,lam,death,order=unpack(rec);leading=[(i,u,v,k) for i,(u,v,k) in enumerate(internal) if sum(u)==order]
 trials=[];checks=0;failed=None
 for seed in range(n):
  S={seed};steps=[]
  while A not in S:
   growth=None
   for i,u,v,k in leading:
    checks+=1
    if all(not z or j in S for j,z in enumerate(u)):
     new={j for j,z in enumerate(v) if z}-S
     if new:growth=(i,new);break
   if growth is None:break
   i,new=growth;steps.append({'internal_row':i,'before':sorted(S),'added':sorted(new)});S|=new
  trials.append({'seed':seed,'support':sorted(S),'steps':steps,'reaches_open_species':A in S})
  if A not in S:failed=S;break
 assert sw['trials']==trials and sw['support_reaction_tests']==checks and sw['leading_order']==order
 assert sw['accessible']==(failed is None)
 if failed is not None:
  assert sw['closed_face_support']==sorted(failed) and sw['all_degree_strict_cone_impossible'] and sw['network_stability']=='UNKNOWN'
  return False
 if 'norm_bound_C' not in sw:return True
 S=sum(k for i,u,v,k in leading);km=min(k for i,u,v,k in leading);C=max(F(1),order**3*S);T=1/(4*C);lev=[F(3,4*n)]
 for _ in range(n):lev.append(min(lev[-1],T*km*lev[-1]**order/(4*n)))
 delta=lev[-1];M=n*max(1,ceil(3*C**3*T**3/(n*delta)));err=3*C**3*T**3/(2*M)
 for key,value in {'norm_bound_C':C,'time_T':T,'minimum_leading_rate':km,'leading_rate_sum':S,'terminal_A_lower_delta':delta,'Euler_step_h':T/M,'directional_Taylor_error_upper':err,'boundary_derivative_margin':delta/(2*T)}.items():assert F(sw[key])==value
 assert list(map(F,sw['support_lower_levels']))==lev and sw['Euler_steps_M']==M and err<=delta/2
 formal=sw['formal_initial_polynomial_degree'];assert formal['base']==order and formal['exponent']==M-1 and formal['degree_integer_bit_upper']==order.bit_length()*(M-1)+1
 assert sw['formal_construction_executed'] is False
 return True

def build(rec,d):
 n,A,J,raw,internal,lam,death,order=unpack(rec);q=d+order-1;variables=list(comps(d,n));dim=len(variables)+1;gens={};multi={}
 for alpha in variables:
  multi[alpha]=F(factorial(d),prod(factorial(z) for z in alpha));g={}
  for u,v,k in internal:
   delta=add(shiftmono(alpha,tuple(y-x for x,y in zip(u,v))),{alpha:-F(1)})
   g=add(g,scale(mul(ffpoly(u),delta),k*multi[alpha]))
  gens[alpha]=g;assert all(sum(a)<=q for a in g)
 rows=[]
 def put(label,f):
  f=list(map(F,f))
  if any(f):rows.append((label,f))
 for i,a in enumerate(variables):
  f=[F(0)]*(dim+1);f[i]=-1;put(['coefficient_lower',list(a)],f)
  f=[F(0)]*(dim+1);f[i]=1;f[-1]=-1;put(['coefficient_upper',list(a)],f)
 forms=[]
 for b in comps(q,len(J)):
  a=[0]*n
  for i,z in zip(J,b):a[i]=z
  a=tuple(a);forms.append((a,[gens[z].get(a,F(0)) for z in variables]+[F(0),F(0)]))
 upper=max([F(1)]+[sum(abs(x) for x in form) for a,form in forms if max(a)==q])
 f=[F(0)]*(dim+1);f[-2]=-1;put(['beta_lower'],f)
 f=[F(0)]*(dim+1);f[-2]=1;f[-1]=-upper;put(['beta_upper'],f)
 for a,form in forms:
  f=[-x for x in form]
  if max(a)==q:f[-2]=1
  put(['pure_boundary' if max(a)==q else 'mixed_boundary',list(a)],f)
 assert all(sum(f[:-2])+f[-1]<=0 for label,f in rows)
 return variables,multi,gens,rows,q

def acquire_independent(rec,d):
 key=(repr(rec['internal']),rec['pivot'],d)
 if key in CACHE:return CACHE[key]
 var,multi,gens,rows,q=build(rec,d);dim=len(var)+1;attempts=nonsing=bits=0;found=None
 for basis in combinations(range(len(rows)),dim):
  attempts+=1;forms=[rows[i][1] for i in basis];x=solver([f[:-1] for f in forms],[-f[-1] for f in forms])
  if x is None:continue
  nonsing+=1;bits=max(bits,max(max(z.numerator.bit_length(),z.denominator.bit_length()) for z in x))
  if x[-1]<=0:continue
  res=[sum(a*b for a,b in zip(f[:-1],x))+f[-1] for label,f in rows]
  if max(res)<=0:found=(basis,x,res);break
 out={'var':var,'multi':multi,'gens':gens,'rows':rows,'q':q,'found':found,'attempts':attempts,'nonsingular':nonsing,'bits':bits,'total':comb(len(rows),dim)};CACHE[key]=out;return out

def verify(rec,cert):
 assert cert['accepted'];n,A,J,raw,internal,lam,death,order=unpack(rec);assert support(rec,cert['support_certificate'])
 d=cert['degree'];q=d+order-1;assert cert['leading_order']==order and cert['denominator_degree']==q-1
 prior=cert['prior_degree_trials'];assert len(prior)==d-1;total=0
 for i,r in enumerate(prior,1):
  z=acquire_independent(rec,i);assert z['found'] is None and r['algebraic_cone_exhausted'] and not r['accepted'] and r['degree']==i
  assert r['basis_attempts']==z['attempts']==z['total'] and r['total_candidate_bases']==z['total'] and r['nonsingular_bases']==z['nonsingular'];total+=z['attempts']
 z=acquire_independent(rec,d);ac=cert['acquisition'];basis,x,res=z['found'];assert ac['accepted'] and ac['degree']==d
 rows=[(r['label'],list(map(F,r['form']))) for r in ac['constraints']]
 assert rows==z['rows'];assert tuple(ac['active_basis'])==basis and list(map(F,ac['basis_solution']))==x and list(map(F,ac['exact_residuals']))==res
 assert ac['basis_attempts']==z['attempts'] and ac['nonsingular_bases']==z['nonsingular'] and ac['total_candidate_bases']==z['total'] and ac['largest_solved_fraction_bits']==z['bits']
 assert cert['total_basis_attempts']==total+z['attempts'] and ac['LP_dimension']==len(z['var'])+1
 coefficients=dict(zip(z['var'],x[:-1]));assert poly(ac['bernstein_coefficients'])==coefficients
 H={};LH={}
 for a,c in coefficients.items():H=add(H,{a:c*z['multi'][a]});LH=add(LH,scale(z['gens'][a],c))
 H={a:c for a,c in H.items() if c};G={a:c for a,c in LH.items() if sum(a)==q};rem={a:c for a,c in LH.items() if sum(a)<q}
 assert poly(ac['H'])==H and poly(ac['LH'])==LH and poly(ac['G'])==G and poly(ac['remainder'])==rem
 K=sum(-c for a,c in G.items() if a[A] and c<0);CR=sum(abs(c) for c in rem.values());beta=x[-1]
 assert F(ac['K'])==K and F(ac['remainder_bound'])==CR and F(ac['beta'])==beta>0
 assert all(0<=c<=1 for c in coefficients.values()) and all(c>=0 for a,c in G.items() if not a[A])
 assert all(G.get(tuple(q*int(i==j) for i in range(n)),F(0))>=beta for j in J)
 work=ac['formal_work'];assert work['homogeneous_basis_polynomials']==len(z['var']) and work['raw_internal_channels']==len(internal)
 assert work['generator_nonzero_monomials']==sum(len(g) for g in z['gens'].values())
 assert work['largest_generator_coefficient_bits']==max([0]+[max(c.numerator.bit_length(),c.denominator.bit_length()) for g in z['gens'].values() for c in g.values()])
 assert work['formal_multiplication_term_pairs']>0
 t=F(cert['t']);D=death*(1-1/t);eps=min(F(1,2),D/(4*K)) if K else F(1,2);m=len(J)
 C=lam*(t/(1-eps)-1)+death*eps*d/(t*(1-eps))+eps*CR/(1-eps);kap=min(D/4,eps*beta/(2**(2*d+2*order-3)*m**(d+order-2)));R=max(1,ceil((C+kap)/kap))
 assert t>1 and F(cert['epsilon'])==eps and F(cert['death_exponential_coefficient'])==D and F(cert['C0'])==C and F(cert['kappa'])==kap and cert['R']==R
 assert cert['finite_exception_count_upper']==comb(R+n-1,n)
 cf=cert['foster_constant'];co=C+kap;nb=co.numerator.bit_length()+R*t.numerator.bit_length();db=co.denominator.bit_length()+R*t.denominator.bit_length()
 assert F(cf['coefficient'])==co and F(cf['base'])==t and cf['exponent']==R and cf['unreduced_numerator_bits_upper']==nb and cf['unreduced_denominator_bits_upper']==db
 assert cf['serialization_bit_cap']==12000 and cf['expanded']==(max(nb,db)<=min(cf['requested_expansion_bit_cap'],12000))
 if cf['expanded']:assert F(cf['value'])==co*t**R
 else:assert 'value' not in cf
 def h(x):return 1-eps*ev(H,x)/F((sum(x)+1)**(q-1))
 def quotient(x):
  N=sum(x);hh=h(x);assert 1-eps<=hh<=1 and 0<=ev(H,x)<=N**d;out=lint=internalquot=F(0)
  for u,v,k in raw:
   rate=k*ff(x,u)
   if not rate:continue
   y=tuple(a-b+c for a,b,c in zip(x,u,v));value=rate*(t**(sum(v)-sum(u))*h(y)/hh-1);out+=value
   if sum(u)==sum(v):lint+=rate*(ev(H,y)-ev(H,x));internalquot+=value
  assert lint==ev(LH,x) and internalquot==-eps*lint/(F((N+1)**(q-1))*hh)
  assert lint>=beta*sum(x[j]**q for j in J)-K*x[A]*N**(q-1)-CR*(N+1)**(q-1)
  mid=C-D*x[A]/2-eps*beta*sum(x[j] for j in J)**q/F(m**(q-1)*(N+1)**(q-1))
  assert out<=mid<=C-kap*N
  return out
 return quotient,H

def check_case(label,rec,cert,limit=14):
 rec=p.clean(rec);cert=p.clean(cert) # Normalize newly proposed in-memory receipts to the JSON wire format.
 f,H=verify(rec,cert);n=len(rec['species']);A=rec['pivot'];J=rec['satellites'];count=0
 for N in range(limit+1):
  for x in comps(N,n):f(x);count+=1
 huge=0
 for N in [cert['R']-1,cert['R'],cert['R']+1,10**6,10**50]:
  points=[tuple(N*int(i==j) for i in range(n)) for j in range(n)]
  z=[0]*n;z[A]=1;z[J[-1]]=N-1;points.append(tuple(z));points.append(tuple(N//n+int(i<N%n) for i in range(n)))
  for x in points:f(x);huge+=1
 return {'case':label,'degree':cert['degree'],'p':rec['leading_order'],'total_basis_attempts':cert['total_basis_attempts'],'ordinary_checks':count,'huge_checks':huge,'H':[{'exponent':a,'coefficient':str(c)} for a,c in sorted(H.items())]}

def main():
 original=json.loads((HERE/'frozen_results.json').read_text());rec=original['recognition'];cert=original['certificate'];cases=[check_case('frozen_demo',rec,cert)]
 exercise=json.loads((HERE/'frozen_exercise_results.json').read_text())
 for row in exercise['cases']:cases.append(check_case(row['label'],row['raw_recognition'],row['certificate']))
 # Independent additional molecularity: fourth-order reversible loss/restoration.
 z=(0,0);A=(1,0);BBBB=(0,4);ABBB=(1,3)
 rn=p.recognize(['A','B'],[(z,A,F(2,3)),(A,z,F(7,5)),(BBBB,ABBB,F(3,7)),(ABBB,BBBB,F(5,2))]);cn=p.construct(rn,max_degree=1)
 cases.append(check_case('independent_fourth_order_two_species',rn,cn,limit=20))
 # Permutation forces raw role reacquisition, not a supplied A position.
 sp,raw=p.demo_network();perm=(2,0,1);rp=p.recognize([sp[i] for i in perm],[(tuple(u[i] for i in perm),tuple(v[i] for i in perm),k) for u,v,k in raw]);cp=p.construct(rp)
 cases.append(check_case('independent_species_permutation',rp,cp,limit=10))
 bad=[]
 for kind in ['H','LH','G','remainder','Bernstein','constraint','residual','basis','beta','K','remainder_bound','denominator_degree','formal_M','formal_degree','Foster_coefficient','bit_bound']:
  c=copy.deepcopy(cert)
  if kind in ['H','LH','G','remainder']:c['acquisition'][kind][0]['coefficient']=str(F(c['acquisition'][kind][0]['coefficient'])+1)
  elif kind=='Bernstein':c['acquisition']['bernstein_coefficients'][0]['coefficient']='2'
  elif kind=='constraint':c['acquisition']['constraints'][0]['form'][0]='0'
  elif kind=='residual':c['acquisition']['exact_residuals'][0]='99'
  elif kind=='basis':c['acquisition']['active_basis'][0]=c['acquisition']['active_basis'][1]
  elif kind in ['beta','K']:c['acquisition'][kind]='0'
  elif kind=='remainder_bound':c['acquisition'][kind]='0'
  elif kind=='denominator_degree':c[kind]+=1
  elif kind=='formal_M':c['support_certificate']['Euler_steps_M']-=1
  elif kind=='formal_degree':c['support_certificate']['formal_initial_polynomial_degree']['exponent']+=1
  elif kind=='Foster_coefficient':c['foster_constant']['coefficient']='0'
  else:c['foster_constant']['unreduced_numerator_bits_upper']=1
  try:verify(rec,c)
  except AssertionError:bad.append(kind)
  else:raise AssertionError('tamper accepted '+kind)
 support(exercise['stable_quadratic_obstruction']['support_certificate'] and p.recognize(['A','B','C'],[((0,0,0),(1,0,0),1),((1,0,0),(0,0,0),1),((1,0,0),(0,1,0),1),((0,1,0),(1,0,0),1),((1,0,0),(0,0,1),1),((0,0,1),(1,0,0),1),((0,2,0),(0,0,2),1),((0,0,2),(0,2,0),1)]),exercise['stable_quadratic_obstruction']['support_certificate'])
 assert not exercise['basis_budget_receipt']['accepted'] and exercise['basis_budget_receipt']['explicit_certificate_status']=='UNKNOWN' and exercise['basis_budget_receipt']['basis_attempts']==330
 assert not exercise['degree_budget_receipt']['accepted'] and exercise['degree_budget_receipt']['explicit_certificate_status']=='UNKNOWN'
 print(json.dumps({'source_sha256':hashlib.sha256((HERE/'frozen_projective_mass.py').read_bytes()).hexdigest(),'independent_basis_and_raw_polynomial_verification':True,'cases':cases,'rejected_receipt_tampers':bad,'budget_UNKNOWN_and_all_degree_obstruction_scope_verified':True,'finite_tests_supplement_ordinary_proof':True},indent=2))
if __name__=='__main__':main()
