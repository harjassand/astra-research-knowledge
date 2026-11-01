"""Exhaustive actual one-square RX ell3 local-recognizer and trace test.
This fixture tests ONE actual RX map and a finite Bell seed, not the full
memory decoder's modified level-2 terminal lookup. The proof note separately
binds that terminal exactly. All actual extra Z checks are retained.
"""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'helpers'))
from actual_rx_rung import build
from gf2 import pivots,member

c=build(3);Q=c['qs'];Z=c['Z'];zn=c['zs'];n=len(Q);r=len(Z)
col=[sum(((row>>q)&1)<<j for j,row in enumerate(Z)) for q in range(n)]
def syndrome(e):
 out=0
 while e:
  t=e&-e;out^=col[t.bit_length()-1];e^=t
 return out
cxq=[q for q,v in enumerate(Q) if v[0]!='qv']
xrows=[j for j,v in enumerate(zn) if v[0] in ('xf','xcf')]
qrows={a:[j for j,v in enumerate(zn) if v[0] in ('qe','qr') and v[1]==a] for a in ('a','b')}
zrows=[j for j,v in enumerate(zn) if v[0]=='z']
qcols={a:[q for q,v in enumerate(Q) if v[0]=='qv' and v[1]==a] for a in ('a','b')}
def mask(xs):return sum(1<<i for i in xs)
xmask=mask(xrows);qmask=mask(qrows['a']+qrows['b']);zmask=mask(zrows)

def table(qs,localmask,outmask):
 T={}
 for bits in range(1<<len(qs)):
  e=sum(((bits>>j)&1)<<q for j,q in enumerate(qs));s=syndrome(e);key=s&localmask
  if (s&outmask).bit_count()>key.bit_count():continue
  if key not in T or e<T[key][0]:T[key]=(e,s)
 assert T[0]==(0,0)
 return T
TX=table(cxq,xmask,qmask)
TQ={a:table(qcols[a],mask(qrows[a]),zmask) for a in ('a','b')}

class Circuit:
 def __init__(self):self.gates=[];self.adj={};self.flags=[]
 def add(self,name,ins,outs,fn):
  assert len(fn([0]*len(ins)))==len(outs)
  assert not any(fn([0]*len(ins)))
  self.gates.append((name,ins,outs,fn));g=('G',name);self.adj.setdefault(g,set())
  for v in ins+outs:
   w=('W',v);self.adj.setdefault(w,set()).add(g);self.adj[g].add(w)
 def run(self,s):
  vals={('s0',j):(s>>j)&1 for j in range(r)};marked={('W',('s0',j)) for j in range(r) if s>>j&1}
  for name,ins,outs,fn in self.gates:
   iv=[vals[v] for v in ins];ov=fn(iv);vals.update(zip(outs,ov))
   if any(iv):marked.add(('G',name));marked.update(('W',v) for v in ins+outs)
  ok=not any(vals[f] for f in self.flags)
  return ok,vals,marked
 def components(self,M):
  todo=set(M);out=[]
  while todo:
   seed=todo.pop();comp={seed};stack=[seed]
   while stack:
    u=stack.pop()
    for v in self.adj.get(u,set())&todo:
     todo.remove(v);comp.add(v);stack.append(v)
   out.append(comp)
  return out
C=Circuit()
def addsolve(name,rows,qs,T,stage):
 affected=sorted({j for q in qs for j in range(r) if col[q]>>j&1})
 ins=[(stage,j) for j in rows];outs=[('f',name,q) for q in qs]+[('d',name,j) for j in affected]+[('flag',name)]
 def fn(bits):
  key=sum(b<<j for b,j in zip(bits,rows));entry=T.get(key)
  if entry is None:return [0]*(len(outs)-1)+[1]
  e,s=entry;return [(e>>q)&1 for q in qs]+[(s>>j)&1 for j in affected]+[0]
 C.add(name,ins,outs,fn);C.flags.append(('flag',name));return affected
AX=addsolve('X',xrows,cxq,TX,'s0')
for j in range(r):
 ins=[('s0',j)]+([('d','X',j)] if j in AX else [])
 C.add(('update1',j),ins,[('s1',j)],lambda b:[sum(b)%2])
AQ={a:addsolve('Q'+a,qrows[a],qcols[a],TQ[a],'s1') for a in ('a','b')}
for j in range(r):
 ins=[('s1',j)]+[('d','Q'+a,j) for a in ('a','b') if j in AQ[a]]
 C.add(('update2',j),ins,[('s2',j)],lambda b:[sum(b)%2])
C.add('diagonal',[('s2',j) for j in zrows],[('parent',0),('flag','diag')],lambda b:[b[0],b[0]^b[1]])
C.flags.append(('flag','diag'))
# Bell seed has one independent Z check; correction uses its first qubit.
C.add('seed',[('parent',0)],[('fseed',0),('flag','seed')],lambda b:[b[0],0]);C.flags.append(('flag','seed'))
# Explicit one-step telescoping identity, coordinate by coordinate.
for j in range(r):
 ins=[('s0',j)]+([('d','X',j)] if j in AX else [])+[('d','Q'+a,j) for a in ('a','b') if j in AQ[a]]+([('parent',0)] if j in zrows else [])
 flag=('flag','identity',j);C.add(('identity',j),ins,[flag],lambda b:[sum(b)%2]);C.flags.append(flag)

P=pivots(col);accepted=0;rejected=0;split_inputs=0;components=0;maxratio=0;maxcomp=0;examples=[]
for s in range(1<<r):
 ok,vals,M=C.run(s);assert ok==member(s,P)
 if not ok:rejected+=1;continue
 accepted+=1
 s1=sum(vals['s1',j]<<j for j in range(r));s2=sum(vals['s2',j]<<j for j in range(r));sp=vals['parent',0]
 assert s1.bit_count()<=s.bit_count() and s2.bit_count()<=s1.bit_count() and 2*sp<=s.bit_count()
 fx=sum(vals['f','X',q]<<q for q in cxq)
 fq=0
 for a in ('a','b'):fq^=sum(vals['f','Q'+a,q]<<q for q in qcols[a])
 liftseed=sum(1<<q for q,v in enumerate(Q) if v[0]=='qv' and v[1]=='a') if sp else 0
 assert syndrome(fx^fq^liftseed)==s
 parts=C.components(M);components+=len(parts);maxcomp=max(maxcomp,len(parts))
 if len(parts)>1:split_inputs+=1
 if s:maxratio=max(maxratio,len(M)/s.bit_count())
 for part in parts:
  sub=sum(1<<j for j in range(r) if s>>j&1 and ('W',('s0',j)) in part)
  assert sub
  ok2,v2,M2=C.run(sub);assert ok2 and member(sub,P) and M2==part
  assert all(v2[v[1]]==vals[v[1]] for v in part if v[0]=='W')
 if len(parts)>1 and len(examples)<3:examples.append(dict(syndrome=s,components=len(parts)))
result=dict(ell=3,qubits=n,Zchecks=r,syndrome_rank=len(P),all_inputs=1<<r,accepted=accepted,rejected=rejected,
 local_table_entries=dict(X=len(TX),Qa=len(TQ['a']),Qb=len(TQ['b'])),
 circuit_gates=len(C.gates),host_objects=len(C.adj),host_max_degree=max(map(len,C.adj.values())),
 accepting_component_replays=components,inputs_with_multiple_components=split_inputs,max_components=maxcomp,
 maximum_observed_trace_to_syndrome_weight=maxratio,split_examples=examples,
 flags_equivalent_to_global_image=True,all_component_replays_exact=True)
print(json.dumps(result,indent=2))
open(Path(__file__).with_name('actual_rx_recognizer_fixture_results.json'),'w').write(json.dumps(result,indent=2))
