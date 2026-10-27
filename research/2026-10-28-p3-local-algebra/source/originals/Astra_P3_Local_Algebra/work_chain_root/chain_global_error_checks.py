#!/usr/bin/env python3
"""Complete acquired local-ring counting beyond the old field-block radius."""
from chain_counter_checks import *
from field_rank_decoder import acquire_quadratic_base

def run():
    cases=[]
    for h,e,rank,seed in [(0x1009,3,6,205701),(0x1009,4,10,205702)]:
        print(json.dumps(dict(stage='make raw input',d=h.bit_length()-1,e=e,rank=rank)),flush=True)
        raw,n,evaluate,reference,metadata=fixture(h,e,seed,rank,'zero')
        source=Path(__file__).with_name('global_example_'+str(n)+'_bit_input.json')
        source.write_text(json.dumps(dict(n=n,polynomial=sorted(raw)),indent=2)+'\n')
        print(json.dumps(dict(stage='raw compiler',n=n,terms=len(raw))),flush=True)
        result=compile_chain(raw,n,error_decoder='sylvester')
        assert result['signed_count']==reference and result['acquired_defect_rank']==rank
        R=ChainRing(result['field_modulus'],result['chain_length']);mask=(1<<R.m)-1
        P={tuple(item['exponents']):item['coefficient'] for item in result['polynomial']}
        rng=random.Random(seed+20);checks=0
        for _ in range(2048):
            y=rng.randrange(1<<n);x=linear_apply(result['coordinate_columns'],y)
            value=R.functional(ring_polynomial(R,P,[(y>>(R.m*i))&mask for i in range(3)]))
            value^=quadratic_value(result['acquired_defect'],y)
            assert value==evaluate(x);checks+=1
        result.update(metadata,reference=reference,pointwise_checks=checks,
                      raw_input_file=source.name,old_global_radius=(R.d-3)//2)
        cases.append(result)
        Path(__file__).with_name('chain_global_error_results.json').write_text(json.dumps(dict(
            status='all completed exact assertions passed',cases=cases,practical_speed_claim=False),indent=2)+'\n')
        print(json.dumps({k:result[k] for k in ['original_variables','field_degree','chain_length',
            'acquired_defect_rank','signed_count','zero_count','walsh_leaf_count','seconds']}),flush=True)
    return cases

if __name__=='__main__':run()
