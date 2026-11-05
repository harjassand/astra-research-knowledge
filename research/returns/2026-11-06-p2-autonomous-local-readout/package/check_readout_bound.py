"""Finite diagnostics for the autonomous local-readout lower bound.

These checks test matrix identities and inequalities used in the proof.
They are not a fault-tolerant processor simulation or a threshold estimate.
Run: python work/check_readout_bound.py
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import logm
from scipy.stats import poisson

RNG = np.random.default_rng(61135274)


def density(d):
    a = RNG.normal(size=(d, d)) + 1j * RNG.normal(size=(d, d))
    x = a @ a.conj().T + np.eye(d)
    return x / np.trace(x)


def choi(action, d):
    out = np.zeros((d*d, d*d), complex)
    for i in range(d):
        for j in range(d):
            e = np.zeros((d, d), complex)
            e[i, j] = 1
            out += np.kron(e, action(e)) / d
    return (out + out.conj().T) / 2


def partial_trace(rho, dims, keep):
    dims = list(dims)
    out = rho.reshape(dims + dims)
    for i in reversed(range(len(dims))):
        if i not in keep:
            out = np.trace(out, axis1=i, axis2=i+len(dims))
            dims.pop(i)
    d = int(np.prod(dims))
    return out.reshape(d, d)


def entropy(rho):
    p = np.linalg.eigvalsh((rho+rho.conj().T)/2)
    p = p[p > 1e-14]
    return float(-np.dot(p, np.log(p)))


def uniformization_checks():
    cases = []
    for d in [2, 3, 4]:
        for q in [0.01, 0.1, 1.0]:
            for _ in range(6):
                a = RNG.normal(size=(d,d)) + 1j*RNG.normal(size=(d,d))
                h = (a+a.conj().T)/(2*d)
                jumps = [(RNG.normal(size=(d,d))+1j*RNG.normal(size=(d,d)))/(3*d)
                         for _ in range(2)]

                def gen(x):
                    y = -1j*(h@x-x@h)
                    for k in jumps:
                        kk = k.conj().T@k
                        y += k@x@k.conj().T - (kk@x+x@kk)/2
                    return y

                jl = choi(gen, d)
                j = np.linalg.norm(jl, 2)
                rate = 2*(j+q) + 2*d*d*j*j/q

                def phi(x):
                    return x + (gen(x)+q*(np.trace(x)*np.eye(d)/d-x))/rate

                jp = choi(phi, d)
                eig = float(np.linalg.eigvalsh(jp)[0])
                tp = float(np.linalg.norm(partial_trace(jp, [d,d], [0])-np.eye(d)/d))
                x = density(d)
                identity = float(np.linalg.norm(rate*(phi(x)-x)
                                               -(gen(x)+q*(np.eye(d)/d-x))))
                assert eig >= -1e-11 and tp <= 1e-11 and identity <= 1e-10
                cases.append(dict(d=d,q=q,rate=float(rate),min_choi_eigenvalue=eig,
                                  trace_preservation_error=tp,generator_error=identity))
    return cases


def exact_qubit_threshold():
    z = np.diag([1.,-1.])
    cases = []
    for omega in [0.,0.2,1.,3.]:
        for q in [0.03,0.4,1.]:
            h = omega*z/2
            boundary = omega*omega/q + 3*q/4
            values = []
            for factor in [0.99,1.,1.01]:
                rate = factor*boundary
                def phi(x):
                    return x + (-1j*(h@x-x@h)+q*(np.trace(x)*np.eye(2)/2-x))/rate
                values.append(float(np.linalg.eigvalsh(choi(phi, 2))[0]))
            assert values[0] < -1e-8 and abs(values[1]) < 1e-10 and values[2] > 0
            cases.append(dict(omega=omega,q=q,exact_rate=boundary,
                              min_eigenvalues_below_at_above=values))
    return cases


def information_drain_checks():
    # Register order: inaccessible reference R, device B, local port P.
    out = []
    for _ in range(100):
        rho = density(8)
        rb = partial_trace(rho,[2,2,2],[0,1])
        bp = partial_trace(rho,[2,2,2],[1,2])
        b = partial_trace(rho,[2,2,2],[1])
        cmi = entropy(rb)+entropy(bp)-entropy(b)-entropy(rho)
        reset = np.kron(rb,np.eye(2)/2)
        q = float(RNG.uniform(0.01,1.))
        direction = q*(reset-rho)
        # rho_R is constant, so this is the derivative of I(R:BP).
        grad = logm(rho)-np.kron(np.eye(2),logm(bp))
        derivative = float(np.trace(direction@grad).real)
        gap = derivative+q*cmi
        assert cmi >= -1e-10 and gap <= 1e-10
        out.append(dict(cmi_nats=cmi,derivative=derivative,q=q,gap=gap))
    return out


def poisson_smoothing_checks():
    cases = []
    for mu in [0.01,0.1,1.,10.,100.,1000.]:
        k = np.arange(int(poisson.ppf(1-1e-14,mu))+3)
        p = poisson.pmf(k,mu)
        for kind in ['random','threshold','alternating']:
            if kind=='random': f=RNG.random(len(k))
            elif kind=='threshold': f=(k>=np.ceil(mu)).astype(float)
            else: f=(k%2).astype(float)
            # Here Lambda=1, t=mu. Score variance is 1/mu.
            derivative = abs(float(np.dot((k/mu-1)*p,f)))
            bound = .5/np.sqrt(mu)
            assert derivative <= bound+1e-10
            cases.append(dict(t=mu,kind=kind,derivative=derivative,bound=float(bound),
                              mass_deficit=float(1-p.sum())))
    return cases


def bell_witness_check():
    x=np.array([[0,1],[1,0]],complex)
    y=np.array([[0,-1j],[1j,0]],complex)
    z=np.diag([1.,-1.])
    bell=np.array([1,0,0,1],complex)/np.sqrt(2)
    ph=np.outer(bell,bell.conj())
    measured=(3*np.eye(4)+np.kron(x,x)-np.kron(y,y)+np.kron(z,z))/6
    err=float(np.linalg.norm(measured-(np.eye(4)/3+2*ph/3)))
    assert err<1e-12
    # Dimension-free BCY CMI bound in nats: 1/8 times one-way-LOCC norm^2.
    # This measurement gives norm >= (4/3) (F-1/2), hence CMI >= (2/9) gap^2.
    return dict(operator_identity_error=err,cmi_gap_squared_coefficient=2/9,
                integrated_gap_squared_bound_coefficient=float(9*np.log(2)),
                endpoint_rate_constant=float(1/(324*np.log(2)**2)))


def main():
    uniform=uniformization_checks()
    exact=exact_qubit_threshold()
    drain=information_drain_checks()
    smooth=poisson_smoothing_checks()
    witness=bell_witness_check()
    result=dict(
        description=__doc__, seed=61135274,
        summary=dict(uniformization_cases=len(uniform),exact_threshold_cases=len(exact),
                     information_drain_cases=len(drain),smoothing_cases=len(smooth),
                     min_choi_eigenvalue=min(c['min_choi_eigenvalue'] for c in uniform),
                     max_trace_preservation_error=max(c['trace_preservation_error'] for c in uniform),
                     max_generator_error=max(c['generator_error'] for c in uniform),
                     largest_information_drain_gap=max(c['gap'] for c in drain),
                     largest_smoothing_ratio=max(c['derivative']/c['bound'] for c in smooth)),
        bell_witness=witness,uniformization=uniform,exact_qubit_threshold=exact,
        information_drain=drain,poisson_smoothing=smooth)
    target=Path(__file__).with_name('finite_checks.json')
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['summary'],indent=2))
    print('All finite diagnostics passed. No processor or threshold was simulated.')


if __name__=='__main__':
    main()
