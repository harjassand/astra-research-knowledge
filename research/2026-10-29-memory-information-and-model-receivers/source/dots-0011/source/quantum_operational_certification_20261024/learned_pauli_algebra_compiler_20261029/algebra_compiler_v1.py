import numpy as np, json, math

def basis(A):
 A=np.array(A,dtype=np.uint8).copy();r=0
 for c in range(A.shape[1]):
  ids=np.where(A[r:,c])[0]
  if not len(ids):continue
  q=r+ids[0];A[[r,q]]=A[[q,r]]
  for j in range(A.shape[0]):
   if j!=r and A[j,c]:A[j]^=A[r]
  r+=1
  if r==len(A):break
 return A[:r]
def sp(p,q,n):return int((np.dot(p[:n],q[n:])+np.dot(p[n:],q[:n]))%2)
def gate_rows(A,g,n):
 typ,*q=g
 if typ=='H':j=q[0];A[:,[j,n+j]]=A[:,[n+j,j]]
 elif typ=='S':j=q[0];A[:,n+j]^=A[:,j]
 elif typ=='CX':c,t=q;A[:,t]^=A[:,c];A[:,n+c]^=A[:,n+t]
 elif typ=='SW':i,j=q;A[:,[i,j]]=A[:,[j,i]];A[:,[n+i,n+j]]=A[:,[n+j,n+i]]
 else:raise ValueError(g)
def compile_algebra(A,n):
 A=basis(A); gates=[];r=0;t=0;a=0;b=0
 def G(*g):gate_rows(A,g,n);gates.append(g)
 def toZ(i,t):
  q=next(j for j in range(t,n) if A[i,j] or A[i,n+j])
  if q!=t:G('SW',q,t)
  for j in range(t,n):
   if A[i,j]:
    if A[i,n+j]:G('S',j)
    G('H',j)
  for j in range(t+1,n):
   if A[i,n+j]:G('CX',j,t)
 while r<len(A):
  pair=next(((i,j) for i in range(r,len(A)) for j in range(i+1,len(A)) if sp(A[i],A[j],n)),None)
  if pair:
   i,j=pair;A[[r,i]]=A[[i,r]]
   # j>i>=r ensures first swap did not move j
   A[[r+1,j]]=A[[j,r+1]]
   toZ(r,t)
   assert A[r+1,t]
   for j in range(t+1,n):
    if A[r+1,n+j]:
     if A[r+1,j]:G('S',j)
     else:G('H',j)
    if A[r+1,j]:G('CX',t,j)
   if A[r+1,n+t]:G('S',t)
   for i in range(r+2,len(A)):
    if A[i,n+t]:A[i]^=A[r]
    if A[i,t]:A[i]^=A[r+1]
   r+=2;a+=1;t+=1
  else:
   toZ(r,t)
   for i in range(r+1,len(A)):
    assert not A[i,t]
    if A[i,n+t]:A[i]^=A[r]
   r+=1;b+=1;t+=1
 return dict(n=n,a=a,b=b,k=n-a-b,gates=gates,canonical_basis=A)

def unitary(g,n):
 d=2**n;U=np.zeros((d,d),complex);typ,*q=g
 for x in range(d):
  bits=[(x>>(n-1-j))&1 for j in range(n)]
  if typ=='H':
   j=q[0]
   for y in [0,1]:
    out=bits.copy();out[j]=y;z=sum(v<<(n-1-i) for i,v in enumerate(out));U[z,x]=(-1)**(bits[j]*y)/math.sqrt(2)
  elif typ=='S':U[x,x]=1j**bits[q[0]]
  else:
   out=bits.copy()
   if typ=='CX':c,t=q;out[t]^=out[c]
   else:i,j=q;out[i],out[j]=out[j],out[i]
   z=sum(v<<(n-1-i) for i,v in enumerate(out));U[z,x]=1
 return U

def pauli(v,n):
 I=np.eye(2);X=np.array([[0,1],[1,0]]);Z=np.diag([1,-1]);P=np.ones((1,1),complex)
 for j in range(n):P=np.kron(P,np.linalg.matrix_power(X,int(v[j]))@np.linalg.matrix_power(Z,int(v[n+j])))
 return P

def run():
 rng=np.random.default_rng(291029); cases=[];maxerr=0
 for n in range(2,8):
  for a in range(n//2+1):
   b=(n-a)//2;k=n-a-b
   if k<1:continue
   canonical=[]
   for j in range(a):
    for col in [j,n+j]:v=np.zeros(2*n,dtype=np.uint8);v[col]=1;canonical.append(v)
   for j in range(a,a+b):v=np.zeros(2*n,dtype=np.uint8);v[n+j]=1;canonical.append(v)
   original=np.array(canonical,dtype=np.uint8)
   for _ in range(8*n):
    typ=rng.choice(['H','S','CX'])
    if typ=='CX':c,t=rng.choice(n,2,replace=False);g=(typ,int(c),int(t))
    else:g=(typ,int(rng.integers(n)))
    gate_rows(original,g,n)
   T=len(original)+12
   samples=(rng.integers(0,2,(T,len(original)),dtype=np.uint8)@original)%2
   learned=basis(samples);assert len(learned)==len(original)
   out=compile_algebra(learned,n);assert (out['a'],out['b'],out['k'])==(a,b,k)
   mapped=original.copy()
   for g in out['gates']:gate_rows(mapped,g,n)
   allowed=np.zeros(2*n,bool);allowed[:a]=True;allowed[n:n+a+b]=True
   assert not np.any(mapped[:,~allowed])
   err=None
   if n<=5:
    U=np.eye(2**n,dtype=complex)
    for g in out['gates']:U=unitary(g,n)@U
    err=0
    for row in original:
     A=U@pauli(row,n)@U.conj().T;ds=2**(a+b);dk=2**k
     # gauge-block coefficients must be scalar multiples of logical identity
     A4=A.reshape(ds,dk,ds,dk)
     coeff=np.einsum('iljl->ij',A4)/dk
     err=max(err,float(np.linalg.norm(A-np.kron(coeff,np.eye(dk)))))
    maxerr=max(maxerr,err)
   cases.append(dict(n=n,a=a,b=b,k=k,samples=T,dimension=len(original),gates=len(out['gates']),operator_factor_error=err))
 # scalable purely exact binary fixture
 n=128;a=32;b=32;A=[]
 for j in range(a):
  for col in [j,n+j]:v=np.zeros(2*n,dtype=np.uint8);v[col]=1;A.append(v)
 for j in range(a,a+b):v=np.zeros(2*n,dtype=np.uint8);v[n+j]=1;A.append(v)
 A=np.array(A)
 for _ in range(2048):
  c,t=rng.choice(n,2,replace=False);gate_rows(A,('CX',int(c),int(t)),n)
  gate_rows(A,('H',int(rng.integers(n))),n);gate_rows(A,('S',int(rng.integers(n))),n)
 out=compile_algebra(A,n)
 large={key:out[key] for key in ['n','a','b','k']};large.update(gates=len(out['gates']),error_rank_log2=len(A),full_row_normalization_log2=len(A)/2)
 print(json.dumps(dict(seed=291029,cases=cases,max_operator_factor_error=maxerr,scalable_fixture=large),indent=2))
if __name__=='__main__':run()
