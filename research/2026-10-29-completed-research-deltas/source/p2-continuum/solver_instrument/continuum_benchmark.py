#!/usr/bin/env python3
import json,time
from coherent_packet_benchmark import run,OUT

if __name__=='__main__':
    s={'times':[0.,.65],'areas':[1.5,1.2],'eta_source':.8,'omega_source':1.,
       'continuum':{'phase_mass':.75**2,'omega_min':.8,'scale':.4,
          'density':'rho(omega)=v*(omega-omega_min)*exp(-(omega-omega_min)/scale)/scale^2 for omega>=omega_min'}}
    t=time.time();r=run(s,order=8,tol=1e-9,prefix='continuum',cutoffs=(12,18,24,32,44))
    r['runtime_seconds']=time.time()-t
    r['exact_temporal_span']='Two bath vectors f_0,f_0.65; continuum span reduction exact for these kicks only.'
    (OUT/'continuum_benchmark_receipt.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
