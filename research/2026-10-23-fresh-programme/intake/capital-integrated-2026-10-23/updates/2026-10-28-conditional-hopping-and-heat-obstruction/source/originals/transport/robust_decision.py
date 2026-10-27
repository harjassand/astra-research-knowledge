"""Exact local Pauli retargeting bounds for an interacting thermodynamic decision.
Source witnesses are inputs, not freshly acquired inverse solutions.
No source code is imported or executed; full translation words are regenerated.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import numpy as np,json,math,time
OUT=Path(__file__).parent
SRC=Path('/Users/harjas/Documents/ChatGPT/coordination/work/astra-opportunity-retrieval-20261027/published_repo/updates/EX/package/frontier_residual/recovered/astra_frontier_residual_response')

def canon(x,z):
 u=x|z
 if not u:return (0,0)
 s=(u&-u).bit_length()-1;return x>>s,z>>s

def reflect(w):
 x,z=w;l=(x|z).bit_length();return int(f'{x:0{l}b}'[::-1],2),int(f'{z:0{l}b}'[::-1],2)

def clean(f):return {w:v for w,v in f.items() if v}

def expand(words,nums):
 f=defaultdict(int)
 for w,n in zip(words,nums):
  w=tuple(map(int,w));f[w]+=int(n);f[reflect(w)]-=int(n)
 return clean(f)

def norm2(f,den,kind):
 sums=defaultdict(int)
 for (x,z),v in f.items():
  q=x.bit_count()
  if kind=='inverse' and not q:continue
  sums[q]+=v*v
 if kind=='inverse':value=sum((F(v,q) for q,v in sums.items()),F())
 elif kind=='S':value=sum((F(q*v) for q,v in sums.items()),F())
 else:value=sum(map(F,sums.values()),F())
 return value/(den*den)

def Efield(f,sigma):
 # Neutral nearest-swap projection (1-ZiZj)/2, then environment projector /4.
 out=defaultdict(int);left,right=divmod(sigma,2);sl=1-2*left;sr=1-2*right
 for (x,z),coef in f.items():
  if x.bit_count()!=2:continue
  k=(x&-x).bit_length()-1
  if x!=(3<<k):continue
  # Source odd sector has exactly one Y on the pair.
  assert (x&z).bit_count()==1
  xx=x<<1;zz=z<<1;k+=1
  for mask,sign in [(0,1),(1<<(k-1),sl),(1<<(k+2),sr),((1<<(k-1))|(1<<(k+2)),sl*sr)]:
   out[canon(xx,zz^mask)]+=coef*sign
   out[canon(xx,zz^xx^mask)]-=coef*sign
 return clean(out) # denominator 8*den

def hnom(V):return [(3,0,-4),(3,3,-4),(0,3,8),(0,5,int(2*V))] # coeff /8, U=4

def hpattern(sigma):
 left,right=divmod(sigma,2);out=[]
 for mask,sign in [(0,1),(1,1-2*left),(8,1-2*right),(9,(1-2*left)*(1-2*right))]:
  out.extend([(6,mask,-sign),(6,mask^6,-sign)])
 return out # actual delta H = sum e_sigma H_sigma

def act(f,ham):
 out=defaultdict(int)
 for (x0,z0),coef in f.items():
  ell=(x0|z0).bit_length();pad=4;x=x0<<pad;z=z0<<pad
  for a,b,h in ham:
   if not h:continue
   R=(a|b).bit_length()
   for shift in range(pad-R+1,ell+pad):
    aa=a<<shift;bb=b<<shift
    if ((aa&z).bit_count()+(bb&x).bit_count())%2==0:continue
    xx=x^aa;zz=z^bb
    phase=((aa&bb).bit_count()+(x&z).bit_count()-(xx&zz).bit_count()+2*(bb&x).bit_count())%4
    assert phase in (1,3)
    out[canon(xx,zz)]+=coef*h*(1 if phase==1 else -1)
 return clean(out) # denominator 4*den

def sup_sqrt(v,bits=60):
 scale=1<<bits;k=math.isqrt((v.numerator*scale*scale+v.denominator-1)//v.denominator)
 ans=F(k,scale)
 if ans*ans<v:ans=F(k+1,scale)
 assert ans*ans>=v
 return ans

def load(name):
 z=np.load(SRC/'results/anchors'/f'{name}.npz');rec=json.loads((SRC/'results/anchors'/f'{name}.json').read_text())
 return expand(z['fw'],z['FN'][0]),expand(z['gw'],z['GN'][0]),int(z['den'][0]),rec

def lower_data(name):
 tick=time.monotonic();f,g,den,src=load(name);V=F(src['parameters']['V']);A0=act(f,hnom(V));assert all(not v for (x,z),v in A0.items() if not x)
 S2=norm2(f,den,'S');A2=norm2(A0,4*den,'inverse');pair=F(-f.get((3,1),0)+f.get((3,2),0),2*den)
 lo=2*pair-S2-A2;assert 4*lo==F(src['D_interval_exact'][0]),('source lower mismatch',lo)
 E=[Efield(f,s) for s in range(4)];edge=defaultdict(int)
 for e in E:
  for w,v in e.items():edge[w]+=v
 edge=clean(edge);edgeS=norm2(edge,8*den,'S')
 aa10=[act(e,hnom(V)) for e in E]
 aa01=[act(f,hpattern(s)) for s in range(4)]
 aa11=[[act(e,hpattern(s)) for e in E] for s in range(4)]
 population=lambda field:{w:v for w,v in field.items() if not w[0] and v}
 for sigma in range(4):
  assert population(aa10[sigma])=={w:8*v for w,v in population(aa01[sigma]).items()}
  for eta in range(4):
   assert population(aa11[sigma][eta])==(population(aa10[eta]) if sigma==eta else {})
 c10=sum((sup_sqrt(norm2(field,32*den,'inverse')) for field in aa10),F())
 c01=sum((sup_sqrt(norm2(field,4*den,'inverse')) for field in aa01),F())
 c11=sum((sup_sqrt(norm2(field,32*den,'inverse')) for row in aa11 for field in row),F())
 span=max((w[0]|w[1]).bit_length() for field in [f,g,*E,*aa10,*aa01,*[v for row in aa11 for v in row]] for w in field);ans={'full_output_span':span,'nominal_D_lower':4*lo,'edge_S_squared':edgeS,'A0_f_inverse_norm':sup_sqrt(A2),'c10':c10,'c01':c01,'c11':c11}
 print('lower exact source replay and perturbation constants',name,time.monotonic()-tick,flush=True)
 return ans

def upper_data(name):
 tick=time.monotonic();f,g,den,src=load(name);V=F(src['parameters']['V']);Ag=act(g,hnom(V));rr={w:-v for w,v in Ag.items()};rr[(3,1)]=rr.get((3,1),0)-2*den;rr[(3,2)]=rr.get((3,2),0)+2*den;rr=clean(rr)
 r2=norm2(rr,4*den,'inverse');up=r2+norm2(g,den,'S');assert 4*up==F(src['D_interval_exact'][1]),('source upper mismatch',up)
 ASg=[act(g,hpattern(s)) for s in range(4)];assert all(w[0] for field in [Ag,*ASg] for w in field);c=sum((sup_sqrt(norm2(field,4*den,'inverse')) for field in ASg),F())+F(1,2)
 span=max((w[0]|w[1]).bit_length() for field in [g,Ag,*ASg] for w in field);ans={'full_output_span':span,'nominal_D_upper':4*up,'residual_inverse_norm':sup_sqrt(r2),'c_upper':c}
 print('upper exact source replay and perturbation constants',name,time.monotonic()-tick,flush=True)
 return ans

if __name__=='__main__':
 lower=lower_data('V1half');upper=upper_data('V0');min_ring_size=2*max(lower.pop('full_output_span'),upper.pop('full_output_span'))+1;rows=[]
 for epsilon in [F(1,100),F(1,1000),F(1,10000),F(1,100000)]:
  rho=epsilon/(1-epsilon);b=rho*lower['c10']+epsilon*lower['c01']+epsilon*rho*lower['c11']
  low=lower['nominal_D_lower']-4*((1/(1-epsilon)**2-1)*lower['edge_S_squared']+2*lower['A0_f_inverse_norm']*b+b*b)
  c=epsilon*upper['c_upper'];up=upper['nominal_D_upper']+4*(2*upper['residual_inverse_norm']*c+c*c)
  row={'epsilon':str(epsilon),'D_high_lower':str(low),'D_low_upper':str(up),'improvement_lower':str(low-up),'float_improvement_lower':float(low-up),'all_size_scope':'actual thermodynamic D; source transfer premises plus new conditional-hop theorem','min_ring_size':min_ring_size};rows.append(row);print(json.dumps({k:v for k,v in row.items() if k!='D_high_lower' and k!='D_low_upper' and k!='improvement_lower'}),flush=True)
 out={'decision':'V=3/2 versus V=0, U=4,d=2; four independent conditional hopping amplitudes in [1-epsilon,1+epsilon]','lower_constants':{k:str(v) for k,v in lower.items()},'upper_constants':{k:str(v) for k,v in upper.items()},'bounds':rows,'source_witnesses':['results/anchors/V1half.npz','results/anchors/V0.npz'],'min_ring_size':min_ring_size,'method':'full ordinary translation Pauli algebra, exact source replay, all20 population-block identities, rational norm-square arithmetic and upward square roots; no optimizer'}
 (OUT/'ROBUST_INTERACTING_DECISION.json').write_text(json.dumps(out,indent=2)+'\n')
