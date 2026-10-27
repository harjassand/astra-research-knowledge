"""Independent NONPHYSICAL arithmetic/CLI review, not an acquired experiment."""
from pathlib import Path
from fractions import Fraction as F
import copy, hashlib, importlib.util, json, subprocess, sys

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'photon_certificate_20261027'
raw=(SOURCE/'photon_certificate.py').read_bytes()
snapshot=HERE/'REVIEWED_READER.py'
snapshot.write_bytes(raw)
spec=importlib.util.spec_from_file_location('reviewed_photon_reader',snapshot)
reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
header=json.loads((SOURCE/'header.example.json').read_text());header['N']=3

def record(points):return {'count':len(points),'phasors':points}
A={'kind':'block','index':0,
   'bright_a':[record([[1,0],[0,1]]),record([[1,0]])],
   'bright_b':[record([[-1,0]]),record([[0,1],[0,-1]])],
   'dark':[record([[0,1]]),record([[-1,0]])]}
B={'kind':'block','index':1,
   'bright_a':[record([[1,0]]),record([[0,1]])],
   'bright_b':[record([[1,0]]),record([[0,1]])],
   'dark':[record([]),record([])]}
C=copy.deepcopy(A);C['index']=2;C['dark'][0]=record([[0,1],[1,0]])
blocks=[A,B,C]
expected_A=list(map(F,['0','-1/8','3/8','0','5/16','1/16','1/8','1/16']))
assert reader.block(A,0,[4,4])[0]==expected_A
assert reader.block(B,1,[4,4])[0]==list(map(F,['1/4','0','0','1/4','0','0','0','0']))
assert reader.block(C,2,[4,4])[0]==[F(0)]*8

def encode(h,bs):return '\n'.join(json.dumps(v,separators=(',',':')) for v in [h,*bs])+'\n'
fixture=encode(header,blocks);(HERE/'NONPHYSICAL_LITERAL.jsonl').write_text(fixture)

def cli(s):
    proc=subprocess.run([sys.executable,str(snapshot),'-'],input=s,text=True,capture_output=True)
    return proc.returncode,json.loads(proc.stdout)

code,result=cli(fixture)
assert code==0 and result['status']=='UNKNOWN'
assert result['confidence_lower']=='49/50' and result['physical_experiment_acquired_or_qualified'] is False
assert result['blocks']=={'expected':3,'processed':3,'clipped_whole':1,'retained':2}
assert list(map(F,result['confidence_construction']['empirical_means']))==list(map(F,['1/12','-1/24','1/8','1/12','5/48','1/48','1/24','1/48']))
assert list(map(F,result['confidence_construction']['unbiased_variances']))==list(map(F,['1/48','1/192','3/64','1/48','25/768','1/768','1/192','1/768']))
(HERE/'NONPHYSICAL_LITERAL_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')

invalid=[]
def reject(name,h=header,bs=blocks,raw_input=None):
    rc,out=cli(raw_input if raw_input is not None else encode(h,bs))
    assert rc==2 and out['status']=='INVALID_INPUT' and out['affinity_lower'] is None,name
    invalid.append(name)

reject('missing fixed-N block',bs=blocks[:-1])
extra=copy.deepcopy(A);extra['index']=3
reject('extra fixed-N block',bs=blocks+[extra])
bad=copy.deepcopy(blocks);bad[1]['index']=2
reject('nonconsecutive index',bs=bad)
bad=copy.deepcopy(blocks);bad[2]['dark'][0]['count']=3
reject('bad count even in clipped block',bs=bad)
bad=copy.deepcopy(blocks);bad[2]['dark'][0]['phasors'][0]=[1,1]
reject('nonunit phasor even in clipped block',bs=bad)
bad=copy.deepcopy(blocks);bad[0]['bright_a'][0]['count']=True
reject('boolean count',bs=bad)
bad=copy.deepcopy(blocks);bad[0]['bright_a'][0]['phasors'][0]=[float('nan'),0]
reject('nonfinite phasor',bs=bad)
h=copy.deepcopy(header);h['alpha_stat']=.01
reject('binary float alpha',h=h)
h=copy.deepcopy(header);h['budget_scope']='PER_RECORD'
reject('per-record budget not accepted as dataset total',h=h)
h=copy.deepcopy(header);h['alpha_other_total']['unfunded']=1
reject('failure budget reaches one',h=h)
h=copy.deepcopy(header);h['unrecognized']=0
reject('unknown header field',h=h)
reject('duplicate JSON key',raw_input=fixture.replace('"N":3','"N":3,"N":3',1))
reject('blank record',raw_input=fixture+'\n')

api_cases=[]
for name,bad_lines in [
    ('None line before an otherwise hidden extra block',fixture.splitlines()+[None,json.dumps(A)]),
    ('non-line integer after fixed N',fixture.splitlines()+[0]),
    ('unencodable text line after fixed N',fixture.splitlines()+['\ud800']),
]:
    try:reader.certify(iter(bad_lines))
    except reader.InputError:api_cases.append(name)
    else:raise AssertionError(name)

# Reference intervals use a different exponential/CDF construction from reader.
oracle=json.loads((HERE.parent/'photon_reader_tail_oracle.json').read_text())
tails,_=reader.poisson_tails(F(80),144)
for k in (143,144,145):
    assert tails[k]>=F(oracle['tail_intervals'][str(k)]['upper'])
    assert tails[k]<=1
assert reader.poisson_tails(F(0),144)[0]=={145:F(0),144:F(0),143:F(0)}

root_cases=0
for x in [F(0),F(1),F(2),F(3,7),F(7,3),F(1,10**1000),F(10**1000)]:
    for bits in [1,3,32,99]:
        lo,hi=reader.sqrt_bounds(x,bits)
        assert 0<=lo<=hi and lo*lo<=x<=hi*hi
        assert x==0 or lo>0
        root_cases+=1
for x in [F(1),F(3,2),F(2),F(3200),F(10**1000)]:
    h=reader.log_upper(x)
    assert h.denominator==1 and (1<<int(h))>=x
    assert not h or (1<<(int(h)-1))<x

# Exact point-moment geometry is a software arithmetic test, not photon data.
g=reader.affinity_geometry([(F(1),F(0))]*2,[F(0)]*2,(F(0),F(1,2)),F(0),[F(1)]*2,[F(0)]*2,40)
assert g['status']=='CONDITIONAL_LOWER_BOUND' and F(g['radius_squared_lower'])==F(1,4)
assert F(g['affinity_squared_lower'])==12
assert F(g['affinity_lower'])**2<=12
gc=reader.affinity_geometry([(F(1),F(0))]*2,[F(0)]*2,(F(0),-F(1,2)),F(0),[F(1)]*2,[F(0)]*2,40)
assert gc['affinity_squared_lower']==g['affinity_squared_lower']
bad=reader.affinity_geometry([(F(1),F(0))]*2,[F(0)]*2,(F(0),F(2)),F(0),[F(1)]*2,[F(0)]*2,40)
assert bad['status']=='UNKNOWN' and 'inconsistent_radius_squared_ge_one' in bad['reasons']

# Deliberately fabricated deterministic stream, not asserted to obey the source,
# caps or IID contracts. It exercises the complete positive numerical branch.
# The conditional output MUST retain its nonphysical tag and False qualification.
positive_header=copy.deepcopy(header);positive_header['N']=8192
positive_header['lambda_on']=['1/1000']*2
positive_header['lambda_dark']=['1/1000']*2
def nonphysical_positive_stream():
    yield json.dumps(positive_header)+'\n'
    for i in range(positive_header['N']):
        row=dict(A);row['index']=i
        yield json.dumps(row)+'\n'
positive=reader.certify(nonphysical_positive_stream())
assert positive['status']=='CONDITIONAL_LOWER_BOUND'
assert F(positive['affinity_squared_lower'])>0
assert F(positive['affinity_lower'])**2<=F(positive['affinity_squared_lower'])
assert positive['data_kind']=='NONPHYSICAL_SOFTWARE_TEST'
assert positive['physical_experiment_acquired_or_qualified'] is False
(HERE/'NONPHYSICAL_POSITIVE_BRANCH_RESULT.json').write_text(json.dumps(positive,indent=2)+'\n')

summary={'scope':'INDEPENDENT_NONPHYSICAL_SOFTWARE_AND_ARITHMETIC_REVIEW_ONLY',
 'source':str(SOURCE/'photon_certificate.py'),'sha256':hashlib.sha256(raw).hexdigest(),
 'literal_block_and_stream_oracles_passed':True,'invalid_stream_cases':invalid,
 'invalid_API_cases':api_cases,
 'independent_poisson_tail_enclosures_passed':True,'sqrt_enclosure_cases':root_cases,
 'log_integer_certificate_cases':5,'exact_geometry_and_conjugation_passed':True,
 'full_stream_positive_numeric_branch_passed':True,
 'positive_stream_obeys_physical_or_IID_promises':False,
 'inconsistent_geometry_returns_unknown':True,'real_photon_or_source_qualification':False}
(HERE/'RESULT.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
