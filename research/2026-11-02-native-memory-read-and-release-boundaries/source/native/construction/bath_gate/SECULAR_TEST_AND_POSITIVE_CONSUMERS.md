# Robust native memory: bath-framework obstruction and positive conditional consumers

2026-11-02 UTC (work begun 2026-11-01). Result: **a minimal exact Davies discontinuity is established; robust native thermal memory is NOT established.** A finite-bandwidth consumer and an exact finite-bath consumer isolate precisely what would suffice. The latter is the cleanest passive physical continuation of the earlier exact-H theorem, conditional on a new actual-native perturbed Gibbs witness bound.

The native model still means bounded-dimensional clocks (K=7 in the supplied construction) and arbitrary allowed Hermitian qubit–qudit two-body couplings, not a qubit-only or prescribed natural-exchange implementation. Generic weak symmetry-breaking calibration perturbations are the new issue here; their thermal robustness has not been earned by the exact-model dressing.

## 1. Minimal local counterexample to continuity of fully secular Davies dynamics

Take two qubits, labeled logical L and ancillary a, and

    H_delta = Delta n_a + delta Z_L n_a,
    n_a=|1><1|_a,   0<|delta|<Delta.

The perturbation is a local two-body term of norm |delta|. The only reservoir contact is the LOCAL ancillary operator X_a; it never directly contacts L.

At delta=0, the positive transition energy is Delta and its downward jump is

    A_down = I_L tensor |0><1|_a.

Its adjoint is the upward jump. Both act trivially on L, so the dissipative dynamics leaves logical coherence exactly unchanged.

For EVERY nonzero delta, the two transition energies are Delta+delta and Delta-delta. Correct Davies secularization now supplies separate downward jumps

    A_+ = Pi_+^L tensor |0><1|_a,
    A_- = Pi_-^L tensor |0><1|_a,

and their adjoints. Choose downward rates one and upward rates exp[-beta(Delta±delta)]. These are bounded, continuous thermal rate functions over this frequency interval. The jump record resolves the logical Z branch, even when the separation 2delta is arbitrarily small.

Here is an explicit dissipative INTERACTION-PICTURE formula in Davies rescaled time tau. Initialize L in |+> and ancilla in the marginal retained by overwriting L in the actual Gibbs state. Set

    p_e(delta)=e^(-beta Delta) cosh(beta delta) /
                   [1+e^(-beta Delta) cosh(beta delta)],
    u_bar(delta)=e^(-beta Delta) cosh(beta delta).

The normalized logical off-diagonal coherence is

    c_delta(tau)=(1-p_e) exp[-u_bar tau]+p_e exp[-tau],  delta !=0.

Jump gain terms vanish on the off-diagonal logical block; the two anticommutators give the displayed decay. At delta=0, c_0(tau)=1 instead. Thus

    lim_(delta->0, delta!=0) c_delta(tau)
       =(1-r) exp[-e^(-beta Delta)tau]+r exp[-tau] <1,
    r=1/(1+e^(beta Delta)), tau>0.

At beta=Delta=tau=1 this limit is approximately 0.6049772267, versus exactly one at delta=0. The X-observable alone lower-bounds the output trace-norm discrepancy by approximately 0.3950227733. The accompanying Python/JSON evaluates these exact formulas down to delta=10^-12. It is a sanity calculation, not a native-code simulation.

This example retains ground-level logical degeneracy but loses it in an excited ancillary level. It demonstrates why full-spectrum logical degeneracy, not merely a protected ground band, mattered to the exact native Davies proof.

For an encoded native memory, a perturbatively induced dispersive splitting could be exponentially small and still be resolved by a strict Davies limit. The toy proves that continuity of that limit cannot be assumed. It does NOT prove that a specified generic local perturbation of the actual recursive clock Hamiltonian realizes this exact effective mechanism with nonvanishing transition weights. That code-specific binding remains unproved.

## 2. This is an order-of-limits obstruction, not a finite-coupling physical no-go

In the standard weak-coupling limit, microscopic coupling lambda tends to zero and dissipative time is tau=lambda^2 t_physical. Holding any nonzero delta fixed while taking that limit permits arbitrarily long spectral resolution. The secular construction distinguishes the two frequencies. Taking delta to zero afterwards need not recover the generator obtained at delta=0.

At fixed microscopic coupling and fixed physical time, exact Hamiltonian dynamics is continuous. For the SAME initial joint state and H_tot(delta)-H_tot(0)=delta Z_L n_a,

    ||U_delta(t)rho U_delta(t)†-U_0(t)rho U_0(t)†||_1
       <=2 |delta| |t|.

The inequality holds with any finite bath and does not depend on its dimension. If initial Gibbs states are also changed, their initialization difference must be added separately. A small splitting relative to the inverse observation/relaxation time is not automatically physically resolved. Hence the toy does not invalidate the exact finite-bath memory consumer.

A simple CP illustration is to retain cross-frequency terms: at beta=0, replace each two-jump rate matrix by gamma[[1,kappa],[kappa,1]] with kappa=exp[-(delta T)^2], for both upward and downward transitions. It is positive semidefinite, and an initially maximally mixed ancilla gives c(tau)=exp[-gamma(1-kappa)tau]. The induced dephasing tends continuously to zero as delta T tends to zero. This is an illustrative coarse-resolution channel, NOT a derived universal physical bath or a general finite-beta Gibbs-preserving construction.

## 3. General finite-bandwidth / approximate-stationarity consumer

The following elementary bound states the needed admission condition without assuming stationarity that a coarse-grained bath may lack.

Let rho be the actual target Gibbs state, P_bad a decoder bad projector commuting with the exact logical Pauli algebra, p=Tr(P_bad rho), and rho_bar its logical twirl. Put d=||rho_bar-rho||_1. The ideal overwrite output obeys E(xi_L)<=2rho_bar. Let Phi_t=exp(tL) be any CPTP semigroup. Suppose for every logical Pauli Q_mu,

    ||L*(Q_mu)||<=a,
    ||L*(Q_mu)-P_bad L*(Q_mu)P_bad||<=e.

Write d_stat(t)=||Phi_t(rho)-rho||_1. Positivity, contraction and the equal-trace effect bound imply

    p_bad(t)<=2p+d+d_stat(t).

The same reference-duality/Pauli-expansion proof as the previous P2 admission gives

    error(T)<=3a T(2p+d)
                +3a integral_0^T d_stat(t) dt+3eT.                 (A)

It holds with arbitrary entangled logical reference and needs no post-loading product assumption beyond the specified overwrite map. If xi=||L(rho)||_1, then d_stat(t)<=t xi and

    error(T)<=3a T(2p+d)+(3/2)a xi T^2+3eT.                       (B)

If instead an exact stationary state sigma is known with ||sigma-rho||_1<=zeta, then d_stat(t)<=2zeta gives a linear-in-T replacement. These are sufficient estimates, not necessary memory criteria.

A finite-time-filtered local contact is quasi-local by real-time locality bounds. Truncating at radius R can supply e_R from its tail, provided the good sector protects the FULL truncated jump algebra, including J†J and coherent correction terms. One also needs a rare-bad estimate p_R for that enlarged support. The original constant-support witness bound does not automatically cover growing R. Both tail norm and strength sums must be charged without multiplying by a fictitious number of individual Bohr frequencies.

Thus an exactly Gibbs-stationary, quasi-local finite-bandwidth generator with stretched-exponentially small p_R, d and e_R would give a positive memory theorem through (A). An approximately thermal physical generator can also qualify if its actual stationarity/admission error has the necessary size. But a fixed small xi or zeta, justified only by weak coupling, does not by itself establish exponential-time retention through these bounds. This is a limitation of that proof transfer, not proof that the physical bath destroys the memory.

## 4. Exact finite-bath consumer: no frequency resolution or GKSL approximation

Let H_nat,0 be the exactly dressed native clock model. Append finite bounded-spin bath degrees of freedom and write

    H_tot = H_nat,0 + H_B + V.

Here V contains generic local native imperfections and memory–bath couplings; terms wholly on the external bath commute with native logical operators and can be placed in H_B. U acts only on data and internal clocks. Let Q_mu be the native dressed DECODED logicals and P_good their constant-support protection projector. Because finite-depth conjugation preserves bounded data footprints, arbitrary bounded-support imperfections have

    [Q_mu,V_X]P_good=0

once the bad set protects the full corresponding local data algebra. No symmetry of V is assumed. The reference H_nat,0 commutes with all Q_mu exactly, and H_B does too.

Assume, as a NEW STATIC INPUT, that the ACTUAL total interacting Gibbs state has

    p=Tr(P_bad exp(-beta H_tot)/Z)
          <=poly(n) exp(-c n^eta)

uniformly in allowed perturbations and finite external-bath volume. This is NOT supplied by the exact unperturbed excursion calculation, the ground gap or the toy bath analysis.

Let v n bound the norm sum of the noncommuting terms touching the native memory/clock region. Pure external-bath terms never enter that sum. Two-sided local logical protection gives

    Q_mu H_tot Q_mu-H_tot=P_bad(... )P_bad,
    ||Q_mu H_tot Q_mu-H_tot||<=2vn.

The exact Gibbs relative-entropy identity and Pinsker then imply

    d=||rho_bar-rho||_1<=2 sqrt(beta vn p).

Initialize the actual interacting Gibbs state and overwrite its decoded logical subsystem, using the native finite-depth dressing and the fixed data decoder at ideal endpoints. This preserves its actual gauge/internal-clock/external-bath marginal; it is not factorized-bath initialization. Exact unitary evolution under the SAME H_tot is stationary on rho, and i[H_tot,Q_mu] is bad-supported with norm <=2vn. Therefore

    error(T)<=6vnT[2p+2sqrt(beta vn p)].                          (C)

This is physical Hamiltonian time. It is the earlier exact-H spin-bath/approximate-twirl consumer applied to a different reference Hamiltonian, not a new theorem about the native thermal state. No finite bandwidth, level spacing, Davies limit, bath mixing or runtime control is required. Uniform finite-volume estimates can pass to local thermodynamic limits as before.

The native system includes its fixed-dimensional clocks; encoding/decoding may access these internal ancillas, not the external environment. Generic noisy loading, efficient equilibration and inaccessible-clock endpoints remain separate. The dynamics argument itself could accommodate broader baths if the static premise were earned, but the previously controlled weak bounded-spin class is the honest concrete target. Unbounded continuum reservoirs require additional mathematical control.

This exact consumer is stronger than a finite-order Markov approximation for the specified equilibrium-initialized physical task: it has no accumulated bath-model error. It does not settle whether the native perturbed joint Gibbs witness estimate is true. That is the decisive next native robustness gate.

## 5. Strong primary comparisons, without confusing thermostats with material baths

- **Nathan–Rudner ULE:** the 2020 construction avoids assumptions on system level spacings, with Markov error governed by bath correlation/relaxation scales. Their response explicitly states that the bare Gibbs state is not generically an exact stationary state. Thus it addresses spectral-resolution fragility but does not supply the missing rare-bad stationary ensemble. Sources: https://arxiv.org/abs/2004.01469 and https://arxiv.org/abs/2011.04574 .

- **Trushechkin unified GKLS:** a rigorous weak-coupling treatment retaining relevant near-degenerate nonsecular effects is an established alternative to indiscriminate full secularization. It is still a specified weak-coupling limit, not a uniform arbitrary finite-coupling/exponential-time native-memory theorem. Source: https://arxiv.org/abs/2103.12042 .

- **Exact quasi-local Gibbs thermostats:** Chen–Kastoryano–Gilyen give exact Gibbs detailed balance with finite-resolution quasi-local constructions; Ding–Li–Lin supply a broader finite-jump KMS family. These can serve the exactly stationary side of (A), if their actual quasi-local tails and native witness enlargement are bound. They are Hamiltonian-dependent designed thermostats, not automatically a fixed material reservoir insensitive to unknown calibration. Sources: https://arxiv.org/abs/2311.09207 and https://arxiv.org/abs/2404.05998 .

- **Current finite-coupling repeated-interaction comparator:** Wang–Ding v4 (September 2026) controls all-order system-bath channels with coupling independent of target precision. The protocol refreshes ancillas, samples bath frequencies and uses time-modulated Gaussian contacts. Its thermal fixed-point bound has a beta*t_mix/sigma contribution; attaining error epsilon requires width of order beta*t_mix/epsilon in the displayed theorem, not merely logarithmic width. Consequently it does not freely provide a fixed-bandwidth passive native bath with exponentially accurate admission. Source inspected: https://arxiv.org/html/2512.03457v4 , Theorem 1/Eq. (4), and model Eqs. (2)–(3).

- **Recent weak-coupling collision analysis:** Ong–Parameswaran–Placke–Hahn obtain rigorous coupling-dependent fixed-point errors for resettable, time-controlled bath protocols. That is valuable implementation progress, but a fixed small Gibbs approximation error is not the required uniform rare-event certificate. Source: https://arxiv.org/abs/2605.03011 and https://journals.aps.org/pra/abstract/10.1103/25wc-17zy .

These comparisons support neither a generic no-go nor a claim that bath engineering is impossible. They identify distinct resource contracts and missing error terms. The exact finite-bath route presently avoids the secular discontinuity most directly, but only after earning the actual native perturbed thermal witness and retaining correlated equilibrium initialization.

## Decision / next proof target

1. Reject continuity-based extension of the EXACT native Davies result to arbitrary small symmetry-breaking imperfections: the minimal local counterexample disproves that reasoning.
2. Do not reinterpret the Davies discontinuity as a finite-coupling physical memory failure for the actual code.
3. Prefer the exact joint-equilibrium consumer (C) for a passive physical robustness theorem; pursue the native perturbed joint Gibbs witness as the hard missing input.
4. If using a coarse-grained/ULE/engineered thermostat instead, explicitly earn the stationarity or invariant-ensemble admission and full local logical-algebra tail required by (A); approximate Gibbs stationarity cannot be silently promoted to exact stationarity.

Only primary public research pages were consulted; no external contacts/actions occurred. The new thermal robustness premise remains unproved.
