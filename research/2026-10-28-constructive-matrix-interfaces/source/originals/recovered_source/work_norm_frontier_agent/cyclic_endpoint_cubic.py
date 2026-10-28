#!/usr/bin/env python3
"""All-source matrix trace cubic counting by cyclic endpoint deletion.

Uniform cost: poly(a,n)*exp(O(sqrt(n))). Fixed nilpotent chain height: poly.
The counter enumerates dimension profiles, not field elements or subspaces.
"""
from collections import Counter,defaultdict
from pathlib import Path
import json,time
from matrix_kloosterman import (Field,eye,mmul,rref,charpoly,factor_polynomial,
                               primary_columns,matrix_kloosterman_from_primary)
from nilpotent_pair_counter import NilpotentPairCounter,choose,canonical_strings

def cyclic_dimensions(parts,m):
    return [sum(sum((c-j)%m==i for j in range(l)) for l,c in parts) for i in range(m)]

def endpoint_deletions(parts,m,color,q,kind,dimension=None):
    """Semisimple endpoint deletion types and exact Gaussian multiplicities.

    'socle': quotient by a socle subspace at color.
    'top': restrict that vertex to a subspace containing its radical.
    """
    if kind not in ('socle','top'):raise ValueError('endpoint kind')
    counts=Counter(tuple(x) for x in parts);eligible={}
    for (l,c),mult in counts.items():
        endpoint=c if kind=='socle' else (c-l+1)%m
        if endpoint==color:eligible[l]=(c,mult)
    lengths=sorted(eligible,reverse=True);out=defaultdict(int)
    def rec(index,old_dim,old_deleted,total,profile,weight):
        if index==len(lengths):
            if dimension is not None and total!=dimension:return
            new=counts.copy()
            for l,u in profile:
                if not u:continue
                c,mult=eligible[l];new[l,c]-=u
                if l>1:
                    cc=(c-1)%m if kind=='socle' else c
                    new[l-1,cc]+=u
            result=tuple(sorted(p for p,mult in new.items() for _ in range(mult)))
            out[total,result]+=weight;return
        l=lengths[index];c,mult=eligible[l]
        for u in range(mult+1):
            if dimension is not None and total+u>dimension:break
            w=choose(mult,u,q)*q**(u*(old_dim-old_deleted))
            rec(index+1,old_dim+mult,old_deleted+u,total+u,profile+[(l,u)],weight*w)
    rec(0,0,0,0,[],1)
    return [(k,state,weight) for (k,state),weight in out.items()]

def suppress_middle_vertex(parts):
    """Compose 0->1->2; retain 2->0. New colors are old0 and old2."""
    out=[]
    for length,c in parts:
        kept=[(c-j)%3 for j in range(length) if (c-j)%3!=1]
        if kept:out.append((len(kept),0 if kept[0]==0 else 1))
    return canonical_strings(out)

class NilpotentCubicCounter:
    def __init__(self,q):
        self.q=q;self.pairs=NilpotentPairCounter(q)
        self.top_profiles=0;self.socle_profiles=0
    def count_signed(self,parts):
        parts=tuple(sorted(tuple(p) for p in parts));dims=cyclic_dimensions(parts,3)
        if len(set(dims))!=1:raise ValueError('initial cubic dimensions must agree')
        n=dims[0];q=self.q;total=0
        for k,after_top,w1 in endpoint_deletions(parts,3,2,q,'top'):
            self.top_profiles+=1
            for kk,after_both,w2 in endpoint_deletions(after_top,3,0,q,'socle',dimension=k):
                self.socle_profiles+=1
                assert kk==k and cyclic_dimensions(after_both,3)==[n-k,n,n-k]
                pair=suppress_middle_vertex(after_both)
                assert sum(l for l,c in pair)==2*(n-k)
                total+=w1*w2*q**(n*k)*self.pairs.count(pair)
        return q**(n*n)*total
    def metadata(self):
        return dict(top_profiles=self.top_profiles,socle_profiles=self.socle_profiles,
                    pair_backend=self.pairs.metadata(),enumerated_field_elements=0,
                    enumerated_subspaces=0)

def cyclic_strings_from_source_ranks(dimensions,ranks,m=3):
    """Acquire an oriented m-cycle, direction i->i+1, from ranks starting k=0."""
    dims=list(dimensions);N=sum(dims)
    if len(dims)!=m or len(ranks)!=m:raise ValueError('color count')
    rs=[]
    for i,row in enumerate(ranks):
        row=list(row)
        if not row or row[0]!=dims[i] or row[-1]!=0:
            raise ValueError('rank sequence must start at dimension and end at zero')
        if any(not isinstance(v,int) or not 0<=v<=dims[i] for v in row):
            raise ValueError('invalid rank')
        row=row[:N+2]+[0]*max(0,N+2-len(row));rs.append(row)
    parts=[]
    for length in range(1,N+1):
        for c in range(m):
            i=(c-length+1)%m;j=(c-length)%m
            mult=rs[i][length-1]-rs[i][length]-rs[j][length]+rs[j][length+1]
            if mult<0:raise ValueError('negative cyclic string multiplicity')
            parts.extend([(length,c)]*mult)
    if cyclic_dimensions(parts,m)!=dims:raise ValueError('incomplete cyclic rank data')
    check=[[0]*(N+2) for _ in range(m)]
    for length,c in parts:
        for j in range(length):
            for k in range(j+1):check[(c-j)%m][k]+=1
    if check!=rs:raise ValueError('inconsistent cyclic rank data')
    return tuple(sorted(parts))

def cubic_from_primary_and_cyclic_ranks(primary_data,matrix_rank,field_h,
                                        source_color_ranks,constant=0):
    """Intrinsic interface: reduced ACB primary data, cyclic ranks of [B,C,A].

    Each source-color list begins at n (k=0), and ends at regular dimension u.
    Regular-action ranks must first be divided by the matrix size as integers.
    """
    F=Field(field_h);n=matrix_rank
    if constant not in (0,1):raise ValueError('binary constant')
    if sum((len(p['irreducible'])-1)*p['multiplicity'] for p in primary_data)!=n:
        raise ValueError('primary dimensions')
    regular=[p for p in primary_data if list(p['irreducible'])!=[0,1]]
    u=sum((len(p['irreducible'])-1)*p['multiplicity'] for p in regular);v=n-u
    Kreg,reg_meta=matrix_kloosterman_from_primary(regular,u,field_h)
    nil_ranks=[[r-u for r in row] for row in source_color_ranks]
    parts=cyclic_strings_from_source_ranks([v,v,v],nil_ranks,3)
    counter=NilpotentCubicCounter(F.q);Snil=counter.count_signed(parts)
    signed=F.q**(u*u+3*u*v)*Kreg*Snil
    bits=3*F.a*n*n;numerator=(1<<bits)+((-1)**constant)*signed
    if numerator%2:raise ArithmeticError('nonintegral Boolean count')
    return numerator//2,dict(original_inputs=bits,matrix_rank=n,field_degree=F.a,
        regular_dimension=u,nilpotent_dimension=v,
        nilpotent_max_chain=max((l for l,c in parts),default=0),
        nilpotent_strings=parts,core_signed_sum=signed,
        signed_sum=((-1)**constant)*signed,constant=constant,regular_backend=reg_meta,
        **counter.metadata())

def cubic_all_sources(A,B,C,field_h=3,constant=0):
    """Count zeros of Tr_{Fq/F2} tr(XYZ+AX+BY+CZ)+constant exactly."""
    F=Field(field_h);n=len(A)
    if len(B)!=n or len(C)!=n or any(len(row)!=n for row in A+B+C):
        raise ValueError('coefficient shape')
    D=mmul(mmul(A,C,F),B,F);cp=charpoly(D,F);primary=[]
    for g,b in factor_polynomial(cp,F):
        primary.append(dict(irreducible=g,multiplicity=b,
                            jordan_columns=primary_columns(D,g,b,F)))
    ranks=[];arrows=[B,C,A]
    for source in range(3):
        current=eye(n);row=[n]
        for k in range(1,3*n+2):
            current=mmul(arrows[(source+k-1)%3],current,F)
            row.append(len(rref(current,F)[1]))
        ranks.append(row)
    return cubic_from_primary_and_cyclic_ranks(primary,n,field_h,ranks,constant)

def cyclic_string_matrices(parts,m=3):
    dims=cyclic_dimensions(parts,m);counts=[0]*m
    arrows=[[[0]*dims[i] for _ in range(dims[(i+1)%m])] for i in range(m)]
    for length,c in parts:
        prev=None
        for j in range(length):
            color=(c-j)%m;i=counts[color];counts[color]+=1
            if prev is not None:
                oldcolor,oldi=prev;assert oldcolor==(color+1)%m
                arrows[color][oldi][i]=1
            prev=(color,i)
    return arrows

def cyclic_string_types(n,m=3):
    options=[((l,c),cyclic_dimensions([(l,c)],m)) for l in range(1,m*n+1) for c in range(m)]
    def rec(start,left,parts):
        if not any(left):yield parts;return
        for i in range(start,len(options)):
            part,dims=options[i]
            if all(a<=b for a,b in zip(dims,left)):
                yield from rec(i,[b-a for a,b in zip(dims,left)],parts+(part,))
    yield from rec(0,[n]*m,())

def checks_binary_spectrum():
    from validate_cubic_spectrum import matrix_from_bits,coefficient_mask
    from matrix_kloosterman import mtrace
    F=Field(3);mats=[matrix_from_bits(x) for x in range(16)];truth=[]
    for word in range(4096):
        X,Y,Z=(mats[(word>>(4*j))&15] for j in range(3))
        truth.append((-1)**mtrace(mmul(mmul(X,Y,F),Z,F)))
    spectrum=truth[:];width=1
    while width<len(spectrum):
        for start in range(0,len(spectrum),2*width):
            for j in range(width):
                x,y=spectrum[start+j],spectrum[start+width+j]
                spectrum[start+j]=x+y;spectrum[start+width+j]=x-y
        width*=2
    cases=[];regular=Counter();start=time.perf_counter()
    for aa,A in enumerate(mats):
        for bb,B in enumerate(mats):
            for cc,C in enumerate(mats):
                mask=coefficient_mask(A)|(coefficient_mask(B)<<4)|(coefficient_mask(C)<<8)
                count,meta=cubic_all_sources(A,B,C)
                assert meta['signed_sum']==spectrum[mask],(A,B,C,meta,spectrum[mask])
                assert count==(4096+spectrum[mask])//2
                regular[meta['regular_dimension']]+=1;cases.append([aa,bb,cc,count])
    result=dict(complete_source_triples=len(cases),independent_truth_table_points=4096,
                regular_dimension_distribution=dict(regular),seconds=time.perf_counter()-start,
                exact_counts=cases)
    Path(__file__).with_name('all_source_cubic_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='exact_counts'},indent=2))

if __name__=='__main__':checks_binary_spectrum()
