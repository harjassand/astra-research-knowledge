"""Exact hidden linear Toda chart acquisition from expanded quadratic coefficients.

No constructor metadata is consumed by acquire(). The generator and its inverse
are nevertheless public below: no advantage over source-aware pattern matching
is claimed. This is a recognition/certification experiment, not a novelty claim.
"""
from pathlib import Path
import sympy as s
import time,json,hashlib

def coeff_columns(expressions,x):
    ps=[s.Poly(z,*x) for z in expressions]
    mon=sorted(set().union(*(set(p.monoms()) for p in ps)))
    return s.Matrix([[p.coeff_monomial(m) for p in ps] for m in mon])

def bitmax(items):
    vals=[]
    for q in items:
        q=s.Rational(q);vals.append(max(abs(int(q.p)).bit_length(),int(q.q).bit_length()))
    return max(vals,default=0)

def toda(y):
    N=len(y)//2;a=list(y[:N]);b=list(y[N:])
    return s.Matrix([a[i]*(b[(i+1)%N]-b[i]) for i in range(N)]+[2*(a[i]**2-a[i-1]**2) for i in range(N)])

def acquire(f,x,x0):
    start=time.perf_counter();n=len(x);assert n%2==0;N=n//2;assert N>=3
    f=s.Matrix([s.expand(v) for v in f]);xx=s.Matrix(x)
    assert all(s.Poly(v,*x).total_degree()==2 and all(sum(m)==2 for m in s.Poly(v,*x).monoms()) for v in f)
    # Linear invariants and Hessian annihilator: exact coefficient linear algebra.
    ellbasis=coeff_columns(f,x).nullspace();assert len(ellbasis)==1
    ell=ellbasis[0].T
    Hess=[s.hessian(v,x)/2 for v in f]
    ann=s.Matrix.vstack(*Hess).nullspace();assert len(ann)==1
    e=ann[0];assert (ell*e)[0]!=0;e=e/(ell*e)[0]
    P=s.Matrix.hstack(*ell.nullspace());d=n-1
    R=(P.T*P).inv()*P.T
    z=s.symbols('z:'+str(d));zz=s.Matrix(z)
    fw=(R*f).subs(dict(zip(x,P*zz)),simultaneous=True).applyfunc(s.expand)
    assert (f.subs(dict(zip(x,P*zz)),simultaneous=True)-P*fw).applyfunc(s.expand)==s.zeros(n,1)
    # Unique quadratic first integral on the noncentral quotient.
    pairs=[(i,j) for i in range(d) for j in range(i,d)]
    invariants=[s.expand((zz[i]*fw[j]+zz[j]*fw[i]) if i!=j else zz[i]*fw[i]) for i,j in pairs]
    null=coeff_columns(invariants,z).nullspace();assert len(null)==1
    G=s.zeros(d)
    for c,(i,j) in zip(null[0],pairs):G[i,j]=G[j,i]=c
    if G[0,0]<0:G=-G
    assert all(G[:i,:i].det()>0 for i in range(1,d+1))
    assert s.expand((zz.T*G*fw)[0])==0
    Ti=[s.hessian(v,z)/2 for v in fw];Gi=G.inv()
    # C=T T*, D=sum L_k* L_k in the acquired metric, no whitening needed.
    K=s.Matrix(d,d,lambda i,j:s.trace(Gi*Ti[i]*Gi*Ti[j]))
    C=K*G
    Dc=s.zeros(d)
    for i in range(d):
        weighted=s.zeros(d)
        for j in range(d):weighted+=G[i,j]*Ti[j]
        Dc+=Ti[i]*Gi*weighted
    D=Gi*Dc;S=C-4*D
    A=s.Matrix.hstack(*S.columnspace());B=s.Matrix.hstack(*S.nullspace())
    assert A.cols==N and B.cols==N-1
    assert A.T*G*B==s.zeros(N,N-1)
    lam=s.trace(S)/N;assert lam<0 and S*S==lam*S
    GA=A.T*G*A;GAi=GA.inv()
    attempts=0;chosen=None
    # Moment-curve deterministic search. Distinct hidden root functionals give
    # a nonzero discriminant polynomial of degree <=(N-2)N(N-1)/2.
    bound=(N-2)*N*(N-1)//2
    for t in range(bound+1):
        beta=B*s.Matrix([s.Integer(t)**j for j in range(N-1)])
        w=G*beta;Q=s.zeros(d)
        for j in range(d):Q+=w[j]*Ti[j]
        E=GAi*(A.T*Q*A)
        cp=E.charpoly().as_poly();attempts+=1
        if s.gcd(cp,cp.diff()).degree()==0:chosen=E;break
    assert chosen is not None
    ev=chosen.eigenvects();assert len(ev)==N and all(m==1 and len(v)==1 for _,m,v in ev)
    lines=[A*v[0] for _,m,v in ev]
    # Orient line against the supplied initial state (positive Toda sector).
    z0=R*(s.Matrix(x0)-e*(ell*s.Matrix(x0))[0])
    lines=[u if (u.T*G*z0)[0]>0 else -u for u in lines]
    assert all((u.T*G*z0)[0]>0 for u in lines)
    roots=[];hs=[]
    for u in lines:
        h=(u.T*G*u)[0];hs.append(h)
        q=s.Matrix([(u.T*t*u)[0] for t in Ti]);roots.append(q/h)
    gamma=(roots[0].T*G*roots[0])[0]
    assert all((v.T*G*v)[0]==gamma for v in roots)
    gram=s.Matrix(N,N,lambda i,j:s.cancel((roots[i].T*G*roots[j])[0]/gamma))
    assert all(gram[i,j] in [s.Integer(0),s.Rational(-1,2)] for i in range(N) for j in range(N) if i!=j)
    neighbors={i:[j for j in range(N) if j!=i and gram[i,j]==-s.Rational(1,2)] for i in range(N)}
    assert all(len(v)==2 for v in neighbors.values())
    order=[0,min(neighbors[0])]
    while len(order)<N:
        options=[j for j in neighbors[order[-1]] if j!=order[-2]];assert len(options)==1
        order.append(options[0])
    assert len(set(order))==N and order[0] in neighbors[order[-1]]
    lines=[lines[i] for i in order];roots=[roots[i] for i in order];hs=[hs[i] for i in order]
    Xproj=R*(s.eye(n)-e*ell)
    arows=[]
    for u,h in zip(lines,hs):
        row=s.sqrt(gamma*h)/2*(u.T*G/h)*Xproj
        arows.append(row)
    qrows=s.Matrix.vstack(*[(v.T*G)*Xproj for v in roots])
    # q_i=b_i-b_(i+1), with mean beta=ell(x).
    cycle=s.zeros(N)
    for i in range(N):cycle[i,i]=1;cycle[i,(i+1)%N]=-1
    augmented=cycle[:N-1,:].col_join(s.ones(1,N))
    brows=augmented.inv()*qrows[:N-1,:].col_join(N*ell)
    chart=s.Matrix.vstack(*arows,brows);assert chart.det()!=0
    decoded=chart*xx
    residual=(chart*f-toda(decoded)).applyfunc(s.expand)
    assert residual==s.zeros(n,1)
    inverse=chart.inv();assert chart*inverse==s.eye(n) and inverse*chart==s.eye(n)
    transformed0=chart*s.Matrix(x0);assert all(v>0 for v in transformed0[:N])
    return {'N':N,'dimension':n,'quadratic_invariant_dimension_after_center':len(null),
      'split_ranks':[A.cols,B.cols],'contraction_nonzero_eigenvalue':str(lam),
      'simple_spectrum_search_attempts':attempts,'cycle_order':order,
      'raw_coefficient_max_bits':bitmax([c for v in f for c in s.Poly(v,*x).coeffs()]),
      'metric_max_bits':bitmax(G),'contraction_max_bits':bitmax(S),
      'chart_max_bits':bitmax(chart),'inverse_chart_max_bits':bitmax(inverse),
      'raw_terms':sum(len(s.Poly(v,*x).terms()) for v in f),
      'exact_component_identities':n,'both_linear_compositions':True,
      'acquired_chart':[[str(c) for c in row] for row in chart.tolist()],
      'acquired_initial_state':list(map(str,transformed0)),
      'seconds':time.perf_counter()-start}

def mix_matrix(n):
    # Fully public constructor for the equally-informed comparator.
    M=s.eye(n)
    for k in range(2*n):
        i=k%n;j=(3*k+1)%n
        if i==j:j=(j+1)%n
        E=s.eye(n);E[i,j]=(k%3)-1 or 2;M=E*M
    return M

def main():
    out={}
    for N in [3,4,5]:
        n=2*N;x=s.symbols('x:'+str(n));y=s.symbols('y:'+str(n));M=mix_matrix(n);Mi=M.inv()
        f=(M*toda(y)).subs(dict(zip(y,Mi*s.Matrix(x))),simultaneous=True).applyfunc(s.expand)
        y0=s.Matrix(list(range(1,N+1))+[s.Integer((i%3)-1) for i in range(N)])
        ans=acquire(f,x,M*y0)
        # Constructor-aware comparator is FREE to invert M directly; report it,
        # rather than hide the syntax or claim a speed separation.
        t=time.perf_counter();assert (Mi*f-toda(Mi*s.Matrix(x))).applyfunc(s.expand)==s.zeros(n,1)
        ans['constructor_aware_exact_comparator_seconds']=time.perf_counter()-t
        ans['constructor_matrix_public']=[[str(c) for c in r] for r in M.tolist()]
        out['dense_mixed_N'+str(N)]=ans
        print(N,ans['seconds'],ans['raw_terms'],flush=True)
    out['scope']='Exact linear-conjugacy acquisition; no unknown nonlinear conjugacies, no source-aware speedup, historical novelty unassessed.'
    p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(out,indent=2));print(p)
if __name__=='__main__':main()
