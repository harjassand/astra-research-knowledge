import numpy as np,itertools,json

def edge(kind,x,y):return (kind,x,y)
def rawcheck(kind,x,y):
 if kind=='X':return [edge('h',x,y),edge('h',x-1,y),edge('v',x,y),edge('v',x,y-1)]
 return [edge('h',x,y),edge('h',x,y+1),edge('v',x,y),edge('v',x+1,y)]
def color(e):k,x,y=e;return ((x+y)%2)+(0 if k=='h' else 2)
def mul(a,b):x,z,k=a;xx,zz,kk=b;return (x^xx,z^zz,(k+kk+2*((z&xx).bit_count()%2))%4)
def dag(a):x,z,k=a;return(x,z,(-k+2*((x&z).bit_count()%2))%4)

def run(checks,eta,rainbow=True,undo=False):
 w=4;edges=sorted(set(sum([rawcheck(*c) for c in checks],[])));ei={e:i for i,e in enumerate(edges)}
 P=[];Q=[]
 for kind,x,y in checks:
  ee=rawcheck(kind,x,y);assert sorted(map(color,ee))==[0,1,2,3]
  order=[1,0,3,2] if rainbow and kind=='Z' else [0,1,2,3]
  ee=sorted(ee,key=lambda e:order.index(color(e)))
  pp=[(1<<ei[e],0,0) if kind=='X' else (0,1<<ei[e],0) for e in ee];P.append(pp)
  qq=[(0,0,0)]
  for p in pp:qq.append(mul(p,qq[-1]))
  if undo:qq+=qq[:w-1]
  Q.append(qq)
 nb=len(Q[0]);nc=len(checks);states=list(itertools.product(range(nb),repeat=nc));idx={r:i for i,r in enumerate(states)};N=len(states)
 GG=[]
 for r in states:
  q=(0,0,0)
  for a,v in enumerate(r):q=mul(q,Q[a][v])
  GG.append(q)
 def scalar(m,p,j,a):
  q=mul(mul(dag(GG[m]),p),GG[j]);assert q[:2] in [(0,0),Q[a][w][:2]];assert q[2] in [0,2]
  return 1 if q[2]==0 else -1
 D=1/eta;A=np.diag(np.full(3,D))+np.diag(np.ones(2),1)+np.diag(np.ones(2),-1);Ai=np.linalg.inv(A);J=-Ai[-1,0];shift=Ai[0,0];h=np.sqrt(abs(J))/2
 H=np.zeros((N,N))
 for j,r in enumerate(states):
  H[j,j]=sum(shift if v in [0,w] else D for v in r)
  for a,v in enumerate(r):
   if v<w:
    rr=list(r);rr[a]+=1;m=idx[tuple(rr)];s=scalar(m,P[a][v],j,a);H[m,j]+=s;H[j,m]+=s
   if v==0:
    rr=list(r);rr[a]=w;m=idx[tuple(rr)];s=J*scalar(m,(0,0,0),j,a);H[m,j]+=s;H[j,m]+=s # all caches wrong c=1
   if undo and v in range(1,w):
    rr=list(r);rr[a]=w+v;m=idx[tuple(rr)];s=h*scalar(m,P[a][v-1],j,a);H[m,j]+=s;H[j,m]+=s
 low=[i for i,r in enumerate(states) if all(v in [0,w] for v in r)];high=[i for i in range(N) if i not in low]
 eff=H[np.ix_(low,low)]-H[np.ix_(low,high)]@np.linalg.solve(H[np.ix_(high,high)],H[np.ix_(high,low)])
 diag=np.diag(eff)/abs(J);rr=[states[i] for i in low];walsh={}
 for mask in range(1<<nc):walsh[str(mask)]=float(sum(diag[j]*(-1)**sum(r[a]==w for a in range(nc) if mask>>a&1) for j,r in enumerate(rr))/(1<<nc))
 target=np.zeros_like(eff)
 for j,r in enumerate(rr):
  for a in range(nc):
   ss=list(r);ss[a]=w-ss[a];m=rr.index(tuple(ss));target[j,m]=-2*abs(J)
 residual=eff-target
 return dict(checks=checks,eta=eta,rainbow=rainbow,undo=undo,H_dimension=N,J=abs(J),max_mixed_diag_over_J=max(abs(v) for k,v in walsh.items() if int(k).bit_count()>=2),walsh_diag_over_J=walsh,max_residual_over_J=float(np.max(np.abs(residual))/abs(J)))
if __name__=='__main__':
 for checks,undo in [([('X',0,0),('Z',0,0),('Z',-1,0)],True),([('X',0,0),('X',1,0),('Z',0,0),('Z',0,-1)],False)]:
  for eta in [.03,.05,.1]:
   for rainbow in [False,True]:print(json.dumps(run(checks,eta,rainbow,undo)),flush=True)
