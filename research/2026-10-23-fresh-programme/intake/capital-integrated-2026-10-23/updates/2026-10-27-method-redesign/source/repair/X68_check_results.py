"""Post-review T74 checker repair: exact batch coverage plus original row checks."""
from pathlib import Path
from fractions import Fraction as F
import json,sys,time
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'lead'))
import check_certificate as exact

def psd(a):
 if a!=exact.tr(a):return False
 a=[row[:] for row in a]
 while a:
  if any(a[i][i]<0 for i in range(len(a))):return False
  pivot=next((i for i in range(len(a)) if a[i][i]>0),None)
  if pivot is None:return all(v==0 for row in a for v in row)
  remaining=[i for i in range(len(a)) if i!=pivot];v=a[pivot][pivot]
  a=[[a[i][j]-a[i][pivot]*a[pivot][j]/v for j in remaining] for i in remaining]
 return True

def verify_portable(kraw,lraw,cert):
 k,l=exact.matrix(kraw),exact.matrix(lraw);c=F(cert['c'])
 assert len(k)==len(l)==3 and all(len(row)==3 for m in [k,l] for row in m)
 assert all(v>0 for m in [k,l] for row in m for v in row)
 assert all(sum(col)==1 for m in [k,l] for col in exact.tr(m));exact.inv(l)
 if cert['kind']=='constant':return c==0 and exact.mul(k,exact.B)==exact.zeros(3,2)
 ak=[exact.form(k,[[[F(i==j)]] for j in range(3)]) for i in range(3)]
 al=[exact.form(l,[[[F(i==j)]] for j in range(3)]) for i in range(3)]
 if cert['kind']=='covariance_vertices':
  return c>=1 and all(psd(exact.sub(exact.scale(c,b),a)) for a,b in zip(ak,al))
 if cert['kind']=='covariance_center':
  if not 0<=c<1:return False
  h=[[F(x)] for x in cert['z']]
  for a,b,e in zip(ak,al,exact.E):
   v=exact.sub(e,h)
   if not psd(exact.sub(exact.sub(exact.scale(c,exact.inv(a)),exact.inv(b)),exact.scale(1-c,exact.mul(v,exact.tr(v))))):return False
  return True
 return False

def verify_general(k,l,cert):
 if cert['kind']!='general_covariance_sdp':
  converted={'kind':{'vertex_expansive':'covariance_vertices','constant':'constant'}[cert['kind']],
             'c':cert['upper']}
  return verify_portable(k,l,converted)
 k,l=exact.matrix(k),exact.matrix(l);c=F(cert['upper']);a=exact.matrix(cert['A'])
 m=exact.mul(k,exact.B);hl=exact.vertices(l)
 if c<0 or len(a)!=9 or any(len(row)!=9 for row in a):return False
 for i in range(3):
  di=exact.diagonal([k[j][i] for j in range(3)])
  ci=exact.mul(exact.mul(m,hl[i]),exact.tr(m))
  if [row[3*i:3*i+3] for row in a[3*i:3*i+3]]!=exact.sub(exact.scale(c,di),ci):return False
 t=exact.zeros(9,6)
 for i in range(3):t[i][i]=1;t[3+i][3+i]=1;t[6+i][i]=-1;t[6+i][3+i]=-1
 s=[[m[i][0]] for i in range(3)]+[[m[i][1]] for i in range(3)]+[[F(0)]]*3
 remainder=exact.mul(exact.mul(exact.tr(t),exact.sub(a,exact.mul(s,exact.tr(s)))),t)
 return psd(a) and psd(remainder)

def verify_witness(kraw,lraw,w):
 k,l=exact.matrix(kraw),exact.matrix(lraw);qs=[exact.matrix(q) for q in w['Q']]
 us=[[[F(v)] for v in u] for u in w['u']];d=w['dimension']
 assert len(qs)==len(us)==3 and all(len(q)==d and psd(q) for q in qs)
 qsum=exact.zeros(d);usum=exact.zeros(d,1)
 for q,u in zip(qs,us):qsum=exact.add(qsum,q);usum=exact.add(usum,u)
 assert qsum==exact.eye(d) and usum==exact.zeros(d,1)
 def f(channel):
  out=F(0)
  for row in channel:
   wy=exact.zeros(d);vy=exact.zeros(d,1)
   for coefficient,q,u in zip(row,qs,us):
    wy=exact.add(wy,exact.scale(coefficient,q));vy=exact.add(vy,exact.scale(coefficient,u))
   out+=exact.quadratic(exact.inv(wy),vy)
  return out
 fk,fl=f(k),f(l)
 assert fl>0 and fk>=0 and fk==F(w['FK']) and fl==F(w['FL']) and fk/fl==F(w['ratio'])
 return True

def check(case,row):
 cert=row['upper_certificate'];data=cert['data'];k,l=case['K'],case['L']
 if cert['source']=='portable':
  assert verify_portable(k,l,data);upper=F(data['c'])
 else:
  assert cert['source']=='general' and verify_general(k,l,data);upper=F(data['upper'])
 assert verify_witness(k,l,row['lower_witness'])
 lower=F(row['lower_witness']['ratio'])
 assert upper==F(row['upper']) and lower==F(row['lower']) and 0<=lower<=upper
 assert row['width_target_pass']==(upper-lower<=F(1,50)*max(1,lower))
 return {'id':row['id'],'status':'PASS','certificate':cert['source'],'dimension':row['lower_witness']['dimension']}

def unique_rows(rows,label):
 if not isinstance(rows,list):raise ValueError(label+' must be a list')
 indexed={}
 for row in rows:
  if not isinstance(row,dict) or not isinstance(row.get('id'),str):
   raise ValueError(label+' rows require string IDs')
  identity=row['id']
  if identity in indexed:raise ValueError('duplicate '+label+' ID: '+repr(identity))
  indexed[identity]=row
 return indexed

def check_batch(inputs,outputs):
 if not isinstance(inputs,dict) or 'cases' not in inputs:
  raise ValueError('input document requires cases')
 if not isinstance(outputs,dict) or 'results' not in outputs:
  raise ValueError('output document requires results')
 cases=unique_rows(inputs['cases'],'input')
 rows=unique_rows(outputs['results'],'result')
 if not cases:raise ValueError('input batch must contain at least one case')
 unknown=set(rows)-set(cases);missing=set(cases)-set(rows)
 if unknown or missing:
  raise ValueError('batch coverage mismatch: unknown='+repr(sorted(unknown))+'; missing='+repr(sorted(missing)))
 return [check(case,rows[identity]) for identity,case in cases.items()]

if __name__=='__main__':
 started=time.perf_counter()
 verdicts=check_batch(json.loads(Path(sys.argv[1]).read_text()),json.loads(Path(sys.argv[2]).read_text()))
 for verdict in verdicts:print(json.dumps(verdict),flush=True)
 print(json.dumps({'checked':len(verdicts),'seconds':time.perf_counter()-started,'dependencies':'Python standard library only'}))
