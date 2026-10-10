"""Independent dense-transition-matrix validation for nonlinear stratified sampler."""
import random,time
import numpy as np
from collections import Counter
from scipy.stats import chi2
from stratified_entropy_sampler import StratifiedModel,sample_states,sample_coordinates,evolve

M=StratifiedModel(
 n=2,c=3,q=2,s='0.19',r='0.08', parents={0:(0,1,1),1:(0,0,1)},
 coeffs=lambda i,h:(1,(h+i)%2,1),
 forcing=lambda i,h,rows: ((i+1)%2 if h==0 else
       (rows[0][0]*rows[1][0] + rows[2][0])%2 if h==1 else
       (rows[0][0]*rows[1][1] + rows[1][0]*rows[2][1] + (rows[2][0]&rows[1][0]))%2),
 residual=(1,0,1))
M.validate()


def to_state(z):
 return (tuple((z>>k)&1 for k in range(3)),tuple((z>>(3+k))&1 for k in range(3)))

def to_index(states):
 return sum(int(states[i][k]) << (3*i+k) for i in range(2) for k in range(3))

def gate(site,old):
 parents=M.input_sites(site)
 ans=[]
 for h in range(M.c):
  same=sum(x*old[p][h] for x,p in zip(M.layer_coeffs(site,h),parents))
  low=M.layer_forcing(site,h,[tuple(old[p][:h]) for p in parents])
  ans.append((same+low)%M.q)
 return tuple(ans)


def exact_transition_matrix():
 P=np.zeros((64,64))
 s,r=float(M.s),float(M.r)
 for j in range(64):
  old=to_state(j)
  rows=[]
  for i in range(2):
   probs=np.ones(8)*s/8
   resid=sum(x<<h for h,x in enumerate(M.residual_state(i)))
   gate_i=sum(x<<h for h,x in enumerate(gate(i,old)))
   probs[resid]+=r
   probs[gate_i]+=(1-s-r)
   rows.append(probs)
  P[j,:]=np.kron(rows[1],rows[0])
 assert np.max(abs(P.sum(axis=1)-1))<1e-13
 return P

def dense_stationary(P):
 A=P.T-np.eye(64)
 A[-1,:]=1
 b=np.zeros(64);b[-1]=1
 pi=np.linalg.solve(A,b)
 assert np.all(pi>0) and max(abs(pi@P-pi))<1e-12
 return pi


def chi2_stat(observed,expected):
 val=sum((c-e)**2/e for c,e in zip(observed,expected) if e>0)
 return val,float(chi2.sf(val,len(observed)-1))


def main():
 P=exact_transition_matrix();pi=dense_stationary(P)
 print('EXACT reference: stationary residual',max(abs(pi@P-pi)),'min mass',min(pi))
 rng=random.Random(20261010)
 draws=24000
 counts=np.zeros(64,dtype=int); all_onsite=[]; times=[]
 t0=time.monotonic()
 sum_ev=0;sum_parents=0
 for j in range(draws):
  ss,diag=sample_states(M,[(0,0),(1,0)],rng,True)
  ind=to_index((ss[(0,0)],ss[(1,0)]))
  counts[ind]+=1
  sum_ev+=diag['fresh_events'];sum_parents+=diag['parent_lookups']
  if j<3000: all_onsite.append((ss[(0,0)],ss[(1,0)]))
 stat,pval=chi2_stat(counts,draws*pi)
 print('N=2, c=3, q=2 full 64-category: draws',draws,'chi2',round(stat,3),'p',pval,'TV empirical',round(sum(abs(counts/draws-pi))/2,5))
 print('resource mean: fresh',round(sum_ev/draws,3),'parents',round(sum_parents/draws,3),'time',round(time.monotonic()-t0,2),'s')
 for k in range(3):
  exact=sum(pi[j] for j in range(64) if to_state(j)[0][k]==to_state(j)[1][k])
  observed=sum(to_state(j)[0][k]==to_state(j)[1][k] for j in range(64) for _ in range(counts[j]))/draws
  print('site coordination layer',k,'exact',round(exact,6),'empirical',round(observed,6))
 # Check many-time correlation: P(X_{0,0}^2=1 and X_{1,-1}^1=1)
 exact=sum(pi[j]*P[j,i] for j in range(64) for i in range(64) if to_state(j)[1][1]==1 and to_state(i)[0][2]==1)
 n2=7000;seen=0
 for z in range(n2):
  x=sample_coordinates(M,[(0,0,2),(1,-1,1)],rng)
  seen+=int(x==[1,1])
 print('cross-time nonlinear joint: exact',round(exact,7),'observed',round(seen/n2,7),'draws',n2)
 # Large implicit nonlinear network, accesses do not scale in N
 big=StratifiedModel(n=1_000_000,c=3,q=2,s='0.20',r='0.02',
  parents=lambda i:tuple((i*2654435761+(h+1)*761 + h*h*37)%1_000_000 for h in range(3)),
  coeffs=lambda i,h:tuple((i//(h+1)+k+h)%2 for k in range(3)),
  forcing=lambda i,h,rows: (i%2 if h==0 else
   (rows[0][0]*rows[1][0]+rows[2][0]*rows[0][0])%2 if h==1 else
   (rows[0][1]*rows[1][0]+rows[1][1]*rows[2][0]*rows[0][0])%2),
  residual=(0,1,1))
 big.validate()
 nb=60
 t0=time.monotonic();s=0;m=0
 for _ in range(nb):
  val,info=sample_states(big,[(123,0),(987654,0)],rng,True)
  s+=info['fresh_events'];m+=info['parent_lookups']
 print('N=1e6 nonlinear stratified (2 joint sites): fresh',round(s/nb,2),'parent lookups',round(m/nb,2),'wall',round(time.monotonic()-t0,2),'s')
 print('PASS independent exact transition checks')

if __name__=='__main__':main()
