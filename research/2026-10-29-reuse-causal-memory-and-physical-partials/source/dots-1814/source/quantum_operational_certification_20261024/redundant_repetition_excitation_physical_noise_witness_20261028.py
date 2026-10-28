"""Exact source-disabled repetition/physical-noise excitation witness."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

es = [0, 4, 2, 1]
ps = [F(1,1000),F(1,100),F(1,20),F(1,10),F(1,4),F(49,100)]

def add_bell_block(J, f, weight):
    inds = [f, 8+(7^f)]
    for a in inds:
        for b in inds:
            J[a][b] += weight/2

fixtures=[]
for p in ps:
    weights=[p**f.bit_count()*(1-p)**(3-f.bit_count()) for f in range(8)]
    assert sum(weights)==1
    GI=[weights[e] for e in es]
    GX=[weights[7^e] for e in es]
    total=[a+b for a,b in zip(GI,GX)]
    kappa=1-2*p
    for a,b in zip(GI,GX):
        assert a>=b>=0
        assert a-b>=kappa*(a+b)
    assert min((a-b)/(a+b) for a,b in zip(GI,GX))==kappa
    r=min(total)/2
    gamma=min(a-b for a,b in zip(GI,GX))/2
    assert r==p*(1-p)/2
    assert gamma==p*(1-p)*(1-2*p)/2
    assert min(total)/2>=gamma
    loss=sum(GX)
    assert loss==3*p*p-2*p*p*p
    Jphysical=[[F(0) for _ in range(16)] for _ in range(16)]
    Jmodel=[[F(0) for _ in range(16)] for _ in range(16)]
    for f,w in enumerate(weights):
        add_bell_block(Jphysical,f,w)
    for e,a,b in zip(es,GI,GX):
        add_bell_block(Jmodel,e,a)
        add_bell_block(Jmodel,7^e,b)
    assert Jphysical==Jmodel
    for l in range(2):
        for m in range(2):
            assert sum(Jphysical[8*l+x][8*m+x] for x in range(8))==(F(1,2) if l==m else 0)
    # Exact coherent encoding identity for all logical matrix units and errors.
    for f in range(8):
        e=f if f.bit_count()<=1 else 7^f
        alpha=0 if f.bit_count()<=1 else 1
        assert e in es
        for l in range(2):
            assert ((7*l)^f)==((7*(l^alpha))^e)
    fixtures.append({'p':str(p),'kappa':str(kappa),'patch_floor':str(r),
                     'signed_gap':str(gamma),'oracle_loss':str(loss),
                     'choi_entries_checked':256,'coherent_error_basis_checks':16})

out={'status':'PASS exact rational physical-noise/majority witness',
     'source_draws':0,'rng_draws':0,'fixtures':fixtures,
     'total_choi_entries_checked':256*len(ps),
     'total_coherent_error_basis_checks':16*len(ps)}
root=Path(__file__).parent
out['sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
 [Path(__file__),root/'redundant_repetition_excitation_physical_noise_witness_20261028.md']}
(root/'redundant_repetition_excitation_physical_noise_witness_20261028.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
