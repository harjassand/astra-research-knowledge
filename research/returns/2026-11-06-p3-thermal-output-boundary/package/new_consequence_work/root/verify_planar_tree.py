"""Finite geometry/count checks; analytic all-size proof is separate."""
from pathlib import Path
from collections import defaultdict
import json, math
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results'
OUT.mkdir(exist_ok=True)

def tree(h):
    vertices, edges = {(0, 0)}, set()
    def path(a, b):
        x, y = a
        dx = (b[0] > x) - (b[0] < x)
        dy = (b[1] > y) - (b[1] < y)
        assert (dx == 0) != (dy == 0)
        while (x, y) != b:
            nxt = (x + dx, y + dy)
            assert nxt not in vertices, (h, (x, y), nxt, 'intersection')
            vertices.add(nxt)
            edges.add(tuple(sorted(((x, y), nxt))))
            x, y = nxt
    def build(k, origin):
        if not k: return
        length = 2 ** (k - 1)
        ox, oy = origin
        for sx in (-1, 1):
            elbow = (ox + sx * length, oy)
            path(origin, elbow)
            for sy in (-1, 1):
                endpoint = (elbow[0], oy + sy * length)
                path(elbow, endpoint)
                build(k - 1, endpoint)
    build(h, (0, 0))
    adjacency = defaultdict(list)
    for a, b in edges:
        assert abs(a[0]-b[0]) + abs(a[1]-b[1]) == 1
        adjacency[a].append(b); adjacency[b].append(a)
    parent, order = {(0, 0): None}, [(0, 0)]
    for v in order:
        for w in adjacency[v]:
            if w == parent[v]: continue
            assert w not in parent
            parent[w] = v; order.append(w)
    assert len(order) == len(vertices) == len(edges) + 1
    sizes = {v: 1 for v in vertices}
    for v in reversed(order[1:]): sizes[parent[v]] += sizes[v]
    return vertices, edges, parent, order, sizes, adjacency

def hook_recurrence(h):
    product, nprev = 1, 1
    for k in range(1, h + 1):
        length = 2 ** (k - 1)
        elbow = 2*nprev + 2*length - 1
        product = (product**4 * math.prod(range(elbow, elbow+length))**2
                   * math.prod(range(nprev, nprev+length))**4)
        nprev = 3*(4**k-2**k)+1
    return product

receipts=[]
for h in range(1, 8):
    vertices, edges, parent, order, sizes, adjacency = tree(h)
    n = len(edges)
    product = math.prod(sizes[v] for v in order[1:])
    assert n == 3*(4**h-2**h)
    assert max(map(len, adjacency.values())) == 3
    assert [v for v in vertices if v[0] == 0] == [(0, 0)]
    assert product == hook_recurrence(h) and product <= 16**n
    area = (2**(h+1)-1)**2
    assert 3*area == 4*len(vertices)-1
    receipts.append({'h':h, 'vertices':len(vertices), 'unit_edges':n,
                     'bounding_area':area, 'max_degree':3,
                     'log_hook_product_per_edge':sum(math.log(sizes[v]) for v in order[1:])/n,
                     'exact_product_le_16_pow_edges':True,
                     'exact_hook_recurrence':True, 'no_intersections':True})

vertices, edges, parent, order, sizes, adjacency = tree(1)
index = {v:i for i,v in enumerate(order)}
nsite, dim = len(order), 2**len(order)
H = np.zeros((dim, dim))
for x in range(dim):
    H[x,x] += x.bit_count()
    for v in order[1:]:
        if (x >> index[parent[v]]) & 1:
            H[x,x] += .5
            H[x ^ (1 << index[v]), x] += .5
assert np.all(H >= 0) and np.array_equal(H,H.T)
energies, basis = np.linalg.eigh(H)
assert abs(energies[0]) < 1e-12 and energies[1] >= 1-1e-12
assert np.linalg.norm(H[:,0]) == 0
U = np.eye(dim)[np.arange(dim)^1]
Ue = basis.T @ U @ basis
spectral=[]
for beta in (.25,.5,1.):
    modular = np.exp((beta/2)*(energies[:,None]-energies[None,:]))*Ue
    kappa = np.linalg.svd(modular,compute_uv=False)[0]**2
    pmax = 1/(1+kappa)
    weights = np.exp(-beta*energies)
    rho = (basis*(weights/weights.sum()))@basis.T
    minima=[]
    for factor in (.9,1.1):
        p = factor*pmax
        inv = ((1-p)*rho-p*U@rho@U)/(1-2*p)
        minima.append(float(np.linalg.eigvalsh(inv)[0]))
    assert minima[0]>-1e-12 and minima[1]<-1e-10
    spectral.append({'beta':beta,'kappa':float(kappa),'p_max':float(pmax),
                     'min_eigenvalue_at_0.9_pmax':minima[0],
                     'min_eigenvalue_at_1.1_pmax':minima[1]})
receipt={'geometry_and_hook_checks':receipts,
         'seven_site_gap':float(energies[1]),
         'seven_site_spectral_diagnostics':spectral,
         'scope':'Finite checks supplement the analytic all-size proofs.'}
(OUT/'planar_tree_checks.json').write_text(json.dumps(receipt,indent=2))
print(json.dumps(receipt,indent=2))

if __name__ == '__main__':
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    v,e,*_=tree(3)
    fig,ax=plt.subplots(figsize=(7.2,6.1))
    for a,b in e:
        ax.plot([a[0],b[0]],[a[1],b[1]],color='#287d84',linewidth=1.35)
    ax.scatter([x for x,y in v],[y for x,y in v],s=9,color='#287d84',zorder=3)
    ax.scatter([0],[0],s=90,color='#b64c37',zorder=4)
    ax.annotate('noisy root port',(0,0),xytext=(.45,.55),color='#8f3727',fontsize=10)
    ax.set_aspect('equal'); ax.set_xlim(-7.8,7.8); ax.set_ylim(-7.8,7.8)
    ax.set_xticks(range(-7,8)); ax.set_yticks(range(-7,8))
    ax.grid(alpha=.14); ax.set_axisbelow(True)
    ax.set_title('A planar cell: 169 qubits, 168 unit-length edges',fontsize=13,pad=14)
    ax.set_xlabel('lattice coordinate'); ax.set_ylabel('lattice coordinate')
    fig.tight_layout(); fig.savefig(OUT/'planar_cell.png',dpi=210)
    fig.savefig(OUT/'planar_cell.svg'); plt.close(fig)
