"""Exact code-pairing certificate and synthetic causal-filter readout check.
Balanced independent phase signs act physically before the detector filter.
"""
from pathlib import Path
from collections import Counter
import json,numpy as np
from thermal_bridge import lyap,expm,adj
ROOT=Path(__file__).resolve().parent

def surviving_pairs(lag,taps):
 # j=lag,k=0. The coefficient is E eps_j eps_k eps_{j-l} eps_{k-m}.
 out=[]
 for l in taps:
  for m in taps:
   c=Counter([lag,0,lag-l,-m])
   if all(v%2==0 for v in c.values()):out.append([l,m])
 return out

def main():
 for m in range(1,8):assert surviving_pairs(m,list(range(12)))==[[0,0]]
 assert surviving_pairs(1,[-1,0,1,2])==[[0,0],[1,-1]]
 rng=np.random.default_rng(23102626);n=2;N=300000;dt=.2;I=np.eye(n);G=-.5*I-1j*np.array([[0,.3],[.3,0]]);C=lyap(G,np.diag([.1,.02]));M=expm(G*dt)
 def sqrtp(A):
  w,V=np.linalg.eigh((A+adj(A))/2);return V*np.sqrt(np.maximum(w,0))
 def complexn(shape):return (rng.normal(size=shape)+1j*rng.normal(size=shape))/np.sqrt(2)
 X=np.empty((N,n),complex);W=np.empty_like(X);LX=sqrtp(C-M@C@adj(M));P=.1*I;LW=sqrtp(P-M@P@adj(M));X[0]=sqrtp(C)@complexn((n,));W[0]=sqrtp(P)@complexn((n,));ix=complexn((N-1,n))@LX.T;iw=complexn((N-1,n))@LW.T
 for k in range(1,N):X[k]=M@X[k-1]+ix[k-1];W[k]=M@W[k-1]+iw[k-1]
 # Correlated unmodulated nuisance is allowed by the code identity.
 Z=.4*X+W;eps=rng.choice([-1.,1.],N);H={0:np.array([[.6,.1],[0,.5]]),1:np.array([[.3,.1],[.05,.2]]),2:np.array([[0,.1],[-.1,.2]])};Hm=np.array([[.2,.07],[.1,.13]])
 Y=Z.copy()
 for l,h in H.items():Y[l:]+=(eps[:N-l,None]*X[:N-l])@h.T
 Ytwo=Y.copy();Ytwo[:-1]+=(eps[1:,None]*X[1:])@Hm.T
 D=eps[:,None]*Y;Dtwo=eps[:,None]*Ytwo
 def lagcov(V,k):return V[k+3:-3].T@V[3:-3-k].conj()/(N-k-6)
 rows=[]
 for k in [1,2,3]:
  target=H[0]@np.linalg.matrix_power(M,k)@C@adj(H[0]);hat=lagcov(D,k);tw=lagcov(Dtwo,k);extra=(H[k]@adj(np.linalg.matrix_power(M,k)@C)@adj(Hm)) if k==1 else np.zeros((n,n))
  rows.append({'lag':k,'causal_estimator_error_F':float(np.linalg.norm(hat-target)),'two_sided_error_if_incorrectly_assumed_causal':float(np.linalg.norm(tw-target)),'two_sided_corrected_formula_error_F':float(np.linalg.norm(tw-target-extra)),'predicted_noncausal_cross_term_F':float(np.linalg.norm(extra))})
 out={'status':'Exact Rademacher coefficient check plus correlated synthetic trace; no detector experiment','seed':23102626,'frames':N,'dt':dt,'causal_survivors':{str(k):surviving_pairs(k,list(range(12))) for k in [1,2,3]},'two_sided_lag1_survivors':surviving_pairs(1,[-1,0,1,2]),'theorem':'For Yk=sum_l>=0 H_l eps_{k-l} X_{k-l}+Zk, iid balanced signs independent of entire joint pre-code X,Z, positive-lag demod covariance is H0 GammaX(m) H0^dagger. X/Z correlation allowed. No need to commute filtering and demodulation.','scope':['Stable summable causal discrete LTI filter or finite FIR','Full-rank nonzero current tap for full-state recovery; known pure delay can be aligned','This is a sampled/held prefilter signal model. Continuous within-exposure dynamics need an exposure-aware feature model.','No code-dependent state evolution, feedback, sensor law or switching transients','Noncausal filters retain crossed term H_m GammaX(-m) H_-m^dagger','No finite-sample guarantee follows from exact coefficient cancellation'],'thermal_metric_from_positive_lags':'If a complete thermal occupation shift gives DeltaC=Delta_n I and H0 invertible, DeltaGamma_m=T^m M_eff Delta_n; T=DeltaGamma_(m+1) DeltaGamma_m^-1 and M_eff=T^-m DeltaGamma_m/Delta_n. Zero-lag detector memory does not supply this metric.','imperfect_two_state_modulation':'For stable repeatable physical maps A+B eps before the filter, balanced demodulation selects H0 B as the effective signal map; an uncoded A channel vanishes from positive-lag code projection but increases variance. Unknown B needs calibration.','rows':rows}
 (ROOT/'causal_filter_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
