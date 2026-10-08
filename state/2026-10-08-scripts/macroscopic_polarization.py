"""Macroscopic polarization at the s=c/sqrt(N) timescale, fixed nu, and separability witness crossing."""
from math import exp,expm1,sqrt,pi,log
from scipy.integrate import quad
from scipy.optimize import brentq

def mean_y(z):
    if z<1.e-4: return 0.5-z/6+z**3/180
    if z>40: return (z-1)*exp(-z) # negligible higher order
    b=expm1(z)
    return (z*exp(z)-b)/(b*b)

def maxwell(x):return sqrt(2/pi)*x*x*exp(-x*x/2)
def polar(c):return quad(lambda x: maxwell(x)*x*(0.5-mean_y(c*x)),0,16,epsabs=1e-12)[0]
cstar=brentq(lambda c:polar(c)-.5,.00001,50,xtol=1e-12)
print('critical c for spin-variance entanglement witness',repr(cstar))
for c in [0, .5,1,cstar,2,3,5,10]:print('c',c,'lim -<Jz>/sqrt N',repr(polar(c)), 'witness limit squared minus1/4',repr(polar(c)**2-.25))
print('M(infinity)/sqrtN theoretical=',sqrt(2/pi))
