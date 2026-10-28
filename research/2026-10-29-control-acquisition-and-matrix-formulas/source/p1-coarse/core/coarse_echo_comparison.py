"""Same-observation comparison with the retained scalar residual compiler."""
from fractions import Fraction as F
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'branches'/'physical'))
from multiboundary_positive_events import binomial_interval
from echo_compiler import EchoCompiler, Interval, propose_maps
from uniform_certificate import uniform_certificate
from run_echo_experiment import dumpable

def run():
    raw=json.loads((ROOT/'results'/'COARSE_SWITCHING_RAW_RECEIPTS.json').read_text())
    observations=raw['balanced_tapes']['counts_by_prefix']
    candidates=[]
    for dictionary in ([(),(0,)],[(),(1,)],[(),(0,),(1,)]):
        records={():Interval(F(1),F(1))}
        for w in EchoCompiler.required_words(dictionary,2):
            if not w:continue
            r=observations[''.join(map(str,w))]
            records[w]=Interval(*binomial_interval(r['survived'],r['assigned_trials'],F(18)))
        maps=propose_maps(dictionary,2,records)
        compiler=EchoCompiler(dictionary,2,records,maps)
        valid=None
        for k in range(1,100):
            try:
                valid=uniform_certificate(compiler,rho=F(k,100))
            except ValueError:
                continue
            break
        candidates.append(dict(dictionary=dictionary,source_words=len(records),
                               certificate=valid))
    useful=[r for r in candidates if r['certificate'] is not None]
    best=min(useful,key=lambda r:r['certificate']['all_word_total_bound'])
    result=dict(candidates=candidates,best=best,new_source_queries=0,
                scope='Retained signed scalar-echo method with box confidence intervals and three small word dictionaries; all candidate contractions and bounds checked exactly. This is not an optimization over every known residual or semidefinite method. Same acquired categorical observations and confidence event as the prefix cover.',
                prior_data_cost_included=True)
    (ROOT/'results'/'COARSE_ECHO_COMPARISON.json').write_text(json.dumps(dumpable(result),indent=2)+'\n')
    print('best dictionary',best['dictionary'],'rho',best['certificate']['rho'],
          'bound',float(best['certificate']['all_word_total_bound']))
    for item in candidates:
        print(item['dictionary'],None if item['certificate'] is None else
              float(item['certificate']['all_word_total_bound']))

if __name__=='__main__':run()
