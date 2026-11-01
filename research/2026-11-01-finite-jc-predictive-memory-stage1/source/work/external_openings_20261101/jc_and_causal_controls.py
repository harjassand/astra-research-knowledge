"""Full quantum JC write/read and a causal passive mode accumulator.

Finite matrices verify the head-channel identity, actual pair/reference
state and complete higher-photon charge. They do not qualify a physical
mode selector or an experimental loss/noise value.
"""
from __future__ import annotations
import hashlib,json,math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/external_openings_20261101'

def annihilator(d):return np.diag(np.sqrt(np.arange(1,d)),1).astype(complex)
def thermal(mean,d):return (mean/(1+mean))**np.arange(d)/(1+mean)
def gauss_pair(s,y,c,db,dm):
    denom=(s+1)*(y+1)-c*c
    p=1-(y+1)/denom;q=1-(s+1)/denom;v=c/denom
    assert p>=0 and q>=-1e-14
    a=annihilator(db);b=annihilator(dm)
    create=v*np.kron(a.conj().T,b.conj().T)
    rr=np.eye(db*dm,dtype=complex);term=rr.copy()
    for j in range(1,min(db,dm)):term=term@create/j;rr+=term
    diag=np.kron(p**np.arange(db),max(0.,q)**np.arange(dm))/denom
    rho=(rr*diag[None,:])@rr.conj().T
    assert np.linalg.eigvalsh((rho+rho.conj().T)/2)[0]>-1e-12
    return rho
def write_kraus(d,angle):
    a=annihilator(d);sm=np.array([[0,1],[0,0]],complex)
    h=np.kron(a,sm.conj().T)+np.kron(a.conj().T,sm)
    u=expm(-1j*angle*h).reshape(d,2,d,2)
    phase=np.diag([1.,1j]) # remove the known swap phase
    return [phase@u[e,:,:,0] for e in range(d)]
def amp_kraus(eta):
    return [np.diag([1.,np.sqrt(eta)]).astype(complex),np.array([[0,np.sqrt(1-eta)],[0,0]],complex)]
def apply_memory(rho,db,dm,kk):
    arr=rho.reshape(db,dm,db,dm);out=np.zeros((db,2,db,2),complex)
    for k in kk:out+=np.einsum('ac,icjd,bd->iajb',k,arr,k.conj(),optimize=True)
    return out.reshape(db*2,db*2)
def norm1(a):return float(np.abs(np.linalg.eigvalsh((a+a.conj().T)/2)).sum())

def main():
    dm=8;db=40;angle=.47*np.pi;eta=.9
    eta_w=math.sin(angle)**2;post=eta/eta_w
    kk=[j@k for k in write_kraus(dm,angle) for j in amp_kraus(post)]
    completeness=np.linalg.norm(sum(k.conj().T@k for k in kk)-np.eye(dm),2)
    assert completeness<1e-13
    # Exact reference-stable head identity, not only population transfer.
    err=0.
    for i in range(2):
        for j in range(2):
            e=np.zeros((dm,dm),complex);e[i,j]=1
            actual=sum(k@e@k.conj().T for k in kk)
            two=e[:2,:2];wanted=sum(k@two@k.conj().T for k in amp_kraus(eta))
            err=max(err,float(np.linalg.norm(actual-wanted,2)))
    assert err<1e-13
    n=.02;loss=.2;s=.5*n+.5;y=loss*n;c=math.sqrt(.5*loss*n*(1+n))
    full=gauss_pair(s,y,c,db,dm)
    actual=apply_memory(full,db,dm,kk)
    virtual=gauss_pair(s,eta*y,math.sqrt(eta)*c,db,dm)
    embedded=np.zeros_like(virtual)
    ix=[b*dm+m for b in range(db) for m in range(2)]
    embedded[np.ix_(ix,ix)]=actual
    distance=norm1(embedded-virtual)
    pc=(y/(1+y))**2
    truncation=(s/(1+s))**db+(y/(1+y))**dm
    assert distance<=4*math.sqrt(pc)+1e-10
    assert 1-np.trace(full).real<=truncation+1e-13
    # Under H1 only the physical JC qubit mean is needed, without a
    # block-length multiplier on the higher-photon probability.
    sourcep=thermal(y,dm);pe=float(sum(sourcep[j]*post*math.sin(angle*math.sqrt(j))**2 for j in range(dm)))
    pe_upper=eta*y/(1+y)**2+pc
    assert pe<=pe_upper+1e-13
    # Independently check the heterodyne-conditioning formula on the
    # full Gaussian state, including its optical coherences.
    vals=[];aa=annihilator(dm)
    for z in (.3+.2j,1.-.7j):
        cv=np.empty(db,complex);cv[0]=np.exp(-abs(z)**2/2)
        for j in range(1,db):cv[j]=cv[j-1]*z/math.sqrt(j)
        cond=np.einsum('b,bmcn,c->mn',cv.conj(),full.reshape(db,dm,db,dm),cv,optimize=True)
        probability=float(np.trace(cond).real);cond/=probability
        expected=c*z.conjugate()/(1+s)
        residual=abs(np.trace(aa@cond)-expected)
        vals.append(float(residual));assert residual<1e-10
    # Exact finite beamsplitter network: one row update per observation.
    rng=np.random.default_rng(202611012);ell=32
    zs=rng.normal(size=ell)+1j*rng.normal(size=ell)
    u=np.eye(ell+1,dtype=complex);running=0.
    for i,z in enumerate(zs):
        total=running+abs(z)**2
        co=math.sqrt(running/total);si=abs(z)/math.sqrt(total);phase=z/abs(z)
        old=u[0].copy();incoming=u[i+1].copy()
        u[0]=co*old+si*phase*incoming
        u[i+1]=-si*phase.conjugate()*old+co*incoming
        running=total
    target=np.r_[0.,zs/np.linalg.norm(zs)]
    mode_error=float(np.max(np.abs(u[0]-target)))
    unitary_error=float(np.linalg.norm(u.conj().T@u-np.eye(ell+1),2))
    assert mode_error<1e-13 and unitary_error<1e-13
    # Loss of a shared accumulator is cumulative. This exposes the
    # missing hardware condition instead of treating it as an ideal wire.
    ell=32768;zs=rng.normal(size=ell)+1j*rng.normal(size=ell);weights=abs(zs)**2;weights/=weights.sum()
    loss_rows=[]
    age=np.arange(ell,0,-1)
    for loss_step in (0.,1e-6,3e-6,1e-5,1e-4,.001):
        decay=(1-loss_step)**(age/2)
        transmission=float(np.sum(weights*decay**2))
        gain=float(np.sum(weights*decay)**2)
        loss_rows.append({'loss_per_step':loss_step,'effective_transmission':transmission,
                          'squared_mode_alignment':gain/transmission,'coherent_signal_gain':gain})
    result={'scope':'finite quantum algebra and exact passive network, no device measurement',
            'JC_write_angle':angle,'head_chain_transmission':eta,'JC_channel_completeness_residual':completeness,
            'reference_stable_head_channel_residual':err,'full_pair_actual_vs_virtual_trace_norm':distance,
            'full_pair_analytic_trace_norm_upper':4*math.sqrt(pc),'numerical_pair_truncation_mass_upper':truncation,
            'actual_JC_false_hypothesis_qubit_population':pe,'qubit_population_upper':pe_upper,
            'heterodyne_mean_residuals':vals,'causal_mode_row_error':mode_error,'passive_network_unitarity_residual':unitary_error,
            'causal_32768_mode_bus_loss_controls':loss_rows,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'jc_and_causal_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
