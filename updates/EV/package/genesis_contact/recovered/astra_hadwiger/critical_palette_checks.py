"""Reproducible falsification search for connected palette-pairing.
This is stronger than the perfect-quotient proposal and is not assumed true.
"""
import json, random
from pathlib import Path
import networkx as nx
from finite_checks import masks_from_graph, chromatic, connected_bipartite, vertices, quotient


def partition_with_limit(adj, limit):
    n = len(adj)
    full = (1 << n) - 1
    good = [m for m in range(1,full+1) if connected_bipartite(adj,m)]
    goodset = set(good)
    byv = [[m for m in good if m & (1 << v)] for v in range(n)]
    for options in byv:
        options.sort(key=int.bit_count, reverse=True)
    def search(left, parts):
        if not left:
            return parts
        if len(parts) == limit - 1:
            return parts + (left,) if left in goodset else None
        v = (left & -left).bit_length()-1
        for bag in byv[v]:
            if bag & left == bag:
                ans = search(left ^ bag, parts + (bag,))
                if ans is not None:
                    return ans
        return None
    return search(full, ())


def critical_core(G, rng):
    k = chromatic(masks_from_graph(G))
    edges = list(G.edges())
    rng.shuffle(edges)
    for u,v in edges:
        G.remove_edge(u,v)
        if chromatic(masks_from_graph(G)) < k:
            G.add_edge(u,v)
    # Edge-minimality makes all nonisolated vertices critical.
    G.remove_nodes_from(list(nx.isolates(G)))
    G = nx.convert_node_labels_to_integers(G)
    a = masks_from_graph(G)
    assert chromatic(a) == k
    assert all(chromatic(a, ((1<<len(a))-1) ^ (1<<v)) < k for v in G)
    return G,k


def run():
    # Reproduce the stronger check on all critical atlas graphs as well.
    atlas_records = []
    for index, graph in enumerate(nx.graph_atlas_g()):
        adj = masks_from_graph(graph)
        n = len(adj)
        k = chromatic(adj)
        if n and all(chromatic(adj, ((1 << n)-1) ^ (1 << v)) < k for v in range(n)):
            bags = partition_with_limit(adj, (k+1)//2)
            atlas_records.append(dict(atlas_index=index, k=k,
                bags=None if bags is None else [list(vertices(b)) for b in bags]))
    Path(__file__).with_name('critical_palette_atlas.json').write_text(
        json.dumps(atlas_records, indent=2))
    rng = random.Random(20261013)
    records = []
    for i in range(100):
        n = rng.choice([9,10,11,12,13,14])
        p = rng.choice([.30,.40,.50,.60])
        G = nx.fast_gnp_random_graph(n,p,seed=rng.randrange(2**32))
        G,k = critical_core(G,rng)
        if k < 3:
            continue
        a = masks_from_graph(G)
        bags = partition_with_limit(a,(k+1)//2)
        record = dict(iteration=i,n=len(G),k=k,edges=list(G.edges()),
                      bags=None if bags is None else [list(vertices(b)) for b in bags])
        records.append(record)
        if bags is None:
            print('COUNTEREXAMPLE', json.dumps(record), flush=True)
            break
    result = dict(seed=20261013, graphs_tested=len(records),
                  failures=sum(r['bags'] is None for r in records),
                  records=records)
    Path(__file__).with_name('critical_palette_checks.json').write_text(json.dumps(result,indent=2))
    print({k:v for k,v in result.items() if k!='records'},flush=True)

if __name__ == '__main__':
    run()
