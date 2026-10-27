#!/usr/bin/env python3
"""Raw wide-field terminal and an independent factorized truth-table oracle."""
from contact_counter_checks import *
from field_kloosterman import gf_trace


def pair_field_oracle(h,pairs):
    q=1<<(h.bit_length()-1);table=[[gf_mul(x,y,h) for y in range(q)] for x in range(q)]
    trace=[gf_trace(x,h) for x in range(q)];fibers=[]
    for z in range(q):
        value=0
        for x in range(q):
            for y in range(q):
                phase=table[table[x][x]][x]^table[x][table[y][y]]^table[table[y][y]][y]^table[z][table[x][y]]
                value+=1-2*trace[phase]
        fibers.append(value)
    return sum(v**pairs for v in fibers),fibers


def run():
    h=19;b=9;R=ChainRing(h,1);n=b*R.m;rng=random.Random(1901)
    H=contact_polynomial(R,b,'one-ray');reference,fibers=pair_field_oracle(h,(b-1)//2)
    columns=random_invertible(n,rng);offset=rng.randrange(1<<n)
    def evaluate(x):
        y=linear_apply(columns,x)^offset
        return R.functional(ring_polynomial(R,H,[(y>>(R.m*i))&R.mask for i in range(b)]))
    raw=extract_anf(evaluate,n);source=Path(__file__).with_name('contact_field_36_input.json')
    source.write_text(json.dumps(dict(n=n,polynomial=sorted(raw)),separators=(',',':'))+'\n')
    result=compile_contact(raw,n);assert result['signed_count']==reference
    field=result['count_certificate']['field_terminal_certificate']
    assert field['field_values_enumerated']==16 and field['gaussian_fiber_variables']==32
    assert result['count_certificate']['candidate_count']==0
    fitted={tuple(row['exponents']):row['coefficient'] for row in result['homogeneous_cubic']}
    Q=set(result['quotient_quadratic']);center=sum(a<<(R.m*i) for i,a in enumerate(result['fit']['acquired_center']))
    for _ in range(1024):
        y=rng.randrange(1<<n);x=linear_apply(result['coordinate_columns'],y);z=y^center
        assert evaluate(x)==(R.functional(ring_polynomial(R,fitted,[(z>>(R.m*i))&R.mask for i in range(b)]))^polynomial_value(Q,z))
    result.update(reference=reference,independent_pair_fibers=fibers,
        independent_pair_assignments=16**3,raw_input_file=source.name,pointwise_checks=1024)
    singular={tuple(int(j in (i,i+1,b-1)) for j in range(b)):1 for i in range(0,b-1,2)}
    signed,certificate=weighted_contact_sum(h,1,singular,set(),b)
    expected=(1<<R.d)**(b-1)+((1<<R.d)-1)*(1<<R.d)**((b-1)//2)
    assert signed==expected and not certificate['geometry']['missing_hyperplane_excluded']
    try:compile_contact(raw,n,terminal_bit_budget=3)
    except ValueError as exc:assert 'field-coordinate enumeration' in str(exc)
    else:raise AssertionError('field scan ignored the explicit bit budget')
    output=dict(raw_field_case=result,degenerate_infinity_field_case=dict(
        module_rank=b,signed_count=signed,reference=expected,certificate=certificate),
        explicit_field_budget_rejection=True)
    Path(__file__).with_name('contact_field_results.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(dict(n=n,b=b,signed_count=result['signed_count'],zero_count=result['zero_count'],
        field_values=field['field_values_enumerated'],gaussian_variables=field['gaussian_fiber_variables'])),flush=True)


if __name__=='__main__':run()
