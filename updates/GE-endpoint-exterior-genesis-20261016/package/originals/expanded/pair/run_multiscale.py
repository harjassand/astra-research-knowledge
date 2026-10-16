"""One bounded graded-path comparison, using original exact-state helper code."""
from pathlib import Path
exec((Path(__file__).parent/'run_checks.py').read_text().split('specs=[]')[0])
n=6; rates=np.array([1.,10.,100.,1000.,10000.]);edges=[(i,i+1) for i in range(5)]
states=space(n,'interchange');maps,index=swap_maps(states,edges);initial=index[tuple(range(n))]
L=laplacian(maps,rates);p,diag=endpoint(L,initial);p=clean(p)
np.savez(OUT/'graded_path_generators.npz',L=L,p=p,rates=rates,edges=np.array(edges),states=np.array(states))
rows=[]
for K in [5,10,20,50,100,200,500,1000,2000,5000,8000]:
    capped=np.minimum(rates,K);q,d=endpoint(laplacian(maps,capped),initial);q=clean(q)
    cert=0.;choices=[]
    for ei,(u,v) in enumerate(edges):
        W=rates[ei]
        if W<=K:continue
        candidates=[]
        for left in range(u+1):
            for right in range(v,n):
                C=range(left,right+1);c=c_local(len(C))
                if K<2*c:continue
                outside=[sum(r for (a,b),r in zip(edges,rates) if (a==x and b not in C) or (b==x and a not in C)) for x in C]
                b=sum(sorted(outside,reverse=True)[:2])
                tail=bound_local(K,[c],[b]);finite=tail-bound_local(W,[c],[b])
                candidates.append((finite,tail,left,right,c,b))
        best=min(candidates);cert+=best[0];choices.append(dict(edge=ei,bound=best[0],infinite_tail=best[1],C=[best[2],best[3]],c=best[4],b=best[5]))
    rows.append(dict(K=K,TV=float(tv(p,q)),Lambda=float(capped.sum()),local_finite_rate_certificate=cert,choices=choices))
    np.save(OUT/('graded_path_endpoint_K'+str(K)+'.npy'),q)
averages=[]
for first in range(1,6):
    # Average the connected fast tail {first,...,5}; preceding vertices stay singleton.
    clusters=[(i,) for i in range(first)]+[tuple(range(first,6))]
    if first==5:continue
    slow=rates.copy();slow[first:]=0
    q,norbit=limit_endpoint(states,clusters,laplacian(maps,slow),initial)
    averages.append(dict(first_fast_vertex=first,clusters=clusters,TV=float(tv(p,q)),Gamma=float(slow.sum()),orbit_count=norbit))
report=dict(graph='six_vertex_graded_path_interchange',rates=list(rates),state_count=len(states),initial='identity',T=1,original_Lambda=float(rates.sum()),diagnostics=diag,caps=rows,boundary_shuffle_limits=averages)
(OUT/'graded_path_results.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
