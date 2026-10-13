"""Fresh finite basis acquisition, physical response jets, exact verification.
No prior response packet or trained inverse is input. This is an instance benchmark,
not a uniform termination theorem. The enrichment rule is fixed and deterministic.
"""
import time, json, resource, sys
from pathlib import Path
start=time.perf_counter()
from adaptive_jets import run
from jet_certificate import round_file
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
log=run(2.166015625,str(out/'discovery'),steps=10,cap=5000,L=8,order=3,maxspan=18)
rec=round_file(out/'discovery/step10.npz',36,out/'witness.npz')
bench=dict(total_seconds=time.perf_counter()-start,peak_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,initial_basis='all allowed translation words through span 8',prior_response_packets_used=False,steps=10,addition_cap_per_parity=5000,maximum_input_span=18,jet_order=3,final_f_basis=rec['f_basis'],final_g_basis=rec['g_basis'],commutator_nnz=rec['commutator_nnz'],certificate_width_D=rec['D_width_float'],jet_intervals=rec['D_jet_intervals_float'],physical_parameters=rec['parameters'],python=sys.version,notes='Single BLAS thread; imported installed compiler may use existing caches. Total includes imports, dictionary acquisition, all solves, rounding and exact verification; excludes development, proof, literature, global anchor acquisition.')
(out/'benchmark.json').write_text(json.dumps(bench,indent=2));print(json.dumps(bench,indent=2),flush=True)
