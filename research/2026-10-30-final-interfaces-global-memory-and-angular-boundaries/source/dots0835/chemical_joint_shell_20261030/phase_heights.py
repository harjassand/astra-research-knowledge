import sympy as s

def heights(K):
 n=s.symbols('n');Q=s.zeros(K+1)
 for b in range(K+1):
  for bb,rate in [(b+1,s.Integer(1)),(b+3,b*n),(b-4,s.prod(range(b-3,b+1))*n**3 if b>=4 else 0)]:
   if 0<=bb<=K and rate:
    Q[b,bb]+=rate;Q[b,b]-=rate
 deg=[]
 for root in range(K+1):
  keep=[j for j in range(K+1) if j!=root]
  poly=s.Poly((-Q).extract(keep,keep).det(method='domain-ge'),n)
  deg.append(poly.degree())
 return [max(deg)-d for d in deg]
if __name__=='__main__':
 for K in [4,8,12]: print(K,heights(K),flush=True)
