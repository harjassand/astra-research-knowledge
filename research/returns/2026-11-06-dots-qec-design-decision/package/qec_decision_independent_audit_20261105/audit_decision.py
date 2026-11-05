from fractions import Fraction as F
from pathlib import Path
from collections import Counter
from math import comb, ceil
import json, time, hashlib
import stim
P=Path(__file__).resolve().parent;R=P.parent
started=time.perf_counter()
rows=[]
for d in [19,21,23]:
 c=stim.Circuit.generated('surface_code:rotated_memory_z',distance=d,rounds=d,after_clifford_depolarization=.001,before_round_data_depolarization=.001,before_measure_flip_probability=.001,after_reset_flip_probability=.001).flattened()
 counts=Counter();noise=Counter();measurements=0
 for ins in c:
  targets=ins.targets_copy();name=ins.name
  if name in ['DEPOLARIZE2','CX']:num=len(targets)//2
  else:num=len(targets)
  if name in ['DEPOLARIZE1','DEPOLARIZE2','X_ERROR','Z_ERROR']:noise[name]+=num
  if name in ['H','CX','R','MR','M']:counts[name]+=num
 coords=c.get_detector_coordinates();selected=[i for i,v in coords.items() if int(v[0]+v[1])%4==0]
 # Noise sites have identical non-identity-event probability exactly 1/1000.
 # This is an original categorical circuit-site count, not a DEM edge count.
 rows.append({'distance':d,'rounds':d,'used_physical_qubits':len(c.get_final_qubit_coordinates()),'data_qubits':d*d,'ancillas':len(c.get_final_qubit_coordinates())-d*d,'qubit_round_volume_excluding_init_readout_ticks':len(c.get_final_qubit_coordinates())*d,'detectors':c.num_detectors,'selected_detectors':len(selected),'measurements':c.num_measurements,'operations':dict(counts),'noise_sites':dict(noise),'total_noise_sites':sum(noise.values()),'expected_fault_sites_exact':str(F(sum(noise.values()),1000)),'exact_p_vs_binary64_site_coupling_upper_exact':str(sum(noise.values())*abs(F(.001)-F(1,1000))),'flattened_circuit_sha256':hashlib.sha256((str(c)+'\n').encode()).hexdigest()})
r=json.loads((R/'qec_fault_tuple_20261105/production_d21_10000.json').read_text());m=json.loads((R/'qec_fault_tuple_20261105/d21/parameters.json').read_text())
z=F(r['normalizer_exact']);tv=F(m['conversion_TV_upper_exact']);n=r['shots'];x=r['counts']['accepted'];D=1<<24
# Compute exact binomial tail inequalities independently from prior confidence code.
def cdf_num(k,j):
 t=comb(n,k)*j**k*(D-j)**(n-k);s=t
 for ell in range(k,0,-1):
  t,rem=divmod(t*ell*(D-j),(n-ell+1)*j);assert not rem;s+=t
 return s
# Approximate proposals need not be trusted: exact inequalities certify.
from scipy.stats import beta
alpha=F(1,3000);target=F(1,10**12);den=D**n
jl=int(float(beta.ppf(float(alpha/2),x,n-x+1))*D)
ju=ceil(float(beta.ppf(float(1-alpha/2),x+1,n-x))*D)
assert (den-cdf_num(x-1,jl))*6000 <= den
assert cdf_num(x,ju)*6000 <= den
assert (den-cdf_num(x-1,jl+1))*6000 > den
assert cdf_num(x,ju-1)*6000 > den
L=max(F(0),z*F(jl,D)-tv);U=min(F(1),z*F(ju,D)+tv)
assert L>target
# Direct one-sided threshold test bound with dyadic domination and geometric tail.
# Under exact circuit failure <= threshold, rounded law acceptance <= (threshold+tv)/Z.
q0=(target+tv)/z;Q=1<<30;q=F(ceil(q0*Q),Q);ratio=F(n-x,x+1)*q/(1-q)
assert ratio<1
term=F(comb(n,x))*q**x*(1-q)**(n-x)
tail_upper=term/(1-ratio)
assert tail_upper<F(1,10**10)
out={'audit_scope':'Independent circuit operation counts; exact widened fixed-n interval for historic d21 data. Does not remedy unknown data selection or prove decoder optimum for every syndrome.','stim_version':stim.__version__,'circuits':rows,'historic_d21':{'n':n,'x':x,'alpha_exact':str(alpha),'allocation_interpretation':'Three predesignated fixed-sample intervals at alpha=1/3000 have familywise error <=1/1000 by union bound. Extra looks or data-selected runs require further error accounting.','acceptance_grid_numerators':[jl,ju],'acceptance_grid_denominator':D,'interval_exact':[str(L),str(U)],'interval_float':[float(L),float(U)],'lower_above_target':True,'conversion_TV':float(tv),'one_sided_threshold_tail_bound_decimal_approximation':format(float(tail_upper),'.12g'),'tail_upper_lt_1e_minus_10_verified_exactly':True,'source_sha256':hashlib.sha256((R/'qec_fault_tuple_20261105/production_d21_10000.json').read_bytes()).hexdigest()},'audit_seconds':time.perf_counter()-started}
(P/'audit_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
