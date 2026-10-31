# Independent shared-spectator guard-extension review

31 October 2026. **Scoped mathematical PASS** after full read of `SHARED_SPECTATOR_GUARD_EXTENSION.md`, SHA-256 `00cc9b0608b0f60bd73b3a99888759215a26104e722eac4e52320d036a2609cf`. The previously frozen occupation proof, resource corollary and executable compiler are unchanged. This is a conditional operator-valued corollary, not a physical guard construction or an automatic extension of the executable grammar.

## Operator inequality and transport

On the guard one-excitation block, i[H_ij,V_u] is Hermitian with off-diagonal operator X of norm at most t_ij|u_i-u_j| times the positive exterior guard weight. The elementary bound [[0,X],[X^dagger,0]]<=||X||I follows by Cauchy--Schwarz on arbitrary spectator-entangled vectors. The exterior weight acts on other guard registers and commutes with X. The stated right side is t_ij(u_i+u_j) times that weight on the one-excitation block, and is nonnegative on the double-excitation block where the commutator vanishes. Thus the scalar edge proof extends exactly, without requiring different T_ij operators to commute or factorizing spectator states.

All real number-controlled A_li terms and guard-independent Delta_l terms commute with V_u despite arbitrary noncommutation on the spectator. Their complexified imaginary parts are bounded by the displayed 2Rc occupation term and 2R||Delta_l|| scalar term. Intended operations remain system-only. Shared spectator access does not relax the actual system patch, controller-support, or source-incidence conditions.

## Backward weight and common dilation

The backward physical-time ODE has linear part -lambda I+diag(sum_j t_ij)+(t_ij), with both row and column sums at most -gamma lambda. For v_i=2Rc on selected active incidences, the first u_i=1 boundary derivative is at most -gamma lambda+4Rc<0 under the proposed radius cap. The same positive comparison and column-sum convolution yield initial and integrated sums 4Rcg|S|/(gamma lambda) and 4Rcg|S|tau/(gamma lambda). Loss and injection bounds are unchanged.

Consequently the squared common-history operator norm has exactly the stated exponent. Taking its square root and applying the multivariate Cauchy kernels yields exp(Rh)/(R-1) with h=2cg(1+a tau)/(gamma lambda)+epsilon_ctl. The optimized constants are therefore those of the separately reviewed physical-unit corollary, with no additional spectator dimension, bandwidth or correlation-time factor.

The jump-record output space and phases must be the same for all z. E is retained, not traced out before subtraction. The bound is on arbitrary G/S/E/reference inputs with the specified Markov loss/injection fields initialized. It is not the norm of an arbitrary full unitary extension on unrestricted incoming fields. The ordinary inclusive fault-amplitude/linearity receiver remains conditional on its real code/gadget/control premises, as in the earlier review. This is not a Pauli probability or a source-state preparation theorem.

## Infinite-dimensional qualification

For finite E, bounded measurable time-dependent coefficients suffice; large finite ||H_E|| does not enter the weight bound because H_E commutes with V_u. For infinite E, the supplied strongly continuous unitary propagator for H_E and uniformly bounded, suitably strongly measurable remaining coefficients are genuine domain/existence premises. In that interaction picture, the latter retain their norms and the guard weight. Bounded time-ordered perturbation series and bounded finite-guard jump operators give compact-z summable sector majorants and operator-norm analyticity. No unknown unbounded time-dependent generator is declared well posed by notation.

In particular the phrase 'arbitrarily large guard/bath terms commuting with n_i' means finite bounded coefficients in this stated infinite-E receiving, unless a further commuting propagator/domain construction is separately acquired. Unbounded T_ij or A_li are excluded. No computational oracle for the spectator propagator is claimed or required for this physical uniform estimate; actual physical realization remains outside the proof.

## Transparent sector, obstruction and illustrative qutrit

If I_G tensor B is invertible, it has no kernel. Unitary conjugation cannot produce an operator Q_G tensor C with a nonzero transparent P_G kernel. This elementary obstruction rules out obtaining the stipulated guard merely by a passive relabeling of that full-rank interaction. It is not a no-go for engineered dissipation, error correction, changed decompositions or approximate decoupling.

The unguarded c Z_S tensor Z_E example is decisive within its stated scope: with E in a Z eigenstate, time pi/(2c) produces a system Z up to phase regardless of lambda. Its integrated residual norm is pi/2, so the guard theorem cannot admit it by increasing an unrelated guard loss. Omitting the term would change the declared model.

A common kernel of the Hermitian B_alpha makes their action zero on that sector and removes off-diagonal blocks by Hermiticity. It is therefore a sufficient known-model transparent sector. It does not identify physical model truth from a covariance or small expectation. A guard-creating residual fails to commute with V_u; its unselected real part must be charged in a new activation/generator inequality, not hidden in epsilon_ctl.

For the qutrit example, the two losses have combined adjoint action -lambda Q, while sqrt(a)|2><0| contributes a u|0><0|<=a uV. Block-diagonal guard/spectator Hamiltonians commute with Q. Hence the one-cell mixed transparent-sector example is correct without preparing a pure state inside P. The phrase 'a family with admitted transport' must mean that an appropriate edge inequality is independently checked for that family; arbitrary qutrit transport is not automatically covered by the qubit hopping grammar.

## Scope of the consequence

The useful conditional information saving is real: acquired local guard/transport/injection norm inequalities suffice without reconstructing the spectator state or spectrum. This does not supply those inequalities for an unknown apparatus, convert a generic full-rank coupling into a guarded one, or prove rate feasibility. Ordinary non-Markovian fault-tolerance receivers already permit shared baths; the accepted content here is this particular guarded microscopic admission, not novelty from arbitrary memory. This review does not independently reopen every prior-work citation or historical internal source in Section 7.

Verdict: accept the stated bounded operator-valued corollary and its explicit domain/input restrictions. No hardware acquisition, arbitrary incoming-field guarantee, fixed-diffusion extension, threshold number, practical advantage or executable-compiler promotion follows.

## Final source-only comparison binding

The author appended an explicitly abstract-scoped leakage-removal comparator paragraph after the initial full read. I read the addition and verified the final source, 13,913 bytes, SHA-256 `0d40d350b57ba6e98548e1f345dd2191a5985c2c5a2ebb58036ec3127a12a2ab`. It changes no equation or receiving premise and explicitly distinguishes guard occupation from data-qubit leakage. The mathematical PASS binds this version. I have not independently converted the newly cited abstracts into full-body hardware/resource comparisons; the author's limited comparison scope remains explicit.
