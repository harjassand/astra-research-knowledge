"""New bounded mechanism checks; no prior scientific suite is replayed."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import resource
import sys
import time
from theta_hub_split import theta_form, color_form, prepare, pair_components

ROOT = Path(__file__).resolve().parent


class Builder:
    def __init__(self):
        self.n = 0
        self.edges = []
        self.blocks = []

    def vertex(self):
        v = self.n; self.n += 1
        return v

    def add(self, lengths, attach=None):
        a, b = self.vertex(), self.vertex()
        paths = []
        for j, length in enumerate(lengths):
            path = [a]
            for i in range(1, length):
                v = attach[0] if attach is not None and (j, i) == attach[1:] else self.vertex()
                path.append(v)
            path.append(b)
            self.edges.extend(tuple(sorted(e)) for e in zip(path, path[1:]))
            paths.append(path)
        self.blocks.append(paths)
        return paths

    def native(self, name):
        return dict(name=name, n=self.n, edges=sorted(self.edges))


def cut_witness(native, colors):
    components = pair_components(native['n'], native['edges'], colors)
    best = None
    for comp in components:
        order, parent = comp['vertices'], comp['parent']
        sizes = {v: 1 for v in order}
        for v in reversed(order[1:]):
            sizes[parent[v]] += sizes[v]
        N = len(order)
        for v in order[1:]:
            g = F(sizes[v] * (N - sizes[v]), N)
            if best is None or g > best[0]:
                best = g, comp, v, sizes
    gamma, comp, child, sizes = best
    pair = comp['pair']; order = comp['vertices']; parent = comp['parent']
    inside = {child}
    for v in order:
        if parent[v] in inside:
            inside.add(v)
    a, b = len(inside), len(order) - len(inside)
    div = {v: F(1, a) if v in inside else -F(1, b) for v in order}
    subtotal = div.copy()
    weights = {}
    for v in reversed(order[1:]):
        sign = 1 if colors[v] == pair[0] else -1
        weights[tuple(sorted((v, parent[v])))] = sign * subtotal[v]
        subtotal[parent[v]] += subtotal[v]
    Y = [[F(0)] * 4 for _ in range(native['n'])]
    for (u, v), w in weights.items():
        Y[u][colors[v]] += w
        Y[v][colors[u]] += w
    norm2 = sum((x*x for row in Y for x in row), F(0))
    e = tuple(sorted((child, parent[child])))
    assert abs(weights[e]) == 1 and norm2 == F(1,a) + F(1,b)
    return dict(pair=pair, cut=e, a=a, b=b, inverse_lower_sq=str(gamma),
                action_norm_sq=str(norm2), diagonal=['0'] * native['n'],
                nonzero_edges=[dict(edge=e, value=str(v)) for e, v in sorted(weights.items())],
                full_original_action=[[str(x) for x in row] for row in Y])


def main():
    wall, cpu = time.perf_counter(), time.process_time()
    chain = Builder()
    previous = None
    for _ in range(12):
        paths = chain.add((2,3,3), None if previous is None else (previous,0,1))
        # Canonical hub 0 of each block is deleted; this is its neighbor on
        # the first length-three branch, distance three from the incoming
        # length-two midpoint in the remaining rooted tree.
        previous = paths[1][1]
    bad_input = chain.native('plain_forest_theta_chain_12')
    f = theta_form(bad_input['n'], bad_input['edges'])
    bad = color_form(f, corrected=False)
    fixed = color_form(f, corrected=True)
    bad_cut = cut_witness(bad_input, bad['colors'])
    good_form, good_design = prepare(bad_input['n'], bad_input['edges'])
    assert fixed == {k: good_design[k] for k in fixed}
    branched = Builder()
    b0 = branched.add((2,3,5,4))
    b1 = branched.add((2,4,3), (b0[2][1],1,2))
    b2 = branched.add((2,3,3), (b0[2][2],0,1))
    b3 = branched.add((3,3,4,2), (b0[2][3],0,1))
    b4 = branched.add((2,3,4,2), (b2[1][2],0,1))
    b5 = branched.add((2,5,3), (b1[2][1],0,1))
    b6 = branched.add((3,2,4), (b4[1][1],0,2))
    mixed_input = branched.native('adjacent_marks_mixed_theta_57')
    mixed_form, mixed_design = prepare(mixed_input['n'], mixed_input['edges'])
    inputs = [bad_input, mixed_input]
    results = []
    for native, form, design in [(bad_input,good_form,good_design),(mixed_input,mixed_form,mixed_design)]:
        comps = pair_components(native['n'], native['edges'], design['colors'])
        results.append(dict(name=native['name'], n=native['n'], m=len(native['edges']),
                            blocks=len(form['blocks']), max_degree=form['max_degree'],
                            max_block_depth=max(form['depth']),
                            max_component_size=max(map(lambda c:len(c['vertices']),comps)),
                            flips=design['flips'], colors=design['colors'],
                            special_hubs=design['special_hubs'],
                            constraints=design['constraints'],spiders=design['spiders']))
    report = dict(status='PASS', scope='New native construction and exact bad-rule cut witness only; not an independent receiving solve or all-size computational proof',
                  corrected_results=results, uncorrected_cut=bad_cut)
    for native in inputs:
        (ROOT/(native['name']+'.json')).write_text(json.dumps(native,indent=2)+'\n')
    (ROOT/'DIAGNOSTIC_RESULT.json').write_text(json.dumps(report,indent=2)+'\n')
    costs = dict(wall_seconds=time.perf_counter()-wall,cpu_seconds=time.process_time()-cpu,
                 peak_process_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                 includes='native input construction, recognition, coloring, structural checks, exact failed-rule original-action witness, and JSON serialization',
                 excludes='proof discovery, reading, authoring, review, integration, interpreter startup; unknown totals remain unknown',
                 source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'theta_hub_split.py',Path(__file__)]})
    (ROOT/'COSTS.json').write_text(json.dumps(costs,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',costs=costs,observations=[{k:v for k,v in r.items() if k in ('name','n','m','blocks','max_degree','max_block_depth','max_component_size','flips')} for r in results],bad_cut={k:bad_cut[k] for k in ['a','b','inverse_lower_sq','action_norm_sq']})))


if __name__ == '__main__':
    main()
