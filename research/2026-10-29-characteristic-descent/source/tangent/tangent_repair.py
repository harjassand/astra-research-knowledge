"""Exact characteristic-two tensor repair experiments; no external solver.

Native AlphaTensor data: Fawzi et al., Nature 610 (2022), CC-BY 4.0.
Own code. The tensor uses the authors' cyclic output convention (AB)^T.
All linear algebra below uses Python integers as exact GF(2) bit vectors.
"""
from pathlib import Path
import argparse, hashlib, json, time
import numpy as np

HERE = Path(__file__).resolve().parent


def bits(x):
    return int.from_bytes(np.packbits(np.asarray(x, dtype=np.uint8).ravel(),
                                      bitorder='little').tobytes(), 'little')


def vec(x, n):
    return np.array([(x >> i) & 1 for i in range(n)], dtype=np.int64)


def columns(a, b, c):
    """Derivative of a tensor term at (a,b,c), ordered a,b,c."""
    n = len(a)
    bc = bits(np.outer(b, c))
    # Explicit indexing avoids depending on a Kronecker/vectorization convention.
    out = [bc << (n*n*i) for i in range(n)]
    for j in range(n):
        out.append(sum(1 << int(i*n*n+j*n+k) for i in np.flatnonzero(a)
                       for k in np.flatnonzero(c)))
    for k in range(n):
        out.append(sum(1 << int(i*n*n+j*n+k) for i in np.flatnonzero(a)
                       for j in np.flatnonzero(b)))
    return out


class Image:
    """A column-echelon basis, with optional exact generating-column track."""
    def __init__(self, cols=(), track=False):
        self.basis = {}
        self.track = track
        self.generators = []
        for col in cols:
            self.add(col)

    def reduce(self, col):
        remainder = 0
        while col:
            p = col.bit_length()-1
            if p not in self.basis:
                remainder |= 1 << p
                col ^= 1 << p
            else:
                col ^= self.basis[p][0]
        return remainder

    def add(self, col):
        j = len(self.generators)
        self.generators.append(col)
        comb = 1 << j if self.track else 0
        while col:
            p = col.bit_length()-1
            if p not in self.basis:
                self.basis[p] = (col, comb)
                return True
            row, code = self.basis[p]
            col ^= row
            comb ^= code
        return False

    def solve(self, col):
        comb = 0
        while col:
            p = col.bit_length()-1
            if p not in self.basis:
                return None
            row, code = self.basis[p]
            col ^= row
            comb ^= code
        return comb


def tensor(shape):
    n, m, p = shape
    t = np.zeros((n*m, m*p, p*n), dtype=np.int64)
    for i in range(n):
        for j in range(m):
            for k in range(p):
                t[i*m+j,j*p+k,k*n+i] = 1
    return t


def load(key='4,4,4'):
    native = np.load(HERE/'factorizations_f2.npz', allow_pickle=False)
    factors = np.array(native[key], dtype=np.int64)
    shape = tuple(map(int,key.split(',')))
    t = tensor(shape)
    reconstructed = np.einsum('ir,jr,kr->ijk', *factors, optimize=True)
    assert np.array_equal(reconstructed % 2, t)
    assert np.all((factors == 0) | (factors == 1))
    return factors, t


def jacobian(factors):
    return [c for r in range(factors.shape[2])
            for c in columns(*factors[:,:,r])]


def defect(factors, t, modulus=2):
    r = t - np.einsum('ir,jr,kr->ijk', *factors, optimize=True)
    assert np.all(r % modulus == 0)
    return bits((r//modulus) % 2)


def expand(factors, i, j, perm):
    """The standard integer plus identity, then reduced mod 2.

    a b c + d e f = a(b+e)c + ae(f-c) + (d-a)ef.
    """
    out = np.delete(factors, [i,j], axis=2)
    src = factors[list(perm)]
    a,b,c = src[:,:,i]
    d,e,f = src[:,:,j]
    terms = np.stack((np.stack((a,(b+e)%2,c)),
                      np.stack((a,e,(f-c)%2)),
                      np.stack(((d-a)%2,e,f))), axis=2)
    unperm = np.argsort(perm)
    return np.concatenate((out,terms[unperm]), axis=2)


def flips(factors):
    """All ordered single flips, with a canonical cyclic order of other modes."""
    import itertools
    r=factors.shape[2]
    for mode in range(3):
        perm=(mode,(mode+1)%3,(mode+2)%3)
        groups={}
        for i in range(r):
            groups.setdefault(bits(factors[mode,:,i]),[]).append(i)
        for group in groups.values():
            for i,j in itertools.permutations(group,2):
                yield mode,perm,i,j


def do_flip(factors,perm,i,j):
    out=factors.copy()
    out[perm[1],:,i]^=out[perm[1],:,j]
    out[perm[2],:,j]^=out[perm[2],:,i]
    nonzero=np.all(np.any(out,axis=1),axis=0)
    return out[:,:,nonzero]


def plus_then_flip():
    """Exhaustive two-step repair, with only necessary quotient pruning.

    Survivors of the union-image test receive the ENTIRE new Jacobian solve.
    This matters: a flip does not preserve the old tangent image.
    """
    import itertools
    from collections import Counter
    begin=time.perf_counter()
    f,t=load()
    base=Image(jacobian(f))
    rr=base.reduce(defect(f,t))
    n=f.shape[1]
    rank=f.shape[2]
    seen=set()
    plus=0
    candidate_count=0
    union_survivors=0
    hits=[]
    rankcounts=Counter()
    for perm in itertools.permutations(range(3)):
        ff=f[list(perm)]
        for i in range(rank):
            for j in range(rank):
                if i==j: continue
                candidate=expand(f,i,j,perm)
                canon=tuple(sorted(tuple(bits(candidate[k,:,r]) for k in range(3))
                                   for r in range(candidate.shape[2])))
                if canon in seen: continue
                seen.add(canon)
                plus+=1
                a,b,c=ff[:,:,i]
                d,e,g=ff[:,:,j]
                central=np.stack((a,e,(g+c)%2))[np.argsort(perm)]
                reduced=[base.reduce(x) for x in columns(*central)]
                extra=Image(reduced)
                rplus=extra.reduce(rr)
                assert rplus
                for mode,p,k,l in flips(candidate):
                    candidate_count+=1
                    # The union of old/new flip tangent images adds just
                    # delta(shared) tensor other_l tensor last_k.
                    cross=candidate[:,:,k].copy()
                    cross[p[1]]=candidate[p[1],:,l]
                    newcols=columns(*cross)[mode*n:(mode+1)*n]
                    reduced_cross=[extra.reduce(base.reduce(x)) for x in newcols]
                    added=Image(reduced_cross)
                    if added.reduce(rplus):
                        continue
                    union_survivors+=1
                    repaired=do_flip(candidate,p,k,l)
                    assert np.array_equal(np.einsum('ir,jr,kr->ijk',*repaired)%2,t)
                    full=Image(jacobian(repaired))
                    feasible=full.reduce(defect(repaired,t))==0
                    rankcounts[len(full.basis)]+=1
                    if feasible:
                        path={'plus_perm':list(perm),'plus_i':i,'plus_j':j,
                              'flip_mode':mode,'flip_i':k,'flip_j':l,
                              'tensor_rank':repaired.shape[2],
                              'jacobian_rank':len(full.basis)}
                        hits.append(path)
                        np.save(HERE/f'repaired_{len(hits):03d}.npy',repaired)
        print(json.dumps({'permutation':perm,'distinct_plus':plus,
                          'flip_candidates':candidate_count,
                          'union_survivors':union_survivors,'hits':len(hits),
                          'elapsed':time.perf_counter()-begin}),flush=True)
    result={'distinct_plus_states':plus,'ordered_flip_candidates':candidate_count,
            'union_survivors':union_survivors,'full_jacobian_rank_counts':dict(rankcounts),
            'mod4_hits':hits,'elapsed_seconds':time.perf_counter()-begin}
    (HERE/'PLUS_FLIP_SCAN.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def single_plus_scan(key='4,4,4', limit=None):
    start=time.perf_counter()
    f,t=load(key)
    cols=jacobian(f)
    base=Image(cols)
    r=defect(f,t)
    rr=base.reduce(r)
    assert rr
    init=time.perf_counter()-start
    n=f.shape[1]
    rank=f.shape[2]
    tested=0
    hits=[]
    # Six mode permutations are needed for a genuinely ordered plus move.
    import itertools
    records=[]
    for perm in itertools.permutations(range(3)):
        ff=f[list(perm)]
        for i in range(rank):
            for j in range(rank):
                if i==j:
                    continue
                a,b,c=ff[:,:,i]
                d,e,g=ff[:,:,j]
                # Undo mode permutation before using the base image.
                central=np.stack((a,e,(g+c)%2))[np.argsort(perm)]
                cross=columns(*central)
                reduced=[base.reduce(x) for x in cross]
                extra=Image(reduced)
                feasible=extra.reduce(rr)==0
                tested+=1
                if feasible:
                    candidate=expand(f,i,j,perm)
                    assert np.array_equal(np.einsum('ir,jr,kr->ijk',*candidate)%2,t)
                    actual=Image(jacobian(candidate))
                    assert actual.reduce(defect(candidate,t))==0
                    path={'perm':list(perm),'i':i,'j':j,
                          'extra_rank':len(extra.basis),
                          'new_rank':len(actual.basis)}
                    hits.append(path)
                    np.save(HERE/f'candidate_{len(hits):03d}.npy',candidate)
                records.append((len(extra.basis),feasible))
                if limit and tested>=limit:
                    break
            if limit and tested>=limit:
                break
        if limit and tested>=limit:
            break
    from collections import Counter
    result={'key':key,'native_shape':list(f.shape),'tensor_identity_mod2':True,
            'base_jacobian_rank':len(base.basis),'base_lifts_mod4':False,
            'initialization_seconds':init,'tested_ordered_plus_moves':tested,
            'extra_rank_counts':dict(Counter(x[0] for x in records)),
            'mod4_hits':hits,'elapsed_seconds':time.perf_counter()-start,
            'native_sha256':hashlib.sha256((HERE/'factorizations_f2.npz').read_bytes()).hexdigest()}
    (HERE/'PLUS_SCAN.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--limit',type=int)
    ap.add_argument('--key',default='4,4,4')
    ap.add_argument('--plus-flip',action='store_true')
    a=ap.parse_args()
    print(json.dumps(plus_then_flip() if a.plus_flip else single_plus_scan(a.key,a.limit),indent=2))
