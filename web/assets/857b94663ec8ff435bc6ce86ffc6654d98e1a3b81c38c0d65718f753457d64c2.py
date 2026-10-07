#!/usr/bin/env python3
"""Bounded independent exact identities for the whole-axial audit.

No peer imports, floating exponentials, optimizer, or generic iid backend.
Dense fixtures are restricted to N<=4. Larger-N checks are combinatorial.
They can falsify the formulas; the all-N proof is in WHOLE_AXIAL_AUDIT.txt.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import datetime
import hashlib
import json
import signal
import time


def bc(n, r):
    return comb(n, r) if 0 <= r <= n else 0


def sector(n, b, k):
    return F((n - 2*b + 1)*(bc(n-k,b)-bc(n-k,b-k-1)),
             (k+1)*2**(n-k))


def zero(d):
    return [[F(0) for _ in range(d)] for _ in range(d)]


def identity(d):
    a = zero(d)
    for i in range(d):
        a[i][i] = F(1)
    return a


def mm(a,b):
    d = len(a)
    return [[sum((a[i][r]*b[r][j] for r in range(d)),F(0))
             for j in range(d)] for i in range(d)]


def linear(a, b, ca=F(1), cb=F(1)):
    return [[ca*x+cb*y for x,y in zip(ar,br)] for ar,br in zip(a,b)]


def trace_pair(a,b):
    return sum((a[i][j]*b[j][i] for i in range(len(a))
                for j in range(len(a))),F(0))


def bits(x,n):
    return tuple((x>>i)&1 for i in range(n))


def j2(n):
    d = 2**n
    a = zero(d)
    for x in range(d):
        a[x][x] = F(n*(4-n),4)
        for i,j in combinations(range(n),2):
            y = x
            if ((x>>i)&1) != ((x>>j)&1):
                y ^= (1<<i)|(1<<j)
            a[y][x] += 1
    return a


def projector(n,b):
    d = 2**n
    a = identity(d)
    q = j2(n)
    lb = F((n-2*b)*(n-2*b+2),4)
    for c in range(n//2+1):
        if c == b:
            continue
        lc = F((n-2*c)*(n-2*c+2),4)
        factor = linear(q,identity(d),F(1,1)/(lb-lc),-lc/(lb-lc))
        a = mm(a,factor)
    return a


def direct_k(n,k):
    d = 2**n
    a = zero(d)
    norm = comb(n,k)*(k+1)*2**(n-k)
    for subset in combinations(range(n),k):
        rest = tuple(i for i in range(n) if i not in subset)
        for x in range(d):
            xb = bits(x,n)
            lx = sum(xb[i] for i in subset)
            for y in range(d):
                yb = bits(y,n)
                if any(xb[i] != yb[i] for i in rest):
                    continue
                if sum(yb[i] for i in subset) != lx:
                    continue
                a[x][y] += F(1,norm*comb(k,lx))
    return a


def direct_branches(n,weights,values):
    d = 2**n
    out = zero(d)
    beta = F(0)
    for k in range(n+1):
        r = n-k
        for u in range(r+1):
            z = sum(values[u:u+k+1],F(0))
            b = weights[k]*F(comb(r,u),(k+1)*2**r)*z
            beta += b
            for subset in combinations(range(n),k):
                rest = tuple(i for i in range(n) if i not in subset)
                for ones in combinations(rest,u):
                    complement = {i:int(i in ones) for i in rest}
                    coefficient = b/F(comb(n,k)*comb(r,u),1)
                    for x in range(d):
                        xb = bits(x,n)
                        if any(xb[i] != complement[i] for i in rest):
                            continue
                        l = sum(xb[i] for i in subset)
                        for y in range(d):
                            yb = bits(y,n)
                            if any(yb[i] != complement[i] for i in rest):
                                continue
                            if sum(yb[i] for i in subset) != l:
                                continue
                            out[x][y] += coefficient*values[u+l]/(z*comb(k,l))
    return out,beta


def kron(a,b):
    return [[a[i][j]*b[r][s] for j in range(len(a))
             for s in range(len(b))] for i in range(len(a))
             for r in range(len(b))]


def power(a,k):
    out = [[F(1)]]
    for _ in range(k):
        out = kron(out,a)
    return out


def rational_tilt(sigma,diagonal):
    a = sum((diagonal[i]**2*sigma[i][i] for i in range(2)),F(0))
    return [[diagonal[i]*diagonal[j]*sigma[i][j]/a
             for j in range(2)] for i in range(2)],a


def exact_weighted_power(atoms,weights,k):
    out = zero(2**k)
    for atom,w in zip(atoms,weights):
        out = linear(out,power(atom,k),F(1),w)
    return out


def run():
    t0=time.monotonic()
    checks=0
    combinatorial_cases=0
    for n in range(1,65):
        m=n//2+1
        columns=[[sector(n,b,k) for b in range(m)] for k in range(n+1)]
        for k,col in enumerate(columns):
            assert all(v>=0 for v in col)
            assert sum(col,F(0))==1
            checks+=2
            combinatorial_cases+=1
        assert columns[n]==[F(int(b==0)) for b in range(m)]
        dimensions=[(n-2*b+1)*(bc(n,b)-bc(n,b-1)) for b in range(m)]
        assert sum(dimensions)==2**n
        assert all(columns[0][b]==F(dimensions[b],2**n) for b in range(m))
        checks+=3

        # Exact Frobenius derivative bound for the diagonal-slack embedding.
        rows=[]
        for k in range(n):
            rows.append([F(int(i==k)) for i in range(n)]+[F(0)]*m)
        rows.append([-F(1)]*n+[F(0)]*m)
        for b in range(m):
            v=[columns[k][b]-columns[n][b] for k in range(n)]
            eb=[F(int(c==b)) for c in range(m)]
            rows += [v+eb,[-x for x in v]+eb,[F(0)]*n+eb,
                     [F(0)]*n+[-x for x in eb]]
        assert len(rows)==n+1+4*m
        assert all(sum((x*x for x in row),F(0))<=n+1 for row in rows)
        assert sum((x*x for row in rows for x in row),F(0))<=16*(n+1)**2
        checks+=3

    dense_sector_cases=0
    branch_entry_checks=0
    for n in range(1,5):
        d=2**n
        projectors=[projector(n,b) for b in range(n//2+1)]
        ptotal=zero(d)
        for b,p in enumerate(projectors):
            assert mm(p,p)==p
            assert sum(p[i][i] for i in range(d))==(n-2*b+1)*(bc(n,b)-bc(n,b-1))
            ptotal=linear(ptotal,p)
            checks+=2
        assert ptotal==identity(d)
        checks+=1
        ks=[]
        for k in range(n+1):
            a=direct_k(n,k)
            ks.append(a)
            assert sum(a[i][i] for i in range(d))==1
            assert mm(j2(n),a)==mm(a,j2(n))
            checks+=2
            for b,p in enumerate(projectors):
                assert trace_pair(p,a)==sector(n,b,k)
                checks+=1
                dense_sector_cases+=1
        denom=(n+1)*(n+2)//2
        weights=[F(k+1,denom) for k in range(n+1)]
        values=[F(3)**(2*t-n)/F(7)**((2*t-n)**2) for t in range(n+1)]
        mixture=zero(d)
        for w,a in zip(weights,ks):
            mixture=linear(mixture,a,F(1),w)
        filtered=[[values[x.bit_count()]*mixture[x][y] for y in range(d)]
                  for x in range(d)]
        by_branch,beta=direct_branches(n,weights,values)
        assert filtered==by_branch
        assert sum(filtered[x][x] for x in range(d))==beta
        checks+=d*d+1
        branch_entry_checks+=d*d

    atoms=[[[F(1,3),F(1,7)],[F(1,7),F(2,3)]],
           [[F(4,5),-F(1,9)],[-F(1,9),F(1,5)]]]
    weights=[F(2,7),F(5,7)]
    tilt_cases=0
    for k in range(1,5):
        for diagonal in ([F(2,5),F(1)],[F(1),F(3,7)]):
            pairs=[rational_tilt(s,diagonal) for s in atoms]
            normalizer=sum((w*a**k for w,(_,a) in zip(weights,pairs)),F(0))
            new_weights=[w*a**k/normalizer for w,(_,a) in zip(weights,pairs)]
            new_atoms=[s for s,_ in pairs]
            for s in new_atoms:
                assert s[0][0]+s[1][1]==1
                assert s[0][0]*s[1][1]-s[0][1]*s[1][0]>=0
                checks+=2
            transformed=exact_weighted_power(new_atoms,new_weights,k)
            original=exact_weighted_power(atoms,weights,k)
            dd=[power([[diagonal[0],F(0)],[F(0),diagonal[1]]],k)[i][i]
                for i in range(2**k)]
            direct=[[dd[i]*original[i][j]*dd[j]/normalizer
                     for j in range(2**k)] for i in range(2**k)]
            assert transformed==direct
            checks+=4**k
            tilt_cases+=1

    return {'status':'PASS','assertion_count':checks,
            'combinatorial_N_range':[1,64],
            'combinatorial_column_cases':combinatorial_cases,
            'dense_N_range':[1,4], 'dense_sector_pair_cases':dense_sector_cases,
            'filtered_branch_matrix_entries_compared':branch_entry_checks,
            'mixed_atom_rational_tilt_cases':tilt_cases,
            'elapsed_seconds':time.monotonic()-t0,
            'scope':'exact finite identities only, not the all-N proof or generic optimizer execution'}


if __name__=='__main__':
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('30-second audit cap')))
    signal.alarm(30)
    result=run()
    result['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    result['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out=Path(__file__).with_name('independent_exact_checks.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
