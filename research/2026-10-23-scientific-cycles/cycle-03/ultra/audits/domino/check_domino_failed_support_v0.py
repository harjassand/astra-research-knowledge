#!/usr/bin/env python3
"""Exact physical common-Gram cone obstruction, without a numerical SDP.

No dense optimization or float input: projectors and Grams use Fraction.
The complete finite enumeration is the proof of the 3x3 rook support minimum.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import json, time, resource

def projector(i, j=None, sign=1):
    p = [[F(0) for _ in range(3)] for _ in range(3)]
    if j is None:
        p[i][i] = F(1)
    else:
        p[i][i] = p[j][j] = F(1,2)
        p[i][j] = p[j][i] = F(sign,2)
    return p

def overlap(p, q):
    return sum(p[i][j]*q[j][i] for i in range(3) for j in range(3))

def partitions(items):
    """Each unordered partition of 9 labels into three triples, exactly once."""
    if not items:
        yield ()
        return
    a = items[0]
    for pair in combinations(items[1:], 2):
        b = (a,)+pair
        rest = tuple(x for x in items if x not in b)
        for tail in partitions(rest):
            yield (b,)+tail

def main(out=None):
    start_cpu, start_wall = time.process_time(), time.perf_counter()
    states = []
    for sign in (1,-1): states.append((projector(0), projector(0,1,sign)))
    for sign in (1,-1): states.append((projector(2), projector(1,2,sign)))
    for sign in (1,-1): states.append((projector(0,1,sign), projector(2)))
    for sign in (1,-1): states.append((projector(1,2,sign), projector(0)))
    states.append((projector(1),projector(1)))
    assert len(states)==9
    for j,(a,b) in enumerate(states):
        for k,(c,d) in enumerate(states):
            assert overlap(a,c)*overlap(b,d)==int(j==k)
    # Total dimensionless Gram G/ln(3) for the two one-site erasures.
    gram = [[(overlap(a,c)+overlap(b,d))/3 for c,d in states] for a,b in states]
    assert all(gram[j][j]==F(2,3) for j in range(9))
    assert all(sum(row)==2 for row in gram)
    zeros = {(j,k) for j in range(9) for k in range(j+1,9) if gram[j][k]==0}
    degrees = [sum(j==a or j==b for a,b in zeros) for j in range(9)]
    histogram, graphs = {}, set()
    for rows in partitions(tuple(range(9))):
        assert len(rows)==3
        for row1 in permutations(rows[1]):
            for row2 in permutations(rows[2]):
                grid=(rows[0], row1, row2)
                edges=set()
                for row in grid:
                    edges.update(tuple(sorted(pair)) for pair in combinations(row,2))
                for col in zip(*grid):
                    edges.update(tuple(sorted(pair)) for pair in combinations(col,2))
                assert len(edges)==18
                edge_tuple=tuple(sorted(edges))
                if edge_tuple in graphs: continue
                graphs.add(edge_tuple)
                bad=len(edges & zeros)
                histogram[bad]=histogram.get(bad,0)+1
    assert len(graphs)==5040
    minimum=min(histogram)
    assert minimum>0, 'No support obstruction was found'
    # W is the Laplacian of the zero graph: PSD by sum_(j,k) (x_j-x_k)^2.
    W=[[F(degrees[j]) if j==k else F(-int(tuple(sorted((j,k))) in zeros))
        for k in range(9)] for j in range(9)]
    traceW=sum(W[j][j] for j in range(9))
    wg=sum(W[j][k]*gram[k][j] for j in range(9) for k in range(9))
    assert wg==F(2,3)*traceW
    kappa_bound=F(2*minimum,3)/traceW
    result={
      'status':'PASS_EXACT_PHYSICAL_CONE_OBSTRUCTION', 'D':3, 'r':2, 'N':1,
      'normalization':'G/m; m=ln(3)',
      'states_order':'0(0+1),0(0-1),2(1+2),2(1-2),(0+1)2,(0-1)2,(1+2)0,(1-2)0,11; all sums normalized',
      'gram':[[str(x) for x in row] for row in gram],
      'zero_edges':sorted(zeros), 'zero_degrees':degrees,
      'rook_graphs_complete':len(graphs), 'bad_edge_histogram':dict(sorted(histogram.items())),
      'minimum_forbidden_rook_edges':minimum,
      'dual_W':[[str(x) for x in row] for row in W], 'traceW':str(traceW),
      'Tr_W_G_over_m':str(wg), 'certified_kappa_over_ln3_lower_bound':str(kappa_bound),
      'cone_failure_is_not_entropy_failure':True,
      'cpu_seconds':time.process_time()-start_cpu,'wall_seconds':time.perf_counter()-start_wall,
      'maxrss_platform_units':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    if out: Path(out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('gram','dual_W','zero_edges')},indent=2))
    return result

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(); p.add_argument('--output',default=str(Path(__file__).with_name('RESULT.json')))
    main(p.parse_args().output)
