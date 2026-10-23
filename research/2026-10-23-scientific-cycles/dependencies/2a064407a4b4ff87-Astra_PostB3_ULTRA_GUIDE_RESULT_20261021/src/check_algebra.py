"""Bounded algebra/information-boundary checks; no RNA matrix values read."""
import json,types,time
from pathlib import Path
import numpy as np
from scipy.optimize import nnls
from run_guide_experiment import Data,fit_nonnegative,project,fit_direction
start=time.perf_counter();root=Path(__file__).resolve().parents[1];design=json.loads((root/'results/DESIGN_MAP.json').read_text());rng=np.random.default_rng(8142)
a=rng.normal(size=(20,32));b=rng.normal(size=(20,32));t=rng.normal(size=(20,32));va=rng.uniform(.1,1,20);vb=rng.uniform(.1,1,20);beta,_=fit_nonnegative(a,b,t,va,vb)
err=[]
for i in range(20):
 floor=1e-8*max(np.dot(a[i],a[i])+np.dot(b[i],b[i]),1e-12);ridge=np.sqrt(np.array([va[i],vb[i]])+floor);x=np.vstack([np.stack([a[i],b[i]],1),np.diag(ridge)]);y=np.r_[t[i],ridge];ordinary,_=nnls(x,y);err.append(float(np.max(np.abs(beta[i]-ordinary))))
if max(err)>1e-8:raise ValueError('NNLS mismatch')
refs=rng.normal(size=(20,4,32));v=rng.normal(size=(20,32));q,rank=project(v,refs)
if np.max(np.abs(np.einsum('nkg,ng->nk',refs,q)))>1e-8:raise ValueError('projection not orthogonal')
# Actual metadata design, synthetic outcomes only.
arrays=sorted(design['delivered_counts']);ai={a:i for i,a in enumerate(arrays)};families=[x for x in design['families'] if x['eligible']];d=types.SimpleNamespace(N=len(families),ng=32,idx=np.array([[ai[a] for a in x['arms']] for x in families]),c=ai[design['matching_control']]);targets=sorted(set([f['a'] for f in families]+[f['b'] for f in families]));d.inc=np.zeros((d.N,len(targets)))
for i,f in enumerate(families):d.inc[i,targets.index(f['a'])]=1;d.inc[i,targets.index(f['b'])]=1
d.noise={k:np.ones(len(arrays))*.001 for k in ['log','rate']};d.hats=[Data.ridge_hats(d,np.array([design['delivered_counts'][arrays[j]] for j in d.idx[:,direction]])) for direction in (0,1)];m=rng.uniform(0,1,size=(len(arrays),32));first=fit_direction(d,m,'log',0,True);mut=m.copy();mut[d.idx[:,1]]+=100*rng.normal(size=(d.N,32));second=fit_direction(d,mut,'log',0,True)
for key in ['beta','cv']:
 if not np.array_equal(first[key],second[key]):raise ValueError('heldout response leaked to calibration '+key)
if first['lambda_index']!=second['lambda_index'] or not np.array_equal(first['null_means'][d.idx[:,1]],second['null_means'][d.idx[:,1]]):raise ValueError('heldout response leaked to null expectation')
c=rng.normal(size=(7,32));mean=c.mean(0);trace=np.sum((c-mean)**2)/(7*6);left=np.dot(mean,mean)-trace;right=(np.sum(c@c.T)-np.sum(c*c))/(7*6)
if abs(left-right)>1e-12:raise ValueError('control U-stat identity')
out={'no_RNA_matrix_values_read':True,'NNLS_independent_max_error':max(err),'projection_orthogonality':'PASS','heldout_pair_response_mutation':'calibration and source-only null expectation unchanged','control_U_statistic_identity_error':abs(left-right),'wall_s':time.perf_counter()-start};(root/'results/ALGEBRA_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
