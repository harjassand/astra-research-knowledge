#!/usr/bin/env python3
"""Real ordinary sampled calibration -> exact rational frame -> standard code -> fresh logical holdout."""
from pathlib import Path
import json,hashlib,itertools,math,sys
import numpy as np
import sympy as s
from scipy.spatial.transform import Rotation
from scipy.stats import binom
import code_and_channels as c
HERE=Path(__file__).parent
CAL_SETTINGS=list(itertools.product([1,2,3],[-1,1],[1,2,3]))
TEST_SETTINGS=list(itertools.product([1,2,3],[-1,1]))

def integer_binomial_cdf_parts(N,k,p):
 # p=a/b; exact lower tail numerator/denominator, no float tail test.
 a=int(s.numer(p));b=int(s.denom(p));base=b-a
 if k<0:return 0,1
 if k>=N:return 1,1
 poly=sum(math.comb(N,j)*a**j*base**(k-j) for j in range(k+1))
 return pow(base,N-k)*poly,pow(b,N)

def exact_tail_check(N,k,p,alpha,lower=True):
 num,den=integer_binomial_cdf_parts(N,k if lower else k-1,p)
 if not lower:num=den-num
 passed=int(s.denom(alpha))*num<=int(s.numer(alpha))*den
 return {'N':N,'failures':k,'null_failure_probability':str(p),'alpha':str(alpha),'tail':'lower' if lower else 'upper','exact_comparison_pass':bool(passed),'tail_float_diagnostic':float(binom.cdf(k,N,float(p)) if lower else binom.sf(k-1,N,float(p))),'integer_numerator_sha256':hashlib.sha256(num.to_bytes((num.bit_length()+7)//8,'big')).hexdigest(),'integer_denominator_sha256':hashlib.sha256(den.to_bytes((den.bit_length()+7)//8,'big')).hexdigest()}

def make_cdf(probs,Q):
 cuts=[]
 for pp in probs:
  assert pp.is_Rational and 0<=pp<=1;cuts.append(int(s.floor(pp*Q)))
 return np.array(cuts,dtype=np.int64)

def draw_binary(N,seed,cuts):
 rng=np.random.default_rng(seed);settings=rng.integers(len(cuts),size=N);u=rng.integers(2**52,size=N,dtype=np.int64);bits=(u<cuts[settings]).astype(np.int64)
 counts=np.bincount(settings*2+bits,minlength=len(cuts)*2).reshape(len(cuts),2);assert counts.sum()==N
 return counts

def frame_from_counts(counts,denom):
 # No generator/source parameters enter this function.
 N=int(counts.sum());Mhat=np.zeros((3,3))
 exactnum=np.zeros((3,3),dtype=np.int64)
 for idx,(j,sg,k) in enumerate(CAL_SETTINGS):exactnum[k-1,j-1]+=9*sg*(int(counts[idx,1])-int(counts[idx,0]))
 Mhat=exactnum.astype(float)/N
 U,sv,Vh=np.linalg.svd(Mhat);O=U@np.diag([1.,1.,np.linalg.det(U@Vh)])@Vh
 q=Rotation.from_matrix(O).as_quat() # x,y,z,w; canonical SO3->SU2 lifting.
 if q[3]<0:q=-q
 t=q[:3]/(1+q[3]);tr=[s.Rational(int(np.rint(v*denom)),denom) for v in t]
 frame=c.stereographic_unitary(tr)
 return frame,{'Bloch_estimate_integer_numerator':exactnum.tolist(),'Bloch_estimate_denominator':N,'floating_singular_values':sv.tolist(),'floating_proper_rotation':O.tolist(),'rational_stereographic_coordinates':list(map(str,tr)),'exact_frame_unitary':[[str(x) for x in row] for row in frame.tolist()]}

def born_calibration_probabilities(M):return [s.cancel((1+M[k,0]+sg*M[k,j])/2) for j,sg,k in CAL_SETTINGS]
def exact_matrix_json(M):return [[str(M[a,b]) for b in range(M.cols)] for a in range(M.rows)]

def main():
 plan=json.loads((HERE/'PREDECLARATION.json').read_text());alpha=s.Rational(plan['one_sided_test_alpha']);Nc=plan['logical_holdout_shots_per_pipeline'];Nu=plan['unencoded_holdout_shots_per_site_per_pipeline'];pc=s.Rational(plan['logical_failure_null_probability']);pu=s.Rational(plan['unencoded_failure_null_probability'])
 assert not (HERE/'raw_counts.npz').exists(), 'Do not repeat or overwrite fresh acquisition'
 # Thresholds and total test budget are checked BEFORE drawing any calibration or holdout.
 threshold_checks=[exact_tail_check(Nc,52,pc,alpha),exact_tail_check(Nc,53,pc,alpha),exact_tail_check(Nu,179,pu,alpha,False),exact_tail_check(Nu,178,pu,alpha,False)]
 assert [x['exact_comparison_pass'] for x in threshold_checks]==[True,False,True,False]
 assert 12*alpha+s.Rational(plan['binary_sampling_record_TV_budget'])<s.Rational(plan['total_failure_budget'])
 (HERE/'threshold_certificates.json').write_text(json.dumps(threshold_checks,indent=2)+'\n')
 # Exact standard-code validations; no acquired measurement involved.
 Enc,Rec=c.exact_encoder_recovery();assert Enc.H*Enc==s.eye(2);assert sum((r.H*r for r in Rec),s.zeros(32))==s.eye(32)
 sources=c.generator_sources();identity=[s.eye(4)]*5;assert c.logical_ptm(identity)==s.eye(4)
 for site in range(5):
  local=identity.copy();local[site]=sources[site]['ideal_residual_PTM'];assert c.logical_ptm(local)==s.eye(4)
 Q=plan['binary_CDF_denominator'];raw={};models={};records=[];cdf_records={};certs=[];total_cal=0;total_log=0;total_un=0
 for ci,N in enumerate(plan['calibration_shots_per_site']):
  learned=[];fitmeta=[]
  for site in range(5):
   cuts=make_cdf(born_calibration_probabilities(sources[site]['PTM']),Q);seed=plan['calibration_seed_base']+100*ci+site;counts=draw_binary(N,seed,cuts)
   key=f'cal_N{N}_site{site}';raw[key]=counts;cdf_records[key]={'seed':seed,'N':N,'cuts':cuts.tolist(),'sampled_bit_one_means':'positive physical Pauli result'};total_cal+=N
   frame,meta=frame_from_counts(counts,plan['rational_frame_stereographic_denominator']);learned.append(frame);fitmeta.append(meta)
  # Candidate selection/physical inverses are now frozen before logical holdout.
  residualKs=[[(frame.H*K).applyfunc(s.cancel) for K in src['Ks']] for frame,src in zip(learned,sources)]
  residual=[c.exact_ptm(ks) for ks in residualKs]
  actual_logical=c.logical_ptm(residual)
  # Actual channel coefficients below belong to the simulator/scorer, not frame fitting or test decision.
  probs=c.holdout_failure_probabilities(actual_logical);cuts=make_cdf(probs,Q);seed=plan['logical_holdout_seed_base']+ci;counts=draw_binary(Nc,seed,cuts);key=f'logical_N{N}';raw[key]=counts;cdf_records[key]={'seed':seed,'N':Nc,'cuts':cuts.tolist(),'sampled_bit_one_means':'logical matched-axis failure'};total_log+=Nc
  failures=int(counts[:,1].sum());test=exact_tail_check(Nc,failures,pc,alpha);certs.append(test)
  row={'calibration_N_per_site':N,'frame_fit_records':fitmeta,'logical_failures':failures,'logical_test':test,'logical_entanglement_fidelity_lower_if_pass':'999/1000','unencoded':[]}
  # All five matched unencoded baselines use the SAME acquired inverse on each site.
  for site,M in enumerate(residual):
   probs=c.holdout_failure_probabilities(M);cuts=make_cdf(probs,Q);seed=plan['unencoded_holdout_seed_base']+100*ci+site;counts=draw_binary(Nu,seed,cuts);key=f'unencoded_N{N}_site{site}';raw[key]=counts;cdf_records[key]={'seed':seed,'N':Nu,'cuts':cuts.tolist(),'sampled_bit_one_means':'unencoded matched-axis failure'};total_un+=Nu
   fail=int(counts[:,1].sum());utest=exact_tail_check(Nu,fail,pu,alpha,False);certs.append(utest)
   row['unencoded'].append({'site':site,'failures':fail,'test':utest,'entanglement_fidelity_upper_if_pass':'997/1000'})
  # Numerical direct32-dimensional verification of the exact16-term Pauli polynomial.
  direct=c.direct_numeric_ptm(residualKs);diff=float(np.max(abs(direct-np.array(actual_logical,float))));assert diff<1e-12
  # Source-informed post hoc scores are computed only after all learning/testing decisions.
  ideal=c.logical_ptm([x['ideal_residual_PTM'] for x in sources]);Jn=np.array(c.choi(actual_logical),complex)
  row['posthoc_actual_logical_infidelity']=float(c.infidelity(actual_logical));row['posthoc_ideal_frame_logical_infidelity']=float(c.infidelity(ideal));row['posthoc_unencoded_infidelities']=[float(c.infidelity(M)) for M in residual];row['direct_channel_PTM_max_error']=diff;row['logical_Choi_min_eigenvalue_float']=float(np.linalg.eigvalsh(Jn).min())
  models[f'logical_PTM_N{N}']=np.array(actual_logical,float)
  for site,frame in enumerate(learned):models[f'learned_frame_N{N}_site{site}']=np.array(frame,complex)
  (HERE/f'exact_channels_N{N}.json').write_text(json.dumps({'logical_PTM':exact_matrix_json(actual_logical),'physical_residual_PTMs':[exact_matrix_json(M) for M in residual],'learned_frames':[exact_matrix_json(U) for U in learned],'source_rates':[str(x['gamma']) for x in sources],'source_PTMs':[exact_matrix_json(x['PTM']) for x in sources],'ideal_frame_logical_PTM':exact_matrix_json(ideal)},indent=2)+'\n')
  records.append(row);print(json.dumps({'N':N,'logical_failures':failures,'logical_pass':test['exact_comparison_pass'],'posthoc_logical_infidelity':row['posthoc_actual_logical_infidelity']}),flush=True)
  # Preserve partial data after each completed fixed candidate; never redraw it on a failure.
  np.savez_compressed(HERE/'raw_counts.npz',**raw)
 np.savez_compressed(HERE/'models.npz',**models);(HERE/'sampling_cdfs.json').write_text(json.dumps(cdf_records,indent=2)+'\n')
 selected=next((r['calibration_N_per_site'] for r in records if r['logical_test']['exact_comparison_pass']),None)
 draws=total_cal+total_log+total_un;TV=s.Rational(draws,Q);assert TV<s.Rational(plan['binary_sampling_record_TV_budget'])
 out={'status':'LOGICAL_HOLDOUT_TARGET_ACCEPTED' if selected is not None else 'ABSTAIN_LOGICAL_HOLDOUT_TARGET','selected_calibration_N_per_site':selected,'calibration_source_exposures':total_cal,'logical_holdout_blocks':total_log,'logical_holdout_physical_exposures':5*total_log,'unencoded_holdout_blocks_and_exposures':total_un,'total_individually_sampled_input_readout_blocks':draws,'total_physical_noise_exposures':total_cal+5*total_log+total_un,'total_final_Pauli_readout_bits':draws,'exact_uniform_test_family_failure_bound':str(12*alpha),'binary_sampling_record_TV_bound':str(TV),'declared_total_failure_budget':plan['total_failure_budget'],'records':records,'controls':{'five_qubit_encoder_calls':total_log,'five_qubit_syndrome_recovery_calls':total_log,'encoded_learned_single_qubit_inverse_calls':5*total_log,'unencoded_learned_single_qubit_inverse_calls':total_un,'clean_zero_ancillas_for_encoding':4*total_log,'discarded_syndrome_qubits':4*total_log,'physical_gate_compilation_executed':False},'scope':'Ideal trusted-control stationary independent-source software instance. Ordinary physical calibration records, learned rational inverses, actual standard-code channel and fresh logical Born readouts. Physical damping paths/syndromes analytically summed, not individually sampled. No hardware, FT threshold, general-memory or positive-capacity claim. Same-information ordinary five-code is identical.','sha256':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in [Path(__file__),HERE/'code_and_channels.py',HERE/'PREDECLARATION.json',HERE/'raw_counts.npz',HERE/'models.npz',HERE/'sampling_cdfs.json',HERE/'threshold_certificates.json']}}
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
