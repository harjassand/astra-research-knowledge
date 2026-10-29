"""Exactly weighted rational sampling with public finite rejection cap.
Caller must schedule all prospective choices as neutral pre-role preflight.
"""
def sample_integer_weights(weights,rng,cap):
 if not weights or any(type(w) is not int or w<=0 for w in weights) or type(cap) is not int or cap<1:raise ValueError('positive integer weights/cap required')
 total=sum(weights);bits=(total-1).bit_length()
 for attempt in range(1,cap+1):
  x=rng.getrandbits(bits)
  if not 0<=x<2**bits:raise ValueError('invalid bit source')
  if x>=total:continue
  for i,w in enumerate(weights):
   if x<w:return dict(index=i,attempts=attempt,bits_per_attempt=bits)
   x-=w
  raise AssertionError('unreachable')
 return dict(index=None,attempts=cap,bits_per_attempt=bits)

if __name__=='__main__':
 import json
 from pathlib import Path
 class Tape:
  def __init__(self,seq):self.seq=iter(seq);self.calls=0
  def getrandbits(self,b):self.calls+=1;return next(self.seq)
 # Every accepted integer routes to exactly its prescribed cumulative interval.
 counts=[0,0,0]
 for x in range(10):
  t=Tape([x]);r=sample_integer_weights([2,3,5],t,4);counts[r['index']]+=1
 assert counts==[2,3,5]
 t=Tape([15]*4+[0]);r=sample_integer_weights([2,3,5],t,4);assert r['index'] is None and t.calls==4
 t=Tape([15]*3+[9]);r=sample_integer_weights([2,3,5],t,4);assert r['index']==2 and t.calls==4
 t=Tape([0]);r=sample_integer_weights([1],t,1);assert r['index']==0 and r['bits_per_attempt']==0
 Path(__file__).with_suffix('.json').write_text(json.dumps(dict(exact_interval_counts=counts,forced_cap_abort=True,last_attempt_accept=True,singleton_zero_bits=True,scope='Finite sampler primitive only; caller owns neutral scheduling/private randomness'),indent=2)+'\n')
 print('All exact cap/boundary fixtures passed')
