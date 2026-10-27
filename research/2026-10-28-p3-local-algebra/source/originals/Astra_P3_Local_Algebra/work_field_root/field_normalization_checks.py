#!/usr/bin/env python3
"""Preserve the concrete wrong-count failure from dropping field-square terms."""
from pathlib import Path
import json
from field_descent import count_balanced


def run():
    source=json.loads(Path(__file__).with_name('field_descent_results.json').read_text())['cases']
    cases=[]
    for case in source:
        poly={tuple(t['exponents']):t['coefficient'] for t in case['balanced_polynomial']}
        wrong={e:c for e,c in poly.items() if not(sum(e)==2 and 2 in e)}
        exact,_=count_balanced(poly,case['field_modulus'])
        bad,_=count_balanced(wrong,case['field_modulus'])
        assert exact==case['signed_count'] and exact!=bad
        cases.append(dict(original_variables=case['original_variables'],modulus=case['field_modulus'],
            balanced_polynomial=case['balanced_polynomial'],exact_signed_count=exact,
            incorrect_count_if_field_squares_are_dropped=bad))
    return dict(status='all regression assertions passed',cases=cases,
        repair='Tr(c X^2)=Tr(c^(2^(d-1)) X); fold into the unary coefficient before counting')


if __name__=='__main__':
    data=run();Path(__file__).with_name('field_normalization_results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(dict(status=data['status'],cases=len(data['cases']))))
