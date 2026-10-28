# Reviewed actual-model warm transfer compression

Root review2026-10-28. Accepted at the following scope: the supplied exact
open-chain moments, a three-vector polynomial and complete even spatial
moments give rigorous warm partition/spatial-purity enclosures on the actual
uniform spin-two rings128/256. No uniform physical gap, cold bootstrap seed,
finite history rank, stochastic mixing or physical apparatus is supplied.

## Source interface, read rather than inferred

The Tasaki continuous-time primary, Sections3.2--3.4 and AppendixC.1, was
read: https://haltasaki.github.io/writings/AI/OpenAI_Haldane_CT.pdf . The
real symmetric history kernel defines a compact self-adjoint K_beta. It may
have negative weights/eigenvalues; no Perron--Frobenius theorem is assumed.
Its even power traces are actual periodic physical partition functions.
Fixing the two endpoint histories empty makes its vacuum matrix element
<vac,K^r vac> the r-site open-chain trace. The empty-history atom has mass1.
These are operator identities for the actual kernel, rather than a generic
moment realization chosen to match short rings.

For J=K/5, the source inputs used here are

    m_r=<vac,J^r vac>=Z_open,r(beta)/5^r, r=1,...,6;
    Tr J²=Tr exp(-2beta h_pair)/25;
    Tr J⁴=Z_periodic4(beta)/625.

The spin addition spectra for the pair and periodic4 supply the last two
complete moments. All unrepresented spatial eigenvalues are included.

## Why the low-dimensional reduction is legitimate

For any compact self-adjoint J, take a normalized trial v with Rayleigh
theta and residual variance r². Suppose theta>=a>0 and a complete even
moment M_p=Tr J^p is known. Let R=M_p-a^p>=0 and rho=R^(1/p).
The true largest positive eigenvalue lambda is at least a. Removing its
contribution leaves sum of pth absolute powers of every other mode at mostR.
Thus each other mode has modulus<=rho. If a>rho, the positive leading mode
is simple and separated BEFORE using the residual. The Temple inequality
then gives lambda<=theta+r²/(theta-rho), with outward interval endpoints.

For completeness, spectral averaging of
(x-lambda)(x-rho)>=0 on the spectrum gives
r²+(theta-lambda)(theta-rho)>=0. This proves the upper bound and needs no
finite-rank or positive-kernel premise. The source trial v is a rational
polynomial of degree2 in J applied to vac; its norm, mean and residual use
exactly the six acquired open-chain functions. Its numerical Cholesky/eigen
calculation merely proposes three rational decimal coefficients.

For every even n>=p,

    a^n <=Tr J^n<=b^n+R rho^(n-p),
    S(n,beta)>=1/[1+R rho^(n-p)/a^n]^2,

where b is the acquired leading upper bound. The spatial-purity formula
cancels the same leading eigenvalue rather than subtracting independently
rounded large logs. Physical Z_n=5^n Tr J^n; this factor is retained in
temporal-purity conversions.

## Actual independent execution and input review

The whole acquire_open_moments.py producer was read. In the unnormalized
spin basis, 2H has integer entries diagonally similar to the physical
Hermitian Hamiltonian. Every magnetization sector is counted; spin-flip
symmetry supplies the negative ones. Sparse integer multiplication stays
within its explicitly checked int64 row/trace bounds. CRT modulus exceeds
twice dim*(12(n-1))^96, so the signed traces are uniquely reconstructed.
Taylor enclosures pay every omitted exponential term, not selected energies.

Root independently checked all97 moments of open2 and open3 using exact
spin-addition spectra, and all chain dimensions/leading moment identities,
physical moment bounds and CRT reconstruction-size conditions. The full
n4..6 modular powers were not independently regenerated. Acceptance of
those data uses the completed producer algorithm/control-flow/arithmetic
review and its actual execution, rather than a hash as a scientific premise.

rational_warm_replay.py imports only stdlib, the serialized exact moments
and candidate coefficients. It reconstructs open trace boxes using Fraction
Taylor sums, proves rational exponential tails by a geometric remainder,
and bounds spectral roots by exact integer roots. It imports none of the
producer's mpmath/interval/core code. Selected beta1/8,1/4,1/2 passed. The
Z256 log-width upper bounds are respectively below2.67721e-11,5.19645e-8,
and2.15853e-4; S128(1/2) defect is below5.11533e-7. The receipt contains
outward exact rational bounds and source hashes; float fields are diagnostics.

These are accepted actual finite-model enclosures. They are not evidence
for cold beta64/96 or a generic superiority over known certified thermal,
Krylov or cluster methods. The later degree192/A4 projection is a distinct
source version and is covered by the separate review below, not by that
degree96 receipt. The conditional gap criterion
also requires temporal purity on the DOUBLE ring; spatial concentration
alone cannot satisfy it.

## Completed sector and cold-boundary extension

Root subsequently whole-read continuation/CONSTRUCTION.md and the twisted4
CRT producer. Its two-component recurrence is exact multiplication in
Z[zeta]/(zeta²+zeta+1), and its row/trace overflow checks cover both components.
The seam phases are conjugate raising/lowering phases, so diagonal similarity
recovers a Hermitian physical twisted Hamiltonian. All its power traces are
real algebraic integers in Q(zeta), hence ordinary integers. Both physical
twists remain positive partition functions. The A4 fourth moment is
(M4+3Z4(P)/625+8Z4(C)/625)/12, and the vacuum trial is fully SO3-scalar.

For integer SO3 spin j, the A4-invariant multiplicity is
[2j+1+3(-1)^j+8chi_j(2pi/3)]/12. At j1 the complement has dimension3;
for every j>=2, |chi_j|<=1 gives complement at least11j/6>3. Thus every
nontrivial scalar-complement eigenmode costs at least three copies in the
complement trace. Using the maximum of the invariant residual fourth-root
and the complement mass/3 fourth-root bounds ALL other modes. The final
ring tail still uses the FULL fourth moment, not a discarded sector mass.

rational_a4_replay.py independently reconstructs these bounds in Fraction
arithmetic, checks all193 open2/open3 analytic moments, degree96/192 exact
overlap and CRT size bounds. It reads pinned copies of the exact inputs;
no author numerical or verification code is imported. Its actual output is

    1-S(256,3/4)<1.85092994054e-24,

with an exact outward rational in RATIONAL_A4_REPLAY.json. Seven doublings
to beta96 amplify the initial log debt by less than2.369191e-22. Fifteen
further normalized thermal-purity inputs are still missing. This is an
accepted warm actual-model operation, not the final cold bootstrap seed.

Root also independently rebuilt the physical381-by381 M0 open5 Hamiltonian
from literal spin ladder coefficients and replayed every dyadic LL^T/LX
entry using integer object products. The positive shifted margin in
INDEPENDENT_COLD_BOUND.json proves H_open5>=-19.604. Integer-spin SU2
completeness and translated open clusters give H_n>=-4.901n. Consequently
||K_beta||<=5 exp(4.901 beta), while TrK_beta^4>=exp(20 beta). Even with an
exact leading vector, the unprojected fourth-moment residual cannot isolate
one mode past beta18.0074; the A4 projected version cannot past about24.28.
At beta64, independent rational exponential bounds give projected mass per
maximum possible mode4 strictly greater than13,542,476. A residual-mass
strategy must capture at least that many modes to leave less than one mode's
mass. This is explicitly a restriction on that tail certificate, not every
compressed transfer method.

## Physical-product-frame applicability

The corpus-first positive-transfer analytic proof was read. It preserves
closed traces rather than assuming a generic positive HMM intertwiner also
preserves periodic traces. Its quadratic9 and exact-exponential25 factors
remain different operations with different error/history costs. The tested
local rank obstruction is not a global scalar-trace lower bound.

independent_product_barrier.py separately reconstructs the ordinary spin2
AKLT tensors and their exact nine-dimensional transfer/projectors from
literal formulas, importing no corpus-first module. It proves the entire
even-ring trial energy family is below-9/2 per bond. Gibbs free-energy and
entropy bounds then give U_beta/n<-9/2+log5/beta. Every fully separable state
has energy at least-4n, and ||H_n+nI||<=5n. A rational Taylor proof of
log5<161/100 therefore gives trace distance greater than3039/64000 at
beta64, or4639/96000 at beta96, from EVERY fully separable state on every
even ring n>=4. This accepted applicability test excludes high-accuracy
one-spin physical PSD product reconstruction of the cold Gibbs state.
Nonphysical worldline factors, entangled blocks and scalar-only algorithms
are not excluded. No physical experiment or new AKLT/entanglement-witness
principle is claimed.
