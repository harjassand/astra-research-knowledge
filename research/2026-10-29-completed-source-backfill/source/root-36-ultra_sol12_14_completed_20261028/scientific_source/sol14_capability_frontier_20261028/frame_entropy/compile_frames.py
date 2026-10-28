"""Exact Hoggar/MUB qualification and entropy receivers; no eigensolver premise."""
from fractions import Fraction as Q
from pathlib import Path
from time import perf_counter
import json,sys
import exact_entropy as e
sys.set_int_max_str_digits(0)
HERE=Path(__file__).resolve().parent
def z(a=0,b=0):return a,b
def add(a,b):return a[0]+b[0],a[1]+b[1]
def mul(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def conj(a):return a[0],-a[1]
def scale(a,x):return a[0]*x,a[1]*x
def total(xs):
 ans=z()
 for x in xs:ans=add(ans,x)
 return ans
def eye(n):return[[z(int(i==j))for j in range(n)]for i in range(n)]
def mm(a,b):return[[total(mul(x,y)for x,y in zip(row,col))for col in zip(*b)]for row in a]
def trace(a):return total(a[i][i]for i in range(len(a)))
def lin(weights,matrices):
 d=len(matrices[0]);return[[total(scale(g[i][j],w)for w,g in zip(weights,matrices))for j in range(d)]for i in range(d)]
def kron(a,b):
 return[[mul(a[i//len(b)][j//len(b)],b[i%len(b)][j%len(b)])for j in range(len(a)*len(b))]for i in range(len(a)*len(b))]
def inner(a,b):return total(mul(conj(x),y)for x,y in zip(a,b))
def design_moments(gs,den):
 n=len(gs);d=len(gs[0]);first=lin([1]*n,gs)
 assert first==[[z(Q(n*den,d)*int(i==j))for j in range(d)]for i in range(d)]
 target=Q(n*den*den,d*(d+1));checks=0
 for i in range(d):
  for j in range(d):
   for k in range(d):
    for l in range(d):
     actual=total(mul(g[i][j],g[k][l])for g in gs)
     expected=target*(int(i==j and k==l)+int(i==l and k==j))
     assert actual==z(expected);checks+=1
 return checks
def hoggar():
 fid=[z(-1,2)]+[z(1)]*7;vectors=[]
 for x in range(8):
  for zz in range(8):
   vectors.append([scale(fid[y^x],(-1)**((zz&y).bit_count()))for y in range(8)])
 gs=[[[mul(x,conj(y))for y in v]for x in v]for v in vectors]
 for i,v in enumerate(vectors):
  assert inner(v,v)==z(12)
  for j,u in enumerate(vectors):
   a=inner(v,u);assert a[0]**2+a[1]**2==(144 if i==j else 16)
 count=design_moments(gs,12)
 return gs,{'d':8,'n':64,'denominator':12,'exact_pair_checks':4096,
 'second_moment_components':count,'off_diagonal_squared_overlap':'1/9',
 'qualification':'SIC plus coherence amplitude 1/3<=1/2','fiducial':['-1+2i']+['1']*7}
def mub4():
 ident2=eye(2);px=[[z(),z(1)],[z(1),z()]]
 py=[[z(),z(0,-1)],[z(0,1),z()]];pz=[[z(1),z()],[z(),z(-1)]]
 p={'I':ident2,'X':px,'Y':py,'Z':pz}
 def op(pair):return kron(p[pair[0]],p[pair[1]])
 generators=[('ZI','IZ'),('XI','IX'),('YI','IY'),('XY','YZ'),('YX','ZY')]
 gs=[];ident=eye(4)
 for aa,bb in generators:
  a,b=op(aa),op(bb);assert mm(a,b)==mm(b,a)
  for s in[-1,1]:
   for t in[-1,1]:
    g=mm(lin([1,s],[ident,a]),lin([1,t],[ident,b]))
    assert trace(g)==z(4)and mm(g,g)==lin([4],[g])
    assert all(g[i][j]==conj(g[j][i])for i in range(4)for j in range(4))
    gs.append(g)
 for i,g in enumerate(gs):
  for j,h in enumerate(gs):
   assert trace(mm(g,h))==z(16 if i==j else(0 if i//4==j//4 else 4))
 count=design_moments(gs,4)
 return gs,{'d':4,'n':20,'denominator':4,'exact_pair_checks':400,
 'second_moment_components':count,'cross_basis_squared_overlap':'1/4',
 'qualification':'Complete MUB with coherence amplitude 1/2',
 'commuting_generators':generators,'uniform_entropy_correction':'(1/2) log(5/4) on the defect side'}

def characteristic(a,den):
 d=len(a);power=eye(d);traces=[]
 for k in range(1,d+1):
  power=mm(power,a);t=trace(power);assert t[1]==0
  traces.append(Q(t[0],den**k))
 elementary=[Q(1)]
 for k in range(1,d+1):
  elementary.append(sum(((-1)**(j-1)*elementary[k-j]*traces[j-1]for j in range(1,k+1)),Q(0))/k)
 polynomial=[Q(0)]*(d+1)
 for k,c in enumerate(elementary):polynomial[d-k]=(-1)**k*c
 assert traces[0]==1
 return polynomial,traces[1]

def evaluate(gs,den,weights,is_sic):
 n=len(gs);d=len(gs[0]);t=sum(weights);p=[Q(x,t)for x in weights]
 a=lin(weights,gs);polynomial,purity=characteristic(a,den*t)
 if is_sic:assert purity==(1+d*sum(v*v for v in p))/(d+1)
 roots,steps=e.roots01(polynomial)
 output=e.entropy(roots);input_=e.entropy([e.iv(v)for v in p])
 correction=e.sub(e.logq(n),e.scale(e.logq(d),2))
 gap=e.add(e.sub(e.scale(output,2),input_),correction)
 relaxation=e.add(e.sub(e.scale(e.hmin(purity,d),2),e.hmax(sum(v*v for v in p),n)),correction)
 assert gap[0]>0
 return{'raw_weights':weights,'input_purity':e.serial(sum(v*v for v in p)),
 'output_purity':e.serial(purity),'characteristic_polynomial_ascending':[e.serial(x)for x in polynomial],
 'eigenvalue_intervals':[e.record(x)for x in roots],'Sturm_splits':steps,
 'entropy_contraction_defect':e.record(gap),'sharp_scalar_purity_relaxation':e.record(relaxation),
 'interpretation':'Defect = D(p||uniform)-2D(M||I/d) = 2S(M)-H(p)+log(n)-2log(d).'}

def main():
 start=perf_counter();gs,h=hoggar();hg_time=perf_counter()-start
 mstart=perf_counter();mgs,m=mub4();mub_time=perf_counter()-mstart
 # A fixed literal permutation, not a stochastic proof premise.
 tail=[((37*j)%63)+1 for j in range(63)];assert sorted(tail)==list(range(1,64))
 vstart=perf_counter();hc=evaluate(gs,12,[864]+tail,True)
 assert Q(hc['sharp_scalar_purity_relaxation']['upper'])<0
 mc=evaluate(mgs,4,[100]+list(range(1,20)),False)
 eval_time=perf_counter()-vstart
 result={'status':'PASS','general_theorem':'PROOF.md, analytic all-d proof',
 'hoggar_qualification':h,'mub_qualification':m,'hoggar_source':hc,'mub_source':mc,
 'costs_seconds':{'Hoggar_qualification':hg_time,'MUB_qualification':mub_time,'exact_entropy_receivers':eval_time,'total':perf_counter()-start},
 'trust_boundary':'Gaussian integer products, Fraction operations, rational Sturm counts and directed log intervals. No numerical eigensolver/optimization.',
 'historical_priority':'UNKNOWN','quantum_memory_or_WHd_claim':False}
 (HERE/'FRAME_RECEIVERS.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'status':'PASS','costs_seconds':result['costs_seconds'],
 'Hoggar_gap':hc['entropy_contraction_defect']['display_only'],
 'Hoggar_scalar_relaxation':hc['sharp_scalar_purity_relaxation']['display_only'],
 'MUB_gap':mc['entropy_contraction_defect']['display_only']},indent=2))
if __name__=='__main__':main()
