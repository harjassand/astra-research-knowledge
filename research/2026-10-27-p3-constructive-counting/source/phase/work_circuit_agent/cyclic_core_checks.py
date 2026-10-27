#!/usr/bin/env python3
"""Exact feedback-deletion and local-cycle checks, using standard library only."""
from itertools import product
from pathlib import Path
import json
from causal_obstructions import matrix_rank


def fixture():
    Q,R,r=3,2,2
    labels=list(product(range(r),repeat=2*Q))
    pos={u:i for i,u in enumerate(labels)}
    D=len(labels)
    M=[[0]*D for _ in range(D)]
    for i,u in enumerate(labels):
        v=list(u[Q:]+u[:Q])
        M[i][pos[tuple(v)]]+=1-Q
        for s in range(Q):
            w=v[:]
            w[s],w[Q+s]=w[Q+s],w[s]
            M[i][pos[tuple(w)]]+=1
    bad={i for i,u in enumerate(labels) if sum(u[s]!=u[Q+s] for s in range(Q))>=R}
    assert all(M[i][j]==M[j][i] for i in range(D) for j in range(D))
    graph=[{j for j in range(D) if i!=j and M[i][j]} for i in range(D)]
    return M,bad,graph


def components(graph,vertices=None):
    pending=set(range(len(graph)) if vertices is None else vertices)
    answer=[]
    while pending:
        seed=min(pending)
        pending.remove(seed)
        comp={seed}
        stack=[seed]
        while stack:
            v=stack.pop()
            new=graph[v]&pending
            pending.difference_update(new)
            comp.update(new)
            stack.extend(new)
        answer.append(sorted(comp))
    return answer


def main():
    M,bad,graph=fixture()
    comps=components(graph)
    D=len(M)
    c=matrix_rank([[int(i==j)-M[i][j] for j in range(D)] for i in range(D)])
    best_by_cap={1:0,2:0,3:0,4:0,8:0}
    component_rows=[]
    subset_checks=0
    for comp in comps:
        L=len(comp)
        base_rank=matrix_rank([[int(i==j)-M[i][j] for j in comp] for i in comp])
        best={cap:L for cap in best_by_cap}
        chosen={cap:None for cap in best_by_cap}
        for mask in range(1<<L):
            kept=[comp[k] for k in range(L) if mask>>k&1]
            deleted=L-len(kept)
            kept_comps=components(graph,kept)
            cap=max((len(x) for x in kept_comps),default=0)
            rank=(matrix_rank([[int(i==j)-M[i][j] for j in kept] for i in kept])
                  if kept else 0)
            hard=len(set(kept)&bad)
            assert rank<=base_rank
            assert not kept or rank*max(1,cap)>=hard
            if cap<=1:
                assert base_rank>=hard
                assert deleted>=len(set(comp)&bad)-base_rank
            for allowed in best:
                if cap<=allowed and deleted<best[allowed]:
                    best[allowed]=deleted
                    chosen[allowed]=[i for i in comp if i not in kept]
            subset_checks+=1
        for cap in best_by_cap:
            best_by_cap[cap]+=best[cap]
        if L>1:
            component_rows.append({'size':L,'hard_vertices':len(set(comp)&bad),
                                   'rank_I_minus_M':base_rank,
                                   'minimum_deletions_by_scc_cap':best})
    assert c==10 and len(bad)==32
    assert best_by_cap[1]==24
    assert best_by_cap[2]==16
    assert best_by_cap[4]==4
    answer={'dimension':D,'hard_diagonal_labels':len(bad),'rank_I_minus_M':c,
            'general_feedback_lower_bound':len(bad)-c,
            'exact_minimum_feedback_deletions':best_by_cap[1],
            'exact_minimum_deletions_by_scc_cap':best_by_cap,
            'all_component_subset_checks':subset_checks,
            'isolated_good_vertices':sum(len(x)==1 and x[0] not in bad for x in comps),
            'nontrivial_components':component_rows}
    Path(__file__).with_name('cyclic_core_results.json').write_text(json.dumps(answer,indent=2)+'\n')
    print(json.dumps({k:v for k,v in answer.items() if k!='nontrivial_components'},indent=2))

if __name__=='__main__':main()
