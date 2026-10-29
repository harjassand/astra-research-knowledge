#!/usr/bin/env python3
"""Exact independent checks for root's clock-capped realization theorem.

No samples, source queries, floating point in mathematical controls, or
optimization library. Every constructed full generator is checked directly.
"""
from fractions import Fraction as F
from pathlib import Path
import json,time

OUT=Path(__file__).resolve().parent

def dot(a,b):return sum((x*y for x,y in zip(a,b)),F())
def solve(a,b):
 if not b:return []
 n=len(b);u=[list(a[i])+[b[i]] for i in range(n)]
 for j in range(n):
  r=next(i for i in range(j,n) if u[i][j]);u[j],u[r]=u[r],u[j]
  p=u[j][j];u[j]=[z/p for z in u[j]]
  for i in range(n):
   if i!=j:
    p=u[i][j];u[i]=[x-p*y for x,y in zip(u[i],u[j])]
 answer=[u[i][-1] for i in range(n)]
 assert all(dot(row,answer)==v for row,v in zip(a,b))
 return answer
def sub(a,ii,jj=None):
 if jj is None:jj=ii
 return [[a[i][j] for j in jj] for i in ii]

def psi(x,f,cap):
 assert x>=0 and f>=0 and cap>0
 if not f:
  if not x:return F()
  raise ValueError('positive residence without channel flow')
 z=cap*x/f;n=z.__floor__()
 return f/cap**2*(n+1)*(2*z-n)

class Builder:
 def __init__(self,wb):self.w=list(wb);self.edges=[];self.m=len(wb)
 def edge(self,i,j,f):
  if not f:return
  assert i!=j and f>0,'no instantaneous self jumps'
  self.edges.append((i,j,f))
 def phase(self,flow,rate):
  assert flow>0 and rate>0
  idx=len(self.w);self.w.append(flow/rate);return idx
 def adjacent(self,i,j,flow,mass,cap):
  if not flow:assert not mass;return
  z=cap*mass/flow;n=z.__floor__();theta=z-n
  if n==0:
   self.edge(i,j,flow*(1-theta))
   if theta:
    k=self.phase(flow*theta,cap)
    self.edge(i,k,flow*theta);self.edge(k,j,flow*theta)
   return
  previous=i
  for unused in range(n):
   k=self.phase(flow,cap);self.edge(previous,k,flow);previous=k
  self.edge(previous,j,flow*(1-theta))
  if theta:
   k=self.phase(flow*theta,cap)
   self.edge(previous,k,flow*theta);self.edge(k,j,flow*theta)
 def zero_exponential(self,i,j,flow,mu,q):
  assert i!=j and mu>0 and q>=2*mu*mu
  rate=2*mu/q;p=mu*rate;assert 0<p<=1
  self.edge(i,j,flow*(1-p))
  k=self.phase(flow*p,rate);self.edge(i,k,flow*p);self.edge(k,j,flow*p)
  return rate
 def off_with_second(self,i,j,flow,mass,q,cap):
  mu=mass/flow;q0=psi(mass,flow,cap)/flow
  assert q>=q0 and mu>0
  q_exp=2*mu/min(cap,1/mu)
  if q==q0:self.adjacent(i,j,flow,mass,cap);return
  if q<q_exp:
   alpha=(q-q0)/(q_exp-q0)
   self.adjacent(i,j,flow*(1-alpha),mass*(1-alpha),cap)
   rate=self.zero_exponential(i,j,flow*alpha,mu,q_exp)
   assert rate<=cap
  else:
   rate=self.zero_exponential(i,j,flow,mu,q);assert rate<=cap
 def diagonal_with_contribution(self,i,mass,capacity,C,cap):
  assert mass>0 and capacity>0
  f0=min(capacity,cap*mass);C0=psi(mass,capacity,cap)/2
  Cexp=mass*mass/f0;assert C>=C0
  if C==C0:self.adjacent(i,i,f0,mass,cap);return
  if C<Cexp:
   alpha=(C-C0)/(Cexp-C0);mu=mass/f0
   self.adjacent(i,i,f0*(1-alpha),mass*(1-alpha),cap)
   k=self.phase(f0*alpha,1/mu)
   self.edge(i,k,f0*alpha);self.edge(k,i,f0*alpha)
  else:
   flow=mass*mass/C;rate=mass/C
   assert flow<=capacity and rate<=cap
   k=self.phase(flow,rate);self.edge(i,k,flow);self.edge(k,i,flow)
 def finish(self,hidden_cap,port_caps):
  n=len(self.w);L=[[F()]*n for unused in range(n)]
  for i,j,f in self.edges:L[i][i]+=f;L[i][j]-=f
  assert all(sum(row)==0 for row in L)
  assert all(sum(L[i][j] for i in range(n))==0 for j in range(n))
  rates=[L[i][i]/self.w[i] for i in range(n)]
  assert all(0<rates[i]<=port_caps[i] for i in range(self.m))
  assert all(0<rate<=hidden_cap for rate in rates[self.m:])
  for start in range(n):
   reached={start};todo=[start]
   while todo:
    i=todo.pop()
    for j in range(n):
     if L[i][j]<0 and j not in reached:reached.add(j);todo.append(j)
   assert len(reached)==n
  return {'L':L,'w':self.w,'m':self.m,'rates':rates}

def record(model):
 L=model['L'];w=model['w'];m=model['m'];ii=list(range(m,len(w)))
 G=sub(L,ii);wi=[w[i] for i in ii];t=solve(G,wi)
 H=[solve(G,[-L[i][j] for i in ii]) for j in range(m)]
 K=[solve(G,[wi[z]*H[j][z] for z in range(len(ii))]) for j in range(m)]
 flows=[[F()]*m for unused in range(m)];M=[[F()]*m for unused in range(m)]
 for i in range(m):
  incoming=[-L[i][j] for j in ii]
  for j in range(m):
   flows[i][j]=(-L[i][j] if i!=j else F())+dot(incoming,H[j])
   M[i][j]=dot(incoming,K[j])
 s=[L[i][i] for i in range(m)]
 assert [sum(row) for row in flows]==s
 assert [sum(flows[i][j] for i in range(m)) for j in range(m)]==s
 S=[[F(i==j)*s[i]-flows[i][j] for j in range(m)] for i in range(m)]
 vR=[sum(row) for row in M];vL=[sum(M[i][j] for i in range(m)) for j in range(m)]
 bR=[w[i]+vR[i] for i in range(m)];bL=[w[i]+vL[i] for i in range(m)]
 c=dot(wi,t)
 return {'F':flows,'M':M,'S':S,'wB':w[:m],'vR':vR,'vL':vL,'bR':bR,'bL':bL,'c':c,'mass':sum(w)}

def check_targets(model,r):
 m=model['m'];results=[]
 for mask in range(1,1<<m):
  target=[i for i in range(m) if mask>>i&1];live=[i for i in range(len(model['w'])) if i not in target]
  wb=[model['w'][i] for i in live];h=solve(sub(model['L'],live),wb)
  exact=dot(wb,h)/sum(wb)
  ports=[i for i in range(m) if i not in target]
  reduced_h=solve(sub(r['S'],ports),[r['bR'][i] for i in ports])
  reduced=(r['c']+dot([r['bL'][i] for i in ports],reduced_h))/(r['mass']-sum(r['wB'][i] for i in target))
  assert exact==reduced
  assert all(dict(zip(live,h))[i]==reduced_h[j] for j,i in enumerate(ports))
  results.append({'target':target,'equilibrium_mean':exact,'boundary_means':dict(zip(ports,reduced_h))})
 return results

def serialize(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,list):return [serialize(v) for v in x]
 if isinstance(x,dict):return {str(k):serialize(v) for k,v in x.items()}
 return x

def main():
 start=time.perf_counter();cap=F(2);wb=[F(2),F(3)];portcaps=[F(1),F(1)]
 M=[[F(1,4),F(3,4)],[F(1,3),F(3,2)]]
 flows=[[F(),F(1)],[F(1),F()]];a=[F(1),F(2)]
 # Complete 2x2 transport parameterization; endpoints and every breakpoint.
 def obj(t):return psi(t,a[0],cap)+psi(1-t,F(1),cap)+psi(F(7,12)-t,F(1),cap)+psi(F(5,4)+t,a[1],cap)
 breakpoints=[F(),F(1,12),F(1,2),F(7,12)]
 costs=[obj(t) for t in breakpoints];J=min(costs)
 assert J==F(43,12) and obj(F(1,4))==J
 # Convexity plus complete linear breakpoints proves this global optimum.
 records=[]
 for extra in [F(),F(1,64),F(7,8)]:
  b=Builder(wb)
  b.adjacent(0,0,min(a[0],cap*M[0][0]),M[0][0],cap)
  b.off_with_second(0,1,F(1),M[0][1],psi(M[0][1],F(1),cap)+2*extra,cap)
  b.adjacent(1,0,F(1),M[1][0],cap)
  b.adjacent(1,1,min(a[1],cap*M[1][1]),M[1][1],cap)
  model=b.finish(cap,portcaps);r=record(model)
  assert r['M']==M and r['c']==J/2+extra
  assert r['S']==[[F(1),F(-1)],[F(-1),F(1)]]
  assert r['F']==[[F(1,2),F(1)],[F(1),F(2)]]
  assert model['rates'][:2]==[F(3,4),F(1)]
  records.append({'extra_c':extra,'state_count':len(model['w']),'record':r,'rates':model['rates'],
                  'stationary_weights':model['w'],'full_L':model['L'],'targets':check_targets(model,r)})
 # Diagonal boundary: attaining a larger c may require decreasing the native
 # port clock; its ceiling, rather than exact rate, is retained by the theorem.
 diagonal=[]
 for mass,capacity,C in [(F(1),F(2),F(1,2)),(F(1),F(2),F(2)),
                         (F(1),F(1),F(7,8)),(F(1),F(1),F(4))]:
  b=Builder([F(1)]);b.diagonal_with_contribution(0,mass,capacity,C,cap)
  model=b.finish(cap,[capacity]);r=record(model)
  assert r['vR']==r['vL']==[mass] and r['c']==C and r['S']==[[F()]]
  diagonal.append({'mass':mass,'port_cap':capacity,'c':C,'actual_port_rate':model['rates'][0],
                   'hidden_rates':model['rates'][1:],'states':len(model['w']),
                   'full_L':model['L'],'stationary_weights':model['w'],'targets':check_targets(model,r)})
 witness=[]
 for n in [1,2,3,7,16]:
  native_c=(1+F(1,n))/2
  for ratecap in [F(n,2),F(n)-F(1,3),F(n),F(n)+F(1,3),F(2*n)]:
   minimum=psi(F(1),F(1),ratecap)/2
   feasible=minimum<=native_c
   assert feasible==(ratecap>=n)
   witness.append({'n':n,'hidden_rate_cap':ratecap,'c_source':native_c,'minimum_c':minimum,'feasible':feasible})
  b=Builder([F(1),F(1)]);b.adjacent(0,1,F(1),F(1),F(n));b.adjacent(1,0,F(1),F(),F(n))
  model=b.finish(F(n),[F(1),F(1)]);r=record(model)
  assert r['c']==native_c and r['vR']==[F(1),F()] and r['vL']==[F(),F(1)]
  check_targets(model,r)
 result={'status':'PASS','arithmetic':'exact rational mathematical controls','RNG_calls':0,'source_calls':0,
  'transport_2x2':{'feasible_parameter_interval':[F(),F(7,12)],'complete_breakpoints':breakpoints,
                   'breakpoint_costs':costs,'minimizer_interval':[F(1,12),F(1,2)],'J_cap':J},
  'fractional_optimizer_and_inflations':records,'diagonal_port_clock_boundary':diagonal,
  'erlang_witness_caps':witness,'witness_full_generators_checked':5,
  'degenerate_input_counterexample':{'S':[[F(1),F(-1)],[F(-1),F(1)]],
   'wB':[F(1),F(1)],'vR':[F(),F()],'vL':[F(),F()],
   'hidden_cap':F(1),'port_caps':[F(1),F(1)],'supplied_c':F(1),'Jcap':F(),
   'passes_uncorrected_inequality':True,
   'impossibility':'The prescribed sum(vR)=0 equals total hidden stationary mass, so no positive hidden state exists; c must be 0.'},
  'fixed_native_port_clock_boundary':{'ports':1,'wB':F(1),'hidden_mass':F(1),
   'hidden_cap':F(2),'port_cap':F(2),'exact_native_port_rate_if_imposed':F(2),
   'then_required_c':F(1,2),'larger_c_constructed_under_cap':F(2),
   'construction_port_rate':F(1,2),
   'explanation':'At exact native flow 2, mean interior duration 1/2 is the minimum at hidden rate cap 2; the duration must be a single Exp(2), forcing c=1/2.'},
  'scope':'Supplied exact mean records, mathematical clock ceilings, and constructed finite CTMCs; no acquisition or physical realization claim.',
  'wall_seconds':time.perf_counter()-start}
 (OUT/'CLOCK_CEILING_CONSTRUCTION_CHECKS.json').write_text(json.dumps(serialize(result),indent=2)+'\n')
 print(json.dumps({'status':'PASS','fractional_optimizer_c':str(J/2),'optimizer_and_inflation_generators':len(records),
                   'diagonal_generators':len(diagonal),'erlang_cap_comparisons':len(witness),
                   'full_erlang_generators':5,'wall_seconds':result['wall_seconds']},indent=2))

if __name__=='__main__':main()
