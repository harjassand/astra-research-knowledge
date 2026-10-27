#!/usr/bin/env python3
from chain_counter_checks import *

def run():
    cases=[]
    for h,e,rank,seed in [(0x1009,2,8,31801),(0x83,4,6,31802)]:
        print(json.dumps(dict(stage='make raw selfadjoint fixture',d=h.bit_length()-1,e=e,rank=rank)),flush=True)
        raw,n,evaluate,reference,metadata=fixture(h,e,seed,rank,'zero')
        source=Path(__file__).with_name('selfadjoint_'+str(n)+'_bit_input.json')
        source.write_text(json.dumps(dict(n=n,polynomial=sorted(raw)),indent=2)+'\n')
        result=compile_chain(raw,n,error_decoder='sylvester')
        assert result['signed_count']==reference and result['acquired_defect_rank']==rank
        assert result['support_certificate']['scalar_orbit_dimension']==7
        R=ChainRing(result['field_modulus'],result['chain_length']);mask=(1<<R.m)-1
        P={tuple(item['exponents']):item['coefficient'] for item in result['polynomial']}
        rng=random.Random(seed+33)
        for _ in range(1024):
            y=rng.randrange(1<<n);x=linear_apply(result['coordinate_columns'],y)
            value=R.functional(ring_polynomial(R,P,[(y>>(R.m*i))&mask for i in range(3)]))
            assert value^quadratic_value(result['acquired_defect'],y)==evaluate(x)
        result.update(metadata,reference=reference,pointwise_checks=1024,raw_input_file=source.name,
                      old_global_radius=(R.d-3)//2,old_ten_direction_orbit_impossible=10*rank>n)
        cases.append(result)
        Path(__file__).with_name('chain_selfadjoint_results.json').write_text(json.dumps(dict(
            status='all completed assertions passed',cases=cases,practical_speed_claim=False),indent=2)+'\n')
        print(json.dumps({k:result[k] for k in ['original_variables','field_degree','chain_length',
            'acquired_defect_rank','signed_count','zero_count','walsh_leaf_count','seconds']}),flush=True)
    return cases

if __name__=='__main__':run()
