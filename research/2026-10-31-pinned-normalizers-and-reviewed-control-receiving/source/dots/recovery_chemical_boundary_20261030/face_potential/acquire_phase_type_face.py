"""Acquire a local catalytic phase-type face from raw rational reaction lists."""
import json
from fractions import Fraction
from pathlib import Path
import sympy as S

def acquire(raw):
 if not isinstance(raw,list) or not raw:return dict(status='INVALID_INPUT')
 try:
  for r in raw:
   for side in ['source','target']:
    if not isinstance(r[side],dict) or any(not isinstance(n,str) or not isinstance(v,int) or isinstance(v,bool) or v<=0 for n,v in r[side].items()):return dict(status='INVALID_INPUT')
   if S.Rational(str(r['rate']))<=0:return dict(status='INVALID_INPUT')
 except (KeyError,TypeError,ValueError):return dict(status='INVALID_INPUT')
 species=sorted({s for r in raw for side in ['source','target'] for s in r[side]})
 for C in species:
  if not all(r['source'].get(C)==r['target'].get(C)==1 and sum(r['source'].values())==sum(r['target'].values())==2 for r in raw):continue
  edges=[]
  for r in raw:
   src=[s for s,v in r['source'].items() if s!=C for _ in range(v)]
   dst=[s for s,v in r['target'].items() if s!=C for _ in range(v)]
   if len(src)!=1 or len(dst)!=1:break
   k=S.Rational(str(r['rate']))
   if k<=0:break
   edges.append((src[0],dst[0],k))
  else:
   for D in sorted(set(v for _,v,_ in edges)-set(u for u,_,_ in edges)):
    T=sorted(set(u for u,_,_ in edges)|set(v for _,v,_ in edges)-{D})
    if D in T:T.remove(D)
    reached={D}
    while True:
     more={u for u,v,k in edges if v in reached};new=reached|more
     if new==reached:break
     reached=new
    if any(u not in reached for u in T):continue
    Q=S.zeros(len(T));idx={v:i for i,v in enumerate(T)}
    for u,v,k in edges:
     if u==v:continue
     Q[idx[u],idx[u]]-=k
     if v!=D:Q[idx[u],idx[v]]+=k
    try:t=-Q.inv()*S.ones(len(T),1)
    except Exception:continue
    if any(v<=0 for v in t) or Q*t!=-S.ones(len(T),1):continue
    return dict(status='LOCAL_PHASE_TYPE_CERTIFICATE',catalyst=C,absorber=D,transient_types=T,
      Q=[[str(q) for q in row] for row in Q.tolist()],mean_vector={v:str(t[idx[v]]) for v in T},
      psi0='sum(t_i*x_i)/(catalyst_count*sum(x_i))',uniform_killed_bound=str(S.Rational(4,3)*max(t)),
      scope='Local face only; ingress/pool/global transfer checks still required.')
 return dict(status='NO_PHASE_TYPE_FACE_CERTIFICATE')

if __name__=='__main__':
 def r(u,v,k=1,C='C'):return dict(source={C:1,u:1},target={C:1,v:1},rate=str(k))
 tests={'two_stage':[r('E','F'),r('F','E'),r('F','D')],
        'three_stage':[r('U','V','2/3'),r('V','U','1/5'),r('V','W','3/2'),r('W','D','7/4')],
        'closed_rejected':[r('E','F'),r('F','E')],
        'unreachable_rejected':[r('E','F'),r('F','E'),r('G','D')]}
 out={name:acquire(net) for name,net in tests.items()}
 assert out['two_stage']['mean_vector']=={'E':'3','F':'2'}
 assert out['three_stage']['status']=='LOCAL_PHASE_TYPE_CERTIFICATE'
 assert out['closed_rejected']['status']==out['unreachable_rejected']['status']=='NO_PHASE_TYPE_FACE_CERTIFICATE'
 print(json.dumps(out,indent=2));Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
