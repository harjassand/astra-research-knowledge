"""Independent exact test of the two terminal signature transitions.

No producer imports or scientific replay. Finite checks supplement PROOF.md.
"""
from itertools import product
from pathlib import Path
import hashlib
import json
import resource
import time


def path(length):
    return {'n':length+1, 'edges':[(i,i+1) for i in range(length)],
            'terminals':[0,length]}


def series(g,h):
    n=g['n']; s,t=g['terminals']; u,v=h['terminals']
    mapping={u:t}
    for i in range(h['n']):
        if i!=u: mapping[i]=n; n+=1
    return {'n':n,'edges':g['edges']+[(mapping[a],mapping[b]) for a,b in h['edges']],
            'terminals':[s,mapping[v]]}


def parallel(children):
    # Outer terminals 0,1; joined child terminals 2,3.
    n=4; edges=[(0,2),(3,1)]
    for g in children:
        s,t=g['terminals']; mapping={s:2,t:3}
        for i in range(g['n']):
            if i not in mapping: mapping[i]=n; n+=1
        edges.extend((mapping[a],mapping[b]) for a,b in g['edges'])
    return {'n':n,'edges':edges,'terminals':[0,1]}


def signature(colors,adj,terminals):
    s,t=terminals; u=adj[s][0]; v=adj[t][0]
    return (colors[s],colors[t],colors[u],colors[v],
            any(colors[w]==colors[s] for w in adj[u] if w!=s),
            any(colors[w]==colors[t] for w in adj[v] if w!=t))


def actual_states(g,palette=4):
    adj=[[] for _ in range(g['n'])]
    for a,b in g['edges']: adj[a].append(b); adj[b].append(a)
    assert all(len(adj[t])==1 for t in g['terminals'])
    s,t=g['terminals']; assert t not in adj[s]
    states=set(); proper=0; star=0
    colors=[-1]*g['n']
    # Enumerate proper assignments exactly; prune only already colored edges.
    def visit(i):
        nonlocal proper,star
        if i<g['n']:
            forbidden={colors[j] for j in adj[i] if j<i}
            for c in range(palette):
                if c not in forbidden:
                    colors[i]=c; visit(i+1)
            colors[i]=-1
            return
        proper+=1
        for a,b in g['edges']:
            if (any(colors[w]==colors[b] for w in adj[a] if w!=b)
                    and any(colors[w]==colors[a] for w in adj[b] if w!=a)):
                return
        star+=1; states.add(signature(colors,adj,g['terminals']))
    visit(0)
    return states,{'proper_assignments':proper,'star_assignments':star}


def series_states(F,G):
    result=set()
    for a,b,p,q,f,g in F:
        for c,d,r,s,h,k in G:
            if b==c and not(q==r and (g or h)):
                result.add((a,d,p,s,f,k))
    return result


def parallel_states(state_sets,palette=4):
    result=set()
    for states in product(*state_sets):
        C,D=states[0][:2]
        if any(s[:2]!=(C,D) for s in states): continue
        for A in range(palette):
            if A==C: continue
            for B in range(palette):
                if B==D: continue
                valid=True
                for i,s in enumerate(states):
                    p,q,f,g=s[2:]
                    if f and (p==A or any(j!=i and r[2]==p for j,r in enumerate(states))):
                        valid=False; break
                    if g and (q==B or any(j!=i and r[3]==q for j,r in enumerate(states))):
                        valid=False; break
                if valid:
                    result.add((A,B,C,D,any(s[2]==A for s in states),any(s[3]==B for s in states)))
    return result


def digest(states):
    return hashlib.sha256(json.dumps(sorted(states),separators=(',',':')).encode()).hexdigest()


def main():
    start=time.perf_counter(); cpu=time.process_time()
    graphs={'L2':path(2),'L3':path(3)}
    graphs['S2_L2_L2']=series(graphs['L2'],graphs['L2'])
    graphs['P2_L2_L2']=parallel([graphs['L2'],graphs['L2']])
    graphs['P3_L2_L2_L2']=parallel([graphs['L2']]*3)
    graphs['P2_L2_L3']=parallel([graphs['L2'],graphs['L3']])
    graphs['S2_L2_P2']=series(graphs['L2'],graphs['P2_L2_L2'])
    actual={}; counts={}
    for name,g in graphs.items(): actual[name],counts[name]=actual_states(g)
    predicted={
        'S2_L2_L2':series_states(actual['L2'],actual['L2']),
        'P2_L2_L2':parallel_states([actual['L2']]*2),
        'P3_L2_L2_L2':parallel_states([actual['L2']]*3),
        'P2_L2_L3':parallel_states([actual['L2'],actual['L3']]),
        'S2_L2_P2':series_states(actual['L2'],actual['P2_L2_L2']),
    }
    results=[]
    for name,pred in predicted.items():
        observed=actual[name]
        assert pred==observed,(name,sorted(pred-observed),sorted(observed-pred))
        results.append({'name':name,'input':graphs[name],'state_count':len(observed),
                        'state_sha256':digest(observed),**counts[name],
                        'actual_states':[list(s) for s in sorted(observed)],'status':'PASS'})
    out={'scope':'Finite independently enumerated checks of exact interface; universal lemma is PROOF.md, not inferred from these inputs.',
         'status':'PASS','tests':results,
         'cost':{'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,
                 'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                 'excludes':'process startup, reading/authoring/reasoning/review, final serialization'}}
    (Path(__file__).resolve().parent/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'tests':[{k:v for k,v in t.items() if k in ('name','state_count','proper_assignments','star_assignments','status')} for t in results],'cost':out['cost']},indent=2))


if __name__=='__main__': main()
