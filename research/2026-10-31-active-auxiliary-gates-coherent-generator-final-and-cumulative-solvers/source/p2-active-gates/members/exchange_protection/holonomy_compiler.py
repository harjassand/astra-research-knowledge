"""Ordinary floating-point checks of explicit one- and two-qubit dark loops.

No device claim and no certified numerical integration.  The exact loop formulas
and invariant-subspace identities in HOLONOMY_CONSTRUCTION.txt are the proof.
Run: python exchange_protection/holonomy_compiler.py
"""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp


def ket(n, j):
    x = np.zeros(n, complex)
    x[j] = 1
    return x


def smooth(x):
    return x*x*(3-2*x)


def smooth_derivative(x):
    return 6*x*(1-x)


def loop(s, theta0):
    """C1 meridian-circle-meridian loop, normalized duration 1."""
    if s < 1/3:
        z = 3*s
        return theta0*smooth(z), 0., 3*theta0*smooth_derivative(z), 0.
    if s < 2/3:
        z = 3*s-1
        return theta0, 2*np.pi*smooth(z), 0., 6*np.pi*smooth_derivative(z)
    z = 3*s-2
    return theta0*(1-smooth(z)), 2*np.pi, -3*theta0*smooth_derivative(z), 0.


def bright_and_derivative(s, theta0, u, a):
    theta, phi, dt, dp = loop(s, theta0)
    b = np.sin(theta)*np.exp(1j*phi)*u + np.cos(theta)*a
    db = ((np.cos(theta)*dt + 1j*np.sin(theta)*dp)*np.exp(1j*phi)*u
          -np.sin(theta)*dt*a)
    return b, db


def kato_holonomy(theta0, u, a):
    n = len(u)
    def ode(s, z):
        U = z.reshape(n, n)
        b, db = bright_and_derivative(s, theta0, u, a)
        P = np.eye(n) - np.outer(b, b.conj())
        dP = -np.outer(db, b.conj())-np.outer(b, db.conj())
        return ((dP@P-P@dP)@U).ravel()
    sol = solve_ivp(ode, (0, 1), np.eye(n, dtype=complex).ravel(),
                    method='DOP853', rtol=3e-12, atol=1e-13,
                    max_step=1/400)
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol.y[:, -1].reshape(n, n)


def real_half_turn_holonomy(u, a):
    """Projector closes although its real bright vector changes sign."""
    n = len(u)
    def ode(s, z):
        theta = np.pi*smooth(s)
        dt = np.pi*smooth_derivative(s)
        b = np.sin(theta)*u+np.cos(theta)*a
        db = dt*(np.cos(theta)*u-np.sin(theta)*a)
        P = np.eye(n)-np.outer(b,b.conj())
        dP = -np.outer(db,b.conj())-np.outer(b,db.conj())
        return ((dP@P-P@dP)@z.reshape(n,n)).ravel()
    sol = solve_ivp(ode,(0,1),np.eye(n,dtype=complex).ravel(),
                    method='DOP853',rtol=3e-12,atol=1e-13,max_step=1/400)
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol.y[:,-1].reshape(n,n)


def main():
    # Arbitrary-ray phase; theta0=pi/4 gives phase pi.
    theta0 = np.pi/4
    u = (ket(3, 0)+np.exp(.37j)*ket(3, 1))/np.sqrt(2)
    a = ket(3, 2)
    U = kato_holonomy(theta0, u, a)
    target = np.eye(2, dtype=complex) + (np.exp(1j*np.pi)-1)*np.outer(u[:2],u[:2].conj())
    one_error = np.linalg.norm(U[:2,:2]-target, 2)
    one_leak = np.linalg.norm(U[2:,:2], 2)

    # Pair Hamiltonian is two products of local ladder operators, not an
    # abstract six-state projector supplied by an oracle.
    n = 5  # 0,1,a,e,f at each physical site
    q1 = np.outer(ket(n,3), ket(n,1))
    qa = np.outer(ket(n,3), ket(n,2))
    comp = [np.kron(ket(n,i),ket(n,j)) for i in [0,1] for j in [0,1]]
    pair_u = comp[3]
    pair_a = np.kron(ket(n,2),ket(n,2))
    pair_e = np.kron(ket(n,3),ket(n,3))
    basis = np.column_stack(comp+[pair_a,pair_e])
    spectator_error = 0.
    reduction_error = 0.
    jump_errors = []
    for s in np.linspace(0,1,71):
        theta,phi,_,_ = loop(s,theta0)
        c1 = np.sin(theta)*np.exp(-1j*phi)
        ca = np.cos(theta)
        X = c1*np.kron(q1,q1)+ca*np.kron(qa,qa)
        H = X+X.conj().T
        b = np.sin(theta)*np.exp(1j*phi)*pair_u+np.cos(theta)*pair_a
        H_target = np.outer(pair_e,b.conj())+np.outer(b,pair_e.conj())
        reduction_error = max(reduction_error,np.linalg.norm((H-H_target)@basis,2))
        spectator_error = max(spectator_error,np.linalg.norm(H@basis[:,:3],2))
        d = np.cos(theta)*pair_u-np.sin(theta)*np.exp(-1j*phi)*pair_a
        dark = np.column_stack(comp[:3]+[d])
        LA = np.kron(np.outer(ket(n,4),ket(n,3)),np.eye(n))
        LB = np.kron(np.eye(n),np.outer(ket(n,4),ket(n,3)))
        jump_errors.append(max(np.linalg.norm(LA@dark,2),np.linalg.norm(LB@dark,2)))

    # Geometric transport in the invariant five-ground-state domain.
    up = ket(5,3)
    ap = ket(5,4)
    U2 = kato_holonomy(theta0,up,ap)
    cz = np.diag([1,1,1,-1]).astype(complex)
    pair_error = np.linalg.norm(U2[:4,:4]-cz,2)
    pair_leak = np.linalg.norm(U2[4:,:4],2)
    Ur = real_half_turn_holonomy(up,ap)
    real_error = np.linalg.norm(Ur[:4,:4]-cz,2)
    real_leak = np.linalg.norm(Ur[4:,:4],2)
    results = {
        'loop_phase':float(2*np.pi*np.sin(theta0)**2),
        'one_qubit_phase_operator_error':float(one_error),
        'one_qubit_endpoint_leakage':float(one_leak),
        'pair_product_coupler_reduction_error':float(reduction_error),
        'spectator_coupling_norm':float(spectator_error),
        'dark_jump_norm':float(max(jump_errors)),
        'controlled_z_operator_error':float(pair_error),
        'controlled_z_endpoint_leakage':float(pair_leak),
        'real_half_turn_controlled_z_error':float(real_error),
        'real_half_turn_endpoint_leakage':float(real_leak),
        'real_half_turn_max_speed':float(1.5*np.pi),
        'real_half_turn_squared_speed_integral':float(6*np.pi**2/5),
        'scope':'Algebra and numerical Kato transport; no microscopic hardware validation.'
    }
    for k,v in results.items():
        if k.endswith('error') or k.endswith('leakage') or k.endswith('norm'):
            assert v < 1e-8, (k,v)
    path = Path(__file__).with_name('holonomy_compiler_results.json')
    path.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))


if __name__=='__main__':
    main()
