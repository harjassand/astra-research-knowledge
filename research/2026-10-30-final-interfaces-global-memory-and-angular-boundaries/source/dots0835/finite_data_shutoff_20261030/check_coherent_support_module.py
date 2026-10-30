"""Finite full-operator support-module regression; NOT the native many-body theorem.
Two coherent owner clocks, overlapping DATA footprints, retained bath, physical
DATA-identity reset channels, finite payload ramps, and an activation insertion.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
# 2 qutrit owner clocks, 4 DATA qubits, 1 retained bath qubit.
dims=[3,3,2,2,2,2,2];D=int(np.prod(dims));I=np.eye(D,dtype=complex)
strides=np.array([int(np.prod(dims[j+1:])) for j in range(len(dims))])
labels=np.array(np.unravel_index(np.arange(D),dims)).T

def embed(op,sites):
 sites=list(sites);sd=[dims[j] for j in sites];ds=int(np.prod(sd));out=np.zeros((D,D),complex)
 for src in range(D):
  old=labels[src];a=np.ravel_multi_index(tuple(old[sites]),sd)
  for b in range(ds):
   val=op[b,a]
   if abs(val):
    new=old.copy();new[sites]=np.unravel_index(b,sd);dst=int(new@strides);out[dst,src]+=val
 return out
X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]);Y=np.array([[0,-1j],[1j,0]])
pr=np.diag([1,0,0]);p2=np.diag([0,0,1]);hop=np.zeros((3,3),complex);hop[2,1]=1
reset=np.zeros((3,3),complex);reset[0,2]=1
P=[embed(pr,[h]) for h in range(2)];B=[I-p for p in P]
U0=expm(-.31j*(np.kron(X,X)+.47*np.kron(Z,Y)))
U1=expm(-.43j*(np.kron(X,Z)+.27*np.kron(Y,X)))
H=[]
for h,sites,u in [(0,[2,3],U0),(1,[3,4],U1)]:
 c=embed(hop,[h])@embed(u,sites);H.append(c+c.conj().T)
Js=[.6*embed(reset,[h]) for h in range(2)]
aux=.13*(embed(hop+hop.conj().T,[0])@embed(hop+hop.conj().T,[1]))
loss=sum((j.conj().T@j for j in Js),np.zeros_like(I))
# Actual piecewise finite amplitude ramp, every segment Hermitian/positive loss.
K1=expm((-1j*(H[0]+.8*H[1]+aux)-loss/2)*.19)
K2=expm((-1j*(.45*H[0]+.2*H[1]+aux)-loss/2)*.23)
K3=expm((-1j*aux-loss/2)*.17) # DATA completely off by final segment.
def norm_comm(a,b):return float(np.linalg.norm(a@b-b@a))
checks=[]
foot={0:{2,3},1:{3,4}}
for mask in [set(),{0},{1},{0,1}]:
 q=I.copy()
 for h in range(2):
  if h not in mask:q=q@P[h]
 support=set().union(*(foot[h] for h in mask)) if mask else set()
 # Nojump segment, plus actual DATA-identity reset at an intermediate time.
 for name,K in [('nojump',K3@K2@K1),('reset0',K3@K2@Js[0]@K1),('reset1',K3@Js[1]@K2@K1)]:
  a=K@q;outside=[s for s in range(2,6) if s not in support]
  err=max([norm_comm(a,embed(p,[s])) for s in outside for p in [X,Z]] or [0.])
  leak=float(np.linalg.norm((I-q)@a))
  assert err<1e-11 and leak<1e-11
  checks.append({'source_nonready_mask':sorted(mask),'coefficient':name,'max_outside_DATA_commutator':err,'source_subspace_leakage':leak})
# One local insertion on owner1+retained bath activates owner1 without directly touching DATA.
activation=np.zeros((3,3),complex);activation[1,0]=activation[0,1]=1
Nleft=embed(activation,[1])@embed(X,[6])
Q0=P[1] # only owner0 permitted active initially
Kact=K3@K2@Nleft@K1@Q0
outside3=max(norm_comm(Kact,embed(p,[5])) for p in [X,Z])
new_data2=max(norm_comm(Kact,embed(p,[4])) for p in [X,Z])
assert outside3<1e-11 and new_data2>1e-3
# Coherent different initial masks: keep each coefficient, do not collapse their supports.
Qexact0=B[0]@P[1];Qexact1=P[0]@B[1]
left0=K2@K1@Qexact0;left1=K2@K1@Qexact1
coherent=np.linalg.norm(left0+1j*left1)
assert coherent>0
# Failure witness: restoring initiation permits DATA action outside the initial empty mask.
init=embed(activation,[1]);Kbad=expm((-1j*(H[0]+H[1]+.7*init+aux)-loss/2)*.7)
qready=P[0]@P[1];bad=max(norm_comm(Kbad@qready,embed(p,[4])) for p in [X,Z])
assert bad>1e-3
# Exact shutoff source: every retained coefficient commutes ALL DATA operators.
finalerr=max(norm_comm(K3,embed(p,[s])) for s in range(2,6) for p in [X,Z])
assert finalerr<1e-11
out={'dimension':D,'DATA_qubits':4,'retained_bath_qubits':1,'nominal_source_module_checks':checks,'one_local_controller_bath_activation_outside_enlarged_support_error':outside3,'one_controller_insertion_does_reach_new_owner_DATA':new_data2,'restoring_initiation_breaks_empty_mask_support':bad,'fully_shutoff_nominal_DATA_identity_error':finalerr,'scope':'Full-matrix coherent support/activation regression on an abstract owner fixture satisfying the proved native alphabet contracts; not an autonomous native apparatus, threshold, detector, or classical-readout simulation.'}
Path(__file__).with_name('coherent_support_module_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
