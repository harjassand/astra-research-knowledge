import itertools,random,json,time
P=2147483647

def modrank(rows,ncols):
 basis={}
 for row in rows:
  v=list(row)
  for j in range(ncols):
   if not v[j]:continue
   if j in basis:
    c=v[j];w=basis[j]
    for k in range(j,ncols):v[k]=(v[k]-c*w[k])%P
   else:
    inv=pow(v[j],-1,P)
    basis[j]=[(x*inv)%P for x in v]
    break
 return len(basis)

def check(n,seed=42):
 lam=[5**i for i in range(n)]
 terms=[list(set(itertools.permutations(t))) for t in itertools.combinations_with_replacement(range(n),4)]
 rng=random.Random(seed);rows=[]
 for _ in range(len(terms)+10):
  s=[rng.randrange(1,P//10) for k in range(3)]
  vs=[[pow((ss+l)%P,-1,P) for l in lam] for ss in [sum(s)]+s]
  rows.append([sum(vs[0][i]*vs[1][j]*vs[2][k]*vs[3][l] for i,j,k,l in ts)%P for ts in terms])
 return {'n':n,'lambda':lam,'dimension':len(terms),'rank_mod_prime':modrank(rows,len(terms)),'prime':P}
if __name__=='__main__':
 out=[check(n) for n in range(2,7)]
 print(json.dumps(out,indent=2))
