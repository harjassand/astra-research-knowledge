"""Bounded floating diagnostics for the independent density-transport proof.

These do not certify interval sampling, the PDE argument, or quantum hardware.
"""
import json
import math
from pathlib import Path
import numpy as np
import mpmath as mp

mp.mp.dps = 40

def point_defect(N):
    a = 2 * mp.mpf(N) ** (-mp.mpf(1)/4)
    M = mp.mpf('0.1')
    C = [mp.mpf('.2'), mp.mpf('.05'), mp.mpf('.15')]
    b = [mp.mpf('.1'), mp.mpf('.08'), mp.mpf('.11')]
    x = [mp.mpf('.7'), mp.mpf('-.3'), mp.mpf('.5')]
    t = mp.mpf('.6')
    d0 = 1 - M/(2*mp.sqrt(N))
    def f(*y):
        r = mp.sqrt(sum(z*z for z in y))
        z = a*r
        V = sum(C[i]*y[i]**2+b[i]*y[i] for i in range(3))
        return (mp.sinh(z)/z)*mp.exp(N*mp.log(mp.cosh(z))-2*mp.sqrt(N)*r*r/d0+t*V)
    def data(y, axis):
        r = mp.sqrt(sum(z*z for z in y))
        z = a*r
        beta = z/mp.tanh(z)
        e = [z/r for z in y]
        v = [(beta*(int(i==axis))+(1-beta)*e[axis]*e[i])/a for i in range(3)]
        divv = -2*(beta-1)*e[axis]/z
        s = N*mp.tanh(z)*e[axis]
        return v, s-divv
    def T(fun, axis):
        def out(*y):
            v, h = data(y,axis)
            grad = [mp.diff(fun,tuple(y),tuple(int(i==j) for i in range(3))) for j in range(3)]
            return h*fun(*y)-sum(v[i]*grad[i] for i in range(3))
        return out
    quad = sum(C[i]*T(T(f,i),i)(*x)/(4*mp.mpf(N)**mp.mpf('1.5')) for i in range(3))
    field = sum(b[i]*T(f,i)(*x)/(2*mp.mpf(N)**mp.mpf('.75')) for i in range(3))
    V = sum(C[i]*x[i]**2+b[i]*x[i] for i in range(3))
    defect = (quad+field)/f(*x)-V
    gradlog = [mp.diff(f,tuple(x),tuple(int(i==j) for i in range(3)))/f(*x) for j in range(3)]
    r2=sum(z*z for z in x)
    first = (-mp.mpf(8)/3*r2*sum(C[i]*x[i]**2 for i in range(3))
             -sum(C)/4-mp.mpf('0.5')*sum(C[i]*x[i]*gradlog[i] for i in range(3))
             -mp.mpf(4)/3*r2*sum(b[i]*x[i] for i in range(3))
             -mp.mpf('.25')*sum(b[i]*gradlog[i] for i in range(3)))
    return {'N':N,'density_defect_over_f':float(defect),'sqrtN_defect':float(mp.sqrt(N)*defect),
            'predicted_first_order':float(first)}

def logsinh(z):
    return z+np.log(-np.expm1(-2*z))-math.log(2)

def isotope(N, order=240):
    nodes, weights = np.polynomial.legendre.leggauss(order)
    r = (nodes+1)*2.5
    dr = weights*2.5
    a = 2*N**(-.25)
    z = a*r
    logp = 2*np.log(r)-4*r**4/3
    radial_p = np.exp(logp)*dr
    radial_p /= radial_p.sum()
    logq = 2*np.log(r)+logsinh(z)-np.log(z)+N*(np.logaddexp(z,-z)-math.log(2))-2*math.sqrt(N)*r*r
    radial_q = np.exp(logq)*dr
    radial_q /= radial_q.sum()
    js = np.arange(0 if N%2==0 else .5,N/2+1,1)
    logm = np.array([math.log(2*j+1)-math.log(N+1)+math.lgamma(N+2)-math.lgamma(N/2-j+1)-math.lgamma(N/2+j+2) for j in js])
    ltarget=logm+np.log(2*js+1)+2*js*(js+1)/N
    target=np.exp(ltarget-ltarget.max()); target/=target.sum()
    logk=(logm[:,None]+logsinh((2*js[:,None]+1)*z[None,:])-logsinh(z)[None,:]
          -N*np.logaddexp(z,-z)[None,:])
    kernel=np.exp(logk)
    output=kernel@radial_p
    exactmix=kernel@radial_q
    return {'N':N,'T_universal':float(np.abs(target-output).sum()/2),
            'sqrtN_T':float(math.sqrt(N)*np.abs(target-output).sum()/2),
            'heat_identity_quadrature_T':float(np.abs(target-exactmix).sum()/2),
            'output_mass':float(output.sum()),'quadrature_order':order}

def sharp_constant():
    rad = lambda r:r*r*mp.exp(-4*r**4/3)
    z=mp.quad(rad,[0,1,2,mp.inf])
    h=lambda r:mp.mpf(2)/3*r*r+mp.mpf(64)/45*r**6
    mean=mp.quad(lambda r:rad(r)*h(r),[0,1,2,mp.inf])/z
    cut=mp.findroot(lambda r:h(r)-mean,1)
    kappa=mp.quad(lambda r:rad(r)*(mean-h(r)),[0,cut])/z
    return {'mean_h0':float(mean),'threshold_radius':float(cut),'kappa':float(kappa),
            'meaning':'Predicted exact limit sqrt(N) T for A=b=0, unchanged universal decoder.'}

if __name__=='__main__':
    result={'scope':'Floating proof diagnostics only; no certified sampler or physical emissions.',
            'density_defect':[point_defect(N) for N in [32,128,512,2048]],
            'isotropic_whole_density':[isotope(N) for N in [16,64,256,1024,4096]],
            'sharp_constant':sharp_constant()}
    target=Path(__file__).with_name('transport_checks.json')
    target.write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
