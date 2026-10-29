"""Actual h5 inner code + received GF32 outer encoder/total syndrome decoder."""
import sys,json,random
from pathlib import Path
import numpy as np
from construct_inner import transform
ROOT=Path(__file__).parent
Q=Path('producer-workspace/quantum_operational_certification_20261024')
sys.path.insert(0,str(Q/'outer_grs_distillation_20261028'))
sys.path.insert(0,str(Q/'compiled_payload_outer_bridge_20261029'))
from direct_outer_checks_v1 import outer_encoder,zbits
from grs_wrapper_v1 import GF,construct,decoded_error,decode_syndrome
from check_field_and_gates_v1 import first_field
from received_algebra_compiler_v1 import gate_rows
inner=json.loads((ROOT/'inner_h5.json').read_text());h=5;ell=80;B=32;tout=4;rin=2;tglobal=tout*(rin+1);N=ell*B
mod,_=first_field(h);g=GF(h,mod);c=construct(g,B,tout);enc,gram=outer_encoder(g,c);dec=list(reversed(enc));ng=B*h
labels=np.eye(2*ng,dtype=np.uint8)
for gate in enc+dec:gate_rows(labels,gate,ng)
assert np.array_equal(labels,np.eye(2*ng,dtype=np.uint8))
fmap={sum(v<<j for j,v in enumerate(zbits(g,f))):f for f in range(g.q)}
gates=inner['decoder_gates'];table=inner['syndrome_table'];rng=random.Random(53455);cases=[]
for trial in range(100):
 # Include exact concentrated bad-inner boundary, arbitrary sparse patterns, and all-good inner blocks.
 if trial%3==0:
  blocks=rng.sample(range(B),tout);positions=[bl*ell+j for bl in blocks for j in rng.sample(range(ell),rin+1)]
 elif trial%3==1:positions=rng.sample(range(N),rng.randrange(tglobal+1))
 else:
  blocks=rng.sample(range(B),tglobal//rin);positions=[bl*ell+j for bl in blocks for j in rng.sample(range(ell),rin)]
 phys=[0]*B
 for j in positions:
  bl,site=divmod(j,ell);p=rng.randrange(1,4)
  phys[bl]^=((p&1)<<site)|(((p>>1)&1)<<(ell+site))
 e=[];f=[];bad=0
 for v in phys:
  mapped,phase=transform(v,(v&(v>>ell)).bit_count()%4,gates,ell)
  sy=mapped&((1<<(ell-h))-1)
  logical=((mapped&((1<<ell)-1))>>(ell-h))|((mapped>>(2*ell-h))<<h)
  logical^=table.get(str(sy),{'logical':0})['logical']
  if logical:bad+=1
  e.append(logical&31);f.append(fmap[logical>>h])
 assert bad<=tout
 dx,dz=decoded_error(g,c,e,f);ss=c['s'];kk=c['ell'];sx=dx[:ss];last=dx[ss+kk:];se=[g.dot(row,last) for row in c['HRt']]
 eh,ok1=decode_syndrome(g,c,se);fh,ok2=decode_syndrome(g,c,sx);assert ok1 and ok2
 cx,cz=decoded_error(g,c,eh,fh)
 assert all(dx[i]==cx[i] and dz[i]==cz[i] for i in range(ss,ss+kk))
 physical=np.array([[(e[i]>>j)&1 for i in range(B) for j in range(h)]+[bit for z in f for bit in zbits(g,z)]],dtype=np.uint8)
 logical=np.zeros((1,2*ng),dtype=np.uint8)
 for i in range(ss*h,(ss+kk)*h):logical[0,i]=rng.randrange(2);logical[0,ng+i]=rng.randrange(2)
 propagated=logical.copy()
 for gate in enc:gate_rows(propagated,gate,ng)
 propagated^=physical
 for gate in dec:gate_rows(propagated,gate,ng)
 correction=np.array([[(cx[i]>>j)&1 for i in range(B) for j in range(h)]+[bit for z in cz for bit in zbits(g,z)]],dtype=np.uint8)
 propagated^=correction;keep=list(range(ss*h,(ss+kk)*h))+list(range(ng+ss*h,ng+(ss+kk)*h))
 assert np.array_equal(propagated[:,keep],logical[:,keep])
 cases.append({'native_fault_count':len(positions),'residual_bad_inner_blocks':bad})
res={'scope':'Exact GF2/finite-field actual concatenated Pauli propagation, not large dense quantum-state simulation. Coherent errors justified by QEC-span theorem separately.','inner':'inner_h5.json','outer_field_modulus':mod,'outer_length':B,'outer_corrects':tout,'native_service_slots':N,'native_fault_radius':tglobal,'payload_qubits':h*(B-4*tout),'outer_encoder_gate_count':len(enc),'inner_decoder_gate_count':len(gates),'trials':len(cases),'arbitrary_logical_paulis_preserved':True,'cases':cases}
(ROOT/'concatenated_results.json').write_text(json.dumps(res,indent=2)+'\n')
(ROOT/'outer_h5_circuit.json').write_text(json.dumps({'encoder':enc,'inverse_decoder':dec,'trace_gram':gram,'field_modulus':mod},indent=2)+'\n')
print(json.dumps({k:v for k,v in res.items() if k!='cases'},indent=2))
