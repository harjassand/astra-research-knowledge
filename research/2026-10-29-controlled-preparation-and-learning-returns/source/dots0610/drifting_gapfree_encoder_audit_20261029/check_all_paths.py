from fractions import Fraction as F
from itertools import product
import math,json
from pathlib import Path
M=2;T=4;eta=F(1,8);alpha=F(1,4);cases=0;maxgap=-1e9
for bits in product([0,1],repeat=M*T):
 losses=[list(map(F,bits[M*t:M*t+M])) for t in range(T)];w=[F(1,M)]*M;alg=F(0)
 for ls in losses:
  alg+=sum(x*y for x,y in zip(w,ls));v=[w[i]*(1-eta*ls[i]) for i in range(M)];z=sum(v);w=[((1-alpha)*v[i]+alpha*z/M)/z for i in range(M)]
 for path in product(range(M),repeat=T):
  switches=sum(path[t]!=path[t-1] for t in range(1,T));c=sum(losses[t][path[t]] for t in range(T));sq=sum(losses[t][path[t]]**2 for t in range(T));K=math.log(M)+switches*math.log(M/float(alpha))+(T-1-switches)*math.log(1/(1-float(alpha)))
  gap=float(alg-c-eta*sq)-K/float(eta);assert gap<1e-12;cases+=1;maxgap=max(maxgap,gap)
Path(__file__).with_suffix('.json').write_text(json.dumps({'loss_path_cases':cases,'exact_updates':True,'max_potential_residual':maxgap,'scope':'Exhaustive tiny fixed-share loss/path diagnostics; logarithm evaluation float, mathematical proof separate.'},indent=2));print('PASS',cases,'loss/path cases')
