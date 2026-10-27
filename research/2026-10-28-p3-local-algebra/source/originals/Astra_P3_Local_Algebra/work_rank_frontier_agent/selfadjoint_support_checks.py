#!/usr/bin/env python3
"""Replay old witnesses under the stronger selfadjoint operator.

Also exhaustively verifies all degree7..11 field presentations and a new
matrix witness whose error rank exceeds the entire small field dimension.
"""
from sylvester_support_checks import *


def run():
    previous=json.loads(Path(__file__).with_name('sylvester_support_results.json').read_text())
    out=[]
    for case in previous['cases']:
        base,defect,dec,cert=acquire_sylvester_base(case['raw_matrix'],case['field_modulus'],case['bandwidth'])
        assert base==case['planted_base'] and defect==case['planted_defect']
        out.append(dict(n=case['n'],d=case['d'],r=case['rank'],s=case['bandwidth'],
            scalar_dimension=cert['scalar_orbit_dimension'],operator=cert['operator'],seconds=cert['seconds']))
    raw=json.loads(Path(__file__).with_name('sylvester_raw_results.json').read_text())
    base,defect,dec,cert=acquire_sylvester_base(raw['quadratic_matrix'],raw['field_modulus'])
    assert base==raw['acquired_field_quadratic'] and defect==raw['acquired_defect']
    out.append(dict(n=108,d=12,r=8,s=1,scalar_dimension=7,operator=cert['operator'],
        raw_acquired_matrix_reused=True,seconds=cert['seconds']))
    fields=[]
    for d in range(7,12):
        for h in range((1<<d)|1,1<<(d+1),2):
            if not irreducible_binary(h): continue
            cert=scalar_certificate(h)
            assert cert['scalar_orbit_dimension']==7 and cert['generator_trials']==1
            # Exhaustively check the annihilator on all Frobenius eigenvalues.
            z=2
            for t in range(d):
                w=gf_pow(z,1<<t,h)
                value=xor_all(gf_mul(left,gf_pow(right,1<<t,h),h)
                              for left,right in zip(cert['coefficients'],cert['operator_right']))
                assert (value==0)==(t in {0,1,d-1})
            fields.append(dict(d=d,h=h,generator=z,scalar_dimension=7))
    h=0x89; d=7; b=15; n=d*b; r=8; rng=random.Random(7158108)
    planted=random_base(h,b,1,rng); U=[rng.getrandbits(n) for _ in range(r)]
    D=defect_from_support(U,h,b); raw=[x^y for x,y in zip(planted,D)]
    base,defect,dec,cert=acquire_sylvester_base(raw,h)
    assert base==planted and defect==D and cert['recovered_orbit_rank']==56
    try: acquire_quadratic_base(raw,h)
    except ValueError as error: old_rejection=str(error)
    else: raise AssertionError('rank-eight error over degree-seven field exceeded old route')
    newcase=dict(n=n,d=d,b=b,r=r,h=h,rank=len(span(D)),raw_matrix=raw,
        planted_base=planted,planted_defect=D,certificate=cert,old_decoder_rejection=old_rejection)
    return dict(status='all exact assertions passed',replayed_cases=out,
        irreducible_presentations_checked=len(fields),field_presentations=fields,new_case=newcase)


if __name__=='__main__':
    result=run(); Path(__file__).with_name('sylvester_selfadjoint_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],replayed_cases=len(result['replayed_cases']),
        field_presentations=result['irreducible_presentations_checked'],new_case={k:result['new_case'][k] for k in ['n','d','b','r']})))
