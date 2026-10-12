"""Finite numerical falsification checks; not a proof of the uniform theorem.
Run: python finite_checks.py --output finite_checks.json
Requires Python 3.10+, numpy.  Independent of the previous Astra check script.
"""
from __future__ import annotations
import argparse
import itertools
import json
from functools import lru_cache
from pathlib import Path
import numpy as np

PAULI = {
    'I': np.eye(2, dtype=complex),
    'X': np.array([[0, 1], [1, 0]], dtype=complex),
    'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
    'Z': np.diag([1., -1.]).astype(complex),
}

def kron_all(matrices: list[np.ndarray]) -> np.ndarray:
    out = np.ones((1, 1), dtype=complex)
    for matrix in matrices:
        out = np.kron(out, matrix)
    return out

@lru_cache(maxsize=512)
def pauli(label: str) -> np.ndarray:
    return kron_all([PAULI[c] for c in label])

def supported(n: int, data: dict[int, str]) -> str:
    return ''.join(data.get(i, 'I') for i in range(n))

@lru_cache(maxsize=20)
def measurement(n: int, visibility: float):
    if not 0 < visibility <= 1:
        raise ValueError('Visibility must lie in (0,1].')
    options = list(itertools.product('XYZ', (-1, 1)))
    records = list(itertools.product(options, repeat=n))
    effects = np.array([kron_all([(PAULI['I']+visibility*s*PAULI[b])/6
                                 for b, s in row]) for row in records])
    assert np.allclose(effects.sum(axis=0), np.eye(2**n), atol=1e-12)
    return records, effects

def gram(operators: np.ndarray, weight: np.ndarray) -> np.ndarray:
    value = np.einsum('aij,bij,ij->ab', operators.conj(), operators, weight).real
    return (value+value.T)/2

def minimum(matrix: np.ndarray) -> float:
    return float(np.linalg.eigvalsh((matrix+matrix.T)/2).min())

def check_instance(n: int, labels: list[str], hterms: dict[str, float],
                   beta: float, visibility: float, case: str) -> dict:
    P = np.array([pauli(a) for a in labels])
    m, d = len(labels), 2**n
    H = sum((v*pauli(a) for a, v in hterms.items()), np.zeros((d,d), complex))
    E, U = np.linalg.eigh(H)
    logs = -beta*(E-E.min())
    logs -= np.log(np.exp(logs).sum())
    p = np.exp(logs)
    rho = (U*p) @ U.conj().T
    mu = np.einsum('ij,aji->a', rho, P).real
    Pc = P-mu[:,None,None]*np.eye(d)[None,:,:]
    Pe = np.array([U.conj().T @ a @ U for a in Pc])
    delta = logs[:,None]-logs[None,:]
    close = np.abs(delta) < 1e-6
    L = np.empty((d,d))
    np.divide(p[:,None]-p[None,:], delta, out=L, where=~close)
    L[close] = (np.exp((logs[:,None]+logs[None,:])/2)
                  *(1+delta**2/24+delta**4/1920))[close]
    arith = (p[:,None]+p[None,:])/2
    C = gram(Pe,L)
    Vq = gram(Pe,arith)
    Q = beta**2*gram(Pe,L**2/arith)
    W = gram(Pe,(p[:,None]-p[None,:])*(E[None,:]-E[:,None]))
    derivatives = np.array([U @ (-beta*L*a) @ U.conj().T for a in Pe])
    records, effects = measurement(n,visibility)
    probabilities = np.einsum('oij,ji->o', effects, rho).real
    if probabilities.min() <= 0:
        raise ArithmeticError('Numerical loss of positive outcome probabilities.')
    dq = np.einsum('oij,aji->oa', effects, derivatives).real
    Fisher = (dq.T/probabilities) @ dq
    Y = np.zeros((len(records),m))
    for o,row in enumerate(records):
        for a,label in enumerate(labels):
            value=1.
            for i,c in enumerate(label):
                if c=='I':
                    continue
                basis, sign=row[i]
                if basis!=c:
                    value=0.
                    break
                value *= 3*sign/visibility
            Y[o,a]=value
    means = probabilities @ Y
    V = (Y.T*probabilities) @ Y-np.outer(means,means)
    R = (V-C+V.T-C.T)/2
    N = (V-Vq+V.T-Vq.T)/2
    response_error = float(np.max(np.abs(Y.T @ dq+beta*C)))
    exact_lower = beta**2*C @ np.linalg.solve(V,C)
    k = max(sum(c!='I' for c in a) for a in labels)
    incidence=max(sum(a[i]!='I' for a in labels) for i in range(n))
    ell=max((sum(c!='I' for c in a) for a in hterms), default=1)
    g=max(sum(abs(v) for a,v in hterms.items() if a[i]!='I') for i in range(n))
    noise_bound=(1+k*(incidence-1))*((3/visibility**2)**k-1)
    commutator_bound=4*g*k*(k+ell)*incidence
    nu=noise_bound+beta*commutator_bound/12
    eye=np.eye(m)
    gaps={
      'C_positive': minimum(C),
      'readout_noise_positive': minimum(N),
      'readout_noise_upper': minimum(noise_bound*eye-N),
      'quantum_variance_positive': minimum(Vq-C),
      'harris_upper': minimum(beta*W/12-(Vq-C)),
      'double_commutator_positive': minimum(W),
      'double_commutator_upper': minimum(commutator_bound*eye-W),
      'moment_information_bound': minimum(Fisher-exact_lower),
      'measurement_below_SLD': minimum(Q-Fisher),
      'SLD_below_BKM': minimum(beta**2*C-Q),
      'state_dependent_additive_loss': minimum(beta**2*R-(beta**2*C-Fisher)),
      'uniform_additive_loss': minimum(beta**2*nu*eye-(Q-Fisher)),
    }
    scale=max(1.,float(np.linalg.norm(V,2)),float(np.linalg.norm(beta**2*C,2)))
    tolerance=2e-9*scale
    passed = min(gaps.values()) >= -tolerance and response_error<=tolerance
    return {'case':case,'n':n,'m':m,'beta':beta,'visibility':visibility,
            'k':k,'ell':ell,'Delta':incidence,'g':g,'nu':nu,
            'minimum_LMI_eigenvalues':gaps,'response_identity_error':response_error,
            'minimum_probability':float(probabilities.min()),
            'tolerance':tolerance,'passed':bool(passed)}

def main(output: Path) -> None:
    rng=np.random.default_rng(20261012)
    rows=[]
    for n in (2,3,4):
        labels=[supported(n,{i:c}) for i in range(n) for c in 'XYZ']
        labels += [supported(n,{i:'Z',i+1:'Z'}) for i in range(n-1)]
        for trial in range(2):
            hterms={a:float(rng.uniform(-.5,.5)) for a in labels}
            # Add background terms absent from the parameter dictionary.
            for i in range(n):
                for j in range(i+1,n):
                    hterms[supported(n,{i:'X',j:'Y'})]=float(rng.uniform(-.3,.3)/n)
            raw_g=max(sum(abs(v) for a,v in hterms.items() if a[i]!='I') for i in range(n))
            hterms={a:v/raw_g for a,v in hterms.items()}
            for beta in (.2,1.,4.):
                for visibility in (1.,.6):
                    rows.append(check_instance(n,labels,hterms,beta,visibility,
                                               f'random-background-{n}-{trial}'))
    # Analytic sharpness check at the maximally mixed state.
    for visibility in (1.,.6):
        labels=[supported(3,{i:'Z'}) for i in range(3)]
        rows.append(check_instance(3,labels,{},1.,visibility,'maximally-mixed'))
    x=1.; beta=1.
    f=np.tanh(beta*x)/x
    fp=(beta*x/(np.cosh(beta*x)**2)-np.tanh(beta*x))/x**2
    nonconvex={'x':x,'beta':beta,'single_Z_plus_NLL_hessian':[[0.,float(fp)],[float(fp),float(f*f)]],
               'determinant':float(-fp*fp)}
    result={'status':'Finite floating-point falsification checks, not theorem validation',
            'seed':20261012,'number_of_instances':len(rows),
            'all_declared_checks_passed':all(row['passed'] for row in rows),
            'minimum_recorded_LMI_eigenvalue':min(min(row['minimum_LMI_eigenvalues'].values()) for row in rows),
            'maximum_response_identity_error':max(row['response_identity_error'] for row in rows),
            'nonconvex_likelihood_example':nonconvex,'instances':rows}
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='instances'},indent=2))
    if not result['all_declared_checks_passed']:
        raise SystemExit('At least one declared numerical check failed.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('finite_checks.json'))
    args=parser.parse_args()
    main(args.output)
