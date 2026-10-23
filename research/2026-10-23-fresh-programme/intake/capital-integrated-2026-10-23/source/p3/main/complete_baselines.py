#!/usr/bin/env python3
"""Extra, declared accounting run for equally certified strong baselines."""
import hashlib
import json
import math
from pathlib import Path
import time
from decimal import Decimal,localcontext,ROUND_CEILING
import numpy as np
import research as base
import critical_confirmation as critical

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results'/'complete_baselines'


def target_count(logK):
    with localcontext() as c:
        c.prec=100
        x=(Decimal(logK).exp()-1)/Decimal('0.000125')
        raw=int(x.to_integral_value(rounding=ROUND_CEILING))
    return max(256,((raw+255)//256)*256)


def main():
    OUT.mkdir(parents=True,exist_ok=True); start=time.perf_counter()
    freeze=json.loads((ROOT/'COMPLETE_BASELINES.json').read_text())
    results={}
    old=json.loads((ROOT/'results'/'main_confirmation'/'results.json').read_text())
    sec=json.loads((ROOT/'results'/'secant_extension'/'main_confirmation'/'results.json').read_text())
    cfg=base.Config(**old['config'])
    q=np.load(ROOT/'results'/'main_confirmation'/'proposals.npz')['linear_tilt']
    logs={'derivative_certificate':old['logK_decimal']['linear_tilt'],
          'secant_certificate':sec['original_linear_tilt_new_certificate_logK']}
    counts={tag:target_count(l) for tag,l in logs.items()}
    n=max(counts.values()); assert n<=freeze['path_cap']
    print('main complete linear baseline: '+str(counts),flush=True)
    scores,receipt=base.sample_paths(cfg,q,n,freeze['seeds']['main_confirmation'])
    np.save(OUT/'main_linear_logweights.npy',scores)
    r={'config':old['config'],'receipt':receipt,'methods':{}}
    for tag,logK in logs.items():
        st=base.statistics(scores[:counts[tag]],cfg,logK,receipt['uniform_log_weight_error_allowance'])
        st['paths']=counts[tag]
        st['sampling_seconds_allocated_proportionally']=receipt['sampling_seconds']*counts[tag]/n
        st['cost_label']='Shared new stream; prefix time allocated proportionally, not separately measured'
        r['methods'][tag]=st
    results['main_confirmation']=r
    old=json.loads((ROOT/'results'/'critical_confirmation'/'critical_spatial_confirmation'/'results.json').read_text())
    cfg=critical.CriticalConfig(**old['config'])
    q=np.load(ROOT/'results'/'critical_confirmation'/'critical_spatial_confirmation'/'proposals.npz')['original_linear_tilt']
    logK=old['linear_tilt_secant_certificate_logK']; n=target_count(logK); assert n<=freeze['path_cap']
    print('critical complete linear baseline: '+str(n),flush=True)
    scores,receipt=critical.sample(cfg,q,n,freeze['seeds']['critical_spatial_confirmation'])
    np.save(OUT/'critical_linear_logweights.npy',scores)
    st=base.statistics(scores,cfg,logK,receipt['uniform_log_weight_error_allowance']); st.update(receipt)
    results['critical_spatial_confirmation']={'config':old['config'],'methods':{'secant_certificate':st}}
    results['receipt']={'elapsed_seconds':time.perf_counter()-start,
                        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                        'freeze_sha256':hashlib.sha256((ROOT/'COMPLETE_BASELINES.json').read_bytes()).hexdigest(),
                        'scope':'Additional complete-process accounting; original confirmation preserved'}
    (OUT/'results.json').write_text(json.dumps(results,indent=2))
    print(json.dumps(results['receipt']),flush=True)


if __name__=='__main__': main()
