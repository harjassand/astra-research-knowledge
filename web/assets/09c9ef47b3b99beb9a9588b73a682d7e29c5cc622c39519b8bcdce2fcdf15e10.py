"""Bounded exact tests of the independently derived graph/star formulas."""
from pathlib import Path
from itertools import combinations
import hashlib,json
import sympy as s

def cyclic_perm(n,shift):return [(i+shift)%n for i in range(n)]
cycle4=[0,2,1,3]
cycle4group=[]
for shift in range(4):
    p=list(range(4))
    for i,v in enumerate(cycle4):p[v]=cycle4[(i+shift)%4]
    cycle4group.append(p)
cases=[
 ('K2',2,[(0,1)],2,[0,1],[cyclic_perm(2,q) for q in range(2)],True),
 ('K3',3,list(combinations(range(3),2)),3,[0,1,2],
  [cyclic_perm(3,q) for q in range(3)],True),
 ('K22',4,[(i,j) for i in [0,1] for j in [2,3]],2,[0,2],cycle4group,True),
 ('C5',5,[(i,(i+1)%5) for i in range(5)],2,[0,1],
  [cyclic_perm(5,q) for q in range(5)],False),
 ('K222',6,[(i,j) for i in range(6) for j in range(i+1,6) if i//2!=j//2],
  3,[0,2,4],[[2*((i//2+q)%3)+(i%2+e)%2 for i in range(6)]
             for q in range(3) for e in range(2)],True),
 ('triangular_prism',6,[(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)],
  3,[0,1,2],[[3*((i//3+e)%2)+(i%3+q)%3 for i in range(6)]
             for q in range(3) for e in range(2)],False)
]
records=[]
for name,d,edges,omega,clique,group,balanced in cases:
    A=s.zeros(d)
    for u,v in edges:A[u,v]=A[v,u]=1
    r=int(sum(A[0,j] for j in range(d)))
    assert all(sum(A[i,j] for j in range(d))==r for i in range(d))
    mu=s.Rational(omega-1,omega)
    t=s.simplify((s.sqrt((r/mu)**2+4*r)-r/mu)/2)
    lam=r+t
    assert s.simplify(t*t+(r/mu)*t-r)==0 and bool(t>0) and bool(t<mu)

    # Original frame Kronecker entries, without assuming the simplified
    # pair identity; exact scalar coefficients include the imaginary Y.
    W={}
    def add(row,col,value):W[(row,col)]=s.simplify(W.get((row,col),0)+value)
    for u,v in edges:
        for matrix in [{(u,v):1,(v,u):1},{(u,v):s.I,(v,u):-s.I}]:
            for (ai,ao),av in matrix.items():
                for (bi,bo),bv in matrix.items():
                    for spectator in range(d):
                        add((ao*d+bi)*d+spectator,(ai*d+bo)*d+spectator,av*bv)
                        add((ao*d+spectator)*d+bi,(ai*d+spectator)*d+bo,av*bv)
    W={key:value for key,value in W.items() if value!=0}
    expected={};active=set()
    def put(row,col):expected[(row,col)]=expected.get((row,col),0)+2
    for k in range(d):
        block={((i*d+i)*d+k) for i in range(d)}|{((i*d+k)*d+i) for i in range(d)}
        assert len(block)==2*d-1 and not active&block
        active|=block
        for u,v in edges:
            for row,col in [((u*d+u)*d+k,(v*d+v)*d+k),
                            ((u*d+k)*d+u,(v*d+k)*d+v)]:
                put(row,col);put(col,row)
    assert W==expected
    assert len(active)==d*(2*d-1) and d**3-len(active)==d*(d-1)**2

    k=0;neighbors=[i for i in range(d) if A[k,i]]
    Q=A.extract(neighbors,neighbors)
    z=(lam*s.eye(r)-Q).inv()*s.ones(r,1)
    h=z*(1-t)
    total=s.simplify(sum(h))
    assert bool(s.simplify(t-total)>=0)
    y=s.Matrix([1 if i==k else s.Rational(1,2) for i in range(d)])
    for i,vertex in enumerate(neighbors):y[vertex]=s.simplify((1+h[i])/2)
    other=[i for i in range(d) if i!=k]
    H=s.zeros(2*d-1);H[:d,:d]=A
    for i,u in enumerate(other):
        H[k,d+i]=H[d+i,k]=A[k,u]
        for j,v in enumerate(other):H[d+i,d+j]=A[u,v]
    yh=y.col_join(y.extract(other,[0]))
    residual=(lam*yh-H*yh).applyfunc(s.simplify)
    assert all(bool(value>=0) for value in residual)
    if balanced:assert residual==s.zeros(2*d-1,1)

    # Actual optimal pure ensemble, with a supplied transitive subgroup.
    rho=s.zeros(d);count=0
    for perm in group:
        assert sorted(perm)==list(range(d))
        assert all(A[perm[i],perm[j]]==A[i,j] for i in range(d) for j in range(d))
        for phase in range(omega):
            psi=s.zeros(d,1)
            for i,vertex in enumerate(clique):
                coeff=s.cos(2*s.pi*phase*i/omega)+s.I*s.sin(2*s.pi*phase*i/omega)
                psi[perm[vertex]]=coeff/s.sqrt(omega)
            assert s.simplify((psi.H*psi)[0])==1
            score=0
            for u,v in edges:
                z0=s.conjugate(psi[u])*psi[v]
                z1=s.conjugate(psi[v])*psi[u]
                score+=(z0+z1)**2+(s.I*(z0-z1))**2
            assert s.simplify(score-2*mu)==0
            rho+=psi*psi.H/(len(group)*omega);count+=1
    assert (rho-s.eye(d)/d).applyfunc(s.simplify)==s.zeros(d)
    records.append({'graph':name,'d':d,'r':r,'omega':omega,
                    'candidate_lambda':str(lam),'W_zero_sector':d*(d-1)**2,
                    'supersolution_exact_eigenvector':balanced,'optimal_ensemble_atoms':count})

out={'status':'PASS','scope':'bounded exact formula checks; analytic theorem separate',
     'fixtures':records,'proof_sha256':hashlib.sha256(Path(__file__).with_name('THEOREM_FIRST_BASELINE.txt').read_bytes()).hexdigest()}
Path(__file__).with_name('EXACT_GRAPH_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
