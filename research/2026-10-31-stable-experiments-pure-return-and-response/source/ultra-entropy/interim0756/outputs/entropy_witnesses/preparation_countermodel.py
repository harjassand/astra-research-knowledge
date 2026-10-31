#!/usr/bin/env python3
"""Exact finite-horizon observational counterfeit with charged preparation."""
from fractions import Fraction as Q
from pathlib import Path
from collections import defaultdict
import json
import time

from entropy_cone import log_bounds

HERE=Path(__file__).resolve().parent


def label(x):
    return int(x%4>=2)


def chain(N):
    m=2*N+4
    pi=[Q(2*3**i,3**m-1) for i in range(m)]
    P=[]
    for i in range(m):
        row=defaultdict(Q)
        row[min(i+1,m-1)]+=Q(3,4)
        row[max(i-1,0)]+=Q(1,4)
        P.append(dict(row))
    return pi,P


def observed_law(P,initial,N):
    paths={(i,(label(i),)):mass for i,mass in initial.items()}
    for _ in range(N):
        nxt=defaultdict(Q)
        for (i,word),mass in paths.items():
            for j,probability in P[i].items():
                nxt[j,word+(label(j),)]+=mass*probability
        paths=nxt
    law=defaultdict(Q)
    for (i,word),mass in paths.items():
        law[word]+=mass
    assert sum(law.values())==1
    return dict(law)


def check_preparation(N):
    pi,P=chain(N)
    assert sum(pi)==1
    for i,row in enumerate(P):
        assert sum(row.values())==1
        for j,p in row.items():
            assert pi[i]*p==pi[j]*P[j].get(i,0)
    support_mass=sum(pi[N:N+4])
    assert support_mass==Q(80*3**N,3**(2*N+4)-1)<Q(1,3**N)
    l3,h3=log_bounds(Q(3),96)
    lnorm,hnorm=log_bounds(Q(3**(2*N+4)-1),96)
    l8,h8=log_bounds(Q(8),96)
    Dlo=lnorm-h8-Q(2*N+3,2)*h3
    Dhi=hnorm-l8-Q(2*N+3,2)*l3
    assert Dlo>N*h3
    scale=2**96
    Dlo=Q((Dlo*scale).numerator//(Dlo*scale).denominator,scale)
    Dhi=Q(-((-Dhi*scale).numerator//(-Dhi*scale).denominator),scale)
    return {'horizon':N,'line_hidden_states':len(pi),
            'stationary_support_mass':str(support_mass),
            'preparation_D_interval':[str(Dlo),str(Dhi)],
            'preparation_D_preview':float((Dlo+Dhi)/2),
            'N_log3_upper_preview':float(N*h3),
            'detailed_balance_exact':True}


def main():
    start=time.perf_counter()
    ring=[{(i+1)%4:Q(3,4),(i-1)%4:Q(1,4)} for i in range(4)]
    comparisons=[]
    for N in range(1,10):
        pi,P=chain(N)
        reference=observed_law(ring,{i:Q(1,4) for i in range(4)},N)
        counterfeit=observed_law(P,{i:Q(1,4) for i in range(N,N+4)},N)
        assert reference==counterfeit
        assert all(reference[word]==reference.get(word[::-1],Q(0)) for word in reference)
        comparisons.append({'horizon':N,'exact_equal_word_laws':True,
                            'distinct_observed_words':len(reference)})
    preparations=[check_preparation(N) for N in (1,2,9,32,128)]
    output={'scope':__doc__,'finite_word_controls':comparisons,
            'preparation_controls':preparations,
            'stationary_reference_entropy_cost':'0',
            'actual_nonstationary_entropy_claimed_zero':False,
            'new_stationary_record_acquisitions':0,
            'general_claim_proof':'PREPARATION.txt',
            'status':'EXACT_PREPARATION_COUNTERMODEL_CHECKED',
            'seconds':time.perf_counter()-start}
    (HERE/'preparation_receipt.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':output['status'],
                      'exact_horizon_checks':len(comparisons),
                      'preparation_checks':len(preparations),
                      'seconds':output['seconds']},indent=2))


if __name__=='__main__':
    main()
