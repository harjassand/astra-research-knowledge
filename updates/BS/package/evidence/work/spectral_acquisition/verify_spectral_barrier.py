"""Finite diagnostics for analytic obstructions; Python 3 + NumPy only.
No empirical matrix/sample claim. Run from any working directory.
"""
import json, math, time
from pathlib import Path
import numpy as np


def sc(z, variance):
    z=np.asarray(z, dtype=complex)
    s=np.sqrt(z*z-4*variance)
    s=np.where(s.imag<0, -s, s)
    return 2/(z+s)


def atomic(z, x, p):
    return np.sum(p/(np.asarray(z)[...,None]-x),axis=-1)


def semicircle_quadrature(k,a):
    theta=np.arange(1,k+1)*np.pi/(k+1)
    return 2*math.sqrt(a)*np.cos(theta), 2*np.sin(theta)**2/(k+1)


def free_atomic(z,x,p,b,tol=1e-15):
    z=np.asarray(z,dtype=complex)
    if b >= np.min(z.imag)**2:
        raise ValueError('This diagnostic only uses contraction-certified nodes')
    g=atomic(z,x,p)
    for it in range(10000):
        nxt=atomic(z-b*g,x,p)
        if np.max(np.abs(nxt-g))<tol:
            return nxt,it+1
        g=nxt
    raise RuntimeError('fixed point did not converge')


def rational_quadrature_demo():
    z=np.array([-1+.8j, .3+1.1j, 1.4+.7j])
    t0=1.25; t=.2; m=len(z)
    g=sc(z,t0); w=z-t*g
    # Reference semicircle Gaussian quadrature, then Lanczos for modified measure.
    # This is floating diagnostic construction, not interval certification.
    x_ref,p_ref=semicircle_quadrature(4096,t0-t)
    q_ref=np.prod(np.abs(w[:,None]-x_ref[None,:])**2,axis=0)
    rho=p_ref/q_ref; mass=np.sum(rho)
    v=np.sqrt(rho/mass); basis=[]; diag=[]; off=[]; prev=np.zeros_like(v)
    beta=0.
    for j in range(m+1):
        basis.append(v.copy())
        r=x_ref*v-beta*prev
        alpha=np.dot(v,r); r-=alpha*v
        for u in basis: r-=np.dot(u,r)*u
        diag.append(alpha)
        if j<m:
            beta=np.linalg.norm(r); off.append(beta); prev=v; v=r/beta
    jac=np.diag(diag)+np.diag(off,1)+np.diag(off,-1)
    nodes,U=np.linalg.eigh(jac)
    rho_weights=mass*U[0,:]**2
    weights=rho_weights*np.prod(np.abs(w[:,None]-nodes[None,:])**2,axis=0)
    interpolation=float(np.max(np.abs(atomic(w,nodes,weights)-g)))
    forward,it=free_atomic(z,nodes,weights,t)
    forward_error=float(np.max(np.abs(forward-g)))
    assert abs(np.sum(weights)-1)<1e-12 and np.min(weights)>0
    assert interpolation<1e-12 and forward_error<1e-12
    return dict(m=m,original_noise=t0,alternative_noise=t,alternative_atoms=nodes.tolist(),
                alternative_weights=weights.tolist(),mass_error=float(abs(np.sum(weights)-1)),
                interpolation_error=interpolation,forward_error=forward_error,iterations=it)


def explicit_hard_family():
    a=1.; b=.25; eta=1.; sigma=.01; failure=.25
    r=(math.sqrt(eta*eta+4*a)-eta)/(2*math.sqrt(a))
    z=np.concatenate([np.linspace(-5,5,4001)+1j*height for height in [eta,1.5,2.]])
    rows=[]; max_identity_error=0.
    for k in [2,5,10,20,30]:
        x,p=semicircle_quadrature(k,a)
        q=math.sqrt(a)*sc(z,a)
        analytic=sc(z,a)*(1-q**(2*k))/(1-q**(2*k+2))
        identity_error=float(np.max(np.abs(analytic-atomic(z,x,p))))
        max_identity_error=max(max_identity_error,identity_error)
        assert identity_error<1e-13
        error_bound=(r**(2*k+1)*(1+r*r)/(math.sqrt(a)*(1-r**(2*k+2))))/(1-b/(eta*eta))
        g,it=free_atomic(z,x,p,b)
        observed=float(np.max(np.abs(g-sc(z,a+b))))
        # Below double precision the theorem, not floating difference, controls.
        assert observed<=error_bound+5e-14
        lower_queries=4*sigma*sigma*(1-2*failure)**2/(error_bound*error_bound)
        rows.append(dict(k=k,variance_gap=a,analytic_uniform_bound=error_bound,
                         grid_max_difference=observed,
                         gaussian_query_lower_bound=lower_queries,iterations=it))
    return dict(a=a,b=b,eta=eta,per_coordinate_sigma=sigma,delta=failure,r=r,
                max_formula_error=max_identity_error,rows=rows)

def full_law_barrier():
    a=1.; b=1.; c=a+b; r=.75; rho=math.sqrt(a/c)
    radius=2*math.sqrt(a)+2*math.sqrt(b)
    rows=[]
    for k in [20,50,100,200]:
        e=r**(2*k+1)*(1+r*r)/(math.sqrt(a)*(1-r**(2*k+2)))
        d=(b/c)*r**(2*k+2)*(1+r*r)/(1-r**(2*k+2))
        h=3*math.sqrt(d)/math.sqrt(a)+e
        gate=rho+3*math.sqrt(d)<r
        tv=radius*h/math.pi
        assert gate and tv<1
        rows.append(dict(k=k,E=e,D=d,H=h,gate_left=rho+3*math.sqrt(d),
                         gate_right=r,tv_upper_bound=tv,
                         iid_lower_bound_linear=.5/tv,
                         iid_lower_bound_product=math.log(2)/(-math.log1p(-tv))))
    # Low-imaginary transform replay: Newton on the proven physical branch.
    k=20
    z=np.linspace(-4.5,4.5,9001)+1e-4j
    q=math.sqrt(a)*sc(z,c)
    for it in range(100):
        num=q**(2*k+1)*(1-q*q); den=1-q**(2*k+2)
        ep=-num/(math.sqrt(a)*den)
        np_=(2*k+1)*q**(2*k)-(2*k+3)*q**(2*k+2)
        dp_=-(2*k+2)*q**(2*k+1)
        dep=-(np_*den-num*dp_)/(math.sqrt(a)*den*den)
        res=c/math.sqrt(a)*q*q-z*q+math.sqrt(a)+b*q*ep
        deriv=2*c/math.sqrt(a)*q-z+b*(ep+q*dep)
        step=res/deriv
        q=q-step
        if np.max(np.abs(step))<1e-14: break
    else: raise RuntimeError('Newton diagnostic failed')
    ep=-q**(2*k+1)*(1-q*q)/(math.sqrt(a)*(1-q**(2*k+2)))
    h=q/math.sqrt(a)+ep
    atoms,weights=semicircle_quadrature(k,a)
    residual=float(np.max(np.abs(h-atomic(z-b*h,atoms,weights))))
    discrepancy=float(np.max(np.abs(h-sc(z,c))))
    assert np.max(q.imag)<0 and np.max(np.abs(q))<r
    assert residual<1e-12 and discrepancy<=rows[0]['H']+1e-13
    return dict(a=a,b=b,r=r,rho=rho,rows=rows,
                low_imaginary_diagnostic=dict(eta=1e-4,k=k,grid_nodes=len(z),
                max_physical_residual=residual,max_transform_difference=discrepancy,
                newton_iterations=it+1,note='finite diagnostic; not interval-certified TV'))


def lower_height_repair():
    rows=[]
    for k in [5,10,20,50,100]:
        z=1j/(k+1); x,p=semicircle_quadrature(k,1.)
        gap=float(abs(atomic(np.asarray(z),x,p)-sc(z,1.)))
        bound=1/(2*math.e)
        assert gap>=bound
        rows.append(dict(k=k,eta=1/(k+1),gap=gap,lower_bound=bound))
    return dict(scope='b=0 pair only; direct support test is stronger IID baseline',rows=rows)

if __name__=='__main__':
    start=time.perf_counter()
    result=dict(status='FINITE_DIAGNOSTICS_ONLY',exact_transcript=rational_quadrature_demo(),
                quantitative=explicit_hard_family(),full_law=full_law_barrier(),
                lower_height_repair=lower_height_repair())
    result['runtime_seconds']=time.perf_counter()-start
    out=Path(__file__).with_name('spectral_diagnostics.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
