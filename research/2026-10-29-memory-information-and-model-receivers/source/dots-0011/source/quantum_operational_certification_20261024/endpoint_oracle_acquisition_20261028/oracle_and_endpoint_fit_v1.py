#!/usr/bin/env python3
"""Full-CPTP qubit endpoint oracle and physically budgeted sampled endpoint fits.
The fit receives counts only. Generator truth used only in sampling and scoring.
No imports from the acquired-frame fitting implementation.
"""
from pathlib import Path
import numpy as np,json,hashlib,itertools
HERE=Path(__file__).parent;Q=HERE.parent
SETTINGS=list(itertools.product(range(3),[-1,1],range(3)))

def oracle(M):
 A=np.array(M,float)[1:,1:];U,s,Vh=np.linalg.svd(A)
 B=Vh.T@np.diag([1.,1.,np.linalg.det(Vh.T@U.T)])@U.T
 R=np.eye(4);R[1:,1:]=B
 score=(1+np.trace(B@A))/4
 formula=(1+s[0]+s[1]+np.linalg.det(Vh.T@U.T)*s[2])/4
 assert abs(score-formula)<1e-12
 return R,float(score)

def fit(counts):
 """Only ordinary endpoint counts enter this function; no channel truth."""
 means=(counts[:,1]-counts[:,0])/counts.sum(axis=1)
 A=np.zeros((3,3))
 for j in range(3):
  for k in range(3):
   ip=SETTINGS.index((j,1,k));im=SETTINGS.index((j,-1,k));A[k,j]=(means[ip]-means[im])/2
 M=np.eye(4);M[1:,1:]=A
 R,_=oracle(M)
 return R,A

def sample_counts(M,N,seed):
 alloc=np.full(18,N//18,int);alloc[:N%18]+=1
 assert alloc.min()>0
 probs=np.array([(1+M[k+1,0]+sg*M[k+1,j+1])/2 for j,sg,k in SETTINGS])
 assert probs.min()>-1e-12 and probs.max()<1+1e-12
 rng=np.random.default_rng(seed);plus=rng.binomial(alloc,np.clip(probs,0,1));return np.stack([alloc-plus,plus],axis=1)

def fe(M):return float((1+np.trace(np.array(M)[1:,1:]))/4)
def source_sets():
 paths=[Q/'noisy_repeated_flagged_storage_20261028/results.json']+sorted((Q/'clocked_flagged_storage_20261028').glob('*_v1.json'))
 out=[]
 for p in paths:
  j=json.loads(p.read_text())
  if 'same_elapsed_unencoded' in j:bs=j['same_elapsed_unencoded'];label=p.stem;scope='equal_elapsed_clocked_model'
  elif 'matched_unencoded' in j:bs=j['matched_unencoded'];label='original_ideal_idle';scope='native_use_count_only_not_elapsed_time'
  else:continue
  out.append((label,p,bs,scope))
 return out

def test_oracle():
 tests=[np.diag([1,1,1,1]),np.diag([1,-1/3,-1/3,-1/3]),np.diag([1,0,0,1]),np.diag([1,0,0,0]),np.diag([1,1,-1,-1])]
 expected=[1,1/3,.5,.25,1]
 for M,target in zip(tests,expected):assert abs(oracle(M)[1]-target)<1e-12
 # Sample random CPTP maps from independent complex Stinespring isometries.
 P=[np.eye(2),np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
 rng=np.random.default_rng(278431)
 def random_ptm():
  A=rng.normal(size=(8,2))+1j*rng.normal(size=(8,2));V=np.linalg.qr(A)[0];Ks=V.reshape(4,2,2)
  return np.array([[sum(np.trace(a@K@b@K.conj().T).real/2 for K in Ks) for b in P] for a in P])
 violation=0
 for _ in range(100):
  M=random_ptm();R,f=oracle(M)
  assert abs(np.linalg.det(R[1:,1:])-1)<1e-12
  assert np.max(abs(R[1:,1:].T@R[1:,1:]-np.eye(3)))<1e-12
  for _ in range(100):violation=max(violation,fe(random_ptm()@M)-f)
 assert violation<1e-12
 return {'known_cases':5,'random_channel_instances':100,'random_CPTP_decoder_challenges':10000,'maximum_score_excess':violation,'not_proof':'Finite challenges supplement the separate full-CPTP proof.'}

def main():
 sets=source_sets();oracle_rows=[];raw={};pilots=[]
 # Fixed before acquisition: all5sites, budgets20480 and102400 native uses,
 # T=1,8,32. No source-selected site/horizon and no best-seed selection.
 chosen=['original_ideal_idle','zero_clock_v1','rate_0.01_v1','rate_0.1_v1']
 for label,path,bs,scope in sets:
  sha=hashlib.sha256(path.read_bytes()).hexdigest();records=[]
  for site in bs:
   sr=[]
   for rr in site['results']:
    M=np.array(rr['logical_PTM']);R,opt=oracle(M)
    sr.append({'T':rr['T'],'fixed_control_entanglement_infidelity':1-fe(M),'full_CPTP_endpoint_oracle_infidelity':1-opt,'oracle_recovery_PTM':R.tolist(),'endpoint_PTM':M.tolist()})
   records.append({'site':site['site'],'results':sr})
  oracle_rows.append({'source_label':label,'source_sha256':sha,'source_file':str(path.relative_to(Q)),'comparison_scope':scope,'sites':records})
  if label not in chosen:continue
  for budget in [20480,102400]:
   for T in [1,8,32]:
    N=budget//(5*T);row={'source_label':label,'total_native_exposure_budget':budget,'T':T,'endpoint_shots_per_site':N,'actual_total_native_exposures':5*N*T,'sites':[]}
    for site in bs:
     idx=site['site'];M=np.array(next(r for r in site['results'] if r['T']==T)['logical_PTM'])
     labelid=chosen.index(label);seed=510000+labelid*100000+budget+T*100+idx
     key=f'{label}_B{budget}_T{T}_site{idx}';counts=sample_counts(M,N,seed);raw[key]=counts
     R,Ahat=fit(counts);opt=oracle(M)[1];score=fe(R@M)
     assert score<=opt+1e-12
     row['sites'].append({'site':idx,'seed':seed,'raw_key':key,'fitted_endpoint_Bloch_estimate':Ahat.tolist(),'fitted_recovery_PTM':R.tolist(),'scorer_true_infidelity_of_sampled_fit':1-score,'source_informed_oracle_infidelity':1-opt,'fixed_control_infidelity':1-fe(M),'scorer_fit_regret_vs_oracle':opt-score})
    pilots.append(row)
 rawpath=HERE/'endpoint_sampled_counts_v1.npz'
 if rawpath.exists():
  prior=np.load(rawpath)
  assert set(prior.files)==set(raw)
  assert all(np.array_equal(prior[k],v) for k,v in raw.items())
 else:np.savez(rawpath,**raw)
 out={'status':'DETERMINISTIC_ORACLE_AND_SEEDED_ORDINARY_ENDPOINT_ACQUISITION_PILOT','oracle_tests':test_oracle(),'oracle_rows':oracle_rows,'endpoint_fit_pilots':pilots,'acquisition_scope':'Each pilot is a separate counterfactual budget experiment, not all pilots jointly within one budget. No statistical high-fidelity certification or operational best-site selection. Each endpoint shot costsT native uses plusT full elapsed windows. Final decoder gate treated as one-off ideal control.','raw_counts_sha256':hashlib.sha256(rawpath.read_bytes()).hexdigest()}
 (HERE/'oracle_and_endpoint_fit_v1.json').write_text(json.dumps(out,indent=2)+'\n')
 print('source sets',len(sets),'budgeted pilots',len(pilots),'sampled endpoint blocks',sum(int(v.sum()) for v in raw.values()))
 for row in oracle_rows:
  vals=[next(r for r in s['results'] if r['T']==32)['full_CPTP_endpoint_oracle_infidelity'] for s in row['sites']]
  print(row['source_label'],'T32oracle',min(vals),max(vals))
if __name__=='__main__':main()
