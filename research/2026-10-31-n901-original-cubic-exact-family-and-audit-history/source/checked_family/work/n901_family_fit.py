"""Fit a parameter-uniform facial N901 certificate for r>=1.

Numerical preparation only. Positivity is imposed on every matrix
Bernstein coefficient after exact rational denominator clearing.
"""
from pathlib import Path
from math import comb
import pickle,sys,json,time
from fractions import Fraction as R
import numpy as np,sympy as s,cvxpy as cp
root=Path(__file__).resolve().parents[1];T=pickle.loads((root/'work/n901_parameter_template.pickle').read_bytes());r=T['r'];t=s.symbols('t');gp=T['Gram_pairs'];sol=T['solution'];free=T['free']
active=[0,2,3,5,7,8,10,11,13,16,18,20,21,23]
fexp=[-1,-1,-2,-1,-2,0,2,-1,-2,0,-3,-1,-1,0]
gexp=[0,1,0,-1,1,0,-1,0,-1,-1,-1,-2]
blocks=[[0,4,6,7,9,11],[1,2,3,5,8,10]]
def prepare():
 expr=[];den=s.Integer(1);minpower=0
 for i,j in gp:
  row=[];k=gp.index((i,j));scale=r**(-gexp[i]-gexp[j])
  for c in [-1]+active:
   e=sol[k][0]*scale if c==-1 else sol[k][c+1]*scale*r**fexp[active.index(c)]
   e=s.cancel(e.subs(r,1/t));nn,dd=s.fraction(e);D=s.Poly(dd,t);low=min((pw[0] for pw,co in D.terms() if co),default=0);dd=s.cancel(dd/t**low);den=s.lcm(den,dd);minpower=min(minpower,-low);row.append(e)
  expr.append(row)
 den=s.Poly(den,t).monic().as_expr();den=s.cancel(den/den.subs(t,1));data=[]
 for row in expr:
  data.append([s.Poly(s.cancel(e*den*t**(-minpower)),t) for e in row])
 maxdegree=max(p.degree() for row in data for p in row if p);print('den',s.factor(den),'Laurent minimum',minpower,'degree',maxdegree,flush=True)
 return {'den':den,'t':t,'minpower':minpower,'maxdegree':maxdegree,'data':data,'active':active,'fexp':fexp,'gexp':gexp,'blocks':blocks}
cache=root/'work/n901_family_kernel.pickle'
if cache.exists():K=pickle.loads(cache.read_bytes())
else:K=prepare();cache.write_bytes(pickle.dumps(K))
def solve(degree,elevate,upper=R(1)):
 start=time.perf_counter();minpower=K['minpower'];data=K['data'];N=K['maxdegree']+minpower+degree+elevate;u=cp.Variable(len(active)*(degree+1));margin=cp.Variable();constant=np.zeros((N-minpower+1,144));linear=np.zeros((N-minpower+1,144,len(active)*(degree+1)))
 for power in range(minpower,N+1):
  for k,(i,j) in enumerate(gp):
   co=float(data[k][0].nth(power-minpower)) if power>=minpower else 0
   constant[power-minpower,i*12+j]=constant[power-minpower,j*12+i]=co
   for a in range(len(active)):
    for l in range(degree+1):
     v=data[k][a+1].nth(power-minpower-l) if power-minpower-l>=0 else 0
     linear[power-minpower,i*12+j,a*(degree+1)+l]=linear[power-minpower,j*12+i,a*(degree+1)+l]=float(v)
 constraints=[]
 for power in range(minpower,0):constraints.append(constant[power-minpower]+linear[power-minpower]@u==0)
 for k in range(N+1):
  bc=sum((comb(k,p)/comb(N,p))*float(upper**p)*constant[p-minpower] for p in range(k+1));bl=sum((comb(k,p)/comb(N,p))*float(upper**p)*linear[p-minpower] for p in range(k+1));B=cp.reshape(bc+bl@u,(12,12),order='C')
  for block in blocks:constraints.append(B[np.ix_(block,block)]-margin*np.eye(6)>>0)
 # Keep the rationalization scale moderate without selecting a certificate
 # through a large arbitrary coefficient norm.
 objective=cp.Maximize(margin);prob=cp.Problem(objective,constraints)
 try:prob.solve(solver='CLARABEL',tol_gap_abs=1e-9,tol_gap_rel=1e-9,tol_feas=1e-10,max_iter=400)
 except cp.error.SolverError as err:return {'degree':degree,'elevation':elevate,'status':'SOLVER_FAILED','error':str(err)}
 return {'degree':degree,'elevation':elevate,'t_upper':str(upper),'Bernstein_degree':N,'status':prob.status,'margin':None if margin.value is None else float(margin.value),'u_coefficients':None if u.value is None else u.value.reshape(len(active),degree+1).tolist(),'seconds':time.perf_counter()-start,'active_free_positions':active,'free_scaling_exponents':fexp,'Gram_scaling_exponents':gexp}
if __name__=='__main__':
 degree=int(sys.argv[1]) if len(sys.argv)>1 else 3;elevate=int(sys.argv[2]) if len(sys.argv)>2 else 0;upper=R(sys.argv[3]) if len(sys.argv)>3 else R(1);suffix='' if upper==1 else '_t'+str(upper).replace('/','_');out=solve(degree,elevate,upper);(root/f'work/n901_family_fit_d{degree}_e{elevate}{suffix}.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='u_coefficients'}),flush=True)
