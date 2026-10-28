"""Exact controlled-syndrome exploration witness. No sampled outcomes."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
ES=[0,4,2,1]
PS=[F(0),F(1,1000),F(1,100),F(1,20),F(1,10),F(1,5),F(1,4),F(49,100),F(1,2)]

def zero(): return [[F(0) for _ in range(16)] for _ in range(16)]
def belladd(J,f,w):
    ix=[f,8+(7^f)]
    for a in ix:
        for b in ix:J[a][b]+=w/2

rows=[]
for p in PS:
    t=1-2*p
    ws=[p**f.bit_count()*(1-p)**(3-f.bit_count()) for f in range(8)]
    ai=[sum(ws[e^g] for e in ES)/4 for g in ES]
    ax=[sum(ws[e^g^7] for e in ES)/4 for g in ES]
    assert [x+y for x,y in zip(ai,ax)]==[F(1,4)]*4
    hz=[x-y for x,y in zip(ai,ax)]
    assert hz==[(3*t-t**3)/8]+[(t+t**3)/8]*3
    assert all(x>=0 for x in hz)
    gamma=min(hz)/2
    assert gamma==(t+t**3)/16
    assert sum(ax)==(3*p-3*p*p+2*p**3)/2
    Jphys=zero(); Jmodel=zero()
    for e in ES:
        for f,w in enumerate(ws):belladd(Jphys,e^f,w/4)
    for g,x,y in zip(ES,ai,ax):
        belladd(Jmodel,g,x);belladd(Jmodel,g^7,y)
    assert Jphys==Jmodel
    for x in range(8):
        for y in range(8):
            assert Jphys[x][y]+Jphys[8+x][8+y]==(F(1,8) if x==y else 0)
    for l in range(2):
        for m in range(2):
            assert sum(Jphys[8*l+x][8*m+x] for x in range(8))==(F(1,2) if l==m else 0)
    native=p*(1-p)*(1-2*p)/2
    ratio=None
    if 0<p<F(1,2):
        ratio=gamma/native
        assert ratio==(1+t*t)/(2*(1-t*t))
        assert (gamma>native)==(3*t*t>1)
    rows.append({'p':str(p),'unsigned_floor':'1/8','signed_X_gap':'1/8',
                 'signed_Z_gap':str(gamma),'native_gap':str(native),
                 'gap_ratio':str(ratio) if ratio is not None else None,
                 'calibration_oracle_loss':str(sum(ax)),
                 'payload_oracle_loss':str(3*p*p-2*p**3)})

root=Path(__file__).parent
out={'status':'PASS exact injected physical-error Choi/contrast witness',
     'source_draws':0,'rng_draws':0,'noise_levels':len(PS),
     'exact_Choi_entries':256*len(PS),'physical_injection_error_terms':32*len(PS),
     'fixtures':rows,
     'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
       [Path(__file__),root/'ordinary_controlled_syndrome_excitation_witness_20261028.md']}}
(root/'ordinary_controlled_syndrome_excitation_witness_20261028.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
