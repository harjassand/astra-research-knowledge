"""Planar anisotropic Lorentz/Maxwell reference model for ASTRA.

NOT a fitted superconducting heterostructure. Inputs and approximation scope
are documented in README.md. Frequency is spectroscopic wavenumber in cm^-1;
q is rad/m. Relative permittivities are dimensionless.
"""
import numpy as np

A=np.array([0,1,1,0,1,0,0,1])
B=1-A
# 0 h10BN, 1 h11BN; SI q and thickness, spectroscopic wavenumbers cm^-1.
def eps(nu,iso,loss=1.0,ideal=False):
    """Return in-plane and normal epsilon; causal e^{-i omega t} convention.

    h10 parameters: Zhang et al., Adv. Sci. (2026), DOI 10.1002/advs.202520556.
    h11 in-plane endpoints: Chen et al., Nat. Commun. (2023), DOI
    10.1038/s41467-023-40449-w. h11 normal-axis frequencies are mass-scaled
    approximations; damping and epsilon-infinity are shared reference values,
    not measurements of the proposed laminate. ideal=True mass-scales both
    in-plane endpoints equally, providing exact static matching.
    """
    if iso not in (0,1) or loss <= 0:
        raise ValueError('iso must be 0 or 1 and loss must be positive')
    scale=1 if iso==0 else 1359.8/1394.5
    TOt=1394.5*scale
    LOt=1650*scale if (ideal or iso==0) else 1608.7
    TOz=785*scale; LOz=845*scale # pure-mass approximation for h11 c axis
    et=5.1*(1+(LOt**2-TOt**2)/(TOt**2-nu**2-1j*nu*1.8*loss))
    ez=2.5*(1+(LOz**2-TOz**2)/(TOz**2-nu**2-1j*nu*1.0*loss))
    return et,ez

def rp(nu,q,seq=A,layer_nm=10,cap_nm=5,loss=1,ideal=False,host=1):
    """p-polarized reflection from an equal-layer hBN stack with h10 end caps.

    Incident relative permittivity is host; terminal half-space is vacuum.
    Retarded kz branches have nonnegative imaginary parts. The specimen used
    in validation has vacuum on BOTH sides. host is not a kappa-ET fit.
    """
    if layer_nm <= 0 or cap_nm < 0 or host <= 0:
        raise ValueError('Invalid layer, cap or host parameter')
    nu,q=np.broadcast_arrays(np.asarray(nu,dtype=complex),np.asarray(q,dtype=complex))
    k0=2*np.pi*100*nu
    # use small frequency limit for static, since finite k0 formula has no divisions by freq
    materials=[(host+0*nu,host+0*nu)]+[eps(nu,int(i),loss,ideal) for i in np.r_[0,seq,0]]+[(1+0*nu,1+0*nu)]
    ds=[cap_nm*1e-9]+[layer_nm*1e-9]*len(seq)+[cap_nm*1e-9]
    kz=[]
    for et,ez in materials:
        k=np.sqrt(et*k0*k0-et/ez*q*q+0j)
        k=np.where((k.imag<0)|((np.abs(k.imag)<1e-15)&(k.real<0)),-k,k)
        kz.append(k)
    rs=[]
    for i in range(len(materials)-1):
        e_i=materials[i][0];e_j=materials[i+1][0]
        rs.append((e_j*kz[i]-e_i*kz[i+1])/(e_j*kz[i]+e_i*kz[i+1]))
    r=rs[-1]
    for i in range(len(ds)-1,-1,-1):
        prop=np.exp(2j*kz[i+1]*ds[i])
        r=(rs[i]+r*prop)/(1+rs[i]*r*prop)
    return r

