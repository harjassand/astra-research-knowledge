"""Small numerical fixtures for the exact expander-history proof.

Uses the already installed NumPy.  The source proof, not these floating-point
fixtures, supplies the spectral theorem and the all-dimension conclusion.
"""

from itertools import product
from math import log2
import numpy as np


def margulis_unitaries(d):
    assert d >= 3 and d % 2 == 1
    omega = np.exp(2j*np.pi/d)
    j = np.arange(d)
    fourier = omega**np.outer(j, j) / np.sqrt(d)
    upper_shear = np.diag(omega**(-j*j))
    lower_shear = fourier @ upper_shear.conj().T @ fourier.conj().T
    phase = np.diag(omega**j)
    shift_minus = np.zeros((d,d), dtype=complex)
    for k in range(d):
        shift_minus[(k-1) % d, k] = 1
    base = [upper_shear, phase @ upper_shear,
            lower_shear, shift_minus @ lower_shear]
    return base + [u.conj().T for u in base]


def channel(x, unitaries):
    return sum((u @ x @ u.conj().T for u in unitaries),
               np.zeros_like(x)) / len(unitaries)


def choi_power(d, n, unitaries):
    tau = np.zeros((d*d, d*d), dtype=complex)
    for i in range(d):
        for k in range(d):
            x = np.zeros((d,d), dtype=complex)
            x[i,k] = 1
            for _ in range(n):
                x = channel(x, unitaries)
            tau[i*d:(i+1)*d, k*d:(k+1)*d] = x/d
    return (tau+tau.conj().T)/2


def entropy(x):
    vals = np.linalg.eigvalsh((x+x.conj().T)/2)
    assert vals.min() >= -2e-11
    vals = vals[vals > 1e-12]
    return float(-np.dot(vals, np.log2(vals)))


def output_gram(d, n, unitaries):
    words = []
    for word in product(range(8), repeat=n):
        u = np.eye(d, dtype=complex)
        for letter in word:
            u = unitaries[letter] @ u
        words.append(u)
    return np.array([[np.trace(u @ v.conj().T)/(d*8**n)
                      for v in words] for u in words])


def fixtures():
    lam = 5*np.sqrt(2)/8
    for d in (3,5,7):
        us = margulis_unitaries(d)
        unitarity = max(np.linalg.norm(u.conj().T@u-np.eye(d)) for u in us)
        superop = sum(np.kron(u.conj(),u) for u in us)/8
        ident = np.eye(d).reshape(-1, order='F')/np.sqrt(d)
        proj = np.eye(d*d)-np.outer(ident,ident.conj())
        actual = float(np.max(np.abs(np.linalg.eigvalsh(proj@superop@proj))))
        assert actual <= lam+1e-11
        print(f"D={d}: unitarity error {unitarity:.3g}; "
              f"traceless contraction {actual:.10f} <= {lam:.10f}.")
        for n in (1,2,4,8):
            tau = choi_power(d,n,us)
            purity = float(np.trace(tau@tau).real)
            bound = 1/d**2+(1-1/d**2)*lam**(2*n)
            s = entropy(tau)
            assert purity <= bound+2e-11
            assert s+2e-11 >= -log2(purity)
            assert s <= 2*log2(d)+2e-11
            print(f"  n={n}: entropy={s:.10f}, purity={purity:.10f}, "
                  f"proved purity upper={bound:.10f}.")
        for n in (1,2):
            tau = choi_power(d,n,us)
            gram = output_gram(d,n,us)
            gap = abs(entropy(gram)-entropy(tau))
            assert gap <= 2e-10
            print(f"  n={n}: emitted-record/boundary entropy gap={gap:.3g}.")
    print("No large-memory family, capacity gap, or main evaluator was executed.")


if __name__ == '__main__':
    fixtures()
