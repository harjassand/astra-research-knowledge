"""Process-scoped callable API for rational cube/partition exact laws.

No GSW statistical guarantee is part of this interface. This wrapper validates
input types/shapes; bridge.run performs candidate checking and exact output checks.
Upstream module callbacks are process-local, so use separate processes for
concurrent calls. No file, network or persistent-runtime write is performed.
"""
from fractions import Fraction as F
from copy import deepcopy
import bridge

def compile_exact_law(A,p,blocks=None,*,method='gsw64_checked',seed=0,name='supplied'):
 A=[[F(v)for v in row]for row in A];p=[F(v)for v in p];n=len(p)
 if not n or not A or any(len(row)!=n for row in A):raise ValueError('A must be a nonempty R by n rational matrix')
 if any(abs(v)>1 for row in A for v in row):raise ValueError('Feature entry outside[-1,1]')
 if any(not 0<=v<=1 for v in p):raise ValueError('Mean outside[0,1]')
 if blocks is not None:
  blocks=deepcopy(blocks)
  if any(not b for b in blocks)or sorted(j for b in blocks for j in b)!=list(range(n)):raise ValueError('Blocks must partition the coordinates exactly')
  if any(sum(p[j]for j in b).denominator!=1 for b in blocks):raise ValueError('Block means must have integral sums')
 if method not in('n24_exact','gsw64_checked','gsw3_checked','greedy8_checked','random8_checked','systematic','dependent_greedy','global_exact_small'):raise ValueError('Unknown method')
 case={'id':name,'split':'supplied','family':'supplied','kind':'cube'if blocks is None else'partition','n':n,'rows':len(A),'seed':int(seed),'A':[[str(v)for v in row]for row in A],'p':[str(v)for v in p],'blocks':blocks}
 return bridge.run(case,method)
