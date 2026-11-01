# Positive conventional competitor for rare global-pattern passage

This supplements the broad WE/operator comparison after root moved to a Gaussian/free-fermion propagator plus finitely many reactive configurations. It is a construction of the conventional competitor, not a claimed new theorem or proof that the exact proposed application has already been published.

## An already available complete singleton mean operation

Let Q be a finite irreducible reversible continuous-time generator with equilibrium pi. Let b be a target configuration, and start from pi conditioned on not-b. Define

    a_b(t)=P_b(X_t=b)-pi_b.

The standard fundamental-matrix/hitting-time identity gives

    E_[pi|not-b] tau_b = A_b/[pi_b(1-pi_b)],
    A_b=int_0^infinity a_b(t)dt.

For completeness, let Z=int_0^infinity(P_t-Pi)dt. Then
`E_i tau_b=(Z_bb-Z_ib)/pi_b`; averaging over pi and using `pi Z=0` gives the displayed expression. Reversibility makes `a_b(t)` a positive sum of decaying exponentials,

    a_b(t)=sum_(j>=1) w_j exp(-lambda_j t),
    w_j>=0, sum_j w_j=1-pi_b.

If `0<g<=lambda_j<=Lambda` are acquired full-process spectral bounds, then

    (1-pi_b)/Lambda <= A_b <= (1-pi_b)/g,
    int_T^infinity a_b(t)dt <= (1-pi_b) exp(-gT)/g.

Consequently `T=g^-1 log(3 Lambda/(g delta))` makes the tail at most `(delta/3) A_b`, regardless of how small pi_b is. Since a_b is decreasing, the width between uniform left/right Riemann sums on [0,T] is at most `h(1-pi_b)`. Taking `h<=delta/(3 Lambda)` earns another `(delta/3) A_b` error. If each kernel evaluation is known to absolute tolerance `eta<=delta(1-pi_b)/(3 Lambda T)`, its accumulated integral error uses the final third. The number of evaluations is

    O((Lambda/(g delta)) log(Lambda/(g delta))).

This is polynomial in inverse gap and inverse requested relative error; it has no factor `1/pi_b`. The denominator's relative numerical error must be paid separately. A target weight exponential in n needs O(n) output bits for its scale, not an exponential number of bits. The argument does not automatically supply a stable Gaussian kernel evaluator, a spectral gap, or a finite-rank multi-target solve; those are its actual interfaces.

For a fixed pattern a as the initial state, the more general formula is `E_a tau_b=int_0^infinity[p_bb(t)-p_ab(t)]dt/pi_b`. Unlike the diagonal stationary-source construction, that integrand need not be a positive spectral mixture. Its error analysis must preserve the source law and control cancellation. The equilibrium-conditioned result should not be silently advertised for arbitrary starts.

## Independent executed check in interacting Glauber dynamics

`return_kernel_baseline.py` builds the full 2^n generator solely as an independent small-system verifier. It does not implement a scalable Pfaffian method. Rates for a periodic zero-field Ising chain are

    w_i(sigma)=0.5[1-(gamma/2) sigma_i(sigma_(i-1)+sigma_(i+1))],
    gamma=tanh(2 beta J).

For n=8, beta J=1.2, and the alternating global target, it gives:

| Quantity | Value |
|---|---:|
| Target equilibrium weight | 1.85687361998e-9 |
| Full-process gap from diagonalization | 0.0163251423063 |
| `1-tanh(2 beta J)` | 0.0163251423063 |
| Return-kernel MFPT | 67,967,644.4914 |
| Killed backward-equation MFPT | 67,967,644.2777 |
| Relative discrepancy | 3.1446e-9 |
| Integration horizon for the 1% tail-only criterion | 703.99434 |
| Horizon / MFPT | 1.03578e-5 |

The discrepancy is consistent with ordinary double precision in the ill-conditioned killed equation; it is not a rigorous enclosure. The exact model matches detailed balance. The current dense spectral evaluation is exponentially large and therefore is not a resource improvement over enumeration. Its role is to show that the conventional return formula is already a successful physical-kinetic calculation, rather than an empty certificate. A Gaussian implementation must be compared against this operation and against matrix-product state methods, not only against brute-force waiting.

## Strong alternatives / prior operations that matter

- The fundamental-matrix identity is ordinary Markov-chain theory: Aldous and Fill, *Reversible Markov Chains and Random Walks on Graphs*, Chapter 2, https://www.stat.berkeley.edu/users/aldous/Book2/book.pdf . The return-probability formula is also proved in Levin–Peres–Wilmer, Chapter 10, https://www.mat.uniroma3.it/users/martin/CP420/17/markovmixing.pdf . These sources are mathematical provenance, not a new application claim.
- Sharpe and Wales, *Numerical analysis of first-passage processes in finite Markov chains exhibiting metastability*, PRE 104, 015301 (2021), DOI https://doi.org/10.1103/PhysRevE.104.015301 . Graph transformations give exact multi-target splitting, mean/variance, visitation probabilities and stable metastable-state reduction once the full graph is represented. State enumeration remains expensive.
- *Finite Time Large Deviations via Matrix Product States*, PRL 128, 090605 (2022), DOI https://doi.org/10.1103/PhysRevLett.128.090605 ; https://arxiv.org/abs/2108.11418 . It computes finite-time dynamical partition sums and constructs rare-event trajectories in 1D. This is a stronger competitor than Monte Carlo alone; tensor ranks still determine cost.
- https://github.com/monalisasroy/MarkovMPS has explicit TT/MPO linear solves for means/splitting and a time stepper for survival. Its current README limits demonstrated tensor-network problems to small instances and uses Monte Carlo alone for the critical 24-site Manna example. It must not be promoted into a proved generic polynomial solver.
- Magoni, Majumdar, Schehr, *Ising model with stochastic resetting*, https://arxiv.org/abs/2002.04867 , already studies exact 1D Glauber stationary behavior under global resets. It does not by itself supply the new target-conditioned first-passage service.
- Blom and Godec, *Criticality in Cell Adhesion*, PRX 11, 031067 (2021), https://doi.org/10.1103/PhysRevX.11.031067 , studies full formation/dissolution first passage in interacting Glauber–Kawasaki bond clusters. Its small-system route is exact full state-space inversion and its large-system route uses a local equilibrium approximation with separately derived bulk scaling. This is an independently important physical use case, but its more general rates/fields/interactions are not automatically free-fermionic.

## Boundaries that could change the central question

1. A small collection of full configurations gives a small-rank boundary perturbation. A small collection of local-pattern predicates generally names exponentially many full configurations and is not a small-rank perturbation.
2. A full-spin pattern must distinguish both orientations if domain walls are used; the domain-wall encoding alone identifies sigma and minus-sigma. Boundary/parity sectors or an equivalent retained spin label must be earned in the Gaussian kernel.
3. A global-pattern-triggered physical reaction is an n-body recognition condition. A compact numerical predicate does not earn a local molecular mechanism implementing it.
4. Polynomial exact propagator evaluation does not automatically earn a polynomial stable inverse Laplace transform at requested relative tiny-tail error, or arbitrary multi-target matrix conditioning.
5. Low-temperature gap closure can restore large computation independently of the event's equilibrium rarity. The positive theorem above charges g explicitly.
6. The new scientific value would need to reside in an earned broad physical class, an efficient stable kernel/interface operation beyond the standard return identity, or a consequential control/interaction consequence. Calling the old identity a novel first-passage principle would be unsupported.
