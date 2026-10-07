"""Exact scope guard: rescaling before NEW probes rescues the example.

Rescaling the already augmented law preserves the no-go. New uniform probes
in the new frame change that law and remove its T dependence.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
import time
from single_pair_checks import family,line_system,weights
from pair_heatbath_kernel import point_weight,transition_distribution
from itertools import combinations


def energy_ratio(lines):
    states={s:point_weight(lines,s) for s in combinations(range(len(lines)),2)}
    states={s:w for s,w in states.items() if w}
    z=sum(states.values(),Q(0))
    pi={s:w/z for s,w in states.items()}
    h=lambda s:int(0 in s)
    p=sum((pi[s]*h(s) for s in pi),Q(0))
    energy=sum((pi[s]*probability*(h(s)-h(target))**2/2 for s in pi for target,probability in transition_distribution(lines,s).items()),Q(0))
    return p*(1-p)/(energy/2)


def main():
    started=time.perf_counter()
    sigma=Q(1,10**8*5**4)
    fixed_ratio=energy_ratio(line_system(Q(1),sigma))
    rows=[]
    for half_length in [1,5,20]:
        T=Q(2**(2*half_length))
        d=[Q(1,2**half_length)]*3+[Q(2**half_length)]
        F=family(T)
        scaled=[[d[i]*F[i][j]*d[j] for j in range(4)] for i in range(4)]
        assert scaled==family(Q(1))
        original=line_system(T,sigma)
        preserving=line_system(Q(1),sigma)
        for label,(i,j) in enumerate(combinations(range(4),2),start=4):
            v,w,a,name=preserving[label]
            preserving[label]=(v,w,sigma*(d[i]*d[j])**2,name)
        for state in combinations(range(10),2):
            assert point_weight(preserving,state)==point_weight(original,state)/(T*T)
        preserving_ratio=energy_ratio(preserving)
        assert preserving_ratio==energy_ratio(original)
        # New uniform probes in the new frame use sigma rather than the
        # rescaled old probe activities; that explicitly changes the target.
        fresh_ratio=energy_ratio(line_system(Q(1),sigma))
        assert fresh_ratio==fixed_ratio
        rows.append({'L':2*half_length,'T':str(T),'preserved_augmented_law_energy_ratio':str(preserving_ratio),'fresh_probe_law_energy_ratio':str(fresh_ratio),'rescaled_core_probe_activity':str(sigma/(T*T)),'rescaled_extra_probe_activity':str(sigma)})
    result={'status':'PASS','arithmetic':'exact rational','fixtures':rows,'scope':'Additional balanced scaling followed by new uniform probes rescues this family; preserved augmented-target-law scaling leaves the obstruction unchanged','wall_seconds':time.perf_counter()-started}
    target=Path(__file__).with_suffix('.json')
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','cases':len(rows),'wall_seconds':result['wall_seconds'],'result_path':str(target)}))


if __name__=='__main__':
    main()
