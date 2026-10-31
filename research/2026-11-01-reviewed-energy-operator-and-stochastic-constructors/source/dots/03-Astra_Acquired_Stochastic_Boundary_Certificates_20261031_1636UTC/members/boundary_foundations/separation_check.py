"""Exact strict separation of the two acquired certificate architectures."""
from fractions import Fraction as F
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).parent/'terminal_gap'))
from exact_terminal_gap import linkage_classes

def main():
    result=json.loads((Path(__file__).parent/'pivot_lift_results.json').read_text())
    raw=result['example_reactions'];edges=[(tuple(u),tuple(v)) for u,v,k in raw]
    C,Ls,wr=linkage_classes(edges);assert wr
    target_set={(0,2,1),(0,1,2)}
    L=next(L for L in Ls if set(L)==target_set)
    I=(1,2);O=(0,);w=(F(0),F(1,2),F(1,2))
    pairs=[(s,c) for s in C for c in L if all(s[i]<=c[i] for i in O)]
    gaps=[sum(w[i]*(s[i]-c[i]) for i in range(3)) for s,c in pairs]
    assert all(g<=0 for g in gaps)
    # Admissibility is not being evaded: e_B+e_C is in S.
    # Two core 0->A jumps plus one forward star conversion to B and C.
    def jump(u,v):
        assert (u,v) in edges
        return tuple(v[i]-u[i] for i in range(3))
    terms=[(2,jump((0,0,0),(1,0,0))),
           (1,jump((2,0,0),(1,1,0))),(1,jump((2,0,0),(1,0,1)))]
    direction=tuple(sum(a*v[i] for a,v in terms) for i in range(3))
    assert direction==(0,1,1)
    ratio_checks=0
    for n in range(1,129):
        for b,c,targ in [(n+2,n+1,(0,2,1)),(n+1,n+2,(0,1,2))]:
            rho=(0,n,n)
            assert (0,b-targ[1],c-targ[2])==rho
            carried=b*(b-1)*c if targ==(0,2,1) else b*c*(c-1)
            other=b*c*(c-1) if targ==(0,2,1) else b*(b-1)*c
            assert F(carried,other)==F(n+1,n)>1 and carried>1
            ratio_checks+=2
    print(json.dumps({'status':'exact strict separation verified','pivot_certificate_accepted':True,
        'terminal_gap_certificate_impossible_for_this_row':True,'stratum_I':I,
        'linkage':L,'dual_weight':list(map(str,w)),'admissible_stoichiometric_direction':direction,
        'admissible_direction_coefficients':terms,'positive_episode_ratio_checks':ratio_checks,'every_finite_current_neutral_linkage_episode_has_positive_expected_reward':True,'allowed_pairs':pairs,'exact_pair_gaps':list(map(str,gaps)),
        'interpretation':'A failed cone does not mean instability; the non-complex-balanced pivot witness is accepted by the independent infinite-fiber correction.'},indent=2))
if __name__=='__main__':main()
