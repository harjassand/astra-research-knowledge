"""Independent exact transcription checks for the full-rank stopping proof.

No stochastic sampler or asymptotic theorem is tested here. All writes are
owned. Small actual tensor kernels are compared to the differential generator;
logdet drift/QV are reconstructed using inverse matrices and the Hessian.
"""
from pathlib import Path
import json
import time
import sympy as s


def tr(x):
    return s.trace(x)


def same(x, y):
    assert all(s.simplify(t) == 0 for t in x - y)


def tensor(xs):
    result = s.ones(1, 1)
    for x in xs:
        result = s.kronecker_product(result, x)
    return result


def dk(rho, n, z):
    result = s.zeros(rho.rows ** n)
    for i in range(n):
        xs = [rho] * n
        xs[i] = z
        result += tensor(xs)
    return result


def d2k(rho, n, z, w):
    result = s.zeros(rho.rows ** n)
    for i in range(n):
        for j in range(n):
            if i != j:
                xs = [rho] * n
                xs[i], xs[j] = z, w
                result += tensor(xs)
    return result


def fixture(d, n):
    if d == 2:
        rho = s.Matrix([[s.Rational(3, 5), s.Rational(1, 20)],
                        [s.Rational(1, 20), s.Rational(2, 5)]])
    else:
        rho = s.Matrix([[s.Rational(1, 2), s.Rational(1, 30), s.I/40],
                        [s.Rational(1, 30), s.Rational(1, 3), s.Rational(1, 50)],
                        [-s.I/40, s.Rational(1, 50), s.Rational(1, 6)]])
    # Rational, nonorthonormal axes: the generator/logdet identities do not
    # require normalization. Full-basis completeness is tested separately.
    t0 = s.diag(1, -1, *([0] * (d - 2)))
    t1 = s.zeros(d); t1[0, 1] = t1[1, 0] = 1
    t2 = s.zeros(d); t2[0, d-1] = -s.I; t2[d-1, 0] = s.I
    ts = [t0, t1, t2]
    c = s.Matrix([[s.Rational(3, 2), s.Rational(1, 3), -s.Rational(1, 7)],
                  [s.Rational(1, 3), s.Rational(7, 6), s.Rational(1, 11)],
                  [-s.Rational(1, 7), s.Rational(1, 11), s.Rational(4, 3)]])
    bs = [s.Rational(1, 5), -s.Rational(2, 7), s.Rational(1, 13)]
    ident = s.eye(d)
    fs = [sum((tensor([t if j == i else ident for j in range(n)])
               for i in range(n)), s.zeros(d ** n)) for t in ts]
    k = tensor([rho] * n)
    means = [tr(rho * t) for t in ts]
    vs = [(t*rho + rho*t)/2 - m*rho for t, m in zip(ts, means)]
    rs = [-s.I * (t*rho-rho*t) for t in ts]

    def dv(j, z):
        return (ts[j]*z+z*ts[j])/2-tr(z*ts[j])*rho-means[j]*z

    def dr(j, z):
        return -s.I * (ts[j]*z-z*ts[j])

    for f, t, mean, v, r in zip(fs, ts, means, vs, rs):
        same((f*k+k*f)/2, n*mean*k+dk(rho, n, v))
        same(-s.I*(f*k-k*f), dk(rho, n, r))
        v_t = tr(v*t)
        v_derivative = (t*v+v*t)/2-tr(v*t)*rho-mean*v
        r_derivative = -s.I*(t*r-r*t)
        second = (n*n*mean*mean+n*v_t)*k + 2*n*mean*dk(rho,n,v)
        second += dk(rho,n,v_derivative)+d2k(rho,n,v,v)
        second -= (dk(rho,n,r_derivative)+d2k(rho,n,r,r))/4
        same((f*f*k+k*f*f)/2, second)

    q = sum((c[i,j]*(fs[i]*fs[j]+fs[j]*fs[i])/2
             for i in range(3) for j in range(3)), s.zeros(d**n))
    field = sum((b*f for b,f in zip(bs,fs)), s.zeros(d**n))
    big_k = q/n+field
    local_b = sum((b*t for b,t in zip(bs,ts)), s.zeros(d))
    vb = (local_b*rho+rho*local_b)/2-tr(rho*local_b)*rho
    drift = vb.copy()
    hessian_k = s.zeros(d**n)
    hessian_log = 0
    qv = 0
    inv = rho.inv()
    for i in range(3):
        for j in range(3):
            drift += c[i,j]*(means[i]*vs[j]+means[j]*vs[i])
            drift += c[i,j]*(dv(j,vs[i])-dr(j,rs[i])/4)/n
            hessian_k += c[i,j]*(d2k(rho,n,vs[i],vs[j])-d2k(rho,n,rs[i],rs[j])/4)/n
            hessian_log += c[i,j]*(-tr(inv*vs[i]*inv*vs[j])+tr(inv*rs[i]*inv*rs[j])/4)/n
            qv += 2*c[i,j]*(tr(inv*vs[i])*tr(inv*vs[j])-tr(inv*rs[i])*tr(inv*rs[j])/4)/n
    potential = tr(big_k*k)
    reconstructed = potential*k+dk(rho,n,drift)+hessian_k
    same((big_k*k+k*big_k)/2, reconstructed)
    zc = sum((c[i,j]*(ts[i]*ts[j]+ts[j]*ts[i])/2
              for i in range(3) for j in range(3)), s.zeros(d))
    xcx = sum(c[i,j]*means[i]*means[j] for i in range(3) for j in range(3))
    expected_drift = -d*(2-s.Rational(1,n))*xcx-d*tr(rho*zc)/n-d*tr(rho*local_b)
    assert s.simplify(tr(inv*drift)+hessian_log-expected_drift) == 0
    assert s.simplify(qv-2*d*d*xcx/n) == 0
    return {'d':d,'N':n,'first_order_filter_and_rotation':True,
            'square_identity_all_axes':True,'full_mixed_generator':True,
            'logdet_drift':str(s.factor(expected_drift)),
            'logdet_qv':str(s.factor(qv))}


def full_basis(d):
    ts=[]
    for i in range(d):
        for j in range(i+1,d):
            x=s.zeros(d); x[i,j]=x[j,i]=1/s.sqrt(2);ts.append(x)
            y=s.zeros(d); y[i,j]=-s.I/s.sqrt(2);y[j,i]=s.I/s.sqrt(2);ts.append(y)
    for k in range(1,d):
        t=s.zeros(d)
        for i in range(k):t[i,i]=1/s.sqrt(k*(k+1))
        t[k,k]=-k/s.sqrt(k*(k+1));ts.append(t)
    return ts


def completeness_and_compact():
    rows=[]
    for d in (2,3):
        rho=s.diag(*[s.Rational(2**i,2**d-1) for i in range(d)])
        z=s.diag(1,-1,*([0]*(d-2)))
        z[0,d-1]=1+s.I;z[d-1,0]=1-s.I
        means=tr(rho*z)
        lhs=0
        for t in full_basis(d):
            v=(t*rho+rho*t)/2-tr(rho*t)*rho
            r=-s.I*(t*rho-rho*t)
            lhs += tr(z*v)**2-tr(z*r)**2/4
        rhs=tr(rho*(z-means*s.eye(d))*rho*(z-means*s.eye(d)))
        assert s.simplify(lhs-rhs)==0
        rows.append({'d':d,'isotropic_full_basis_identity':True})
    # Proper spin-one compact Lie representation, rho=e^(log2 Jz)/Z.
    rho=s.diag(s.Rational(4,7),s.Rational(2,7),s.Rational(1,7))
    jx=s.Matrix([[0,1,0],[1,0,1],[0,1,0]])
    jy=s.Matrix([[0,-s.I,0],[s.I,0,-s.I],[0,s.I,0]])
    jz=s.diag(1,0,-1)
    for t, kt in [(jx,-jy/3),(jy,jx/3),(jz,s.zeros(3))]:
        r=-s.I*(t*rho-rho*t)
        v=(kt*rho+rho*kt)/2-tr(rho*kt)*rho
        same(r/2,v)
    rows.append({'proper_compact_group':'spin1_SU2','R_over2_equals_V_K_exact':True,
                 'K_root_tanh':'1/3'})
    return rows


if __name__=='__main__':
    start=time.perf_counter()
    result={'status':'PASS_EXACT_TRANSCRIPTION',
            'generator_fixtures':[fixture(d,n) for d in (2,3) for n in (1,2)],
            'local_geometry_fixtures':completeness_and_compact(),
            'scope':'Small exact identities only; no SDE sampler or asymptotic theorem verification.'}
    result['runtime_seconds']=time.perf_counter()-start
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'runtime_seconds':result['runtime_seconds']}))
