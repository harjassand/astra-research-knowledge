import itertools,json
from pathlib import Path
from fractions import Fraction as F
G=['XZZXI','IXZZX','XIXZZ','ZXIXZ'];P={'I':(0,0),'X':(1,0),'Y':(1,1),'Z':(0,1)}
def vec(word):return tuple(P[p][0] for p in word)+tuple(P[p][1] for p in word)
def add(a,b):return tuple(x^y for x,y in zip(a,b))
def symp(a,b):return sum(a[i]*b[5+i]+a[5+i]*b[i] for i in range(5))%2
gs=list(map(vec,G));zero=(0,)*10;stab={zero}
for g in gs:stab|={add(x,g) for x in list(stab)}
assert len(stab)==16 and all(symp(a,b)==0 for a in gs for b in gs)
LX=vec('XXXXX');LZ=vec('ZZZZZ');lookup={(0,)*4:zero}
for i in range(5):
 for letter in 'XYZ':
  w=['I']*5;w[i]=letter;e=vec(w);syn=tuple(symp(e,g) for g in gs);assert syn not in lookup;lookup[syn]=e
assert len(lookup)==16
rows={k:{'total':0,'logical_identity':0,'logical_nonidentity':0} for k in range(6)}
for word in itertools.product('IXYZ',repeat=5):
 e=vec(word);weight=sum(p!='I' for p in word);syn=tuple(symp(e,g) for g in gs);rem=add(e,lookup[syn]);assert all(symp(rem,g)==0 for g in gs)
 logical=(symp(rem,LZ),symp(rem,LX));assert (logical==(0,0))==(rem in stab)
 bad=any(logical);rows[weight]['total']+=1;rows[weight]['logical_nonidentity' if bad else 'logical_identity']+=1
 if weight<=1:assert not bad
assert sum(r['total'] for r in rows.values())==1024
N=14397;examples=[]
for L in range(1,5):
 K=5**L;Pports=6*K*N;examples.append({'L':L,'service_calls':K,'error_bound_exact':str(F(1,10)**(2**L)/10),'noisy_Choi_ports':Pports,'protected_program_qubit_lower_bound':2*Pports})
assert F(3,N+3)==F(1,4800) and F(3,4)*F(1,100)+6*F(1,2400)==F(1,100)
result={'stabilizer_group_size':16,'code_dimension':2,'all_pauli_patterns':1024,'counts_by_weight':rows,'all_weight_0_or_1_corrected':True,'logical_Pauli_after_every_syndrome_correction':True,'example_gate_ports':N,'examples':examples,'scope':'Exact binary-symplectic conventional code check; no physical fault-tolerant gates'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
