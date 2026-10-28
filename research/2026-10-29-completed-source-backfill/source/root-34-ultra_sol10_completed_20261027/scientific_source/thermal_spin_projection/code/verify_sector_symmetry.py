"""Exact integer/sqrt6 component controls for +/-physical magnetization.

No eigensolver is used. This checks the physical spin-inversion permutation
that justifies retaining positive-M blocks twice in the angular trace.
"""
import json,pathlib,time
from angular_spin_projection import ROOT,sector_parts

def main():
    start=time.monotonic();rows=[];dimension=0
    for mag in range(13):
        states,positive=sector_parts(6,mag);negative_states,negative=sector_parts(6,-mag)
        lookup={w:i for i,w in enumerate(negative_states)}
        permutation=[lookup[tuple(-m for m in w)]for w in states]
        assert len(permutation)==len(states)==len(negative_states)
        for k in range(4):
            transformed=negative[k][permutation,:][:,permutation]
            target=positive[k]if k<2 else positive[k].T
            assert (transformed-target).nnz==0
        dimension+=len(states)*(1 if mag==0 else 2)
        rows.append({'magnetization':mag,'block_dimension':len(states),
                     'D0_D1_spin_inversion_exact':True,'E0_E1_transpose_spin_inversion_exact':True})
    assert dimension==15625
    result={'status':'PASS_EXACT_ALL_SIGNED_SECTOR_SPIN_INVERSION','rows':rows,
            'all_physical_states_counted':dimension,'seconds':time.monotonic()-start,
            'scope':'Exact physical component/symmetry control; no floating trace-exp or new thermal input certification.'}
    (ROOT/'results/sector_symmetry_replay.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k!='rows'},indent=2))

if __name__=='__main__':main()
