#!/usr/bin/env python3
"""Independent exact puncture/unique-decode checks; no K enumeration."""
import itertools
import json
from pathlib import Path
from mixed_adversarial_checks import (
    alt, alt_check, bits, column_basis, edge_weight, left_inverse,
    mixed_sum, multiply, rank, submatrix, transpose, witness,
)


def codewords(columns):
    value=0
    yield value
    for j in range(1,1<<len(columns)):
        value ^= columns[(j&-j).bit_length()-1]
        yield value


def puncture_decode(b,initial_removed,pivots,delta,budget):
    n=len(b);removed=set(initial_removed);history=[]
    first_rank=None
    while True:
        remain=[i for i in range(n) if i not in removed]
        raw_u=submatrix(b,remain,pivots)
        chosen_local=column_basis(raw_u,len(pivots))
        chosen=[pivots[i] for i in chosen_local]
        u=submatrix(b,remain,chosen)
        d=len(chosen)
        if first_rank is None: first_rank=d
        if history: assert d<history[-1]['rank_before']
        columns=transpose(u,d)
        short=next((word for word in codewords(columns)
                    if word and word.bit_count()<=2*delta),None)
        if short is None: break
        support=[remain[i] for i in bits(short)]
        removed.update(support)
        history.append(dict(rank_before=d,deleted_vertices=support))
    assert len(history)<=first_rank
    assert len(removed-set(initial_removed))<=2*delta*first_rank
    assert all(not word or word.bit_count()>2*delta for word in codewords(columns))
    actual=submatrix(b,remain,remain)
    decoded=[]
    for i,column in enumerate(transpose(actual,len(remain))):
        matches=[word for word in codewords(columns) if (word^column).bit_count()<=delta]
        assert len(matches)<=1
        if not matches:
            return dict(accepted=False,reason='no nearby codeword',failed_column=remain[i],
                        removed=sorted(removed),punctures=history)
        decoded.append(matches[0])
    a_hat=transpose(decoded,len(remain))
    if a_hat!=transpose(a_hat,len(remain)):
        return dict(accepted=False,reason='decoded matrix is nonsymmetric',
                    removed=sorted(removed),punctures=history)
    if any(row>>i&1 for i,row in enumerate(a_hat)):
        return dict(accepted=False,reason='decoded matrix is not alternating',
                    removed=sorted(removed),punctures=history)
    sparse=[x^y for x,y in zip(actual,a_hat)]
    if edge_weight(sparse)>budget:
        return dict(accepted=False,reason='sparse residual exceeds budget',
                    removed=sorted(removed),punctures=history)
    ell=left_inverse(u,d)
    k=multiply(multiply(ell,a_hat),transpose(ell,len(remain)))
    assert alt_check(k)
    assert multiply(multiply(u,k),transpose(u,d))==a_hat
    return dict(accepted=True,b=b,remain=remain,removed=sorted(removed),
                u=u,clean_basis_rank=d,accepted_k=k,accepted_residual=sparse,
                decoded_a=a_hat,punctures=history,initial_code_rank=first_rank,
                decoded_rank=rank(a_hat),residual_edges=edge_weight(sparse))


def main():
    source=json.loads(Path(__file__).with_name('mixed_adversarial_results.json').read_text())
    records=[];total_leaves=0
    for original in source['records']:
        a=original['a_rows'];s=original['s_rows'];delta=original['delta']
        w=witness(a,s,delta)
        decoded=puncture_decode(w['b'],w['removed'],w['initial_pivots'],delta,w['budget'])
        assert decoded['accepted'],(original['name'],decoded)
        assert decoded['decoded_a']==submatrix(a,decoded['remain'],decoded['remain'])
        assert len(decoded['removed'])<=2*w['budget']//(delta+1)+3*w['rank_a']*delta
        value,leaves=mixed_sum(set(original['local_polynomial']),decoded)
        assert value==original['exact_mixed_phase_sum']
        total_leaves+=leaves
        records.append(dict(name=original['name'],accepted=True,
                            initial_removed=w['removed'],final_removed=decoded['removed'],
                            initial_code_rank=decoded['initial_code_rank'],
                            final_code_rank=decoded['clean_basis_rank'],decoded_rank=decoded['decoded_rank'],
                            punctures=decoded['punctures'],residual_edges=decoded['residual_edges'],
                            exact_mixed_phase_sum=value,exact_leaf_sums=leaves))
    failures=[
        ('empty code with a column too far away',alt(5,[(i,(i+1)%5) for i in range(5)]),[],[],1,5,
         'no nearby codeword'),
        ('star decodes columnwise to a nonsymmetric matrix',alt(5,[(0,i) for i in range(1,5)]),[],[0],1,4,
         'decoded matrix is nonsymmetric'),
        ('complete graph decodes to a nonalternating all-ones matrix',
         alt(6,list(itertools.combinations(range(6),2))),[0],[0],1,15,
         'decoded matrix is not alternating'),
        ('unique codeword exists but residual budget is too small',alt(4,[(0,1),(2,3)]),[],[],1,1,
         'sparse residual exceeds budget'),
    ]
    failure_records=[]
    for name,b,e,i,delta,m,reason in failures:
        result=puncture_decode(b,e,i,delta,m)
        assert not result['accepted'] and result['reason']==reason,(name,result)
        failure_records.append(dict(name=name,**result))
    empty=puncture_decode(alt(4,[(0,1),(2,3)]),[],[],1,2)
    assert empty['accepted'] and empty['clean_basis_rank']==empty['decoded_rank']==0
    assert any(r['punctures'] for r in records)
    assert any(r['final_code_rank']>r['decoded_rank'] for r in records)
    out=dict(status='all assertions passed',true_witness_cases=len(records),
             exact_mixed_leaf_sums=total_leaves,rejection_cases=len(failure_records),
             empty_code_acceptance=True,records=records,rejections=failure_records,
             space_note='Codewords are streamed by Gray code in the mathematical algorithm; the finite checker retains only the at-most-one decoding match.',
             limitation='Exhaustive finite phase sums; no asymptotic engine or general decomposition-search benchmark.')
    Path(__file__).with_name('puncture_decode_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('records','rejections')},indent=2))
    for r in records:
        if r['punctures'] or r['final_code_rank']>r['decoded_rank']:
            print(json.dumps(r,sort_keys=True))


if __name__=='__main__': main()
