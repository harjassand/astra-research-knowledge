#!/usr/bin/env python3
"""Deterministic density-matrix channel propagation; no fresh acquisition.
Fixed sampled frame is imported from the received pilot. Physical32-dimensional
state is retained between cycles. No intermediate ideal decoder/reencoder.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
import sys,json,hashlib,time,importlib.util
import numpy as np
HERE=Path(__file__).parent;Q=HERE.parent;PILOT=Q/'five_qubit_acquired_frame_pilot_20261028'
sys.path.insert(0,str(PILOT));import code_and_channels as c
spec=importlib.util.spec_from_file_location('fc',Q/'flagged_five_qubit_storage_check_20261028.py');fc=importlib.util.module_from_spec(spec);spec.loader.exec_module(fc)
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);H=(X+Z)/np.sqrt(2);PA={'I':I,'X':X,'Y':Y,'Z':Z};CX=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],complex)
def rotation(P,a):return np.cos(a/2)*np.eye(len(P))-1j*np.sin(a/2)*P
def left(U,g,qs,n):
 rest=[q for q in range(n) if q not in qs];perm=list(qs)+rest+[n]
 a=U.reshape([2]*n+[U.shape[1]]).transpose(perm)
 a=g@a.reshape(2**len(qs),-1)
 return a.reshape([2]*n+[U.shape[1]]).transpose(np.argsort(perm)).reshape(U.shape)
def fullword(w):
 a=np.ones((1,1),complex)
 for p in w:a=np.kron(a,PA[p])
 return a

def check(k,flagged,eta):
 n=7 if flagged else 6;s=5;f=6;U=np.eye(2**n,dtype=complex)
 # Native preparation |0>,|+> followed by a coherent Y mispreparation.
 U=left(U,rotation(Y,eta),[s],n)
 if flagged:U=left(U,rotation(Y,eta),[f],n)
 for kind,qs in fc.circuit(k,flagged):
  if kind not in ('H','CX'):continue
  U=left(U,H if kind=='H' else CX,qs,n)
  U=left(U,rotation(X if kind=='H' else np.kron(Z,Z),eta),qs,n)
 # Local terminal measurement-basis misalignment. Readout bits otherwise ideal.
 U=left(U,rotation(Y,eta),[s],n)
 if flagged:U=left(U,rotation(Z,eta),[f],n)
 if flagged:
  # Initial s=0,f=+; measure final s inZ, f inX.
  V=(U[:,np.arange(32)*4]+U[:,np.arange(32)*4+1])/np.sqrt(2)
  out={}
  for sb in (0,1):
   for fb in (0,1):out[(sb,fb)]=(V[np.arange(32)*4+2*sb]+(-1)**fb*V[np.arange(32)*4+2*sb+1])/np.sqrt(2)
 else:
  V=U[:,np.arange(32)*2];out={sb:V[np.arange(32)*2+sb] for sb in (0,1)}
 assert np.max(abs(sum(v.conj().T@v for v in out.values())-np.eye(32)))<1e-12
 return out

def correction(word,eta):
 U=np.eye(32,dtype=complex)
 for q,p in enumerate(word):
  if p!='I':U=left(U,rotation(X,eta)@PA[p],[q],5)
 return U

def ec_kraus(eta):
 flagged=[check(k,True,eta) for k in range(4)];plain=[check(k,False,eta) for k in range(4)]
 fresh={(0,)*0:np.eye(32,dtype=complex)}
 for k in range(4):fresh={ss+(bit,):op@old for ss,old in fresh.items() for bit,op in plain[k].items()}
 result=[];prefix=np.eye(32,dtype=complex);fallback=0
 for k in range(4):
  for (sb,fb),op in flagged[k].items():
   if (sb,fb)==(0,0):continue
   for ss,post in fresh.items():
    e=fc.FLAGCOR[k].get(ss) if fb else fc.W1COR[ss]
    if e is None:e=fc.W1COR[ss];fallback+=1
    result.append(correction(fc.string(e),eta)@post@op@prefix)
  prefix=flagged[k][(0,0)]@prefix
 result.append(prefix);K=np.array(result)
 err=float(np.max(abs(np.einsum('kai,kaj->ij',K.conj(),K)-np.eye(32))))
 assert err<2e-12,err
 return K,err,fallback

def superop(K):return np.einsum('kai,kbj->abij',K,K.conj(),optimize=True).reshape(1024,1024)
def apply_local_batch(A,Ks,site):return np.array([c.numpy_apply_local(a,Ks,site) for a in A])
def decode_ptm(A,Rec):
 out=np.array([sum((R@a@R.conj().T for R in Rec),np.zeros((2,2),complex)) for a in A])
 return np.array([[np.trace(c.Pnp[j]@out[k]).real/2 for k in range(4)] for j in range(4)])
def choi(M):return sum((M[a,b]*np.kron(c.Pnp[a],c.Pnp[b].T)/4 for a in range(4) for b in range(4)),np.zeros((4,4),complex))
def metrics(M):
 ch=choi(M);phi=np.array([1,0,0,1])/np.sqrt(2);J0=np.outer(phi,phi)
 return {'logical_PTM':M.tolist(),'entanglement_infidelity':float((3-np.trace(M[1:,1:]))/4),'choi_min_eigenvalue':float(np.linalg.eigvalsh(ch).min()),'choi_trace':float(np.trace(ch).real),'normalized_choi_trace_distance':float(np.linalg.eigvalsh(ch-J0).__abs__().sum()/2),'TP_row_error':float(np.max(abs(M[0]-[1,0,0,0])))}
def main():
 start=time.time();models=np.load(PILOT/'models.npz');selection=json.loads((PILOT/'results.json').read_text())['selected_calibration_N_per_site'];sources=c.generator_sources()
 learned=[models[f'learned_frame_N{selection}_site{i}'].astype(complex) for i in range(5)]
 localKs=[[F.conj().T@np.array(K,complex) for K in src['Ks']] for F,src in zip(learned,sources)]
 Enc,Rec=c.exact_encoder_recovery();Enc=np.array(Enc,complex);Rec=[np.array(r,complex) for r in Rec]
 idealF=superop(np.array([Enc@R for R in Rec]))
 idealK=ec_kraus(0.)[0]
 native_site_bounds=[]
 for ks in localKs:
  pm=np.array([[sum(np.trace(c.Pnp[a]@k@c.Pnp[b]@k.conj().T).real/2 for k in ks) for b in range(4)] for a in range(4)])
  native_site_bounds.append(min(2.,4*metrics(pm)['normalized_choi_trace_distance']))
 native_bound=min(2.,sum(native_site_bounds))
 initial=np.array([Enc@p@Enc.conj().T for p in c.Pnp]);ts=[1,2,4,8,16,32,64,128];rows=[]
 for eta in [0.,0.0001,0.0003,0.001,-0.001,0.003,0.01,-0.01,0.03,-0.03]:
  K,tperr,fb=ec_kraus(eta);F=superop(K)
  if eta==0.:assert np.max(abs(F-idealF))<2e-13
  overlaps=np.einsum('kai,kai->k',idealK.conj(),K)
  phases=np.ones(len(K),complex);mask=abs(overlaps)>1e-14;phases[mask]=overlaps[mask]/abs(overlaps[mask])
  diff=K-phases[:,None,None]*idealK
  gram=np.einsum('kai,kaj->ij',diff.conj(),diff)
  stinespring=float(np.sqrt(max(0.,np.linalg.eigvalsh(gram).max())))
  ec_bound=min(2.,2*stinespring)
  A=initial.copy();run=[]
  for t in range(1,max(ts)+1):
   for site,Ks in enumerate(localKs):A=apply_local_batch(A,Ks,site)
   A=(F@A.reshape(4,1024).T).T.reshape(4,32,32)
   if t in ts:
    row={'T':t,**metrics(decode_ptm(A,Rec))}
    if eta==0. and t==1:assert np.max(abs(np.array(row['logical_PTM'])-models[f'logical_PTM_N{selection}'].astype(float)))<2e-12
    # Diagnostic physical codespace occupation on logical maximally mixed input.
    row['physical_codespace_weight']=float(np.trace((Enc@Enc.conj().T)@A[0]/2).real)
    first=np.array(row['logical_PTM']) if t==1 else np.array(run[0]['logical_PTM'])
    naive=np.linalg.matrix_power(first,t)
    row['naive_decoded_round_product_PTM_max_difference']=float(np.max(abs(np.array(row['logical_PTM'])-naive)))
    row['naive_decoded_round_product_entanglement_infidelity']=metrics(naive)['entanglement_infidelity']
    row['floating_separated_reuse_half_diamond_upper_diagnostic']=min(1.,t*min(1.,2*(row if t==1 else run[0])['normalized_choi_trace_distance'])+(t-1)*(native_bound+ec_bound)*ec_bound/(1-2*ec_bound)) if ec_bound<.5 else None
    run.append(row)
  rows.append({'coherent_angle_per_noisy_operation':eta,'instrument_kraus_count':len(K),'instrument_TP_max_entry_error':tperr,'controller_fallback_branches':fb,'floating_common_stinespring_operator_difference':stinespring,'floating_EC_full_diamond_upper_diagnostic':ec_bound,'results':run});print('completed eta',eta,'seconds',time.time()-start,flush=True)
 # Matched unencoded controls retain the same acquired inverse each native use.
 unencoded=[]
 for site,Ks in enumerate(localKs):
  A=np.array(c.Pnp,complex);rr=[]
  for t in range(1,max(ts)+1):
   A=np.array([sum((K@a@K.conj().T for K in Ks),np.zeros((2,2),complex)) for a in A])
   if t in ts:
    M=np.array([[np.trace(c.Pnp[j]@A[k]).real/2 for k in range(4)] for j in range(4)]);rr.append({'T':t,**metrics(M)})
  unencoded.append({'site':site,'results':rr})
 out={'status':'DETERMINISTIC_PHYSICAL_STATE_REUSE_CALCULATION','selected_existing_calibration_N_per_site':selection,'no_fresh_acquisition':True,'source_models_sha256':hashlib.sha256((PILOT/'models.npz').read_bytes()).hexdigest(),'source_generator_sha256':hashlib.sha256((PILOT/'code_and_channels.py').read_bytes()).hexdigest(),'floating_native_full_diamond_upper_diagnostic':native_bound,'floating_native_site_full_diamond_upper_diagnostics':native_site_bounds,'native_source_gammas':[float(s['gamma']) for s in sources],'ideal_EC_full_operator_match_max_error':float(np.max(abs(superop(ec_kraus(0.)[0])-idealF))),'coherent_EC_full_diamond_triangle_bound':'min(2,101*2*abs(sin(eta/2))); branch-uniform potential noisy-slot count, with ideal idles/readout','EC_control_model':'stationary coherent post-CX ZZ, post-H X, prep Y, measurement Y(s)/Z(f), correction X rotation; common angle eta. No twirling. Idles and classical readout ideal.','fallback':'undefined flag syndrome uses ordinary weight1 correction','encoded_runs':rows,'matched_unencoded':unencoded,'elapsed_seconds':time.time()-start}
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
 print('DONE',time.time()-start,flush=True)
if __name__=='__main__':main()
