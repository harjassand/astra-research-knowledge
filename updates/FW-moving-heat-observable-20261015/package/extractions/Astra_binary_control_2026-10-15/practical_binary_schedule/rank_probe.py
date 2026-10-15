import random,itertools,json
P=1000003

def solve(A,b):
 n=len(b); C=[list(row)+[bb] for row,bb in zip(A,b)]
 for k in range(n):
  q=next(i for i in range(k,n) if C[i][k]%P); C[k],C[q]=C[q],C[k]
  t=pow(C[k][k],-1,P); C[k]=[v*t%P for v in C[k]]
  for i in range(n):
   if i!=k:
    t=C[i][k]; C[i]=[(x-t*y)%P for x,y in zip(C[i],C[k])]
 return [r[-1] for r in C]
def rank(A):
 A=[r[:] for r in A]; k=0
 for j in range(len(A[0])):
  q=next((i for i in range(k,len(A)) if A[i][j]),None)
  if q is None:continue
  A[k],A[q]=A[q],A[k]; t=pow(A[k][j],-1,P); A[k]=[v*t%P for v in A[k]]
  for i in range(k+1,len(A)):
   t=A[i][j]
   if t:A[i]=[(x-t*y)%P for x,y in zip(A[i],A[k])]
  k+=1
  if k==len(A):break
 return k

def probe(m,c=None):
 rng=random.Random(100+m); a=[rng.randrange(1,P) for _ in range(m)]; B=[[0 if i==j else rng.randrange(P) for j in range(m)] for i in range(m)]; edges=[(i,j) for i in range(m) for j in range(m) if i!=j]; J=[]
 for mask in range(1<<m):
  S=[i for i in range(m) if mask>>i&1]
  if len(S)<2 or c is not None and len([i for i in S if i>=c])>2:continue
  C=[[int(i==j)+B[i][j] for j in S] for i in S]; v=solve(C,[1]*len(S)); u=solve(list(map(list,zip(*C))),[a[i] for i in S]); ui=dict(zip(S,u));vi=dict(zip(S,v)); J.append([-ui.get(i,0)*vi.get(j,0)%P for i,j in edges])
 return {'m':m,'anchors':c,'rows':len(J),'columns':len(edges),'rank':rank(J)}
if __name__=='__main__':
 out=[]
 for m in range(2,9):
  for c in [None,1,2,3,4]:
   if c is not None and c>=m:continue
   r=probe(m,c); print(r,flush=True);out.append(r)
 open('/workspace/shared/practical_binary_schedule/ranks.json','w').write(json.dumps(out,indent=2))
