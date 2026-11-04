import numpy as np,math,json
from decimal_intervals import iv
from constant_cavity_receiver_certificate import build,scaled_taylor,report

def upper(x):return np.nextafter(float(x.b),math.inf)
def coefficient_certificate(L,n=4096,N=6):
 d=8*N;vals={};sqr=[iv.sqrt(k) for k in range(N)];G=1/iv.sqrt(40*iv.pi)
 def idx(A,S,c,b):return (((A*2+S)*N+c)*2+b)
 states=[(A,S,c,b) for A in range(2) for S in range(2) for c in range(N) for b in range(2)]
 def add(row,col,v):
  key=(row,col);vals[key]=vals.get(key,iv.mpc(0))+v
 hs=[]
 for A,S,c,b in states:
  out=[(idx(A,S,c,b),iv.mpf(1-2*b)/2),(idx(A,1-S,c,b),iv.mpf(1)/2)]
  if c>0:out.append((idx(A,S,c-1,b),G*(1-2*S)*sqr[c]))
  if c<N-1:out.append((idx(A,S,c+1,b),G*(1-2*S)*sqr[c+1]))
  hs.append(out)
 q=iv.mpf(1)/5;ii=iv.mpc(0,1)
 for i,(A,S,c,b) in enumerate(states):
  for j,(E,U,k,f) in enumerate(states):
   col=i+d*j
   for l,h in hs[i]:add(l+d*j,col,-ii*h)
   for l,h in hs[j]:add(i+d*l,col,ii*h)
   add(col,col,-10*(c+k)-q*(b+f)/2)
   if c and k:add(idx(A,S,c-1,b)+d*idx(E,U,k-1,f),col,20*sqr[c]*sqr[k])
   if b and f:add(idx(A,S,c,0)+d*idx(E,U,k,0),col,q)
   if c and f:add(idx(A,S,c-1,b)+d*idx(E,U,k,0),col,ii*q*sqr[c])
   if b and k:add(idx(A,S,c,0)+d*idx(E,U,k-1,f),col,-ii*q*sqr[k])
   if c and not b:add(idx(A,S,c-1,1)+d*j,col,-ii*q*sqr[c])
   if k and not f:add(i+d*idx(E,U,k-1,1),col,ii*q*sqr[k])
 h=iv.pi/n
 A=(np.pi/n*L).tocoo();approx={(int(i),int(j)):v for i,j,v in zip(A.row,A.col,A.data)}
 colerr=[iv.mpf(0) for _ in range(d*d)]
 for row,col in vals.keys()|approx.keys():
  z=h*vals.get((row,col),iv.mpc(0))-iv.mpc(approx.get((row,col),0))
  colerr[col]+=abs(z.real)+abs(z.imag)
 return max(upper(x) for x in colerr),len(vals),len(approx)

if __name__=='__main__':
 L,y,F,Lam,z=build(Gamma=.2)
 da,nex,nap=coefficient_certificate(L)
 yf,roundcert=scaled_taylor(L,y,z['T'],Lam)
 B=roundcert['induced_l1_step'];n=roundcert['n'];d=48
 coefficient_error=n*d*da*math.exp(B+da)
 # Exact initial nonzero density entries are +/-1/4.
 exact=np.zeros_like(y);active=np.abs(y)>0;exact[active]=np.sign(y[active].real)/4
 initial_error=float(np.sum(np.abs(y-exact)))
 # Safety factors cover evaluation of the nonnegative sums/norms used in the error budget.
 error=1.001*(roundcert['roundoff_trace_bound']+coefficient_error+initial_error+roundcert['taylor_remainder_trace'])+8e-12
 res=report(yf,F,z)
 # final numerical expectation/filter error allowance is <1e-12 before normalization
 error+=1e-12
 p=res['success'];f=res['fidelity'];fid_lower=(p*f-error)/(p+error)
 print(json.dumps(dict(step_coefficient_induced_l1_error=da,exact_stored_entries=nex,float_stored_entries=nap,coefficient_error_trace=coefficient_error,initial_error_trace=initial_error,rounding=roundcert,full_cavity_trace_error_bound=error,p_interval=[p-error,p+error],fidelity_lower=fid_lower,observed=res)),flush=True)
