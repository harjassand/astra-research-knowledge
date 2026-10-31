"""Streaming recovery, source-commutator, cavity, and spectral regularity checks.

The proofs are in STREAMING_RECOVERY_AND_SPECTRAL_BUDGET.txt.  These checks
exercise them, including the full inherited 12-level optical interaction.
They do not certify a built cavity or collection apparatus.
"""
from pathlib import Path
import itertools
import json
import sys
import numpy as np
from scipy.linalg import expm, norm, eig

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "next_recycling_optics"))
from recycling_and_sidebands import operators

I = np.eye(2)
X = np.array([[0, 1], [1, 0]])
Z = np.diag([1, -1])
H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)


def integer_stream_identities():
    """Unnormalized maps give an exact integer proof of the relay relation."""
    eye = np.eye(2, dtype=np.int64)
    z = Z.astype(np.int64)
    hh = np.array([[1, 1], [1, -1]], dtype=np.int64)
    plus = np.array([1, 1], dtype=np.int64)
    load = np.kron(eye, plus[:, None])
    errors = []
    for m, n in itertools.product(range(2), repeat=2):
        odd = np.concatenate([eye, (-1)**m * z], axis=1)
        even = np.concatenate([eye, (-1)**n * z], axis=0)
        errors.append(int(np.max(np.abs(odd @ even - 2*(m == n)*eye))))
        errors.append(int(np.max(np.abs(odd @ load - hh @ np.linalg.matrix_power(z, m)))))
    endpoint_errors = []
    for m, n, q in itertools.product(range(2), repeat=3):
        even = np.concatenate([eye, (-1)**n*z], axis=0)
        read = np.kron(eye, np.array([[1, (-1)**q]], dtype=np.int64))
        got = read @ even @ hh @ np.linalg.matrix_power(z, m)
        want = 2*(-1)**(m*q)*np.linalg.matrix_power(z, m+n) @ np.linalg.matrix_power(X, q)
        endpoint_errors.append(int(np.max(np.abs(got-want))))
    return {"exact_integer_relay_and_first_transfer_max_error": max(errors),
            "exact_integer_even_endpoint_max_error": max(endpoint_errors)}


def full_model_stream():
    """Every record up to six informative photons, changing quantum source."""
    h0, v, jumps = operators(20., 22., 1.)
    y = np.array([[0, -1j], [1j, 0]])
    gains = [I+.17*X+.11j*Z, I-.13*Z+.09j*X, I+.07*y-.12j*Z]
    sources = [.37*X+2.41*Z, -1.73*X+.22*y, 71.1*Z+.19*X]
    q = sum(j.conj().T@j for j in jumps)
    j_e = [np.kron(j, I) for j in jumps]
    propagators = []
    for t, a, he in zip([.27, .41, .33], gains, sources):
        h = np.kron(h0, I)+np.kron(v, a)+np.kron(v.conj().T, a.conj().T)+np.kron(np.eye(12), he)
        propagators.append(expm((-1j*h-np.kron(q,I)/2)*t))
    # Full order: optical(12), source(2), receiver memory(2).
    jm = [(np.kron(j_e[0], I)+(-1)**m*np.kron(j_e[1], Z))/np.sqrt(2) for m in range(2)]
    jz = np.kron(j_e[2], I)
    segments = [np.kron(p, I) for p in propagators]
    load = np.zeros((48, 4), complex)
    for j, e, a in itertools.product(range(2), repeat=3):
        load[4*j+2*e+a, 2*j+e] = 1/np.sqrt(2)
    extract_odd = np.zeros((4,48), complex)
    for a,e in itertools.product(range(2), repeat=2):
        extract_odd[2*a+e, 4*2+2*e+a] = 1
    endpoint_errors=[]; forbidden=[]; allowed=[]
    for n in range(1,7):
        for record in itertools.product(range(2), repeat=n):
            k=load.copy()
            for j,m in enumerate(record):
                # Retain a z recycling jump before selected x/y emissions.
                k=segments[j%3]@k
                if j in (1,4):
                    k=segments[(j+1)%3]@jz@k
                k=jm[m]@k
            allowed_record=all(record[j] == record[j-1] for j in range(2,n,2))
            if not allowed_record:
                forbidden.append(float(norm(k)))
                continue
            allowed.append(float(norm(k)))
            if n%2:
                correction=np.linalg.matrix_power(Z,sum(record)%2)@H
                kk=np.kron(correction,I)@extract_odd@k
                common=kk[:2,:2]
                endpoint_errors.append(float(norm(kk-np.kron(I,common))/max(norm(kk),1e-300)))
            else:
                for bit in range(2):
                    extract=np.zeros((4,48),complex)
                    for j,e,a in itertools.product(range(2), repeat=3):
                        extract[2*j+e,4*j+2*e+a]=(-1)**(bit*a)/np.sqrt(2)
                    correction=np.linalg.matrix_power(X,bit)@np.linalg.matrix_power(Z,sum(record)%2)
                    kk=np.kron(correction,I)@extract@k
                    common=kk[:2,:2]
                    endpoint_errors.append(float(norm(kk-np.kron(I,common))/max(norm(kk),1e-300)))
    return {"max_relative_corrected_endpoint_factorization_error":max(endpoint_errors),
            "max_forbidden_record_operator_norm":max(forbidden),
            "minimum_allowed_history_operator_norm":min(allowed),
            "checked_photon_counts":[1,2,3,4,5,6],
            "checked_all_records_count":sum(2**n for n in range(1,7))}


def global_parity_mode_mixing():
    """Arbitrary unitaries in the commutant may mix time-order labels.

    This is more general than a passive polarization-blind optical circuit.
    It tests the algebraic assertion, not a proposed optical implementation.
    """
    rng=np.random.default_rng(61732)
    errors=[]; covariance=[]; anticommutation=[]
    for n in range(1,7):
        dim=2**n
        px=X.copy(); pz=Z.copy(); xbasis=H.copy()
        for _ in range(n-1):
            px=np.kron(px,X); pz=np.kron(pz,Z); xbasis=np.kron(xbasis,H)
        anticommutation.append(float(norm(px@pz-(-1)**n*pz@px)))
        raw=rng.normal(size=(dim,dim))+1j*rng.normal(size=(dim,dim))
        raw=(raw+raw.conj().T)/(2*np.sqrt(dim))
        commuting=(raw+px@raw@px+pz@raw@pz+px@pz@raw@pz@px)/4
        u=expm(1j*commuting)
        covariance.append(max(float(norm(u@px-px@u)),float(norm(u@pz-pz@u))))
        if n%2:
            # V maps input to first photon, then adjacent Bell pairs.
            v=np.zeros((dim,2),complex)
            for j in range(2):
                for paired in itertools.product(range(2),repeat=(n-1)//2):
                    bits=[j]
                    for b in paired: bits.extend([b,b])
                    index=sum(b*2**(n-1-k) for k,b in enumerate(bits))
                    v[index,j]=2**(-(n-1)/4)
            v=u@v
            for r in range(dim):
                bra=xbasis[r,:]
                kk=np.stack([bra@v,bra@pz@v],axis=0)/np.sqrt(2)
                s=r.bit_count()%2
                kk=np.linalg.matrix_power(Z,s)@H@kk
                errors.append(float(norm(kk-np.trace(kk)*I/2)))
        else:
            # Output order is emitter L, then the n photons.
            v=np.zeros((2,dim,2),complex)
            for j in range(2):
                for paired in itertools.product(range(2),repeat=n//2):
                    bits=[j]
                    for b in paired[:-1]: bits.extend([b,b])
                    bits.append(paired[-1])
                    index=sum(b*2**(n-1-k) for k,b in enumerate(bits))
                    v[paired[-1],index,j]=2**(-n/4)
            v=np.einsum('ab,lbj->laj',u,v)
            for r,q in itertools.product(range(dim),range(2)):
                bra=xbasis[r,:]@(np.eye(dim)+(-1)**q*pz)/2
                kk=np.einsum('a,laj->lj',bra,v)
                s=r.bit_count()%2
                kk=np.linalg.matrix_power(X,q)@np.linalg.matrix_power(Z,s)@kk
                errors.append(float(norm(kk-np.trace(kk)*I/2)))
    return {"global_parity_relation_error":max(anticommutation),
            "random_mode_commutant_covariance_error":max(covariance),
            "corrected_fine_operator_max_absolute_error":max(errors),
            "checked_photon_counts":[1,2,3,4,5,6]}


def commutator_budget():
    h0,v,jumps=operators(20.,22.,1.)
    gamma=1.; a=1.3; d=np.sqrt(22**2+gamma**2/4)
    gain=I+.17*X+.11j*Z
    q=np.kron(sum(j.conj().T@j for j in jumps),I)
    je=[np.kron(j,I) for j in jumps]
    values=[]; reference=None
    for omega in [0.,1.,1e3,1e6]:
        h=np.kron(h0,I)+np.kron(v,gain)+np.kron(v.conj().T,gain.conj().T)+np.kron(np.eye(12),omega*Z+.7*X)
        gen=-1j*h-q/2
        cs=[j@gen-gen@j for j in je]
        s=sum(c.conj().T@c for c in cs)
        if reference is None: reference=cs
        values.append({"source_frequency":omega,
                       "stacked_commutator_norm_squared":float(np.linalg.eigvalsh(s)[-1]),
                       "difference_from_zero_source_frequency":max(float(norm(c-r)) for c,r in zip(cs,reference))})
    return {"uniform_bound":float(gamma*(d+np.sqrt(3)*a)**2),
            "source_speed_checks":values,
            "all_two_jump_products_zero":max(float(norm(j@k)) for j in jumps for k in jumps)}


def cavity_checks():
    examples=[]
    for kap,gam,g,band in [(1.,.1,5.,.005),(1.,.1,10.,.0001),(10.,.1,10.,.01)]:
        w=np.linspace(-band,band,20001)
        aa=kap/2; bb=gam/2
        den=(aa-1j*w)*(bb-1j*w)+g*g
        r0=1-kap/(aa-1j*w)
        r1=1-kap*(bb-1j*w)/den
        loss=kap*gam*g*g/np.abs(den)**2
        dmin=g*g+aa*bb-band*band
        zeta=2*band/np.sqrt(aa*aa+band*band)+kap*np.sqrt(bb*bb+band*band)/dmin
        loss_bound=kap*gam*g*g/(dmin*dmin)
        examples.append({"kappa":kap,"gamma":gam,"g":g,"band":band,
                         "cooperativity":4*g*g/(kap*gam),
                         "observed_max_reflection_error":float(np.max(np.abs(r1+r0))),
                         "uniform_reflection_error_bound":float(zeta),
                         "observed_max_loss":float(np.max(loss)),
                         "uniform_loss_bound":float(loss_bound),
                         "optical_theorem_residual":float(np.max(np.abs(np.abs(r1)**2+loss-1)))})
    return examples


def one_photon_spectral_check():
    """Absorbing optical source: exact whole Fock state has 0 or 1 photon.

    Source speed is changed by 500x, while [L,H_source] remains zero.
    This tests the full-field frequency/derivative identity independently
    of the decoder algebra.  FFT is a numerical check, not the proof.
    """
    gamma=1.; delta=3.; duration=4.; total_time=64.
    count=2**18; dt=total_time/count
    ts=np.arange(count)*dt
    gain=.6*(I+.2*X+.1j*np.array([[0,-1j],[1j,0]]))
    source0=np.array([1.,1j])/np.sqrt(2)
    initial=np.concatenate([source0,np.zeros(2)])
    pe=np.diag([0,0,1,1])
    output=[]
    for omega in [0.,50.,500.]:
        he=omega*Z/2
        ham=np.block([[he,gain.conj().T],[gain,he+delta*I]])
        gen=-1j*ham-gamma*pe/2
        vals,vecs=eig(gen); coeff=np.linalg.solve(vecs,initial)
        mask=ts<=duration; tt=ts[mask]
        states=vecs@(coeff[:,None]*np.exp(vals[:,None]*tt))
        derivatives=gen@states
        phases=np.exp(1j*np.diag(he)[:,None]*tt)
        f=np.zeros((2,count),complex); df=np.zeros_like(f)
        f[:,mask]=np.sqrt(gamma)*phases*states[2:]
        df[:,mask]=np.sqrt(gamma)*phases*(derivatives[2:]+1j*he@states[2:])
        end=expm(gen*duration)@initial
        ft=np.sqrt(gamma)*np.exp(1j*np.diag(he)*duration)*end[2:]
        tail_t=ts[~mask]-duration
        f[:,~mask]=ft[:,None]*np.exp((-gamma/2-1j*delta)*tail_t)
        df[:,~mask]=(-gamma/2-1j*delta)*f[:,~mask]
        fs=np.fft.fft(f,axis=1)*dt/np.sqrt(2*np.pi)
        ws=2*np.pi*np.fft.fftfreq(count,d=dt); dw=2*np.pi/total_time
        spectrum=np.sum(np.abs(fs)**2,axis=0)
        m2=float(np.sum(ws**2*spectrum)*dw)
        derivative=float(np.sum(np.abs(df)**2)*dt)
        prob=float(np.sum(np.abs(f)**2)*dt)
        tail_band=20.
        tail=float(np.sum(spectrum[np.abs(ws)>tail_band])*dw)
        output.append({"source_splitting":omega,
                       "emission_probability":prob,
                       "spectral_second_moment_fft":m2,
                       "temporal_derivative_norm_squared":derivative,
                       "relative_parseval_error":abs(m2-derivative)/derivative,
                       "photon_weight_outside_band_20":tail,
                       "moment_tail_bound_at_band_20":m2/tail_band**2})
    return output


def main():
    data={"integer_circuit":integer_stream_identities(),
          "full_optical_model":full_model_stream(),
          "global_parity_mode_mixing":global_parity_mode_mixing(),
          "source_uniform_commutator_budget":commutator_budget(),
          "cavity_band_and_loss":cavity_checks(),
          "spectral_regularization_check":one_photon_spectral_check()}
    target=ROOT/"streaming_decoder_results.json"
    target.write_text(json.dumps(data,indent=2)+"\n")
    print(json.dumps(data,indent=2))

if __name__=="__main__": main()
