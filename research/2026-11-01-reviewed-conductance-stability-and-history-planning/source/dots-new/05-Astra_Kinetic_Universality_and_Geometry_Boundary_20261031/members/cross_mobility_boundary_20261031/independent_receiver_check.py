#!/usr/bin/env python3
"""Independent exact output replay and parser adversaries for receive.py."""
from copy import deepcopy
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path
import random

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('cross_receiver_under_review', HERE/'receive.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
def readq(o): return Q(int(o['numerator']),int(o['denominator']))
def source(k,e): return {'schema':module.SCHEMA,'k':k,'epsilon':{'numerator':e.numerator,'denominator':e.denominator}}

def verify(cert):
    src=cert['input']; k=src['k']; e=Q(src['epsilon']['numerator'],src['epsilon']['denominator'])
    c=Q(k*k)/(1-e)
    expected_matrix=[[Q(1),Q(k)],[Q(k),c]]
    assert [[readq(v) for v in row] for row in cert['model']['mobility']]==expected_matrix
    assert readq(cert['model']['determinant'])==c-k*k>0
    assert readq(cert['model']['longitudinal_schur_complement'])==e
    x=Q(k*k,128); floorx=x.numerator//x.denominator
    y=Q(k*k,2); ceily=-((-y.numerator)//y.denominator)
    lo=max(e,Q(1,3**ceily))/16
    hi=36*e+Q(1200,k*2**floorx)
    cp=cert['capacity_normalized']
    assert readq(cp['lower'])==lo
    assert readq(cp['upper'])==hi
    assert readq(cp['core_upper'])==36*e
    assert readq(cp['patch_upper'])==hi-36*e
    assert readq(cp['tilted_line_lower'])==Q(1,16*3**ceily)
    assert readq(cert['capacity_over_basin_mass']['lower'])==2*lo
    assert readq(cert['capacity_over_basin_mass']['upper'])==4*hi
    assert readq(cert['eigenvalue_condition_number']['lower'])==c/e
    assert readq(cert['eigenvalue_condition_number']['upper'])==(c+1)**2/(c*e)
    assert lo<=hi

n_existing=0
for cert in json.loads((HERE/'certificates.json').read_text()):
    verify(cert); n_existing+=1
rng=random.Random(731)
n_new=0
for _ in range(70):
    k=rng.randint(1,128)
    denom=rng.randint(2,100000)
    e=Q(rng.randint(1,denom-1),denom)
    verify(module.receive(source(k,e))); n_new+=1
for k,e in [(1,Q(1,10**50+3)),(3,Q(10**50+2,10**50+3)),(128,Q(1,10**20+1))]:
    verify(module.receive(source(k,e))); n_new+=1
base=source(7,Q(1,13))
bad=[]
for field,value in [('k',False),('k',[]),('k',{}),('schema',None),('schema',[])]:
    v=deepcopy(base);v[field]=value;bad.append(v)
for field,value in [('numerator',False),('numerator','1'),('denominator',True),('denominator',None),('denominator',13.0)]:
    v=deepcopy(base);v['epsilon'][field]=value;bad.append(v)
for field in ['schema','k','epsilon']:
    v=deepcopy(base);del v[field];bad.append(v)
v=deepcopy(base);v['epsilon']=[1,13];bad.append(v)
v=deepcopy(base);v['epsilon']['denominator']=-13;bad.append(v)
v=deepcopy(base);v['epsilon']={'numerator':2,'denominator':26};bad.append(v)
v=deepcopy(base);v['epsilon']['another']=0;bad.append(v)
for v in bad:
    try: module.receive(v)
    except (ValueError,TypeError,KeyError): pass
    else: raise AssertionError(f'accepted malformed input {v!r}')
duplicate_rejections=0
for raw in [
    '{"k":1,"k":2}',
    '{"epsilon":{"numerator":1,"numerator":2,"denominator":3}}',
    '{"k":1,"\\u006b":2}',
]:
    try: module.strict_json_loads(raw)
    except ValueError as error:
        assert 'duplicate JSON key' in str(error); duplicate_rejections+=1
    else: raise AssertionError('duplicate raw key accepted')
budget_rejections=0
for invalid_budget in [0,-1,True,1.0,'128']:
    try: module.receive(base,max_expanded_power=invalid_budget)
    except ValueError: budget_rejections+=1
    else: raise AssertionError('invalid resource budget accepted')
for k in [16,17]:
    needed=(k*k+1)//2
    verify(module.receive(source(k,Q(1,13)),max_expanded_power=needed))
    try: module.receive(source(k,Q(1,13)),max_expanded_power=needed-1)
    except ValueError as error:
        assert 'resource_budget' in str(error); budget_rejections+=1
    else: raise AssertionError('power budget boundary missed')
try: module.receive(source(10**20,Q(1,2)))
except ValueError as error:
    assert 'resource_budget' in str(error); budget_rejections+=1
else: raise AssertionError('huge expanded power not rejected')
result={'status':'PASS','duplicate_raw_key_rejections':duplicate_rejections,
        'resource_budget_rejections':budget_rejections,'exact_budget_boundaries_accepted':2,'existing_certificates_replayed':n_existing,'additional_valid_models_checked':n_new,
        'additional_malformed_objects_rejected':len(bad),'exact_arithmetic':True,
        'not_claimed':'Huge k was rejected before power allocation; no actual memory-exhaustion test, capacity PDE, or physical identification.'}
(HERE/'independent_receiver_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
