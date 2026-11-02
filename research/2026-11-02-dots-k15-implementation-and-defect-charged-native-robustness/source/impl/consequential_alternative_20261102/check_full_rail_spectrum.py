from direct_pair_search import elem
import numpy as np,json
eta=.78;G=2-eta;t=eta/G;q=(G-1)/G;a=t/(G-1);b=1-t;M=8
p0=elem(0,0,eta,M)[:-1,:-1];p1=elem(1,1,eta,M)[:-1,:-1];x=elem(1,0,eta,M)[:-1,:-1]
B0=np.kron(p1,p0);B1=np.kron(p0,p1);X=np.kron(x,x.T)
J=np.block([[B0,X],[X.T,B1]])/2;B=(B0+B1)/2
out=[]
for N in range(M+1):
 idx=np.array([i*(M+1)+N-i for i in range(N+1)])
 ridx=np.r_[idx,idx+(M+1)**2]
 c=G**-2*q**N
 want=np.r_[np.repeat(c/2*(b+a*(N+1)),N),np.repeat(c*b/2,N+2)]
 err=max(np.max(abs(np.sort(np.linalg.eigvalsh(J[np.ix_(ridx,ridx)]))-np.sort(want))),np.max(abs(np.linalg.eigvalsh(B[np.ix_(idx,idx)])-c*(b+a*N/2))))
 out.append({'N':N,'error':float(err)})
print(json.dumps(out,indent=2))
assert max(r['error'] for r in out)<1e-13
