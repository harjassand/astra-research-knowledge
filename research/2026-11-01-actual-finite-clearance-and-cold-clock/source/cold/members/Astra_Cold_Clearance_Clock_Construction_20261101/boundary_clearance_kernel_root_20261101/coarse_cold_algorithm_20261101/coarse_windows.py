#!/usr/bin/env python3
"""Second phase of the prospective cold algorithm: use its FRESH scalar output.
Not a validator for an adversarially supplied certificate; phase one performs
both exact passes itself. No historical numerical scalar is read.
"""
from fractions import Fraction as Q
from math import isqrt,factorial
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
MANIFEST_SHA='9a682f735281dedfb5574da86d10c4e3e9a706ddd5d92867da0cab48ec71d348'
SOURCE_LIMIT=1<<20

def bounded_read(path,limit):
    with path.open('rb') as stream:data=stream.read(limit+1)
    if len(data)>limit:raise ValueError('bounded input exceeded')
    return data

def check_sources():
    blob=bounded_read(HERE/'COLD_SOURCE_BINDINGS.json',1<<16)
    assert len(blob)<1<<16 and hashlib.sha256(blob).hexdigest()==MANIFEST_SHA
    rows=json.loads(blob)['files'];assert len(rows)<=64
    total=len(blob);seen=set()
    for row in rows:
        name=row['path'];p=Path(name)
        assert len(name)<=256 and not p.is_absolute() and '..' not in p.parts and name not in seen
        seen.add(name);path=ROOT/p
        data=bounded_read(path,SOURCE_LIMIT-total);total+=len(data)
        assert total<=SOURCE_LIMIT
        assert hashlib.sha256(data).hexdigest()==row['sha256']
        if 'accepted_status' in row:
            assert json.loads(data).get(row.get('accepted_status_key','status'))==row['accepted_status']
    return len(rows),total

def sqrt_up(x):
    scale=10**24
    n=isqrt(x.numerator*scale*scale//x.denominator)
    if Q(n*n,scale*scale)<x:n+=1
    out=Q(n,scale)
    assert out*out>=x and Q((n-1)**2,scale*scale)<x
    return out

def decimal(x,places,up):
    assert x>=0
    scale=10**places;n=x.numerator*scale//x.denominator
    if up and Q(n,scale)<x:n+=1
    return str(n//scale)+'.'+str(n%scale).zfill(places)

def fixture(t,lo,hi):
    assert t in (10000,100000)
    r=Q(11,20000)+Q(4380,19*t)+Q(7254,t*t)
    v=Q(1449,800*t)+Q(1285200,t**3)
    j=Q(27,25*t)
    m=2*j+sqrt_up(12*v+4*j*j)
    eps=Q(1,t)+r+m+Q(3000000,t**6)
    assert hi+Q(1,t)+r+m+Q(1,70*t*t)<4
    low=lo-eps;high=hi+eps+Q(5,t)
    for x in (r,v,j,m,eps,low,high):
        assert max(abs(x.numerator).bit_length(),x.denominator.bit_length())<2048
    return {'N':str(t**5),'T':str(t),'scaled_interval':[decimal(low,6,False),decimal(high,6,True)],
            'physical_interval':[decimal(low*t,6,False),decimal(high*t,6,True)],
            'epsilon_upper':decimal(eps,15,True),'total_failure_upper':'<1/100 under the separately received source theorems',
            'output_scope':'First S<=15(N+2)/16 from raw corner; original4T, actual entropy5 continuation'}

def main():
    count,size=check_sources()
    data=bounded_read(HERE/'COARSE_CERTIFICATE.json',(1<<16)-1)
    cert=json.loads(data)
    assert cert['fixed_parameters']=={'bits':80,'degree':28,'order':6,'grid_power':6,'terminal_e':16}
    assert cert['algorithm_source_sha256']==hashlib.sha256(bounded_read(HERE/'coarse_clock.py',1<<16)).hexdigest()
    assert cert['second_exact_pass_matched'] and cert['steps']<=320
    verified=json.loads(bounded_read(HERE/'INDEPENDENT_COARSE_CHECK.json',(1<<16)-1))
    assert verified['status']=='PASS_DIFFERENT_IMPLEMENTATION_COARSE_EXACT_REPLAY'
    assert verified['verifier_source_sha256']==hashlib.sha256(bounded_read(HERE/'independent_coarse_verify.py',1<<16)).hexdigest()
    assert verified['scalar_decimal_outward']==cert['s_star_decimal_outward']
    assert verified['scalar_width_upper']==cert['total_width_decimal_upper']
    assert len(verified['mathematical_fields_exactly_rebuilt'])>=20
    lo,hi=Q(cert['s_star_lower']),Q(cert['s_star_upper'])
    assert 0<lo<hi<2 and hi-lo<Q(1,100000)
    # The same elementary arithmetic failure budget as the received two fixtures.
    assert sum(Q(6**k,factorial(k)) for k in range(18))>400
    assert sum(Q(4**k,factorial(k)) for k in range(10))>50
    assert 50**16>6*10**25 and 160*10**50<2**200
    assert Q(50000**2,520*64**2+1)>1000
    assert Q(1,200)+Q(1,10**8)+Q(16,2**100)<Q(1,100)
    for t in (10000,100000):
        n=t**5;y=Q(n,1920*10**12)-169
        assert y>=50000 and y/n<Q(1,1920*10**12)
        assert min(Q(n,6200),t,5*t,276,Q(t**3-1,20),Q(t**3,2500),Q(t,80))>=100
    out={'status':'NEW_COARSE_COLD_RECEIVER_AUTHOR_PENDING_INDEPENDENT_REVIEW',
         'fresh_scalar_decimal_outward':cert['s_star_decimal_outward'],
         'fresh_scalar_width_upper':cert['total_width_decimal_upper'],
         'source_files_verified':count,'source_bytes_read_including_manifest':size,
         'fresh_scalar_passes_charged':3,'different_verification_implementation_passed':True,'historical_scalar_certificates_read':0,
         'fixtures':[fixture(t,lo,hi) for t in (10000,100000)],
         'prospective_bit_cost_upper':'300000000000000000000',
         'cost_scope':'Specified bounded arithmetic algorithm with source input, two exact passes, verification, and both fixtures; not Python wall time or total research expenditure.'}
    blob=(json.dumps(out,indent=2)+'\n').encode();assert len(blob)<1<<16
    (HERE/'COARSE_WINDOWS.json').write_bytes(blob)
    print(blob.decode(),end='')

if __name__=='__main__':main()
