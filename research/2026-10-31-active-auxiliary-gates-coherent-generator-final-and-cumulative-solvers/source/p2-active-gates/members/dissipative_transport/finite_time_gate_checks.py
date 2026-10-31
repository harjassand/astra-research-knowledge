"""Finite-source diagnostics for dissipative dark-space transport.

The proofs are in MAIN_THEOREM.txt.  These ordinary NumPy/SciPy calculations
have no interval rounding certificate and are not hardware performance data.
Run from any directory: python /absolute/path/to/finite_time_gate_checks.py
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm


I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1., -1.]).astype(complex)


def ket(n, j):
    v = np.zeros(n, complex)
    v[j] = 1
    return v


def certificate(g, h, kappa, d=0.):
    alpha = min(1., kappa/(2*h+(kappa/2+d)**2/g))
    C = np.sqrt((2+alpha)/(2-alpha))
    lam = alpha*g/(2*(2+alpha))
    return alpha, C, lam


def matrix_gate(T, pieces, kappa=2.):
    """Exact product for real constant-speed pi loop; arbitrary source switches.

    pieces=(duration_fraction, H_E, A, D) use the co-moving frame.  Common H_E
    evolves throughout; neither it nor the quantum gain is inverted physically.
    """
    dE = pieces[0][1].shape[0]
    n = 4  # logical u,v, helper a, decaying e
    ident = np.eye(n*dE, dtype=complex)
    K = ident.copy()
    UE = np.eye(dE, dtype=complex)
    PE = np.outer(ket(n,3),ket(n,3))
    ea = np.outer(ket(n,3),ket(n,2))
    geom = np.zeros((n,n), complex)
    geom[0,2] = -1j*np.pi/T
    geom[2,0] = 1j*np.pi/T
    for frac, HE, A, D in pieces:
        H = (np.kron(np.eye(n),HE) + np.kron(ea,A)
             +np.kron(ea.conj().T,A.conj().T)
             +np.kron(PE,D) +np.kron(geom,np.eye(dE)))
        K = expm((-1j*H-kappa/2*np.kron(PE,np.eye(dE)))*(frac*T))@K
        UE = expm(-1j*HE*(frac*T))@UE
    Rfinal = np.diag([-1.,1.,-1.,1.])
    code = np.kron(np.eye(n)[:,:2],np.eye(dE))
    N = np.kron(Rfinal,np.eye(dE))@K@code
    V = np.kron(np.eye(n)[:,:2]@np.diag([-1.,1.]), UE)
    delta = np.linalg.norm(N-V,2)
    q = max(0.,np.linalg.eigvalsh(np.eye(2*dE)-N.conj().T@N)[-1].real)
    return {"T":T,"no_emission_operator_error":float(delta),
            "maximum_emission_probability":float(q),
            "full_channel_half_diamond_upper":float(min(1.,delta+q/2))}


def mismatch_witness():
    """Individual positive gains need not have a common protected dark plane."""
    # Two lower levels u,a and excited e; source initially maximally mixed.
    # Both gains have eigenvalues 1.4,2.6, but their source dependence differs.
    n=3
    e,u,a=(ket(n,j) for j in (2,0,1))
    eu=np.outer(e,u)
    ea=np.outer(e,a)
    A1=(2*I2+.6*Z)/np.sqrt(2)
    A2=(2*I2-.6*Z)/np.sqrt(2)
    H=(np.kron(np.eye(n),.75*X)+np.kron(eu,A1)+np.kron(eu.T,A1)
       +np.kron(ea,A2)+np.kron(ea.T,A2))
    M=-1j*H-np.kron(np.outer(e,e),I2)  # kappa=2
    D=np.kron(((u-a)/np.sqrt(2))[:,None],I2)
    rows=[]
    for T in (0,2,10,50,200,1000):
        ND=expm(M*T)@D
        rows.append({"T":T,"survival_mixed_source":float(np.trace(ND.conj().T@ND).real/2),
                     "survival_worst_source":float(np.linalg.norm(ND,2)**2)})
    return {"individual_gain_eigenvalues_before_ray_weight":[1.4,2.6],
            "maximum_generator_real_part":float(np.linalg.eigvals(M).real.max()),
            "runs":rows}


def main():
    alpha,C,lam=certificate(1.,3.,2.)
    # Gains are accretive.  The imaginary Hermitian components and source
    # Hamiltonians change abruptly and do not mutually commute.
    pieces=[(.19,200*X,2*I2+.8*Z+.3j*Y,.2*X),
            (.31,73*Y,2*I2+.8*X-.3j*Z,-.2*Z),
            (.17,111*Z,2*I2+.8*Y+.4j*X,.2*Y),
            (.33,37*(X+Z),2*I2+.8*Z-.4j*Y,.1*X)]
    alpha_d,C_d,lam_d=certificate(1.,3.,2.,.2)
    switched=[]
    for T in (30.,100.,300.,1000.,3000.):
        z=matrix_gate(T,pieces)
        bound=min(1.,C_d*(2*np.pi**2+np.pi)/(lam_d*T))
        z["analytic_full_channel_bound"]=float(bound)
        assert z["full_channel_half_diamond_upper"] <= bound+1e-8
        switched.append(z)

    # Exact scalar source benchmark checks the loss-time inequality.  An exact
    # diamond norm is not computed: the theorem's delta+q/2 bound is sufficient.
    scalar=[]
    for T in (30.,100.,300.,1000.):
        z=matrix_gate(T,[(1.,np.zeros((1,1)),np.ones((1,1))*2,np.zeros((1,1)))])
        eps=z['full_channel_half_diamond_upper']
        lower=4*2*(1-eps)**2/(4*eps) if 0<eps<1 else 0.
        z['required_T_from_upper_error_tolerance']=float(lower)
        assert T+1e-8 >= lower
        scalar.append(z)
    result={
        'core_constants':{'g':1.,'h':3.,'kappa':2.,'alpha':alpha,'C':C,'lambda':lam},
        'switched_source_constants':{'d':.2,'alpha':alpha_d,'C':C_d,'lambda':lam_d},
        'switched_source_gate_checks':switched,
        'scalar_loss_time_checks':scalar,
        'different_positive_leg_gains':mismatch_witness(),
        'scope':'Finite matrices; all retained source inputs bounded through operator norms. Not measured device errors or certified rounding.'}
    out=Path(__file__).with_name('finite_time_gate_results.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
