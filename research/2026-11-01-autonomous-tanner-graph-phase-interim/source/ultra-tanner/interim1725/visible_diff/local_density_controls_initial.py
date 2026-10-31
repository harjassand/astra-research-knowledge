"""Exact controls of the localized descent-density proof.

Small instances test local implications, not the large-degree existence
theorem. Parameter checks certify only the added analytic inequalities;
they do not acquire a large robust base code or physical device.
"""
from __future__ import annotations
import hashlib
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"outputs/tanner_global_phase_20261101"


def subsets(mask):
    z=mask
    while True:
        yield z
        if z==0:break
        z=(z-1)&mask


def positions(mask):return [i for i in range(mask.bit_length()) if mask>>i&1]


def embed(local,inds):return sum(((local>>j)&1)<<q for j,q in enumerate(inds))


def local_checks(patches,codes,N,centers):
    # All local words and arbitrary deterministic nearest-word tie rules.
    counters=dict(configurations=0,stalled_centers=0,neutral_R_flips=0,
                  low_overlap_words=0,globally_nonstalled_local_cases=0)
    embedded=[[embed(c,positions(p)) for c in code] for p,code in zip(patches,codes)]
    for reverse in [False,True]:
        nearest=[];pot=[]
        for e in range(1<<N):
            cs=[];rs=[]
            for patch,code in zip(patches,embedded):
                ev=e&patch
                best=min((ev^c).bit_count() for c in code)
                tied=[c for c in code if (ev^c).bit_count()==best]
                c=max(tied) if reverse else min(tied)
                cs.append(c);rs.append(ev^c)
            nearest.append((cs,rs));pot.append(sum(r.bit_count() for r in rs))
        for e in range(1<<N):
            cs,rs=nearest[e]
            active={j for j,patch in enumerate(centers)
                    if any(pot[e^f]<pot[e] for f in subsets(patch))}
            union=0;dup=0
            for r in rs:dup|=union&r;union|=r
            Y={v for v,c in enumerate(cs) if c}
            # Each data variable belongs to exactly two factor patches.
            assert pot[e]<=max(p.bit_count() for p in patches)*(len(Y)+len(active))
            for q in positions(dup):
                assert all(j in active for j,p in enumerate(centers) if p>>q&1)
            counters['configurations']+=1
            for j,patch in enumerate(centers):
                if j in active:continue
                counters['stalled_centers']+=1
                if active:counters['globally_nonstalled_local_cases']+=1
                assert not (dup&patch)
                for f in subsets(union&patch):
                    assert pot[e^f]==pot[e]
                    changed=[r^(f&p) for r,p in zip(rs,patches)]
                    assert all(z.bit_count()==min(((e^f)&p^c).bit_count() for c in code)
                               for z,p,code in zip(changed,patches,embedded))
                    assert all(((e^f)&p)^z==c for z,p,c in zip(changed,patches,cs))
                    assert __import__('functools').reduce(int.__or__,changed,0)==union
                    counters['neutral_R_flips']+=1
                if j<len(patches) and centers[j]==patches[j]:
                    for c in embedded[j]:
                        assert 2*((union&patch)&c).bit_count()<=c.bit_count()
                        counters['low_overlap_words']+=1
    return counters


def small_tanner():
    p=5;A=[1,4];B=[2,3]
    squares=set()
    for g,a,b in itertools.product(range(p),A,B):
        sq=tuple(sorted([(0,g),(1,(g+a)%p),(1,(g+b)%p),(0,(g+a+b)%p)]))
        assert len(set(sq))==4
        squares.add(sq)
    faces=sorted(squares);N=len(faces)
    assert N==10
    patches={v:sum(1<<q for q,f in enumerate(faces) if v in f)
             for v in itertools.product(range(2),range(p))}
    assert all(m.bit_count()==4 for m in patches.values())
    local=[patches[1,g] for g in range(p)]
    centers=local+[patches[0,g] for g in range(p)]
    code=[c for c in range(16) if c.bit_count()%2==0]
    # CA=CB=<11>, so C1^perp is exactly the even-parity local code.
    for x in patches.values():
        for z in patches.values():
            pass
    assert all((patches[0,a]&patches[1,b]).bit_count()%2==0
               for a,b in itertools.product(range(p),repeat=2))
    return dict(n=N,Delta=2,group="Z/5, A=+-1, B=+-2",
                local_checks=local_checks(local,[code]*p,N,centers),
                scope="Exact local-lemma control; this small cyclic complex does not satisfy the asymptotic expansion/robustness hypotheses")


def generic_factor_checks():
    edges=list(itertools.combinations(range(4),2));N=len(edges)
    patches=[sum(1<<q for q,e in enumerate(edges) if v in e) for v in range(4)]
    triangles=[sum(1<<q for q,e in enumerate(edges) if set(e)<=set(vs))
               for vs in itertools.combinations(range(4),3)]
    choices=[[0,7],[c for c in range(8) if c.bit_count()%2==0],[0,1,6,7],[0]]
    out=[]
    for labels in [(0,0,0,0),(1,1,1,1),(0,1,2,3),(2,0,2,1)]:
        out.append(dict(codes=list(labels),checks=local_checks(
            patches,[choices[i] for i in labels],N,patches+triangles)))
    return out


def parameter_certificate():
    delta=Q(1,100);eps=Q(1,100);epsprime=Q(1,50)
    x=2**20 # Delta^(1/100) >= x is sufficient for these added bounds.
    a=delta**2/8192;bad=1280/a
    conditions={
        'density_exception_fraction':x**102>=258,
        'candidate_not_active':x**2>=32/a,
        'bad_neighbor_cost':x**2>=3*delta*bad,
        'dense_edge_distance':x**49>=4/delta**2,
        'bipartite_mean_absorption':x**49>=2/delta,
        'local_reduced_error_contradiction':x**49>100/(a*delta**2),
        'robustness_margin':x>=10/delta,
        'robustness_below_product_distance':x**48>=2/delta**2,
        'robust_exponents':0<eps<epsprime<Q(1,28),
        'base_distance_entropy_margin':100**400<2**100*99**396,
    }
    assert all(conditions.values())
    return dict(delta=str(delta),analysis_epsilon=str(eps),robust_epsilon=str(epsprime),
                additional_sufficient_Delta_lower="2^2000",
                conditions=conditions,
                drift_density="active centers >= U/(2 Delta^(3+2 epsilon))",
                scope="Exact rational sufficient-inequality check; base-code existence still uses the primary sufficiently-large-Delta theorem, no explicit code at Delta=2^2000 is asserted")


def main():
    data=dict(generic_local_factor_checks=generic_factor_checks(),
              small_quantum_tanner=small_tanner(),
              added_parameter_certificate=parameter_certificate())
    data['program_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'local_density_controls.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(dict(output=str(OUT/'local_density_controls.json'),checks=list(data))))


if __name__=='__main__':main()
