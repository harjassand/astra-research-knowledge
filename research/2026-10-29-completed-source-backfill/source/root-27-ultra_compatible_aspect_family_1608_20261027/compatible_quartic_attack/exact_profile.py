"""Exact integer/rational P1 moments and attained affine-background minimum."""
import json,pathlib,math,time
from fractions import Fraction as F
ROOT=pathlib.Path(__file__).resolve().parent
def clean(p):return {e:c for e,c in p.items()if c}
def add(*ps):
 out={}
 for p in ps:
  for e,c in p.items():out[e]=out.get(e,F(0))+c
 return clean(out)
def mul(p,q):
 out={}
 for e,c in p.items():
  for f,d in q.items():
   g=tuple(a+b for a,b in zip(e,f));out[g]=out.get(g,F(0))+c*d
 return clean(out)
def scale(p,c):return clean({e:v*c for e,v in p.items()})
def var(i):
 e=[0]*4;e[i]=1;return {tuple(e):F(1)}
def diff(p,i):
 out={}
 for e,c in p.items():
  if e[i]:z=list(e);z[i]-=1;out[tuple(z)]=c*e[i]
 return clean(out)
def polynomial():
 a,b,c,d=[var(i)for i in range(4)];u=add(mul(a,a),mul(c,c));v=add(mul(b,b),mul(d,d));w=add(mul(a,b),mul(c,d));q=add(mul(a,d),scale(mul(b,c),-1))
 p=list(map(F,json.loads((ROOT/'TARGET.json').read_text())['coefficients']))
 bases=[mul(u,u),mul(v,v),mul(u,v),mul(w,w),mul(u,w),mul(v,w),mul(q,u),mul(q,v),mul(q,w)]
 return add(*(scale(x,y)for x,y in zip(bases,p))),p
def solve_ldl(A,b):
 n=len(b);L=[[F(i==j)for j in range(n)]for i in range(n)];D=[]
 for j in range(n):
  d=A[j][j]-sum(L[j][k]**2*D[k]for k in range(j));assert d>0;D.append(d)
  for i in range(j+1,n):L[i][j]=(A[i][j]-sum(L[i][k]*D[k]*L[j][k]for k in range(j)))/d
 y=[]
 for i in range(n):y.append(b[i]-sum(L[i][j]*y[j]for j in range(i)))
 z=[y[i]/D[i]for i in range(n)];x=[F(0)]*n
 for i in reversed(range(n)):x[i]=z[i]-sum(L[j][i]*x[j]for j in range(i+1,n))
 assert all(sum(A[i][j]*x[j]for j in range(n))==b[i]for i in range(n))
 return x,D

def acquire(record,denominator=10**8):
 start=time.monotonic();n=record['mesh'];assert not record['alternating_diagonal']
 nodes=[[[round(float(x)*denominator)for x in v]for v in row]for row in record['normalized_nodes']]
 atoms=[]
 for i in range(n):
  for j in range(n):
   v0=nodes[i][j];v1=nodes[(i+1)%n][j];v2=nodes[(i+1)%n][(j+1)%n];v3=nodes[i][(j+1)%n]
   atoms.append(tuple(n*x for o in range(2)for x in [v1[o]-v0[o],v2[o]-v1[o]]))
   atoms.append(tuple(n*x for o in range(2)for x in [v2[o]-v3[o],v3[o]-v0[o]]))
 N=len(atoms);assert N==2*n*n
 assert all(sum(x[i]for x in atoms)==0 for i in range(4))
 assert sum(x[0]*x[3]-x[1]*x[2]for x in atoms)==0
 f,p=polynomial();df=[diff(f,i)for i in range(4)];hh=[[diff(df[i],j)for j in range(4)]for i in range(4)]
 needed=set(f)
 for q in df:needed.update(q)
 for row in hh:
  for q in row:needed.update(q)
 # Include all quadratic moments and the fourth power of the Euclidean norm.
 norm2=add(*(mul(var(i),var(i))for i in range(4)));norm4=mul(norm2,norm2);needed.update(norm4)
 sums={e:0 for e in needed}
 for x in atoms:
  powers=[[1,z,z*z,z*z*z,z**4]for z in x]
  for e in needed:sums[e]+=math.prod(powers[i][e[i]]for i in range(4))
 moments={e:F(v,N*denominator**sum(e))for e,v in sums.items()}
 def average(poly):return sum(c*moments[e]for e,c in poly.items())
 c=average(f);b=[average(q)for q in df];H=[[average(q)for q in row]for row in hh]
 v,pivots=solve_ldl(H,b);loss=sum(x*y for x,y in zip(b,v))/2;gap=c-loss;m2=average(norm2);m4=average(norm4)
 # Acoustic certificate rho=1/200000 implies this lower matrix bound for
 # compatible covariance; verify it independently on this exact profile.
 _,shiftp=solve_ldl([[H[i][j]-(m2/F(200000)if i==j else 0)for j in range(4)]for i in range(4)],[F(0)]*4)
 A,B,C,E,G,Hc,L,M,Nc=p;assert A==B and G==Hc==Nc==0
 gamma=-E;ell=abs((L-M)/2)+abs((L+M)/2);kappa=A-ell*ell/(4*gamma);assert gamma>0 and kappa>0
 assert c>=kappa*m4
 ratio=loss/c
 result={'status':'EXACT_COMPATIBLE_P1_PROFILE_ACQUIRED','mesh':n,'node_denominator':denominator,'integer_nodes':nodes,
  'target_coefficients':list(map(str,p)),'L_plus_M_exact':str(L+M),
  'mean_gradient':'0','mean_determinant':'0','triangle_count':len(atoms),
  'c':str(c),'b':list(map(str,b)),'H':[[str(z)for z in row]for row in H],
  'positive_H_LDL_pivots':list(map(str,pivots)),'strict_acoustic_shift_LDL_pivots':list(map(str,shiftp)),
  'background_minimizer':list(map(str,[-z for z in v])),'optimized_gap':str(gap),'Schur_loss':str(loss),
  'Delta_over_c':str(gap/c),'Delta_over_M4':str(gap/m4),'Schur_loss_over_c':str(ratio),
  'pointwise_coercivity_kappa':str(kappa),'fourth_moment':str(m4),'second_moment':str(m2),
  'genuine_negative_Jensen_witness':gap<0,'compatible_scaling_curve_nonconvex':ratio>F(2,3),
  'scaling_curve_second_derivative_at_loss_over_2c':str(loss*(2-3*ratio)),
  'seconds':time.monotonic()-start,'scope':'One actual periodic P1 profile and all its affine backgrounds/scalings, via exact deflation. Positive gap is not a global QC proof.'}
 return result
def run():
 p=ROOT/'data/schur_refinement.json'
 if p.exists():
  d=json.loads(p.read_text());last=d['levels'][-1];r=min(last['runs'],key=lambda r:r['Delta_over_c'])
 else:
  d=json.loads((ROOT/'data/schur_ratio_search.json').read_text());r=min((r for r in d['runs']if r['kind']=='fem'),key=lambda r:r['Delta_over_c'])
 result=acquire(r);(ROOT/'data/EXACT_COMPATIBLE_PROFILE.json').write_text(json.dumps(result,indent=2))
 print({k:result[k]for k in ['status','mesh','genuine_negative_Jensen_witness','compatible_scaling_curve_nonconvex','seconds']})
 print('Delta/c',float(F(result['Delta_over_c'])),'loss/c',float(F(result['Schur_loss_over_c'])))
 return result
if __name__=='__main__':run()
