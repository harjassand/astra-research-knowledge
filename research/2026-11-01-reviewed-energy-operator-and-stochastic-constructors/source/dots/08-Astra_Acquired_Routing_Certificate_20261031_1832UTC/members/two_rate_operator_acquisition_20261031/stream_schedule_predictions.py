#!/usr/bin/env python3
"""Execute every prediction with bounded online state, not a large prefix cache."""
from pathlib import Path
import gzip
import hashlib
import json
import random
import time
from retained_large_acquisition import integer_step,integer_output

ROOT=Path(__file__).resolve().parent


def main():
    path=ROOT/'history_sensitive_4096_result.json';out=json.loads(path.read_text());c=out['compiled']
    L=out['length'];Q=out['screening']['supplied_schedules'];rng=random.Random(451)
    def words():
        yield tuple([0]*L);yield tuple([1]*L);yield tuple(i%2 for i in range(L))
        for _ in range(Q-3):yield tuple(rng.randrange(out['m']) for _ in range(L))
    target=ROOT/'history_sensitive_4096_predictions.tsv.gz';timer=time.perf_counter()
    word_hash=hashlib.sha256();best=None;worst=None;peak=0;count=0
    # Exclusive create: preserve any previous prediction artifact.
    with target.open('xb') as raw:
        with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as file:
            file.write(b'query_id\tobservable_application_word\tgrid_numerator\tgrid_denominator\n')
            for i,w in enumerate(words()):
                state=c['initial_grid_state'][:];word_hash.update(bytes(w))
                for a in w:state,bits=integer_step(c['operators'][a],state);peak=max(peak,bits)
                value=integer_output(c,state);grid=int(value*(1<<c['bits']))
                file.write((str(i)+'\t'+''.join(map(str,w))+'\t'+str(grid)+'\t'+str(1<<c['bits'])+'\n').encode())
                best=value if best is None else max(best,value);worst=value if worst is None else min(worst,value);count+=1
    assert count==Q and word_hash.hexdigest()==out['screening']['word_list_sha256']
    assert str(best)==out['screening']['best_score'] and str(worst)==out['screening']['worst_score']
    result={'status':'PASS','predictions':count,'word_symbols_read':count*L,
            'online_state_integer_entries':out['rank'],'maximum_live_word_symbols':L,
            'operator_integer_scalar_products':count*L*out['rank']**2,
            'output_integer_scalar_products':count*out['rank'],
            'peak_accumulator_bits':peak,'output_bytes':target.stat().st_size,
            'seconds':time.perf_counter()-timer,'output_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'model_result_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'scope':'All predictions actually emitted using integer replay. Input generator reproduces the explicit saved-list hash; reverse words for physical chronological Markov controls. No additional source calls.'}
    (ROOT/'history_sensitive_streaming_checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
