#!/usr/bin/env python3
"""Checks for the odd repeated reciprocal grid used in the bit-cost proof."""
import json
from pathlib import Path
import mpmath as mp
from response_exact_bath import repeated_dyadic_nodes,realize

mp.mp.dps=100
rows=[]
for L,m in [(1,3),(2,3)]:
    aa=repeated_dyadic_nodes(L,m);r=realize(aa);ss=r['poles'];U=sum(aa);M=len(aa)+1
    assert abs(sum(1/a for a in aa)-U)<mp.mpf('1e-90')
    assert min(ss)>=mp.pi/(2*U)
    assert max(ss)<=2*U/mp.pi
    assert min(ss[i+1]-ss[i] for i in range(len(ss)-1))>=mp.pi/(2*U)
    assert min(abs(s-1) for s in ss)>=mp.pi/(4*U)
    Rsum=2+sum(ss);H=r['H'];trH2=sum((H*H)[i,i] for i in range(M))
    assert mp.re(trH2)<=Rsum**2
    assert r['physical_residual']<mp.mpf('1e-65')
    assert r['transfer_error']<mp.mpf('1e-65')
    rows.append({'L':L,'m':m,'modes':M,'pole_separation_checks':'PASS',
                 'gram_condition':str(r['gram_condition']),
                 'physical_residual':str(r['physical_residual']),
                 'transfer_error':str(r['transfer_error']),
                 'H_F_norm':str(mp.sqrt(mp.re(trH2))),
                 'proved_H_norm_upper':str(Rsum)})
P=Path(__file__).resolve().parent
(P/'results/reciprocal_synthesis.json').write_text(json.dumps(rows,indent=2))
print(json.dumps(rows,indent=2))
