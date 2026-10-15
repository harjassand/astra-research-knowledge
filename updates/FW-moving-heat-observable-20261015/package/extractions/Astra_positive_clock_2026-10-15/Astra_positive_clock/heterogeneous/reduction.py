from pathlib import Path
exec(open(str(Path(__file__).resolve().parent)+'/test.py').read().split('rows=[]')[0])
from scipy.linalg import eigh
n=128;x,w,r=rounded(n,.05/n);q=2.**-n;mean=np.dot(w,1/x)/q;z=np.array([.01,.1,.3,1,3,10,100]);s=z/mean
full=np.array([q/(q+v*np.dot(w,1/(x+v))) for v in s]);out=[]
for k in [2,4,6,8,10,12]:
 t=time.perf_counter();v=np.array([0.]);
 for rr in r[-k:]:v=np.r_[v,v+rr]
 v=np.sort(v[1:]);p=np.full(len(v),2.**-k);qs=2.**-k
 F=np.array([qs/(qs+ss*np.dot(p,1/(v+ss))) for ss in s]);out.append(dict(k=k,states=2**k,LTgap=float(max(abs(F-full))),seconds=time.perf_counter()-t))
print(json.dumps(out,indent=2));open(str(Path(__file__).resolve().parent)+'/reduction.json','w').write(json.dumps(out,indent=2))
# Explicit mixture extraction on rounded grid, rescale λ by smallest rate.
for n in [16,32,64]:
 x,w,r=rounded(n,.05/n);x=x/x[0];q=2.**-n;t=time.perf_counter();rs=[];a=[]
 for j,upper in enumerate(x):
  lower=0 if j==0 else x[j-1]
  # Solve dimensionless relative interval variable; positive poles handled by nextafter.
  def fun(y):
   rr=lower+(upper-lower)*y
   return q-rr*np.dot(w,1/(x-rr))
  y=brentq(fun,np.nextafter(0.,1.) if lower==0 else 1e-13,1-1e-13,xtol=1e-14)
  rr=lower+(upper-lower)*y;aa=q/(rr*np.dot(w*x,1/(x-rr)**2));rs.append(rr);a.append(aa)
 rs=np.array(rs);a=np.array(a);m=np.dot(w,1/x)/q;ss=np.array([.1,.3,1,3,10])/m
 err=max(abs(np.array([q+np.dot(a,rs/(rs+v)) for v in ss])-np.array([q/(q+v*np.dot(w,1/(x+v))) for v in ss])))
 print(dict(n=n,K=len(x),root_seconds=time.perf_counter()-t,weight_sum=a.sum(),expected=1-q,max_LT_error=err))
