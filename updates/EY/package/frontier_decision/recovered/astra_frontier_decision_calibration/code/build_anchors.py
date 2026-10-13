"""Construct all global-design anchor packets without importing prior response data.
The two large anchors reuse the dictionary acquired by the fresh central run; its
acquisition cost is charged to that run. Other anchors enumerate span-eight words.
"""
import time,sys,json,gc,resource
from pathlib import Path
start=time.perf_counter()
import numpy as np
from fast_algebra import basis
from jet_solver import JetSolver
from jet_certificate import round_file
root=Path(sys.argv[1]);root.mkdir(parents=True,exist_ok=True)
main=np.load(Path(sys.argv[2]))
largef=[tuple(map(int,w)) for w in main['fw']];largeg=[tuple(map(int,w)) for w in main['gw']]
records=[]
for name,V,large in [('V0',0.,False),('Vhalf',.5,False),('V1',1.,False),('V1half',1.5,False),('V3',3.,False),('V2',2.,True),('V2half',2.5,True)]:
 t=time.perf_counter();fw,gw=(largef,largeg) if large else (basis(8,1),basis(8,0))
 solver=JetSolver(fw,gw,V=V);solver.solve(0,output=root/(name+'_discovery'))
 rec=round_file(root/(name+'_discovery.npz'),36,root/(name+'.npz'))
 records.append(dict(name=name,parameter=rec['parameters']['V'],large=large,seconds=time.perf_counter()-t,width=rec['D_width_float'],interval=rec['D_interval_float'],sha256=rec['witness_sha256']))
 del solver;gc.collect()
report=dict(seconds=time.perf_counter()-start,peak_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,records=records,notes='All anchor response coefficients newly solved. Two dictionaries reuse the fully charged fresh central dictionary; no prior response packet. Total includes imports, assembly, all solves, dyadic rounding and exact checks, not central dictionary acquisition.')
(root/'benchmark.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2),flush=True)
