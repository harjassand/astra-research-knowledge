"""Exact rational checks of synthetic thermal-projection witnesses."""
import json,math,importlib.util
from fractions import Fraction as F
from pathlib import Path
root=Path(__file__).parent
spec=importlib.util.spec_from_file_location('capacity_exact',root/'capacity_geometry_exact.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);solve=mod.solve_exact
def zero(n):return [[F(0) for _ in range(n)] for _ in range(n)]
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def enc(x):return {'fraction':str(x),'decimal':float(x)}
def evaluate(inp):
 n=inp['states'];N=2*n;Q=zero(N);r=[F(0)]*N
 edges=[(x,y,F(str(kp)),F(str(km)),d) for x,y,kp,km,d in inp['edges']]
 gamma=F(str(inp['gamma']));R=F(str(inp['R']))
 for x,y,kp,km,d in edges:
  assert kp/km==R**d
  Q[x][y]+=kp;Q[y][x]+=km;Q[x][x]-=kp;Q[y][y]-=km;r[x]+=kp*d;r[y]-=km*d
 for i in range(n):
  x,y=2*i,2*i+1;Q[x][y]+=gamma;Q[y][x]+=gamma;Q[x][x]-=gamma;Q[y][y]-=gamma
 M=[list(row) for row in zip(*Q)];M[-1]=[F(1)]*N;z=[F(0)]*N;z[-1]=F(1);pi=solve(M,z)
 assert min(pi)>0 and sum(pi)==1
 assert all(sum(pi[i]*Q[i][j] for i in range(N))==0 for j in range(N))
 Kg=[[[sum(Q[2*i+g][2*j:2*j+2]) for j in range(n)] for g in range(2)] for i in range(n)]
 K=[[sum(Kg[i][g][j] for g in range(2))/2 for j in range(n)] for i in range(n)]
 rb=[(r[2*i]+r[2*i+1])/2 for i in range(n)]
 M=[list(row) for row in zip(*K)];M[-1]=[F(1)]*n;z=[F(0)]*n;z[-1]=F(1);mut=solve(M,z)
 J=dot(pi,r);Jth=dot(mut,rb)
 M=[row[:] for row in K];M[-1]=[F(1)]*n;z=[Jth-v for v in rb];z[-1]=F(0);h=solve(M,z)
 assert all(dot(K[i],h)==Jth-rb[i] for i in range(n))
 w=[r[2*i+1]-r[2*i]+dot([Kg[i][1][j]-Kg[i][0][j] for j in range(n)],h) for i in range(n)]
 mu=[pi[2*i]+pi[2*i+1] for i in range(n)];p=[pi[2*i+1]/mu[i] for i in range(n)]
 defect=sum(mu[i]*(p[i]-F(1,2))*w[i] for i in range(n));assert defect==J-Jth
 V=sum(mu[i]*w[i]**2/(8*gamma) for i in range(n));Vm=max(wi**2/(8*gamma) for wi in w)
 A=math.log(float(R));sigma=A*float(J);kappa=A*float(Vm/Jth)
 return {'synthetic':True,'affinity':'log('+str(R)+')','all_rate_ratio_stationarity_and_Poisson_identities_exact':True,
  'edges':[[x,y,str(kp),str(km),d] for x,y,kp,km,d in edges],
  'pi':[str(x) for x in pi],'chemical_mu':[str(x) for x in mu],'gate_conditionals':[str(x) for x in p],
  'poisson_h':[str(x) for x in h],'w':[enc(x) for x in w],'J':enc(J),'Jth':enc(Jth),'gain':enc(J/Jth),
  'Vmu':enc(V),'Vmax':enc(Vm),'kappa_max':kappa,'gain_bound_max':1+kappa/2+math.sqrt(kappa+kappa*kappa/4),
  'absolute_bound_mu':math.sqrt(sigma*float(V)),'positive_absolute_change':float(J-Jth),
  'bound_tightness_mu':float((J-Jth)**2/V)/sigma}
def main():
 data=json.loads((root/'projection_positive_search_result.json').read_text());result={k:evaluate(v) for k,v in data.items()}
 (root/'projection_exact_witnesses_results.json').write_text(json.dumps(result,indent=2)+'\n')
 for k,r in result.items():print(k,{x:r[x] for x in ['J','Jth','gain','gain_bound_max','absolute_bound_mu','bound_tightness_mu']})
if __name__=='__main__':main()
