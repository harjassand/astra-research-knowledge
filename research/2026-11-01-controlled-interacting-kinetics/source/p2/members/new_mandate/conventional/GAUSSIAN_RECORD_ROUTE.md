# Resolved classical reaction records: an existing matchgate construction

Root considered retaining a full conditional Gaussian probability vector while observing selected individual reaction channels and applying causal feedback. The following constructive conventional route displaces a foundational novelty claim for that closure. It does not invoke quantum Born probabilities.

## Local algebra

For nearest-neighbor pair creation `00->11` at c, annihilation `11->00` at a, and hopping `10->01` at d, `01->10` at e, the column generator in basis 00,01,10,11 is

    q = [[-c,  0,  0,  a],
         [ 0, -e,  d,  0],
         [ 0,  e, -d,  0],
         [ c,  0,  0, -a]].

Its even and odd block traces are equal precisely when `a+c=d+e`. Hence `exp(t q)` has parity blocks of equal determinant, the standard matchgate condition. Removing an observed channel's off-diagonal jump matrix J leaves the diagonal unchanged, so `q0=q-sum J` retains this trace equality and quadratic fermion form. A sum over bonds is still a quadratic global generator; its propagator is a Gaussian linear map. A periodic boundary requires its actual parity-sector sign.

Each individually resolved jump matrix `J=r|out><in|` within one parity sector is a singular matchgate: both 2x2 block determinants vanish. Equivalently it is a product of two linear creation/annihilation operators (including the required JW sign). Applying such a map to a pure fermionic Gaussian amplitude vector retains that class, possibly with a different Gaussian chart. Single-chart BCS coordinates may become singular; that is a representation issue, not permission to discard the event.

## The classical normalization is also a Gaussian contraction

On a fixed even-parity sector, define the unnormalized bra

    <Omega| = <0| exp(sum_(i<j) c_j c_i).

Its coefficient on every even occupancy set I is `Pf(S_I)`, where `S_ij=1` for i<j and `S_ji=-1`. This Pfaffian is 1 for every even I: expand in the first row; the alternating sum of 2k-1 ones is 1, and induct on k. Consequently `<Omega|p>` is exactly the sum of the classical probabilities, with no squaring of amplitudes. An extra auxiliary mode handles odd parity, or two parity components can be carried separately.

For an observed record with marked jumps a_1,...,a_m at times t_1,...,t_m, its likelihood density is the ordinary contraction

    <Omega| exp(Q0*(T-t_m)) J_(a_m) ... J_(a_1) exp(Q0*t_1) |p0>.

Every factor and both boundary states are Gaussian/matchgate objects for admitted initial data. Thus existing nonunitary matchgate/Pfaffian algebra evaluates it in polynomial arithmetic cost in system size and record length. Feedback merely selects the next admitted generator from the already observed record; a fixed record branch still has the same form. The sum over all possible feedback records need not be Gaussian, but sampling one record does not enumerate that sum.

In particular `S(t)=<Omega|exp(Q0 t)|p>` is no-record survival and `f_a(t)=<Omega|J_a exp(Q0 t)|p>` is the marked density. The stochastic generator identity gives `-S'(t)=sum_a f_a(t)`. Inverting S and sampling proportional marked densities yields the usual next-observed-event construction, provided finite-horizon/tail, numerical precision, and any no-event mass are handled. This is a classical linear-probability interpretation of existing Gaussian contraction machinery.

## Governing sources

- Valiant, *Quantum circuits that can be simulated classically in polynomial time*, SIAM J. Comput. 31, 1229–1254 (2002), DOI https://doi.org/10.1137/S0097539700377025 . Its theorem explicitly does not require unitarity.
- Knill, *Fermionic Linear Optics and Matchgates* (2001), https://arxiv.org/abs/quant-ph/0108033 ; exact PDF https://arxiv.org/pdf/quant-ph/0108033 . The introduction treats computation of entries and traces of products; the monoid construction includes nonunitary maps and number projections.
- Jozsa, Miyake, Strelchuk, *Jordan–Wigner formalism for arbitrary 2-input 2-output matchgates and their classical simulation*, Quantum Information and Computation 15, 541–556 (2015), https://arxiv.org/abs/1311.3046 ; exact PDF https://www.rintonpress.com/xxqic15/qic-15-78/0541-0556.pdf . Theorem 1 explicitly includes noninvertible matchgates as the closure of quadratic/linear fermionic exponentials.

This comparison is a positive derivation from those established operations. It does not claim that one of these papers already advertises the identical chemical-filtering API or its exact stochastic l1 notation. The representation change and classical normalizer do not constitute an earned foundational gap in those operations.

## Useful failures and remaining costs

- An unresolved mark replaces J_a by a sum of jump maps. A general sum of Gaussian maps is not Gaussian; the posterior can require a growing mixture. Exact bond/channel resolution is a material information assumption.
- Generic reaction networks fail `a+c=d+e`; their generator contains quartic fermion terms.
- Nonlocal physical reaction detection, time resolution, initialization, and feedback implementation are additional physical resources. An algebraic detector is not an acquired instrument.
- Polynomial arithmetic complexity does not automatically establish uniform polynomial bit cost for near-zero likelihoods, singular charts, arbitrary real time schedules, or ill-conditioned matrices.
- An efficient next-observed-event calculation alone does not establish a new rare-pattern full first-passage operation. A pattern predicate is not generally a resolved elementary jump.

## Focused comparison for the subsequent collective-pattern bridge

The finite reactive-boundary transformation itself also has strong prior theory:

- Hartich–Godec, J. Stat. Mech. 2019 024002, DOI https://doi.org/10.1088/1742-5468/ab00df , exact primary PDF https://www.mpinat.mpg.de/634361/Hartich_2019_J-Stat-Mech.pdf . It explicitly writes `L_a=L-L|a><a|` and obtains the full first-passage distribution from the reversible relaxation eigensystem. It does not supply a polynomial-size free-fermion global-pattern oracle.
- Giuggioli, PRX 10, 021045 (2020), DOI https://doi.org/10.1103/PhysRevX.10.021045 , gives multiple-target first-passage generating functions from confined random-walk propagators.
- Sarvaharman–Giuggioli, PRResearch 5, 043281 (2023), DOI https://doi.org/10.1103/PhysRevResearch.5.043281 , gives finite-defect propagators and first-passage/return/exit generating functions from an unperturbed propagator on arbitrary lattice shapes and dimensions.

The focused search did not find a paper explicitly joining polynomial Gaussian many-body configuration kernels, arbitrary Fock preparation, finite competing global targets, and controlled rare-scale numerical inversion. Historical novelty of that exact completed service remains UNKNOWN; renewal, finite-rank defects, Gaussian propagation, and stationary-pole extraction must retain prior credit.
