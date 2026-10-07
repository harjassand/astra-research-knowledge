"""Finite exact energy and reversibility check, not a general mixing claim."""
from fractions import Fraction as Q
from pathlib import Path
import json
import time
from pair_heatbath_kernel import transition_distribution,point_weight
from single_pair_checks import line_system,weights


def main():
    started = time.perf_counter()
    sigma=Q(1,10**8*5**4)
    rows=[]
    for length in [2,10,30]:
        t=Q(2**length)
        lines=line_system(t,sigma)
        stateweights={s:w for s,w in weights(t,sigma).items() if w}
        z=sum(stateweights.values(),Q(0))
        pi={s:w/z for s,w in stateweights.items()}
        P={s:transition_distribution(lines,s) for s in stateweights}
        for s in stateweights:
            assert point_weight(lines,s)==stateweights[s]
            for target,p in P[s].items():
                assert pi[s]*p == pi[target]*P[target].get(s,Q(0))
        h=lambda s:int(0 in s)
        energy=sum((pi[s]*p*(h(s)-h(target))**2/2 for s in pi for target,p in P[s].items()),Q(0))
        mean=sum((pi[s]*h(s) for s in pi),Q(0))
        variance=mean*(1-mean)
        # The pair kernel chooses first-layer Gibbs and full layer swap equally.
        # The swap term vanishes for h+h, giving E_pair = E_single/2.
        pair_energy=energy/2
        ratio=variance/pair_energy
        assert ratio >= t*t/240
        rows.append({'L':length,'positive_states':len(pi),'single_energy':str(energy),'pair_energy':str(pair_energy),'variance':str(variance),'required_comparison':str(ratio),'universal_lower_bound':str(t*t/240)})
    result={'status':'PASS','arithmetic':'exact rational','fixtures':rows,'kernel':'one-pair conditional heat bath in first layer with probability 1/2; complete layer swap with probability 1/2','oracle_interface':'Each transition acquired from <=10 point determinant weights per removal, no unconditional or ambient-hole partition normalizer','scope':'Exact small reversibility/energy calculation; general no-go theorem is in single_pair_no_go.txt','wall_seconds':time.perf_counter()-started}
    target=Path(__file__).with_suffix('.json')
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','cases':len(rows),'wall_seconds':result['wall_seconds'],'result_path':str(target)}))


if __name__=='__main__':
    main()
