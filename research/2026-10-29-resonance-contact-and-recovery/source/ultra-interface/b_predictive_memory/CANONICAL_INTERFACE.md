# Fixed charge: a real distinction, an ordinary constructive receiver, and one unpaid step

## 1. Primary screen and decision

The broad claim that weakly interacting fermionic Gibbs mixtures still lack
an efficient sampler is outdated. Han--Zhao--Liu, arXiv:2609.35159 (September
2026), Theorem 1 and Appendix E, supplies a Gaussian-leaf tree Metropolis
sampler at fixed finite beta, fixed spatial dimension/range, and sufficiently
small interaction. The sampling threshold can be smaller than the
convex-Gaussianity threshold. Chen et al., arXiv:2512.12010v2, supplies a
tree-determinant/importance-sampling method for log Z and local observables
with its own Green-function/locality/weak-coupling conditions. These are
ordinary comparators, not available at arbitrary interaction or temperature.

Bu--Ren, arXiv:2609.09608, also has a separate atomic/strong-Hubbard
convex-Gaussian existence window. For coordination number D and t/U small,
its explicit bound is

    beta <= (2/|U|) log(1+|U|/(576 D |t|)).

For repulsive U>0, at the superexchange scale `J_ex=4t^2/U`, its allowed `beta J_ex` tends to
zero as `t/U ->0`. Therefore it cannot be silently promoted to a sampler
for low-temperature magnetic Hubbard physics. Its strong-coupling sampling
question and the September 28 WEAK-coupling sampler are different scopes.
No general new Gibbs-sampling lane is justified by these statements alone.

## 2. Exact full-rank counter to charge-preserving Gaussianity

Consider four modes, paired as 12 and 34. On each two-mode Fock space let

    tau = exp[r(c_1^dagger c_2^dagger+c_2 c_1)]/6,
    cosh(r)=2, sinh(r)=sqrt(3).

In the order 00,01,10,11, tau has even block
`[[2,sqrt(3)],[sqrt(3),2]]/6` and odd diagonal entries `1/6`.
It is a full-rank Gaussian density matrix. Form the Gaussian product
`rho_G=tau_12 tensor tau_34` and dephase ONLY total particle number:

    rho_bar = (1/5) sum_(j=0)^4 exp(2pi i j N/5) rho_G exp(-2pi i j N/5).

This is an explicit mixture of FIVE Gaussian states, full rank, and
commutes with N. Its N=2 sector has probability `1/3`. In the six-dimensional
two-particle space its normalized conditional state is

    rho_2 = I_6/12 + |psi><psi|/2,
    |psi>=(|12>+|34>)/sqrt(2).

Every normalized Slater determinant has overlap squared at most `1/2`
with psi: write its two orthonormal orbitals f,g and apply Cauchy--Schwarz
to the unit-norm antisymmetric form `J_12 direct_sum J_34`.
Every Gaussian component of a positive decomposition supported at fixed
N=2 must itself be a Slater determinant (zero number variance).
Thus the witness `I_6/2-|psi><psi|` is nonnegative on every such
convex-Gaussian state, but its expectation in rho_2 is `-1/12`.

Canonical projection therefore need not preserve convex-Gaussianity,
EVEN when the input commutes with N and the sector is not rare. This is
not a counterexample to any weak-coupling Gibbs theorem: `-log(rho_bar)`
is number conserving, but no weak-coupling bound on it has been supplied.

## 3. A direct receiver that does not require projected Gaussianity

For a Gaussian state with Majorana covariance
`Gamma_ab=i Tr(rho gamma_a gamma_b)` for a!=b, define J as block diagonal
copies of `[[0,1],[-1,0]]`. Wick's theorem gives the polynomial identity

    chi(z)=Tr(rho z^N)
          =2^(-n) Pf[(1+z)J+(z-1)Gamma].                 (1)

Expand `z^n_i=[(1+z)+(z-1)i gamma_(2i-1)gamma_(2i)]/2` and use the
principal-pair-minor expansion of the Pfaffian to prove (1). No square-root
branch is needed. The coefficients `w_q=[z^q]chi(z)` are the charge
probabilities. They can be computed with n+1 Pfaffian evaluations and
polynomial interpolation, in polynomial exact arithmetic. The vacuum
convention is Gamma=-J; the fully occupied convention is Gamma=+J.

There is a rejection-free TERMINAL occupation sampler from
`rho_q=Pi_q rho Pi_q/w_q`. Suppose mode i is next. Its unconditioned
probabilities are `p_x=(1+s Gamma_ab)/2`, s=2x-1. The ordinary conditional
Gaussian covariance on the remaining modes is

    Gamma'_cd = Gamma_cd
      + s( -Gamma_ca Gamma_db + Gamma_cb Gamma_da )/(1+s Gamma_ab).

The exact conditional branch probability in the fixed-charge state is

    Pr(x | q) = p_x w_(q-x)(Gamma')/w_q(Gamma).          (2)

Update the Gaussian component, remove that mode, and reduce q by x.
Repeated use of (1)--(2) yields an occupation sample without rejection
cost `1/w_q`. A direct implementation uses O(n^5) arithmetic operations;
more efficient standard Pfaffian/counting implementations are allowed the
same information. Rational inputs can be treated with exact reduced
rational arithmetic; numerical inputs require an outward/precision
contract, especially at small branch probabilities. No floating diagnostic
is a finite-bit sampler certificate.

This receiver also supports number-conserving Gaussian instruments on a
charge-projected Gaussian representation. Such Kraus operators commute
with Pi_q, so each update remains a charge projection of a Gaussian state.
A finite weak measurement of a single n_i has an outcome law that is a
mixture of the two calibrated Gaussian read distributions with weights
given by (2); the unprojected covariance updates by the Gaussian Kraus
operator. Number-conserving quadratic feedback preserves the form. This
does not include arbitrary pairing feedback, arbitrary non-Gaussian
operations, or a growing number of independent charge projections.

These are established counting/projection/Gaussian-operation mechanisms:
Klich (2014), arXiv:1403.7824; Fanto--Alhassid--Bertsch (2017),
arXiv:1610.08954; and the broader Gaussian-superposition simulation
framework of Dias--Koenig (2024), arXiv:2307.12912. This self-contained
receiver is not promoted as a new discovery. Exact projection can be
computationally useful outside convex-Gaussian state geometry.

## 4. The remaining acquisition cannot be skipped

If a Gibbs sampler returns Gaussian components rho_a according to p(a),
then charge conditioning changes their distribution to

    p_q(a)=p(a) w_q(a)/E_p w_q(a).

Conditioning each sampled component with its OLD probability p(a) is
generally wrong. Equations (1)--(2) pay the within-component problem,
not this outer reweighting. Rejection costs `1/Pr(N=q)`; weighted ratio
estimation requires a controlled second-moment ratio
`E w_q^2/(E w_q)^2`; a new tree Metropolis proof needs its own charge-trace
oracle and mixing bound. Neither convex-Gaussianity nor a Pfaffian leaf
formula supplies these for free.

This is a precise different question if fixed-charge predictions are the
actual scientific target. It is not presently a justified leading route:
ordinary full-counting-statistics, number-projected Monte Carlo and the
2026 tree sampler must receive the same charge information, and typical
sectors may already be economical with ordinary conditioning. No generic
rare-sector advantage, low-temperature Hubbard operation, or completed
canonical Gibbs sampler was acquired here.
