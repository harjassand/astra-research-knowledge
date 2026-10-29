#!/usr/bin/env python3
"""Exact GF(2^m) CSS/GRS construction and total Berlekamp-Welch decoder.
No oracle or floating finite-field arithmetic; tests use small certified fields.
"""
from pathlib import Path
import itertools,json,random,math
HERE=Path(__file__).parent
class GF:
 def __init__(self,m,mod):self.m=m;self.q=1<<m;self.mod=mod
 def mul(self,a,b):
  out=0
  while b:
   if b&1:out^=a
   b>>=1;a<<=1
   if a&self.q:a^=self.mod
  return out
 def pow(self,a,n):
  z=1
  while n:
   if n&1:z=self.mul(z,a)
   a=self.mul(a,a);n>>=1
  return z
 def inv(self,a):
  if not a:raise ZeroDivisionError
  return self.pow(a,self.q-2)
 def trace(self,a):
  z=0;x=a
  for _ in range(self.m):z^=x;x=self.mul(x,x)
  assert z in [0,1];return z
 def dot(self,a,b):
  z=0
  for x,y in zip(a,b):z^=self.mul(x,y)
  return z
 def eval(self,p,a):
  z=0
  for c in reversed(p):z=self.mul(z,a)^c
  return z
 def solve(self,A,b):
  if not A:return [],[]
  n=len(A[0]);Z=[row[:]+[v] for row,v in zip(A,b)];pivs=[];row=0
  for col in range(n):
   i=next((i for i in range(row,len(Z)) if Z[i][col]),None)
   if i is None:continue
   Z[row],Z[i]=Z[i],Z[row];a=self.inv(Z[row][col]);Z[row]=[self.mul(a,z) for z in Z[row]]
   for i in range(len(Z)):
    if i!=row and Z[i][col]:
     a=Z[i][col];Z[i]=[x^self.mul(a,y) for x,y in zip(Z[i],Z[row])]
   pivs.append(col);row+=1
   if row==len(Z):break
  if any(not any(z[:n]) and z[n] for z in Z):return None,pivs
  x=[0]*n
  for i,c in enumerate(pivs):x[c]=Z[i][n]
  return x,pivs
 def mm(self,A,B):return [[self.dot(row,col) for col in zip(*B)] for row in A]
 def rowmul(self,x,A):return [self.dot(x,col) for col in zip(*A)]
 def transpose(self,A):return list(map(list,zip(*A)))
 def eye(self,n):return [[int(i==j) for j in range(n)] for i in range(n)]
 def inverse(self,A):
  n=len(A);cols=[]
  for j in range(n):
   x,p=self.solve(A,[int(i==j) for i in range(n)]);assert len(p)==n;cols.append(x)
  return self.transpose(cols)
 def divide(self,Q,E):
  Q=Q[:]
  while Q and not Q[-1]:Q.pop()
  de=len(E)-1;out=[0]*max(1,len(Q)-de);lead=self.inv(E[-1])
  while len(Q)>de:
   j=len(Q)-1-de;a=self.mul(Q[-1],lead);out[j]=a
   for i,e in enumerate(E):Q[i+j]^=self.mul(a,e)
   while Q and not Q[-1]:Q.pop()
  return out,Q

def construct(g,B,t):
 assert 0<=4*t<B<=g.q
 s=2*t;r=B-s;ell=B-2*s;a=list(range(B));v=[]
 for i,x in enumerate(a):
  prod=1
  for j,y in enumerate(a):
   if i!=j:prod=g.mul(prod,x^y)
  w=g.inv(prod);z=g.pow(w,g.q//2);assert g.mul(z,z)==w;v.append(z)
 C=[[g.mul(v[i],g.pow(a[i],h)) for i in range(B)] for h in range(r)];H=C[:s];L=C[s:]
 _,pivs=g.solve(C,[0]*r);assert len(pivs)==r
 R=[[int(i==j) for i in range(B)] for j in range(B) if j not in pivs]
 T=H+L+R;Ti=g.inverse(T);A=g.mm(H,g.transpose(R)) if s else []
 assert len(R)==s and g.mm(T,Ti)==g.eye(B)
 if s:
  assert all(not any(row) for row in g.mm(H,g.transpose(C)))
  assert len(g.solve(A,[0]*s)[1])==s
 return {'B':B,'t':t,'s':s,'r':r,'ell':ell,'a':a,'v':v,'C':C,'H':H,'L':L,'R':R,'T':T,'Ti':Ti,'HRt':A}

def decode_word(g,c,y):
 B,t,r=c['B'],c['t'],c['r'];z=[g.mul(a,g.inv(b)) for a,b in zip(y,c['v'])]
 # Q has degree <r+t; E is monic of degree t.
 A=[];b=[]
 for a,w in zip(c['a'],z):
  A.append([g.pow(a,j) for j in range(r+t)]+[g.mul(w,g.pow(a,j)) for j in range(t)])
  b.append(g.mul(w,g.pow(a,t)))
 sol,_=g.solve(A,b)
 if sol is None:return None
 Q=sol[:r+t];E=sol[r+t:]+[1];f,rem=g.divide(Q,E)
 if rem or len(f)>r:return None
 word=[g.mul(v,g.eval(f,a)) for v,a in zip(c['v'],c['a'])]
 if sum(x!=y for x,y in zip(word,y))>t:return None
 if any(g.dot(h,word) for h in c['H']):return None
 return word

def decode_syndrome(g,c,synd):
 if c['s']==0:return [0]*c['B'],True
 y,_=g.solve(c['H'],synd);assert y is not None
 word=decode_word(g,c,y)
 if word is None:return [0]*c['B'],False
 e=[x^z for x,z in zip(y,word)]
 assert [g.dot(h,e) for h in c['H']]==synd
 return e,True

def field_linear_gates(g,T):
 # Column elimination: T E1 ... EL=I, so reverse inverse gates implement T.
 n=len(T);A=[r[:] for r in T];reduce=[]
 for j in range(n):
  k=next(k for k in range(j,n) if A[j][k])
  if k!=j:
   for row in A:row[j],row[k]=row[k],row[j]
   reduce.append(('swap',j,k,0))
  scale=g.inv(A[j][j])
  if scale!=1:
   for row in A:row[j]=g.mul(row[j],scale)
   reduce.append(('scale',j,0,scale))
  for k in range(n):
   if k!=j and A[j][k]:
    coeff=A[j][k]
    for row in A:row[k]^=g.mul(coeff,row[j])
    reduce.append(('add',j,k,coeff))
 assert A==g.eye(n)
 return [(kind,i,j,g.inv(a) if kind=='scale' else a) for kind,i,j,a in reversed(reduce)]
def apply_gates(g,x,gates):
 x=x[:]
 for kind,i,j,a in gates:
  if kind=='swap':x[i],x[j]=x[j],x[i]
  elif kind=='scale':x[i]=g.mul(x[i],a)
  else:x[j]^=g.mul(a,x[i])
 return x

def decoded_error(g,c,e,f):
 ep=g.rowmul(e,c['Ti']);fp=g.rowmul(f,g.transpose(c['T']));s=c['s'];ell=c['ell']
 # Fourier on first s swaps X/Z labels there.
 x=fp[:s]+ep[s:];z=ep[:s]+fp[s:]
 return x,z

def one_way_correction(g,c,e,f):
 x,z=decoded_error(g,c,e,f);s=c['s'];ell=c['ell']
 du=x[:s];dz=x[s+ell:]
 se=[g.dot(row,dz) for row in c['HRt']] if s else []
 sf=du
 eh,ok1=decode_syndrome(g,c,se);fh,ok2=decode_syndrome(g,c,sf)
 xh,zh=decoded_error(g,c,eh,fh)
 return [a^b for a,b in zip(x[s:s+ell],xh[s:s+ell])],[a^b for a,b in zip(z[s:s+ell],zh[s:s+ell])],ok1 and ok2

def errors(B,q,t):
 yield [0]*B
 for w in range(1,t+1):
  for pos in itertools.combinations(range(B),w):
   for values in itertools.product(range(1,q),repeat=w):
    e=[0]*B
    for j,a in zip(pos,values):e[j]=a
    yield e

def main():
 rng=random.Random(202610282340);out=[]
 for m,mod,B,t in [(3,0b1011,5,1),(3,0b1011,7,1),(3,0b1011,8,1),(4,0b10011,9,2),(4,0b10011,13,3)]:
  g=GF(m,mod)
  # Exact finite field and trace-pair nondegeneracy; verifies the small supplied polynomials.
  for a in range(1,g.q):assert g.mul(a,g.inv(a))==1
  for a in range(g.q):
   assert sum((-1)**g.trace(g.mul(a,b)) for b in range(g.q))==(g.q if a==0 else 0)
  c=construct(g,B,t);gates=field_linear_gates(g,c['T'])
  for x in g.eye(B):assert apply_gates(g,x,gates)==g.rowmul(x,c['T'])
  num=0
  if B<=9:
   for e in errors(B,g.q,t):
    synd=[g.dot(h,e) for h in c['H']];eh,ok=decode_syndrome(g,c,synd);assert ok and eh==e;num+=1
  else:
   for _ in range(1000):
    e=[0]*B
    for pos in rng.sample(range(B),rng.randrange(t+1)):e[pos]=rng.randrange(1,g.q)
    eh,ok=decode_syndrome(g,c,[g.dot(h,e) for h in c['H']]);assert ok and eh==e;num+=1
  quantum=0
  # Exhaust all weight-one q-ary Pauli errors, then random errors through t.
  cases=[([0]*B,[0]*B)]
  for pos in range(B):
   for a,b in itertools.product(range(g.q),repeat=2):
    if a==b==0:continue
    e=[0]*B;f=[0]*B;e[pos]=a;f[pos]=b;cases.append((e,f))
  for _ in range(500):
   e=[0]*B;f=[0]*B
   for pos in rng.sample(range(B),rng.randrange(t+1)):
    a,b=rng.randrange(g.q),rng.randrange(g.q)
    if a==b==0:a=1
    e[pos]=a;f[pos]=b
   cases.append((e,f))
  for e,f in cases:
   x,z,ok=one_way_correction(g,c,e,f);assert ok and not any(x) and not any(z);quantum+=1
  # Out-of-radius syndromes must still give a total answer or a declared fallback.
  failed=0
  for _ in range(100):
   ss=[rng.randrange(g.q) for _ in range(c['s'])];eh,ok=decode_syndrome(g,c,ss);assert len(eh)==B;failed+=not ok
  out.append({'m':m,'irreducible_polynomial_bits':bin(mod),'q':g.q,'B':B,'t':t,'quantum_dimension_qudits':c['ell'],'distance':2*t+1,'classical_error_tests':num,'one_way_Pauli_pattern_tests':quantum,'out_of_radius_fallbacks':failed,'linear_field_gate_count':len(gates),'linear_field_gates':gates,'construction':c})
  print('PASS',m,B,t,'classical',num,'Pauli',quantum,flush=True)
 (HERE/'exact_wrapper_checks_v1.json').write_text(json.dumps({'status':'PASS_EXACT_FINITE_FIELD_CSS_BW_AND_ONE_WAY_PAULI_TESTS','seed':202610282340,'cases':out,'scope':'Exact finite field/Pauli propagation, not noisy hardware or dense quantum-state simulation.'},indent=2)+'\n')
if __name__=='__main__':main()
