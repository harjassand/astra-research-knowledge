from bdl_matrices import *
import itertools,json
from pathlib import Path

def seed():return Tanner(2,3,1,[(0,0),(0,1),(1,1),(1,2)],[(0,0),(1,0),(2,0)],[(0,0,0,1),(1,1,0,2)])
def build():
 T=rx(seed());r=T.nz;cs=[1<<i for i in range(r)]+[0]*T.nq
 for q,z in T.qz:cs[r+q]|=1<<z
 return T,cs

def test(cs,order):
 ids,v=basis_reduce(cs,order);rows=[0]*len(ids)
 for i,a in enumerate(v):
  for j in bits(a):rows[j]|=1<<i
 for a,b,c in itertools.combinations(range(len(rows)),3):
  A,B,C=rows[a],rows[b],rows[c];ms=[A&~B&~C,B&~A&~C,A&B&~C,C&~A&~B,A&C&~B,B&C&~A,A&B&C]
  if all(ms):return {'basis':ids,'keep':[a,b,c],'contract':[i for j,i in enumerate(ids) if j not in (a,b,c)],'retain':[(m&-m).bit_length()-1 for m in ms]}
 return None

if __name__=='__main__':
 T,cs=build();r=T.nz;cert=None
 for q in range(T.nq):
  order=[r+q]+list(range(r))+[r+p for p in range(T.nq) if p!=q]
  cert=test(cs,order)
  if cert:break
 if cert is None:
  for seedid in range(1000):
   order=list(range(len(cs)));random.Random(seedid).shuffle(order);cert=test(cs,order)
   if cert:break
 assert cert
 cert['dimensions']=[T.nx,T.nq,T.nz]
 def label(i):return ('check',T.zlabels[i]) if i<r else ('qubit',T.qlabels[i-r])
 cert['contract_labels']=[label(i) for i in cert['contract']];cert['retain_labels']=[label(i) for i in cert['retain']]
 Path(__file__).with_name('two_square_fano_discovery.json').write_text(json.dumps(cert,indent=2)+'\n')
 print('dimensions',cert['dimensions'],'contract',cert['contract'],'retain',cert['retain'])
 for key in ['contract_labels','retain_labels']:
  print(key)
  for x in cert[key]:print(x)
