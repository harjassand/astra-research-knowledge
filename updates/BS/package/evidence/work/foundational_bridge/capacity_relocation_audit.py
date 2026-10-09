from functools import lru_cache
from collections import Counter
import json

@lru_cache(None)
def matchings(vertices):
    if not vertices:
        return (frozenset(),)
    a=vertices[0]
    ans=[]
    for b in vertices[1:]:
        rest=tuple(v for v in vertices if v not in (a,b))
        for m in matchings(rest):
            ans.append(m | {(min(a,b),max(a,b))})
    return tuple(ans)

def holes(m,n):
    return frozenset(range(n))-frozenset(v for e in m for v in e)

def path(m,p,a,layer):
    ms=(m,p)
    adj=[{v:e for e in q for v in e} for q in ms]
    current=a
    result=[]
    while current in adj[layer]:
        e=adj[layer][current]
        result.append((layer,e))
        current=e[0] if current==e[1] else e[1]
        layer=1-layer
    return current,result

def switch(m,p,edges):
    out=[set(m),set(p)]
    for layer,e in edges:
        out[layer].remove(e)
        out[1-layer].add(e)
    return tuple(frozenset(q) for q in out)

results=[]
for n in (4,6,8,10):
  for k in (2,4):
    if k>=n: continue
    s=frozenset(range(k)); a=0; z=k
    # Relabeling symmetry covers the only two possible p categories:
    # p in S excluding a, or p outside S excluding z.
    for p in (1,k+1):
      cases=Counter(); seen={}
      for m in matchings(tuple(v for v in range(n) if v not in s)):
        for q in matchings(tuple(v for v in range(n) if v not in {z,p})):
          endpoint,edges=path(m,q,a,1)
          mm,qq=switch(m,q,edges)
          az=(a,z)
          assert az not in m and az not in q
          if endpoint==z:
            case='i'
            expected=(s-{a}|{z},frozenset({a,p}))
          elif endpoint==p:
            case='ii'
            assert p not in s
            assert az not in qq
            qq=qq|{az}
            expected=(s-{a}|{p},frozenset())
          else:
            case='iii'
            assert endpoint in s-{a,p}
            assert az not in qq
            qq=qq|{az}
            expected=(s-{a,endpoint},frozenset({p,endpoint}))
          assert (holes(mm,n),holes(qq,n))==expected
          key=(case,endpoint,mm,qq)
          assert key not in seen, ('collision',n,k,p,key)
          seen[key]=(m,q)
          cases[case]+=1
          before=Counter(m)+Counter(q)
          after=Counter(mm)+Counter(qq)
          if case!='i': before[az]+=1
          assert before==after
          inverse_q=qq if case=='i' else qq-{az}
          inverse_endpoint,inverse_path=path(mm,inverse_q,a,0)
          assert inverse_endpoint==endpoint
          assert switch(mm,inverse_q,inverse_path)==(m,q)
      results.append({'n':n,'hole_count':k,'p_in_S':p in s,'input_pairs':sum(cases.values()),'cases':dict(cases),'status':'PASS'})
print(json.dumps({'scope':'exact finite structural overlay enumeration; not independent proof certification','total_input_pairs':sum(r['input_pairs'] for r in results),'results':results},indent=2))
