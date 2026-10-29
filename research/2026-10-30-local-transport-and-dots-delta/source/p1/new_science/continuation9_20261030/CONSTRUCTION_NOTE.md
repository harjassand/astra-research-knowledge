# Moving local memory: physical task and first construction

30 October 2026. Root working construction, not yet reviewed.

## Intended consequence

Implement the long-wavelength density/current law of a globally projected harmonic transport bath by an actual nearest-neighbor controller with bounded local dynamical coefficients. Retain nonflat periodic heat relaxation and its rare density histories, while suppressing net circulation on the same physical diffusive clock. The full density history objective is stronger than the earlier local elastic-memory stationary fluctuation objective. A helper is constructing ordinary inertial transport; useful relaxation alone is therefore not a sufficient novelty target.

## Candidate

Let B be the ring incidence, D>0 unknown but in a warranted compact interval, kappa_N between N^-2 and N^-1, and A a nearest-neighbor skew memory-advection matrix with A1=0. Actual currents and controller are

    dJ=-D(B^T x+kappa_N z)dt+sqrt(2D)dW,
    dx=B dJ,
    dz=dJ+A zdt.

The complete current, including controller backreaction, is counted. Product Gaussian x covariance identity on zero sum, z covariance kappa_N^-1 identity is invariant. This is a nonreversible local controller; no extension of the earlier reversible bound is asserted. Total current equals the change of sum z. Memory is independent across sites initially, but its amplitude in displacement units grows. With normalized cells w=sqrt(kappa)z, this instead pays weak reciprocal taps sqrt(kappa), their precision and dynamic range; memory energy is not asserted to diverge. The new resource is runtime memory transport, rather than a nonlocal prepared covariance or an event-wide bit.

For low nonzero wave number k~1/N, A has frequency order 1/N while physical density relaxation has frequency order 1/N^2. The window N^-2 << kappa_N << N^-1 should preserve the heat branch and suppress the harmonic branch. This requires a proof of path precision, not just formal elimination.

## Scope and early attacks

The displayed white-current bath is a mathematical port. It does not claim a finite hard bandwidth or a device. A finite-response current realization and an explicit operation-level resource ledger are still needed. Unknown homogeneous D is different from arbitrary unknown heterogeneous mobility. Under heterogeneous mobility passive constraint projection is metric-weighted and can change the density equation; no unchanged heterogeneous law is asserted.

An inertial local memory attempt with fixed stiffness produces quadratic sound modes rather than ordinary heat. Dipole-conserving hydrodynamics already contains such modes and is a strong predecessor. A symmetric diffusive memory communication channel has gap of order N^-2, leaving no kappa window at bounded coefficients. Ballistic or accelerated local communication is the opening to examine.

Primary sources being read include Tegling et al., arXiv:1710.02880 (distributed dynamic feedback limitations), and Glorioso et al., JHEP05(2023)022 (dipole/momentum hydrodynamics). A failed search is not evidence of novelty.
