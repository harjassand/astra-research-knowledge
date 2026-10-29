from itertools import product
from pathlib import Path
import json

class Circuit:
 def __init__(self):self.n=0;self.inputs=[];self.ops=[];self.clauses=[];self.const={}
 def inp(self):self.n+=1;self.inputs.append(self.n);return self.n
 def constant(self,b):
  if b not in self.const:
   self.n+=1;self.const[b]=self.n;self.clauses.append([self.n if b else -self.n])
  return self.const[b]
 def gate(self,typ,*vs):
  self.n+=1;o=self.n
  f={'and':lambda a,b:a&b,'or':lambda a,b:a|b,'xor':lambda a,b:a^b,'not':lambda a:1-a}[typ]
  self.ops.append((o,vs,f))
  for bits in product([0,1],repeat=len(vs)+1):
   if bits[-1]!=f(*bits[:-1]):self.clauses.append([-v if b else v for v,b in zip((*vs,o),bits)])
  return o
 def lookup(self,ins,table):
  terms=[]
  for row in product([0,1],repeat=len(ins)):
   if table(row):
    literals=[v if b else self.gate('not',v) for v,b in zip(ins,row)]
    p=literals[0]
    for v in literals[1:]:p=self.gate('and',p,v)
    terms.append(p)
  if not terms:return self.constant(0)
  o=terms[0]
  for t in terms[1:]:o=self.gate('or',o,t)
  return o
 def evaluate(self,ins):
  v=dict(zip(self.inputs,ins));v.update({i:b for b,i in self.const.items()})
  for o,vs,f in self.ops:v[o]=f(*(v[x] for x in vs))
  assert len(v)==self.n
  assert all(any(v[abs(l)]==(l>0) for l in c) for c in self.clauses)
  return v
 def less(self,z,w):
  eq=self.constant(1);lt=self.constant(0)
  for a,b in zip(reversed(z),reversed(w)):
   lt=self.gate('or',lt,self.gate('and',eq,self.gate('and',self.gate('not',a),b)))
   eq=self.gate('and',eq,self.gate('not',self.gate('xor',a,b)))
  return lt

def bits(x,n):return tuple((x>>j)&1 for j in range(n))
def value(bs):return sum(b<<j for j,b in enumerate(bs))
res=[]
for B in [1,2,3,4,5]:
 c=Circuit();z=[c.inp() for _ in range(B)];w=[c.inp() for _ in range(B)];lt=c.less(z,w)
 for a in range(2**B):
  for b in range(2**B):assert c.evaluate(bits(a,B)+bits(b,B))[lt]==int(a<b)
 assert max(map(len,c.clauses))<=3
 res.append({'selector_bits':B,'variables':c.n,'clauses':len(c.clauses),'input_cases':4**B,'unique_extension':'Every gate clause is an exact equivalence; DAG induction fixes all auxiliaries.'})
# Actual signed/imaginary lookup and mod4 phase gadget.
# Input row i,o,c chooses real/imag component of [[2,-i],[i,2]].
c=Circuit();ins=[c.inp() for _ in range(3)];p=[c.inp() for _ in range(2)]
def comp(row):
 i,o,imag=row
 if i==o:return 0 if imag else 2
 return (1 if o==1 else -1) if imag else 0
mag=[c.lookup(ins,lambda row,j=j:(abs(comp(row))>>j)&1) for j in range(2)]
neg=c.lookup(ins,lambda row:int(comp(row)<0))
lo=c.gate('xor',p[0],ins[2]);hi=c.gate('xor',c.gate('xor',p[1],neg),c.gate('and',p[0],ins[2]))
for b in product([0,1],repeat=5):
 v=c.evaluate(b);a=comp(b[:3]);assert value([v[x] for x in mag])==abs(a)
 assert value([v[lo],v[hi]])==(value(b[3:])+b[2]+2*(a<0))%4
res.append({'signed_lookup_phase_variables':c.n,'clauses':len(c.clauses),'input_cases':32,'max_clause_width':max(map(len,c.clauses))})
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
