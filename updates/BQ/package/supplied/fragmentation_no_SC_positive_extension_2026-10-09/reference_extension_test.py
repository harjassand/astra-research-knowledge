"""Deterministic continuous-kernel checks for the provisional extension.

Independent classical uniformization + trapezoidal spatial quadrature forward;
closed reference density; two linear Volterra inverse quadratures.
"""
import json
import numpy as np
from scipy.integrate import quad
from scipy.special import hyp1f1,gammaln
from scipy.stats import poisson


def reference_density(a,s,b,gamma):
    s=np.asarray(s);a=np.asarray(a)
    return a*b*np.exp(-a-b*s)*hyp1f1(1+b/gamma,2,a*(-np.expm1(-gamma*s)))


def density_forward(k,s,t,gamma):
    h=s[1]-s[0];D=np.exp(-gamma*s)
    M=int(poisson.isf(1e-15,t))+4
    weights=np.exp(-t+np.arange(M+1)*np.log(t)-gammaln(np.arange(M+1)+1))
    v=np.zeros_like(s);atom=1.;f=np.zeros_like(s)
    for m in range(M):
        dv=D*v
        gain=h*(np.convolve(k,dv)[:len(s)]-.5*k*dv[0]-.5*k[0]*dv)
        v=(1-D)*v+k*atom+gain
        atom=0.
        f+=weights[m+1]*v
    return f


def reference_inverse(f,s,t,gamma,b):
    h=s[1]-s[0];D=np.exp(-gamma*s)
    E=np.exp(-t*D);d=E-np.exp(-t)
    base=reference_density(t,s,b,gamma)
    residual=f-base
    r=np.zeros_like(s);k=np.zeros_like(s);k[0]=b
    # Data-derived one-sided boundary derivative, not supplied from true k.
    r[0]=(-11*residual[0]+18*residual[1]-9*residual[2]+2*residual[3])/(6*h*t*gamma*np.exp(-t))
    for n in range(1,len(s)):
        u=s[1:n]
        A=f[n-1:0:-1]-reference_density(t*np.exp(-gamma*u),s[n]-u,b,gamma)
        Ann=f[0]-reference_density(t*D[n],0.,b,gamma)
        numerator=residual[n]+h*(.5*residual[n]*r[0]+np.dot(A,r[1:n]))
        r[n]=numerator/(d[n]-.5*h*Ann)
    kb=b*np.exp(-b*s)
    for n in range(1,len(s)):
        source=(1-D[n])*r[n]+kb[n]
        source+=h*(.5*kb[n]*r[0]+np.dot(kb[n-1:0:-1],D[1:n]*r[1:n])+.5*b*D[n]*r[n])
        k[n]=(source-h*np.dot(k[n-1:0:-1],r[1:n])-.5*h*b*r[n])/(1+.5*h*r[0])
    return k,r


def main():
    result={'reference_transform':[],'independent_forward':[],'inverse_mesh':[]}
    for a in [.3,2.,4.]:
      for b in [1.,2.,3.7]:
       gamma=1.3
       for lam in [.2,1.,3.]:
        numerical=np.exp(-a)+quad(lambda s:np.exp(-lam*s)*reference_density(a,s,b,gamma),0,np.inf,epsabs=1e-11)[0]
        exact=hyp1f1(lam/gamma,(lam+b)/gamma,-a)
        result['reference_transform'].append({'a':a,'b':b,'lambda':lam,'error':float(abs(numerical-exact))})
    gamma=1.3;t=2.;b=1.
    # True binary daughter law: half uniform, half Beta(3,3).
    # The mass-weighted log-jump density has k(0)=1, so SC fails.
    for hfine in [.004,.002]:
        s=np.arange(round(4/hfine)+1)*hfine
        k=np.exp(-2*s)+30*np.exp(-4*s)*(1-np.exp(-s))**2
        f=density_forward(k,s,t,gamma)
        fref=density_forward(b*np.exp(-b*s),s,t,gamma)
        result['independent_forward'].append({'h':hfine,
            'reference_sup_error':float(max(abs(fref-reference_density(t,s,b,gamma)))),
            'boundary_error':float(abs(f[0]-t*np.exp(-t)*b))})
        for h in [.08,.04,.02]:
            step=round(h/hfine);sc=s[::step];fc=f[::step];truth=k[::step]
            kh,r=reference_inverse(fc,sc,t,gamma,b)
            result['inverse_mesh'].append({'forward_h':hfine,'inverse_h':h,
                'kernel_l1':float(np.trapezoid(abs(kh-truth),sc)),
                'kernel_sup_error':float(max(abs(kh-truth))),
                'boundary_r_estimate':float(r[0]),'boundary_r_true':-1/gamma,
                'min_recovered_density':float(min(kh))})
    print(json.dumps(result,indent=2))
    with open('reference_extension_results.json','w') as fh:json.dump(result,fh,indent=2)

if __name__=='__main__':main()
