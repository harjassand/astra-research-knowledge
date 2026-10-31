"""Complete LS=1x1 optical closure, with a 3-level ground triplet.

Algebra is exact up to floating point. Optional full finite-source Lindblad
diagnostics use the 12 internal states (3 ground, all 9 excited) and retain
every Cartesian dipole emission. No excited hyperfine/fine sector is omitted.
These are dimensionless model checks, not an atomic device qualification.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm, norm

ROOT=Path(__file__).resolve().parent

def optical_operators():
    i3=np.eye(3); i9=np.eye(9)
    swap=np.zeros((9,9))
    for i in range(3):
        for j in range(3): swap[3*j+i,3*i+j]=1
    sing=np.eye(3).reshape(9)/np.sqrt(3)
    p0=np.outer(sing,sing)
    p1=(i9-swap)/2
    p2=(i9+swap)/2-p0
    dips=[np.kron(np.eye(3)[:,j:j+1],i3) for j in range(3)]
    return (p0,p1,p2),dips

def algebra_checks():
    ps,ds=optical_operators(); p0,p1,p2=ps
    rng=np.random.default_rng(41)
    out={"projector_completeness":float(norm(sum(ps)-np.eye(9)))}
    for label,e in [("real",np.array([.3,.4,np.sqrt(.75)])),
                    ("complex",rng.normal(size=3)+1j*rng.normal(size=3))]:
        e=e/norm(e); d=sum(e[j]*ds[j] for j in range(3))
        b=e.conj(); bp=np.outer(b,b.conj()); ep=np.outer(e,e.conj())
        p=np.eye(3)-bp
        expected=[bp/3,(np.eye(3)-ep)/2,(np.eye(3)+ep)/2-bp/3]
        errs=[float(norm(d.conj().T@pj@d-ej)) for pj,ej in zip(ps,expected)]
        r1=1/(20-.5j); r2=1/(22-.5j)
        jumps=[dl.conj().T@(r1*p1+r2*p2)@d@p for dl in ds]
        if label=="real":
            a=(r1+r2)/2; z=(r2-r1)/2
            formula=[a*e[j]*p+z*np.outer(e,np.eye(3)[j])@p for j in range(3)]
            badsum=sum(p@j.conj().T@bp@j@p for j in jumps)
            scalar_block=[p@j@p for j in jumps]
            errors={"fine_jump_formula":max(float(norm(j-f)) for j,f in zip(jumps,formula)),
                    "bad_jump_effect":float(norm(badsum-abs(z)**2*p)),
                    "scalar_survival":max(float(norm(j-a*e[k]*p)) for k,j in enumerate(scalar_block))}
        else: errors={}
        equalj=[dl.conj().T@(r1*(p1+p2))@d@p for dl in ds]
        equalerr=max(float(norm(j-r1*e[k]*p)) for k,j in enumerate(equalj))
        out[label]={"strength_identity_errors":errs,"equal_resolvent_fine_scalar":equalerr,**errors}
    d1=29.616955018e9*2*np.pi; d2=31.90813098e9*2*np.pi
    gamma=1/(98e-9)
    r1=1/(-d1-1j*gamma/2);r2=1/(-d2-1j*gamma/2)
    out["helium_ratios"]={"Gamma":gamma,"Delta1":-d1,"Delta2":-d2,
          "Gamma_over_smallest_Delta":gamma/min(d1,d2),
          "differential_to_sum_resolvent":abs((r2-r1)/(r2+r1)),
          "bad_fraction_effective":abs(r2-r1)**2/(abs(r2-r1)**2+abs(r2+r1)**2)}
    return out

def moving_subsystem_geometry_checks():
    """Connection and transverse derivative of the exact static LS subsystem."""
    theta=.73;phi=.29;td=.6;pd=-.42
    e=np.array([np.sin(theta)*np.cos(phi),np.sin(theta)*np.sin(phi),np.cos(theta)])
    dt=np.array([np.cos(theta)*np.cos(phi),np.cos(theta)*np.sin(phi),-np.sin(theta)])
    dp=np.array([-np.sin(phi),np.cos(phi),0.])
    d=np.column_stack([dt,dp])
    ed=td*dt+pd*np.sin(theta)*dp
    dd=np.column_stack([-td*e+pd*np.cos(theta)*dp,
                        -pd*np.sin(theta)*e-pd*np.cos(theta)*dt])
    j=np.zeros((12,4));jd=np.zeros_like(j)
    j[:3,:2]=d;j[3:,2:]=np.kron(e[:,None],d)
    jd[:3,:2]=dd;jd[3:,2:]=np.kron(ed[:,None],d)+np.kron(e[:,None],dd)
    k=d.T@dd;q=d.T@ed;a2=ed@ed
    expected_connection=np.kron(np.eye(2),k)
    trans=(np.eye(12)-j@j.T)@jd
    expected_trans=np.zeros((4,4));expected_trans[:2,:2]=np.outer(q,q)
    expected_trans[2:,2:]=a2*np.eye(2)+np.outer(q,q)
    # Exact full H and every physical jump factor on the static subsystem.
    ps,ds=optical_operators();delta=20.
    op=sum(e[l]*ds[l] for l in range(3))
    hf=np.zeros((12,12),complex);hf[3:,3:]=delta*(ps[1]+ps[2])
    hf[3:,:3]=np.sqrt(3)*op;hf[:3,3:]=np.sqrt(3)*op.conj().T
    ha=np.array([[0.,np.sqrt(3)],[np.sqrt(3),delta]])
    htarget=np.kron(ha,np.eye(2)) # auxiliary-first ordering
    jump_errors=[]
    for l,dl in enumerate(ds):
        lf=np.zeros((12,12));lf[:3,3:]=dl.T
        la=np.array([[0.,e[l]],[0.,0.]])
        jump_errors.append(float(norm(lf@j-j@np.kron(la,np.eye(2)))))
    return {"isometry_error":float(norm(j.T@j-np.eye(4))),
            "connection_factorization_error":float(norm(j.T@jd-expected_connection)),
            "transverse_gram_error":float(norm(trans.T@trans-expected_trans)),
            "transverse_norm":float(norm(trans,2)),
            "predicted_transverse_norm":float(np.sqrt(2*a2)),
            "full_H_factorization_error":float(norm(hf@j-j@htarget)),
            "full_fine_jump_factorization_errors":jump_errors}

def full_model(T=200.,delta1=20.,delta2=22.,omega=3.,eta=.25,g=1.,gamma=1.,settle=12.):
    """One real pi rotation, with a maximally mixed active TLS gain source.

    In the co-rotating frame the Liouvillian is constant. Rotation is around
    Cartesian y. Tracing the source gives the logical Choi-state trace error.
    This is a state/channel diagnostic, not a diamond-norm certificate.
    """
    ps,ds=optical_operators(); p0,p1,p2=ps
    x=np.array([[0,1],[1,0]],complex);z=np.diag([1.,-1.]);i2=np.eye(2)
    gain=g*(i2+eta*z);he=.5*omega*x
    # Cartesian spin-1 generator for R_y(theta): x'=cos(theta)x+sin(theta)z.
    jy=np.array([[0,0,1j],[0,0,0],[-1j,0,0]],complex)
    jtot=np.zeros((12,12),complex);jtot[:3,:3]=jy
    jtot[3:,3:]=np.kron(jy,np.eye(3))+np.kron(np.eye(3),jy)
    hbase=np.zeros((12,12),complex);hbase[3:,3:]=delta1*p1+delta2*p2
    # epsilon=z: resonant e0 matrix element is g, requiring dipole sqrt(3)g.
    vb=np.zeros((12,12),complex);vb[3:,:3]=np.sqrt(3)*ds[2]
    h=np.kron(hbase-(np.pi/T)*jtot,i2)+np.kron(np.eye(12),he)+np.kron(vb+vb.conj().T,gain)
    jumps=[]
    for dl in ds:
        l=np.zeros((12,12),complex);l[:3,3:]=np.sqrt(gamma)*dl.conj().T
        jumps.append(np.kron(l,i2))
    n=h.shape[0];ii=np.eye(n)
    # For column-major vectorization.
    liou=-1j*(np.kron(ii,h)-np.kron(h.T,ii))
    for l in jumps:
        ll=l.conj().T@l
        liou+=np.kron(l.conj(),l)-.5*np.kron(ii,ll)-.5*np.kron(ll.T,ii)
    # Four blocks of a maximally entangled logical/reference state.
    vecs=[]
    for a in range(2):
        for b in range(2):
            op=np.zeros((12,12),complex);op[a,b]=.5
            rho=np.kron(op,i2/2)
            vecs.append(rho.reshape(-1,order='F'))
    ini=np.column_stack(vecs)
    # Add expected emission-count integral to generator; linear function of rho.
    pe=np.zeros((12,12));pe[3:,3:]=np.eye(9)
    m=np.kron(gamma*pe,i2)
    aug=np.zeros((n*n+1,n*n+1),complex);aug[:-1,:-1]=liou
    aug[-1,:-1]=m.T.reshape(-1,order='F')
    ai=np.vstack([ini,np.zeros((1,4))])
    result=expm(T*aug)@ai
    before_settle=result.copy()
    if settle:
        hoff=np.kron(hbase,i2)+np.kron(np.eye(12),he)
        loff=-1j*(np.kron(ii,hoff)-np.kron(hoff.T,ii))
        for l in jumps:
            ll=l.conj().T@l
            loff+=np.kron(l.conj(),l)-.5*np.kron(ii,ll)-.5*np.kron(ll.T,ii)
        aoff=np.zeros_like(aug);aoff[:-1,:-1]=loff
        aoff[-1,:-1]=m.T.reshape(-1,order='F')
        result=expm(settle*aoff)@result
    output=np.zeros((24,24),complex)
    for a in range(2):
        for b in range(2):
            rho=result[:-1,a*2+b].reshape((n,n),order='F')
            red=np.einsum('aibi->ab',rho.reshape(12,2,12,2))
            output[a::2,b::2]=red
    # Compare in rotating frame, where target gate is the identity.
    bell=np.zeros(24,complex);bell[0]=1/np.sqrt(2);bell[3]=1/np.sqrt(2)
    target=np.outer(bell,bell.conj())
    ev=np.linalg.eigvalsh((output-target+output.conj().T-target)/2)
    error=.5*np.sum(abs(ev))
    photons=float(np.real(result[-1,0]+result[-1,3]))
    return {"T":T,"drive_off_settle":settle,"total_duration":T+settle,
            "delta1":delta1,"delta2":delta2,"omega":omega,"eta":eta,
            "logical_choi_trace_error":float(error),"mean_all_emissions":photons,
            "trace":float(np.trace(output).real),
            "minimum_eigenvalue":float(np.linalg.eigvalsh((output+output.conj().T)/2)[0])}

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--full',action='store_true')
    ar=ap.parse_args();out=algebra_checks()
    out['moving_subsystem_geometry']=moving_subsystem_geometry_checks()
    if ar.full:
        out['full_model']=[full_model(T=t) for t in (100.,200.,400.)]
        out['full_model_equal_complement']=[full_model(T=200.,delta1=20.,delta2=20.)]
        out['full_model_large_split']=[full_model(T=200.,delta1=20.,delta2=40.)]
    path=ROOT/'atomic_closure_results.json';path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
