"""Exact two-gain barrier for arbitrary randomized commuting cF rotations.

Numpy only checks the displayed sharp feasible witness. The proof, including
the exact value (sqrt(3)-1)/2, is in DERIVATION.md.
"""

import numpy as np


def main():
    eta = (np.sqrt(3)-1)/2
    p = (1 - 1/np.sqrt(3))/2
    z = np.array([-1, np.exp(-1j*np.pi/3)])
    weights = np.array([p, 1-p])
    m1 = weights @ z
    m2 = weights @ z**2
    t = np.array([[1, np.conj(m1), np.conj(m2)],
                  [m1, 1, np.conj(m1)], [m2, m1, 1]])
    target = np.array([[1, 1j, 1j], [-1j, 1, 1j], [-1j, -1j, 1]])
    v = np.exp(1j*np.pi*np.arange(3)/3)/np.sqrt(3)
    assert np.linalg.norm(target @ v - (1-np.sqrt(3))*v) < 2e-15
    assert np.min(np.linalg.eigvalsh(t)) > -2e-15
    assert abs(abs(m1+1j)-eta) < 2e-15
    assert abs(abs(m2+1j)-eta) < 2e-15
    print('Sharp two-gain commuting-macro diamond-error floor:', eta)
    print('Target coherence multiplier: -i')
    print('Optimal two-atom circle distribution:')
    print('  P(Z=-1) = (1-1/sqrt(3))/2 =', p)
    print('  P(Z=exp(-i*pi/3)) =', 1-p)
    print('m1 =', m1, '; m2 =', m2)
    print('Moment Toeplitz eigenvalues:', np.linalg.eigvalsh(t))
    print('Both errors |m_j+i|:', abs(m1+1j), abs(m2+1j))
    print('Finite witness checks support the analytic exact proof; no optimization solver used.')


if __name__ == '__main__':
    main()
