"""Population algebra check for the reciprocal wave counter.

No sampling experiment or finite-data certificate. This independently builds
the normalized drift/noise matrices, compares their characteristic polynomial
and stationary covariance, tests the slow projection, and checks the native
current spectrum including the independent conservative auxiliary bath.
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm


def matrix(k, kap, r, gam, a, tau):
    b = np.exp(1j*k)-1
    ell = abs(b)**2
    g = np.sqrt(kap)
    G = np.array([
        [0,0,0,b/np.sqrt(tau)],
        [0,0,-a*b.conjugate(),g/np.sqrt(tau)],
        [0,a*b,-gam*ell,0],
        [-b.conjugate()/np.sqrt(tau),-g/np.sqrt(tau),0,-r/tau],
    ], dtype=complex)
    Q = np.diag([0,0,2*gam*ell,2*r/tau])
    return b,ell,G,Q


def run():
    results=[]
    polyerr=lyaperr=theterr=projerr=psderr=0.
    max_cov_ratio=0.
    theta=np.diag([1,1,-1,-1])
    for N in [32,128,512]:
        # The projection proof is local in small ell,kappa. A larger finite-N
        # kappa can merge two real poles into a complex pair, where the real-
        # pole Krein projection formula is deliberately not asserted.
        for kap in [.1/np.log(N+1), N**-1.5]:
            for r,gam,a,tau in [(0.8,0.,1.2,.7),(1.7,.4,.9,1.1)]:
                k=2*np.pi/N
                b,ell,G,Q=matrix(k,kap,r,gam,a,tau)
                expected=np.polymul([tau,r,ell],[1,gam*ell,a*a*ell])
                expected[-3]+=kap
                expected[-2]+=kap*gam*ell
                expected=expected/tau
                polyerr=max(polyerr,float(np.max(abs(np.poly(G)-expected))))
                lyaperr=max(lyaperr,float(np.max(abs(G+G.conj().T+Q))))
                theterr=max(theterr,float(np.max(abs(G.conj().T-theta@G@theta))))
                vals,vecs=np.linalg.eig(G)
                idx=np.argmin(abs(vals+ell/r))
                lam=vals[idx]
                assert abs(lam.imag)<1e-10
                h=vecs[:,idx]/vecs[0,idx]
                den=np.vdot(h,theta@h)
                P=np.outer(h,(theta@h).conj())/den
                projerr=max(projerr,float(np.max(abs(G@P-lam*P))),
                            float(np.max(abs(P@P-P))))
                covs=[]
                for t in [0.,1.,.1*N*N,N*N,10*N*N]:
                    C=expm(t*G)[0,0]
                    covs.append(float(abs(C-np.exp(-ell*t/r))))
                ratio=max(covs)/(kap+ell)
                max_cov_ratio=max(max_cov_ratio,ratio)
                for w in [.001,.03,.2,1.,4.]:
                    H=np.linalg.inv(1j*w*np.eye(4)-G)
                    actual=(H@Q@H.conj().T)[3,3].real/tau
                    Z=r+1j*tau*w+ell/(1j*w)+kap*(1j*w+gam*ell)/(a*a*ell-w*w+1j*gam*ell*w)
                    predicted=2*(1/Z).real
                    psderr=max(psderr,abs(actual-predicted))
                    assert actual <= 2/r+1e-10
                results.append({'N':N,'kappa':kap,'r':r,'gamma':gam,
                                'slow_eigenvalue':{'real':float(lam.real),'imag':float(lam.imag)},
                                'native_heat_rate':-ell/r,
                                'max_sampled_covariance_error':max(covs),
                                'error_over_kappa_plus_ell':ratio})

    # Grounded loss is a distinct bath. Its slow rate approaches k^4/(kappa gamma).
    grounded=[]
    for N in [128,512,2048]:
        k=2*np.pi/N; kap=.08; gamma=.3; r=1.1; a=1.; tau=.7
        b,ell,G,Q=matrix(k,kap,r,0.,a,tau)
        G[2,2]=-gamma
        vals=np.linalg.eigvals(G)
        slow=vals[np.argmax(vals.real)]
        predicted=-a*a*ell*ell/(kap*gamma)
        grounded.append({'N':N,'slow_rate':float(slow.real),
                         'k4_asymptotic':predicted,
                         'ratio':float(slow.real/predicted)})

    print(json.dumps({'diagnostic_polynomial':polyerr,'diagnostic_projection':projerr,'diagnostic_spectrum':psderr}))
    assert polyerr<1e-10 and lyaperr<1e-12 and theterr<1e-12
    assert projerr<1e-9 and psderr<1e-9
    out={'status':'passed population matrix/impedance checks',
         'max_characteristic_coefficient_error':polyerr,
         'max_stationarity_identity_error':lyaperr,
         'max_momentum_reversal_error':theterr,
         'max_projection_identity_error':projerr,
         'max_spectrum_identity_error':psderr,
         'max_sampled_covariance_error_ratio':max_cov_ratio,
         'cases':results,'grounded_loss_cases':grounded,
         'scope':'Finite matrices check algebra and failure mechanism; proofs carry all-time and path/LDP statements. No apparatus or acquired confidence budget.'}
    target=Path(__file__).with_name('WAVE_COUNTER_CHECKS.json')
    target.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['cases','grounded_loss_cases']},indent=2))


if __name__=='__main__':
    run()
