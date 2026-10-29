#!/usr/bin/env python3
"""Replay saved acquisition/holdout only; never calls pipeline main or draws new data."""
from pathlib import Path
import json,hashlib,itertools,math,importlib.util
import numpy as np
import sympy as s
D=Path(__file__).parent
sp=importlib.util.spec_from_file_location('code',D/'code_and_channels.py');c=importlib.util.module_from_spec(sp);sp.loader.exec_module(c)
plan=json.loads((D/'PREDECLARATION.json').read_text());res=json.loads((D/'results.json').read_text());cdf=json.loads((D/'sampling_cdfs.json').read_text());raw=np.load(D/'raw_counts.npz');models=np.load(D/'models.npz');thresholds=json.loads((D/'threshold_certificates.json').read_text());Q=plan['binary_CDF_denominator']
for f,h in res['sha256'].items():assert hashlib.sha256((D/f).read_bytes()).hexdigest()==h
frozen=json.loads((D/'FROZEN_PROTOCOL_HASHES.json').read_text())
for f,h in frozen.items():
 if isinstance(h,str) and len(h)==64 and (D/f).exists():assert hashlib.sha256((D/f).read_bytes()).hexdigest()==h
I=s.eye(2);P=c.P;source=c.generator_sources();CAL=list(itertools.product([1,2,3],[-1,1],[1,2,3]));TEST=list(itertools.product([1,2,3],[-1,1]));replayed=0;cdf_verified=0;exact_frames=0;ptm_errors=[];seen_tests=[];truths=[]
def loadmatrix(M):return s.Matrix([[s.sympify(v) for v in row] for row in M])
def checkbank(key,cuts):
 global replayed,cdf_verified
 meta=cdf[key];assert list(map(int,cuts))==meta['cuts'];cdf_verified+=len(cuts);N=meta['N'];rng=np.random.default_rng(meta['seed']);settings=rng.integers(len(cuts),size=N);u=rng.integers(Q,size=N,dtype=np.int64);bits=(u<np.array(cuts,dtype=np.int64)[settings]).astype(np.int64);cnt=np.zeros((len(cuts),2),np.int64);np.add.at(cnt,(settings,bits),1);assert np.array_equal(cnt,raw[key]);replayed+=N
 return cnt
def binarycuts(probs):return [int(s.floor(p*Q)) for p in probs]
def tail(N,k,p,upper=False):
 # Exact binomial numerator using integer recurrence, independently of comb-sum implementation.
 aa=int(s.numer(p));bb=int(s.denom(p));z=bb-aa;kk=k-1 if upper else k
 term=pow(z,N);num=term
 for j in range(kk):
  factor_num=(N-j)*aa;factor_den=(j+1)*z;newnum=term*factor_num;assert newnum%factor_den==0;term=newnum//factor_den;num+=term
 den=pow(bb,N)
 if upper:num=den-num
 return num,den
def checktest(record):
 num,den=tail(record['N'],record['failures'],s.Rational(record['null_failure_probability']),record['tail']=='upper');alpha=s.Rational(record['alpha']);passed=int(s.denom(alpha))*num<=int(s.numer(alpha))*den
 assert passed==record['exact_comparison_pass']
 h=lambda v:hashlib.sha256(v.to_bytes((v.bit_length()+7)//8,'big')).hexdigest()
 assert h(num)==record['integer_numerator_sha256'] and h(den)==record['integer_denominator_sha256'];seen_tests.append(passed)
for r in thresholds:checktest(r)
for ci,N in enumerate(plan['calibration_shots_per_site']):
 row=res['records'][ci];saved=json.loads((D/f'exact_channels_N{N}.json').read_text());frames=[];localKs=[];local=[]
 for i in range(5):
  src=source[i];M=src['PTM'];assert M==loadmatrix(saved['source_PTMs'][i]);probs=[]
  for j,sg,k in CAL:
   rho=(I+sg*P[j])/2;out=sum((K*rho*K.H for K in src['Ks']),s.zeros(2));probs.append(s.cancel(s.trace((I+P[k])/2*out)))
  counts=checkbank(f'cal_N{N}_site{i}',binarycuts(probs));num=np.zeros((3,3),np.int64)
  for z,(j,sg,k) in enumerate(CAL):num[k-1,j-1]+=9*sg*(int(counts[z,1])-int(counts[z,0]))
  fit=row['frame_fit_records'][i];assert num.tolist()==fit['Bloch_estimate_integer_numerator'];Mhat=num/N;u,sv,vh=np.linalg.svd(Mhat);O=u@np.diag([1,1,np.linalg.det(u@vh)])@vh
  # Independent SO3 lift (positive scalar quaternion branch valid on all saved fits).
  q0=np.sqrt(1+np.trace(O))/2;assert q0>.05
  qv=np.array([O[2,1]-O[1,2],O[0,2]-O[2,0],O[1,0]-O[0,1]])/(4*q0);ts=qv/(1+q0);den=plan['rational_frame_stereographic_denominator'];t=[s.Rational(int(np.rint(v*den)),den) for v in ts];assert list(map(str,t))==fit['rational_stereographic_coordinates']
  d=1+sum(v*v for v in t);U=((1-sum(v*v for v in t))/d)*I-s.I*sum((2*t[j]*P[j+1]/d for j in range(3)),s.zeros(2));U=U.applyfunc(s.cancel);assert U==loadmatrix(saved['learned_frames'][i]) and U==loadmatrix(fit['exact_frame_unitary']);assert (U.H*U-I).applyfunc(s.cancel)==s.zeros(2);exact_frames+=1;frames.append(U)
  Ks=[(U.H*K).applyfunc(s.cancel) for K in src['Ks']];localKs.append(Ks);T=c.exact_ptm(Ks);assert T==loadmatrix(saved['physical_residual_PTMs'][i]);local.append(T)
 T=c.logical_ptm(local);assert T==loadmatrix(saved['logical_PTM']);assert np.max(abs(np.array(T,float)-models[f'logical_PTM_N{N}']))==0
 # Complete Kraus composition independent of tensor-superoperator implementation.
 Enc,Rec=c.exact_encoder_recovery();En=np.array(Enc,complex);Rs=[np.array(r,complex) for r in Rec];globalKs=[np.ones((1,1),complex)]
 for loc in localKs:globalKs=[np.kron(g,np.array(k,complex)) for g in globalKs for k in loc]
 Ls=[r@g@En for r in Rs for g in globalKs];Pn=[np.array(p,complex) for p in P]
 dense=np.array([[sum(np.trace(Pn[a]@l@Pn[b]@l.conj().T).real/2 for l in Ls) for b in range(4)] for a in range(4)]);err=float(np.max(abs(dense-np.array(T,float))));assert err<1e-12;ptm_errors.append(err)
 failures=[s.cancel((1-T[j,j]-sg*T[j,0])/2) for j,sg in TEST];assert s.cancel(sum(failures)/6)==s.Rational(2,3)*c.infidelity(T)
 cnt=checkbank(f'logical_N{N}',binarycuts(failures));assert int(cnt[:,1].sum())==row['logical_failures'];checktest(row['logical_test'])
 for i,Tsite in enumerate(local):
  fail=[s.cancel((1-Tsite[j,j]-sg*Tsite[j,0])/2) for j,sg in TEST];cnt=checkbank(f'unencoded_N{N}_site{i}',binarycuts(fail));assert int(cnt[:,1].sum())==row['unencoded'][i]['failures'];checktest(row['unencoded'][i]['test'])
 truth=float(c.infidelity(T));assert abs(truth-row['posthoc_actual_logical_infidelity'])<1e-16;truths.append(truth)
selected=next((r['calibration_N_per_site'] for r in res['records'] if r['logical_test']['exact_comparison_pass']),None);assert selected==res['selected_calibration_N_per_site']==4096
cal=5*sum(plan['calibration_shots_per_site']);logical=2*plan['logical_holdout_shots_per_pipeline'];uncoded=10*plan['unencoded_holdout_shots_per_site_per_pipeline'];draws=cal+logical+uncoded;exposures=cal+5*logical+uncoded
assert replayed==draws==1019904 and exposures==2068480;assert draws==res['total_individually_sampled_input_readout_blocks'] and exposures==res['total_physical_noise_exposures'];tv=s.Rational(draws,Q);assert tv==s.Rational(res['binary_sampling_record_TV_bound']) and tv<s.Rational(plan['binary_sampling_record_TV_budget']);alpha=s.Rational(plan['one_sided_test_alpha']);assert 12*alpha==s.Rational(res['exact_uniform_test_family_failure_bound']);assert 12*alpha+s.Rational(plan['binary_sampling_record_TV_budget'])<s.Rational(plan['total_failure_budget'])
out={'status':'PASS_FROZEN_ACQUIRED_FRAME_STANDARD_CODE_AND_FRESH_HOLDOUT','saved_input_readout_records_replayed':replayed,'new_acquisition_during_review':0,'exact_CDF_thresholds_recomputed':cdf_verified,'exact_rational_frames_verified':exact_frames,'complete_learned_pipeline_PTM_errors':ptm_errors,'exact_binomial_tail_checks':len(seen_tests),'observed_tests_pass':all(seen_tests[4:]),'selected_calibration_N_per_site':selected,'code_failures':[r['logical_failures'] for r in res['records']],'posthoc_logical_infidelities':truths,'nominal_total_family_failure':'3/5000','sampling_record_TV_bound':str(tv),'physical_noise_exposures':exposures,'scope':'Exact known controls/code/PTM and ideal stationary-source simulation with finite sampled holdout. Trusted encoding, decoding, preparation and readout. No hardware, oracle-optimal unencoded comparison or general memory claim.','sha256':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in [Path(__file__),D/'PREDECLARATION.json',D/'GOVERNING_PROTOCOL.md',D/'FROZEN_PROTOCOL_HASHES.json',D/'code_and_channels.py',D/'run_pipeline.py',D/'raw_counts.npz',D/'models.npz',D/'results.json',D/'sampling_cdfs.json',D/'threshold_certificates.json',D/'exact_channels_N4096.json',D/'exact_channels_N16384.json']}}
(D/'independent_pipeline_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
