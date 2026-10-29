import math,json
from scipy.stats import binom
checks=[]
for R in [.1,.75,1.,3.,10.]:
 p=1/(1+R);u=1-p
 for t in [0,1,3,8]:
  for b in [0,1,3]:
   H=[[0.]*(b+2) for _ in range(t+2)]
   for j in range(b+1):H[t+1][j]=1.
   for i in range(t,-1,-1):
    for j in range(b,-1,-1):H[i][j]=u*H[i+1][j]+p*H[i][j+1]
   tail=sum(math.comb(t+j,j)*u**(t+1)*p**j for j in range(b+1));assert abs(H[0][0]-tail)<1e-12
   maxdrift=-1e100
   for i in range(t+1):
    for j in range(b+1):
     for g in [.001,.01,.1,1/(1+R)]:
      if (R+1)*g>1+1e-12:continue
      for f in [0,R*g/2,R*g]:maxdrift=max(maxdrift,f*(H[i+1][j]-H[i][j])+g*(H[i][j+1]-H[i][j]))
   assert maxdrift<1e-12
   checks.append({'R':R,'t':t,'b':b,'tail':tail,'max_checked_supermartingale_drift':maxdrift})
sizes=[]
for n,J,t,R in [(8,5,1,1),(12,63,5,.1),(12,127,20,1),(20,255,25,1)]:
 d0=math.comb(n,n//2)//(n//2+1);k=d0.bit_length()-1;C=d0/(1<<k)*(n-1);s=R/(C+R);L=math.ceil(1.3*J/s);yield0=float(binom.sf(J-1,L,s));ell=J-4*t
 sizes.append({'n':n,'inner_logical_qubits':k,'J':J,'t':t,'outer_logical_symbols':ell,'payload_qubits':ell*k,'R':R,'service_probability':s,'cap_L':L,'NB_bound_b0':(R/(1+R))**(t+1),'ideal_zero_test_failure_acceptance':yield0,'secure_endpoint_buffer_qubits_each_at_most':J*k,'caveat':'Ideal source/test/holding/control; not measured throughput or hardware.'})
print(json.dumps({'NB_checks':checks,'illustrative_ideal_sizes':sizes},indent=2))
