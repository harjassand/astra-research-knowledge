#!/usr/bin/env python3
"""Read-only saved-data verification. No trajectories, compilation or network."""
import sys
sys.dont_write_bytecode = True
import hashlib, json, math
from pathlib import Path
ROOT = Path(__file__).resolve().parent
B = ROOT / 'benchmark'
sys.path.insert(0, str(B))
from independent_audit import bd, hom, decode_id, ORI
assert __debug__, 'Run without -O: assertions are required'
def read(name): return json.loads((B/name).read_text())
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
for v in read('ORIGINAL_VERSION_MANIFEST.json')['versions']:
    assert sha(B/v['source']) == v['source_sha256']
historical = {}; omitted = {'simulator','simulator_equalreads','simulator_readouts'}
for name in ('SHA256SUMS','PHASE3_SHA256SUMS','PHASE4_SHA256SUMS','PHASE4_ENDPOINT_SHA256SUMS'):
    checked=[]; absent=[]
    for line in (B/name).read_text().splitlines():
        if not line.strip(): continue
        digest, fname=line.split()
        if (B/fname).is_file():
            assert sha(B/fname)==digest, fname
            checked.append(fname)
        else:
            assert fname in omitted, fname
            absent.append(fname)
    historical[name]={'verified':checked,'intentionally_omitted_machine_binaries':absent}
def cp(k,n):
    def cdf(p,j): return sum(math.comb(n,i)*p**i*(1-p)**(n-i) for i in range(j+1))
    def solve(j,target):
        lo,hi=0.,1.
        for _ in range(100):
            mid=(lo+hi)/2
            if cdf(mid,j)>target: lo=mid
            else: hi=mid
        return (lo+hi)/2
    return [0. if k==0 else solve(k-1,.975),1. if k==n else solve(k,.025)]
phases={}; rawsets={}
for phase, prefix in ((1,'pilot'),(2,'phase2'),(3,'phase3')):
    raw=[json.loads(s) for s in (B/f'{prefix}_raw.jsonl').read_text().splitlines() if s.strip()]
    rawsets[phase]=raw
    summary=read(f'{prefix}_summary.json'); summary=summary if isinstance(summary,list) else [summary]
    groups=[]
    for s in summary:
        rs=[r for r in raw if (r['alpha'],r['method'])==(s['alpha'],s['method'])]
        n=len(rs);k=sum(r['failure'] for r in rs)
        assert (n,k)==(s['trials'],s['failures'])
        assert [r['logical_bits'] for r in rs]==s['logical_bits']
        assert sum(r['fallback'] for r in rs)==s.get('fallbacks',s.get('fallback'))
        for key in ('unresolved','noise_attempts','correction_attempts','check_reads','successful_corrections','rng_draws','components','eligible_components'):
            if key in s: assert sum(r[key] for r in rs)==s[key],key
        ci=cp(k,n);assert all(abs(x-y)<1e-12 for x,y in zip(ci,s['failure_95pct_CP']))
        if 'mean_syndrome_weight' in s: assert abs(sum(r['syndrome_weight'] for r in rs)/n-s['mean_syndrome_weight'])<1e-10
        for r in rs:
            assert r['kappa']==1 and r['T']==5
            assert r['check_reads']==r['correction_attempts']*(8 if r['method']=='sweep' else 2)
        groups.append({'alpha':s['alpha'],'method':s['method'],'trials':n,'failures':k,'CP95':ci})
    assert sum(g['trials'] for g in groups)==len(raw)
    phases[str(phase)]={'saved_endpoints':len(raw),'groups':groups}
rows=read('phase4_readout_results.json'); scores=[]; endpoints={}
def decode_unique(ids,L,k):
    assert len(set(ids))==len(ids)
    assert all(isinstance(i,int) and 0<=i<(6 if k==2 else 4)*L**4 for i in ids)
    return {decode_id(i,L,k) for i in ids}
for method in ('sweep','toom'):
    d=read(f'phase4_endpoint_{method}.json');L=d['L']
    assert d['format']=='4d-memory-endpoint-v1'
    assert (L,d['alpha'],d['T'],d['seed'])==(32,.001,5,101)
    E=decode_unique(d['E'],L,2);S=decode_unique(d['S'],L,1)
    assert bd(E,L)==S
    endpoints[method]=S
    for policy in ('D0','D1','D2'):
        r=read(f'phase4_recovery_{method}_{policy}.json')
        assert r['format']=='4d-memory-recovery-v1'
        R=decode_unique(r['R'],L,2);assert bd(R,L)==S
        C=E^R;assert not bd(C,L)
        h=hom(C);assert all(hom(C,c)==h for c in (1,L-1))
        mask=sum(1<<ORI.index(a) for a in h)
        row=next(v for v in rows if (v['method'],v['policy'])==(method,policy))
        assert (mask,len(R),len(C),int(bool(mask)))==(row['logical_bits'],row['recovery_faces'],row['residual_faces'],row['failure'])
        assert mask==(7 if method=='toom' and policy=='D0' else 0)
        scores.append(row)
# Reconstruct the strict-cutoff component diagnosis from saved syndrome only.
S=endpoints['toom']; unseen=set(S);bad=[];count=0;L=32
while unseen:
    x,a=min(unseen);lift={x:x};queue=[x];component=set();consistent=True
    for x in queue:
        for a in range(4):
            for sign in (-1,1):
                y=list(x);y[a]=(y[a]+sign)%L;y=tuple(y)
                e=(x if sign==1 else y,(a,))
                if e not in S:continue
                component.add(e);unseen.discard(e)
                z=list(lift[x]);z[a]+=sign;z=tuple(z)
                if y not in lift:lift[y]=z;queue.append(y)
                elif lift[y]!=z:consistent=False
    coords=[set(x[a] for x in lift) for a in range(4)]
    diam=[max(min(abs(u-v),L-abs(u-v)) for u in c for v in c) for c in coords]
    spans=[max(x[a] for x in lift.values())-min(x[a] for x in lift.values()) for a in range(4)]
    count+=1
    if not consistent or max(diam)*8>=L:
        bad.append({'edges':len(component),'vertices':len(lift),'consistent':consistent,'wrapped_coordinate_diameters':diam,'lift_box_spans':spans,'D2_eligible':consistent and max(spans)<L})
geometry={'components':count,'strict_ineligible':bad}
assert geometry==read('phase4_ineligible_geometry.json')
replays=[json.loads(s) for s in (B/'phase4_replays.jsonl').read_text().splitlines() if s.strip()]
for r in replays:
    old=next(x for x in rawsets[2 if r['method']=='sweep' else 3] if x['seed']==101 and x['alpha']==.001 and x['method']==r['method'])
    for key,val in old.items():
        if key.endswith('_seconds'):continue
        assert r[key]==val,(key,r[key],val)
print(json.dumps({'status':'PASS','new_trajectories':0,'compiled_binaries':0,'historical_hashes':historical,'source_versions':3,'phases':phases,'endpoint_boundaries':2,'recovery_boundary_and_homology_checks':6,'homology_cuts':[0,1,31],'selected_endpoint_scores':scores,'strict_cutoff_geometry':geometry,'legacy_nontiming_replay_matches':len(replays),'CI_method':'Exact Clopper-Pearson definition, numerical binomial inversion; tolerance 1e-12'},indent=2))
