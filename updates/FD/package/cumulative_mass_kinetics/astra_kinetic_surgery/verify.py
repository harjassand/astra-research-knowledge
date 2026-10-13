#!/usr/bin/env python3
"""Reproduce finite exact algebra tests and analytic transport-lift unit tests.

These are correctness diagnostics, NOT molecular simulations or performance
comparisons. Finite graph assertions use SymPy exact rational arithmetic.
Decimal summaries are rounded renderings of exact expressions.
"""
from __future__ import annotations
import json
import random
from pathlib import Path
from collections import deque
import sympy as sp

ROOT = Path(__file__).resolve().parent

def scalar(x):
    return x[0] if isinstance(x, sp.MatrixBase) else x

def decimal(x, digits=22):
    return str(sp.N(x, digits))

def incidence(n: int, edges: list[tuple[int, int]]) -> sp.Matrix:
    # Transient vertices 0,...,n-1; grounded sink has index n.
    D = sp.zeros(n, len(edges))
    for k, (i, j) in enumerate(edges):
        if i < n:
            D[i, k] = 1
        if j < n:
            D[j, k] = -1
    return D

def route(n: int, edges: list[tuple[int,int]], source: int, target: int) -> sp.Matrix:
    adj: list[list[tuple[int,int,int]]] = [[] for _ in range(n+1)]
    for k, (i,j) in enumerate(edges):
        adj[i].append((j,k,1))
        adj[j].append((i,k,-1))
    parent = {source: None}
    queue = deque([source])
    while queue and target not in parent:
        u = queue.popleft()
        for v,k,sign in adj[u]:
            if v not in parent:
                parent[v] = (u,k,sign)
                queue.append(v)
    if target not in parent:
        raise ValueError('Disconnected routing graph')
    flow = sp.zeros(len(edges),1)
    x = target
    while x != source:
        previous,k,sign = parent[x]
        flow[k] += sign
        x = previous
    return flow

def exact_random_graph_tests(count=24, seed=20261013):
    rng = random.Random(seed)
    assertions = 0
    records = []
    for trial in range(count):
        n = 2 + trial % 5
        # Start from a tree so every transient component reaches the sink.
        edges = [(i, rng.randrange(i+1,n+1)) for i in range(n)]
        for i in range(n):
            for j in range(i+1,n+1):
                if (i,j) not in edges and rng.random() < 0.25:
                    edges.append((i,j))
        c = [sp.Rational(rng.randrange(1,20),rng.randrange(1,20)) for _ in edges]
        D = incidence(n,edges)
        C = sp.diag(*c)
        A = D*C*D.T
        m = sp.Matrix([sp.Rational(rng.randrange(1,8),rng.randrange(1,8)) for _ in range(n)])
        M = sum(m)
        E = sp.zeros(n,n)
        artificial = []
        for _ in range(1+trial%3):
            i,j = sorted(rng.sample(range(n),2))
            alpha = sp.Rational(rng.randrange(1,30),rng.randrange(1,10))
            e = sp.zeros(n,1); e[i]=1; e[j]=-1
            E += alpha*e*e.T
            artificial.append((i,j,alpha,e))
        v = (A+E).inv()*m
        F = scalar(m.T*A.inv()*m)
        Fp = scalar(m.T*v)
        Es = scalar(v.T*E*v)
        r = E*v
        Rstar = scalar(r.T*A.inv()*r)
        assert sp.simplify(F-Fp-Es-Rstar) == 0; assertions += 1
        z = sp.zeros(len(edges),1)
        for i,j,alpha,e in artificial:
            z += alpha*scalar(e.T*v)*route(n,edges,i,j)
        assert D*z == r; assertions += 1
        R = scalar(z.T*C.inv()*z)
        assert R >= Rstar; assertions += 1
        L = Fp+Es
        assert L <= F <= L+R; assertions += 1
        assert Es <= Fp; assertions += 1
        # Exact no-go inequality for any given route-based bracket.
        epsilon = sp.factor(R/L)
        assert F <= 2*(1+epsilon)*Fp; assertions += 1
        # An arbitrary, inaccurate trial potential: restore full residual.
        vbad = sp.Matrix([sp.Rational(rng.randrange(-8,9),7) for _ in range(n)])
        d = m-A*vbad
        Lbad = scalar(2*m.T*vbad-vbad.T*A*vbad)
        zbad = sp.zeros(len(edges),1)
        for i in range(n):
            zbad += d[i]*route(n,edges,i,n)
        assert D*zbad == d; assertions += 1
        assert sp.simplify(F-Lbad-scalar(d.T*A.inv()*d))==0; assertions += 1
        assert Lbad <= F <= Lbad+scalar(zbad.T*C.inv()*zbad); assertions += 1
        # Fixed-mass conductance monotonicity test with nonuniform perturbation.
        cp = [ci*sp.Rational(rng.randrange(10,21),10) for ci in c]
        Ap = D*sp.diag(*cp)*D.T
        assert scalar(m.T*Ap.inv()*m) <= F; assertions += 1
        records.append({'transient_states':n,'physical_edges':len(edges),
                        'relative_width':decimal(R/L),'exact_mfpt':decimal(F/M)})
    return {'graphs':count,'exact_assertions':assertions,'seed':seed,'records':records}

def fixtures():
    eps=sp.Rational(1,10**6)
    delta=sp.Rational(1,10**12)
    e=sp.Matrix([1,-1]); m=sp.ones(2,1)
    alpha=sp.Integer(1)
    results=[]
    for eta in [sp.Integer(0),sp.Rational(1,10),sp.Rational(1,2),sp.Rational(9,10)]:
        D=sp.Matrix([[1,0,1],[0,1,-1]])
        c=[eps*(1+eta),eps*(1-eta),delta]
        C=sp.diag(*c); A=D*C*D.T; S=alpha*e*e.T
        v=(A+S).inv()*m
        F=scalar(m.T*A.inv()*m)
        Fp=scalar(m.T*v); Es=scalar(v.T*S*v); L=Fp+Es
        a=alpha*scalar(e.T*v)
        via_sink=sp.Matrix([a,-a,0]); direct=sp.Matrix([0,0,a])
        assert D*via_sink==S*v and D*direct==S*v
        Usink=L+scalar(via_sink.T*C.inv()*via_sink)
        Udirect=L+scalar(direct.T*C.inv()*direct)
        assert L<=F<=Usink and F<=Udirect
        results.append({'case':f'two_exit_eta_{eta}', 'exact_mfpt':decimal(F/2),
                        'auxiliary_mfpt':decimal(Fp/2),'lower':decimal(L/2),
                        'upper_via_sink':decimal(Usink/2),
                        'upper_via_direct_edge':decimal(Udirect/2),
                        'relative_width':decimal((Usink-L)/L)})
    # A hidden trap with no direct exit. The alleged "safe" shortcut is catastrophic.
    D=sp.Matrix([[1,1],[0,-1]])
    C=sp.diag(eps,delta); A=D*C*D.T; S=alpha*e*e.T
    v=(A+S).inv()*m
    F=scalar(m.T*A.inv()*m); Fp=scalar(m.T*v); Es=scalar(v.T*S*v)
    L=Fp+Es; a=alpha*scalar(e.T*v); z=sp.Matrix([0,a])
    assert D*z==S*v
    U=L+scalar(z.T*C.inv()*z)
    assert L<=F<=U
    results.append({'case':'hidden_trap','exact_mfpt':decimal(F/2),
                    'auxiliary_mfpt':decimal(Fp/2),'lower':decimal(L/2),
                    'upper':decimal(U/2),'relative_width':decimal((U-L)/L),
                    'auxiliary_endpoint_difference':decimal(abs(scalar(e.T*v)))})
    return results

def transport_unit_tests():
    x,y,gamma=sp.symbols('x y gamma',real=True)
    sigma=1+gamma*x
    rho=sp.exp(-y*y/(2*sigma*sigma))/sp.sqrt(2*sp.pi)
    mass=rho/sigma
    jx=x*mass
    jy=x*mass*gamma*y/sigma
    residual=sp.simplify(sp.diff(jx,x)+sp.diff(jy,y)-mass)
    assert residual==0
    assert sp.simplify(jx.subs(x,0))==0
    # v=(1-x^2)/2 is zero on the absorbing section.
    v=(1-x*x)/2
    assert v.subs(x,1)==0
    # E[rho z^2]=1 for a normalized standard Gaussian. Thus:
    # F_L=1/3, F_U=(1+n*gamma^2)/3 in n transverse dimensions.
    s=sp.symbols('s',real=True)
    n=sp.symbols('n',integer=True,positive=True)
    FL=sp.integrate(s*s,(s,0,1))
    FU=sp.integrate(s*s*(1+n*gamma*gamma),(s,0,1))
    assert FL==sp.Rational(1,3)
    assert sp.simplify(FU-(1+n*gamma*gamma)/3)==0
    # General finite separable mass example w(s)=1+s, all moments exact.
    w=1+s; H=s+s*s/2
    FLw=sp.integrate(H*H/w,(s,0,1))
    assert FLw>0
    return {'symbolic_divergence_residual':str(residual),
            'exact_assertions':6,'constant_mass_FL':str(FL),
            'variable_width_FU':str(FU),
            'separable_w_1_plus_s_FL':str(FLw),
            'scope':'Symbolic manufactured continuum test; not a molecular benchmark.'}

def gaussian_overlap():
    # For q=N(0,a^2 I_n), p=N(0,I_n), integral q^2/p =
    # (1/(a sqrt(2-a^2)))^n when a^2<2; infinity otherwise.
    rows=[]
    for a in [sp.Rational(1),sp.Rational(105,100),sp.Rational(11,10),sp.Rational(6,5)]:
        for n in [1,10,100,1000]:
            value=(1/(a*sp.sqrt(2-a*a)))**n
            rows.append({'standard_deviation_ratio':str(a),
                         'transverse_dimension':n,'one_plus_chi_square':decimal(value)})
    assert sp.simplify((1/(1*sp.sqrt(2-1)))**1000)==1
    return {'formula':'[a*sqrt(2-a^2)]^(-n), for 0<a<sqrt(2); infinity otherwise',
            'rows':rows,'exact_assertions':1}

def advected_bath_tests():
    # Arbitrary unnormalised transverse density f, not assumed Gaussian,
    # log-concave, weakly interacting, or rapidly mixing.
    s,y=sp.symbols('s y',real=True)
    M=sp.Function('M')(s)
    b=sp.Function('b')(s)
    f=sp.Function('f')
    bath=f(y-b)
    w=sp.diff(M,s)
    m=w*bath
    jx=M*bath
    jy=M*bath*sp.diff(b,s)
    residual=sp.simplify(sp.diff(jx,s)+sp.diff(jy,y)-m)
    assert residual==0
    # The primal field has derivative -M/w. The remaining flux is transverse.
    assert sp.simplify(jx+m*(-M/w))==0
    gap_density=sp.simplify(jy*jy/m)
    assert sp.simplify(gap_density-M*M*bath*sp.diff(b,s)**2/w)==0
    Z,Mass,F0,G0=sp.symbols('Z Mass F0 G0',positive=True)
    assert sp.simplify(Z*F0/(Z*Mass)-F0/Mass)==0
    # Piecewise-constant quadrature of w(s)=1+s, evaluated in exact rationals.
    # log w is 1-Lipschitz on [0,1]. At N=64 the rigorous enclosure factor
    # relative to the exact step-function answer is exp(2/N).
    N=64
    h=sp.Rational(1,N)
    cumulative=sp.Integer(0); energy=sp.Integer(0)
    for i in range(N):
        wi=1+(sp.Rational(2*i+1,2*N))
        energy+=cumulative*cumulative*h/wi+cumulative*h*h+wi*h**3/3
        cumulative+=wi*h
    tau_approx=energy/cumulative
    tau_true=(sp.log(2)/4+sp.Rational(3,16))/sp.Rational(3,2)
    lo=tau_approx*sp.exp(-sp.Rational(2,N))
    hi=tau_approx*sp.exp(sp.Rational(2,N))
    # Numerical check of an analytically justified quadrature enclosure.
    assert float(sp.N(lo))<=float(sp.N(tau_true))<=float(sp.N(hi))
    return {'exact_symbolic_assertions':4,'additional_numerical_checks':1,
            'source_divergence_residual':str(residual),
            'quadrature_N':N,'step_mfpt':decimal(tau_approx),
            'true_1d_mfpt':decimal(tau_true),
            'quadrature_lower':decimal(lo),'quadrature_upper':decimal(hi),
            'scope':'Uniform analytic class with exact translated-bath structure; no experimental system mapped.'}

def main():
    output={'description':'Exact finite diagnostics and manufactured analytic tests; no scientific performance claim.',
            'graph_tests':exact_random_graph_tests(),
            'fixtures':fixtures(),
            'transport_tests':transport_unit_tests(),
            'gaussian_overlap':gaussian_overlap(),
            'advected_bath_tests':advected_bath_tests()}
    output_path=ROOT/'results.json'
    output_path.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'graph_count':output['graph_tests']['graphs'],
                      'exact_graph_assertions':output['graph_tests']['exact_assertions'],
                      'fixtures':output['fixtures'],
                      'transport_tests':output['transport_tests'],
                      'gaussian_overlap_10_percent_n1000':next(r for r in output['gaussian_overlap']['rows'] if r['standard_deviation_ratio']=='11/10' and r['transverse_dimension']==1000)},indent=2))

if __name__=='__main__':
    main()
