"""Bounded floating quadrature for the whole-state isotropic decoder error.

Schur sector probabilities determine trace distance exactly for these invariant
states. The quadrature and scipy arithmetic here are NOT interval certified.
"""
import json
import math
from pathlib import Path
import numpy as np


def logsinh(x):
    return x + np.log(-np.expm1(-2*x)) - math.log(2)


def probe(N, nodes=256):
    q = N**(-.25)
    j = np.arange(N % 2 / 2, N/2 + .1, 1)
    logm = np.log(2*j+1)-np.log(N/2+j+1)+math.lgamma(N+1)-np.array([math.lgamma(v) for v in N/2-j+1])-np.array([math.lgamma(v) for v in N/2+j+1])
    loga = np.log(2*j+1)+logm+2*j*(j+1)/N
    target = np.exp(loga-np.max(loga))
    target /= target.sum()
    roots, weights = np.polynomial.legendre.leggauss(nodes)
    radius = 2*(roots+1)
    density_weights = 2*weights*radius**2*np.exp(-4*radius**4/3)
    density_weights /= density_weights.sum()
    theta = 4*q*radius
    logchar = logsinh((j[:,None]+.5)*theta)-logsinh(theta/2)
    logden = N*np.logaddexp(theta/2,-theta/2)
    sector_kernel = np.exp(logm[:,None]+logchar-logden)
    decoded = sector_kernel@density_weights
    err = .5*np.abs(decoded-target).sum()
    return dict(N=N, nodes=nodes, trace_error=float(err), sqrt_N_error=float(math.sqrt(N)*err),
                normalization_error=float(abs(decoded.sum()-1)),
                max_kernel_normalization_error=float(np.max(abs(sector_kernel.sum(axis=0)-1))))


def main():
    nodes=512
    roots, weights=np.polynomial.legendre.leggauss(nodes)
    r=2*(roots+1)
    p=2*weights*r**2*np.exp(-4*r**4/3)
    p/=p.sum()
    mean_r2=(4/3)**(-.5)*math.gamma(5/4)/math.gamma(3/4)
    h=2*r**2/3+64*r**6/45
    positive_root=next(v.real for v in np.roots([64/45,0,2/3,-2*mean_r2]) if abs(v.imag)<1e-12 and v.real>0)
    threshold=float(np.sqrt(positive_root))
    upper_radius=(4-threshold)*(roots+1)/2+threshold
    upper_weights=(4-threshold)*weights/2*upper_radius**2*np.exp(-4*upper_radius**4/3)
    radial_normalizer=(4/3)**(-.75)*math.gamma(.75)/4
    limit=np.sum(upper_weights*(2*upper_radius**2/3+64*upper_radius**6/45-2*mean_r2))/radial_normalizer
    data=dict(scope="Floating scalar radial quadrature for exact whole Schur-sector trace distance; no interval certification or hardware.",
              predicted_constant=float(limit), mean_r2=float(mean_r2), threshold_radius=threshold,
              coarse=[probe(N) for N in [32,64,128,256,512,1024,2048]],
              refinement=probe(1024,nodes=384),
              forward_radial=[radial_jitter_probe(N) for N in [32,64,128,256,512,1024,2048]],
              forward_refinement=radial_jitter_probe(1024,nodes=96))
    path=Path(__file__).with_name('isotropic_decoder_probe.json')
    path.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))


def radial_jitter_probe(N,nodes=64):
    s=N**.75
    j=np.arange(N % 2 / 2,N/2+.1,1)
    logm=np.log(2*j+1)-np.log(N/2+j+1)+math.lgamma(N+1)-np.array([math.lgamma(v) for v in N/2-j+1])-np.array([math.lgamma(v) for v in N/2+j+1])
    loga=np.log(2*j+1)+logm+2*j*(j+1)/N
    target=np.exp(loga-max(loga)); target/=target.sum()
    lower=j/s; lower[0]=0
    upper=(j+1)/s
    widths=upper-lower
    roots,weights=np.polynomial.legendre.leggauss(nodes)
    r=lower[:,None]+widths[:,None]*(roots+1)/2
    normalizer=(4/3)**(-.75)*math.gamma(.75)/4
    limit_density=r**2*np.exp(-4*r**4/3)/normalizer
    absolute=np.sum(abs(target[:,None]/widths[:,None]-limit_density)*weights*widths[:,None]/2)
    tail_r=upper[-1]+(4-upper[-1])*(roots+1)/2
    tail=np.sum(weights*(4-upper[-1])/2*tail_r**2*np.exp(-4*tail_r**4/3)/normalizer)
    error=(absolute+tail)/2
    return dict(N=N,nodes=nodes,radial_TV=float(error),sqrt_N_TV=float(math.sqrt(N)*error))


if __name__=='__main__':
    main()
