"""Exact six-state order witness and endpoint-only direct comparator."""
from fractions import Fraction as F
from pathlib import Path
import json, math, sys
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"core"))
from echo_compiler import sqrt_upper


def matrices():
    blocks=[[[F(4,5),F(9,50),0],[F(9,50),F(79,100),F(1,100)],
             [0,F(1,100),F(97,100)]],
            [[F(97,100),0,F(1,100)],[0,F(4,5),F(9,50)],
             [F(1,100),F(9,50),F(79,100)]]]
    result=[]
    for block in blocks:
        a=[[F(0) for _ in range(6)] for _ in range(6)]
        for i in range(3):
            for j in range(3):a[i][j]=F(block[i][j])
            a[i][i+3]=a[i+3][i]=F(1,500)
        for i,x in enumerate((F(1,4),F(1,3),F(2,5))):a[i+3][i+3]=x
        assert all(a[i][j]==a[j][i] for i in range(6) for j in range(6))
        assert max(map(sum,a))==F(491,500)
        assert all(a[i][i]>sum(a[i])-a[i][i] for i in range(6))
        result.append(a)
    return result


def truth(ops,word,end=0):
    v=[F(1)]+[F(0)]*5
    for i in word:v=[sum((x*y for x,y in zip(row,v)),F(0)) for row in ops[i]]
    return v[end]


def direct_trials(ops,word,n,rng):
    tables=[]
    for a in ops:
        rows=[]
        for row in a:
            ints=[int(x*1500) for x in row]
            assert all(F(x,1500)==y for x,y in zip(ints,row))
            rows.append(ints+[1500-sum(ints)])
        rows.append([0]*6+[1500])
        tables.append(np.cumsum(np.array(rows,dtype=np.int64),axis=1))
    state=np.zeros(n,dtype=np.int8)
    for i in word:
        draws=rng.integers(1500,size=n)
        state=np.sum(draws[:,None]>=tables[i][state],axis=1).astype(np.int8)
    return int(np.count_nonzero(state==0))


def interval(x,n,ell=10):
    return (max(F(0),(F(x)-sqrt_upper(F(2*ell*x)))/n),
            min(F(1),(F(x+ell)+sqrt_upper(F(ell*ell+2*ell*x)))/n))


if __name__=="__main__":
    ops=matrices()
    high=tuple(map(int,"00000000001111111111"))
    low=tuple(map(int,"00101101011010110100"))
    assert len(high)==len(low)==20
    assert high.count(0)==low.count(0)==10
    ph,pl=truth(ops,high),truth(ops,low)
    assert ph-pl>F(63,1000)
    assert truth(ops,high[::-1])==ph and truth(ops,low[::-1])==pl
    transport_forward=truth(ops,high,end=2)
    transport_reverse=truth(ops,high[::-1],end=2)
    assert transport_forward>transport_reverse
    n=10000; rng=np.random.default_rng(2026102851)
    counts=[direct_trials(ops,w,n,rng) for w in (high,low)]
    intervals=[interval(x,n) for x in counts]
    gap=intervals[0][0]-intervals[1][1]
    assert gap>0
    result={
        "modes":[[[str(x) for x in row] for row in a] for a in ops],
        "exact_source_norm_upper":str(F(491,500)),
        "source_cap_used_by_parent":str(F(99,100)),
        "high_word":"".join(map(str,high)),"low_word":"".join(map(str,low)),
        "same_mode_counts":[10,10],"length":20,
        "high_probability_exact":str(ph),"low_probability_exact":str(pl),
        "difference_exact":str(ph-pl),
        "probability_diagnostics":[float(ph),float(pl),float(ph-pl)],
        "global_optimality_claimed":False,
        "transport_witness":{"source":0,"receiver":2,
            "forward_word":"".join(map(str,high)),
            "reverse_word":"".join(map(str,high[::-1])),
            "forward_probability_exact":str(transport_forward),
            "reverse_probability_exact":str(transport_reverse),
            "difference_exact":str(transport_forward-transport_reverse),
            "probability_diagnostics":[float(transport_forward),float(transport_reverse),
                                       float(transport_forward-transport_reverse)]},
        "direct_comparator":{"trials_per_word":n,"endpoint_counts":counts,
            "probability_intervals":[[str(x) for x in pair] for pair in intervals],
            "certified_gap_lower":str(gap),"certified_gap_lower_float":float(gap),
            "failure_probability_upper":4*math.exp(-10),
            "logical_trials":2*n,"physical_preparations_upper":2+2*n-sum(counts),
            "primitive_steps":40*n,"endpoint_membership_readings":2*n,
            "hidden_ids_used_by_estimator":False,"seed":2026102851},
        "all_exact_checks_passed":True}
    path=Path(__file__).with_name("MULTIBOUNDARY_ORDER_RESULTS.json")
    path.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"probabilities":result["probability_diagnostics"],
        "counts":counts,"certified_gap_lower":float(gap),
        "primitive_steps":40*n,"physical_preparations_upper":2+2*n-sum(counts),
        "output":str(path)},indent=2))
