"""Independent raw-coefficient comparator: self-adjoint multiplication kernel.
No producer imports. Exact rational coefficient tables and x0 are the interface.
"""
from pathlib import Path
import sympy as sp
import json,time,hashlib

def columns(polys,x):
    ps=[sp.Poly(p,*x) for p in polys]
    mons=sorted(set().union(*(set(p.monoms()) for p in ps)))
    return sp.Matrix([[p.coeff_monomial(m) for p in ps] for m in mons])

def bits(items):
    return max((max(abs(int(sp.Rational(v).p)).bit_length(),int(sp.Rational(v).q).bit_length()) for v in items),default=0)

def standard(y):
    N=len(y)//2;a=y[:N];b=y[N:]
    return sp.Matrix([a[i]*(b[(i+1)%N]-b[i]) for i in range(N)]+[2*(a[i]**2-a[i-1]**2) for i in range(N)])

def recognize(f,x,x0):
    started=time.perf_counter();n=len(x);N=n//2;assert n==2*N and N>=3
    f=sp.Matrix([sp.expand(v) for v in f]);X=sp.Matrix(x)
    assert all(sum(mon)==2 for v in f for mon in sp.Poly(v,*x).monoms())
    invariants=columns(f,x).nullspace();assert len(invariants)==1
    ell=invariants[0].T
    hs=[sp.hessian(v,x)/2 for v in f]
    an=sp.Matrix.vstack(*hs).nullspace();assert len(an)==1
    e=an[0];assert (ell*e)[0]!=0;e=e/(ell*e)[0]
    P=sp.Matrix.hstack(*ell.nullspace());R=(P.T*P).inv()*P.T;d=n-1
    z=sp.symbols('z:'+str(d));Z=sp.Matrix(z)
    g=(R*f).subs(dict(zip(x,P*Z)),simultaneous=True).applyfunc(sp.expand)
    pairs=[(i,j) for i in range(d) for j in range(i,d)]
    candidates=[sp.expand(Z[i]*g[i] if i==j else Z[i]*g[j]+Z[j]*g[i]) for i,j in pairs]
    qs=columns(candidates,z).nullspace();assert len(qs)==1
    G=sp.zeros(d)
    for v,(i,j) in zip(qs[0],pairs):G[i,j]=G[j,i]=v
    if G[0,0]<0:G=-G
    assert all(G[:i,:i].det()>0 for i in range(1,d+1))
    metric_seconds=time.perf_counter()-started
    T=[sp.hessian(v,z)/2 for v in g]
    # L_j(y)=T(e_j,y). Kernel of skew part is hidden b-space.
    L=[sp.Matrix(d,d,lambda out,k:T[out][j,k]) for j in range(d)]
    skew=sp.Matrix.hstack(*[(G*m-m.T*G).reshape(d*d,1) for m in L])
    B=sp.Matrix.hstack(*skew.nullspace());assert B.cols==N-1
    A=sp.Matrix.hstack(*(B.T*G).nullspace());assert A.cols==N
    GA=A.T*G*A;left=GA.inv()*A.T*G
    bound=(N-2)*N*(N-1)//2
    for trial in range(bound+1):
        beta=B*sp.Matrix([sp.Integer(trial)**j for j in range(N-1)])
        mul=sum((beta[j]*L[j] for j in range(d)),sp.zeros(d))
        E=left*mul*A
        cp=E.charpoly().as_poly()
        if sp.gcd(cp,cp.diff()).degree()==0:break
    else:raise AssertionError('No simple contraction')
    ev=E.eigenvects();assert len(ev)==N
    lines=[A*vs[0] for _,mult,vs in ev if mult==1 and len(vs)==1];assert len(lines)==N
    Xproj=R*(sp.eye(n)-e*ell)
    rows=[];cof=[];amp=[]
    for u in lines:
        h=(u.T*G*u)[0];row=(u.T*G/h)*Xproj
        if (row*sp.Matrix(x0))[0]<0:row=-row;u=-u
        assert (row*sp.Matrix(x0))[0]>0
        # Classical linear Darboux polynomial and cofactor, verified by division.
        p=(row*X)[0];dp=(row*f)[0]
        c=sp.cancel(dp/p);assert sp.Poly(c,*x).total_degree()==1
        c_row=sp.Matrix([[sp.diff(c,v) for v in x]])
        assert sp.expand(dp-p*c)==0
        # Normalize physical a_i directly by the c_i derivative on its line.
        xu=P*u
        curvature=(c_row*f.subs(dict(zip(x,xu)),simultaneous=True))[0]
        scale=sp.sqrt(-curvature/4);assert scale>0
        rows.append(scale*row);cof.append(c_row);amp.append(str(scale))
    # Invariant dual-metric Gram of the linear cofactors identifies cycle order.
    Q=sp.Matrix.vstack(*[c*P for c in cof]);gram=Q*G.inv()*Q.T;diag=gram[0,0]
    assert diag>0 and all(gram[i,i]==diag for i in range(N))
    adj={i:[j for j in range(N) if j!=i and gram[i,j]==-diag/2] for i in range(N)}
    assert all(len(v)==2 for v in adj.values())
    assert all(gram[i,j] in [0,-diag/2] for i in range(N) for j in range(N) if i!=j)
    order=[0,min(adj[0])]
    while len(order)<N:
        opts=[j for j in adj[order[-1]] if j!=order[-2]];assert len(opts)==1
        order.append(opts[0])
    assert len(set(order))==N and order[0] in adj[order[-1]]
    ar=sp.Matrix.vstack(*[rows[i] for i in order]);cr=sp.Matrix.vstack(*[cof[i] for i in order])
    diff=sp.zeros(N)
    for i in range(N):diff[i,i]=-1;diff[i,(i+1)%N]=1
    b=diff[:N-1,:].col_join(sp.ones(1,N)).inv()*cr[:N-1,:].col_join(N*ell)
    chart=ar.col_join(b);assert chart.det()!=0
    assert (chart*f-standard(chart*X)).applyfunc(sp.expand)==sp.zeros(n,1)
    inv=chart.inv();assert chart*inv==sp.eye(n) and inv*chart==sp.eye(n)
    return {'N':N,'acquisition_seconds':time.perf_counter()-started,'metric_seconds':metric_seconds,
       'selfadjoint_kernel_dimension':B.cols,'nonselfadjoint_complement_dimension':A.cols,
       'simple_spectrum_attempts':trial+1,'exact_raw_identities':n,'both_compositions':True,
       'chart_max_bits':bits(chart),'acquired_chart':[[str(v) for v in row] for row in chart.tolist()],
       'chart':chart}

def mix(n):
    M=sp.eye(n)
    for k in range(2*n):
        i=k%n;j=(3*k+1)%n
        if i==j:j=(j+1)%n
        E=sp.eye(n);E[i,j]=(k%3)-1 or 2;M=E*M
    return M

def main():
    out={}
    for N in [3,4,5]:
        n=2*N;x=sp.symbols('x:'+str(n));y=sp.symbols('y:'+str(n));M=mix(n);Mi=M.inv()
        f=(M*standard(y)).subs(dict(zip(y,Mi*sp.Matrix(x))),simultaneous=True).applyfunc(sp.expand)
        y0=sp.Matrix(list(range(1,N+1))+[sp.Integer((i%3)-1) for i in range(N)])
        ans=recognize(f,x,M*y0);del ans['chart'];out['dense_mixed_N'+str(N)]=ans
        print(N,ans['acquisition_seconds'],flush=True)
    # Non-cycle connected graph: preserve elementary energy, center, and dimensions.
    N=4;n=8;x=sp.symbols('x:'+str(n));a=x[:N];b=x[N:];edges=[(0,1),(1,2),(2,0),(0,3)]
    bad=sp.Matrix([a[i]*(b[v]-b[u]) for i,(u,v) in enumerate(edges)]+[sum(2*a[i]**2*((u==k)-(v==k)) for i,(u,v) in enumerate(edges)) for k in range(N)])
    try:recognize(bad,x,sp.Matrix([1,2,3,4,0,1,2,3]));out['noncycle_rejected']=False
    except AssertionError:out['noncycle_rejected']=True
    out['scope']='Independent exact raw-coefficient self-adjoint multiplication-kernel comparator; no producer imports, no constructor matrix passed into recognition. Historical identity not claimed.'
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
