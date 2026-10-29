#!/usr/bin/env python3
"""Explicit Clifford encoder and noisy physical inverse decoder; no logical oracle."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
import sys,json,numpy as np
HERE=Path(__file__).parent;Q=HERE.parent
sys.path.insert(0,str(Q/'clocked_flagged_storage_20261028'));import clocked_channel_v1 as m
I,X,Y,Z=m.P;H=m.old.H;S=np.diag([1,1j]);CX=m.old.CX
GATES={'H':H,'S':S,'SDG':S.conj().T,'X':X,'CX':CX}
CLOCK={'one':1.,'two':2.,'prep':2.,'measure':4.,'feedback':1.}
def full(g,qs):return m.old.left(np.eye(32,dtype=complex),g,qs,5)
def word(A):
 # Single Pauli, coefficients recovered exactly to floating roundoff.
 best=None
 for ix,d in enumerate(m.digits(5)):
  B=m.old.fullword(''.join('IXYZ'[v] for v in d));z=np.trace(B@A)/32
  if abs(z)>.5:return list(d),int(round(z.real))
 raise ValueError('not Pauli')
def synthesize():
 gens=[m.old.fullword(w) for w in m.c.GWORDS]+[m.old.fullword('ZZZZZ')]
 U=np.eye(32,dtype=complex);ops=[]
 def apply(name,qs):
  nonlocal U,gens
  V=full(GATES[name],qs);U=V@U;gens=[V@a@V.conj().T for a in gens];ops.append((name,list(qs)))
 targets=[1,2,3,4,0]
 for k,t in enumerate(targets):
  for j,p in enumerate(targets[:k]):
   d,sg=word(gens[k])
   if d[p]==3:gens[k]=gens[k]@gens[j]
   else:assert d[p]==0
  remain=targets[k:];d,sg=word(gens[k]);pivot=next(p for p in remain if d[p])
  if pivot!=t:
   apply('CX',[pivot,t]);apply('CX',[t,pivot]);apply('CX',[pivot,t])
  for p in remain:
   d,sg=word(gens[k])
   if d[p]==1:apply('H',[p])
   elif d[p]==2:apply('SDG',[p]);apply('H',[p])
  for p in remain:
   if p==t:continue
   d,sg=word(gens[k])
   if d[p]==3:apply('CX',[p,t])
  d,sg=word(gens[k]);assert d[t]==3 and sum(v!=0 for v in d)==1
  if sg<0:apply('X',[t])
 # Correct the exact logical phase by comparing the two canonical code columns.
 E=np.array(m.c.exact_encoder_recovery()[0],complex);B=U@E;V=B[[0,16],:]
 assert np.max(abs(np.delete(B,[0,16],axis=0)))<1e-12
 ratio=V[1,1]/V[0,0]
 choices=[('X',X),('S',S),('SDG',S.conj().T)]
 if abs(ratio+1)<1e-10:apply('S',[0]);apply('S',[0])
 elif abs(ratio-1j)<1e-10:apply('SDG',[0])
 elif abs(ratio+1j)<1e-10:apply('S',[0])
 else:assert abs(ratio-1)<1e-10
 B=U@E;phase=B[0,0];assert np.max(abs(B[[0,16],:]/phase-np.eye(2)))<1e-12
 inv={'H':'H','S':'SDG','SDG':'S','X':'X','CX':'CX'}
 return ops,[(inv[n],qs) for n,qs in reversed(ops)],U

def circuit(A,ops,eta,rate):
 for name,qs in ops:
  err=np.kron(Z,Z) if name=='CX' else X
  gate=m.old.rotation(err,eta)@GATES[name]
  A=m.local(A,m.ptm(gate),qs,5)
  A=m.background(A,rate,2 if name=='CX' else 1,list(range(5)),5)
 return A

def initial(eta,rate):
 # Single arbitrary unknown input q0; four local fresh |0> ancillas.
 A=np.zeros((1024,4))
 for d in m.digits(5):
  if all(v in [0,3] for v in d[1:]):A[np.ravel_multi_index(d,[4]*5),d[0]]=2
 for q in range(1,5):
  A=m.local(A,m.ptm(m.old.rotation(Y,eta)),[q],5)
  # Sequential reset/preparation; data q0 and already prepared ancillas are live.
  A=m.background(A,rate,2,list(range(q+1)),5)
 return A

def output(A):return A[[0,256,512,768],:]/2

def syndrome_table(U):
 E=np.array(m.c.exact_encoder_recovery()[0],complex);table={}
 for w in ['IIIII']+[''.join(p if k==q else 'I' for k in range(5)) for q in range(5) for p in 'XYZ']:
  B=U@m.old.fullword(w)@E
  for a in range(16):
   C=B[[a,16+a],:]
   if np.linalg.norm(C)>.1:
    assert np.linalg.norm(C)>1.4
    p=next(j for j,P in enumerate(m.P) if abs(np.trace(P@C)/2)>.99)
    assert a not in table;table[a]=p
 assert len(table)==16
 return table

def measured_decode(A,U,eta,rate):
 table=syndrome_table(U);live=list(range(5))
 for q in range(1,5):
  # Background during actual readout followed by basis misalignment, as prior model.
  A=m.background(A,rate,4,live,5)
  A=m.local(A,m.ptm(m.old.rotation(Y,eta)),[q],5);live.remove(q)
 A=m.background(A,rate,1,[0],5) # classical feedback latency
 result=np.zeros((4,A.shape[1]))
 for a in range(16):
  bits=[(a>>(3-q))&1 for q in range(4)];B=np.zeros_like(result)
  for d in m.digits(5):
   if all(v in [0,3] for v in d[1:]):
    sign=(-1)**sum(bits[q] for q in range(4) if d[q+1]==3)
    B[d[0]]+=sign*A[np.ravel_multi_index(d,[4]*5)]/32
  if table[a]:B=m.ptm(m.old.rotation(X,eta)@m.P[table[a]])@B
  B=np.diag([1,np.exp(-rate),np.exp(-rate),1])@B
  result+=B
 return result
def run(eta=.001,integrated=.03,T=32,r=2):
 dec,enc,U=synthesize();rate=integrated/201;A=initial(eta,rate);A=circuit(A,enc,eta,rate)
 F,timing=m.build_ec(eta,rate,CLOCK);mts=m.native()
 for step in range(T):
  for q,M in enumerate(mts):A=m.local(A,M,[q],5)
  if (step+1)%r==0:A=F@A
 A=circuit(A,dec,eta,rate);M=measured_decode(A,U,eta,rate)
 return {'eta':eta,'integrated':integrated,'T':T,'r':r,'physical_output_PTM':M.tolist(),**m.old.metrics(M),'encoder_gates':enc,'decoder_gates':dec,'terminal_syndrome_lookup':syndrome_table(U),'boundary_time':26+2*sum(2 if n=='CX' else 1 for n,q in dec),'storage_time':2*T+201*(T//r),'notes':'Output is actual physical q0 after inverse Clifford, four noisy syndrome measurements, feedback and conditional physical Pauli. No ideal terminal recovery. Boundary noise is explicit; endpoint single-qubit test SPAM remains trusted.'}
if __name__=='__main__':
 dec,enc,U=synthesize();A=circuit(initial(0,0),enc,0,0);canonical,_=m.code_coordinates();assert np.max(abs(A-canonical))<1e-11
 M=output(circuit(A,dec,0,0));assert np.max(abs(M-np.eye(4)))<1e-11
 (HERE/'encoder_check_v2.json').write_text(json.dumps({'gates':dec,'zero_noise_code_entry_error':float(np.max(abs(A-canonical))),'zero_noise_roundtrip_error':float(np.max(abs(M-np.eye(4))))},indent=2))
 assert np.max(abs(measured_decode(circuit(canonical,dec,0,0),U,0,0)-np.eye(4)))<1e-11
 rows=[]
 for integ,T,r in [(.0,0,1),(.03,0,1),(.03,32,2),(.1,32,4)]:
  row=run(integrated=integ,T=T,r=r);rows.append(row);print(integ,T,r,row['entanglement_infidelity'],flush=True)
 (HERE/'results_v2.json').write_text(json.dumps(rows,indent=2)+'\n')
