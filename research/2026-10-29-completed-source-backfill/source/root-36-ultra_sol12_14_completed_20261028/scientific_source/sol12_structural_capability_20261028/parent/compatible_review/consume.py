"""Independent consumer of new contact Grams and global inverse bounds."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
import runpy,json,math,time
OUT=Path(__file__).resolve().parent;SRC=OUT.parents[1]/'convex_capability'
h=runpy.run_path(str(OUT.parents[2]/'sol11_operation_discovery_20261028/parent/normal_strip/certify.py'))
inputs,ldl,bs,gp,add,sc,mon=[h[k] for k in ['inputs','ldl','bs','gp','add','sc','mon']]
F,p,q,T=inputs()
def val(poly,a):return sum((c*math.prod(t**n for t,n in zip(a,e)) for e,c in poly.items()),Q(0))
def der(poly,i):
 out={}
 for e,c in poly.items():
  if e[i]:
   f=list(e);f[i]-=1;out[tuple(f)]=c*e[i]
 return out
DF=[der(F,i) for i in range(4)]
def jet(a):
 t=val(T,a);k=val(p,a)/(t*t) if t else Q(0);cof=[a[3],-a[2],-a[1],a[0]]
 return [val(df,a)-k*c for df,c in zip(DF,cof)]+[k]
def translate(poly,a):
 out={}
 for e,c in poly.items():
  for k in product(*(range(t+1) for t in e)):
   v=c*math.prod(math.comb(t,h)*a[i]**(t-h) for i,(t,h) in enumerate(zip(e,k)))
   out[k]=out.get(k,Q(0))+v
 return {e:c for e,c in out.items() if c}
start=time.perf_counter();raw=json.loads((SRC/'INVERSE_RESULT.json').read_text())
data=list(map(Q,raw['data']));nu=Q(raw['known_noise_l1'])
assert sum(abs(x-y) for x,y in zip(data,jet([Q(1),Q(0),Q(0),Q(1)])))<=nu
rows=[]
for trial in raw['trials']:
 a=list(map(Q,trial['proposal']));t=val(T,a);ka=val(p,a)/(t*t)
 target={ex:c for ex,c in translate(F,a).items() if sum(ex)>=2}
 target=add(target,sc(-ka,q));contact=trial['contact'];den=int(contact['Gram_denominator'])
 g=[[Q(v,den) for v in row] for row in contact['Gram_numerators']]
 assert gp(g,bs(1)+bs(2))==target
 mu=Q(contact['mu']);g0=[[v-(mu if i==j and i<4 else 0) for j,v in enumerate(row)] for i,row in enumerate(g)]
 pivot=ldl(g0,Q(0));residual=sum(abs(x-y) for x,y in zip(jet(a),data))
 for key in ['new_receiver','matched_coarse_receiver']:
  c=trial[key];rho=Q(c['rho']);cc=Q(c['C']);mmu=Q(c['mu']);b=Q(c['global_quartic_margin'])
  assert rho==residual+nu and cc*cc>=1+t and cc>0
  if key=='matched_coarse_receiver':assert mmu==t/2400000
  else:assert mmu==mu
  upper=Q(c['state_error_upper']);assert upper*(mmu+b*upper*upper)/(cc+upper/2)>=rho
 rows.append({'seed':trial['seed_name'],'identity':'ALL_COEFFICIENTS_PASS','PD_margin':str(mu),'exact_LDL':'PASS','global_noisy_bounds':'PASS'})
# Exact stress-only ambiguity polynomial, independent of root/interval choices.
Sa=val(DF[0],[Q(1),Q(0),Q(0),Q(1)]);Sd=val(DF[3],[Q(1),Q(0),Q(0),Q(1)])
def diagpoly(poly):
 o=[Q(0)]*4
 for e,c in poly.items():
  if not e[1] and not e[2]:o[e[3]]+=c
 return o
pa,pr=diagpoly(DF[0]),diagpoly(DF[3]);actual=[Sa*y-Sd*x for x,y in zip(pa,pr)]
aa,bb,cc=map(Q,raw['stress_ambiguity']['ratio_quadratic_coefficients']);factor=[-cc,cc-bb,bb-aa,aa];scale=actual[3]/aa
assert actual==[scale*v for v in factor]
out={'status':'INDEPENDENT_CONTACT_AND_INVERSE_REPLAY_PASSED','trials':rows,'data_noise_promise':'EXACT','stress_ambiguity_cubic_factor':'EXACT_INDEPENDENT_RECONSTRUCTION','seconds':time.perf_counter()-start,'scope':'Two exact14-Gram identities/PD bounds and noisy global receivers; uses accepted historical180 proof. No producer imports. Stress cubic factor checked, not a new physical-data acquisition or general inverse proposal solver.'}
(OUT/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
