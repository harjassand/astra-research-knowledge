import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import erf
from math import sqrt,pi
f=lambda x: np.sqrt(2/np.pi)*x*x*np.exp(-x*x/2)
def mean_y_tilt(a):
    if a < 1e-4: return .5-a/12 + a**3/720
    if a> 700: return 1/a
    return 1/a - 1/np.expm1(a)
def P(gamma):
    return quad(lambda x:f(x)*x*(.5-mean_y_tilt(x/gamma)),0,16,epsabs=1e-10)[0]
def tv_tilt_uniform(a):
    if a<1e-4: return a/8
    z=1-np.exp(-a)
    y0=np.log(a/z)/a
    # p= a e^-ay /z, p>1 at y<y0; TV=F_pi(y0)-F_u(y0)
    return -np.expm1(-a*y0)/z-y0
def C(gamma):
    return quad(lambda x:f(x)*tv_tilt_uniform(x/gamma),0,16,epsabs=1e-10)[0]
for gamma in [.01,.03,.05,.1,.15,.2,.3,.5,1,2,10]:
    print(f'gamma={gamma:8g} P_station={P(gamma):.10f} TV_station_to_I={C(gamma):.10f}')
root=brentq(lambda g:P(g)-.5,.0001,1)
print('witness_gamma_critical:',root)
for M in [30,100,300]:
    gamma=.2; nu=gamma*M/.99 # for x around .99 arbitrary test
    q=nu/(nu+1)
    p=q**np.arange(M+1);p=p/p.sum()
    approx=np.exp(-np.arange(M+1)/nu);approx/=approx.sum()
    print('M',M,'TV discrete geometric vs exponent',np.abs(p-approx).sum()/2)
