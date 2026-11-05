"""Fresh independent graph-noise extension, not a circuit-depolarizing model.
T data-error rounds, T-1 noisy syndrome observations, perfect initial/final closure.
"""
from sampler import Model,Proposal,F,np,pymatching,csr_matrix,exact_cp
from pathlib import Path
import time,random,json,argparse
class RepeatedModel(Model):
 def __init__(self,d,T):
  assert d>=3 and T>=1
  self.d=d;self.T=T
  self.coords=[(x,y,t) for t in range(T) for x in range(d+1) for y in range(d)]
  self.node={q:i for i,q in enumerate(self.coords)};self.edges=[];self.cut=[]
  for t in range(T):
   for x in range(d):
    for y in range(d):
     if x==0:self.cut.append(len(self.edges))
     self.edges.append((self.node[x,y,t],self.node[x+1,y,t]))
   for x in range(1,d):
    for y in range(d-1):self.edges.append((self.node[x,y,t],self.node[x,y+1,t]))
  for t in range(T-1):
   for x in range(1,d):
    for y in range(d):self.edges.append((self.node[x,y,t],self.node[x,y,t+1]))
  self.adj=[[] for q in self.coords]
  for i,(u,v) in enumerate(self.edges):self.adj[u].append((v,i));self.adj[v].append((u,i))
  for a in self.adj:a.sort(key=lambda x:x[1])
  self.left=[self.node[0,y,t] for t in range(T) for y in range(d)]
  self.right=set(self.node[d,y,t] for t in range(T) for y in range(d))
  self.checks=[self.node[x,y,t] for t in range(T) for x in range(1,d) for y in range(d)]
  self.checkid={v:i for i,v in enumerate(self.checks)};self.m=pymatching.Matching()
  hrows=[];hcols=[];self.edge_checks=[]
  for i,(u,v) in enumerate(self.edges):
   ends=[self.checkid[z] for z in (u,v) if z in self.checkid]
   hrows.extend(ends);hcols.extend([i]*len(ends));self.edge_checks.append(ends)
   if len(ends)==2:self.m.add_edge(*ends,fault_ids={i},weight=1.)
   else:self.m.add_boundary_edge(ends[0],fault_ids={i},weight=1.)
  self.H=csr_matrix((np.ones(len(hrows),dtype=np.uint8),(hrows,hcols)),shape=(len(self.checks),len(self.edges)))

def run(d,T,p,Lmax,shots,seed,out,confidence):
 start=time.perf_counter();m=RepeatedModel(d,T);q=Proposal(m,p,Lmax);setup=time.perf_counter()-start
 rng=random.Random(seed);counts={k:0 for k in ['accepted','nonsimple','not_failure','other_witness']};ts=time.perf_counter()
 for i in range(shots):v,why=q.trial(rng);counts[why]+=1
 sampling=time.perf_counter()-ts;tc=time.perf_counter()
 result={'model':'independent phenomenological data-Z and syndrome-bit noise; T rounds, perfect initial/final syndrome closure; NOT circuit depolarizing noise','distance':d,'rounds':T,'physical_qubits':2*d*d-2*d+1,'graph_fault_edges':len(m.edges),'detectors':len(m.checks),'p':str(p),'Lmax':Lmax,'shots':shots,'seed':seed,'counts':counts,'Z_exact':str(q.Z),'Z':float(q.Z),'tail_bound':float(q.tail),'tail_exact':str(q.tail),'point_estimate':float(q.Z*F(counts['accepted'],shots))}
 if confidence:
  lo,hi=exact_cp(counts['accepted'],shots)
  result.update(confidence='.999, ideal iid bits and exact MWPM contract',interval=[float(q.Z*lo),float(q.Z*hi+q.tail)],interval_exact=[str(q.Z*lo),str(q.Z*hi+q.tail)])
 else:result['scope']='exploratory acceptance/time screen, no confidence claim'
 result['timing_seconds']={'setup':setup,'sampling':sampling,'confidence':time.perf_counter()-tc,'total_before_json':time.perf_counter()-start}
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if 'exact' not in k},indent=2))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--distance',type=int,default=13);a.add_argument('--rounds',type=int,default=13);a.add_argument('--p',default='1/1000');a.add_argument('--length',type=int,default=100);a.add_argument('--shots',type=int,default=1000);a.add_argument('--seed',type=int,default=2026110507);a.add_argument('--out',default='phenomenological.json');a.add_argument('--confidence',action='store_true');v=a.parse_args();run(v.distance,v.rounds,F(v.p),v.length,v.shots,v.seed,v.out,v.confidence)
