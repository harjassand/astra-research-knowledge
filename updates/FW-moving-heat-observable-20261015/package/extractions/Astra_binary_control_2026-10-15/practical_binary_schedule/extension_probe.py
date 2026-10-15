from rank_probe import *

def inverse(A):
 n=len(A); cols=[solve(A,[int(i==j) for i in range(n)]) for j in range(n)];return list(map(list,zip(*cols)))
def test(k):
 rng=random.Random(k+120);a=[rng.randrange(1,P) for i in range(k+1)];B=[[0 if i==j else rng.randrange(P) for j in range(k+1)] for i in range(k+1)]
 rows=[]
 for mask in range(1,1<<k):
  T=[i for i in range(k) if mask>>i&1];M=[[int(i==j)+B[i][j] for j in T] for i in T]; inv=inverse(M);p=solve(M,[1]*len(T));q=solve(list(map(list,zip(*M))),[a[i] for i in T]);u=[B[k][i] for i in T];v=[B[i][k] for i in T]
  den=(1-sum(u[i]*inv[i][j]*v[j] for i in range(len(T)) for j in range(len(T))))%P
  h=(a[k]-sum(qi*vi for qi,vi in zip(q,v)))*(1-sum(ui*pi for ui,pi in zip(u,p)))*pow(den,-1,P)%P
  pd=dict(zip(T,p));qd=dict(zip(T,q));idx={x:i for i,x in enumerate(T)}
  row=[a[k]*pd.get(i,0)%P for i in range(k)]+[qd.get(i,0)%P for i in range(k)]+[-(h*(inv[idx[i]][idx[j]] if i in idx and j in idx else 0)+pd.get(i,0)*qd.get(j,0))%P for i in range(k) for j in range(k)]
  rows.append(row)
 r=rank(rows);print(k,len(rows),len(rows[0]),r,flush=True)
for k in range(3,9):test(k)
