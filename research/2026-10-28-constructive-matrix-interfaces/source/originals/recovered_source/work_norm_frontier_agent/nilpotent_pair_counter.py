#!/usr/bin/env python3
"""Exact singular matrix Kloosterman sums by acquired cyclic-quiver strings.

For each fixed maximum alternating nilpotent chain length L this is polynomial
in n and log(q). There is NO claim of a polynomial uniform in L. The counter
enumerates dimension profiles, never finite-field elements or subspaces.
Separate small-field oracles in other files validate this construction.
"""
from functools import lru_cache
from collections import defaultdict
from pathlib import Path
import json,time,sys
from matrix_kloosterman import (Field,gaussian_table,matrix_ramanujan,
                               rref,mmul,eye)


@lru_cache(None)
def gaussian(n,q):
    return gaussian_table(n,q)

def choose(n,k,q):
    return gaussian(n,q)[n][k] if 0<=k<=n else 0

def gl_order(n,q):
    return matrix_ramanujan(n,0,q)

def rank_matrices(rows,cols,r,q):
    if not 0<=r<=min(rows,cols):return 0
    return choose(rows,r,q)*choose(cols,r,q)*gl_order(r,q)


@lru_cache(None)
def disjoint_intersection_count(N,a,b,c,k,j,q):
    """# k-subspaces L of N-space with L cap A=0, dim(L cap B)=j.

    dim A=a, dim B=b, dim(A cap B)=c. Closed Gaussian strata.
    """
    if not (0<=c<=min(a,b) and a+b-c<=N and
            0<=k<=N-a and 0<=j<=min(k,b-c)):
        return 0
    total=0
    for u in range(max(0,k-(N-a-b+c),j),min(k,b-c)+1):
        rm=rank_matrices(u,a-c,u-j,q)
        if not rm:continue
        total+=(choose(b-c,u,q)*choose(N-a-b+c,k-u,q)*
                q**((b-c-u)*(k-u)+a*(k-u)+c*u)*rm)
    return total


@lru_cache(None)
def ambient_weight(n,s,t,b,rank_m,rank_bj,h,v,q):
    """Weighted ambient kernels with a fixed socle subspace H.

    A=E_s, t=rank(B_top), b=rank B, M=B_top J,
    h=dim H, v=dim(H cap ker(BJ)).
    """
    N0=n-t;m=s-rank_m;c0=s-rank_bj;k0=n-s
    if not (0<=h<=min(m,k0) and 0<=v<=min(h,c0)):
        return 0
    N=N0-h;a=m-h;bb=n-b-v;c=c0-v;k=k0-h
    total=0
    for j in range(v,min(k0,n-b)+1):
        count=disjoint_intersection_count(N,a,bb,c,k,j-v,q)
        if count:
            total+=count*matrix_ramanujan(k0,k0-j,q)
    return total


def flag_profile_intersections(block_dims,kernel_block_dims,profile,q):
    """Count H with fixed flag increments and each dim(H cap K0).

    A basis simultaneously adapted to the flag and K0 exists; only their
    intersection dimensions enter. State is the current intersection v.
    """
    dp={0:1};D=C=h=0
    for d,c,u in zip(block_dims,kernel_block_dims,profile):
        if not (0<=c<=d and 0<=u<=d):return {}
        out=defaultdict(int)
        for v,value in dp.items():
            quotient_dim=D-C-h+v
            assert quotient_dim>=0
            for j in range(max(0,u-d+c),min(u,c)+1):
                subspaces=(choose(c,j,q)*choose(d-c,u-j,q)*
                           q**((c-j)*(u-j)))
                free=q**((D-h)*(u-j)+(C-v)*j)
                for z in range(max(0,j-quotient_dim),j+1):
                    count=rank_matrices(j,quotient_dim,j-z,q)
                    if count:out[v+z]+=value*subspaces*free*count
        dp=dict(out);D+=d;C+=c;h+=u
    return dp


def canonical_strings(parts):
    x=tuple(sorted(tuple(p) for p in parts))
    y=tuple(sorted((l,1-c) for l,c in x))
    return min(x,y)


def string_matrices(parts):
    dims=[sum((l+(c==i))//2 for l,c in parts) for i in (0,1)]
    if dims[0]!=dims[1]:raise ValueError('unbalanced string dimensions')
    n=dims[0];A=[[0]*n for _ in range(n)];B=[[0]*n for _ in range(n)]
    cnt=[0,0]
    for length,c in parts:
        prev=None
        for j in range(length):
            color=(c+j)%2;i=cnt[color];cnt[color]+=1
            if prev is not None:
                oldcolor,oldi=prev
                if color==1:A[oldi][i]=1
                else:B[oldi][i]=1
            prev=(color,i)
    return A,B


def partial_permutation_strings(A,B):
    """Canonical strings for a nilpotent partial-permutation pair."""
    n=len(A);out={};incoming=set()
    for color,M in ((1,A),(0,B)):
        for i,row in enumerate(M):
            for j,c in enumerate(row):
                if c:
                    assert c==1 and (color,j) not in out
                    out[color,j]=(1-color,i)
                    assert (1-color,i) not in incoming
                    incoming.add((1-color,i))
    parts=[];seen=set()
    for color in (0,1):
        for i in range(n):
            node=(color,i)
            if node in incoming:continue
            length=1
            while node in out:
                assert node not in seen;seen.add(node)
                node=out[node];length+=1
            assert node not in seen;seen.add(node)
            parts.append((length,node[0]))
    if len(seen)!=2*n:raise ValueError('pair has a directed cycle')
    return canonical_strings(parts)


def acquire_nilpotent_strings(A,B,field_h=3):
    """Acquire all cyclic nilpotent strings from arbitrary field matrices.

    No matrix-unit or string decomposition is an input. Alternating ranks
    determine multiplicities by adjacent differences.
    """
    n=len(A);F=Field(field_h)
    if len(B)!=n or any(len(row)!=n for row in A+B):raise ValueError('shape')
    ranks=[[n],[n]]
    for source_color in (0,1):
        current=eye(n)
        for length in range(1,2*n+2):
            color=(source_color+length-1)%2
            current=mmul(A if color==1 else B,current,F)
            ranks[source_color].append(len(rref(current,F)[1]))
    if ranks[0][2*n] or ranks[1][2*n]:
        raise ValueError('pair has a nonzero regular monodromy component')
    return strings_from_source_ranks(n,ranks)


def strings_from_source_ranks(n,ranks):
    """Recover multiplicities from ranks(T^k restricted to each color)."""
    if len(ranks)!=2 or any(len(r)<2*n+2 or r[0]!=n for r in ranks):
        raise ValueError('need both source-color ranks through length 2n+1')
    if ranks[0][2*n] or ranks[1][2*n]:raise ValueError('non-nilpotent rank data')
    parts=[]
    for length in range(1,2*n+1):
        for c in (0,1):
            i=(c+length-1)%2;j=1-i
            at_least=ranks[i][length-1]-ranks[i][length]
            longer=ranks[j][length]-ranks[j][length+1]
            multiplicity=at_least-longer
            if multiplicity<0:raise ArithmeticError('invalid alternating ranks')
            parts.extend([(length,c)]*multiplicity)
    if sum(l for l,c in parts)!=2*n:raise ArithmeticError('incomplete strings')
    return canonical_strings(parts)


def nilpotent_pair_from_alternating_ranks(matrix_rank,field_degree,
                                         ranks_start_A,ranks_start_B):
    """Intrinsic interface needing no matrix units.

    The sequences are ranks of A, AB, ABA, ... and B, BA, BAB, ...,
    respectively. Both must terminate at zero. Their ranks are over Fq;
    regular-action ranks in an acquired matrix algebra must first be divided
    by its matrix size, as an integer operation.
    """
    n=matrix_rank;a=field_degree
    x=list(ranks_start_A);y=list(ranks_start_B)
    if n<0 or a<1 or not x or len(x)!=len(y) or x[-1] or y[-1]:
        raise ValueError('invalid or nonterminated alternating rank sequences')
    if any(not isinstance(v,int) or not 0<=v<=n for v in x+y):
        raise ValueError('invalid ranks')
    if len(x)>2*n+1:x=x[:2*n+1];y=y[:2*n+1]
    x += [0]*(2*n+1-len(x));y += [0]*(2*n+1-len(y))
    ranks=[[n],[n]]
    for k in range(1,2*n+2):
        ranks[0].append(y[k-1] if k%2 else x[k-1])
        ranks[1].append(x[k-1] if k%2 else y[k-1])
    parts=strings_from_source_ranks(n,ranks)
    # Check the reconstructed rank data rather than accepting inconsistent
    # arbitrary integer sequences that happen to have nonnegative differences.
    counts=[[0]*(2*n+2) for _ in range(2)]
    for length,c in parts:
        for j in range(length):
            for k in range(j+1):counts[(c+j)%2][k]+=1
    # Canonical color interchange can exchange the two rank sequences.
    if counts!=ranks and counts[::-1]!=ranks:raise ValueError('inconsistent cyclic rank data')
    counter=NilpotentPairCounter(1<<a);value=counter.count(parts)
    return value,dict(matrix_rank=n,field_degree=a,
                      max_chain_length=max((l for l,c in parts),default=0),
                      strings=parts,**counter.metadata())


class NilpotentPairCounter:
    def __init__(self,q):
        if q<2:raise ValueError('field order')
        self.q=q;self.cache={};self.profile_count=0;self.weight_calls=0

    def count(self,parts):
        key=canonical_strings(parts)
        if key in self.cache:return self.cache[key]
        A,B=string_matrices(key);n=len(A);q=self.q
        ra=sum(map(sum,A));rb=sum(map(sum,B))
        if min(ra,rb)==0:
            value=matrix_ramanujan(n,max(ra,rb),q)
        elif max(ra,rb)==n:
            value=(-1)**n*q**(n*(n-1)//2)
        else:
            if rb<ra:A,B=B,A;ra,rb=rb,ra
            value=self._reduce(A,B,ra,rb,max(l for l,c in key))
        self.cache[key]=value
        return value

    def _reduce(self,A,B,s,b,max_height):
        n=len(A);q=self.q
        # Independent coordinate permutations put the partial permutation A=E_s.
        pivots=[(i,j) for i,row in enumerate(A) for j,x in enumerate(row) if x]
        rows=[i for i,j in pivots];cols=[j for i,j in pivots]
        rows += [i for i in range(n) if i not in rows]
        cols += [i for i in range(n) if i not in cols]
        B=[[B[i][j] for j in rows] for i in cols]
        M=[row[:s] for row in B[:s]]
        top=B[:s];bj=[row[:s] for row in B]
        t=sum(map(sum,top));rank_m=sum(map(sum,M));rank_bj=sum(map(sum,bj))
        V0={i for i,row in enumerate(top) if any(row)}
        im_m={i for i,row in enumerate(M) if any(row)}
        U={j for j in range(s) if not any(M[i][j] for i in range(s))}
        K0={j for j in range(s) if not any(bj[i][j] for i in range(n))}
        def image(S):return {i for i,row in enumerate(M) if any(row[j] for j in S)}
        powers=[set(range(s))];v_powers=[V0]
        while powers[-1]:
            powers.append(image(powers[-1]));v_powers.append(image(v_powers[-1]))
        # Ascending interleaved socle flag, deleting repeated steps.
        flag=[set()]
        for j in range(len(powers)-2,-1,-1):
            for S in (U & v_powers[j],U & powers[j]):
                assert flag[-1]<=S
                if S!=flag[-1]:flag.append(S)
        assert flag[-1]==U
        blocks=[sorted(flag[i]-flag[i-1]) for i in range(1,len(flag))]
        dims=[len(x) for x in blocks]
        kdims=[len(set(x)&K0) for x in blocks]
        total=0
        def profiles(i,chosen,h):
            if i==len(dims):
                if t-rank_m<=h<=n-s:yield tuple(chosen)
                return
            for u in range(min(dims[i],n-s-h)+1):
                yield from profiles(i+1,chosen+[u],h+u)
        for profile in profiles(0,[],0):
            self.profile_count+=1;h=sum(profile)
            counts=flag_profile_intersections(dims,kdims,profile,q)
            weighted=0
            for v,count in counts.items():
                self.weight_calls+=1
                weighted+=count*ambient_weight(n,s,t,b,rank_m,rank_bj,h,v,q)
            if not weighted:continue
            H={j for block,u in zip(blocks,profile) for j in block[:u]}
            quotient=[j for j in range(s) if j not in H]
            P=[[0]*s for _ in range(s)];Q=[[0]*s for _ in range(s)]
            for i,j in enumerate(quotient):
                P[i][j]=1
                for z in range(s):Q[z][i]=M[z][j]
            extra=sorted(V0-im_m)
            assert len(extra)<=h
            for k,j in enumerate(extra):Q[j][s-h+k]=1
            parts=partial_permutation_strings(P,Q)
            assert max((l for l,c in parts),default=0)<=max_height
            total+=weighted*self.count(parts)
        return q**(s*(n-s))*total

    def metadata(self):
        return dict(states=len(self.cache),dimension_profiles=self.profile_count,
                    ambient_weight_calls=self.weight_calls,enumerated_field_elements=0,
                    enumerated_subspaces=0)


def nilpotent_pair(A,B,field_h=3,max_chain_length=None):
    F=Field(field_h);parts=acquire_nilpotent_strings(A,B,field_h)
    L=max((l for l,c in parts),default=0)
    if max_chain_length is not None and L>max_chain_length:
        raise ValueError('acquired nilpotency length exceeds requested bound')
    counter=NilpotentPairCounter(F.q);value=counter.count(parts)
    return value,dict(matrix_rank=len(A),field_degree=F.a,max_chain_length=L,
                      strings=parts,**counter.metadata())


def checks():
    start=time.perf_counter();rows=[]
    data=json.loads(Path(__file__).with_name('nilpotent_strings_n4.json').read_text())
    counter=NilpotentPairCounter(2)
    for item in data['data']:
        value=counter.count(item['strings'])
        assert value==item['K'],(item,value)
    rows.append(dict(n=4,q=2,types=len(data['data']),GL_oracle_matrices=data['GL_size'],
                     **counter.metadata()))
    # Every binary dimension-three nilpotent pair, via the saved complete spectrum.
    d3=json.loads(Path(__file__).with_name('pair_spectrum_results.json').read_text())[-1]
    counter3=NilpotentPairCounter(2);total_pairs=0
    for item in d3['nilpotent_type_data']:
        aa,bb=item['representative'];n=3
        A=[[(aa>>(i*n+j))&1 for j in range(n)] for i in range(n)]
        B=[[(bb>>(i*n+j))&1 for j in range(n)] for i in range(n)]
        parts=acquire_nilpotent_strings(A,B,3)
        value=counter3.count(parts)
        assert value==item['K'],(item,parts,value)
        total_pairs+=item['pairs']
    rows.append(dict(n=3,q=2,acquired_types=len(d3['nilpotent_type_data']),
                     oracle_pairs_covered_by_validated_orbit_invariance=total_pairs,
                     **counter3.metadata()))
    result=dict(checks=rows,seconds=time.perf_counter()-start)
    Path(__file__).with_name('nilpotent_pair_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))

if __name__=='__main__':checks()
