import numpy as np,itertools
exec(open('producer-workspace/find_move.py').read().split('rng=')[0])
faces=list(itertools.combinations(range(5),3));tets=[t for t,s in T]
nodes=[(ti,f) for ti,t in enumerate(tets) for f in itertools.combinations(t,3)];ix={x:i for i,x in enumerate(nodes)}
p0=[tuple(ix[ti,f] for ti,t in enumerate(tets) if set(f)<=set(t)) for f in faces]
edges=sorted(set(tuple(sorted(e)) for e in p0)|{(i,j) for i,(ti,f) in enumerate(nodes) for j,(tj,g) in enumerate(nodes) if i<j and ti==tj});ei={e:i for i,e in enumerate(edges)}
def pairing(n,choice):
 pairs=[e for f,e in zip(faces,p0) if n[f]%2==0]
 for ti,t in enumerate(tets):
  ns=[ix[ti,f] for f in itertools.combinations(t,3) if n[f]%2]
  if len(ns)==2:pairs.append(tuple(ns))
  elif len(ns)==4:
   a,b,c,d=ns;pairs+=([(a,b),(c,d)],[(a,c),(b,d)],[(a,d),(b,c)])[choice]
 return sorted(tuple(sorted(e)) for e in pairs)
def pf(p):
 s=sum(([a,b] for a,b in sorted(p)),[])
 return sum(s[i]>s[j] for i in range(len(s)) for j in range(i+1,len(s)))%2
def row(p):
 mask=0
 for e in p:mask^=1<<ei[tuple(sorted(e))]
 return mask
rng=np.random.default_rng(4)
samples=[]
for bits in itertools.product([0,1], repeat=4):
 for ranks in itertools.permutations(range(1,5)):
  samples.append(dat(np.array([0]+[r/10+b/2 for r,b in zip(ranks,bits)])))
print("complete generic rotor chambers",len(samples))
for choice in range(3):
 basis={};bad=False
 for q,m,n in samples:
  p=pairing(n,choice);a=row(p)^row(p0);b=q%2^pf(p)^pf(p0)
  while a:
   k=a.bit_length()-1
   if k in basis:a^=basis[k][0];b^=basis[k][1]
   else:basis[k]=(a,b);break
  if not a and b:bad=True;break
 print('choice',choice,'consistent',not bad,'rank',len(basis))
 if not bad:
  sol=0
  for k,(a,b) in sorted(basis.items()):
   if ((a&sol).bit_count()%2)^b:sol|=1<<k
  np.savez('producer-workspace/matching.npz',nodes=np.array(nodes,dtype=object),edges=np.array(edges),signs=np.array([(-1)**((sol>>i)&1) for i in range(len(edges))]),choice=choice)
  p=np.array([.39162483,.18725257,.34596067,.51106597,.89120941]);p2=p.copy();p2[0]=.77556394
  pa=pairing(dat(p)[2],choice);pb=pairing(dat(p2)[2],choice)
  print('p',pa,'pprime',pb,'changed',set(pa)^set(pb),'signbits',sol)
