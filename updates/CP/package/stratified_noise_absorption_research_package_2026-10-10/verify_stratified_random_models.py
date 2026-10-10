"""Randomized adversarial model battery with independent full-state Markov reference.

N=2 sites, c=2 levels over F2, 16 global states. For each seeded
nonlinear network, compute its full transition matrix and stationary law,
then compare 1500 joint exact-sampler draws using chi-square calibration.
"""
import random
import numpy as np
from scipy.stats import chi2
from stratified_entropy_sampler import StratifiedModel,sample_states


def main():
 rng=random.Random(157101)
 num_models=32
 total_p=[]
 worst=(None,1.0)
 allstat=0
 worst_tv=0
 for rep in range(num_models):
  pp={i:tuple(rng.randrange(2) for _ in range(4)) for i in range(2)}
  cc={(i,h):tuple(rng.randrange(2) for _ in range(4)) for i in range(2) for h in range(2)}
  # Complete truth tables of Boolean lower forcing from all 4 parent level-0 inputs;
  # allows non-monotone functions of repeated-parent dependent coordinates.
  ff={(i,h):tuple(rng.randrange(2) for _ in range(16)) for i in range(2) for h in range(2)}
  rr=tuple(rng.randrange(2) for _ in range(2))
  s= rng.choice([.05,.12,.30,.53])
  r= rng.choice([.01,.07,.18])
  model=StratifiedModel(n=2,c=2,q=2,s=str(s),r=str(r),
        parents=pp,
        coeffs=lambda i,h:cc[(i,h)],
        forcing=lambda i,h,v:ff[(i,h)][0 if h==0 else sum(int(v[j][0])<<j for j in range(4))],
        residual=rr)
  model.validate()

  def state(z):return ((z&1,(z>>1)&1),((z>>2)&1,(z>>3)&1))
  def output_gate(i,ss):
   inputs=pp[i]
   return tuple((sum(cc[(i,h)][j]*ss[inputs[j]][h] for j in range(4)) +
             ff[(i,h)][0 if h==0 else sum(ss[inputs[j]][0]<<j for j in range(4))])%2 for h in range(2))
  P=np.empty((16,16))
  for x in range(16):
   old=state(x)
   D=[]
   for i in range(2):
    prob=np.ones(4)*s/4
    residual_int=rr[0]+2*rr[1]
    g=output_gate(i,old)
    gate_int=g[0]+2*g[1]
    prob[residual_int]+=r
    prob[gate_int]+=1-s-r
    D.append(prob)
   P[x,:]=np.kron(D[1],D[0])
  B=P.T-np.eye(16); B[-1,:]=1
  rhs=np.zeros(16); rhs[-1]=1
  pi=np.linalg.solve(B,rhs)
  assert np.min(pi)>0 and np.max(np.abs(pi@P-pi))<1e-10
  obs=np.zeros(16,dtype=int)
  n=1500
  sampler_rng=random.Random(100*rep+37)
  for _ in range(n):
   v=sample_states(model,[(0,0),(1,0)],sampler_rng)
   a=v[(0,0)];b=v[(1,0)]
   z=a[0]+2*a[1]+4*b[0]+8*b[1]
   obs[z]+=1
  exp=n*pi
  X=sum((obs-exp)**2/exp)
  pval=float(chi2.sf(X,15))
  tv=.5*np.sum(abs(obs/n-pi))
  total_p.append(pval)
  allstat+=X
  worst_tv=max(worst_tv,tv)
  if pval<worst[1]:worst=(rep,pval)
 print('Models',num_models,'full independent transition matrices 16x16, joint draws',1500*num_models)
 print('Chi-square mean statistic',round(allstat/num_models,3),'expected 15')
 print('P values below 0.05',sum(p<.05 for p in total_p),'expected 1.6')
 print('Worst calibrated p value:',worst,'maximum empirical histogram TV',round(worst_tv,4))
 print('All p values:',','.join(f'{v:.3f}' for v in total_p))
 print('PASS random-model battery (statistical, not proof)')

if __name__=='__main__':main()
