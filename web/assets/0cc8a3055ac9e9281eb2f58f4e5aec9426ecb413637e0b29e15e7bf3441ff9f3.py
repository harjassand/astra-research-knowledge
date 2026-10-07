"""Exact recognition and support compiler for a scoped hard-BCS subclass.

The module does not implement Chen--Liu counting or a quantum circuit. It
acquires a bipartite pair representation, a rational graph Slater matrix,
and deterministic exact prefix feasibility/witnesses. Only the inverse
branch requires n=2k; diagonal shifts preserve every hard-sector minor.
"""
from fractions import Fraction as Q
from collections import deque
from itertools import combinations


class C:
    __slots__ = ('re', 'im')
    def __init__(self, re=0, im=0):
        self.re, self.im = Q(re), Q(im)
    @staticmethod
    def make(x):
        if isinstance(x, C): return x
        if isinstance(x, (tuple, list)): return C(*x)
        return C(x)
    def __add__(self, x):
        x = C.make(x); return C(self.re+x.re, self.im+x.im)
    __radd__ = __add__
    def __neg__(self): return C(-self.re, -self.im)
    def __sub__(self, x): return self + -C.make(x)
    def __rsub__(self, x): return C.make(x) + -self
    def __mul__(self, x):
        x = C.make(x)
        return C(self.re*x.re-self.im*x.im, self.re*x.im+self.im*x.re)
    __rmul__ = __mul__
    def __truediv__(self, x):
        x = C.make(x); d = x.re*x.re+x.im*x.im
        return C((self.re*x.re+self.im*x.im)/d,
                 (self.im*x.re-self.re*x.im)/d)
    def __bool__(self): return bool(self.re or self.im)
    def __eq__(self, x):
        x = C.make(x); return self.re == x.re and self.im == x.im
    def conjugate(self): return C(self.re, -self.im)
    def abs2(self): return self.re*self.re+self.im*self.im
    def json(self): return [str(self.re), str(self.im)]
    def __repr__(self): return f'C({self.re},{self.im})'


def matrix(a): return [[C.make(x) for x in row] for row in a]
def minor(a, rows, cols): return [[a[i][j] for j in cols] for i in rows]


def det(a):
    a = matrix(a); n = len(a); d = C(1)
    for j in range(n):
        p = next((i for i in range(j, n) if a[i][j]), None)
        if p is None: return C(0)
        if p != j: a[p], a[j] = a[j], a[p]; d = -d
        pivot = a[j][j]; d = d*pivot
        for i in range(j+1, n):
            if a[i][j]:
                q = a[i][j]/pivot
                for k in range(j+1, n): a[i][k] = a[i][k]-q*a[j][k]
                a[i][j] = C(0)
    return d


def inverse(a):
    a = matrix(a); n = len(a)
    b = [row + [C(i == j) for j in range(n)] for i, row in enumerate(a)]
    for j in range(n):
        p = next((i for i in range(j, n) if b[i][j]), None)
        if p is None: raise ValueError('singular matrix')
        b[p], b[j] = b[j], b[p]
        pivot = b[j][j]; b[j] = [x/pivot for x in b[j]]
        for i in range(n):
            if i != j and b[i][j]:
                q = b[i][j]; b[i] = [x-q*y for x,y in zip(b[i], b[j])]
    return [row[n:] for row in b]


def rank(a):
    if not a: return 0
    a = matrix(a); r = 0
    for j in range(len(a[0])):
        p = next((i for i in range(r, len(a)) if a[i][j]), None)
        if p is None: continue
        a[p], a[r] = a[r], a[p]
        q = a[r][j]; a[r] = [x/q for x in a[r]]
        for i in range(r+1, len(a)):
            if a[i][j]:
                q = a[i][j]; a[i] = [x-q*y for x,y in zip(a[i],a[r])]
        r += 1
        if r == len(a): break
    return r


def strip_diagonal(a):
    return [[C(0) if i == j else x for j,x in enumerate(row)]
            for i,row in enumerate(matrix(a))]


def bipartition(a):
    """Returns acquired colors, or an explicit odd closed walk."""
    n = len(a); color = [None]*n; parent = [None]*n
    edges = [[j for j in range(n) if j != i and (a[i][j] or a[j][i])]
             for i in range(n)]
    for s in range(n):
        if color[s] is not None: continue
        color[s] = 0; queue = deque([s])
        while queue:
            i = queue.popleft()
            for j in edges[i]:
                if color[j] is None:
                    color[j] = 1-color[i]; parent[j] = i; queue.append(j)
                elif color[j] == color[i]:
                    left=[]; x=i
                    while x is not None: left.append(x); x=parent[x]
                    right=[]; x=j
                    while x not in left: right.append(x); x=parent[x]
                    lca=x; left=left[:left.index(lca)+1]
                    return None, left+list(reversed(right))+[i]
    return color, None


def graph_slater(h, color):
    aa=[i for i,c in enumerate(color) if c == 0]
    bb=[i for i,c in enumerate(color) if c == 1]
    a,b=len(aa),len(bb); z=C(0)
    g=[]; row_sites=[]; row_spins=[]
    for i in aa:
        g.append([z]*b+[h[i][j] for j in bb]); row_sites.append(i); row_spins.append('U')
    for i in aa:
        g.append([-h[j][i] for j in bb]+[z]*b); row_sites.append(i); row_spins.append('D')
    for offset, spin in [(0,'D'),(b,'U')]:
        for j,i in enumerate(bb):
            g.append([C(t == offset+j) for t in range(2*b)])
            row_sites.append(i); row_spins.append(spin)
    return g,row_sites,row_spins,aa,bb


def recognize(f, k, shifts=(0,)):
    """Exact finite-union recognition; rejection means outside this compiler.

    Default branches: off-diagonal bipartite F, or off-diagonal bipartite
    F^{-1} at half filling. Explicit rational scalar diagonal shifts may
    enlarge the inverse branch; their number and encodings are charged.
    """
    f=matrix(f); n=len(f)
    if any(len(row) != n for row in f): raise ValueError('F must be square')
    if not (0 <= k <= n//2): return {'status':'ZERO','reason':'hard capacity'}
    h=strip_diagonal(f); color,odd=bipartition(h)
    scalar=C(1); branch='DIRECT_BIPARTITE'; shifted=None
    if color is None:
        if n != 2*k:
            return {'status':'REJECTED_SUBCLASS','reason':'inverse identity requires n=2k','odd_walk':odd}
        for shift in shifts:
            q=C.make(shift)
            shifted=[[x+(q if i == j else 0) for j,x in enumerate(row)] for i,row in enumerate(f)]
            determinant=det(shifted)
            if not determinant: continue
            h=strip_diagonal(inverse(shifted)); color,odd_inv=bipartition(h)
            if color is not None:
                scalar=((-1)**k)*determinant; branch='INVERSE_BIPARTITE_HALF_FILL'; break
        else:
            return {'status':'REJECTED_SUBCLASS','reason':'all inverse branches rejected','odd_walk':odd}
    g,sites,spins,aa,bb=graph_slater(h,color)
    return {'status':'COMPILED','branch':branch,'n':n,'k':k,'F':f,'H':h,
            'G':g,'color':color,'scalar':scalar,'norm_factor':scalar.abs2(),
            'row_sites':sites,'row_spins':spins,'A':aa,'B':bb,
            'shift':None if shifted is None else q}


def prefix_support(compiled, spin_constraints):
    """Deterministic full-single-occupancy support/witness by matroid intersection.

    spin_constraints is {site:'U'/'D'}. The full-occupancy interface has only
    n physical spin bits. Returns ZERO or an exact verified witness; no
    randomized norm estimate is used as feasibility evidence.
    """
    if compiled['status'] != 'COMPILED': return {'status':compiled['status']}
    n,k=compiled['n'],compiled['k']
    if n != 2*k: raise ValueError('this executable prefix interface requires half filling')
    g=compiled['G']; sites=compiled['row_sites']; spins=compiled['row_spins']
    r=len(g[0]) if g else 0
    if r != n: return {'status':'ZERO','reason':'unequal color populations'}
    if any(i < 0 or i >= n or s not in ('U','D') for i,s in spin_constraints.items()):
        raise ValueError('invalid physical spin constraint')
    forced={x for x in range(2*n) if spin_constraints.get(sites[x]) == spins[x]}
    removed={x for x in range(2*n) if sites[x] in spin_constraints and x not in forced}
    if rank([g[x] for x in sorted(forced)]) != len(forced):
        return {'status':'ZERO','reason':'forced dependent rows'}
    remaining=set(range(2*n))-forced-removed; chosen=set(); target=n-len(forced)
    def linear(v):
        vv=forced|v; return rank([g[x] for x in sorted(vv)]) == len(vv)
    def partition(v):
        return len({sites[x] for x in forced|v}) == len(forced|v)
    while len(chosen) < target:
        outside=remaining-chosen
        sources=[x for x in sorted(outside) if linear(chosen|{x})]
        sinks={x for x in outside if partition(chosen|{x})}
        queue=deque(sources); parent={x:None for x in sources}; end=None
        while queue:
            x=queue.popleft()
            if x in sinks: end=x; break
            if x in chosen:
                successors=[y for y in sorted(outside) if linear((chosen-{x})|{y})]
            else:
                successors=[y for y in sorted(chosen) if partition((chosen-{y})|{x})]
            for y in successors:
                if y not in parent: parent[y]=x; queue.append(y)
        if end is None:
            reachable=set(parent)
            linear_rank=rank([g[x] for x in sorted(forced|(remaining-reachable))])-len(forced)
            partition_rank=len({sites[x] for x in reachable})
            assert linear_rank+partition_rank == len(chosen)
            return {'status':'ZERO','reason':'matroid rank-sum certificate',
                    'maximum_size':len(forced|chosen),'certificate':{
                    'reachable':sorted(reachable),'linear_contracted_rank':linear_rank,
                    'partition_contracted_rank':partition_rank,
                    'upper_total':len(forced)+linear_rank+partition_rank}}
        path=[]; x=end
        while x is not None: path.append(x); x=parent[x]
        chosen ^= set(path)
        assert linear(chosen) and partition(chosen)
    rows=sorted(forced|chosen); up=sorted(sites[x] for x in rows if spins[x] == 'U')
    down=sorted(set(range(n))-set(up))
    amplitude=det(minor(compiled['F'],up,down))
    assert len(up) == k and amplitude
    return {'status':'POSITIVE','up':up,'down':down,'rows':rows,
            'amplitude':amplitude,'weight':amplitude.abs2()}


def physical_coefficient(compiled, up):
    n,k=compiled['n'],compiled['k']; up=sorted(up)
    if len(up) != k: return Q(0)
    down=sorted(set(range(n))-set(up))
    return det(minor(compiled['F'],up,down)).abs2()


def exhaustive_prefix_norm(f, constraints):
    """Small exact diagnostic only: exponential, never the production counter."""
    f=matrix(f); n=len(f); k=n//2; answer=Q(0)
    for up in combinations(range(n),k):
        up=set(up)
        if any(('U' if i in up else 'D') != s for i,s in constraints.items()): continue
        down=sorted(set(range(n))-up)
        answer += det(minor(f,sorted(up),down)).abs2()
    return answer
