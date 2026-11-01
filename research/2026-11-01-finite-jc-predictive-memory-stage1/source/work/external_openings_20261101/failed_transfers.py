"""Exact finite optical countercontrol and a smooth-system transfer obstruction.

The optimal j=2 bath saturates its output eigenvalue cap but preserves a
resolved quantum branch. Replacing the thermal relevance channel invalidates
the Gaussian classical converse. The actual finite comparisons are recorded,
including cases that do not establish a classical win.
"""
from __future__ import annotations
import hashlib,json,math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/external_openings_20261101'

def entropy(r):
    e=np.linalg.eigvalsh((r+r.conj().T)/2);e=e[e>1e-15]
    return float(-np.sum(e*np.log(e)))
def g(x):return (1+x)*math.log1p(x)-x*math.log(x) if x else 0.
def reductions(r,db,dm):
    t=r.reshape(db,dm,db,dm)
    return np.einsum('bmcm->bc',t),np.einsum('bmbn->mn',t)
def mi(r,db,dm):
    b,m=reductions(r,db,dm)
    return entropy(b)+entropy(m)-entropy(r)
def noise_kraus(da):
    # The input never has total photon number above da. The output basis
    # has da+1 states per port, so these columns have no cutoff error.
    d=da+1;a=np.diag(np.sqrt(np.arange(1,d)),1).astype(complex)
    gen=np.kron(a,a.conj().T)-np.kron(a.conj().T,a)
    u=expm(math.pi/4*gen).reshape(d,d,d,d)
    return [u[:,e,:da,1] for e in range(d)]
def channel(r,kk):return sum(k@r@k.conj().T for k in kk)
def main():
    da=12;db=da+1;kk=noise_kraus(da)
    assert np.linalg.norm(sum(k.conj().T@k for k in kk)-np.eye(da),2)<1e-13
    # Determine the common phase of the isometric branch from the real
    # beamsplitter convention, rather than assuming a harmless sign.
    cross=np.zeros((da,da));cross[0,1]=1
    phase=channel(cross,kk)[1,2]/.5
    v=np.zeros((db,2),complex);v[1,0]=1;v[2,1]=phase.conjugate()
    residual=0.
    for i in range(2):
        for j in range(2):
            x=np.zeros((da,da));x[i,j]=1
            want=.5*v@x[:2,:2]@v.conj().T
            if i==j:want[0,0]+=.5
            residual=max(residual,float(np.linalg.norm(channel(x,kk)-want,2)))
    assert residual<1e-13
    bell=np.zeros((da,2),complex);bell[0,0]=bell[1,1]=1/math.sqrt(2)
    rr=np.outer(bell.ravel(),bell.ravel().conj())
    choi=sum(np.kron(k,np.eye(2))@rr@np.kron(k.conj().T,np.eye(2)) for k in kk)
    bout,mout=reductions(choi,db,2)
    pt=choi.reshape(db,2,db,2).transpose(0,3,2,1).reshape(db*2,db*2)
    negativity=float(-np.linalg.eigvalsh(pt)[np.linalg.eigvalsh(pt)<-1e-14].sum())
    product_norm=float(np.abs(np.linalg.eigvalsh(choi-np.kron(bout,mout))).sum())
    assert abs(negativity-.25)<1e-13 and abs(product_norm-.75)<1e-13
    rows=[];ret=.2
    for n in (.01,.003,.001,.0003,.0001):
        pn=(n/(1+n))**np.arange(da)/(1+n)
        # Retain optical |0>,|1> coherently; reset the higher tail to |0>.
        aq=np.zeros((da*2,da*2),complex)
        for m,p in enumerate(pn):
            one=m*ret*(1-ret)**(m-1) if m else 0.
            aq[2*m,2*m]=p*(1-one);aq[2*m+1,2*m+1]=p*one
        for m in range(da-1):
            z=math.sqrt(pn[m]*pn[m+1]*(m+1)*ret)*(1-ret)**m
            aq[2*m,2*(m+1)+1]=z;aq[2*(m+1)+1,2*m]=z
        bq=sum(np.kron(k,np.eye(2))@aq@np.kron(k.conj().T,np.eye(2)) for k in kk)
        quantum=mi(bq,db,2)
        # Legal classical output: original purifier photon number reduced
        # to the one-bit predicate N>0. A predetermined fraction q of
        # pairs is stored; the schedule is public, not a retained flag.
        bl=np.zeros((db*2,db*2),complex)
        for m,p in enumerate(pn):
            e=np.zeros((da,da));e[m,m]=p
            block=channel(e,kk);index=int(m>0)
            bl[index::2,index::2]+=block
        cfull=mi(bl,db,2)
        budget=g(n)+g(ret*n)-g((1-ret)*n)
        fraction=budget/g(n)
        classical=fraction*cfull
        rows.append({'n':n,'quantum_reset_encoder_relevance':quantum,
                     'legal_classical_predetermined_timeshare_relevance':classical,
                     'source_information_upper':budget,'predetermined_store_fraction':fraction,
                     'input_fock_tail_probability':float((n/(1+n))**da),
                     'quantum_minus_this_classical_encoder':quantum-classical,
                     'scope':'finite controlled diagnostic; this single classical encoder is not a non-Gaussian classical frontier'})
    # At the exact binary-source/erasure interface the quantum and a
    # legal classical timeshare have IDENTICAL relevance at actual cost.
    binary=[]
    def h(x):return -x*math.log(x)-(1-x)*math.log1p(-x)
    for p in (.01,.1,.3):
        cost=h(p)+h(ret*p)-h((1-ret)*p)
        q=cost/h(p)
        quantum=.5*cost;classical=q*.5*h(p)
        assert 0<q<1 and abs(quantum-classical)<1e-15
        binary.append({'source_excitation_probability':p,'actual_source_information':cost,
                       'quantum_relevance':quantum,'classical_timeshare_relevance':classical,
                       'classical_predetermined_store_fraction':q})
    # For any T adaptive black-box probes, averaging a width-2w smooth
    # unit-height bump over an interval of length J gives some centre
    # with total hit probability <=2*T*w/J. Until a first hit the probe
    # law is the zero-response law. Probe energies can all be <=1.
    bump=[{'queries':t,'bump_half_width':1e-9,'centre_interval_length':1.,
           'some_centre_total_hit_probability_upper':2*t*1e-9} for t in (100,1000,10000)]
    result={'status':'PASS finite full-channel controls; smooth-bump argument is analytic',
            'optimal_noise_bath':'one photon at eta=1/2, output cap c=1/2',
            'nonGaussian_bath_photons':1.,'optimal_Gaussian_bath_photons':2.,
            'resolved_erasure_channel_residual':residual,'reference_Choi_negativity':negativity,
            'reference_trace_norm_from_product':product_norm,
            'reference_half_trace_distance_from_product':product_norm/2,
            'nonGaussian_thermal_source_comparisons':rows,
            'exact_binary_source_erasure_classical_ties':binary,'smooth_bump_controls':bump,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'failed_transfers.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
