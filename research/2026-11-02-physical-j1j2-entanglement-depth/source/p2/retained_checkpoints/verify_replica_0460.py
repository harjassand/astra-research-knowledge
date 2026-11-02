#!/usr/bin/env python3
"""Exact integer-arithmetic spectral certificate for every <=4-site connected
interaction motif of square-lattice spin-1/2 J1-J2 at J2/J1=1/2.

No floating eigensolvers, external packages, or assumed physical gap.
"""
from fractions import Fraction
from itertools import permutations
from collections import defaultdict
from math import lcm
import json, sys, hashlib
from pathlib import Path

SHIFT=Fraction(23,50)  # 0.46 per spin: conservative fully rational threshold
NEIGHBORS=((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1))

def edge_weight(p,q):
    dx=abs(p[0]-q[0]); dy=abs(p[1]-q[1])
    if dx+dy==1:return Fraction(1)
    if dx==1 and dy==1:return Fraction(1,2)
    return Fraction(0)

def canonical_key(w):
    n=len(w)
    return min(tuple(int(2*w[p[i]][p[j]]) for i in range(n) for j in range(i)) for p in permutations(range(n)))

def shapes(max_k=4):
    prev={frozenset(((0,0),))}; classes={}
    for k in range(1,max_k+1):
        newclasses={}
        for shape in prev:
            pts=sorted(shape)
            w=[[edge_weight(pts[i],pts[j]) for j in range(k)] for i in range(k)]
            key=canonical_key(w)
            if key not in newclasses:newclasses[key]={'points':pts,'w':w}
        classes[k]=dict(sorted(newclasses.items(), key=lambda it:it[0]))
        if k==max_k:break
        nextset=set()
        for shape in prev:
            for x,y in shape:
                for dx,dy in NEIGHBORS:
                    p=(x+dx,y+dy)
                    if p in shape:continue
                    candidate=shape | {p}
                    xm=min(s[0] for s in candidate); ym=min(s[1] for s in candidate)
                    nextset.add(frozenset((a-xm,b-ym) for a,b in candidate))
        prev=nextset
    return classes

def add_dot(rows,n,i,j,J):
    """Add J*S_i.S_j on n spin-1/2 sites in computational basis."""
    if not J:return
    for state in range(1<<n):
        bi=(state>>i)&1; bj=(state>>j)&1
        rows[state][state]+= J*Fraction(1 if bi==bj else -1,4)
        if bi!=bj:
            flipped=state^(1<<i)^(1<<j)
            rows[flipped][state]+=J*Fraction(1,2)

def replica_matrix(w):
    k=len(w); n=2*k; d=1<<n
    rows=[defaultdict(Fraction) for _ in range(d)]
    # W=(H(copy1)+H(copy2))/2 - sum_(i,j)A_ij S_i(1).S_j(2)
    for i in range(k):
        for j in range(i):
            if w[i][j]:
                add_dot(rows,n,i,j,w[i][j]/2)
                add_dot(rows,n,i+k,j+k,w[i][j]/2)
    for i in range(k):
        for j in range(k):
            a=(Fraction(1) if i==j else Fraction(0))+w[i][j]/2
            add_dot(rows,n,i,j+k,-a)
    for state in range(d):rows[state][state]+=k*SHIFT
    return rows

def bareiss_positive_definite(a):
    """Fraction-free exact Sylvester test, returns first failing pivot or summary.
       If all leading principal minors are positive the Hermitian matrix is SPD.
       Every division is exact and checked."""
    n=len(a)
    if not n:return {'pass':True,'n':0,'last_pivot_digits':0}
    m=[row[:] for row in a]; previous=1
    for j in range(n):
        pivot=m[j][j]
        if pivot<=0:return {'pass':False,'pivot_index':j,'pivot':str(pivot)}
        if j==n-1:break
        for i in range(j+1,n):
            mik=m[i][j]
            for h in range(i,n):
                numerator=pivot*m[i][h]-mik*m[j][h]
                q,r=divmod(numerator,previous)
                if r: raise AssertionError(f'nonexact Bareiss division in {n}x{n} at {j},{i},{h}')
                m[i][h]=q
                m[h][i]=q
            m[i][j]=m[j][i]=0
        previous=pivot
    return {'pass':True,'n':n,'last_pivot_digits':len(str(m[-1][-1]))}

def witness(w):
    k=len(w);raw=replica_matrix(w);n=2*k
    den=lcm(*[v.denominator for row in raw for v in row.values()]); assert den>0
    assert all(raw[i].get(j,Fraction(0))==raw[j].get(i,Fraction(0)) for i in range(1<<n) for j in raw[i])
    groups=defaultdict(list)
    for state in range(1<<n):groups[state.bit_count()].append(state)
    evidence=[]
    for mag,idx in sorted(groups.items()):
        vals=[[int(raw[i].get(j,0)*den) for j in idx] for i in idx]
        # exactly preserves total S_z (no off-sector matrix elements)
        assert all((j.bit_count()==i.bit_count()) or (v==0) for i,row in enumerate(raw) for j,v in row.items())
        outcome=bareiss_positive_definite(vals)
        if not outcome['pass']:raise AssertionError(f'NOT SPD k={k} M={mag} outcome={outcome}')
        evidence.append({'magnetization_up':mag,**outcome})
    return {'denominator':den,'sector_dims':[x['n'] for x in evidence],
            'largest_sector':max(x['n'] for x in evidence),
            'all_sectors_pass':all(x['pass'] for x in evidence),
            'max_pivot_digits':max(x['last_pivot_digits'] for x in evidence)}

def run():
    cs=shapes(4);out={'proof':'Two-replica exact integer SPD for k<=4','energy_lower_per_site':'-23/50',
        'coupling':'J2/J1=1/2','counts':{},'cases':[]}
    for k,items in cs.items():
        out['counts'][k]=len(items)
        for key,data in items.items():
            w=data['w'];res=witness(w)
            print(f'k={k} edges={key} sector_max={res["largest_sector"]} SPD PASS',flush=True)
            out['cases'].append({'k':k,'geometry':data['points'],'pair_weights_key':key,**res})
    assert out['counts']=={1:1,2:2,3:4,4:15},out['counts']
    out['cases_verified']=len(out['cases'])
    base=Path(__file__).resolve().parent
    (base/'REPLICA_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print('ALL EXACT CASES PASS',out['counts'])
if __name__=='__main__':run()
