# Independent boundary review: small mean-square strength is insufficient

2026-10-30. Reviewed initial `MEAN_STRENGTH_IS_NOT_ENOUGH.md`, SHA-256 `77012fc6ba80d1a7de71500cdf4eabeb0b62df44cb730d1973800fedebb63fec`, and final channel-scope-clarified version SHA-256 `b54dabbc3498d16a8f778eb16d6984bb0e309a5f134b74fc166b8741bdd56d0c`. Both exact versions are preserved in `reviewed_sources/`. The final diff correctly restricts the Duhamel comparison to system, finite apparatus and reference; it grants no arbitrary coherently retained reset-reservoir output.

## Verdict

**The rare common-bath logical-Pauli pulse is a valid scope counterexample.** Its fixed-small per-site mean-square coupling coexists with a polynomial logical error, and thus cannot support the stated uniform exponential-in-N memory guarantee. The reference/decoder and rare-branch weighting are rigorous with the comparisons below. It does not contradict the bounded-joint-norm theorem and is not a novelty claim.

Two precisions: (1) the `O(p_N N/A_N)` comparison keeps the no-pulse nominal branch **exact**; replacing nominal decoded evolution by identity adds its exponentially small error; (2) the stated bounded-generator Duhamel estimate covers the finite DATA/controller channel and any explicitly included reference or bounded-generator classical record system. It does not by itself prove the same estimate for an arbitrary coherently retained Stinespring output. Reset records are unnecessary for this counterexample.

## 1. Exact pulse and moment budget

Choose a nontrivial Hermitian logical Pauli with physical tensor representative

    L_phys=product_(i in S) P_i,

where each P_i is a nonidentity onsite Pauli, acting on distinct sites. Set a static bath bit initially to

    sigma_B=(1-p)|0><0|+p|1><1|,

independently of every logical/reference input. Take bath-only Hamiltonian zero, and let nominal apparatus dynamics act trivially on this bit. During `[0,tau]`, add

    H_noise=A |1><1|_B tensor sum_(i in S) P_i,
    tau=pi/(2A).

Because the onsite P_i commute,

    exp(-i A tau sum_i P_i)=(-i)^|S| L_phys.

Thus the bath-1 noise-only pulse is exactly Ad_L; bath-0 is identity. The bath bit is conserved, including during nominal evolution, so the branch probability stays p. Each affected site's coupling-square expectation equals `p A^2` throughout the pulse. With

    A=N^2,   p=eta^2/N^4,

this is exactly eta^2, while mean absolute coupling is `p A=eta^2/N^2`. Outside the pulse both vanish. If strength is defined using the conditional commutator-generator norm rather than Hamiltonian amplitude, a fixed factor of two is absorbed by rescaling p; the conclusion is unchanged.

The peak local joint interaction norm is A and grows with N. The support of each system/bath term is only one physical system site; correlations arise through the shared bath bit. This is why bounded system support or an average moment alone cannot replace the incident joint-norm hypothesis.

## 2. Keep the unpulsed branch exact

Let J encode DATA and initialize all controller auxiliaries ready; let D be the prescribed final frame inverse and ideal mathematical decoder. Let M_t be the noiseless nominal DATA/controller semigroup, and write

    C_t=D M_t J.

For time-dependent nominal dynamics use the analogous two-time notation. The accepted nominal memory result supplies a uniform decoded bound

    ||C_t-id_L||_diamond <=delta_N(t),
    delta_N(t)<=C N^(3/2)t exp(-cN).

Let R_tau be the actual conditional bath-1 evolution during the pulse, including the nominal apparatus generator. If its nominal completely bounded/predual diamond generator norm is at most `C_gen N`, Duhamel compares it to the strong noise-only unitary without any factor depending on A:

    ||R_tau-Ad_Lphys||_diamond
       <=C_gen N tau = C' N/A.                     (2.1)

This uses contractivity of both intervening physical propagators, not a perturbative series in the strong Hamiltonian.

For any final time T>=tau after the noise has been switched off, the actual decoded channel is

    Phi_T=(1-p) C_T + p D M_(T-tau) R_tau J.

Compare first to

    Psi_T=(1-p) C_T + p C_(T-tau) Ad_Llogical.

The identification in the second branch is exact: `Ad_Lphys J=J Ad_Llogical`, since the ideal pulse maps the code space to itself and leaves ready auxiliaries unchanged. Hence

    ||Phi_T-Psi_T||_diamond <=p C' N/A.              (2.2)

Subsequent nominal CPTP evolution and D cannot increase this discrepancy. No claim that the controller exactly commutes with every physical representative of L is required. Its accepted preservation of arbitrary encoded logical inputs is sufficient.

Replacing both C channels by identity costs

    ||Psi_T-[(1-p)id_L+p Ad_Llogical]||_diamond
       <=(1-p)delta_N(T)+p delta_N(T-tau)
       <=delta_N(T).                               (2.3)

Thus the unweighted nominal error is exponential, while the pulse-approximation error is correctly weighted by p. It would be wrong to approximate the entire actual channel directly by the noise-only mixture and silently drop an unweighted nominal-comparison error.

## 3. Explicit reference/decoder lower bound

For a nontrivial logical Pauli, `Tr L_logical=0`. Apply the channel to a maximally entangled logical/reference state. Its L-transformed state is orthogonal to the original, so

    ||Ad_Llogical-id_L||_diamond=2,
    ||[(1-p)id_L+p Ad_Llogical]-id_L||_diamond=2p.

The reverse triangle inequality and (2.2)-(2.3) give

    ||Phi_T-id_L||_diamond
       >=2p-delta_N(T)-C' p N/A.                   (3.1)

For every fixed positive T, eventually tau<T, and with `A=N^2`, `p=eta^2/N^4`,

    ||Phi_T-id_L||_diamond
       >=(2-O(1/N)) eta^2/N^4-delta_N(T)
       =(2-o(1)) eta^2/N^4.

Equivalently the trace-distance error on that witness is asymptotic to p. A pure logical input orthogonal to its Pauli transform supplies a witness without a reference as well.

This is incompatible with a uniform exponential-in-N decoded bound based solely on the pointwise mean-square condition. Merely saying that subsequent CPTP dynamics cannot amplify error would not establish persistence of a lower bound: CPTP maps can erase distinctions. Here persistence is instead established by the controller's nominal preservation of *both* legitimate encoded logical inputs, quantitatively through (2.3).

## 4. Reset-record qualification

The proof needs the reduced DATA/controller generator bound in (2.1), with arbitrary external reference amplification. There is no need to grant the final decoder access to bath bits or emitted reset records. If classical reset records are included via a physical marked-jump generator with the same O(N) norm budget, (2.1) remains valid on that extended channel.

An arbitrary coherent Stinespring output is a different comparison. In general a jump of probability O(tau) changes a coherent dilation by trace distance O(sqrt(tau)), although the reduced channel changes by O(tau). Therefore the reduced-generator norm premise alone does not justify the phrase “including any reset records” in this stronger sense. One can omit that phrase, explicitly restrict the record model, or separately prove the stronger dilation estimate from the actual all-ready/dark-state architecture. Even a weaker relative error O(sqrt(N/A)) would still tend to zero for A=N^2 and would leave (3.1)'s polynomial obstruction intact.

## Final scope

This is a finite-dimensional classical shared-bath counterexample family with initially independent bath state, onsite system supports, finite pulse duration, and a legitimate Hamiltonian perturbation. It disproves substituting only a mean-square/mean-strength bound for the theorem's uniform joint norm budget. It does not disprove exponential protection under additional tail bounds, bath dynamical restrictions, or other explicitly earned hypotheses. No unbounded-bath existence issue, priority assertion, or new physical implementation is needed.
