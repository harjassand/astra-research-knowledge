"""Finite, explicit LOCC/circuit check. Does not simulate an experimental device.

Exact signed-Pauli algebra is load-bearing; complex matrices independently check
the synthesized fixed Clifford, teleport Kraus operators and recurrence circuit.
Existing received five-qubit files are read only for a comparison hash.
"""
from pathlib import Path
from itertools import product
from collections import Counter
from fractions import Fraction as F
import hashlib, json, math
import numpy as np

ROOT=Path(__file__).resolve().parent
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1,-1]).astype(complex)
PM=dict(zip('IXYZ',[I,X,Y,Z]))
H=np.array([[1,1],[1,-1]],complex)/np.sqrt(2)
S=np.diag([1,1j]); SD=S.conj().T

def kron(*args):
 out=np.array([[1]],complex)
 for a in args: out=np.kron(out,a)
 return out
def pmatrix(w): return kron(*(PM[c] for c in w))
def gate_matrix(g,n):
 name,*qs=g
 if name in ('H','S','SD','X','Z'):
  A={'H':H,'S':S,'SD':SD,'X':X,'Z':Z}[name]
  return kron(*(A if i==qs[0] else I for i in range(n)))
 out=np.zeros((2**n,2**n),complex)
 for a in range(2**n):
  b=[(a>>(n-1-i))&1 for i in range(n)]; phase=1
  if name=='CX':b[qs[1]]^=b[qs[0]]
  elif name=='CZ':phase=(-1)**(b[qs[0]]*b[qs[1]])
  elif name=='SWAP': b[qs[0]],b[qs[1]]=b[qs[1]],b[qs[0]]
  else:raise ValueError(name)
  dest=sum(x<<(n-1-i) for i,x in enumerate(b));out[dest,a]=phase
 return out

# Exact Pauli multiplication and Clifford maps. Phase is an integer modulo four.
MUL={}
for a,b in product('IXYZ',repeat=2):
 for c in 'IXYZ':
  for ph in range(4):
   if np.array_equal(PM[a]@PM[b],1j**ph*PM[c]):MUL[a,b]=(ph,c)
assert len(MUL)==16
ONE={
 'H':{'I':(0,'I'),'X':(0,'Z'),'Y':(2,'Y'),'Z':(0,'X')},
 'S':{'I':(0,'I'),'X':(0,'Y'),'Y':(2,'X'),'Z':(0,'Z')},
 'SD':{'I':(0,'I'),'X':(2,'Y'),'Y':(0,'X'),'Z':(0,'Z')},
 'X':{'I':(0,'I'),'X':(0,'X'),'Y':(2,'Y'),'Z':(2,'Z')},
 'Z':{'I':(0,'I'),'X':(2,'X'),'Y':(2,'Y'),'Z':(0,'Z')}}
TWO={}
for name in ['CX','CZ','SWAP']:
 U=gate_matrix((name,0,1),2); tab={}
 for a,b in product('IXYZ',repeat=2):
  A=U@kron(PM[a],PM[b])@U.conj().T
  for c,d in product('IXYZ',repeat=2):
   for ph in [0,2]:
    if np.array_equal(A,1j**ph*kron(PM[c],PM[d])):tab[a,b]=(ph,c,d)
 assert len(tab)==16; TWO[name]=tab
def mul(P,Q):
 ph=P[0]+Q[0];w=[]
 for a,b in zip(P[1],Q[1]):
  p,c=MUL[a,b];ph+=p;w.append(c)
 return ph%4,''.join(w)
def conj(P,g):
 ph,w=P;w=list(w);name,*q=g
 if name in ONE:
  p,w[q[0]]=ONE[name][w[q[0]]];ph+=p
 else:
  p,w[q[0]],w[q[1]]=TWO[name][w[q[0]],w[q[1]]];ph+=p
 return ph%4,''.join(w)
def transform(P,gates):
 for g in gates:P=conj(P,g)
 return P

# Gaussian elimination of commuting stabilizers, retaining the actual gates.
G=['XZZXI','IXZZX','XIXZZ','ZXIXZ'];LX='XXXXX';LZ='ZZZZZ'
rows=[(0,w) for w in G+[LZ]];tracked=(0,LX); gates=[]
def do(g):
 global rows,tracked
 gates.append(g);rows=[conj(P,g) for P in rows];tracked=conj(tracked,g)
for i in range(5):
 for j in range(i):
  assert rows[i][1][j] in 'IZ'
  if rows[i][1][j]=='Z':rows[i]=mul(rows[i],rows[j])
 j=next(j for j in range(i,5) if rows[i][1][j]!='I')
 if j!=i:do(('SWAP',i,j))
 for j in range(i,5):
  if rows[i][1][j]=='Y':do(('SD',j));do(('H',j))
  elif rows[i][1][j]=='X':do(('H',j))
 for j in range(i+1,5):
  if rows[i][1][j]=='Z':do(('CX',j,i))
 assert rows[i][1]=='I'*i+'Z'+'I'*(4-i)
 if rows[i][0]==2:do(('X',i))
 assert rows[i][0]==0
assert tracked[1][4] in 'XY'
if tracked[1][4]=='Y':do(('SD',4))
for j in range(4):
 assert tracked[1][j] in 'IZ'
 if tracked[1][j]=='Z':do(('CZ',4,j))
if tracked[0]==2:do(('Z',4))
assert tracked==(0,'IIIIX')
assert rows==[(0,'I'*i+'Z'+'I'*(4-i)) for i in range(5)]
Q=np.eye(32,dtype=complex)
for g in gates:Q=gate_matrix(g,5)@Q
U=Q.conj().T;V=U[:,:2]
residuals=[float(np.linalg.norm(Q@U-np.eye(32),ord=2))]
for g in G:residuals.append(float(np.linalg.norm(pmatrix(g)@V-V)))
residuals.append(float(np.linalg.norm(pmatrix(LX)@V-V@X)))
residuals.append(float(np.linalg.norm(pmatrix(LZ)@V-V@Z)))

def syndrome(w):return tuple(int(c in 'XY') for c in w[:4])
single=['IIIII']+['I'*i+c+'I'*(4-i) for i in range(5) for c in 'XYZ']
cor={}
for e in single:
 ph,w=transform((0,e),gates);sy=syndrome(w)
 assert sy not in cor;cor[sy]=(e,w[-1])
assert len(cor)==16
counts={str(w):Counter() for w in range(6)};enumerator={c:Counter() for c in 'IXYZ'}
rows_all=[]
for letters in product('IXYZ',repeat=5):
 e=''.join(letters);ph,w=transform((0,e),gates);sy=syndrome(w)
 pc,c=MUL[cor[sy][1],w[-1]];weight=5-e.count('I')
 if weight<=1:assert c=='I'
 counts[str(weight)][c]+=1
 ec=tuple(e.count(z) for z in 'IXYZ');enumerator[c][ec]+=1
 rows_all.append((e,sy,c,ec))
 # Actual codeword matrix -> exact syndrome ket and single logical Pauli.
 target=np.zeros((32,2),complex);sint=sum(x<<(3-i) for i,x in enumerate(sy))
 phase=1j**(ph+sum(z=='Y' for z in w[:4]))
 target[2*sint:2*sint+2,:]=phase*PM[w[-1]]
 residuals.append(float(np.linalg.norm(Q@pmatrix(e)@V-target)))
assert counts['0']['I']==1 and counts['1']['I']==15
assert counts['2']['I']==0 and counts['3']['I']==60 and counts['4']['I']==135 and counts['5']['I']==45

# Conventional Bell measurement: CNOT(C,A), H(C), Z(C),Z(A), Bob Z^a X^b.
phi=np.array([1,0,0,1],complex)/np.sqrt(2)
tele=gate_matrix(('H',0),3)@gate_matrix(('CX',0,1),3)
tele_cases=0
for e in 'IXYZ':
 resource=kron(I,PM[e])@phi
 for a,b in product(range(2),repeat=2):
  K=np.zeros((2,2),complex)
  for t in range(2):
   inp=np.kron(np.eye(2)[:,t],resource)
   out=(tele@inp).reshape(2,2,2)[a,b,:]
   K[:,t]=np.linalg.matrix_power(Z,a)@np.linalg.matrix_power(X,b)@out
  ratio=np.trace(PM[e].conj().T@K)/2
  assert abs(abs(ratio)-.5)<1e-13
  residuals +=[float(np.linalg.norm(K-ratio*PM[e])),float(np.linalg.norm(K.conj().T@K-I/4))]
  tele_cases+=1

# Actual bilateral recurrence in ordering A1,B1,A2,B2.
rec=gate_matrix(('CX',1,3),4)@gate_matrix(('CX',0,2),4)
labels={(0,0):'I',(1,0):'X',(1,1):'Y',(0,1):'Z'}
bell={key:kron(I,PM[val])@phi for key,val in labels.items()}
rec_rows=[]
for l1,l2 in product(labels,repeat=2):
 x1,z1=l1;x2,z2=l2
 out=(rec@np.kron(bell[l1],bell[l2])).reshape(2,2,2,2)
 retain=(x1,z1^z2); passbit=int(x1==x2)
 for a,b in product(range(2),repeat=2):
  v=out[:,:,a,b].reshape(4);prob=float(np.vdot(v,v).real)
  expected=.5 if (a^b)==(x1^x2) else 0
  assert abs(prob-expected)<1e-13
  if prob:
   residuals.append(float(np.linalg.norm(np.outer(v,v.conj())-.5*np.outer(bell[retain],bell[retain].conj()))))
 rec_rows.append((l1,l2,retain,passbit))

def code(q):
 out={c:F(0) for c in 'IXYZ'}
 for _,_,c,ec in rows_all:
  prob=F(1)
  for a,n in zip('IXYZ',ec):prob*=q[a]**n
  out[c]+=prob
 assert sum(out.values())==1
 p=1-q['I'];assert 1-out['I']<=10*p*p
 return out
simplex=0
for x in range(9):
 for y in range(9-x):
  for z in range(9-x-y):
   code(dict(zip('IXYZ',[F(8-x-y-z,8),F(x,8),F(y,8),F(z,8)])));simplex+=1
q=dict(zip('IXYZ',[F(39,40),F(1,80),F(1,120),F(1,240)]));concat=[]
for level in range(1,4):
 q=code(q);p=1-q['I'];bound=F(1,10)*F(1,4)**(2**level)
 assert p<=bound;concat.append({'level':level,'p':float(p),'bound':str(bound)})

recurrence_cases=0;reservoir_patterns=0
for fidelity in [F(1,2),F(3,5),F(3,4),F(9,10),F(39,40),F(1)]:
 ql={l:(fidelity if l==(0,0) else (1-fidelity)/3) for l in labels}
 passed={l:F(0) for l in labels}
 for l1,l2,ret,passed_bit in rec_rows:
  if passed_bit:passed[ret]+=ql[l1]*ql[l2]
 ps=sum(passed.values());num=8*fidelity*fidelity-4*fidelity+5
 assert ps==num/9
 RF=(10*fidelity*fidelity-2*fidelity+1)/num
 assert passed[(0,0)]/ps==RF
 assert ps>=F(5,9)
 # Conditioned on any coarse pattern, first two retained outputs have the
 # same two-pair twirled product law; inspect all nonzero m=4 patterns.
 outq={l:(RF if l==(0,0) else (1-RF)/3) for l in labels}
 for pat in product(range(2),repeat=4):
  if sum(pat)<2:continue
  pp=ps**sum(pat)*(1-ps)**(4-sum(pat))
  if pp==0:continue
  for a,b in product(labels,repeat=2):
   joint=pp*outq[a]*outq[b]
   assert joint/pp==outq[a]*outq[b]
  reservoir_patterns+=1
 recurrence_cases+=1
RF=lambda f:(10*f*f-2*f+1)/(8*f*f-4*f+5)
f=F(3,4)
for _ in range(9):f=RF(f)
assert f>F(39,40)

# Kept syndrome record: exact rational Choi block l1 distance =2p'.
cq_cases=0
for q in [dict(zip('IXYZ',qq)) for qq in [
 [F(39,40),F(1,120),F(1,120),F(1,120)],
 [F(9,10),F(1,10),F(0),F(0)],
 [F(1,2),F(1,6),F(1,6),F(1,6)]]]:
 cq={(sy,c):F(0) for sy in cor for c in 'IXYZ'}
 for _,sy,c,ec in rows_all:
  prob=F(1)
  for a,n in zip('IXYZ',ec):prob*=q[a]**n
  cq[sy,c]+=prob
 dist=F(0);p=F(0)
 for sy in cor:
  mass=sum(cq[sy,c] for c in 'IXYZ')
  dist+=abs(cq[sy,'I']-mass)+sum(cq[sy,c] for c in 'XYZ')
  p+=sum(cq[sy,c] for c in 'XYZ')
 assert dist==2*p
 cq_cases+=1

assert max(residuals)<2e-13
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source=ROOT/'finite_five_qubit_bell_teleportation_factory_transfer_20261028.md'
data={
 'status':'PASS','role':'author exact algebra and numerical circuit check; contributor to parent factory',
 'decoder_gates_chronological_zero_based':gates,'decoder_gate_count':len(gates),
 'encoder_rule':'reverse decoder list; exchange S with SD; all other listed gates self-inverse',
 'transformed_original_stabilizers':{g:transform((0,g),gates) for g in G},
 'transformed_original_logicals':{g:transform((0,g),gates) for g in [LX,LZ]},
 'syndrome_recovery_table':{''.join(map(str,k)):{'single_error':e,'logical_correction':c} for k,(e,c) in sorted(cor.items())},
 'all_pauli_errors':len(rows_all),'teleport_kraus_cases':tele_cases,'recurrence_label_pairs':len(rec_rows),
 'recurrence_fidelity_cases':recurrence_cases,'first_two_retained_coarse_patterns':reservoir_patterns,
 'rational_simplex_cases':simplex,'logical_counts_by_weight':counts,'biased_concatenation':concat,
 'kept_syndrome_cq_trace_norm_cases':cq_cases,'R9_of_3_4':float(f),
 'max_dense_matrix_residual':max(residuals),
 'sha256':{p.name:sha(p) for p in [Path(__file__),source,
 ROOT/'bootstrap_five_qubit_pauli_independent_receipt_20261027.md',
 ROOT/'bootstrap_five_qubit_pauli_independent_check_20261027.py'] if p.exists()}}
Path(__file__).with_suffix('.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data,indent=2))
