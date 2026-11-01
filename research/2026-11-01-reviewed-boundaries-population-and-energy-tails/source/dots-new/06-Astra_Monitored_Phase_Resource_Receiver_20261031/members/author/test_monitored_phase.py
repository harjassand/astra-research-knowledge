#!/usr/bin/env python3
"""Exact identities + independent full joint-generator diagnostics; not hardware evidence."""
import json,hashlib
from pathlib import Path
from fractions import Fraction as F
import numpy as np
import sympy as s
from scipy.linalg import expm
import monitored_phase as m
import certify_receiver as cert
checks={'exact':0,'floating':0}
def exact(ok):
 assert ok;checks['exact']+=1

def near(a,b,tol=2e-10):
 assert np.linalg.norm(np.asarray(a)-np.asarray(b))<tol,(a,b);checks['floating']+=1

I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1);sm=s.Matrix([[0,1],[0,0]]);W=s.diag(1,1,1,-1);k=s.kronecker_product
for A,B in [(k(X,Z),k(X,I)),(k(sm,I),k(sm,Z)),(k(sm.T,I),k(sm.T,Z)),(k(I,Z),k(I,Z)),(k(I,X),k(Z,X))]:exact(W*A*W==B)
exact(W*W==s.eye(4))
# Two source/two data graph interaction remains source blind in proof frame.
W4=s.diag(*[(-1)**(((j>>3)&1)*((j>>1)&1)+((j>>2)&1)*(j&1)) for j in range(16)])
for A in [k(I,I,Z,Z),k(I,I,Z,I),k(I,I,I,Z)]:exact(W4*A*W4==A)
# Exact trace-preservation on the actual lifted CQ generator, including dark/up.
args=(F(2,3),F(7,2),F(1,3),F(4,5),F(1,4),F(2,7),F(1,100))
A,C=cert.build(*args);tr=np.array([1,0,0,1]*4,dtype=object)
exact(all(v==0 for M in A for v in tr@M))

# Independent physical source+DATA instrument; no parity-gauge reduction.
def physical_maps(c,loss,up,em,ep,dt,dark):
 I2=np.eye(2);I4=np.eye(4);X=np.array([[0,1],[1,0]]);Z=np.diag([1,-1]);sm=np.array([[0,1],[0,0]])
 H=c*np.kron(X,Z);L=np.kron(sm,I2);Q=L.T@L;P=L@L.T
 A=-1j*(np.kron(I4,H)-np.kron(H.T,I4))-.5*loss*(np.kron(I4,Q)+np.kron(Q.T,I4))-.5*up*(np.kron(I4,P)+np.kron(P.T,I4))
 Jm=loss*np.kron(L,L);Jp=up*np.kron(L.T,L.T)
 active=A+(1-em)*Jm+(1-ep)*Jp-dark*np.eye(16);inactive=A+Jm+Jp
 click=em*Jm+ep*Jp+dark*np.eye(16)
 E=expm(dt*np.block([[active,np.zeros((16,16))],[click,inactive]]))
 return E[:16,:16],E[16:,:16]

def full_joint(c,loss,up,em,ep,T,bins,q0,e,dark,opt):
 maps=physical_maps(c,loss,up,em,ep,T/bins,dark)
 _,signed=m.instruments(c,loss,up,em,ep,T/bins,dark)
 source=np.diag([1,0]) if q0==0 else np.diag([0,1]);plus=np.ones((2,2))/2
 branches=[(np.kron(source,plus).reshape(16,order='F'),source.reshape(4,order='F'))]
 Z=np.diag([1,-1]);Zbig=np.kron(np.eye(2),Z);Ad=np.kron(Zbig,Zbig)
 for _ in range(bins):
  branches=[((Ad if click else np.eye(16))@maps[click]@rho,signed[click]@d) for rho,d in branches for click in [0,1]]
 out=np.zeros((2,2),complex)
 for rho,d in branches:
  rho=rho.reshape(4,4,order='F')
  for reported in [0,1]:
   score=((1-e)*d[0]-e*d[3]) if reported==0 else ((1-e)*d[3]-e*d[0])
   extra=int(score.real<0) if opt else 0
   U=Z if (reported+q0+extra)%2 else np.eye(2)
   for actual in [0,1]:
    prob=1-e if actual==reported else e
    block=rho[2*actual:2*actual+2,2*actual:2*actual+2]
    out+=prob*U@block@U
 return out

cases=[(1,4,0,.9,0,1,3,0,.01,0),(1,16,2,.99,.1,1,3,1,.2,.03),(.3,0,2,.2,.8,.7,2,0,.03,.02),(0,3,0,1,0,1,2,1,0,0)]
for args in cases:
 c,l,a,em,ep,T,bins,q0,e,d=args
 pos,neg=m.instruments(c,l,a,em,ep,T/bins,d)
 tr=np.array([1,0,0,1]);near(tr@sum(pos),tr)
 for opt in [False,True]:
  p=(m.bayes_error if opt else m.blind_error)(c,l,a,em,ep,T,bins,q0,e,d)
  out=full_joint(*args,opt)
  near(out,np.array([[.5,.5-p],[.5-p,.5]]));near(np.trace(out),1)
  assert np.linalg.eigvalsh(out).min()>-1e-10
 p=m.bayes_error(c,l,a,em,ep,T,bins,q0,e,d);raw=m.raw_error(c,l,a,T)
 assert p<=min(raw,1-raw)+1e-10;checks['floating']+=1

# Compare rational-certificate central values to separately written floating instrument.
rows=json.loads(Path(__file__).with_name('receiver_certificates.json').read_text())['rows']
for row in rows:
 p={k:(int(v) if k in ['bins','q0'] else float(F(v))) for k,v in row['parameters'].items() if k!='endpoint'}
 near(row['bayes_risk_display'],m.bayes_error(p['c'],p['loss'],p['up'],p['eta_m'],p['eta_p'],p['T'],p['bins'],p['q0'],p['readout'],p['dark']))
 exact(F(row['bayes_risk_interval'][1])<F(row['blind_risk_interval'][1])+F(1,10**20))
 exact(F(row['process_risk_radius'])<F(1,10**22))
# Photon-only is an absent source measurement, not noisy measurement hardware.
for row in rows:
    p=row['photon_only_receiver'];l=float(F(p['parameters']['loss']))
    near(p['bayes_risk_display'],m.photon_only_error(1,l,0,.99,0,1,4))
    near(p['blind_risk_display'],m.photon_only_error(1,l,0,.99,0,1,4,opt=False))
    near(p['bayes_risk_display'],m.bayes_error(1,l,0,.99,0,1,4,readout=.5))
    exact(F(p['bayes_risk_interval'][1])<=F(p['blind_risk_interval'][1])+F(1,10**20))
# Higher precision replay; output snapshots are not overwritten.
old=(cert.BITS,cert.S,cert.DEGREE);cert.BITS=128;cert.S=1<<128;cert.DEGREE=52
replay=cert.certify_case(loss=F(256))
prior=rows[2]
exact(max(F(replay['bayes_risk_interval'][0]),F(prior['bayes_risk_interval'][0]))<=min(F(replay['bayes_risk_interval'][1]),F(prior['bayes_risk_interval'][1])))
cert.BITS,cert.S,cert.DEGREE=old
# Literal physical comparison claims.
exact(F(prior['bayes_risk_interval'][1])<F(1,4000))
exact(F(prior['blind_risk_interval'][0])>F(1,1000))
exact(F(rows[-1]['blind_risk_interval'][0])>F(rows[-1]['no_record_comparator']['raw_dephasing_interval'][1]))
# Cold activity bound checked over wide diagnostics, not used as proof.
for l in [1,4,64,1024]:
 for c in [.1,1,3]:
  n=m.count_moments(c,l,0,1);assert n<=4*c*c/l+1e-10;checks['floating']+=1
out={'checks':checks,'scope':'Exact frame/CQ identities and certified interval replay; floating full source-data/record comparisons including upward events and dark counts. No apparatus/hardware claim.','source_sha256':{f:hashlib.sha256(Path(__file__).with_name(f).read_bytes()).hexdigest() for f in ['monitored_phase.py','certify_receiver.py','CONTROLLED_PHASE_RESOURCE_AND_RECEIVER.md']}}
Path(__file__).with_name('test_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
