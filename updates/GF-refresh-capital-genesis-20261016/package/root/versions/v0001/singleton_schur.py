"""Exact rational singleton Schur certificate; no full matrix in production."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json,time,resource,hashlib

def certify(etas,p,q,h):
 etas=list(map(F,etas));p,q,h=map(F,(p,q,h));a=p*q
 assert etas and all(0<=x<1 for x in etas) and 0<p<1 and 0<q<1 and h>0 and h*h==a*(1-p)*(1-q)
 t=h/a;order=sorted(range(len(etas)),key=lambda j:etas[j],reverse=True);A0=A1=A2=F(0);found=None
 for ell,j in enumerate(order,1):
  e=etas[j]
  if not e:break
  d=1-e*e;A0+=1/d;A1+=e/d;A2+=e*e/d;D=(1+A2)*A0-A1*A1;assert D>0
  tau=(t*A0-A1)/D;mu=(t*A1-(1+A2))/D
  if tau<=0 or mu<=0:continue
  k=mu/tau;next_eta=etas[order[ell]] if ell<len(order) else F(0)
  if e>=k>=next_eta:
   found=(ell,tau,mu,k);break
 if not found:return {'status':'UNRESOLVED','reason':'No positive-multiplier binding singleton prefix; no full optimizer claimed.'}
 ell,tau,mu,k=found;active=order[:ell];v=[F(0)]*len(etas)
 for j in active:v[j]=(tau*etas[j]-mu)/(1-etas[j]**2)
 assert sum(v)==1 and all(x>=0 for x in v)
 s=sum((e*x for e,x in zip(etas,v)),F(0));assert tau==t-s
 prod=F(1);invsum=F(0);G=[]
 for count,j in enumerate(active,1):
  prod*=etas[j];invsum+=1/etas[j];G.append(prod*(1-count+k*invsum))
 M=max([k]+[-x for x in G]);quad=s*s+sum(((1-e*e)*x*x for e,x in zip(etas,v)),F(0));Q=p+q-p*q
 lo=Q+2*h*s-a*quad;upper=Q+a*quad+2*a*tau*M;gap=2*a*tau*(M-k);assert upper-lo==gap
 return {'status':'EXACT' if gap==0 else 'CERTIFIED_BRACKET','lower':lo,'upper':min(F(1),upper),'raw_tangent_upper':upper,'tangent_gap':gap,'v':v,'active_indices':active,'tau':tau,'mu':mu,'k':k,'G':G,'gradient_infinity_norm':a*tau*M,'m':len(etas)}

def exhaustive_gradient(etas,p,q,h,r):
 # Independent finite diagnostic: construct every nonempty coordinate by XOR.
 etas=list(map(F,etas));m=len(etas);a=F(p)*F(q);s=F(0);mx=F(0);badmask=None
 for mask in range(1,1<<m):
  c=F(1)
  for j,e in enumerate(etas):
   if mask>>j&1:c*=e
  bv=F(0)
  for j,x in enumerate(r['v']):
   if not x:continue
   b=F(1);xor=mask^(1<<j)
   for k,e in enumerate(etas):
    if xor>>k&1:b*=e
   bv+=b*x
  val=abs(F(h)*c-a*bv)
  if val>mx:mx=val;badmask=mask
 assert mx==r['gradient_infinity_norm'],(etas,mx,r)
 return {'coordinates_checked':(1<<m)-1,'exact_norm':str(mx),'maximizing_mask':badmask}

def serial(v):
 if isinstance(v,F):return str(v)
 if isinstance(v,dict):return {k:serial(x) for k,x in v.items()}
 if isinstance(v,list):return list(map(serial,v))
 return v

def main():
 start=time.perf_counter();cpu=time.process_time();checks=[]
 for m in range(1,8):
  families=[[F(1,4)]*m,[F(j+1,4*m+1) for j in range(m)],[F(4,5)]*m,[F(1,3) if j%2 else F(2,3) for j in range(m)]]
  for etas in families:
   for p in [F(1,4),F(1,20),F(2,5)]:
    r=certify(etas,p,p,p*(1-p))
    if r['status']=='UNRESOLVED':checks.append({'m':m,'status':'UNRESOLVED'});continue
    checks.append({'m':m,'status':r['status'],'check':exhaustive_gradient(etas,p,p,p*(1-p),r)})
 cases=[]
 for name,etas,p in [('source32',[F(1,4)]*32,F(1,4)),('unequal128',[F(j+1,512) for j in range(128)],F(1,4)),('fails_singleton',[F(4,5)]*8,F(2,5))]:
  r=certify(etas,p,p,p*(1-p));cases.append({'case':name,'etas':list(map(str,etas)),'p':str(p),'q':str(p),'h':str(p*(1-p)),'result':serial(r)})
 assert cases[0]['result']['status']=='EXACT' and F(cases[0]['result']['lower'])==F(4305,8192)
 assert cases[1]['result']['status']=='EXACT'
 receipt={'schema':'astra.gf-singleton-schur.v1','status':'EXACT_CHECKS_PASS','checks':checks,'cases':cases,'wall_seconds':time.perf_counter()-start,'local_process_CPU_seconds':time.process_time()-cpu,'peak_process_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Exact finite algebra diagnostics and compressed certificates under analytic theorem. No physical model, prior novelty or general algorithmic superiority validation.'}
 (Path(__file__).parent/'SINGLETON_SCHUR_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'status':receipt['status'],'finite_checks':len(checks),'cases':[(x['case'],x['result']['status'],x['result'].get('lower'),x['result'].get('upper')) for x in cases],'wall_seconds':receipt['wall_seconds']}))
if __name__=='__main__':main()
