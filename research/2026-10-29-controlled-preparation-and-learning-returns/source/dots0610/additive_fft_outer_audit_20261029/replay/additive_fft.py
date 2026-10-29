"""Exact additive FFT over degree-filtered subspace-polynomial basis.
Known classical transform, compiled to an explicit ancilla-free binary CNOT circuit.
"""
import numpy as np, json,random,hashlib,importlib.util
from pathlib import Path
from received_grs_wrapper_v1 import GF,one_way_correction,decoded_error
HERE=Path(__file__).parent
class Compiler:
 def __init__(self,h,mod):
  self.h=h;self.g=GF(h,mod);self.q=1<<h;g=self.g
  sv=list(range(self.q));self.t=[]
  for j in range(h):
   c=sv[1<<j];assert c;ci=g.inv(c);self.t.append([g.mul(v,ci) for v in sv]);sv=[g.mul(v,v)^g.mul(c,v) for v in sv]
  self.field=[];self.butterflies=0
  def visit(j,start,alpha):
   if j<0:return
   half=1<<j;c=self.t[j][alpha]
   for i in range(half):
    a=start+i;b=start+half+i
    if c:self.field.append((b,a,c))
    self.field.append((a,b,1));self.butterflies+=1
   visit(j-1,start,alpha);visit(j-1,start+half,alpha^(1<<j))
  visit(h-1,0,0);self.bits=[]
  for src,dst,c in self.field:
   for j in range(h):
    out=g.mul(c,1<<j)
    for k in range(h):
     if (out>>k)&1:self.bits.append((src*h+j,dst*h+k))
  assert self.butterflies==self.q*h//2
  assert len(self.bits)<=self.q*h*h*(h+1)//2
 def apply(self,x,inverse=False):
  x=list(x)
  for src,dst,c in reversed(self.field) if inverse else self.field:x[dst]^=self.g.mul(c,x[src])
  return x
 def apply_bits(self,x,inverse=False):
  v=[(a>>j)&1 for a in x for j in range(self.h)]
  for src,dst in reversed(self.bits) if inverse else self.bits:v[dst]^=v[src]
  return [sum(v[i*self.h+j]<<j for j in range(self.h)) for i in range(self.q)]
 def basis_at(self,x):
  v=[1]*self.q
  for j in range(self.h):
   for i in range(1<<j):v[i+(1<<j)]=self.g.mul(v[i],self.t[j][x])
  return v
 def direct(self,c,x):return self.g.dot(c,self.basis_at(x))
 def matrix(self):return [list(r) for r in zip(*(self.basis_at(x) for x in range(self.q)))]
 def inverse_matrix(self):return [self.apply([int(i==j) for j in range(self.q)],True) for i in range(self.q)]
 def code(self,t):
  g=self.g;B=self.q;assert 4*t<B;s=2*t;r=B-s;ell=B-4*t;T=self.matrix();Ti=self.inverse_matrix();C=T[:r];H=T[:s];R=T[r:]
  assert g.mm(T,Ti)==g.eye(B)
  assert all(not any(row) for row in g.mm(H,g.transpose(C)))
  HRt=g.mm(H,g.transpose(R));assert len(g.solve(HRt,[0]*s)[1])==s
  return {'B':B,'t':t,'s':s,'r':r,'ell':ell,'a':list(range(B)),'v':[1]*B,'C':C,'H':H,'L':T[s:r],'R':R,'T':T,'Ti':Ti,'HRt':HRt}
 def phasebits(self,a):return [self.g.trace(self.g.mul(a,1<<j)) for j in range(self.h)]
 def phasefield(self,bits):
  # Exact classical trace-dual decoding, not an extra quantum Fourier-basis circuit.
  return next(a for a in range(self.q) if self.phasebits(a)==bits)
 def decode_bit_paulis(self,e,f):
  x=[(a>>j)&1 for a in e for j in range(self.h)];z=[b for a in f for b in self.phasebits(a)]
  for c,t in reversed(self.bits):x[t]^=x[c];z[c]^=z[t]
  ex=[sum(x[i*self.h+j]<<j for j in range(self.h)) for i in range(self.q)];fz=[self.phasefield(z[i*self.h:(i+1)*self.h]) for i in range(self.q)]
  return ex,fz

def main():
 rng=random.Random(202610290437);mods={3:0b1011,4:0b10011}
 for r in json.load(open(HERE/'field_certificates_received.json')):mods[r['h']]=r['irreducible_polynomial_integer']
 rows=[]
 for h in [3,4,5,6,8,11]:
  c=Compiler(h,mods[h]);g=c.g;B=c.q
  for x in range(1,B):assert g.mul(x,g.inv(x))==1
  checks=0
  for case in range(3):
   x=[rng.randrange(B) for _ in range(B)];y=c.apply(x);assert c.apply(y,True)==x;assert c.apply_bits(x)==y;assert c.apply_bits(y,True)==x
   points=list(range(B)) if h<=6 else rng.sample(range(B),64)
   for pt in points:assert y[pt]==c.direct(x,pt);checks+=1
  matrix_checks=0
  if h<=5:
   T=c.matrix()
   for i in range(B):assert c.apply([int(j==i) for j in range(B)])==T[i];matrix_checks+=1
  np.savez_compressed(HERE/f'circuit_h{h}.npz',field_additions=np.array(c.field,dtype=np.uint16),cnots=np.array(c.bits,dtype=np.uint16),h=h,mod=mods[h])
  rows.append({'h':h,'B':B,'mod':mods[h],'buffer_qubits':B*h,'butterflies':c.butterflies,'field_addition_gates':len(c.field),'actual_CNOT_count_one_transform':len(c.bits),'proved_CNOT_upper_bound_one_transform':B*h*h*(h+1)//2,'direct_polynomial_point_checks':checks,'all_basis_vector_matrix_checks':matrix_checks,'random_forward_inverse_CNOT_checks':3})
 tests=[]
 for h,t in [(3,1),(4,1),(4,3),(5,2),(5,5)]:
  c=Compiler(h,mods[h]);g=c.g;B=c.q;code=c.code(t);cases=[]
  # All single-coordinate nonzero X and Z values, plus truly mixed multi-symbol cases.
  for pos in range(B):
   for val in range(1,B):
    e=[0]*B;f=[0]*B;e[pos]=val;cases.append((e,f));e=[0]*B;f=[0]*B;f[pos]=val;cases.append((e,f))
  # Bound decoding tests on larger fields, retaining deterministic spread and random cases.
  if h>=4:cases=rng.sample(cases,64)
  for w in [0,1,t]:
   for repeat in range(12):
    e=[0]*B;f=[0]*B
    for pos in rng.sample(range(B),w):e[pos]=rng.randrange(1,B);f[pos]=rng.randrange(1,B)
    cases.append((e,f))
  for e,f in cases:
   ep,fp=c.decode_bit_paulis(e,f);assert ep==g.rowmul(e,code['Ti']) and fp==g.rowmul(f,g.transpose(code['T']))
   # Decode circuit readout: H on first s converts phase bits to Z-readout;
   # trace-dual conversion returns fp[:s], last computational readout is ep[-s:].
   sf=fp[:2*t];dz=ep[-2*t:];se=[g.dot(row,dz) for row in code['HRt']]
   assert sf==[g.dot(row,f) for row in code['H']];assert se==[g.dot(row,e) for row in code['H']]
   x,z,ok=one_way_correction(g,code,e,f);assert ok and not any(x) and not any(z)
  tests.append({'h':h,'B':B,'t':t,'payload_field_symbols':B-4*t,'tested_correctable_Pauli_patterns':len(cases),'exact_binary_CNOT_field_label_and_syndrome_checks':len(cases)})
 out={'seed':202610290437,'status':'new explicit additive-FFT CSS compiler pending independent review','transform_cases':rows,'CSS_total_decoder_tests':tests,'scope':'Exact finite-field/CNOT/Pauli propagation, not noisy hardware or dense logical quantum amplitudes. B=q differs from old B=q-1 optimization grid. Known additiveFFT used, not claimed novel.'};(HERE/'compiler_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
