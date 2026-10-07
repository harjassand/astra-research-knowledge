"""Gaussian-mixture completion and lossy two-fermion sampling.

Research prototype, 7 October 2026. NumPy floating-point implementation, NOT
an interval-certified implementation. The proof describes a finite-bit repair.

Conventions: mode 0 is the least significant occupation bit. Majoranas are
c[2*j]=a_j+a_j^dagger, c[2*j+1]=-i(a_j-a_j^dagger),
Gamma[j,k]=i <c_j c_k> for j!=k. Thus vacuum has Gamma[2*j,2*j+1]=-1.
eta is particle survival probability, not survival amplitude.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Sequence
import math
import numpy as np
from numpy.typing import NDArray

Array = NDArray[np.float64]
CArray = NDArray[np.complex128]


def vacuum_covariance(m: int) -> Array:
    if m < 0:
        raise ValueError("Number of modes must be nonnegative.")
    g = np.zeros((2*m, 2*m), dtype=float)
    idx = np.arange(m)
    g[2*idx, 2*idx+1] = -1.0
    g[2*idx+1, 2*idx] = 1.0
    return g


def realification(u: CArray) -> Array:
    """Rectangular complex one-particle map -> interleaved Majorana map."""
    u = np.asarray(u, dtype=complex)
    if u.ndim != 2:
        raise ValueError("Expected a matrix.")
    out = np.zeros((2*u.shape[0], 2*u.shape[1]), dtype=float)
    out[0::2, 0::2] = u.real
    out[0::2, 1::2] = -u.imag
    out[1::2, 0::2] = u.imag
    out[1::2, 1::2] = u.real
    return out


def gaussian_loss(gamma: Array, transfer: CArray) -> Array:
    """Apply a passive vacuum-loss contraction (unitaries included)."""
    t = np.asarray(transfer, dtype=complex)
    if gamma.shape != (2*t.shape[1], 2*t.shape[1]):
        raise ValueError("Covariance/transfer dimensions do not agree.")
    if np.linalg.norm(t, 2) > 1 + 2e-10:
        raise ValueError("Transfer matrix is not a contraction.")
    r = realification(t)
    j_in = vacuum_covariance(t.shape[1])
    ans = vacuum_covariance(t.shape[0]) + r @ (gamma-j_in) @ r.T
    return (ans-ans.T)/2


def pair_covariance(z: complex) -> Array:
    """Covariance of (|00>+z|11>)/sqrt(1+|z|^2), analytically."""
    d = 1 + abs(z)**2
    n = abs(z)**2/d
    # Cross-correlations are also checked independently against Fock matrices.
    g = np.zeros((4, 4), dtype=float)
    g[0, 1] = g[2, 3] = 2*n-1
    g[0, 2] = 2*z.imag/d
    g[0, 3] = -2*z.real/d
    g[1, 2] = -2*z.real/d
    g[1, 3] = -2*z.imag/d
    return g-g.T


def completion_parameter(weights: Array, a: float, b: float) -> float:
    """Solve product_j(1+x*w_j)=1+b/a by monotone bisection.

    weights sum to one. This avoids a poorly conditioned polynomial expansion.
    """
    w = np.asarray(weights, dtype=float)
    if a <= 0 or b < 0 or np.any(w < 0):
        raise ValueError("Require a>0, b>=0, nonnegative weights.")
    if abs(w.sum()-1) > 1e-9:
        raise ValueError("Weights must sum to one.")
    if b == 0:
        return 0.0
    target = math.log1p(b/a)
    lo, hi = target, b/a  # log(1+t) <= x <= t
    for _ in range(100):
        mid = (lo+hi)/2
        if float(np.log1p(mid*w).sum()) < target:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2


@dataclass
class TwoFermionBlock:
    """Canonical two-form sum_j s[j] u[2j]^dag u[2j+1]^dag |vac>.

    orbitals is an isometry of shape (ambient_modes, 2*len(s)); omitted means
    the canonical basis. Coefficients may be complex. balanced_magic=True
    uses the globally trace-optimal four-mode construction, valid only for
    equal magnitudes of its two coefficients (phases are allowed).
    """
    coefficients: CArray
    eta: float
    orbitals: Optional[CArray] = None
    balanced_magic: bool = False

    def __post_init__(self) -> None:
        self.coefficients = np.asarray(self.coefficients, dtype=complex)
        if self.coefficients.ndim != 1 or not len(self.coefficients):
            raise ValueError("Provide at least one pair coefficient.")
        if not np.all(np.isfinite(self.coefficients)):
            raise ValueError("Nonfinite coefficient.")
        if abs(float(np.vdot(self.coefficients,self.coefficients).real)-1) > 1e-9:
            raise ValueError("Pair coefficients must have squared norm one.")
        if not 0 <= self.eta < 1:
            raise ValueError("This prototype requires 0 <= eta < 1.")
        r = len(self.coefficients)
        if self.orbitals is None:
            self.orbitals = np.eye(2*r, dtype=complex)
        self.orbitals = np.asarray(self.orbitals, dtype=complex)
        if self.orbitals.ndim != 2 or self.orbitals.shape[1] != 2*r:
            raise ValueError("Incorrect orbital-isometry shape.")
        if np.linalg.norm(self.orbitals.conj().T@self.orbitals-np.eye(2*r)) > 1e-8:
            raise ValueError("Orbital columns are not orthonormal.")
        if self.balanced_magic and (r != 2 or np.max(np.abs(np.abs(self.coefficients)**2-.5)) > 1e-10):
            raise ValueError("balanced_magic requires two equal pair weights.")

    @property
    def modes(self) -> int:
        return self.orbitals.shape[0]

    @property
    def rank(self) -> int:
        return len(self.coefficients)

    def parameters(self) -> tuple[float,float,float,float]:
        a, b = (1-self.eta)**2, self.eta**2
        if self.balanced_magic and b >= 3*a:
            x, delta = 2.0, (b-a)/2
        else:
            x = completion_parameter(abs(self.coefficients)**2, a, b)
            # Cancellation-safe identity for rank-two balanced magic.
            if self.balanced_magic:
                delta = b*b/(math.sqrt(a+b)+math.sqrt(a))**2
            else:
                delta = max(0.0, b-a*x)
        return a,b,x,delta

    def sample_covariance(self, rng: np.random.Generator) -> Array:
        a,b,x,_ = self.parameters()
        active_modes = 2*self.rank
        if rng.random() < a+b:
            theta = 2*math.pi*int(rng.integers(self.rank+1))/(self.rank+1)
            g = np.zeros((2*active_modes,2*active_modes))
            for j,s in enumerate(self.coefficients):
                g[4*j:4*j+4,4*j:4*j+4] = pair_covariance(math.sqrt(x)*s*np.exp(1j*theta))
        else:
            j = int(rng.choice(active_modes, p=np.repeat(abs(self.coefficients)**2/2,2)))
            g = vacuum_covariance(active_modes)
            g[2*j,2*j+1],g[2*j+1,2*j] = 1.,-1.
        r = realification(self.orbitals)
        ans = vacuum_covariance(self.modes)+r@(g-vacuum_covariance(active_modes))@r.T
        return (ans-ans.T)/2


def canonical_two_form(a: CArray, tolerance: float = 1e-10) -> tuple[CArray,CArray,float]:
    """Acquire a Youla/Slater decomposition of a normalized antisymmetric matrix.

    Returns (coefficients, orbital_isometry, discarded_two_form_vector_norm).
    This floating implementation is verified on random complex inputs by the
    included tests, not a certified SVD implementation. Tiny singular pairs
    are deliberately dropped; the returned retained coefficients are normalized.
    """
    a = np.asarray(a, dtype=complex)
    if a.ndim != 2 or a.shape[0] != a.shape[1] or np.linalg.norm(a+a.T)>1e-9:
        raise ValueError("Expected a complex skew-symmetric square matrix.")
    if abs(np.linalg.norm(a,'fro')**2/2-1)>1e-8:
        raise ValueError("Two-form must have Fock norm one.")
    residual = a.copy()
    columns, values = [],[]
    for _ in range(a.shape[0]//2):
        vals,vecs = np.linalg.eigh(residual@residual.conj().T)
        s = math.sqrt(max(0.,float(vals[-1])))
        if s <= tolerance:
            break
        u = vecs[:,-1]
        v = -residual@u.conj()/s
        # Exact arithmetic gives orthonormal u,v; numerical input is checked.
        columns.extend([u,v]); values.append(s)
        residual -= s*(np.outer(u,v)-np.outer(v,u))
        residual = (residual-residual.T)/2
    if not values:
        raise ValueError("Tolerance discarded the entire input.")
    w = np.column_stack(columns)
    if np.linalg.norm(w.conj().T@w-np.eye(w.shape[1])) > 1e-7:
        raise ArithmeticError("Loss of orthogonality; use higher precision.")
    v = np.asarray(values,dtype=complex)
    v /= np.linalg.norm(v)
    reconstructed = w @ canonical_pair_matrix(v) @ w.T
    error = np.linalg.norm(a-reconstructed,'fro')/math.sqrt(2)
    return v,w,float(error)


def canonical_pair_matrix(s: CArray) -> CArray:
    a = np.zeros((2*len(s),2*len(s)),dtype=complex)
    for j,z in enumerate(s):
        a[2*j,2*j+1],a[2*j+1,2*j] = z,-z
    return a


def condition_first_mode(gamma: Array, bit: int) -> tuple[float,Array]:
    """Born probability and conditioned covariance after removing first mode."""
    if bit not in (0,1) or gamma.shape[0] < 2:
        raise ValueError("Invalid measurement.")
    s = 2*bit-1
    den = 1+s*float(gamma[0,1])
    p = den/2
    if p < -1e-9 or p > 1+1e-9:
        raise ArithmeticError("Unphysical covariance; numerical failure.")
    p = float(np.clip(p,0,1))
    if p <= 0:
        return 0., gamma[2:,2:].copy()
    cross = np.outer(gamma[2:,0],gamma[1,2:])-np.outer(gamma[2:,1],gamma[0,2:])
    ans = gamma[2:,2:] + (s/den)*cross
    return p,(ans-ans.T)/2


def sample_covariance(gamma: Array, rng: np.random.Generator) -> NDArray[np.int8]:
    """O(M^3) arithmetic, O(M^2) memory occupation sampler."""
    g = np.asarray(gamma,dtype=float).copy()
    if g.ndim != 2 or g.shape[0] != g.shape[1] or g.shape[0] % 2:
        raise ValueError("Covariance must be an even-size square matrix.")
    bits=[]
    for _ in range(g.shape[0]//2):
        p1 = float(np.clip((1+g[0,1])/2,0,1))
        bit = int(rng.random()<p1)
        if len(g) == 2:
            # No further conditioning is needed for the final measurement.
            bits.append(bit)
            break
        p,g = condition_first_mode(g,bit)
        if p == 0:
            raise ArithmeticError("Numerically sampled an impossible outcome.")
        bits.append(bit)
    return np.asarray(bits,dtype=np.int8)


def sample_lossy_two_fermions(blocks: Sequence[TwoFermionBlock],
                             transfer: CArray, shots: int = 1,
                             seed: Optional[int] = None) -> dict:
    """Sample Gaussian approximant after the supplied passive contraction.

    The target has already suffered each block's declared input loss. For a
    passive interferometer followed by uniform output loss eta, declare eta
    in each block and pass the lossless interferometer, not sqrt(eta)*U.
    """
    if shots < 1:
        raise ValueError("shots must be positive")
    m = sum(b.modes for b in blocks)
    t = np.asarray(transfer,dtype=complex)
    if t.ndim != 2 or t.shape[1] != m or np.linalg.norm(t,2)>1+2e-10:
        raise ValueError("Incorrect transfer shape or noncontractive transfer.")
    rng = np.random.default_rng(seed)
    results = np.empty((shots,t.shape[0]),dtype=np.int8)
    for shot in range(shots):
        gamma = np.zeros((2*m,2*m)); pos=0
        for block in blocks:
            gb = block.sample_covariance(rng)
            gamma[pos:pos+len(gb),pos:pos+len(gb)] = gb
            pos += len(gb)
        results[shot] = sample_covariance(gaussian_loss(gamma,t),rng)
    deltas = [b.parameters()[3] for b in blocks]
    # All local target/approximant pairs commute, so product couplings apply.
    tv = -math.expm1(sum(math.log1p(-d) for d in deltas)) if all(d<1 for d in deltas) else 1.
    return {"samples":results,"state_error_bound":tv,"block_errors":deltas,
            "implementation":"floating-point prototype; no rounding certificate"}


if __name__ == '__main__':
    blocks = [TwoFermionBlock(np.array([1,1])/math.sqrt(2),.1,balanced_magic=True) for _ in range(10)]
    result = sample_lossy_two_fermions(blocks,np.eye(40),shots=5,seed=7)
    print("Symbolic state bound (numerically evaluated, not interval-certified):", result['state_error_bound'])
    print("Particle counts in five prototype samples:",result['samples'].sum(axis=1).tolist())
