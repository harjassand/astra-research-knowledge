"""Scaled shifted-barrier scalar resistance for the explicitly reconstructed current."""
from fractions import Fraction as F
import positive_integrals as p
core=p.old.core
class Shifted(core.Scalar):
 def __init__(self,*args,abar):super().__init__(*args);self.abar=abar;self.vstar=1+self.kappa
 def point(self,y,kind):
  if kind!='shifted':return super().point(y,kind)
  key=(y,kind)
  if key in self.cache:return self.cache[key]
  if len(self.cache)>=self.max_points:raise p.Unknown('shifted scalar-point budget')
  if not 0<=y<=F(1,2):raise p.Unknown('shifted slab domain')
  v=1+self.kappa*(1-y*y)**2;den=2*self.abar-v
  if den<=0:raise p.Unknown('positive shifted-flux density denominator')
  ans=self.power(self.abar*self.abar/(self.vstar*den),self.alpha);self.cache[key]=ans;return ans
 def slab(self,N):
  h=F(1,2*N);prev=self.point(F(0),'shifted');lo=hi=0
  for j in range(1,N+1):
   cur=self.point(j*h,'shifted');lo+=min(prev[0],cur[0]);hi+=max(prev[1],cur[1]);prev=cur
  return 2*h*F(lo,self.S),2*h*F(hi,self.S)

