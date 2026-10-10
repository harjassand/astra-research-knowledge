"""Exact integer verification of the cover reduction and restricted coupling.
No floating-point optimizer is used by this verifier. Python standard library only.
"""
from itertools import combinations
from random import Random
from pathlib import Path
import json,time

def span(basis):
    s={0}
    for x in basis:s|={x^y for y in tuple(s)}
    return frozenset(s)

def dimension(s):
    assert len(s)>0 and len(s)&(len(s)-1)==0
    return len(s).bit_length()-1

def all_subspaces(m):
    seen={frozenset({0})};todo=list(seen)
    while todo:
        s=todo.pop()
        for x in range(1,1<<m):
            if x not in s:
                t=s|frozenset(x^y for y in s)
                if t not in seen:seen.add(t);todo.append(t)
    return sorted(seen,key=lambda s:(len(s),tuple(sorted(s))))

def intersection(family,ambient):
    out=set(ambient)
    for s in family:out.intersection_update(s)
    return frozenset(out)

def irredundant_cover(family,ambient):
    inds=list(range(len(family)))
    assert set().union(*family)==set(ambient)
    for i in tuple(inds):
        remaining=[j for j in inds if j!=i]
        if set().union(*(family[j]for j in remaining))==set(ambient):inds.remove(i)
    W=intersection([family[i]for i in inds],ambient)
    assert dimension(ambient)-dimension(W)<=len(inds)-1, 'Brouwer inequality'
    return inds

def find_plane(kernels,ambient):
    """Construct a witness if dimension(ambient)>=2*len(kernels), joint kernel0.
    Returns None if below sufficient threshold; this is not a nonexistence test.
    """
    assert intersection(kernels,ambient)=={0}
    if not kernels:return None,[]
    if dimension(ambient)<2*len(kernels):return None,[]
    active=list(kernels);H=frozenset(ambient);trace=[]
    while active:
        n=dimension(H);w=len(active)
        assert n>=2*w
        outside=sorted(H-set().union(*active))
        if not outside:
            selected=irredundant_cover(active,H);case='original cover';bound=len(selected)-1
        else:
            x=outside[0]
            extended=[K|frozenset(x^z for z in K)for K in active]
            outside_extended=sorted(H-set().union(*extended))
            if outside_extended:
                y=outside_extended[0]
                assert x and y and x!=y
                U=span([x,y])
                assert all(len(U&K)in(1,4)for K in kernels)
                trace.append({'case':'witness','dimension':n,'blocks':w,'basis':[x,y]})
                return (x,y),trace
            selected=irredundant_cover(extended,H);case='extended cover';bound=2*len(selected)-1
        newH=intersection([active[i]for i in selected],H)
        drop=n-dimension(newH)
        assert drop<=bound
        trace.append({'case':case,'dimension':n,'blocks':w,'removed':len(selected),'dimension_drop':drop,'drop_bound':bound})
        active=[K&newH for i,K in enumerate(active)if i not in selected];H=newH
        assert intersection(active,H)=={0}
    assert not H or H=={0}
    raise AssertionError('Dimension potential should prohibit reaching empty active list')

def valid_pairs(kernels,m):
    zero_masks=[sum((1<<i)for i,K in enumerate(kernels)if x in K)for x in range(1<<m)]
    return [(x,y)for x in range(1<<m)for y in range(1<<m)if zero_masks[x]==zero_masks[y]==zero_masks[x^y]]

def random_kernel(rng,m,rank):
    forms=[]
    while len(forms)<rank:
        x=rng.randrange(1,1<<m)
        if x not in span(forms):forms.append(x)
    return frozenset(x for x in range(1<<m)if all((x&a).bit_count()%2==0 for a in forms))

def replay():
    rng=Random(20261010);cases=[];witnesses=0;triples=0;cover_steps=0
    for m in range(2,8):
        for w in range(1,5):
            for rep in range(6):
                ks=[random_kernel(rng,m,rng.randrange(1,m+1))for _ in range(w)]
                if intersection(ks,range(1<<m))!={0}:continue
                C=valid_pairs(ks,m)
                assert len(C)*4**(2*w)>=4**m
                assert (len(C)-1)%6==0
                if m>=2*w:
                    xy,trace=find_plane(ks,frozenset(range(1<<m)))
                    assert xy is not None;witnesses+=1
                    cover_steps+=sum(t['case']!='witness'for t in trace)
                # Exact marginal counts, restricted to moderate dimensions.
                if m<=5:
                    marg=[[0]*(1<<m)for _ in range(3)]
                    for x,y in C:
                        for a in range(1<<m):
                            for j,z in enumerate((a,a^x,a^y)):marg[j][z]+=1
                            triples+=1
                    assert all(all(t==len(C)for t in row)for row in marg)
                cases.append({'m':m,'w':w,'valid_pairs':len(C),'good_planes':(len(C)-1)//6})
    # Cases exercising each reduction branch, separately from threshold search.
    reductions=[]
    for m in range(2,6):
        ambient=frozenset(range(1<<m))
        # All coordinate kernels: no good plane, jointly injective.
        ks=[frozenset(x for x in ambient if not(x>>i&1))for i in range(m)]
        assert intersection(ks,ambient)=={0} and len(valid_pairs(ks,m))==1
        x=(1<<m)-1;js=[K|frozenset(x^z for z in K)for K in ks]
        inds=irredundant_cover(js,ambient)
        H=intersection([ks[i]for i in inds],ambient)
        assert m-dimension(H)<=2*len(inds)-1
        reductions.append({'m':m,'selected':len(inds),'drop':m-dimension(H)})
    return {'seed':20261010,'jointly_injective_cases':len(cases),'witnesses_constructed':witnesses,'witness_reduction_steps':cover_steps,'exact_coupling_triples_checked':triples,'count_bound':'|C| >= 4^(m-2w)','cases':cases,'reduction_examples':reductions,'scope':'Exact arithmetic checks; theorem is established by the proof using Brouwer 1986, not by tests.'}

if __name__=='__main__':
    t=time.time();ans=replay();ans['seconds']=time.time()-t
    Path(__file__).with_name('verification_results.json').write_text(json.dumps(ans,indent=2))
    print(json.dumps({k:v for k,v in ans.items()if k not in ('cases','reduction_examples')},indent=2))
