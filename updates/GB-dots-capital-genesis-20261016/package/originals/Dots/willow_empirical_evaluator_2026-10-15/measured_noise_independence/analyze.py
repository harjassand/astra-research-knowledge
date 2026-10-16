import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import re,json,hashlib,time,resource,csv
from pathlib import Path
import numpy as np
from scipy.stats import hypergeom, fisher_exact
resource.setrlimit(resource.RLIMIT_CPU,(120,120))
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
start=time.process_time()
OUT=Path(__file__).parent
BASE=(Path(__file__).resolve().parent.parent / 'measured_syndrome_acquisition/data/google_105Q_surface_code_d3_d5_d7/d5_at_q8_7/X/r50')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def parse_dem(path):
    coords={}; support=[set() for _ in range(1200)]; mechanisms=[]; separators=0; cancels=0
    for lineno,line in enumerate(path.read_text().splitlines(),1):
        s=line.split('#')[0].strip()
        if not s:continue
        m=re.fullmatch(r'error\(([^)]+)\) (.*)',s)
        if m:
            p=float(m[1]); assert 0<=p<=1
            active=set(); targets=m[2].split(); separators+= '^' in targets
            for t in targets:
                if t=='^' or re.fullmatch(r'L\d+',t):continue
                assert re.fullmatch(r'D\d+',t),(lineno,t)
                d=int(t[1:]); assert 0<=d<1200
                if d in active: active.remove(d); cancels+=1
                else:active.add(d)
            ident=len(mechanisms)
            mechanisms.append({'id':ident,'source_line':lineno,'p':p,'detectors':sorted(active)})
            for d in active:support[d].add(ident)
            continue
        m=re.fullmatch(r'detector\(([^)]+)\) D(\d+)',s)
        if m:
            d=int(m[2]); assert d not in coords
            coords[d]=tuple(float(x) for x in m[1].split(','));continue
        if re.fullmatch(r'logical_observable L\d+',s):continue
        raise ValueError(('Unsupported DEM instruction',lineno,s))
    assert len(coords)==1200
    return coords,support,{'error_lines':len(mechanisms),'lines_with_correlated_components':separators,'parity_cancellations':cancels,'sha256':sha(path)},mechanisms
models={}
for name in ['rl_optimized','si1000']:
    path=BASE/f'decoding_results/correlated_matching_decoder_with_{name}_prior/error_model.dem'
    models[name]=parse_dem(path)
coords=models['rl_optimized'][0]
assert coords==models['si1000'][0]
circuit=BASE/'circuit_ideal.stim'
circuitcoords=[]
for s in circuit.read_text().splitlines():
    assert not re.match(r'\s*(REPEAT|SHIFT)',s)
    m=re.match(r'DETECTOR\(([^)]+)\)',s)
    if m:circuitcoords.append(tuple(float(x) for x in m[1].split(',')))
assert circuitcoords==[coords[d] for d in range(1200)]
lookup={v[:3]:d for d,v in coords.items()};assert len(lookup)==1200
pairs=[];excluded=[]
for d,c in sorted(coords.items()):
    x,y,t=c[:3]
    if not 1<=t<=49:continue
    for lag in range(2,11):
        if t+lag>49:continue
        e=lookup[(x,y,t+lag)]
        overlaps={name:len(m[1][d]&m[1][e]) for name,m in models.items()}
        rec={'d1':d,'d2':e,'x':x,'y':y,'t1':t,'t2':t+lag,'lag':lag,**{name+'_overlap':v for name,v in overlaps.items()}}
        (excluded if any(overlaps.values()) else pairs).append(rec)
assert len(pairs)+len(excluded)==9288
family={'pairs':pairs,'excluded':excluded,'models':{n:m[2] for n,m in models.items()},'circuit_sha256':sha(circuit),'protocol_sha256':sha(OUT/'PROTOCOL.md')}
(OUT/'frozen_family.json').write_text(json.dumps(family,indent=2))
print('FROZEN FAMILY',len(pairs),'excluded',len(excluded),'sha',sha(OUT/'frozen_family.json'),flush=True)
if '--structure-only' in __import__('sys').argv:raise SystemExit
# No measured values accessed above this point.
idxpath=(Path(__file__).resolve().parent.parent / 'measured_syndrome_audit/diagnostic_indices.txt')
assert sha(idxpath)=='80d49493e16e51d3f2cfe8574ec3316ded74e0a51ae49865165e9def979ee2ae'
indices=list(map(int,idxpath.read_text().split())); assert len(set(indices))==len(indices)==25000
expected=sorted(range(50000),key=lambda i:hashlib.sha256(('astra-willow-split-v1:'+str(i)).encode()).digest())[:25000]
assert indices==expected
buf=bytearray()
with (BASE/'detection_events.b8').open('rb') as f:
    for i in indices:
        f.seek(i*150); row=f.read(150);assert len(row)==150;buf.extend(row)
bits=np.unpackbits(np.frombuffer(buf,dtype=np.uint8).reshape(25000,150),axis=1,bitorder='little')
# Pack each detector's 25,000 values into one Python int for exact joint counts.
packed=np.packbits(bits.T,axis=1,bitorder='little')
columns=[int.from_bytes(row.tobytes(),'little') for row in packed]
margins=[c.bit_count() for c in columns];del bits,packed,buf
N=25000;M=len(pairs);results=[]
for rec in pairs:
    a=rec['d1'];b=rec['d2']; ma=margins[a]; mb=margins[b]
    n11=(columns[a]&columns[b]).bit_count(); n10=ma-n11;n01=mb-n11;n00=N-ma-mb+n11
    p=float(hypergeom.sf(n11-1,N,ma,mb)) if 0<ma<N and 0<mb<N else 1.
    odds=n11*n00/(n10*n01) if n10*n01 else None
    covariance=n11/N-ma*mb/N**2
    phi=covariance/((ma/N)*(1-ma/N)*(mb/N)*(1-mb/N))**.5 if 0<ma<N and 0<mb<N else None
    results.append({**rec,'N':N,'n11':n11,'n10':n10,'n01':n01,'n00':n00,'marginal1':ma,'marginal2':mb,'joint_probability':n11/N,'independent_expected_n11':ma*mb/N,'excess_joint_probability':covariance,'odds_ratio':odds,'phi':phi,'p_one_sided':p,'p_bonferroni':min(1.,M*p)})
results.sort(key=lambda r:(r['p_one_sided'],r['d1'],r['d2']))
with (OUT/'pair_results.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
r=results[0];fp=float(fisher_exact([[r['n11'],r['n10']],[r['n01'],r['n00']]],alternative='greater').pvalue)
assert abs(fp-r['p_one_sided'])<=max(1e-300,abs(fp)*1e-10)
summary={'N':N,'tests':M,'excluded_pairs':len(excluded),'alpha_family':.01,'unadjusted_threshold':.01/M,'rejected_pairs':sum(r['p_bonferroni']<=.01 for r in results),'top10':results[:10],'by_lag':{lag:{'tests':sum(r['lag']==lag for r in results),'rejections':sum(r['lag']==lag and r['p_bonferroni']<=.01 for r in results),'min_adjusted_p':min(r['p_bonferroni'] for r in results if r['lag']==lag)} for lag in range(2,11)},'fisher_exact_crosscheck':fp,'family_sha256':sha(OUT/'frozen_family.json'),'indices_sha256':sha(idxpath),'cpu_seconds':time.process_time()-start,'max_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'reserved_rows_read':0}
(OUT/'results_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
