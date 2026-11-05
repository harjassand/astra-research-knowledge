"""Reproduce selected granular-memory groups with the authors' v1.1 algorithm.
The file is a secondary analysis, not a new constitutive model.
Run with the scientific Python runtime; input CSVs are immutable.
"""
from pathlib import Path
import json, io, contextlib, csv, hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import t as student_t
ROOT=Path(__file__).resolve().parent
src=(ROOT/'trackParticlesAndStrains.py').read_text().split('# UNCOMMENT ONE LINE')[0]
ns={}
exec(compile(src, 'author_analysis_prefix', 'exec'),ns)
f=ns['findTrajectories']
manifest=json.loads((ROOT/'source_manifest.json').read_text())
results={}; failures=[]
for group,ids in manifest['groups'].items():
    rows=[]
    for name in ids:
        p=ROOT/'raw'/(name+'-readout')
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                strobes, displacement=f(str(p),particles=True)
                allstrains,_=f(str(p),particles=False)
                tp=ROOT/'raw'/name
                if tp.is_dir():
                    trainstrains,_=f(str(tp),particles=False)
                else: trainstrains=None
            delta_strain=allstrains[:2]-allstrains[:2,0,None]
            magnitude=np.linalg.norm(delta_strain,axis=0)
            frames_per_cycle=(len(magnitude)-1)//5
            peaks=None if allstrains.shape[1]==6 else [float(np.max(magnitude[k*frames_per_cycle:(k+1)*frames_per_cycle+1])) for k in range(5)]
            trained_peak=None if trainstrains is None or trainstrains.shape[1]==6 else float(np.max(np.linalg.norm(trainstrains[:2]-trainstrains[:2,0,None],axis=0)))
            d=np.asarray(displacement)
            cusp=float((d[2]+d[4])/2-d[3]) if len(d)==6 else None
            rows.append({'name':name,'displacement':d.tolist(),'strobes':strobes.tolist(),
                         'readout_peaks':peaks,'training_peak':trained_peak,
                         'full_boundary_frame_count':allstrains.shape[1],
                         'cusp_at_readout3':cusp,
                         'boundary_residual_norm':np.linalg.norm(strobes[:2]-strobes[:2,0,None],axis=0).tolist()})
        except Exception as exc:
            failures.append({'group':group,'name':name,'error':str(exc)})
    ds=np.array([r['displacement'] for r in rows]); cs=np.array([r['cusp_at_readout3'] for r in rows])
    if len(rows):
        sem=ds.std(axis=0,ddof=1)/len(rows)**.5
        csem=cs.std(ddof=1)/len(rows)**.5
        q=student_t.ppf(.975,len(rows)-1)
        results[group]={'n':len(rows),'mean_displacement':ds.mean(axis=0).tolist(),
          'sem_displacement':sem.tolist(),'cusp_mean':float(cs.mean()),'cusp_sem':float(csem),
          'cusp_95_t_interval':[float(cs.mean()-q*csem),float(cs.mean()+q*csem)],
          'raw':rows}
# Content hashes for downloaded data: Git blob identity matches source-tree manifests or not.
verification=[]
for entry in manifest['entries']:
    p=ROOT/'raw'/entry['path']
    if p.exists():
        b=p.read_bytes(); actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        verification.append({'path':entry['path'],'match':actual==entry['sha'],'git_sha':actual,'sha256':hashlib.sha256(b).hexdigest()})
output={'description':'Exact author algorithm from public v1.1 data; units are fraction of box size. Cusp contrast is mean(D2,D4)-D3. Intervals are descriptive across 5 or 7 preparations, not a fully randomized causal study.',
        'results':results,'failures':failures,'verified_files':len(verification),'hash_mismatches':[v for v in verification if not v['match']],
        'file_hashes':verification}
(ROOT/'reproduction_results.json').write_text(json.dumps(output,indent=2))
with (ROOT/'reproduction_summary.csv').open('w') as ff:
    writer=csv.writer(ff); writer.writerow(['group','n','D1','D2','D3','D4','D5','cusp','cusp_95_low','cusp_95_high'])
    for g,v in results.items(): writer.writerow([g,v['n'],*v['mean_displacement'][1:],v['cusp_mean'],*v['cusp_95_t_interval']])
labels={'control':'No training; SB readout','sb_small':'SB training; SB readout','sa_to_sb':'SA training; SB readout','alternating':'Alternating training; mixed readout','mixed':'Mixed training; mixed readout'}
fig,axs=plt.subplots(1,2,figsize=(11,4.3))
for g in ['control','sb_small','sa_to_sb']:
    v=results[g]; axs[0].errorbar(range(6),v['mean_displacement'],yerr=v['sem_displacement'],marker='o',capsize=2,label=labels[g])
for g in ['alternating','mixed']:
    v=results[g]; axs[1].errorbar(range(6),v['mean_displacement'],yerr=v['sem_displacement'],marker='o',capsize=2,label=labels[g])
for ax in axs:
    ax.set_xlabel('Readout cycle (increasing strain amplitude)');ax.set_ylabel('Mean nonaffine displacement / box size');ax.grid(alpha=.2);ax.legend(fontsize=8)
axs[0].set_title('Strong direction dependence at equal drive amplitude')
axs[1].set_title('Two-axis protocols (training amplitudes differ)')
fig.suptitle('Reproduction of public granular-memory data (error bars: SEM)',fontsize=13)
fig.tight_layout();fig.savefig(ROOT/'granular_reproduction.png',dpi=180)
print(json.dumps({'summary':{g:{k:v[k] for k in ['n','mean_displacement','cusp_mean','cusp_95_t_interval']} for g,v in results.items()},'failures':failures,'verified_files':len(verification),'hash_mismatches':len(output['hash_mismatches'])},indent=2))
