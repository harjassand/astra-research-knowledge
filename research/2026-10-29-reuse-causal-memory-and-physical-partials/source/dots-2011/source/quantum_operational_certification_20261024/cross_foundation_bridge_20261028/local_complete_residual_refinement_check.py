import runpy,json,tempfile,shutil
from hashlib import sha256
from pathlib import Path
from itertools import product
HERE=Path(__file__).resolve().parent
BASE='COMPLETE_PORT_PHYSICAL_RESIDUAL_SIMULATOR.md'
CHECK='complete_port_physical_residual_check.py'
assert sha256((HERE/BASE).read_bytes()).hexdigest()=='d2564c18b184b92fdd471e9d73720c693389c7f2f07f82432885663189da7a92'
assert sha256((HERE/CHECK).read_bytes()).hexdigest()=='db9b7c2e9500f2ffce3952078253d9e833917e01c637da00170576f8cd64dd5f'
with tempfile.TemporaryDirectory(prefix='complete_local_residual_') as tmp:
  for name in [BASE,CHECK]:shutil.copyfile(HERE/name,Path(tmp)/name)
  v=runpy.run_path(str(Path(tmp)/CHECK))
s=v['s'];coords=v['coords'];Din=v['Din'];Bout=v['Bout'];M=v['M'];DH=v['DH'];w=v['w'];ports=v['true_ports'];en=v['entry_norm'];clean=v['clean'];K=v['Kcore']
bounds={};statbounds={};rawbounds={}
for a,Ks in ports.items():
  estimates=[];stats=[]
  for j in range(4):
    total=0;stat=0
    for i,o in product(range(4),range(len(Ks))):
      J=clean(sum(((coords[('true',a,u,o,b)][i,j]-coords[('fit',a,u,o,b)][i,j])*s.kronecker_product(Din[u].T,Bout[b]) for u,b in product(range(6),repeat=2)),s.zeros(4)))
      assert J==J.conjugate().T
      total+=en(J)
    for u,o,b in product(range(6),range(len(Ks)),range(6)):
      E=M*(s.ones(4)*w+DH*v['absM'](coords[('true',a,u,o,b)]))
      stat+=sum(2*E[i,j] for i in range(4))
    estimates.append(total+stat);stats.append(stat)
  bounds[a]=max(estimates);statbounds[a]=max(stats)
gnew=max(bounds.values());gtri=v['g'];etanew=K*(3*gnew+v['delta_m'])/2
assert gnew<gtri and etanew<v['eta']
out={'source_sha256':sha256((HERE/'LOCAL_COMPLETE_RESIDUAL_CHOICERTIFICATE.md').read_bytes()).hexdigest(),
 'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
 'frozen_base_source_sha256':sha256((HERE/BASE).read_bytes()).hexdigest(),
 'frozen_base_check_sha256':sha256((HERE/CHECK).read_bytes()).hexdigest(),
 'status':'PASS new complete-Choi cancellation bound on frozen author fixture; NOT independent receiving',
 'complete_Choi_bound_method':'entrywise real+imag nuclear-norm upper; no SDP or eigenvalue optimizer',
 'complete_residual_plus_uncertainty_exact':str(gnew),'complete_residual_plus_uncertainty_decimal':str(s.N(gnew,18)),
 'old_dual_triangle_epsilon_decimal':str(s.N(gtri,18)),
 'epsilon_improvement_factor':str(s.N(gtri/gnew,18)),
 'horizon3_eta_new_decimal':str(s.N(etanew,18)),'horizon3_eta_old_decimal':str(s.N(v['eta'],18)),
 'local_complete_statistics_upper_decimal':str(s.N(max(statbounds.values()),18)),
 'source_calls':0,'RNG_calls':0,'hardware':0,'SDP_executed':False}
(HERE/'local_complete_residual_refinement_check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
