#!/usr/bin/env python3
"""Finite diagnostics for the projected Gaussian construction.

No finite sampled-rank test certifies the uniform low-rank norm used in the
proof. The theorem-sized matrices are NOT materialized. All tests here check
identities, scaling and explicit separable decompositions in small dimensions.
"""
from __future__ import annotations
import json, math, platform
from pathlib import Path
from fractions import Fraction
import numpy as np
import scipy
from numpy.linalg import eigh, eigvalsh, norm, svd

ROOT = Path(__file__).resolve().parents[1]
RNG = np.random.default_rng(2026100803)


def basis_sym0(d: int) -> np.ndarray:
    out = []
    for i in range(d):
        for j in range(i + 1, d):
            a = np.zeros((d, d)); a[i,j] = a[j,i] = 1/math.sqrt(2)
            out.append(a)
    for k in range(1, d):
        a = np.zeros((d, d)); a[np.arange(k),np.arange(k)] = 1
        a[k,k] = -k
        out.append(a/math.sqrt(k*(k+1)))
    return np.array(out)


def partial_transpose(a: np.ndarray, d: int) -> np.ndarray:
    return a.reshape(d,d,d,d).transpose(0,3,2,1).reshape(d*d,d*d)


def partial_traces(a: np.ndarray, d: int):
    q = a.reshape(d,d,d,d)
    return np.einsum('ijil->jl',q), np.einsum('ijkj->ik',q)


def orthogonal_projection(a: np.ndarray, d: int) -> np.ndarray:
    # For a real symmetric input, this first average makes both local
    # transposes invariant. Remove the two identity sectors afterwards.
    a = (a + partial_transpose(a,d))/2
    ta,tb = partial_traces(a,d)
    eye = np.eye(d)
    return (a - np.kron(eye/d,ta) - np.kron(tb,eye/d)
            + np.trace(a)*np.eye(d*d)/(d*d))


def gaussian_projected(d: int):
    m=d*d
    a=RNG.normal(size=(m,m))
    # Isotropic standard Gaussian in the real symmetric HS space:
    # diagonal variance 1; off-diagonal variance 1/2.
    a=(a+a.T)/2
    return orthogonal_projection(a,d)/d


def random_rank_vector(d: int,k: int):
    u,_=np.linalg.qr(RNG.normal(size=(d,k))+1j*RNG.normal(size=(d,k)))
    v,_=np.linalg.qr(RNG.normal(size=(d,k))+1j*RNG.normal(size=(d,k)))
    s=RNG.random(k); s/=norm(s)
    return ((u*s)@v.conj().T).reshape(-1)


def sep_ball_decomposition(e: np.ndarray,r: int,d: int, eps: float):
    """Return positive tensor factors for I+e, provided ||e||<=eps<=1/(2r-1)."""
    terms=[]; eye=np.eye(d); blocks=e.reshape(r,d,r,d)
    for i in range(r):
        a=np.zeros((r,r),complex); a[i,i]=1
        b=eye+blocks[i,:,i,:]-2*eps*(r-1)*eye
        terms.append((a,b))
    for i in range(r):
        for j in range(i+1,r):
            p=np.zeros((r,r),complex); p[i,i]=p[j,j]=1
            x=np.zeros((r,r),complex); x[i,j]=x[j,i]=1
            y=np.zeros((r,r),complex); y[i,j]=1j; y[j,i]=-1j
            z=blocks[i,:,j,:]
            h=(z+z.conj().T)/2
            k=(z-z.conj().T)/(2j)
            for a,b in ((x,h),(y,k)):
                terms.append(((p+a)/2,eps*eye+b))
                terms.append(((p-a)/2,eps*eye-b))
    return terms


def map_from_choi(c: np.ndarray,x: np.ndarray,d: int):
    return np.einsum('ij,iajb->ab',x,c.reshape(d,d,d,d))


def exact_constants():
    c=2**23
    # Relax log(49)<4 and log(9)<5/2; these follow from the exponential series.
    assert sum(Fraction(4)**i/math.factorial(i) for i in range(10)) > 49
    assert sum(Fraction(5,2)**i/math.factorial(i) for i in range(10)) > 9
    assert Fraction(25,8)-Fraction(5,2) > Fraction(1,2)
    assert Fraction(1,65536)-Fraction(36,c) >= Fraction(1,131072)
    assert Fraction(1,1)-Fraction(32,6)*Fraction(9,40)==-Fraction(1,5)
    assert (Fraction(9,40)/6-Fraction(1,64))/10==Fraction(7,3200)
    assert Fraction(1,5)/Fraction(11,6)==Fraction(6,55)
    rows=[]
    for r in range(1,65):
        d=c*r**3
        assert 32*Fraction(1,64*r) <= Fraction(1,2*r-1)
        assert Fraction(d*d,65536*r*r)-36*d*r >= Fraction(d*d,131072*r*r)
        # All three failure terms are far below exp(-100) at this d.
        assert d*d/2 > 100 and Fraction(d**4,1600)>100 and Fraction(d*d,131072*r*r)>100
        rows.append({'r':r,'sufficient_d':d})
    return {'dimension_constant':c,'r_eb_examples':rows,
            'state_half_trace_gap':'7/3200','map_diamond_gap':'6/55',
            'strict_witness_pairing_bound':'-1/5','r2_sufficient_d':c*8}


def main():
    maxima={'basis_gram':0.,'basis_trace':0.,'projection_two_implementations':0.,
      'gaussian_hs_identity':0.,'partial_transpose':0.,'partial_trace':0.,
      'separable_reconstruction':0.,'separable_factor_negative':0.,
      'choi_action':0.,'choi_pure_compression':0.,'map_tp_unital':0.,
      'svd_split_reconstruction':0.}
    counts={'basis_dimensions':0,'basis_projection_fixtures':0,'gaussian_samples':0,
      'complex_rank_pairs':0,'separable_ball_fixtures':0,'choi_fixtures':0,
      'svd_split_fixtures':0}
    # Two distinct implementations of the same orthogonal projection.
    for d in range(2,10):
        s=basis_sym0(d); h=len(s); counts['basis_dimensions']+=1
        maxima['basis_gram']=max(maxima['basis_gram'],float(norm(np.einsum('aij,bij->ab',s,s)-np.eye(h))))
        maxima['basis_trace']=max(maxima['basis_trace'],float(np.max(abs(np.trace(s,axis1=1,axis2=2)))))
        for _ in range(4):
            a=RNG.normal(size=(d*d,d*d)); a=(a+a.T)/2
            coeff=np.einsum('aij,bkl,ikjl->ab',s,s,a.reshape(d,d,d,d), optimize=True)
            direct=np.einsum('ab,aij,bkl->ikjl',coeff,s,s,optimize=True).reshape(d*d,d*d)
            proj=orthogonal_projection(a,d)
            maxima['projection_two_implementations']=max(maxima['projection_two_implementations'],float(norm(direct-proj)))
            maxima['gaussian_hs_identity']=max(maxima['gaussian_hs_identity'],float(abs(np.sum(proj*proj)-np.sum(coeff*coeff))))
            counts['basis_projection_fixtures']+=1
    diagnostics=[]
    for d in [2,3,4,6,8,12,16,24]:
        for trial in range(3):
            g=gaussian_projected(d); m=d*d; counts['gaussian_samples']+=1
            ev=eigvalsh(g); energy=float(np.sum(g*g)/m)
            maxima['partial_transpose']=max(maxima['partial_transpose'],float(norm(g-partial_transpose(g,d))))
            ta,tb=partial_traces(g,d)
            maxima['partial_trace']=max(maxima['partial_trace'],float(max(norm(ta),norm(tb))))
            rank_results=[]
            for k in sorted(set([1,min(2,d),min(4,d)])):
                sampled=0.
                for _ in range(40):
                    x=random_rank_vector(d,k); y=random_rank_vector(d,k)
                    sampled=max(sampled,float(abs(np.vdot(x,g@y))))
                    counts['complex_rank_pairs']+=1
                rank_results.append({'rank_cap':k,'sampled_bilinear_max_lower_bound_only':sampled})
            rho=(np.eye(m)+g/6)/m; w=np.eye(m)-32*g
            diagnostics.append({'d':d,'trial':trial,'op_norm':float(max(abs(ev))),
              'hs_energy_div_d_squared':energy,'rho_min_eigenvalue':float((1+ev[0]/6)/m),
              'w_rho_pairing':float(np.trace(w@rho)),'rank_tests':rank_results,
              'claim':'Not a uniform rank-norm certificate; small d is below theorem regime.'})
    for r in [1,2,3,4,6]:
        for d in [2,3,5,9]:
            for _ in range(5):
                z=RNG.normal(size=(r*d,r*d))+1j*RNG.normal(size=(r*d,r*d))
                e=(z+z.conj().T)/2; eps=1/(2*r-1)
                e*=eps/max(abs(eigvalsh(e)))
                terms=sep_ball_decomposition(e,r,d,eps)
                recovered=sum((np.kron(a,b) for a,b in terms),start=np.zeros_like(e))
                maxima['separable_reconstruction']=max(maxima['separable_reconstruction'],float(norm(recovered-np.eye(r*d)-e)))
                low=min(min(eigvalsh(a)[0],eigvalsh(b)[0]) for a,b in terms)
                maxima['separable_factor_negative']=max(maxima['separable_factor_negative'],float(max(0,-low)))
                counts['separable_ball_fixtures']+=1
    for d in [3,4,6,8]:
        s=basis_sym0(d); h=len(s)
        for _ in range(5):
            coeff=RNG.normal(size=(h,h))
            g=np.einsum('ab,aij,bkl->ikjl',coeff,s,s,optimize=True).reshape(d*d,d*d)/d
            c=(np.eye(d*d)-32*g)/d
            x=RNG.normal(size=(d,d))+1j*RNG.normal(size=(d,d))
            direct=np.trace(x)*np.eye(d)/d -32/d**2*np.einsum('ab,a,bkl->kl',coeff,np.einsum('aij,ji->a',s,x),s)
            via=map_from_choi(c,x,d)
            maxima['choi_action']=max(maxima['choi_action'],float(norm(via-direct)))
            ta,tb=partial_traces(c,d)
            maxima['map_tp_unital']=max(maxima['map_tp_unital'],float(max(norm(ta-np.eye(d)),norm(tb-np.eye(d)))))
            r=min(2,d); v,_=np.linalg.qr(RNG.normal(size=(d,r))+1j*RNG.normal(size=(d,r)))
            a=RNG.normal(size=(r,r))+1j*RNG.normal(size=(r,r))
            psi=(a@v.T).reshape(-1); p=np.outer(psi,psi.conj()).reshape(r,d,r,d)
            out=np.zeros((r,d,r,d),complex)
            for i in range(r):
                for j in range(r): out[i,:,j,:]=map_from_choi(c,p[i,:,j,:],d)
            iso=np.kron(v.conj(),np.eye(d))
            compressed=iso.conj().T@c@iso
            filtered=np.kron(a,np.eye(d))@compressed@np.kron(a.conj().T,np.eye(d))
            maxima['choi_pure_compression']=max(maxima['choi_pure_compression'],float(norm(out.reshape(r*d,r*d)-filtered)))
            counts['choi_fixtures']+=1
    for d in [4,8,12]:
        for k in [1,2]:
            for _ in range(20):
                z=random_rank_vector(d,min(2*k,d)).reshape(d,d)
                u,s,vh=svd(z,full_matrices=False)
                z1=(u[:,:k]*s[:k])@vh[:k,:]
                z2=(u[:,k:2*k]*s[k:2*k])@vh[k:2*k,:]
                maxima['svd_split_reconstruction']=max(maxima['svd_split_reconstruction'],float(norm(z-z1-z2)))
                assert norm(z1)+norm(z2)<=math.sqrt(2)+1e-12
                counts['svd_split_fixtures']+=1
    constants=exact_constants()
    assert max(maxima.values())<1e-9, maxima
    result={'status':'INTERNAL FINITE DIAGNOSTICS, not external validation or uniform low-rank certification',
      'seed':2026100803,'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
      'counts':counts,'max_absolute_residuals':maxima,'exact_constants':constants,
      'gaussian_small_dimension_diagnostics':diagnostics,
      'not_executed':['The theorem-sized random matrices','An exhaustive Schmidt-rank net','A quantifier-elimination certificate','Tensor-stability for all powers']}
    dest=ROOT/'results'/'gaussian_verification.json'
    dest.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'counts':counts,'max_absolute_residuals':maxima,'output':str(dest)},indent=2))

if __name__=='__main__': main()
