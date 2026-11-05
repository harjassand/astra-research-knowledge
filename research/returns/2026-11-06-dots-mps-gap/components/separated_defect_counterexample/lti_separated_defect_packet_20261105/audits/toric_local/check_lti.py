from itertools import product

def xor_all(xs):
    a=0
    for x in xs:a^=x
    return a

def check(w,h):
    sites=[(x,y) for y in range(h) for x in range(w)]
    idx={(x,y,k):2*(y*w+x)+k for x,y in sites for k in (0,1)}
    def mask(edges):return sum(1<<idx[e] for e in edges)
    A=[mask([(x,y,0),(x,y,1),(x-1,y,0),(x,y-1,1)]) for y in range(1,h) for x in range(1,w)]
    B=[mask([(x,y,0),(x,y,1),(x,y+1,0),(x+1,y,1)]) for y in range(h-1) for x in range(w-1)]
    N=len(A)
    d={}
    for s in range(1<<N):
        xm=xor_all(A[i] for i in range(N) if (s>>i)&1)
        coeff=N-2*s.bit_count()
        for t in range(1<<len(B)):
            zm=xor_all(B[i] for i in range(len(B)) if (t>>i)&1)
            assert (xm&zm).bit_count()%2==0
            assert (xm,zm) not in d
            d[xm,zm]=coeff
    def marginal(xlo,xhi,ylo,yhi):
        keep=[(x,y,k) for y in range(ylo,yhi) for x in range(xlo,xhi) for k in (0,1)]
        km=mask(keep)
        def repack(v):return sum(((v>>idx[p])&1)<<j for j,p in enumerate(keep))
        return {(repack(x),repack(z)):v for (x,z),v in d.items() if ((x|z)&~km)==0}
    assert marginal(0,w-1,0,h)==marginal(1,w,0,h)
    assert marginal(0,w,0,h-1)==marginal(0,w,1,h)
    for uw in range(1,w+1):
      for uh in range(1,h+1):
        ref=marginal(0,uw,0,uh)
        for x in range(w-uw+1):
          for y in range(h-uh+1):assert ref==marginal(x,x+uw,y,y+uh)
    print(f'{w}x{h}: {N} stars + {len(B)} plaquettes, {len(d)} Pauli coefficients, all translated rectangular marginals EXACTLY equal')
for wh in [(2,2),(2,3),(3,3),(3,4),(4,3)]:check(*wh)
