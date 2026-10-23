"""Small process-isolated same-batch throughput measurement, not a BVP benchmark."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import sys, time, json, resource, subprocess, hashlib, platform
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent.parent/'nitrogen_quench_recovery_20261021'


def worker(method,n):
    t0=time.perf_counter()
    import numpy as np
    sys.path[:0]=[str(SOURCE/'deps'),str(SOURCE)]
    if method.startswith('native'):
        from paper_model import gas_model
    else:
        from kernel import Kernel
    import_s=time.perf_counter()-t0
    t0=time.perf_counter()
    obj=gas_model() if method.startswith('native') else Kernel()
    setup_s=time.perf_counter()-t0
    with np.load(ROOT/'benchmark_batch.npz') as d:
        T,Y,h=d['T'][:n],d['Y'][:,:n],d['h'][:n]
    def execute():
        if method=='vector_TPY':return obj.evaluate(T,Y)
        if method=='vector_HPY':return obj.evaluate_hpy(h,Y)
        out={'mass_production':np.empty((6,n)),'h_species':np.empty((6,n)),
             **{key:np.empty(n) for key in ['rho','cp','enthalpy','viscosity','conductivity','T']}}
        for i in range(n):
            if method=='native_TPY':obj.TPY=T[i],101325.,Y[:,i]
            else:obj.HPY=h[i],101325.,Y[:,i]
            out['mass_production'][:,i]=obj.net_production_rates*obj.molecular_weights
            out['h_species'][:,i]=obj.partial_molar_enthalpies/obj.molecular_weights
            out['rho'][i]=obj.density;out['cp'][i]=obj.cp_mass;out['enthalpy'][i]=obj.enthalpy_mass
            out['viscosity'][i]=obj.viscosity;out['conductivity'][i]=obj.thermal_conductivity;out['T'][i]=obj.T
        return out
    t0=time.perf_counter();out=execute();warmup_s=time.perf_counter()-t0
    samples=[]
    for _ in range(7):
        t0=time.perf_counter();out=execute();samples.append(time.perf_counter()-t0)
    print(json.dumps({'method':method,'batch_size':n,'import_wall_s':import_s,
                      'construction_wall_s':setup_s,'warmup_wall_s':warmup_s,
                      'repeat_wall_s':samples,'median_wall_s':float(np.median(samples)),
                      'max_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      'checksum_T':float(out['T'].sum()),'checksum_rho':float(out['rho'].sum()),
                      'one_blas_thread':True,'kernel_sha256':hashlib.sha256((ROOT/'kernel.py').read_bytes()).hexdigest(),'python_version':platform.python_version()}))


def main():
    import numpy as np
    with np.load(ROOT/'validation_cases.npz') as d:
        ix=np.arange(4096)%len(d['T']);T=d['T'][ix];Y=d['Y'][:,ix]
        y=np.maximum(Y,0);y/=y.sum(axis=0);h=(y*d['native_h_species'][:,ix]).sum(axis=0)
    # Avoid the physically tiny nonunique NASA splice for throughput comparison;
    # splice/cancellation behavior is instead reported in dedicated validation.
    from kernel import Kernel
    close=abs(T-1000)<.01
    T=T.copy();T[close]=1001.
    h[close]=Kernel().evaluate(T[close],Y[:,close])['enthalpy']
    np.savez_compressed(ROOT/'benchmark_batch.npz',T=T,Y=Y,h=h)
    rows=[]
    for n in [1024,4096]:
        for method in ['native_TPY','vector_TPY','native_HPY','vector_HPY']:
            result=subprocess.run([sys.executable,__file__,'--worker',method,str(n)],check=True,text=True,capture_output=True)
            row=json.loads(result.stdout);rows.append(row);print(json.dumps(row),flush=True)
    ratios=[]
    for n in [1024,4096]:
        for state in ['TPY','HPY']:
            a=next(r for r in rows if r['batch_size']==n and r['method']=='native_'+state)
            b=next(r for r in rows if r['batch_size']==n and r['method']=='vector_'+state)
            ratios.append({'states':n,'mode':state,'native_over_vector_median':a['median_wall_s']/b['median_wall_s']})
    report={'rows':rows,'median_ratios':ratios,'kernel_sha256':hashlib.sha256((ROOT/'kernel.py').read_bytes()).hexdigest(),'batch_sha256':hashlib.sha256((ROOT/'benchmark_batch.npz').read_bytes()).hexdigest(),'measurement_environment':'Shared execution environment, no CPU pinning or exclusive-host control; other activity can affect wall time.','scope':'Single-thread bounded synthetic batch drawn from validation states; same T,Y/h inputs and same requested property outputs, separate fresh processes, one warmup and seven repeats. HPY native uses prior loop state as initial guess; vector uses its branch-safe default. No BVP/end-to-end speedup or hardware-general performance claim. RSS includes imported runtime and all timed runs; construction excludes imports and benchmark data loading; cache build separate in manifest.'}
    (ROOT/'benchmark.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(ratios,indent=2))

if __name__=='__main__':
    if len(sys.argv)>1:worker(sys.argv[2],int(sys.argv[3]))
    else:main()
