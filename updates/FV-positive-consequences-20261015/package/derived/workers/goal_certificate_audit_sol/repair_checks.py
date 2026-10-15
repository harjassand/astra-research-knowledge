#!/usr/bin/env python3
"""Check repaired snapshot against independent references and prior failures."""
import decimal
from decimal import Decimal as D
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import sys
sys.dont_write_bytecode=True
import audit_checks as audit

BASE=Path(__file__).resolve().parent
path=BASE/'snapshots/repaired_terminal_mass_certificate.py'
spec=importlib.util.spec_from_file_location('repaired_certificate',path)
mod=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=mod
spec.loader.exec_module(mod)
audit.mod=mod
np=mod.np

def rejects(fn):
    try: fn()
    except (ValueError,AssertionError,IndexError,TypeError) as e:
        return dict(rejected=True,error=repr(e))
    raise AssertionError('Invalid certificate input was accepted')

def main():
    rng=random.Random(776)
    result={'snapshot_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'valid_cases':[],'rejections':{}}
    g=mod.graph(2,[(0,1,1)],[1,1],0,1)
    result['rejections']['ungrounded']=rejects(lambda:mod.interval_certificate(g,np.zeros(2),np.ones(2),np.array([0]),50))
    result['rejections']['duplicate_tree']=rejects(lambda:mod.interval_certificate(g,np.zeros(2),np.zeros(2),np.array([0,0]),50))
    for name,cval,wval in [('negative_mass',1,-1),('zero_mass',1,0),('zero_conductance',0,1),('nonfinite_conductance',float('inf'),1)]:
        bad=mod.graph(2,[(0,1,cval)],[wval,1],0,1)
        result['rejections'][name]=rejects(lambda:mod.interval_certificate(bad,np.zeros(2),np.zeros(2),np.array([0]),50))
    g=mod.graph(3,[(0,1,1),(1,2,1),(2,0,1)],[1,1,1],0,2)
    result['rejections']['false_cached_blocks']=rejects(lambda:mod.interval_certificate(g,np.zeros(3),np.zeros(3),np.array([0,1]),50,
        blocks=(np.arange(3),np.ones(3,dtype=int))))
    gmass=mod.graph(2,[(0,1,1)],[1,1],0,1)
    gmass.w_bounds=[(D('2'),D('3')),(D('1'),D('1'))]
    massonly=mod.interval_certificate(gmass,np.zeros(2),np.zeros(2),np.array([0]),50)
    result['mass_only_bands_metadata']={'certificate':massonly,
        'nominal_binary64_mfpt':'1',
        'nominal_binary64_excluded':not audit.F(D(massonly['lower']))<=1<=audit.F(D(massonly['upper'])),
        'remaining_issue':'scope label should indicate coefficient bands when either c_bounds or w_bounds is present'}
    for name,bands in [('negative_band',[(D('-1'),D('1'))]*3),('inverted_band',[(D('2'),D('1'))]*3),
                       ('nonfinite_band',[(D('1'),D('Infinity'))]*3),('wrong_band_count',[(D('1'),D('1'))])]:
        g.c_bounds=bands
        result['rejections'][name]=rejects(lambda:mod.interval_certificate(g,np.zeros(3),np.zeros(3),np.array([0,1]),50))
    for run in range(60):
        n=rng.randint(2,8)
        edges=[(i,rng.randrange(i),audit.F(rng.randint(1,30),8)) for i in range(1,n)]
        for _ in range(rng.randint(0,7)):
            u,v=rng.sample(range(n),2)
            edges.append((u,v,audit.F(rng.randint(1,30),8)))
        target=rng.randrange(n); source=(target+1)%n
        g=mod.graph(n,[(u,v,float(c)) for u,v,c in edges],
                    [rng.randint(1,50)/16 for _ in range(n)],source,target)
        x=np.array([rng.randint(-50,50)/32 for _ in range(n)])
        y=np.array([rng.randint(-50,50)/32 for _ in range(n)])
        x[target]=y[target]=0
        _,tree=audit.independent_tree_route(n,edges,target,[audit.F(0)]*n)
        result['valid_cases'].append(audit.certificate_check(g,x,y,tree,30))
    result['status']='PASS_REPAIRED_GROUND_CACHE_AND_POSITIVITY_VALIDATION'
    result['valid_case_count']=len(result['valid_cases'])
    (BASE/'repair_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='valid_cases'},indent=2))

if __name__=='__main__': main()
