"""Exact rational killed proposal; iid claims assume ideal random bits.

NumPy is used only for deterministic integer-vector operations. Python Random
supplies a reproducible PRNG implementation, not a proof of physical randomness.
"""
import argparse,bisect,hashlib,json,random,resource,sys,time
from fractions import Fraction as F
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'canonical_qec_circuit_gate_20261105'))
from tilted_pilot import CircuitModel
sys.path.insert(0,str(ROOT.parent/'canonical_qec_witness_20261105'))
from confidence_fast import exact_cp

class FoldedProposal:
 def __init__(self,N=64):
  self.meta=json.loads((ROOT/f'certificate_N{N}.json').read_text());self.N=N
  path=ROOT.parent/'canonical_qec_circuit_gate_20261105/d13_r13_p1_1000_graph.json'
  assert hashlib.sha256(path.read_bytes()).hexdigest()==self.meta['input_sha256']
  self.G=json.loads(path.read_text());self.model=CircuitModel(self.G)
  table=ROOT/f'certified_table_N{N}.bin'
  assert hashlib.sha256(table.read_bytes()).hexdigest()==self.meta['table_sha256']
  a=np.load(ROOT/f'automaton_N{N}.npz');self.states=[tuple(map(int,x)) for x in a['states']]
  self.U=np.fromfile(table,dtype=np.uint64).reshape(len(self.states),N)
  self.starts=list(map(int,a['starts']));self.end=a['end'];self.delta=list(map(int,a['delta']))
  row=a['row'];col=a['col'];self.nxt=[list(map(int,col[int(row[i]):int(row[i+1])])) for i in range(len(self.states))]
  self.w=list(map(int,self.meta['weight_numerators']));self.wb=self.meta['weight_denominator_exponent'];self.qb=self.meta['table_denominator_exponent']
  self.q=np.array(self.meta['q_numerators'],dtype=np.uint64)
  self.initial=[];total=0
  for s in self.starts:total+=self.w[s]*int(self.U[s,self.delta[s]%N]);self.initial.append(total)
  self.Znum=total;self.Z=F(total,1<<(self.wb+self.qb));assert str(self.Z)==self.meta['Z_exact']
  self.max_vertices=1+max(max(e) for e in self.G['edges'])

 def trial(self,rng):
  s=self.starts[bisect.bisect_right(self.initial,rng.randrange(self.Znum))]
  u,v,e,b=self.states[s];seen={u,v};path=[e];bits=[b];score=self.delta[s];r=score%self.N;steps=1
  while True:
   H=int(self.U[s,r]);assert H>0
   if self.end[s]:
    # Exact terminal mass 2^{-r}/(U/2^qb).
    if r<=self.qb:good=rng.randrange(H)<(1<<(self.qb-r))
    else:good=rng.randrange(H<<(r-self.qb))==0
    if not good:return 0,'null',steps,0,score
    break
   pick=rng.randrange(H<<self.wb);chosen=None
   for j in self.nxt[s]:
    rr=(r+self.delta[j])%self.N;mass=self.w[j]*int(self.U[j,rr])
    if pick<mass:chosen=j;r=rr;break
    pick-=mass
   if chosen is None:return 0,'null',steps,0,score
   s=chosen;u,v,e,b=self.states[s];steps+=1
   if v in seen:return 0,'nonsimple',steps,0,score+self.delta[s]
   seen.add(v);path.append(e);bits.append(b);score+=self.delta[s]
   assert steps<=self.max_vertices
  if score<0:return 0,'negative_score',steps,0,score
  exponent=score-r;assert exponent>=0 and exponent%self.N==0
  if exponent and rng.getrandbits(exponent)!=0:return 0,'fold_reject',steps,0,score
  errors=(np.frombuffer(rng.randbytes(8*len(self.q)),dtype='<u8')<self.q).astype(np.uint8)
  errors[path]=bits
  witness=self.model.witness(errors)
  if witness is None:return 0,'not_failure',steps,1,score
  if witness!=tuple(path):return 0,'other_witness',steps,1,score
  return 1,'accepted',steps,1,score

def run(shots,seed,confidence=True,output='production_100k.json'):
 ts=time.perf_counter();P=FoldedProposal();setup=time.perf_counter()-ts;rng=random.Random(seed)
 counts={k:0 for k in ['null','nonsimple','negative_score','fold_reject','not_failure','other_witness','accepted']};steps=0;decoders=0;maxsteps=0;maxscore=0
 sample_start=time.perf_counter()
 for i in range(shots):
  value,kind,L,decoded,S=P.trial(rng);counts[kind]+=1;steps+=L;decoders+=decoded;maxsteps=max(maxsteps,L);maxscore=max(maxscore,S)
  if (i+1)%10000==0:print(json.dumps({'completed':i+1,'seconds':time.perf_counter()-sample_start}),flush=True)
 sample_seconds=time.perf_counter()-sample_start;tc=time.perf_counter();interval=None
 if confidence:
  lo,hi=exact_cp(counts['accepted'],shots,F(1,1000),bits=24);bias=F(P.meta['conversion_TV_upper_exact']);L=max(F(0),P.Z*lo-bias);U=min(F(1),P.Z*hi+bias)
  interval={'confidence':.999,'acceptance_exact':[str(lo),str(hi)],'failure_probability_exact':[str(L),str(U)],'failure_probability_float':[float(L),float(U)],'includes_conversion_bias':True,'finite_length_tail':0}
 result={'scope':'exact rational proposal and outward statistical interval under ideal independent random bits; fixed circuit and decoder only','shots':shots,'seed':seed,'counts':counts,'normalizer_exact':str(P.Z),'normalizer_float':float(P.Z),'point_estimate':float(P.Z*counts['accepted']/shots),'interval':interval,'mean_path_steps':steps/shots,'maximum_path_steps':maxsteps,'maximum_true_score':maxscore,'decoder_calls':decoders,'setup_seconds':setup,'sampling_seconds':sample_seconds,'confidence_seconds':time.perf_counter()-tc,'total_seconds':time.perf_counter()-ts,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'implementation_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'certificate_table_sha256':P.meta['table_sha256']}
 (ROOT/output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--shots',type=int,default=100000);a.add_argument('--seed',type=int,default=202611051864);a.add_argument('--no-confidence',action='store_true');a.add_argument('--output',default='production_100k.json');v=a.parse_args();run(v.shots,v.seed,not v.no_confidence,v.output)
