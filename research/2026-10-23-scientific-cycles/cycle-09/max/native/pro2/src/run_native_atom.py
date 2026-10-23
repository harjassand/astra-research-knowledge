"""New native graph receiving use; no supplied recursive expression oracle."""
from pathlib import Path
import json,time,resource
from atom_normal_form import prepare_atom,color_native_atom
from run_receiving import receiving

ROOT=Path(__file__).resolve().parents[1]

def main():
    start=time.perf_counter();cpu=time.process_time()
    source=json.loads((ROOT/'inputs/native_atom_9.json').read_text())
    stages={}
    def graph():
        t=time.perf_counter();form=prepare_atom(source['n'],source['edges'])
        stages['native_support_normalization']=time.perf_counter()-t
        t=time.perf_counter();g=color_native_atom(form)
        stages['certificate_color_on_original_vertices']=time.perf_counter()-t
        g['original_native_input']=source
        return g
    result=receiving('native_atom_9_four_action',graph,4)
    # Distinct branch checks: the cycle normalization and C3 identity exception.
    t=time.perf_counter()
    cycle=color_native_atom(prepare_atom(5,[(0,1),(1,2),(2,3),(3,4),(4,0)]))
    triangle=color_native_atom(prepare_atom(3,[(0,1),(1,2),(2,0)]))
    branch_checks=dict(cycle=cycle,triangle=triangle)
    stages['cycle_and_triangle_branch_checks']=time.perf_counter()-t
    (ROOT/'results/native_atom_branch_checks.json').write_text(json.dumps(branch_checks,indent=2)+'\n')
    result['native_preparation_substages']=stages
    result['total_including_branch_checks_wall_seconds']=time.perf_counter()-start
    result['total_including_branch_checks_cpu_seconds']=time.process_time()-cpu
    result['peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024
    result['scope']='one new native-support original-action receiving use plus cycle/C3 code-branch checks; no graph-size sweep'
    (ROOT/'results/NATIVE_ATOM_COSTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
