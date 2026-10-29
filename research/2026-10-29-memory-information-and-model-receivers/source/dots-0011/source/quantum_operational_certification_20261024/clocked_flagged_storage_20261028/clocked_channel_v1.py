#!/usr/bin/env python3
"""Exact finite-dimensional CPTP model evaluated in floating Pauli coordinates.
Clock v1: independent Markovian Z dephasing on every live qubit throughout each
interval, including gate supports. Coherent control model matches prior run.
No trajectories and no intermediate decoded reset.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
import numpy as np,json,sys,importlib.util,time
HERE=Path(__file__).parent;Q=HERE.parent
spec=importlib.util.spec_from_file_location('old',Q/'noisy_repeated_flagged_storage_20261028/run_channel.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
fc=old.fc;c=old.c
P=[old.I,old.X,old.Y,old.Z]
def ptm(U):
 n=int(round(np.log2(len(U))));basis=[np.ones((1,1),complex)]
 for _ in range(n):basis=[np.kron(a,b) for a in basis for b in P]
 return np.array([[np.trace(a@U@b@U.conj().T).real/len(U) for b in basis] for a in basis])
HT=ptm(old.H);CXT=ptm(old.CX)
DIGITS={}
def digits(n):
 if n not in DIGITS:DIGITS[n]=np.array(np.unravel_index(np.arange(4**n),[4]*n)).T
 return DIGITS[n]
def local(B,T,qs,n):
 """Sparse local PTM left action on rows, preserving arbitrary column payload."""
 d=digits(n);loc=np.zeros(len(d),int)
 for q in qs:loc=4*loc+d[:,q]
 powers=np.array([4**(n-1-q) for q in qs]);base=np.arange(len(d))-d[:,qs]@powers
 out=np.zeros_like(B)
 for a in range(len(T)):
  rows=np.flatnonzero(loc==a)
  for b in np.flatnonzero(abs(T[a])>1e-14):
   bd=np.array(np.unravel_index(b,[4]*len(qs)));ix=base[rows]+bd@powers
   out[rows]+=T[a,b]*B[ix]
 return out

def background(B,rate,duration,live,n):
 if rate==0 or duration==0:return B
 count=np.sum(np.isin(digits(n)[:,live],[1,2]),axis=1)
 return np.exp(-rate*duration*count)[:,None]*B

def duration(kind,clock):
 if kind in ('H','P'):return clock['one']
 if kind=='CX':return clock['two']
 if kind.startswith('prep'):return clock['prep']
 if kind.startswith('measure'):return clock['measure']
 if kind.startswith('readout'):return clock['feedback']
 raise ValueError(kind)
def check(k,flagged,eta,rate,clock):
 n=7 if flagged else 6;ancn=4**(n-5);B=np.zeros((4**n,1024))
 av=np.kron([1,0,0,1],[1,1,0,0]) if flagged else np.array([1,0,0,1])
 for a in np.flatnonzero(av):B[np.arange(1024)*ancn+a,np.arange(1024)]=av[a]
 live=list(range(5))
 for kind,qs in fc.circuit(k,flagged):
  dt=duration(kind,clock)
  if kind.startswith('prep'):
   live+=list(qs);B=local(B,ptm(old.rotation(old.Y,eta)),qs,n)
  elif kind=='H':B=local(B,ptm(old.rotation(old.X,eta)@old.H),qs,n)
  elif kind=='CX':B=local(B,ptm(old.rotation(np.kron(old.Z,old.Z),eta)@old.CX),qs,n)
  # Every live qubit receives the background process for this full interval.
  B=background(B,rate,dt,live,n)
  if kind.startswith('measure'):
   B=local(B,ptm(old.rotation(old.Y if kind=='measureZ' else old.Z,eta)),qs,n)
   live=[q for q in live if q not in qs]
  # Ancilla measurement projectors commute with all subsequent local operations;
  # postpone their contraction, but never expose a discarded ancilla again.
 if flagged:
  A=B.reshape(1024,4,4,1024)
  out={(s,f):(A[:,0,0]+(-1)**s*A[:,3,0]+(-1)**f*A[:,0,1]+(-1)**(s+f)*A[:,3,1])/4 for s in (0,1) for f in (0,1)}
 else:
  A=B.reshape(1024,4,1024);out={s:(A[:,0]+(-1)**s*A[:,3])/2 for s in (0,1)}
 total=sum(out.values());assert np.max(abs(total[0]-np.eye(1024)[0]))<1e-11
 return out

def correction(B,word,eta,rate,clock):
 for q,p in enumerate(word):
  if p!='I':B=local(B,ptm(old.rotation(old.X,eta)@old.PA[p]),[q],5)
  # ALL five fixed site windows elapse, including identity/bypassed corrections.
  B=background(B,rate,clock['one'],list(range(5)),5)
 return B

def build_ec(eta,rate,clock):
 start=time.time();flag=[check(k,True,eta,rate,clock) for k in range(4)];plain=[check(k,False,eta,rate,clock) for k in range(4)]
 tf=sum(duration(k,clock) for k,qs in fc.circuit(0,True));tu=sum(duration(k,clock) for k,qs in fc.circuit(0,False))
 fresh={():np.eye(1024)}
 for k in range(4):fresh={ss+(s,):op@prev for ss,prev in fresh.items() for s,op in plain[k].items()}
 recovery={}
 for mode in [-1,0,1,2,3]:
  R=np.zeros((1024,1024))
  for ss,op in fresh.items():
   e=fc.W1COR[ss] if mode==-1 else fc.FLAGCOR[mode].get(ss,fc.W1COR[ss])
   R+=correction(op,fc.string(e),eta,rate,clock)
  recovery[mode]=R
 F=np.zeros((1024,1024));prefix=np.eye(1024)
 for k in range(4):
  for (s,f),op in flag[k].items():
   if (s,f)==(0,0):continue
   stopped=op@prefix
   # Remaining flagged windows really elapse as data memory exposure.
   stopped=background(stopped,rate,(3-k)*tf,list(range(5)),5)
   F+=recovery[k if f else -1]@stopped
  prefix=flag[k][(0,0)]@prefix
 prefix=background(prefix,rate,4*tu,list(range(5)),5)
 F+=correction(prefix,'IIIII',eta,rate,clock)
 assert np.max(abs(F[0]-np.eye(1024)[0]))<3e-11
 return F,{'flag_window':tf,'unflagged_window':tu,'total_EC_time':4*tf+4*tu+5*clock['one'],'construction_seconds':time.time()-start}

def code_coordinates():
 initial=np.zeros((1024,4));decoder=np.zeros((4,1024))
 for j,row in enumerate(c.COS):
  for w,sign in row:
   ix=np.ravel_multi_index(w,[4]*5);initial[ix,j]=2*sign
   decoder[j,ix]=sign*(16-4*sum(v!=0 for v in w))/32
 assert np.max(abs(decoder@initial-np.eye(4)))==0
 return initial,decoder

def native():
 models=np.load(old.PILOT/'models.npz');sel=json.loads((old.PILOT/'results.json').read_text())['selected_calibration_N_per_site'];srcs=c.generator_sources();mts=[]
 for i,src in enumerate(srcs):
  W=models[f'learned_frame_N{sel}_site{i}'].astype(complex);ks=[W.conj().T@np.array(K,complex) for K in src['Ks']]
  mts.append(np.array([[sum(np.trace(P[a]@K@P[b]@K.conj().T).real/2 for K in ks) for b in range(4)] for a in range(4)]))
 return mts

def run_one(eta,integrated,clock,Ts=(1,2,4,8,16,32)):
 tf=sum(duration(k,clock) for k,qs in fc.circuit(0,True));tu=sum(duration(k,clock) for k,qs in fc.circuit(0,False));tau=4*tf+4*tu+5*clock['one'];rate=integrated/tau
 F,timing=build_ec(eta,rate,clock);initial,D=code_coordinates();mts=native();A=initial.copy();rows=[]
 for t in range(1,max(Ts)+1):
  for q,M in enumerate(mts):A=local(A,M,[q],5)
  A=F@A
  if t in Ts:rows.append({'T':t,**old.metrics(D@A)})
 baseline=[]
 idle=np.diag([1,np.exp(-integrated),np.exp(-integrated),1])
 for i,M in enumerate(mts):
  E=idle@M;baseline.append({'site':i,'results':[{'T':t,**old.metrics(np.linalg.matrix_power(E,t))} for t in Ts]})
 return {'eta':eta,'integrated_background_strength_EC_window':integrated,'background_rate_per_reference_time':rate,'clock':clock,'timing':timing,'encoded':rows,'same_elapsed_unencoded':baseline,'TP_max_entry_error':float(np.max(abs(F[0]-np.eye(1024)[0])))}

if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--eta',type=float,default=.001);ap.add_argument('--integrated',type=float,default=0.);ap.add_argument('--output',default='case_v1.json');args=ap.parse_args()
 clock={'one':1.,'two':2.,'prep':2.,'measure':4.,'feedback':1.}
 result=run_one(args.eta,args.integrated,clock)
 (HERE/args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'output':args.output,'timing':result['timing'],'T32_infidelity':result['encoded'][-1]['entanglement_infidelity']},indent=2))
