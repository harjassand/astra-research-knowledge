#!/usr/bin/env python3
"""Positive Gram matrix for two actual local symmetry-breaking errors.

delta*(nL-nR) + epsilon*(nA0-nB0), in the physical rail coordinates.
Outputs leading small-g matrix AND complete finite-g second-order matrices.
"""
import json
import math
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from local_detuning_response import A,B,compute,green,density,surface,smooth_integral


def finite_matrix(g,nq=160):
    rm=compute(g,nq,'memory')
    rr=compute(g,nq,'first_rung')
    lam,N=rm['pair_energy'],rm['pair_normalizer']
    t,w=leggauss(nq)
    theta=(t+1)*np.pi/2
    lo,hi=max(4.,lam-2),min(6.,lam)
    x=(lo+hi)/2-(hi-lo)*np.cos(theta)/2
    y=lam-x
    weight=w*np.pi/2*(hi-lo)*np.sin(theta)/2*density(x,5.,2*g*g)*density(y,1.,g*g)
    gp=lambda s:green(s,5.,2*g*g)
    gm=lambda s:green(s,1.,g*g)
    hp=lambda s:((s-3)*gp(s)-1)/(math.sqrt(2)*g)
    hm=lambda s:((s-3)*gm(s)-1)/g
    mem=-N*(gp(lam-x)+gm(lam-y))-(rm['alpha_real']+1j*rm['alpha_imag'])
    rung=-N*((y-3)/g*hp(lam-x)+(x-3)/(math.sqrt(2)*g)*hm(lam-y))-(rr['alpha_real']+1j*rr['alpha_imag'])
    amp=np.array([mem,rung])
    gram=2*np.pi*np.real(np.einsum('ik,jk,k->ij',amp,amp.conj(),weight))
    ratio=-gram[0,1]/gram[1,1]
    residual=gram[0,0]-gram[0,1]**2/gram[1,1]
    return dict(g=g,matrix_over_g8=(gram/g**8).tolist(),
                optimal_epsilon_over_delta=float(ratio),
                residual_over_g8=float(residual/g**8),
                remaining_fraction=float(residual/gram[0,0]),
                eigenvalues_over_g8=(np.linalg.eigvalsh(gram)/g**8).tolist())


def main():
    pref=3*A/math.sqrt(2)
    W=lambda x:(2/np.pi)**2*(1-(x-5)**2)/(x-3)**4
    m=lambda x:np.real(surface(x,1))
    I=[float(smooth_integral(lambda x,j=j:W(x)*m(x)**j,4,6,200).real) for j in range(3)]
    gram=4*np.pi*np.array([[B*B*I[0], B*pref*I[1]],
                           [B*pref*I[1],pref*pref*I[2]]])
    ratio=-gram[0,1]/gram[1,1]
    res=gram[0,0]-gram[0,1]**2/gram[1,1]
    result=dict(basis=['memory delta*(nL-nR)','first rung epsilon*(nA0-nB0)'],
        kernel_integrals=I,leading_probability_width_matrix=gram.tolist(),
        eigenvalues=np.linalg.eigvalsh(gram).tolist(),
        epsilon_over_delta_minimizer=float(ratio),
        residual_coefficient_per_delta2=float(res),
        remaining_fraction_vs_memory_only=float(res/gram[0,0]),
        finite_g=[finite_matrix(g) for g in [.4,.2,.1,.05,.025]],
        scope='Gamma_pole = g^8 * [delta,epsilon] M [delta,epsilon]^T at leading second order in errors, then small g; no full gate guarantee')
    Path(__file__).with_name('local_error_gram_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
