"""Exploratory boundary-resolvent first-passage evaluator.

Arbitrary-precision floating point, NOT an interval or finite-bit certificate.
The numerical algorithm constructs only target-indexed matrices.  An optional
small-state spectral comparator is used solely for checking examples.
"""
import argparse
import json
import time
from pathlib import Path
import mpmath as mp
import numpy as np

def boundary_kernel(p, rates, targets, t):
    e=[mp.exp(-r*t) for r in rates]
    cross=[mp.sqrt(x*(1-x))*(-mp.expm1(-r*t)) for x,r in zip(p,rates)]
    m=len(targets); out=mp.matrix(m,m)
    for a in range(m):
        for b in range(a,m):
            val=mp.mpf(1)
            for i,x in enumerate(p):
                ai=(targets[a]>>i)&1; bi=(targets[b]>>i)&1
                if ai!=bi: val*=cross[i]
                else:
                    z=x if ai else 1-x
                    val*=z+(1-z)*e[i]
            out[a,b]=val; out[b,a]=val
    return out

def target_vector(p,targets):
    return mp.matrix([mp.sqrt(mp.fprod(x if a>>i&1 else 1-x for i,x in enumerate(p))) for a in targets])

def initial_boundary(p,rates,r,targets,t,b):
    q=[x+(a-x)*mp.exp(-rate*t) for x,a,rate in zip(p,r,rates)]
    return [mp.fprod(x if a>>i&1 else 1-x for i,x in enumerate(q))/b[j]
            for j,a in enumerate(targets)]

def exp_polynomial(degree,scale=1):
    """Floating Chebyshev projection and conversion to powers of y."""
    samples=4*(degree+1)
    theta=[mp.pi*(j+mp.mpf('.5'))/samples for j in range(samples)]
    vals=[mp.exp(scale*(1-2/(1+mp.cos(v)))) for v in theta]
    cheb=[(1 if k==0 else 2)*sum(v*mp.cos(k*th) for v,th in zip(vals,theta))/samples
          for k in range(degree+1)]
    a=[mp.mpf(0)]*(degree+1)
    prev=[mp.mpf(1)]; cur=[mp.mpf(-1),mp.mpf(2)]
    for k,c in enumerate(cheb):
        poly=prev if k==0 else cur
        for j,v in enumerate(poly): a[j]+=c*v
        if k>=1 and k<degree:
            nxt=[mp.mpf(0)]*(len(cur)+1)
            for j,v in enumerate(cur): nxt[j]-=2*v; nxt[j+1]+=4*v
            for j,v in enumerate(prev): nxt[j]-=v
            prev,cur=cur,nxt
    return a,cheb

def arbitrary_survival(p,rates,r,targets,t,degree=24,digits=90,step='0.06',scaled_pole=False):
    """Arbitrary-start CDF query; exploratory floating implementation."""
    with mp.workdps(digits):
        p=list(map(mp.mpf,p));rates=list(map(mp.mpf,rates));r=list(map(mp.mpf,r));t=mp.mpf(t)
        scale=degree if scaled_pole else 1
        s=scale/t;step=mp.mpf(step);b=target_vector(p,targets);m=len(targets)
        budget=(digits-12)*mp.log(10)
        lo=int(mp.floor(-budget/step));hi=int(mp.ceil(mp.log(2*budget+10)/step))
        nodes=[]
        for j in range(lo,hi+1):
            v=mp.exp(j*step);factor=step*v
            nodes.append((v,boundary_kernel(p,rates,targets,v/s)*factor,
                          [x*factor for x in initial_boundary(p,rates,r,targets,v/s,b)]))
        count=4*(degree+1);gvals=[];unit=[]
        for ell in range(count):
            w=mp.exp(2j*mp.pi*ell/count);z=1+w/2;mat=mp.matrix(m,m);num=mp.matrix(1,m)
            for v,base,initial in nodes:
                weight=mp.exp(-z*v)
                for a in range(m):
                    num[a]+=weight*initial[a]
                    for c in range(a,m):mat[a,c]+=weight*base[a,c]
            for a in range(m):
                for c in range(a):mat[a,c]=mat[c,a]
            f=(num*mp.lu_solve(mat,b))[0]
            gvals.append((1-f)/z);unit.append(w)
        mass0=sum(mp.fprod(x if a>>i&1 else 1-x for i,x in enumerate(r)) for a in targets)
        moments=[1-mass0]
        for k in range(degree):
            moments.append((-2)**k*sum(g*w**(-k) for g,w in zip(gvals,unit))/count)
        coeff,cheb=exp_polynomial(degree,scale)
        ans=sum(a*v for a,v in zip(coeff,moments))
        return {'survival':float(mp.re(ans)), 'survival_decimal':mp.nstr(mp.re(ans),digits-10),
                'cdf_decimal':mp.nstr(1-mp.re(ans),digits-10),'imag_residual':float(abs(mp.im(ans))),
                'degree':degree,'digits':digits,'components':len(p),'targets':m,'pole_scale':scale,
                'quadrature_nodes':len(nodes),'cauchy_nodes':count,
                'last_chebyshev_coefficient':float(abs(cheb[-1])),
                'coefficient_l1':float(sum(abs(x) for x in coeff)),
                'mass_at_zero':float(mass0)}

def survival(p, rates, targets, t, order=16, digits=40, step='0.15'):
    """Post-Widder plus Cauchy quadrature; dimensionless Green integration."""
    with mp.workdps(digits):
        p=list(map(mp.mpf,p)); rates=list(map(mp.mpf,rates)); t=mp.mpf(t)
        n=order; k=n-1; s=n/t; step=mp.mpf(step)
        b=target_vector(p,targets); m=len(targets)
        # Fixed conservative truncation for these floating diagnostics only.
        # Re(z/s)>=1/2; exp(-v/2) controls the upper tail.
        budget=(digits-8)*mp.log(10)
        lo=int(mp.floor(-budget/step)); hi=int(mp.ceil(mp.log(2*budget+10)/step))
        nodes=[]
        for j in range(lo,hi+1):
            v=mp.exp(j*step)
            nodes.append((v,boundary_kernel(p,rates,targets,v/s)*(step*v)))
        count=max(2*n+16,64); accum=mp.mpc(0)
        for ell in range(count):
            w=mp.exp(2j*mp.pi*ell/count); z=1+w/2
            mat=mp.matrix(m,m)
            for v,base in nodes:
                weight=mp.exp(-z*v)
                for a in range(m):
                    for c in range(a,m): mat[a,c]+=weight*base[a,c]
            for a in range(m):
                for c in range(a): mat[a,c]=mat[c,a]
            f=(b.T*mp.lu_solve(mat,b))[0]/z
            g=(1-f)/z
            accum+=g*w**(-k)
        result=(-1)**k*2**k*accum/count
        return {'survival':float(mp.re(result)), 'imag_residual':float(abs(mp.im(result))),
                'order':n,'targets':m,'components':len(p),'quadrature_nodes':len(nodes),
                'cauchy_nodes':count,'digits':digits,'step':str(step)}

def exact_small(p,rates,targets,t,r=None):
    # Dense symmetric generator on the complement, independent of resolvent.
    p=list(map(float,p)); rates=list(map(float,rates)); n=len(p)
    complement=[x for x in range(1<<n) if x not in targets]
    ix={x:j for j,x in enumerate(complement)}; mat=np.zeros((len(ix),len(ix)))
    b=np.zeros(len(ix));a=np.zeros(len(ix));r=p if r is None else list(map(float,r))
    for x,j in ix.items():
        b[j]=np.sqrt(np.prod([p[i] if x>>i&1 else 1-p[i] for i in range(n)]))
        a[j]=np.prod([r[i] if x>>i&1 else 1-r[i] for i in range(n)])/b[j]
        for i in range(n):
            mat[j,j]-=rates[i]*(1-p[i] if x>>i&1 else p[i])
            y=x^(1<<i)
            if y in ix: mat[j,ix[y]]=rates[i]*np.sqrt(p[i]*(1-p[i]))
    evals,evecs=np.linalg.eigh(mat); weights=(evecs.T@b)*(evecs.T@a)
    return {'survival':float(weights@np.exp(evals*float(t))),
            'post_widder':float(weights@((1-evals*float(t)/16)**(-16))),
            'state_dimension':len(ix)}

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--large',action='store_true')
    args=parser.parse_args(); start=time.time(); cases=[]
    if args.large:
        # Heterogeneous explicitly specified components: no count lumping.
        p=['0.5']*32; rates=[str(1+i/32) for i in range(32)]
        targets=[0,(1<<32)-1]; t=str(2**32/32)
        row=survival(p,rates,targets,t,order=16,digits=45,step='0.12')
        row.update({'time':t,'implicit_states':str(1<<32),'stationary_target_mass':'2^-31'})
        cases.append(row)
    else:
        p=['0.4','0.6','0.7']; rates=['0.3','1.1','2.7']; targets=[0,7]
        for t in ('0.3','2','8'):
            row=survival(p,rates,targets,t)
            exact=exact_small(p,rates,targets,t); row.update({'time':t,'comparator':exact})
            row['integration_error_vs_post_widder']=abs(row['survival']-exact['post_widder'])
            row['smoothing_error_vs_exact']=abs(exact['post_widder']-exact['survival'])
            assert row['integration_error_vs_post_widder']<1e-8
            cases.append(row)
    result={'status':'floating_diagnostic_only','elapsed_seconds':time.time()-start,'cases':cases}
    name='multitarget_large.json' if args.large else 'multitarget_small.json'
    Path(__file__).with_name(name).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
