#!/usr/bin/env python3
"""Freeze the new rational branch/lift fixtures once; charge body and cases."""
import hashlib,importlib.util,json,resource,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from exact_ops import serial,graph_size
from core_cancel import build as core_build
from cone_lift import build as cone_build
from low_projection import build as low_build


def main():
    wall=time.perf_counter(); cpu=time.process_time()
    old=ROOT/'inherited'/'separator_witness.py'
    spec=importlib.util.spec_from_file_location('inherited_exact_tents',old)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    folder=ROOT/'witnesses'; folder.mkdir(exist_ok=True)
    jobs=[('core_t2_narrow',lambda:core_build(2,4,12)),
          ('core_t2_large',lambda:core_build(2,64,24)),
          ('core_t3',lambda:core_build(3,16,5)),
          ('cone_three_copies',lambda:cone_build(module.build)),
          ('low_projection_actual_input',lambda:low_build(module.build))]
    rec=[]
    for name,fn in jobs:
        target=folder/(name+'.json')
        if target.exists():raise FileExistsError(target)
        w0=time.perf_counter(); c0=time.process_time(); obj=serial(fn())
        inp={k:obj[k] for k in ('n','q','edges','X')}
        obj['input_sha256']=hashlib.sha256(json.dumps(inp,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        raw=(json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode()
        target.write_bytes(raw)
        item={'name':name,'n':obj['n'],'q':obj['q'],'bytes':len(raw),
          'sha256':hashlib.sha256(raw).hexdigest(),'input_sha256':obj['input_sha256'],
          'action_squared':obj['action_squared'],'operator_lower_squared':obj['operator_lower_squared'],
          'ratio_lower_squared':obj['ratio_lower_squared'],
          'constraint_rank':obj.get('constraint_rank'),
          'wall_seconds':time.perf_counter()-w0,'cpu_seconds':time.process_time()-c0}
        rec.append(item);print(json.dumps(item),flush=True)
    counts=[]
    for t in range(5):
        for R in (1,2):
            counts.append({'t':t,'R':R,'vertices':graph_size(t,R)})
    report={'schema':'astra.cycle3_producer.v1','fixtures':rec,'symbolic_sizes':counts,
      'wall_seconds':time.perf_counter()-wall,'cpu_seconds':time.process_time()-cpu,
      'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
      'inherited_source_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),
      'scope':'One producer run; rational fixture construction/serialization included. Symbolic graph sizes only; huge universal examples not materialized.'}
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results'/'producer.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('fixtures','symbolic_sizes')}),flush=True)

if __name__=='__main__':main()
