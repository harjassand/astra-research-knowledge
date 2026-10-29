"""Actual binary Clifford direct CSS encoder/decoder + service-group typing checks."""
from pathlib import Path
import sys,json,random,numpy as np
Q=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Q/'outer_grs_distillation_20261028'))
sys.path.insert(0,str(Q/'learned_pauli_algebra_compiler_20261029'))
from grs_wrapper_v1 import GF,construct,decoded_error,decode_syndrome
from check_field_and_gates_v1 import first_field,binary_linear
from algebra_compiler_v1 import gate_rows

def layout(B,k0):
 h=max(1,(B-1).bit_length());u=max(1,(h+k0-1)//k0);s=u*k0//h
 return dict(B=B,k0=k0,h=h,u=u,stripes=s,J=u*B,active_per_group=s*h,padding_per_group=u*k0-s*h)
def outer_encoder(g,c):
 h=g.m;g2=GF(1,3);gram=[[g.trace(g.mul(1<<i,1<<j)) for j in range(h)] for i in range(h)];K=g2.inverse(gram)
 result=[]
 for symbol in range(c['s']):
  result.extend(('H',symbol*h+j) for j in range(h))
  result.extend(('SW' if kind=='SWAP' else kind,symbol*h+i,symbol*h+j) for kind,i,j in binary_linear(g2,K))
 result.extend(('SW' if kind=='SWAP' else kind,i,j) for kind,i,j in binary_linear(g,c['T']))
 return result,gram

def zbits(g,f):return [g.trace(g.mul(f,1<<j)) for j in range(g.m)]
def run():
 rng=random.Random(202610290058);records=[]
 for B,t,k0 in [(8,1,1),(9,2,2),(13,3,7),(16,2,9)]:
  typ=layout(B,k0);h=typ['h'];u=typ['u'];stripes=typ['stripes'];J=typ['J'];mod,_=first_field(h);g=GF(h,mod);c=construct(g,B,t)
  enc,gram=outer_encoder(g,c);dec=list(reversed(enc));N=B*h
  # Explicit inverse-circuit check overcompletebinaryPauli basis.
  labels=np.eye(2*N,dtype=np.uint8)
  for gate in enc+dec:gate_rows(labels,gate,N)
  assert np.array_equal(labels,np.eye(2*N,dtype=np.uint8))
  fmap={sum(bit<<j for j,bit in enumerate(zbits(g,f))):f for f in range(g.q)};assert len(fmap)==g.q
  total=0;logical_tests=0
  for trial in range(200):
   # Arbitrarycorrelatedbits acrossallstripes in atmostt serviceblocks.
   bad=rng.sample(range(J),rng.randrange(t+1));xb=[0]*(J*k0);zb=xb.copy()
   for service in bad:
    for j in range(k0):xb[service*k0+j]=rng.randrange(2);zb[service*k0+j]=rng.randrange(2)
   groups={service//u for service in bad};assert len(groups)<=t
   for stripe in range(stripes):
    e=[];f=[]
    for group in range(B):
     start=group*u*k0+stripe*h
     e.append(sum(xb[start+j]<<j for j in range(h)))
     f.append(fmap[sum(zb[start+j]<<j for j in range(h))])
    physical=np.array([[(e[i]>>j)&1 for i in range(B) for j in range(h)]+[bit for z in f for bit in zbits(g,z)]],dtype=np.uint8)
    # Verify actualbinaryClifford againstfieldPauli formulas.
    decoded=physical.copy()
    for gate in dec:gate_rows(decoded,gate,N)
    dx,dz=decoded_error(g,c,e,f)
    expected=np.array([[(dx[i]>>j)&1 for i in range(B) for j in range(h)]+[bit for z in dz for bit in zbits(g,z)]],dtype=np.uint8)
    assert np.array_equal(decoded,expected)
    # Measuredancillas arecomputational |0>; theirX labelsAREactualsyndromes.
    s=c['s'];ell=c['ell'];sx=dx[:s];last=dx[s+ell:]
    se=[g.dot(row,last) for row in c['HRt']]
    eh,ok1=decode_syndrome(g,c,se);fh,ok2=decode_syndrome(g,c,sx);assert ok1 and ok2
    cx,cz=decoded_error(g,c,eh,fh)
    assert all(dx[i]==cx[i] and dz[i]==cz[i] for i in range(s,s+ell))
    # Preserve arbitrarylogicalPaulis, not merelyone stabilizerinput.
    logical=np.zeros((1,2*N),dtype=np.uint8)
    for i in range(s*h,(s+ell)*h):logical[0,i]=rng.randrange(2);logical[0,N+i]=rng.randrange(2)
    propagated=logical.copy()
    for gate in enc:gate_rows(propagated,gate,N)
    propagated^=physical
    for gate in dec:gate_rows(propagated,gate,N)
    correction=np.array([[(cx[i]>>j)&1 for i in range(B) for j in range(h)]+[bit for z in cz for bit in zbits(g,z)]],dtype=np.uint8)
    propagated^=correction
    keep=list(range(s*h,(s+ell)*h))+list(range(N+s*h,N+(s+ell)*h))
    assert np.array_equal(propagated[:,keep],logical[:,keep]);total+=1;logical_tests+=1
  payload=stripes*h*(B-4*t)
  assert 2*stripes*h>=u*k0
  records.append(dict(**typ,t=t,payload_qubits=payload,outer_ancilla_qubits=stripes*h*4*t,field_modulus=mod,trace_gram=gram,binary_encoder_gates=enc,binary_decoder_gates=dec,binary_gate_count_per_stripe=len(enc),typed_correlated_error_checks=total,arbitrary_logical_Pauli_checks=logical_tests,all_indices_within_stripe=all(0<=j<N for gate in enc for j in gate[1:])))
 print(json.dumps(dict(seed=202610290058,status='PASS_EXACT_BINARY_CLIFFORD_AND_FINITE_FIELD',scope='DirectpayloadCSS circuits andtyping; no noisyhardwareorlargequantumstate simulation',cases=records),indent=2))
if __name__=='__main__':run()
