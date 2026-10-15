import json, ast, math, time, hashlib, sys
from fractions import Fraction as F
from pathlib import Path
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent/'heterogeneous'; t=time.time()
j=json.loads((p/'dyadic128_exact.json').read_text());c=json.loads((p/'mixture_certificate.json').read_text());law=json.loads((p/'compact_law.json').read_text())
ns={'Fraction':F,'math':math};tree=ast.parse((p/'dyadic.py').read_text());tree.body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in ('floor_rate','compile_hist')];exec(compile(tree,'audit','exec'),ns)
k,counts,shift,b=ns['compile_hist'](128,.05)
assert k==list(map(int,j['rates'])) and counts==list(map(int,j['counts'])) and shift==j['shift'] and b==j['b']
D=int(c['root_denominator']);W=int(c['weight_denominator']);S=1<<c['evaluation_precision']; rows=c['intervals'];assert len({r['root_index'] for r in rows})==len(rows)
sl=sh=0
for row in rows:
 a=int(row['lower_numerator']); bb=int(row['upper_numerator']);ix=row['root_index']; assert (0 if ix==0 else k[ix-1]*D)<a<bb<k[ix]*D
 def fbound(z):
  zsum=sum((z*ct*S)//(kk*D-z) for kk,ct in zip(k,counts));return zsum,zsum+len(k)
 assert fbound(a)[1]<S and fbound(bb)[0]>S
 dl=du=0
 for kk,ct in zip(k,counts):
  d1=kk*D-a;d2=kk*D-bb;assert d1*d2>0
  dl+=(a*D*ct*kk*S)//max(d1*d1,d2*d2)
  du+=(bb*D*ct*kk*S)//min(d1*d1,d2*d2)+1
 l=(S*W)//du;h=-((-S*W)//dl)
 assert l==int(row['weight_lower_numerator']) and h==int(row['weight_upper_numerator']);sl+=l;sh+=h
q=F(1,1<<128);res=1-q-F(sl,W)
assert res==F(int(law['coupling_failure_upper']['numerator']),int(law['coupling_failure_upper']['denominator']))
probs=list(map(int,law['positive_probability_numerators']));assert sum(probs)+1==1<<128
for idx,row in enumerate(rows):
 a=int(row['lower_numerator']);bb=int(row['upper_numerator']);rate=F(int(law['rates'][idx]['numerator']),int(law['rates'][idx]['denominator']));assert rate==F(a+bb,2*D*(1<<shift))
 assert probs[idx]==int(row['weight_lower_numerator'])*(1<<(128-80))+(int(res*(1<<128)) if idx==0 else 0)
rel=max(F(int(x['upper_numerator'])-int(x['lower_numerator']),int(x['lower_numerator'])) for x in rows)
total=(1+F(1,1<<(b-1)))**129*(1+rel)-1
assert total==F(int(law['total_relative_error_bound']['numerator']),int(law['total_relative_error_bound']['denominator']))
print(json.dumps(dict(verified=True,bins=len(k),rows=len(rows),n=128,shift=shift,b=b,mass_lower=float(F(sl,W)),mass_upper=float(F(sh,W)),residual=float(res),relative=float(total),seconds=time.time()-t,law_sha256=hashlib.sha256((p/'compact_law.json').read_bytes()).hexdigest()),indent=2))
