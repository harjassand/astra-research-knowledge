"""Independent checks of reference-joint compression and a physical learned Petz map.
No SDP, unknown-channel adjoint, hardware, or large-N Schur implementation is used.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parent


def partial_output(C,k,d):
    return np.einsum('aibi->ab',C.reshape(k,d,k,d))
def choi(Ks,k):
    return sum(np.outer(K.T.reshape(-1),K.T.reshape(-1).conj()) for K in Ks)/k
def kraus_from_choi_sqrt(C,k,d):
    # A matrix-square-root column decomposition, independently of the
    # author's eigenvector Kraus decomposition.
    lam,v=np.linalg.eigh(C)
    assert lam.min()>0
    Q=(v*np.sqrt(lam))@v.conj().T
    return [np.sqrt(k)*Q[:,j].reshape(k,d).T for j in range(k*d)]
def petz(Ks,k):
    S=sum(K@K.conj().T for K in Ks)/k
    lam,v=np.linalg.eigh(S)
    inverse=(v*(1/np.sqrt(lam)))@v.conj().T
    return [K.conj().T@inverse/np.sqrt(k) for K in Ks],S
def fe(Rs,Ks,k):
    return sum(abs(np.trace(R@K))**2 for R in Rs for K in Ks)/k**2
def trace_norm(X):
    return float(np.sum(np.abs(np.linalg.eigvalsh((X+X.conj().T)/2))))


def exact_repairs_and_fallback():
    k,d=2,4;h=k*d;a=sp.Rational(1,100);I=sp.eye(h)
    def marg(C):
        return sp.Matrix(k,k,lambda i,j:sum(C[i*d+t,j*d+t] for t in range(d)))
    def repair(A):
        B=A-sp.kronecker_product(marg(A)-sp.eye(k)/k,sp.eye(d)/d)
        C=(B+2*a*I)/(1+2*h*a)
        return B,C
    threshold=a/(2*(1+2*h*a))
    def exact_psd(M):
        # All principal minors: exponential but tiny h=8 diagnostic only.
        for size in range(1,h+1):
            for ind in combinations(range(h),size):
                if M.extract(ind,ind).det()<0:return False
        return True
    def exact_pd(M):
        return all(M[:j,:j].det()>0 for j in range(1,h+1))
    # Exact pure-junk encoder J, with an actual zero junk eigenvalue.
    v=sp.zeros(h,1);v[0]=1;v[6]=1;J=v*v.T/2
    B,C=repair(J)
    assert marg(C)==sp.eye(k)/k and sp.trace(C)==1
    assert exact_psd(C-threshold*I)
    assert exact_pd(C-threshold*I)
    assert exact_psd(C-a/(1+2*h*a)*I)
    good_min=min(C.eigenvals())
    # A valid range-respecting raw diagonal estimate passes STRICTLY above
    # the weaker threshold but below the incorrectly claimed stronger floor.
    tau0=sp.Rational(3,2)*k*threshold
    tau=sp.diag(tau0,*([(1-tau0)/(d-1)]*(d-1)))
    Cweak=sp.kronecker_product(sp.eye(k)/k,tau)
    Aweak=(1+2*h*a)*Cweak
    assert all(0<=Aweak[i,i]<=1 for i in range(h))
    _,got=repair(Aweak)
    assert got==Cweak and exact_pd(got-threshold*I)
    Sweak=sp.Matrix(d,d,lambda i,j:sum(got[t*d+i,t*d+j] for t in range(k)))
    assert min(Sweak.eigenvals())==3*k*a/(4*(1+2*h*a))
    assert min(Sweak.eigenvals())>k*a/(2*(1+2*h*a))
    assert min(Sweak.eigenvals())<k*a/(1+2*h*a)
    # The finite schedule explicitly rejects equality at its acceptance
    # threshold, although that equality would still define a physical map.
    edge=sp.kronecker_product(sp.eye(k)/k,sp.diag(k*threshold,*([(1-k*threshold)/(d-1)]*(d-1))))
    assert exact_psd(edge-threshold*I) and not exact_pd(edge-threshold*I)
    # A bad but range-respecting raw count estimate must fall back physically.
    Abad=sp.zeros(h);Abad[0,0]=1
    _,Cbad=repair(Abad)
    assert not exact_pd(Cbad-threshold*I)
    fallback=sp.eye(h)/h
    assert marg(fallback)==sp.eye(k)/k
    assert exact_pd(fallback-threshold*I)
    return {'dimension_h':h,'all_principal_minor_certification':True,
            'good_exact_min_C':str(good_min),'weak_accepted_min_S':str(min(Sweak.eigenvals())),
            'correct_uniform_min_S':str(k*a/(2*(1+2*h*a))),
            'original_stronger_min_S_is_not_uniform':True,
            'strict_threshold_boundary_rejected':True,
            'bad_raw_count_fixture_selects_CPTP_fallback':True}


def physical_petz_tests():
    rng=np.random.default_rng(112709)
    rows=[]
    for k,r in [(2,1),(2,2),(2,3),(3,2),(3,3)]:
        d=k*r;h=k*d
        spectra=[np.ones(r)/r]
        if r>1:
            spectra += [np.r_[0.,np.ones(r-1)/(r-1)],np.r_[1e-18,(1-1e-18)*np.ones(r-1)/(r-1)]]
        for spectrum in spectra:
            Z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));U=np.linalg.qr(Z)[0]
            true=[np.sqrt(spectrum[j])*U[:,[i*r+j for i in range(k)]] for j in range(r)]
            J=choi(true,k)
            correct=[U[:,[i*r+j for i in range(k)]].conj().T for j in range(r)]
            assert abs(fe(correct,true,k)-1)<2e-14
            for e in [1e-5,1e-7]:
                # Coordinatewise confidence-good perturbation, not a fitted
                # perturbation of the already-repaired channel.
                E=np.zeros((h,h),complex)
                for i in range(h):
                    E[i,i]=e*rng.uniform(-1,1)
                    for j in range(i+1,h):
                        E[i,j]=e*(rng.uniform(-1,1)+1j*rng.uniform(-1,1));E[j,i]=E[i,j].conj()
                A=J+E
                B=A-np.kron(partial_output(A,k,d)-np.eye(k)/k,np.eye(d)/d)
                a=4*h*e
                assert np.linalg.norm(B-J,2)<=a+1e-12
                C=(B+2*a*np.eye(h))/(1+2*h*a)
                assert np.linalg.norm(partial_output(C,k,d)-np.eye(k)/k)<1e-13
                assert np.linalg.eigvalsh(C).min()>=a/(1+2*h*a)-1e-13
                assert trace_norm(C-J)<=5*h*a+1e-12
                learned=kraus_from_choi_sqrt(C,k,d)
                recover,S=petz(learned,k)
                TP=sum(R.conj().T@R for R in recover)
                residual=float(np.linalg.norm(TP-np.eye(d),2))
                assert residual<1e-8
                assert np.linalg.eigvalsh(S).min()>=k*a/(1+2*h*a)-1e-12
                competitor=fe(correct,learned,k)
                model=fe(recover,learned,k)
                actual=fe(recover,true,k)
                assert model+1e-10>=competitor**2
                delta=min(1,k*trace_norm(C-J)/2)
                assert competitor>=1-delta-1e-10
                assert actual>=1-3*delta-1e-9
                assert abs(actual-model)<=delta+1e-9
                decoded=choi([R@K for R in recover for K in true],k)
                phi=np.eye(k).reshape(-1)/np.sqrt(k);target=np.outer(phi,phi)
                choi_distance=trace_norm(decoded-target)/2
                assert choi_distance<=np.sqrt(max(0,1-actual))+1e-9
                # Direct actual unknown input/reference experiment.
                z=rng.normal(size=k*k)+1j*rng.normal(size=k*k);z/=np.linalg.norm(z)
                rho=np.outer(z,z.conj())
                output=sum(np.kron(np.eye(k),R@K)@rho@np.kron(np.eye(k),R@K).conj().T for R in recover for K in true)
                ref_distance=trace_norm(output-rho)/2
                assert ref_distance<=k*np.sqrt(3*delta)+1e-9
                rows.append({'k':k,'r':r,'junk_spectrum':spectrum.tolist(),'coordinate_radius':e,
                             'decoder_TP_operator_residual':residual,'competitor_model_Fe':competitor,
                             'Petz_model_Fe':model,'Petz_actual_Fe':actual,'model_halfdiamond_upper':delta,
                             'actual_Choi_distance':choi_distance,'random_reference_input_distance':ref_distance})
    return {'seed':112709,'physical_decoder_cases':len(rows),'zero_and_1e_minus_18_junk_eigenvalues_included':True,
            'kraus_method':'Columns of positive matrix square root, not author eigenvector Kraus decomposition','rows':rows}


def swap(d):
    P=np.zeros((d*d,d*d))
    for i in range(d):
        for j in range(d):P[j*d+i,i*d+j]=1
    return P
def two_copy_schur_channel(X,D,d,refdim):
    out=np.zeros((d*d*refdim,d*d*refdim),complex)
    for sign in [1,-1]:
        big=(np.eye(D*D)+sign*swap(D))/2
        small=(np.eye(d*d)+sign*swap(d))/2
        T=np.einsum('ba,arbs->rs',big,X.reshape(D*D,refdim,D*D,refdim))
        out+=np.kron(small/np.trace(small),T)
    return out
def cliffords():
    H=np.array([[1,1],[1,-1]],complex)/np.sqrt(2);S=np.diag([1,1j])
    def norm(U):
        pivot=next(z for z in U.reshape(-1) if abs(z)>1e-8)
        return U*np.exp(-1j*np.angle(pivot))
    def key(U):return tuple(np.round(np.r_[U.real.reshape(-1),U.imag.reshape(-1)],10))
    out={key(np.eye(2)):np.eye(2,dtype=complex)};queue=list(out.values())
    while queue:
        U=queue.pop()
        for G in [H,S]:
            V=norm(G@U);q=key(V)
            if q not in out:out[q]=V;queue.append(V)
    assert len(out)==24
    return list(out.values())


def joint_compression_tests():
    rng=np.random.default_rng(119184)
    refdim=4;d=2;D=3
    raw=rng.normal(size=(D,d))+1j*rng.normal(size=(D,d));V=np.linalg.qr(raw)[0]
    z=rng.normal(size=d*d*refdim)+1j*rng.normal(size=d*d*refdim);z/=np.linalg.norm(z)
    X=np.outer(z,z.conj())
    E=np.kron(np.kron(V,V),np.eye(refdim))
    compressed=two_copy_schur_channel(E@X@E.conj().T,D,d,refdim)
    group=cliffords()
    averaged=np.zeros_like(X)
    for U in group:
        W=np.kron(np.kron(U,U),np.eye(refdim));averaged+=W@X@W.conj().T/len(group)
    residual=float(np.max(np.abs(compressed-averaged)))
    assert residual<1e-13
    rho_ref=np.einsum('aras->rs',X.reshape(d*d,refdim,d*d,refdim))
    independently_twirl=np.kron(np.eye(d*d)/(d*d),rho_ref)
    gap=trace_norm(compressed-independently_twirl)/2
    assert gap>1e-3
    # Mixed junk, same joint reference identity, checked directly at n=2.
    k=r=2;d=4;D=5;weights=[.013,.987]
    Omega=np.zeros((d*d*4,d*d*4),complex)
    for a in range(r):
        for b in range(r):
            z=np.zeros(d*d*4,complex)
            for i in range(k):
                for j in range(k):z[((i*r+a)*d+(j*r+b))*4+(i*k+j)]=1/k
            Omega+=weights[a]*weights[b]*np.outer(z,z.conj())
    raw=rng.normal(size=(D,d))+1j*rng.normal(size=(D,d));V=np.linalg.qr(raw)[0]
    E=np.kron(np.kron(V,V),np.eye(4))
    left=two_copy_schur_channel(E@Omega@E.conj().T,D,d,4)
    right=two_copy_schur_channel(Omega,d,d,4)
    mixed_residual=float(np.max(np.abs(left-right)))
    assert mixed_residual<1e-13
    # One training Choi plus an entangled payload; retain the SAME U.
    phi4=np.eye(4).reshape(-1)/2;Omega=np.outer(phi4,phi4)
    joint=np.zeros_like(Omega,dtype=complex);posterior=np.zeros((4,4),complex);p=0.
    phi2=np.eye(2).reshape(-1)/np.sqrt(2);bell=np.outer(phi2,phi2)
    for U in group:
        W=np.kron(np.kron(U,U),np.eye(4));joint+=W@Omega@W.conj().T/len(group)
        likelihood=abs(np.trace(U)/2)**2
        q=np.kron(U,np.eye(2))@phi2
        posterior+=likelihood*np.outer(q,q.conj())/len(group);p+=likelihood/len(group)
    # Order output_train,output_payload,ref_train,ref_payload -> train pair,payload pair.
    reordered=joint.reshape([2]*8).transpose(0,2,1,3,4,6,5,7).reshape(4,4,4,4)
    measured=np.einsum('ba,arbs->rs',bell,reordered)
    posterior_residual=float(np.max(np.abs(measured-posterior)))
    assert posterior_residual<1e-13 and abs(p-.25)<1e-13
    conditional_fe=float(np.trace(bell@measured).real/p)
    assert abs(conditional_fe-.5)<1e-13
    return {'seed':119184,'external_reference_dimension':4,'exact_two_copy_Clifford_design_size':24,
            'D3_to_d2_reference_joint_residual':residual,'independent_compression_trace_distance_counterexample':gap,
            'D5_to_d4_mixed_junk_reference_joint_residual':mixed_residual,
            'posterior_latent_U_measurement_residual':posterior_residual,
            'training_Bell_event_probability':p,'conditional_payload_entanglement_fidelity':conditional_fe,
            'independent_frame_payload_entanglement_fidelity':.25}


def schedule_identities():
    k,h,delta=sp.symbols('k h delta',positive=True)
    e=delta/(10*k*h*h);a=4*h*e
    assert sp.simplify(1/(2*e*e)-50*k*k*h**4/delta**2)==0
    inverse_squared=sp.factor(2*(1+2*h*a)/(k*a))
    assert sp.simplify(inverse_squared-(5*h/delta+4*h/k))==0
    finite=[]
    for kk,rr,epsilon in [(2,1,F(1,10)),(2,2,F(1,100)),(3,2,F(1,20))]:
        dd=kk*rr;hh=kk*dd;delv=epsilon**2/(12*kk*kk);beta=epsilon/4;ee=delv/(10*kk*hh*hh)
        L=0
        while F(2**L)<2*hh*hh/beta:L+=1
        raw=F(L)/(2*ee*ee);m=-(-raw.numerator//raw.denominator)
        assert 2*m*ee*ee>=L and F(2*hh*hh,2**L)<=beta
        finite.append({'k':kk,'r':rr,'epsilon':str(epsilon),'L':L,'m_per_setting':m,'training_queries':hh*hh*m})
    return {'Hoeffding_m_coefficient':'50*k^2*h^4/delta^2',
            'uniform_accepted_inverse_S_sqrt_norm_squared_upper':str(inverse_squared),
            'simplified':'5*h/delta+4*d, where h=k*d',
            'required_fidelity_range':'0<=delta<=1, or replace(1-delta)^2 by max(0,1-delta)^2',
            'exact_log_free_integer_schedule_cases':finite}


def main():
    result={'exact_repairs':exact_repairs_and_fallback(),'physical_Petz':physical_petz_tests(),
            'reference_joint_compression':joint_compression_tests(),'schedule_identities':schedule_identities(),
            'scope':'Independent exact small-matrix certification and finite compressed-model/reference tests. Not a large-N Schur run, physical experiment, SDP, or unknown-adjoint oracle.'}
    (ROOT/'INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
