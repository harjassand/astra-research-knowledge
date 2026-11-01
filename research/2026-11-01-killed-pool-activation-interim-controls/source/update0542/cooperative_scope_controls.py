"""Exact structural comparison for the distinguishing degree-five input.

This checks the literal common-offset obstruction of the existing accepted
raw certificate architecture. It does NOT reimplement its finder or infer
failure of recurrence from a rejected guard.
"""
import json,hashlib
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]


def rank(rows):
    a=[[Fraction(x) for x in row] for row in rows];head=0
    for col in range(len(a[0])):
        k=next((j for j in range(head,len(a)) if a[j][col]),None)
        if k is None:continue
        a[k],a[head]=a[head],a[k]
        pivot=a[head][col];a[head]=[v/pivot for v in a[head]]
        for j in range(len(a)):
            if j!=head and a[j][col]:
                z=a[j][col];a[j]=[x-z*y for x,y in zip(a[j],a[head])]
        head+=1
    return head


def model(m):
    q=m+1;zero=(0,0,0);ab=(1,0,1);end=(m,0,q)
    reactions=[{'id':'immigration','source':zero,'product':ab,'rate':1},
               {'id':'activation','source':ab,'product':end,'rate':1},
               {'id':'clearing','source':end,'product':zero,'rate':1}]
    for j,(ku,kd) in enumerate(zip((2,7,11),(1,3,5)),2):
        if j>=m:break
        s=(j,m-j,q);t=(j+1,m-j-1,q)
        reactions.extend(({'id':f'fast_{j}_up','source':s,'product':t,'rate':ku},
                          {'id':f'fast_{j}_down','source':t,'product':s,'rate':kd}))
    return reactions


def main():
    reactions=model(5);m=5;q=6;offset=(m-2,0,q)
    failures=[]
    for e in reactions[3:]:
        for side in ('source','product'):
            if any(v<w for v,w in zip(e[side],offset)):
                failures.append({'reaction':e['id'],'side':side,'complex':e[side]})
    assert failures
    complexes={tuple(e[s]) for e in reactions for s in ('source','product')}
    stoich_rank=rank([[b-a for a,b in zip(e['source'],e['product'])] for e in reactions])
    assert len(complexes)==6 and stoich_rank==3
    ratios=[Fraction(2,1),Fraction(7,3),Fraction(11,5)]
    assert len(set(ratios))>1
    # Explicit reachable tier-failure sequence, all steps genuinely enabled.
    for n in range(1,17):
        a,x,b=6*n,0,6*n
        for _ in range(n):
            assert a>=5 and b>=6
            a-=1;x+=1
        for _ in range(n):
            assert a>=5 and b>=6
            a-=5;b-=6
        assert (a,x,b)==(0,n,0)
    overlap=model(4);assert all(e[s][0]>=2 and e[s][2]>=5 for e in overlap[3:] for s in ('source','product'))
    result={'status':'PASS exact structural distinctions',
            'model_species_order':['A','X','B'],'distinguishing_raw_network':reactions,
            'm':5,'q':6,'composition_degree':5,'minimum_fast_A':2,
            'complex_count':len(complexes),'linkage_classes':1,'stoichiometric_rank':stoich_rank,
            'deficiency':len(complexes)-1-stoich_rank,
            'not_complex_balanced_witness':{'required_A_to_X_ratios':[str(r) for r in ratios],
                 'reason':'Leaf balance fixes the first ratio; consecutive middle balances force all three ratios equal. They are unequal.'},
            'old_raw_architecture_common_offset':offset,'failed_offset_guards':failures,
            'alternative_A_B_swap':'would require q_prime=5>m_prime=6, false',
            'accepted_pure_family_guard':'fails: pure 5X is absent',
            'accepted_one_A_family_guard':'fails: A+4X is absent',
            'ACK_Theorem6_1_guard':{'reachable_sequence':'(A,X,B)=(0,n,0)',
                 'path':'6n immigrations, n conversions 5A+6B->4A+X+6B, n clearings',
                 'D_top':'2A+3X+6B, vee-one monomial n^3',
                 'S_top':'0, the only enabled source',
                 'conclusion':'S_top is not contained in D_top; this sufficient theorem does not apply.'},
            'm4_overlap_control':'Fits the inspected existing raw baseline/true-F architecture after A=2+a, D=X; not new coverage. The full old finder was not executed here.',
            'scope':'Failure of named sufficient guards is not historical novelty clearance or a failure of recurrence.',
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT/'outputs/mechanism_selection_20261101/cooperative_scope_controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','deficiency','not_complex_balanced_witness','failed_offset_guards','m4_overlap_control')},indent=2))


if __name__=='__main__':main()
