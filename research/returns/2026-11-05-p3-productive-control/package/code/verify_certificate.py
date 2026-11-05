#!/usr/bin/env python3
"""Verify a saved rational policy certificate without the synthetic source."""
import json
from fractions import Fraction as F
from pathlib import Path
root=Path(__file__).resolve().parents[1]
records=[]
for suffix in ('','_swapped'):
    data=json.loads((root/'results'/('calibration_counts'+suffix+'.json')).read_text())
    cert=json.loads((root/'results'/('policy_certificate'+suffix+'.json')).read_text())
    m=int(data['samples_per_action']);radius=F(data['total_radius'])
    rows={a:{k:F(v) for k,v in row.items()} for a,row in cert['boxes'].items()}
    for a,row in rows.items():
        cnt=data['counts'][a]
        assert sum(cnt.values())==m
        assert row['pL']==F(cnt['up'],m)-radius
        assert row['pU']==F(cnt['up'],m)+radius
        assert row['qL']==F(cnt['down'],m)-radius
        assert row['qU']==F(cnt['down'],m)+radius
        assert row['rL']==row['rU']==F(data['rewards'][a])
        assert 0<row['pL']<=row['pU'] and 0<=row['qL']<=row['qU']
        assert row['pU']+row['qU']<1
    a0=cert['prefix'][0];tail=cert['tail']
    L=rows[a0]['rL']/rows[a0]['pU']
    assert L==F(cert['d0_lower'])
    for a,row in rows.items():
        if a!=a0:assert L>row['rU']/row['pL']
    R=rows[tail]['qL']/rows[tail]['pU'];c=rows[tail]['rL']/rows[tail]['pU']
    assert R>1
    for a,row in rows.items():
        if a==tail:continue
        upper_slope=row['qU']/row['pL'];upper_intercept=row['rU']/row['pL']
        assert R>upper_slope
        # Positivity at L plus positive slope proves every d >= L.
        assert (c-upper_intercept)+(R-upper_slope)*L>0
    assert c+R*L>=L
    records.append({'input':suffix or 'standard','status':'PASS','prefix':[a0],'tail':tail,
                    'proof':'startup dominance; affine tail dominance on [L,infinity); interval invariant'})
(root/'results'/'independent_certificate_verification.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records,indent=2))
