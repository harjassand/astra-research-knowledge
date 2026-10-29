"""Independent exact algebra controls for entropy completion. No draws.

Fraction checks are exact. Decimal logarithms and SciPy quadratures are
numerical controls of separately proved ordinary identities.
"""
from fractions import Fraction as F
from decimal import Decimal, localcontext
from pathlib import Path
from itertools import permutations
import hashlib
import json
import math
from scipy.integrate import quad


def zero(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def mul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def inv(a):
    n = len(a)
    z = [[F(x) for x in row]+[F(i == j) for j in range(n)] for i, row in enumerate(a)]
    for j in range(n):
        k = next(k for k in range(j, n) if z[k][j])
        z[j], z[k] = z[k], z[j]
        d = z[j][j]; z[j] = [x/d for x in z[j]]
        for i in range(n):
            if i != j:
                d = z[i][j]; z[i] = [x-d*y for x, y in zip(z[i], z[j])]
    return [row[n:] for row in z]


def dec(x):
    return Decimal(x.numerator)/Decimal(x.denominator)


def generator(flow, w):
    assert all(sum(flow[i]) == sum(row[i] for row in flow) for i in range(len(w)))
    q = [[flow[i][j]/w[i] for j in range(len(w))] for i in range(len(w))]
    for i in range(len(w)): q[i][i] = -sum(q[i])
    return q


def build(wb, channels, means, stages, direct):
    m, chains, w = len(wb), {}, list(wb)
    for key, a in sorted(channels.items()):
        chains[key] = list(range(len(w), len(w)+stages))
        w += [a*means[key[2]]/stages]*stages
    f, theta = zero(len(w)), list(range(len(w)))
    for i in range(m):
        for j in range(m): f[i][j] = direct[i][j]
    for (i, j, k), ids in chains.items():
        path = [i]+ids+[j]
        for x, y in zip(path, path[1:]): f[x][y] = channels[i, j, k]
        rev = chains[j, i, k]
        for l, x in enumerate(ids): theta[x] = rev[-1-l]
    q = generator(f, w)
    assert all(theta[theta[i]] == i and q[i][i] == q[theta[i]][theta[i]] for i in range(len(w)))
    return q, w, f, theta


def entropy(q, w, f, theta):
    rate, naive = Decimal(0), Decimal(0)
    for x in range(len(q)):
        for y in range(len(q)):
            if x != y and f[x][y]:
                a, b = theta[y], theta[x]
                assert q[a][b] > 0
                rate += dec(f[x][y])*dec(q[x][y]/q[a][b]).ln()
                naive += dec(f[x][y])*dec(f[x][y]/f[a][b]).ln()
        rate += dec(w[x]*(q[x][x]-q[theta[x]][theta[x]]))
    boundary = sum(dec(w[x])*dec(w[x]/w[theta[x]]).ln() for x in range(len(w)))/dec(sum(w))
    return rate, boundary, naive


def transform(q, w, m, s):
    ii = list(range(m, len(q)))
    g = inv([[(s if i == j else 0)-q[x][y] for j, y in enumerate(ii)] for i, x in enumerate(ii)])
    A = [[w[i]*q[i][x] for x in ii] for i in range(m)]
    B = [[q[x][j] for j in range(m)] for x in ii]
    return mul(mul(A, g), B)


def channel_controls():
    outputs = []
    for n in [1, 3, 7]:
        q, w, f, theta = build([F(1), F(2)], {(0,1,0):F(3), (1,0,0):F(1)},
                               {0:F(2)}, n, [[F(0),F(1)],[F(3),F(0)]])
        E, D, naive = entropy(q, w, f, theta)
        assert abs(E-4*Decimal(3).ln()) < Decimal('1e-65')
        assert abs(D-4*Decimal(3).ln()/11) < Decimal('1e-65')
        assert abs(naive-2*(n+2)*Decimal(3).ln()) < Decimal('1e-65')
        assert sum(w[2:]) == 8 and [-q[0][0],-q[1][1]] == [4,2]
        for s in [F(0),F(1,3),F(1),F(5)]:
            g = (F(n)/(n+2*s))**n
            assert transform(q,w,2,s) == [[0,3*g],[g,0]]
        outputs.append(dict(stages=n, states=len(w), intrinsic_E=E, stationary_boundary_D=D,
                            incorrect_flux_expression=naive, total_mass=sum(w)))
    return outputs


def mixture():
    q,w,f,theta=build([F(1)]*2,{(0,1,0):F(3),(1,0,0):F(1),(0,1,1):F(1),(1,0,1):F(3)},
                      {0:F(1),1:F(1,2)},1,zero(2))
    E,D,naive=entropy(q,w,f,theta)
    J=-Decimal(8)/3+Decimal(15)/2*(Decimal(5)/3).ln()-Decimal(7)/18*Decimal(7).ln()
    assert sum(w[2:])==6 and 0<J<E
    assert abs(E-4*Decimal(3).ln())<Decimal('1e-65')
    num,err=quad(lambda x:(2-4*x)*math.log((3+2*x)/(1+6*x)),0,1,epsabs=1e-12,epsrel=1e-12)
    assert abs(num-float(J))<1e-11
    for s in [F(0),F(1),F(3)]:
        k=transform(q,w,2,s)
        assert k[0][1]==3/(s+1)+2/(s+2) and k[1][0]==1/(s+1)+6/(s+2)
    return dict(states=len(w),intrinsic_E=E,observed_J=J,stationary_boundary_D=D,
                quadrature=num,quadrature_error_estimate=err,
                exact_finite_saturation='Impossible by non-exponential-ratio theorem in ordinary proof.')


def path_order_obstruction():
    f,w=zero(5),[F(1)]*5
    path=[0,2,1,3,4,0]
    for i,j in zip(path,path[1:]): f[i][j]=F(1)
    q=generator(f,w)
    ii=[2,3,4]
    A=[[q[i][x] for x in ii] for i in [0,1]]
    B=[[q[x][j] for j in [0,1]] for x in ii]
    T=[[q[x][y] for y in ii] for x in ii]
    assert mul(A,B)==[[0,1],[0,0]]
    assert mul(mul(A,T),B)==[[0,-1],[1,0]]
    for s in [F(0),F(1),F(3)]:
        k=transform(q,w,2,s)
        assert k==[[0,1/(s+1)],[1/(s+1)**2,0]]
    parities=[]
    for p in permutations(ii):
        theta=[0,1]+list(p)
        if all(theta[theta[i]]==i for i in range(5)):
            bad=[(i,j) for i in range(5) for j in range(5)
                 if i!=j and q[i][j]>0 and q[theta[j]][theta[i]]==0]
            assert bad
            parities.append(dict(theta=theta,unsupported_reversed_edges=bad))
    assert len(parities)==4
    num,err=quad(lambda t:math.exp(-t)*(1-t)*(-math.log(t)),0,math.inf,
                 epsabs=1e-11,epsrel=1e-11)
    assert abs(num-1)<1e-10
    return dict(states=5,total_mass=F(5),hidden_mass=F(3),departure_flux=F(2),
                observed_J_exact=F(1),quadrature=num,quadrature_error_estimate=err,
                all_parities_of_displayed_generator=parities,
                all_dimensions_statement='Ordinary shortest-path proof covers all finite completions; enumeration only checks this generator.')


def exact_exponential_attainment():
    a,delta=F(3),F(1,2)
    alpha=[[F(1,3),F(2,3)]]
    T=[[F(-3),F(1)],[F(1,2),F(-2)]]
    r=[[-sum(row)] for row in T]
    z=mul([[a*x for x in alpha[0]]],inv([[-x for x in row] for row in T]))[0]
    assert z==[F(6,11),F(14,11)]
    Tl=[[T[j][i]*z[j]/z[i] for j in range(2)] for i in range(2)]
    rl=[[a*alpha[0][i]/z[i]] for i in range(2)]
    betal=[[z[i]*r[i][0]/a for i in range(2)]]
    shifted=[[(-Tl[i][j]+(delta if i==j else 0)) for j in range(2)] for i in range(2)]
    h=[row[0] for row in mul(inv(shifted),rl)]
    assert h==[F(7,9),F(16,21)]
    C=sum(betal[0][i]*h[i] for i in range(2))
    assert C==F(76,99)
    b=a
    Tm=[[(Tl[i][j]-(delta if i==j else 0))*h[j]/h[i] for j in range(2)] for i in range(2)]
    rm=[rl[i][0]/h[i] for i in range(2)]
    betam=[betal[0][i]*h[i]/C for i in range(2)]
    zm=mul([[b*x for x in betam]],inv([[-x for x in row] for row in Tm]))[0]
    assert Tm==[[F(-7,2),F(8,7)],[F(7,16),F(-5,2)]]
    assert rm==[F(33,14),F(33,16)] and betam==[F(7,19),F(12,19)]
    assert zm==[F(91,209),F(200,209)]
    w=[F(1),F(2)]+z+zm
    q=zero(6)
    for x in range(2):
        q[0][2+x]=a*alpha[0][x]/w[0]
        q[1][4+x]=b*betam[x]/w[1]
        q[2+x][1]=r[x][0]
        q[4+x][0]=rm[x]
        for y in range(2):
            if x!=y:
                q[2+x][2+y]=T[x][y]
                q[4+x][4+y]=Tm[x][y]
    for i in range(6): q[i][i]=-sum(q[i])
    f=[[w[i]*q[i][j] if i!=j else F(0) for j in range(6)] for i in range(6)]
    assert generator(f,w)==q
    theta=[0,1,4,5,2,3]
    E,D,naive=entropy(q,w,f,theta)
    target=delta*(sum(z)-sum(zm))
    assert target==F(89,418)
    hold=sum(w[i]*(q[i][i]-q[theta[i]][theta[i]]) for i in range(6))
    assert hold==target and abs(E-dec(target))<Decimal('1e-65')
    checks=[]
    for s in [F(0),F(1,3),F(1),F(3),F(5)]:
        k=transform(q,w,2,s)
        shifted_kernel=transform(q,w,2,s+delta)
        assert k[1][0]==shifted_kernel[0][1]/C
        checks.append(dict(s=s,transform=k))
    return dict(states=6,forward_T=T,reverse_T=Tm,forward_entrance=alpha[0],
                reverse_entrance=betam,forward_weights=z,reverse_weights=zm,
                h=h,C=C,delta=delta,exact_intrinsic_and_observed_entropy=target,
                evaluated_intrinsic_entropy=E,exact_holding_contribution=hold,
                stationary_boundary_information=D,total_mass=sum(w),
                exact_shifted_transform_checks=checks)


def serialize(x):
    if isinstance(x,(F,Decimal)): return str(x)
    if isinstance(x,dict): return {k:serialize(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [serialize(v) for v in x]
    return x


def main():
    with localcontext() as ctx:
        ctx.prec=75
        result=dict(status='PASS',channels=channel_controls(),mixture=mixture(),
                    path_order=path_order_obstruction(),
                    exponential_attainment=exact_exponential_attainment(),source_draws=0,
                    code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
        out=Path(__file__).with_name('ENTROPY_COMPLETION_CHECKS.json')
        out.write_text(json.dumps(serialize(result),indent=2)+'\n')
        print(json.dumps(dict(status='PASS',exact_generator_models=6,exact_transform_checks=23,
                              displayed_graph_parities=4,source_draws=0,output=str(out)),indent=2))


if __name__=='__main__': main()
