#!/usr/bin/env python3
"""Complete singular-pair counter using only endpoint Hall operations.

Embed K(A,B)=q^-n² S(I,A,B), delete endpoints, and recurse. The sole
same-size leaf has one unit coefficient and an immediate value. This form
is intended for testing Hall/Cauchy resummation of the partition states.
"""
from pathlib import Path
import json,time
from matrix_kloosterman import matrix_ramanujan
from nilpotent_pair_counter import canonical_strings,NilpotentPairCounter
from cyclic_endpoint_cubic import endpoint_deletions,suppress_middle_vertex,cyclic_dimensions

def expand_pair_to_identity_cubic(parts):
    """S(I,A,B): old0 becomes new1; old1 becomes new(0,2)."""
    return tuple(sorted((length+sum((c+j)%2==1 for j in range(length)),
                         1 if c==0 else 0) for length,c in parts))

class EndpointPairCounter:
    def __init__(self,q):
        self.q=q;self.cache={};self.top_profiles=0;self.socle_profiles=0
    def count(self,parts):
        key=canonical_strings(parts)
        if key in self.cache:return self.cache[key]
        n=sum(l for l,c in key)//2;q=self.q
        if sum(sum((c+j)%2==0 for j in range(l)) for l,c in key)!=n:
            raise ValueError('unbalanced pair')
        ra=sum(sum((c+j)%2==1 for j in range(1,l)) for l,c in key)
        rb=sum(l-1 for l,c in key)-ra
        if min(ra,rb)==0:value=matrix_ramanujan(n,max(ra,rb),q)
        elif max(ra,rb)==n:value=(-1)**n*q**(n*(n-1)//2)
        else:
            triple=expand_pair_to_identity_cubic(key)
            assert cyclic_dimensions(triple,3)==[n,n,n]
            value=0
            for k,after_top,w1 in endpoint_deletions(triple,3,2,q,'top'):
                self.top_profiles+=1
                for kk,after_both,w2 in endpoint_deletions(after_top,3,0,q,'socle',k):
                    self.socle_profiles+=1;assert kk==k
                    if k==0:leaf=(-1)**n*q**(n*(n-1)//2)
                    else:
                        pair=suppress_middle_vertex(after_both)
                        assert sum(l for l,c in pair)==2*(n-k)
                        leaf=self.count(pair)
                    value+=q**(n*k)*w1*w2*leaf
        self.cache[key]=value;return value
    def metadata(self):
        return dict(states=len(self.cache),top_profiles=self.top_profiles,
                    socle_profiles=self.socle_profiles,enumerated_field_elements=0,
                    enumerated_subspaces=0)

def checks():
    start=time.perf_counter();rows=[]
    from nilpotent_strings_probe import string_types
    for q in (2,4,8,256):
        old=NilpotentPairCounter(q);new=EndpointPairCounter(q);total=0
        for parts in string_types(5):
            value=new.count(parts);expected=old.count(parts)
            assert value==expected,(q,parts,value,expected);total+=1
        rows.append(dict(q=q,n=5,types=total,endpoint=new.metadata(),
                         rank_compression=old.metadata()))
    data=json.loads(Path(__file__).with_name('nilpotent_strings_n4.json').read_text())
    new=EndpointPairCounter(2)
    for item in data['data']:assert new.count(item['strings'])==item['K']
    result=dict(checks=rows,independent_GL4_types=len(data['data']),seconds=time.perf_counter()-start)
    Path(__file__).with_name('endpoint_pair_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))

if __name__=='__main__':checks()
