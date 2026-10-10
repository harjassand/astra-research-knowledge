import numpy as np, json, math

def gibbs(V):
    n=V.shape[0]//2
    Om=np.block([[np.zeros((n,n)),np.eye(n)],[-np.eye(n),np.zeros((n,n))]])
    vals,vecs=np.linalg.eig(2*V@(1j*Om))
    if np.max(np.abs(vals.imag))>1e-7 or np.min(np.abs(vals.real))<=1+1e-9:
        return None
    z=0.5*np.log((vals+1)/(vals-1))
    G=2j*Om@(vecs@np.diag(z)@np.linalg.inv(vecs))
    if np.max(np.abs(G.imag))>1e-5: return None
    return (G.real+G.real.T)/2

def gap(eta,u,w,rr,sa=1.0,sr=1.0,nu=1.0):
    sh=math.sinh(rr);ch=math.cosh(rr)
    r=u*ch*ch+w*sh*sh;a=w*ch*ch+u*sh*sh;c=(u+w)*sh*ch
    v=nu+.5;ce=math.sqrt(nu*(nu+1));se=math.sqrt(eta);sl=math.sqrt(1-eta)
    # q,p ordering grouped by quadrature. Local squeezing on R and A.
    Qb=np.array([[r*sr*sr,se*c*sr*sa],[se*c*sr*sa,eta*a*sa*sa+(1-eta)*v]])
    Pb=np.array([[r/sr/sr,-se*c/sr/sa],[-se*c/sr/sa,eta*a/sa/sa+(1-eta)*v]])
    Qe=np.array([[r*sr*sr,-sl*c*sr*sa,0],[-sl*c*sr*sa,(1-eta)*a*sa*sa+eta*v,se*ce],[0,se*ce,v]])
    Pe=np.array([[r/sr/sr,sl*c/sr/sa,0],[sl*c/sr/sa,(1-eta)*a/sa/sa+eta*v,-se*ce],[0,-se*ce,v]])
    Gb=gibbs(np.block([[Qb,np.zeros((2,2))],[np.zeros((2,2)),Pb]]))
    Ge=gibbs(np.block([[Qe,np.zeros((3,3))],[np.zeros((3,3)),Pe]]))
    if Gb is None or Ge is None:return None
    # Compare means displaced solely at input A; reference mean unchanged.
    Tb=np.diag([1.0, math.sqrt(eta)])
    Te=np.array([[1.0,0.0],[0.0,-math.sqrt(1-eta)],[0.0,0.0]])
    Dq=Te.T@Ge[:3,:3]@Te-Tb.T@Gb[:2,:2]@Tb
    Dp=Te.T@Ge[3:,3:]@Te-Tb.T@Gb[2:,2:]@Tb
    return min(np.linalg.eigvalsh(Dq)[0],np.linalg.eigvalsh(Dp)[0])

if __name__=='__main__':
    rng=np.random.default_rng(20261010)
    out={'status':'floating-point diagnostics only; no inequality proof','tests':[]}
    for eta in [.749,.75,.7501,.751,.755,.76,.77,.78,.7841,.79,.8]:
        best=(float('inf'),None);valid=0
        for i in range(3200):
            u=.5+10**rng.uniform(-2.5,2.5)
            w=.5+10**rng.uniform(-2.5,2.5)
            rr=rng.uniform(0,2.5)
            sa=10**rng.uniform(-1,1)
            sr=1.0
            gg=gap(eta,u,w,rr,sa,sr)
            if gg is None:continue
            valid+=1
            if gg<best[0]:best=(gg,[u,w,rr,sa,sr])
        row={'eta':eta,'valid':valid,'smallest_gap_E_minus_B':best[0],'parameters_u_w_r_sa_sr':best[1]}
        print(json.dumps(row),flush=True);out['tests'].append(row)
    with open('work/continuation_03/reports/e4_zero_support/gaussian_reference_full_mean_probe.json','w') as f:json.dump(out,f,indent=2)
