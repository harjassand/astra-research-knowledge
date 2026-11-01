# Comparison at the complete-operation interface

The comparison is to the **same acquired passive Gaussian memory**, actual controlled system circuits, initial retained vacuum, horizon `T`, complete-channel error `epsilon`, and system/instrument output. The memory remains quantum and is carried through every interval. Acquisition, occupation cutoff, rate/frequency magnitudes, coefficient precision, discarded-field bookkeeping and digital evolution all count. Alternative bath representations are allowed when they independently earn the same output/error contract. None of the comparisons below is a lower bound against every possible refit or reduction.

## What is received and what is proposed

[Huang–Park–Chan–Lin, 2506.10308v2](https://arxiv.org/html/2506.10308v2) supplies the established CP coupled-pseudomode framework, realization construction and mode-count analysis. Its Table 1 is expressly a mode-count comparison. Equations 2–8 and Theorem 1 govern the realization interface. The present proposal uses this machinery; it does not claim to originate coupled physical modes. It contributes a candidate consumer of an actually supplied passive coupled network. The stage-one rational bath is one fully acquired input to that consumer.

N1510 is an already accepted internal result, not newly discovered work. Its final receiver has independent strictly positively damped coordinates and diagonal number frequencies, with actual system encodings supplied. The final source and whole internal review, including the repaired `(-i)^k` phase, are preserved under the stage-one source receipts. Its complete-isometry amplification/private-record algebra is reused at that actual interface. It does not provide the coupled source of this stage; the construction here allows arbitrary Hermitian one-particle mixing and a rank-deficient loss matrix, including a dark mode. Calling its independent-mode source with a dense coupled drift would assume the operation at issue.

## Strong complete coupled-mode consumer

[Chen–Gao–Wang–Zhou, 2609.18757v1](https://arxiv.org/html/2609.18757v1), abstract and Section 1.1, gives query-optimal and gate-efficient general Lindblad simulation with a Hamiltonian block encoding and a projected encoding of the **stacked** jump operator. Its normalized time is `theta=T(alpha_H+alpha_B^2)` and its query bound is

    O(theta + log(1/epsilon)/log[e+log(1/epsilon)/theta]).

Gate overhead is polylogarithmic over that bound; the catalyst is removed by the actual algorithm, not assumed prepared. This is a stronger comparator than a Trotter method or a 2017 generic consumer. For the retained cutoff, the stacked physical jump norm squared is exactly `K||EE^dagger||`. The paper's oracle normalization is at least this norm, irrespective of whether individual loss columns are encoded separately. Its general theorem does not exploit the special one-particle trace clock derived here. This is a comparison of applicable upper bounds, not a special-structure lower bound.

[Wang–Ye, 2609.17490v2](https://arxiv.org/html/2609.17490v2), Eq. 4 and Theorem 19, independently achieves optimal additive normalized-time/precision query scaling and near-optimal gate complexity using transducers and actual catalyst removal. It uses `theta=T(alpha_H+sum alpha_j^2)`; its discussion also permits stacked access. Thus neither additive query scaling nor catalyst-free history compression is new in this proposal. Their normalization continues to contain the loss norm. Their black-box optimality does not prohibit fast processing of the special classically described Gaussian part.

The best ordinary application first removes the **known Gaussian Hamiltonian** in a Hamiltonian interaction picture. One-particle `exp(-iHt)` and second quantization can be implemented from the actual small matrix, with the same paid binary Fock rotations used here. Conjugating the jumps preserves the norm of their stack. Consequently the normalization of the remaining Lindbladian still contains `K||EE^dagger||`. [He et al., 2405.19245v1](https://arxiv.org/html/2405.19245v1), Section 4, Eqs. 80–84 and Theorems 4.2–4.3, implements this Hamiltonian picture; its easy part is explicitly `-i[H1,·]`. It does not provide an inverse dissipative channel. Time derivatives after conjugation enter quadrature precision, which is paid. Its availability removes large **unitary** frequencies as a putative distinction, while leaving the dissipative-clock question.

Writing `C_IP` for the actual cost of the transformed system/stacked-loss circuits, a strong ordinary pipeline has leading cost governed by

    theta_IP = T[h+2a sqrt(K+1)+K||EE^dagger||],
    C_IP * (theta_IP + polylog(1/epsilon)),

with the precise joint precision term supplied by the 2026 theorem and actual Gaussian/unitary/time arithmetic charged. No independent-Lorentzian replacement is made in this comparison.

## Other whole Gaussian-bath pipelines

[Christensen–Agerskov–Nathan, 2509.12717v2](https://arxiv.org/html/2509.12717v2) is a genuine nonperturbative alternative: its ancilla train carries memory and covers arbitrary Gaussian environments and coupling strengths. It is not excluded for being different from a pseudomode representation. Section II.2, Eqs. 32–33, gives ancillary width `O(max[Gamma*tau_b/eta^2, Lambda(eta)*tau_b/eta])` and added gates `O(max[tau_b*T*sqrt(Gamma^3*sdot)/eta^3, Lambda(eta)*tau_b*T*sqrt(Gamma*sdot)/eta^2])`, for its relative-accuracy parameter `eta` and bath scales. Its error budget is converted to the same absolute horizon error before comparison. These are polynomial inverse-accuracy upper bounds; the expressions are not lower bounds against improved train compilation. The present proposal earns a polylogarithmic inverse-accuracy upper bound for the supplied passive finite network and, by composition, the specific stage-one continuum. ATA may have much better constants or horizon dependence.

[Chen–Cai, 2610.29372v1](https://arxiv.org/abs/2610.29372) is another complete nonperturbative alternative, already read in stage one. Sections 3–5 use positive temporal-kernel spectral compression, finite oscillator occupation or dilution, and explicit Hamiltonian circuits. Eq. 22 charges `M_Trot[D_sys+N q d D_int]`; Section 5.2 gives polynomial time/accuracy sufficient scalings under eigenvalue-tail and coupling-derivative assumptions. There is no dissipative rate in this representation. This defeats any suggestion that every complete Gaussian simulator must pay a Lindblad norm. It does not supply this coupled-network loss-clock operation. A low-rank temporal representation with efficiently evaluable couplings can also be combined with stronger Hamiltonian simulation than its second-order Trotter consumer; whenever its acquisition, rank and coupling norms are favorable, that combination must be included as an ordinary competitor. No universal separation from it is established here.

[Huang et al., 2603.25708v1](https://arxiv.org/html/2603.25708v1), conclusion, distinguishes efficient complex exponential approximation from the still-required physical coupled-Lindblad constraints. This stage receives the actually constructed physical passive input, rather than equating a complex exponential fit with an implementable bath or with a cheap evolution algorithm.

## Closely related trajectory constructions and their interfaces

[Li–Wang, 2212.02051v2](https://arxiv.org/html/2212.02051v2), Theorem 11 and its implementation, already uses high-order Duhamel expansion and LCU for channels. Its normalization contains the Hamiltonian and squared jump normalizations. Forward Duhamel, positive quadrature, LCU and complete-isometry amplification are established tools. The proposed addition is the specifically acquired Gaussian contraction block, trace-bounded loss CDF, cross-source convolution and actual count cap that remove the large passive rate from the normalization.

[Peng–Sun–Zhao–Zhou, 2408.10505v2](https://arxiv.org/html/2408.10505v2) already gives trajectory-inspired high-precision Lindbladian simulation. This proposal does not claim to originate trajectory simulation or its near-linear normalized-time, polylogarithmic precision goal. The comparison concerns the actual normalization and available structure of the jump/no-jump source.

[Borras–Marvian, 2509.10425v2](https://arxiv.org/html/2509.10425v2), Eq. 19 and Section 4, exploits `sum L_mu^dagger L_mu=Gamma I`, giving an input-independent exponential waiting clock. The present losses have a vacuum kernel and `sum L_mu^dagger L_mu=dGamma(EE^dagger)`, so they are not scalar on the cutoff. The present envelope is instead computed from the one-particle contraction, and only the **whole** first-event source has input-independent amplification success. It does not assert a state-independent physical waiting distribution.

[Li–Wang, 2111.03240v2](https://arxiv.org/html/2111.03240v2), Section 1.1 and Theorems 2 and 10, has a succinct GQME and polylogarithmic digital precision, but its microscopic model comparison assumes weak coupling and has an `O(lambda^3)` model error. That is not the arbitrary-coupling, arbitrary-inverse-accuracy continuum contract here. Its pole magnitudes are also charged. It remains useful at its actual perturbative scope; it is not dismissed on the basis of its abstract alone.

Asymptotic-preserving reduction is legitimate when an actual error certificate is available. [AlMasri, 2605.18886v1](https://arxiv.org/html/2605.18886v1) analyzes a slow-limit operation with gap/centering and native relaxation or an acquired manifold projection. It does not provide the finite-rate coupled source here. Nor does this absence prove that a specific supplied network cannot be reduced. In the numerical stiffness family below, the fast mode has an analytic eliminable limit; using that sweep as an end-to-end advantage benchmark would therefore be misleading.

I also ran this stronger ordinary comparator. For `A_R=[[0,sqrt(R)],[-sqrt(R),-R]]`, the slow eigenvalue tends to `-1`. A one-mode memory with `A=-1`, `E=sqrt(2)` and the same slow coupling `.12` is compared against the actual two-mode model, using the same noncommuting system Hamiltonian, total horizon `.7`, cutoff `K=2`, and intermediate system rotation. The numerical Choi-derived diamond upper bounds are `.0084062`, `.00246283`, `.000226363` and `.0000226130` for `R=4,40,4000,400000`. The large-rate sweep is therefore not an end-to-end advantage demonstration: an ordinary reduced model already approaches the desired finite output. These are finite channel diagnostics, not a uniform continuum elimination theorem. The raw calculation is `reduction_comparator.py`, with all results saved.

## What the proposed upper bound changes

Put `v=1+h+2a sqrt(K+1)`, `lambda=(aT)^2`, `Jmax=O(lambda+log(1/epsilon))`, `S=O(vT+p+Jmax)`, and `A0=O(sqrt(1+KM))`. The derived bound is

    G_new = O(S A0 {q[O~(M^2 K)+C_D]
                       +poly(M,r,B,input bits)}),
    q=polylog(S A0/epsilon),
    B=polylog(M,K,R,v,T,1/epsilon).

All small-matrix arithmetic, source preparation, Gaussian gates, loss directions and amplification are part of this bound. It has no positive power of `R` from passive rate/frequency magnitude, but may have a large power of `T`, `K` or `M`. The exact output bath is private; arbitrary coherent access to old emitted photons is not promised. Cold-zero and thermal limitations of the first stage are unchanged.

| Complete pipeline | Known structural cost that matters here | Scope of the comparison |
|---|---|---|
| Acquired coupled realization + current query-optimal consumer + Gaussian Hamiltonian picture | Remaining normalization includes `T K||EE^dagger||`; actual transformed circuits and high-precision gates paid | Strong same-network baseline; an upper bound, not a lower bound for this structure |
| Direct ancilla train | Published polynomial inverse-accuracy ancillary width and added gates; bath scales and UV truncation paid | Valid same continuum output; potentially better constants/time dependence |
| Positive temporal-kernel compression + best Hamiltonian consumer | Rank acquisition, eigenvalue tail, accumulated coupling and coherent function access determine cost | Can avoid rate normalization without this primitive; no general separation claimed |
| Certified ordinary bath reduction/refit | Its own finite-horizon complete-channel error, acquisition and subsequent evolution | Must be used whenever it wins; the two-mode sweep alone cannot defeat it |
| Proposed forward-contraction/loss-clock consumer | `S sqrt(KM)` amplifications, explicit Gaussian blocks and prefix CDF arithmetic; only logarithmic rate bits | Candidate broadly reusable stiffness-removal principle; high horizon/cutoff overhead |

For the acquired stage-one reciprocal-dyadic bath, `M=O(log^2(T/epsilon))`, `a` stays bounded, `R=poly(T/epsilon)` and coefficient synthesis is polynomial in logarithmic accuracy parameters. Together with the proved vacuum factorial cutoff, the proposed consumer gives a complete **polylogarithmic inverse-accuracy upper bound at fixed horizon**, provided the actual supplied system-access circuits have at most polynomial logarithmic precision cost. Otherwise their actual `C_D` is retained. Current general consumers on this same realization do not give that bound directly. This is the substantive proposed result. Historical novelty, independent correctness of the entire conjunction and practical crossover remain unestablished. No claimed physical device or experimental speedup follows.
