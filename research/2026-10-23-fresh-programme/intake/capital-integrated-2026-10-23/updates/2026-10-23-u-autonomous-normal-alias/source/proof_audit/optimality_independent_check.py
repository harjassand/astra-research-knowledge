"""Fresh exact tests of the proposed uniform-memory converse.

No candidate implementation is imported.  A physical-state breadth-first
search is independent of the gallery proof.  Its extension from full to
partial contacts at fixed word length follows from multi-affineness.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
from pathlib import Path
from random import Random
import hashlib
import json

ROOT = Path(__file__).resolve().parent
CANDIDATE = ROOT.parent/'sharp_statistics'/'THERMAL_RECALL_OPTIMALITY.txt'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def physical_search(n, depth):
    """Exact full contacts, quotienting only by within-block symmetries."""
    initial = (0, *([1]*n), *([0]*n))
    seen, frontier = {initial}, {initial}
    pairs = list(combinations(range(2*n), 2))
    expected = F(comb(2*n,n), 4**n)
    records = []
    best = F(1)
    for length in range(1, depth+1):
        fresh = set()
        for exponent, *values in frontier:
            for i,j in pairs:
                if values[i] == values[j]:
                    continue
                output = [2*x for x in values]
                output[i] = output[j] = values[i]+values[j]
                new_exponent = exponent+1
                while new_exponent and all(x % 2 == 0 for x in output):
                    output = [x//2 for x in output]
                    new_exponent -= 1
                key = (new_exponent, *sorted(output[:n]), *sorted(output[n:]))
                if key not in seen:
                    fresh.add(key)
        for exponent, *values in fresh:
            error = F(sum(values[:n]), n*2**exponent)
            best = min(best,error)
            require(error >= expected, 'physical contact word violates candidate')
        seen.update(fresh)
        frontier = fresh
        records.append(dict(depth=length, new_states=len(fresh),
                            total_states=len(seen), smallest_A_mass=str(best)))
    return dict(n=n, exhaustive_contact_depth=depth, quotient_states=len(seen),
                minimum_A_mass=str(best), conjectured_minimum=str(expected),
                covers_partial_contacts_by='multiaffine objective reaches its fixed-word maximum at q=0 or q=1/2',
                levels=records)


def permutation(word,d):
    order = list(range(d))
    for i in word:
        order[i],order[i+1] = order[i+1],order[i]
    return tuple(order)


def crossings(word,d):
    order=list(range(d))
    locations={}
    for position,i in enumerate(word):
        pair=tuple(sorted((order[i],order[i+1])))
        locations.setdefault(pair,[]).append(position)
        order[i],order[i+1] = order[i+1],order[i]
    return locations


def check_all_crossing_deletions():
    checked = words = 0
    for length in range(10):
        for word in product(range(2),repeat=length):
            target=permutation(word,3)
            for positions in crossings(word,3).values():
                for a,b in combinations(positions,2):
                    reduced=word[:a]+word[a+1:b]+word[b+1:]
                    require(permutation(reduced,3)==target,
                            'two same-original-strand crossings fail deletion')
                    checked+=1
            words+=1
    return dict(words=words, every_repeated_pair_deletion_checked=checked,
                dimension=3, maximum_word_length=9)


def majorizes(v,u):
    require(all(v[i]>=v[i+1] for i in range(len(v)-1)), 'ordered envelope')
    require(all(u[i]>=u[i+1] for i in range(len(u)-1)), 'ordered actual vector')
    require(sum(v)==sum(u), 'same total mass')
    return all(sum(v[:k])>=sum(u[:k]) for k in range(1,len(v)))


def average(values,i):
    out=list(values)
    out[i]=out[i+1]=(out[i]+out[i+1])/2
    return tuple(out)


def contact(values,i,j,q):
    out=list(values)
    x,y=out[i],out[j]
    out[i],out[j]=(1-q)*x+q*y,q*x+(1-q)*y
    return tuple(out)


def canonical(n):
    order=list(range(2*n))
    word=[]
    for j in range(n):
        while order.index(n+j)>j:
            index=order.index(n+j)-1
            word.append(index)
            order[index],order[index+1]=order[index+1],order[index]
    return tuple(word)


def rank_envelope(n,word):
    v=(F(1,n),)*n+(F(0),)*n
    for i in word:
        v=average(v,i)
    return v


def check_rectangles():
    counts={}
    for n in (1,2,3):
        target=tuple(range(n,2*n))+tuple(range(n))
        expected=rank_envelope(n,canonical(n))
        count=0
        stack=[(tuple(range(2*n)),())]
        while stack:
            order,word=stack.pop()
            if order==target:
                require(len(word)==n*n,'rectangle crossing count')
                require(rank_envelope(n,word)==expected,'reduced envelope differs')
                count+=1
                continue
            for k in range(2*n-1):
                if order[k]<n<=order[k+1]:
                    new=list(order)
                    new[k],new[k+1]=new[k+1],new[k]
                    stack.append((tuple(new),word+(k,)))
        require(sum(expected[:n])==1-F(comb(2*n,n),4**n),'central binomial formula')
        counts[str(n)]=count
    return counts


def check_physical_sweeps():
    records=[]
    for n in range(1,33):
        p=(F(1,n),)*n+(F(0),)*n
        for j in range(n):
            for i in reversed(range(n)):
                p=contact(p,i,n+j,F(1,2))
        expected=F(comb(2*n,n),4**n)
        require(sum(p[:n])==expected,'physical sweep central-binomial formula')
        require(tuple(sorted(p,reverse=True))==rank_envelope(n,canonical(n)),
                'physical sweep differs from rank envelope')
        if n<=6 or n in (12,24,32):
            records.append(dict(n=n,A_mass=str(expected),B_mass=str(1-expected)))
    return dict(all_n_from_1_through=32,selected_values=records)


def tie_gallery(n,raw_steps):
    # Add strictly finite q=1/4 contacts, not ideal full thermalizations.
    steps=list(raw_steps)
    p=(F(1,n),)*n+(F(0),)*n
    for i,j,q in steps:
        p=contact(p,i,j,q)
    mass_b=sum(p[n:])
    require(mass_b>F(1,2),'raw input to gallery needs B majority')
    added=0
    while min(p[n:])<=max(p[:n]):
        for block in (list(range(n)),list(range(n,2*n))):
            i=max(block,key=lambda a:p[a])
            j=min(block,key=lambda a:p[a])
            if p[i]!=p[j]:
                step=(i,j,F(1,4))
                steps.append(step)
                p=contact(p,*step)
                added+=1
        require(added<10000,'separation iteration safeguard')
    final=p
    initial_order=(sorted(range(n),key=lambda i:(-final[i],i))+
                   sorted(range(n,2*n),key=lambda i:(-final[i],i)))
    tie_key={a:i for i,a in enumerate(initial_order)}
    order=list(initial_order)
    p=(F(1,n),)*n+(F(0),)*n
    envelope=tuple(p[i] for i in order)
    word=[]
    wall_checks=0
    simultaneous_roots=0

    for i,j,q in steps:
        slopes=[F(0)]*(2*n)
        slopes[i],slopes[j]=p[j]-p[i],p[i]-p[j]
        roots={F(0),q}
        root_multiplicities={}
        for a,b in combinations(range(2*n),2):
            if slopes[a]!=slopes[b]:
                root=(p[b]-p[a])/(slopes[a]-slopes[b])
                if 0<=root<=q:
                    roots.add(root)
                    root_multiplicities[root]=root_multiplicities.get(root,0)+1
        simultaneous_roots+=sum(x>1 for x in root_multiplicities.values())
        for t in sorted(roots):
            actual=tuple(x+t*s for x,s in zip(p,slopes))
            require(majorizes(envelope,tuple(actual[a] for a in order)),
                    'majorization lost between walls')
            # Exact one-sided rank order: no epsilon, perturbation, or genericity.
            after=sorted(range(2*n),key=lambda a:(-actual[a],
                         -slopes[a] if t<q else F(0),tie_key[a]))
            for rank,label in enumerate(after):
                location=order.index(label)
                while location>rank:
                    k=location-1
                    require(actual[order[k]]==actual[order[k+1]],'swap away from actual tie')
                    envelope=average(envelope,k)
                    order[k],order[k+1]=order[k+1],order[k]
                    require(majorizes(envelope,tuple(actual[a] for a in order)),
                            'wall lemma fails')
                    word.append(k)
                    wall_checks+=1
                    location-=1
        p=contact(p,i,j,q)
    require(p==final,'gallery changed physical endpoint')
    target=tuple(range(n,2*n))+tuple(range(n))
    require(permutation(word,2*n)==target,'retrospective label ordering fails')
    reduced=tuple(word)
    while True:
        repeats=[positions for positions in crossings(reduced,2*n).values() if len(positions)>1]
        if not repeats:
            break
        # Delete first and LAST occurrences, deliberately not candidate's first-repeat rule.
        a,b=repeats[-1][0],repeats[-1][-1]
        reduced=reduced[:a]+reduced[a+1:b]+reduced[b+1:]
        require(permutation(reduced,2*n)==target,'iterated deletion endpoint fails')
    require(len(reduced)==n*n,'remaining gallery is not reduced block exchange')
    best=rank_envelope(n,canonical(n))
    require(rank_envelope(n,reduced)==best,'rectangle commuting envelope fails')
    require(majorizes(best,envelope),'deleting operators failed majorization')
    require(sum(final[n:])==mass_b,'separation changed raw block mass')
    require(mass_b<=sum(best[:n]),'raw output beats candidate')
    return dict(n=n, raw_contacts=len(raw_steps), finite_separation_contacts=added,
                tie_swaps=wall_checks, simultaneous_root_times=simultaneous_roots,
                raw_B_mass=str(mass_b), deleted_letters=len(word)-len(reduced))


if __name__=='__main__':
    physical=[physical_search(2,14),physical_search(3,8)]
    rng=Random(754321)
    gallery_cases=[]
    for n in (2,3,4):
        accepted=0
        while accepted<8:
            # A nonoptimal strict or full-contact sweep, then arbitrary perturbations.
            steps=[(i,n+j,rng.choice((F(2,5),F(1,2))))
                   for j in range(n) for i in reversed(range(n))]
            for _ in range(rng.randrange(8)):
                i,j=rng.sample(range(2*n),2)
                steps.append((i,j,rng.choice((F(0),F(1,5),F(2,5),F(1,2)))))
            p=(F(1,n),)*n+(F(0),)*n
            for step in steps:
                p=contact(p,*step)
            if sum(p[n:])<=F(51,100):
                continue
            gallery_cases.append(tie_gallery(n,steps))
            accepted+=1
    out=dict(candidate_sha256=hashlib.sha256(CANDIDATE.read_bytes()).hexdigest(),
             arithmetic='Exact Python Fractions and dyadic integers; no candidate code imported',
             physical_exhaustive_searches=physical,
             deletion_checks=check_all_crossing_deletions(),
             reduced_rectangle_word_counts=check_rectangles(),
             physical_sweep_formula_checks=check_physical_sweeps(),
             rational_tie_gallery_cases=gallery_cases,
             negative_control_q_above_half=dict(n=1,q='3/4',B_mass='3/4',candidate_bound='1/2'),
             scope='Finite falsification checks; the independent written proof supplies the unbounded-word conclusion.')
    (ROOT/'optimality_independent_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(candidate_sha256=out['candidate_sha256'],
                         physical_searches=[{k:v for k,v in x.items() if k!='levels'} for x in physical],
                         deletion_checks=out['deletion_checks'],
                         reduced_word_counts=out['reduced_rectangle_word_counts'],
                         gallery_cases=len(gallery_cases),
                         wall_checks=sum(x['tie_swaps'] for x in gallery_cases)),indent=2))
