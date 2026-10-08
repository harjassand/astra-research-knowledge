from itertools import product
from pathlib import Path
import numpy as np,json,math,time
from pfaffian_lift_check import network

# Positive unbiased Parseval estimator uses |Pf(K)|^2 for complex unit phases.
def logpf2(A):
 A=A.copy();N=len(A);value=0.
 for k in range(0,N,2):
  p=k+1+int(np.argmax(np.abs(A[k,k+1:])))
  if abs(A[k,p])<1e-14:return -np.inf
  if p!=k+1:
   A[[p,k+1],:]=A[[k+1,p],:];A[:,[p,k+1]]=A[:,[k+1,p]]
  q=A[k,k+1];value+=2*math.log(abs(q))
  b=A[k,k+2:];c=A[k+1,k+2:]
  A[k+2:,k+2:]+=(np.outer(c,b)-np.outer(b,c))/q
 return value

def setup(n,edges,t,mode):
 m=len(edges);w=network(n,edges);A=np.zeros((4*m,4*m),complex)
 vals=[(0,1,math.sqrt(.75*t)),(2,3,math.sqrt(.75*t)),(0,2,math.sqrt(1+t)),(1,3,math.sqrt(1+t)),(0,3,math.sqrt(.25*t)),(1,2,math.sqrt(.25*t))]
 for k in range(m):
  for i,j,x in vals:A[4*k+i,4*k+j]=x;A[4*k+j,4*k+i]=-x
 phases=np.ones(len(w),complex)
 if mode=='one_i_per_worldline':
  pos=0
  for z in range(n):
   occ=sum(z in e for e in edges)
   if occ:phases[pos]=1j;pos+=occ
 elif mode=='distributed_i_per_worldline':
  pos=0
  for z in range(n):
   occ=sum(z in e for e in edges)
   if occ:phases[pos:pos+occ]=np.exp(1j*math.pi/(2*occ));pos+=occ
 return A,w,phases

def simulate(n,edges,t,mode,count,seed):
 A,w,phases=setup(n,edges,t,mode);rng=np.random.default_rng(seed);vals=[]
 for rep in range(count):
  B=A.copy();signs=rng.choice([-1,1],len(w))
  for (i,j),phase,s in zip(w,phases,signs):
   if i>j:i,j=j,i
   B[i,j]+=phase*s;B[j,i]-=phase*s
  vals.append(logpf2(B))
 top=max(vals);xs=np.exp(np.asarray(vals)-top);mean=xs.mean();r=(xs**2).mean()/mean**2
 return {'mode':mode,'samples':count,'sample_mean':float(mean*math.exp(top)),'sample_relative_second_moment':float(r),'sample_zero_fraction':float(np.mean(xs==0)),'status':'finite diagnostic only; not a variance bound'}

start=time.monotonic();results=[]
for beta,M in [(0.,1),(1.,1),(1.,2),(1.,4),(1.,8),(3.,4),(3.,8),(6.,8)]:
 edges=[(0,1),(0,2),(1,2)]*M
 row={'qubits':3,'gates':len(edges),'beta':beta,'cycles':M,'t':beta/M,'diagnostics':[]}
 for mode in ['one_i_per_worldline','distributed_i_per_worldline']:
  row['diagnostics'].append(simulate(3,edges,beta/M,mode,300,20261008+M))
 results.append(row);print(json.dumps(row),flush=True)
Path('work/agents/epr_parity/results/tuned_phase_diagnostics.json').write_text(json.dumps({'results':results,'seconds':time.monotonic()-start,'status':'finite floating diagnostics; no acquired polynomial variance or mixing theorem'},indent=2)+'\n')
