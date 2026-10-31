"""Same-raw-list comparisons against preserved earlier sufficient finders."""
from pathlib import Path
import importlib.util,sys,json,hashlib
import adaptive_mass as new
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def main():
    sp,raw=new.demo_network();out={}
    sys.path.insert(0,str(ROOT/'stochastic_boundary_construction_20261031'))
    old=load('old_compiler',ROOT/'stochastic_boundary_construction_20261031/compile_recurrence.py')
    out['initial_unified_compiler']=old.compile_raw(sp,raw)
    for name,file in [('protected_family','stochastic_protected_boundary_20261031/protected_boundary.py'),('partial_row_coverage','stochastic_coverage_pending_20261031/coverage_boundary.py')]:
        path=ROOT/file;m=load(name,path);out[name]={'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'raw_recognition':m.recognize(sp,raw)}
    assert not out['initial_unified_compiler']['accepted']
    assert all(not out[name]['raw_recognition']['accepted'] for name in ['protected_family','partial_row_coverage'])
    print(json.dumps(out,default=new.encode,indent=2,sort_keys=True))
if __name__=='__main__':main()
