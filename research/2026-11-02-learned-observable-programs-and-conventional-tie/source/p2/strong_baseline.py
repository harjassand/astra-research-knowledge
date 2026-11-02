"""The honest equal-information comparator: retain the entire empirical local rate table,
then use ordinary Walsh expansion directly. No learning of a special dual program is
needed beyond established symbolic Boolean algebra.
"""
import json,math
from fractions import Fraction
from pathlib import Path
from synthesize import PATTERNS,walsh_fit,local_residual,LocalRecords
from execute import model_error_envelope

def parse_spin(s):return tuple(1 if x=='+' else -1 for x in s)

def recover_records(frozen_measurements):
    r={}
    for mode,obj in frozen_measurements.items():
        counts={parse_spin(p):int(k) for p,k in obj['counts'].items()}
        E=int(obj['exposure_per_configuration'])
        # Preserve exact original CI: stored JSON has floats. Rebuild conservative
        # original integer root from measured counts without accessing source_device.
        from math import isqrt
        x=22;scale=10**12
        intervals={}
        for p,k in counts.items():
            root=Fraction(isqrt(2*k*x*scale*scale)+1,scale)
            intervals[p]=(max(Fraction(0),(k-x-root)/E),(k+2*x+root)/E)
        r[mode]=LocalRecords(mode,E,counts,intervals,{p:Fraction(k,E) for p,k in counts.items()})
    return r

def compute_baseline(records):
    programs={}
    for mode,record in records.items():
        th=walsh_fit(record.estimates)
        a=th[0]
        # Include ALL coefficients, positive and negative. Signed walks are okay
        # if death=2alpha-sum(abs(jump coefficients)) >=0.
        rules={b:-2*c for b,c in th.items() if b}
        kill=2*a-sum(abs(q) for q in rules.values())
        local_res=local_residual(record,a,rules)
        programs[mode]={'mode':mode,'alpha':float(a),'jumps':[{'toggle_mask':b,'offsets':[j-1 for j in range(3) if b>>j&1],
                                                             'rate':float(abs(q)),'sign':1 if q>=0 else -1} for b,q in sorted(rules.items())],
                        'kill':float(kill),'local_residual_bound':float(local_res),
                        'program_size_rules':len(rules),'full_rate_table_retained':True}
    return programs

if __name__=='__main__':
    root=Path(__file__).parent
    records=recover_records(json.loads((root/'frozen_measurements.json').read_text()))
    baseline=compute_baseline(records)
    for mode,p in baseline.items():print(mode,'rules=',p['program_size_rules'],'kill=',p['kill'],'rho=',p['local_residual_bound'])
    (root/'strong_baseline_results.json').write_text(json.dumps(baseline,indent=2))
