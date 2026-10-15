from itertools import combinations, permutations
import json, sys

def maps(n):
    ans=[]
    pairs=list(combinations(range(n),2)); ind={p:i for i,p in enumerate(pairs)}
    for k in range(n+1):
        for dom in combinations(range(n),k):
            for image in permutations(range(n),k):
                f=[-1]*n
                for x,y in zip(dom,image): f[x]=y
                edge=[]
                for x,y in pairs:
                    if f[x]<0 or f[y]<0: edge.append(-1)
                    else: edge.append(ind[tuple(sorted((f[x],f[y])))])
                if any(i==v for i,v in enumerate(edge)): continue
                # Reject single-generator pair cycles.
                cyc=False
                for i in range(len(pairs)):
                    seen=set(); cur=i
                    while cur>=0:
                        if cur in seen: cyc=True; break
                        seen.add(cur); cur=edge[cur]
                    if cyc: break
                if not cyc: ans.append((tuple(f),tuple(edge),sum(1<<x for x in dom)))
    return ans

def main(n):
    ms=maps(n); D=n*(n-1)//2
    best=0; witness=None; checked=0
    for ia,(a,ea,da) in enumerate(ms):
        for b,eb,db in ms[ia:]:
            if da|db != (1<<n)-1: continue
            checked+=1
            color=[0]*D; depth=[0]*D
            def dfs(i):
                if color[i]==1: return -1
                if color[i]==2: return depth[i]
                color[i]=1; val=1
                for j in (ea[i],eb[i]):
                    if j>=0:
                        z=dfs(j)
                        if z<0: return -1
                        val=max(val,z+1)
                depth[i]=val; color[i]=2; return val
            maxval=0
            for i in range(D):
                d=dfs(i)
                if d<0: break
                maxval=max(maxval,d)
            else:
                if maxval>best: best=maxval; witness=(a,b); print(json.dumps({'n':n,'best_collapse_index':best,'a':a,'b':b}),flush=True)
    result={'n':n,'candidate_maps':len(ms),'pairs_checked':checked,'maximum':best,'witness':witness}
    print(json.dumps(result),flush=True)
    return result
if __name__=='__main__': main(int(sys.argv[1]))
