"""Instantiate the universal passive phonon design and inverse spectra.

The mathematical theorem is FAMILY_THEOREM.md. Numerical results here
instantiate its exact objects; floating-point residuals are not a replacement
for its analytic global proof or a uniform conditioning guarantee.
"""
import json, math
from pathlib import Path
from fractions import Fraction
import numpy as np

HERE=Path(__file__).resolve().parent
GLX,GLW=np.polynomial.legendre.leggauss(96)

def bose(w,theta):
    x=w/theta
    if abs(x)<1e-3:
        y=x*x
        return 1-y/12+y*y/240-y*y*y/6048
    if x>50:
        z=math.exp(-x)
        return x*x*z/(1-z)**2
    z=math.expm1(x)
    return x*x*(z+1)/(z*z)

def band_integral(a,b,theta):
    # Exponentially tiny tails beyond 80 theta are omitted, explicitly.
    if a>=80*theta: return 0.
    b=min(b,80*theta)
    if b<=a: return 0.
    n=max(1,math.ceil((b-a)/(4*theta)))
    ans=0.
    for j in range(n):
        lo=a+(b-a)*j/n;hi=a+(b-a)*(j+1)/n
        mid=(lo+hi)/2;half=(hi-lo)/2
        ans+=half*sum(float(wt)*bose(mid+half*float(x),theta)
                      for x,wt in zip(GLX,GLW))
    return ans

def endpoints(r,A,B):
    d=math.hypot(r*r+A-2*B,2*math.sqrt(B*(A-B)))
    s2=(r*r+A+d)/2
    p2=B*r*r/s2
    return math.sqrt(p2),math.sqrt(s2),d

def derivative(r,A,B,theta):
    p,s,d=endpoints(r,A,B)
    pp=r*B*(A-B)/(p*d*(s*s-B))
    sp=r*(s*s-B)/(s*d)
    return bose(p,theta)*pp+bose(s,theta)*sp-bose(r,theta)

def design_optimum(K,M,m0,theta):
    assert K>0 and M>m0>0 and theta>0
    A=4*K/m0;B=4*K/M
    start=max(math.sqrt(A),theta)
    lo=hi=start
    for _ in range(1024):
        if derivative(lo,A,B,theta)<0: break
        lo/=2
    else: raise ArithmeticError("negative derivative bracket not found")
    for _ in range(1024):
        if derivative(hi,A,B,theta)>0: break
        hi*=2
    else: raise ArithmeticError("positive derivative bracket not found")
    for _ in range(120):
        mid=math.sqrt(lo*hi)
        if derivative(mid,A,B,theta)<0:lo=mid
        else:hi=mid
        if hi/lo-1<2e-14:break
    r=math.sqrt(lo*hi)
    p,s,d=endpoints(r,A,B)
    mu=(p*bose(p,theta)-r*bose(r,theta))/(2*(r*r-p*p))
    lam=-p*bose(p,theta)-2*mu*p*p
    MS=M-m0;k=r*r*m0*MS/M
    masses=np.array([m0,MS])
    H=k*np.array([[1.,-1.],[-1.,1.]])
    im=1/np.sqrt(masses)
    D0=im[:,None]*H*im[None,:]
    Dpi=D0.copy();Dpi[0,0]+=4*K/m0
    al=np.linalg.eigvalsh(D0);be=np.linalg.eigvalsh(Dpi)
    assert np.allclose(al,[0,r*r],rtol=1e-12,atol=1e-12)
    assert np.allclose(be,[p*p,s*s],rtol=1e-12,atol=1e-12)
    assert mu>0>lam
    dual_res=max(abs(x*bose(x,theta)+lam+2*mu*x*x) for x in (p,r,s))
    J=band_integral(0,p,theta)+band_integral(r,s,theta)
    Jr=band_integral(0,math.sqrt(B),theta)
    return dict(inputs=dict(K=K,total_mass=M,backbone_min=m0,theta=theta),
                exact_object="unique positive zero of j'(r) defined in FAMILY_THEOREM.md",
                optical_root=r,root_bracket=[lo,hi],bands=[[0.,p],[r,s]],
                network=dict(backbone_mass=m0,side_mass=MS,
                             intercell_spring=K,internal_spring=k),
                dual=dict(lambda_=lam,mu=mu,three_endpoint_residual=dual_res),
                moments=dict(trace_target=A,trace_actual=p*p+s*s-r*r,
                             log_target=math.log(math.sqrt(B)),
                             log_actual=math.log(p)+math.log(s)-math.log(r)),
                checks=dict(D0_eigenvalues=al.tolist(),Dpi_eigenvalues=be.tolist(),
                            derivative_residual=derivative(r,A,B,theta)),
                conductance=dict(J=J,J_rigid=Jr,ratio=J/Jr,
                                 normalization="G=k_B J/(2pi)",
                                 omitted_tail_start=80*theta))

def synthesize_star(alpha,beta,K):
    """Positive finite star from strict squared endpoint spectra."""
    n=len(alpha);assert len(beta)==n and alpha[0]==0 and K>0
    for j in range(n):
        assert alpha[j]<beta[j]
        if j+1<n:assert beta[j]<alpha[j+1]
    S=Fraction(4)*Fraction(K)
    aa=list(map(Fraction,alpha));bb=list(map(Fraction,beta))
    residues=[]
    for j in range(n):
        num=math.prod(y-aa[j] for y in bb)
        den=S*math.prod(aa[l]-aa[j] for l in range(n) if l!=j)
        residues.append(num/den)
    assert all(c>0 for c in residues)
    m=1/sum(residues);M=1/residues[0]
    def q_minus(sigma):
        return sum(float(c)/(float(a)-sigma) for c,a in zip(residues,aa))
    def qp_minus(sigma):
        return -sum(float(c)/(float(a)-sigma)**2 for c,a in zip(residues,aa))
    sig=[];springs=[];side=[]
    for j in range(1,n):
        lo=float(aa[j-1]);hi=float(aa[j])
        for _ in range(100):
            mid=(lo+hi)/2
            if mid==lo or mid==hi:break
            if q_minus(mid)>0:hi=mid
            else:lo=mid
        sigma=(lo+hi)/2
        rho=-1/(sigma*qp_minus(sigma))
        sig.append(sigma);springs.append(rho);side.append(rho/sigma)
    masses=np.array([float(m)]+side)
    H=np.zeros((n,n))
    for j,k in enumerate(springs,1):
        H[0,0]+=k;H[j,j]+=k;H[0,j]-=k;H[j,0]-=k
    im=1/np.sqrt(masses)
    D0=im[:,None]*H*im[None,:]
    Dpi=D0.copy();Dpi[0,0]+=float(S/m)
    al=np.linalg.eigvalsh(D0);be=np.linalg.eigvalsh(Dpi)
    assert np.allclose(al,list(map(float,aa)),rtol=1e-11,atol=1e-11)
    assert np.allclose(be,list(map(float,bb)),rtol=1e-11,atol=1e-11)
    assert abs(sum(side)-(float(M-m)))<1e-12
    Ab=sum(bb)-sum(aa);E=sum(y*y for y in bb)-sum(x*x for x in aa)
    incident=S*(E-Ab*Ab)/(2*Ab*Ab)
    assert abs(sum(springs)-float(incident))<1e-12
    return dict(squared_endpoints=dict(alpha=alpha,beta=beta),
                K=K,exact_residues=[str(c) for c in residues],
                exact_backbone_mass=str(m),exact_total_mass=str(M),
                branch_squared_frequencies=sig,branch_masses=side,
                branch_springs=springs,exact_incident_stiffness=str(incident),
                D0_eigenvalues=al.tolist(),Dpi_eigenvalues=be.tolist(),
                mass_residual=float(sum(masses)-float(M)))

def main():
    # An unengineered input resource vector demonstrates the universal map.
    opt=design_optimum(K=1.,M=2.,m0=1.,theta=.5)
    (HERE/"universal_design_example.json").write_text(json.dumps(opt,indent=2)+"\n")
    # A genuine THREE-band inverse object, not only the optimum's two bands.
    inv=synthesize_star(alpha=[0,4,16],beta=[1,9,25],K=1)
    (HERE/"three_band_star_example.json").write_text(json.dumps(inv,indent=2)+"\n")
    print("UNIVERSAL DESIGN:",json.dumps(opt,indent=2))
    print("THREE-BAND POSITIVE STAR:",json.dumps(inv,indent=2))
    print("PASS: actual positive networks, full endpoint matrices, moments and spring cost.")

if __name__=="__main__":main()

