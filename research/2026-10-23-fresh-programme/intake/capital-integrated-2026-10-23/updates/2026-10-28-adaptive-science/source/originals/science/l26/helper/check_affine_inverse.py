"""Finite Hermite checks; the infinite-dimensional proof is AFFINE_INVERSE.md."""
from pathlib import Path
import csv
import math
import numpy as np

ROOT = Path(__file__).resolve().parent


def sample_inverse_correction(residual, g, z, kappa, rng):
    """One residual-value action; unbiased for delta_Z T^-1 P_a residual.

    g,z may be arrays of jointly independent standard Gaussians for the
    integrated L2 receipt, or fixed outer values for conditional unbiasedness.
    The residual must accept its two scalar/array arguments.
    """
    a=math.sqrt(1-kappa*kappa)
    normal=rng.standard_normal((4,)+np.shape(g))
    q=np.sum(normal[:3]**2,axis=0)/np.sum(normal**2,axis=0)
    w1,w2=rng.standard_normal((2,)+np.shape(g))
    yz=q*z+np.sqrt(1-q*q)*w1
    yg=(a*g-kappa*(1-q)*z
        +kappa*q*np.sqrt((1-q)/(1+q))*w1
        +kappa*np.sqrt(2*q/(1+q))*w2)
    v=(np.sqrt(2*q*(1-q))*z
       -math.sqrt(2)*q*np.sqrt(q/(1+q))*w1
       +np.sqrt((1-q)/(1+q))*w2)
    return math.pi/(2*math.sqrt(2)*a)*v*residual(yg,yz)


def sector(n, kappa, rho=1.0):
    a = math.sqrt(1-kappa*kappa)
    T = np.diag(a*(np.arange(n+1)+2))
    for j in range(1, n+1):
        T[j,j-1] = kappa*math.sqrt((n-j+1)*j)
    V = np.zeros((n+1,n+1))
    for ell in range(n+1):
        V[ell,ell] = rho**(n-ell)/(a*(ell+2))
        for j in range(ell+1,n+1):
            V[j,ell] = -kappa*math.sqrt((n-j+1)*j)/(a*(j+2))*V[j-1,ell]
    return a,T,V


def main():
    records=[]
    max_relative_error=0.0
    for kappa in [0.1,0.5,0.8,0.95]:
        for n in [0,1,2,5,10,20,50,100,200]:
            a,T,V=sector(n,kappa,math.sqrt(1-kappa*kappa))
            target=np.diag(a**(n-np.arange(n+1)))
            error=np.linalg.norm(T@V-target,2)/max(1.0,np.linalg.norm(target,2))
            max_relative_error=max(max_relative_error,error)
            norms=[]
            for power in [0.0,0.5,1.0]:
                norms.append(np.linalg.norm((np.arange(n+1)+1)[:,None]**power*V,2))
            records.append([kappa,a,n,error,*norms])
            assert norms[0] <= 1/(2*a)+1e-10
            c0=4+2*math.sqrt(2)/3
            assert norms[2] <= 1/a+c0/(a*a)
        for n in [1,2,5,10,20,50]:
            a,T,V=sector(n,kappa,1.0)
            explicit=np.array([
                (-kappa/a)**j*math.sqrt(math.comb(n,j))/(a*(j+1)*(j+2))
                for j in range(n+1)
            ])
            assert np.allclose(V[:,0],explicit,rtol=1e-12,atol=1e-13)
    with (ROOT/'affine_inverse_checks.csv').open('w',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(['kappa','a','total_chaos','relative_residual','J_norm','u_norm','DZu_norm'])
        writer.writerows(records)
    min_noise_eig=1.0
    min_damping_eig=1.0
    for kappa in [.01,.1,.5,.8,.95,.999]:
        a=math.sqrt(1-kappa*kappa)
        for q in np.linspace(.001,.999,999):
            B=np.array([[a,0],[-kappa*(1-q),q]])
            C=np.eye(2)-B@B.T
            D=np.diag([kappa*kappa*q/2,q*(1-q)/2])
            min_noise_eig=min(min_noise_eig,np.linalg.eigvalsh(C)[0])
            min_damping_eig=min(min_damping_eig,np.linalg.eigvalsh(C-D)[0])
            assert np.linalg.eigvalsh(C-D)[0]>=-1e-12
    print(f'Max sector relative residual: {max_relative_error:.3g}')
    print(f'Min tested noise eigenvalue: {min_noise_eig:.3g}')
    print(f'Min tested damping remainder eigenvalue: {min_damping_eig:.3g}')
    print('At kappa=0.5, critical-smoothed D_Zu norms:')
    for r in records:
        if r[0]==.5 and r[2] in [0,20,100,200]:
            print(f'  n={r[2]}: {r[-1]:.9g}; 1/a={1/r[1]:.9g}')
    rng=np.random.default_rng(231974)
    g,z=rng.standard_normal((2,1000000))
    kappa=.5
    a=math.sqrt(1-kappa*kappa)
    sample=sample_inverse_correction(lambda x,y:(x*x-1)/math.sqrt(2),g,z,kappa,rng)
    coefficients=sector(2,kappa,a)[2][:,0]
    u=(coefficients[0]*(g*g-1)/math.sqrt(2)*z
       +coefficients[1]*math.sqrt(2)*g*(z*z-1)/math.sqrt(2)
       +coefficients[2]*math.sqrt(3)*(z*z*z-3*z)/math.sqrt(6))
    print('Monte Carlo formula check (not a proof or a TV certificate):')
    print(f'  E[Uhat^2]={np.mean(sample*sample):.8g}; exact={math.pi**2/(8*a*a):.8g}')
    print(f'  E[Uhat*u]={np.mean(sample*u):.8g}; E[u^2]={np.mean(u*u):.8g}')
    print('Exact Gaussian full-TV check for constant residual R=c, X=0, tau=1:')
    Phi=lambda x:(1+math.erf(x/math.sqrt(2)))/2
    phi1=math.exp(-.5)/math.sqrt(2*math.pi)
    for c in [.01,.1,.5,1.0]:
        s1=math.sqrt(1+c*c/(4*a*a))
        s2=math.sqrt(1+math.pi**2*c*c/(8*a*a))
        crossing=math.sqrt(2*math.log(s2/s1)/(1/(s1*s1)-1/(s2*s2)))
        exact_tv=2*(Phi(crossing/s1)-Phi(crossing/s2))
        bound=phi1*c*c/(a*a)*(math.pi**2/8-.25)
        assert exact_tv<=bound+1e-12
        print(f'  c={c}: TV={exact_tv:.8g}; bound={bound:.8g}')
    print('All checks passed. Output: affine_inverse_checks.csv')


if __name__=='__main__':
    main()
