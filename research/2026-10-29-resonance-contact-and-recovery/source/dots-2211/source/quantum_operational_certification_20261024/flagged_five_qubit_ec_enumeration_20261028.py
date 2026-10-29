"""Known Chao-Reichardt-style two-ancilla five-qubit EC, exact Pauli enumeration.
Native parity-P measurement gates and flag CNOTs are 2-qubit locations.
No stochastic shots, threshold estimate, or arbitrary classical processor faults.
"""
from itertools import product
from pathlib import Path
import json
P={'I':(0,0),'X':(1,0),'Y':(1,1),'Z':(0,1)};rev={v:k for k,v in P.items()}
def vec(w):return tuple(P[c][0] for c in w)+tuple(P[c][1] for c in w)
def add(a,b):return tuple(x^y for x,y in zip(a,b))
def sp(a,b):return sum(a[i]*b[i+5]+a[i+5]*b[i] for i in range(5))%2
G=list(map(vec,['XZZXI','IXZZX','XIXZZ','ZXIXZ']));syn=lambda e:tuple(sp(e,g) for g in G)
S={vec('IIIII')}
for g in G:S|={add(x,g) for x in list(S)}
def weight(e):return sum(bool(e[i] or e[i+5]) for i in range(5))
def reduced_weight(e):return min(weight(add(e,g)) for g in S)
def word(e):return ''.join(rev[e[i],e[i+5]] for i in range(5))
zero=vec('IIIII');standard={syn(zero):zero};inputs=[zero]
for i in range(5):
 for c in 'XYZ':
  e=vec('I'*i+c+'I'*(4-i));standard[syn(e)]=e;inputs.append(e)
def gates(g):
 sites=[(g+k)%5 for k in range(4)];letters='XZZX'
 return [('parity',sites[0],5,letters[0]),('cnot',6,5,'Z'),('parity',sites[1],5,letters[1]),('parity',sites[2],5,letters[2]),('cnot',6,5,'Z'),('parity',sites[3],5,letters[3])]
def inject(x,z,q,c):x[q]^=P[c][0];z[q]^=P[c][1]
def cnot(x,z,c,t):x[t]^=x[c];z[c]^=z[t]
def propagate(x,z,gate):
 typ,c,t,p=gate
 if typ=='parity' and p=='X':x[c],z[c]=z[c],x[c]
 cnot(x,z,c,t)
 if typ=='parity' and p=='X':x[c],z[c]=z[c],x[c]
def faults(g):
 fs=[]
 for a in [5,6]:
  for p in 'XYZ':fs.append(('prep',a,p))
 for b in range(7):
  for a in range(7):
   for p in 'XYZ':fs.append(('idle',b,a,p))
 for k,gate in enumerate(gates(g)):
  for p,q in product('IXYZ',repeat=2):
   if p+q!='II':fs.append(('gate',k,p,q))
 for a in ['syndrome','flag']:fs.append(('readout_flip',a))
 return fs
def measure(g,data,fault=None):
 x=list(data[:5])+[0,0];z=list(data[5:])+[0,0]
 if fault and fault[0]=='prep':inject(x,z,fault[1],fault[2])
 for k in range(7):
  if fault and fault[0]=='idle' and fault[1]==k:inject(x,z,fault[2],fault[3])
  if k==6:break
  gate=gates(g)[k];propagate(x,z,gate)
  if fault and fault[0]=='gate' and fault[1]==k:
   inject(x,z,gate[1],fault[2]);inject(x,z,gate[2],fault[3])
 syndrome=x[5];flag=z[6]
 if fault and fault[0]=='readout_flip':
  if fault[1]=='syndrome':syndrome^=1
  else:flag^=1
 return tuple(x[:5]+z[:5]),syndrome,flag
# Build flag tables from all admitted single faults; certify syndrome uniqueness modulo stabilizer.
tables=[];table_rows=[]
for g in range(4):
 t={};examples={}
 for f in faults(g):
  e,s,fl=measure(g,zero,f)
  if fl:
   sy=syn(e)
   if sy in t:assert add(e,t[sy]) in S,(g,f,word(e),word(t[sy]))
   else:t[sy]=e;examples[sy]=f
 assert len(t)==8,(g,len(t))
 tables.append(t);table_rows.append({''.join(map(str,k)):word(v) for k,v in sorted(t.items())})
def plain_syndromes(data):
 outcomes=[];e=data
 for g in range(4):
  x=list(e[:5])+[0,0];z=list(e[5:])+[0,0]
  for gate in gates(g):
   if gate[0]=='parity':propagate(x,z,gate)
  outcomes.append(x[5]);e=tuple(x[:5]+z[:5])
 assert e==data and tuple(outcomes)==syn(data)
 return e,tuple(outcomes)
def run(data,fault_round=None,fault=None):
 transcript=[];e=data;couplings=0;preps=0;reads=0
 for g in range(4):
  e,s,f=measure(g,e,fault if fault_round==g else None);couplings+=6;preps+=2;reads+=2;transcript.append([g,s,f])
  if f or s:
   e,sy=plain_syndromes(e);couplings+=16;preps+=4;reads+=4
   correction=tables[g][sy] if f else standard[sy]
   e=add(e,correction)
   return e,transcript,{'two_qubit_couplings':couplings,'ancilla_preparations':preps,'ancilla_readouts':reads,'correction_word':word(correction),'repeat_syndrome':sy}
 return e,transcript,{'two_qubit_couplings':couplings,'ancilla_preparations':preps,'ancilla_readouts':reads,'correction_word':'IIIII'}
# Proper1-EC: zero faults corrects everyweight<=1 input; cleaninput+onefault leavesweight<=1modstabilizer.
input_checks=[]
for e in inputs:
 out,tr,res=run(e);assert reduced_weight(out)==0,(word(e),word(out));input_checks.append(word(e))
count=0;maxweight=0;maxg=0;remainders={};records=[]
for g in range(4):
 for fault in faults(g):
  out,tr,res=run(zero,g,fault);rw=reduced_weight(out);assert rw<=1,(g,fault,word(out));count+=1;maxweight=max(maxweight,rw);maxg=max(maxg,res['two_qubit_couplings']);remainders[rw]=remainders.get(rw,0)+1
  records.append({'round':g,'fault':fault,'residual':word(out),'min_weight_mod_stabilizer':rw,'transcript':tr,'resources':res})
# A physical single-qubit correction-pulse error is also locally correctable after clean no-fault protocol.
for i in range(5):
 for p in 'XYZ':assert reduced_weight(vec('I'*i+p+'I'*(4-i)))==1
# Arbitrary global classical misdispatch is explicitly NOT covered: logicalXXXXX is weight3modstabilizer.
assert reduced_weight(vec('XXXXX'))==3
out={'status':'PASS_EXACT_KNOWN_FLAGGED_1EC_ENUMERATION','source_draws':0,'primary':'Chao-Reichardt arXiv1705.02329v1 SectionII/Fig2; cyclic stabilizer ordering','flag_tables':table_rows,'fault_free_input_checks':input_checks,'single_fault_cases':count,'fault_model_counts_per_flagged_circuit':{'ancilla_preparation_Paulis':6,'all_qubit_boundary_idle_Paulis':147,'two_qubit_gate_Paulis':90,'readout_bit_flips':2},'residual_minweight_counts':remainders,'maximum_residual_weight_mod_stabilizer':maxweight,'maximum_executed_twoqubit_couplings':maxg,'max_ancilla_preparations_and_readouts_each':12,'physical_qubits':7,'classical_control_contract':'Reliable table/branch logic; readout-bit faults included. Arbitrary global correction-word misdispatch is not a local quantum fault and can cause logicalerror. Correction pulse errors are single-qubit locations; on clean singlefaultpaths correctivebranch already requires thefault, so a secondfaultthere is outside1EC premise.','scope':'Correctable residual, not exactcodespace output after fault; no exRec threshold or repeated-storage rate inferred.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');Path(__file__).with_name('flagged_five_qubit_ec_all_fault_records_20261028.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps(out,indent=2))
