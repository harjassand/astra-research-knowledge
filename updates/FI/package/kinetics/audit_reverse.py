from fractions import Fraction as F
from pathlib import Path
import json,time
from model import fixture,add_context_clock
from kinetic_tomography import physical_clock
from reverse_tomography import recover_reverse
from audit import replay
ROOT=Path(__file__).parent

def main():
    t=time.perf_counter();checks=0
    for label,truth in [('A',fixture(B=3,m=6,rarity=3)),('B',add_context_clock(fixture(B=3,m=6,rarity=3),F(1,100)))]:
        tr=json.load(open(ROOT/f'reverse_{label}_transcript.json'));m,cc,derived=recover_reverse(18,tr)
        for key,z in tr['reverse_rates'].items():
            i,x=map(int,key.split(':'));aa=physical_clock(truth,i,x)
            assert aa/2<=F(z)<=aa;checks+=1
            assert 2*F(derived[key])==aa;checks+=1
        assert m['edges']==truth['edges'] and m['fields']==truth['fields'];checks+=1
    a=json.load(open(ROOT/'reverse_A_transcript.json'));b=json.load(open(ROOT/'reverse_B_transcript.json'))
    assert a['weights']==b['weights'];checks+=1
    for i in range(18):assert a['reverse_rates'][f'{i}:0']==b['reverse_rates'][f'{i}:0'];checks+=1
    reps=[replay('reverse_A'),replay('reverse_B'),replay('reverse_matched_tensor')];checks+=sum(r['exact_endpoint_matches'] for r in reps)
    out=dict(exact_assertions=checks,replays=reps,seconds=time.perf_counter()-t,scope='exact synthetic query consistency and private-data-free final response replay; no experimental validation')
    json.dump(out,open(ROOT/'reverse_audit_results.json','w'),indent=2)
    old=json.load(open(ROOT/'combined_audit.json'));old['reverse_extension']=out;old['all_exact_assertions_total']=old['exact_assertions_total']+checks
    json.dump(old,open(ROOT/'combined_audit.json','w'),indent=2)
    print(checks,'total',old['all_exact_assertions_total'],'seconds',out['seconds'],flush=True)
if __name__=='__main__':main()
