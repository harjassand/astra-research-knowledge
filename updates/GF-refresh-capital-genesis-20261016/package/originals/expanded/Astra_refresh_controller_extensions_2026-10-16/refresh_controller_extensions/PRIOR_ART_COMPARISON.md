# Targeted prior-art comparison: causal parity-refresh bounds

Date: 2026-10-16

## Conclusion and coverage

The all-pass product mechanism is directly inherited from Gutoski–Watrous. The substantive priority question is the Hamiltonian-to-independent-private-tester reduction, together with its exact local values. This bounded investigation inspected the relevant statements and arguments in **six primary papers**, listed below. It did not identify an exact matching statement in those inspected results. That is not a historical absence claim, an exhaustive literature review, or a novelty rating.

The statements being compared are: the sharp ideal-refresh endpoint-effect bound with factors Q_i = 1 − ∏_k cos²(min(a_ik, π/2)); the sharp two-gap partial-dephasing factors F; and the conditional finite-window private-random-Z certificate R. The latter is a bound, not an asserted exact finite-window optimum.

Three attribution points matter:

- Exact preservation of fractional-query action under Trotter approximation is explicit in Cleve et al. The overhead in their subsequent full-query simulation must not obscure that intermediate result.
- Local non-Markovian fault-tolerance analysis bounds **sums of fault paths**, not merely individual histories.
- Older Zeno work explicitly distinguishes endpoint occupation after nonselective measurements from selected survival at every measurement.

Page references below use the printed manuscript pagination unless otherwise noted. For the four-page AKP journal article, page numbers are article-page numbers 050504-1 through 050504-4.

## 1. Gutoski–Watrous: exact causal domination and all-pass products

G. Gutoski and J. Watrous, *Toward a General Theory of Quantum Games* (2007).

Primary source: https://cs.uwaterloo.ca/~watrous/Papers/GeneralTheoryQuantumGames.pdf

**Locator:** Theorem 9, printed p. 13, proof p. 14; Theorem 6, p. 10, with its equivalent trace constraints and Corollaries 7–8 on p. 12.

Theorem 9 identifies maximum forcing probability with the least p for which the positive outcome operator is dominated by p times a normalized strategy. Its co-strategy counterpart is explicit. Tensoring normalized causal operators and positive inequalities immediately gives exact multiplicativity for independent all-pass tests, even against a joint adversary with memory.

Asynchronous private operations do not obstruct this corollary: local testers can be padded into a common sequence of communication rounds. Specified imperfect local channels can also be part of each tester. Thus general independent-tester multiplicativity is established mathematics.

The missing application premise is that the interacting Hamiltonian process admits the required independent testers. GW does not supply the parity-private copy-message interface, its universal parity-preservation property, or an unchanged-action simulation of arbitrary own-odd generators. Those steps, together with singleton bounds, are necessary to infer the physical product-Q or product-F result.

## 2. Cleve et al.: action-preserving continuous-to-fractional simulation

R. Cleve, D. Gottesman, M. Mosca, R. D. Somma, and D. L. Yonge-Mallo, *Efficient discrete-time simulations of continuous-time quantum query algorithms*, arXiv:0811.4428 (2008; STOC 2009).

Primary source: https://arxiv.org/pdf/0811.4428

**Locator:** Theorem 1, p. 2; fractional-query definition Eq. (7), p. 3; §II.A, pp. 4–5, Eqs. (8)–(14).

Section II.A approximates continuous evolution by fractional queries while preserving total fractional query cost T/π. It permits a time-dependent driving Hamiltonian with an integrable norm envelope. Accuracy improves with the slicing; the later full-query conversion has overhead. Exact-action Trotter passage should therefore be attributed as established methodology.

The interface differs. A fixed oracle Hamiltonian with input-independent driving operations does not itself provide private parity registers, arbitrary bath-dependent own-odd contractions, inaccessible refresh records, or separately budgeted asynchronous gaps. Applying this methodology requires the parity-specific contraction decomposition and control-interface reduction. The query-simulation theorem alone is not a parameter-substitution proof of the parity endpoint bound.

## 3. Lee–Roland: strong query direct products

T. Lee and J. Roland, *A strong direct product theorem for quantum query complexity*, arXiv:1104.4468 (2011; CCC 2012).

Primary source: https://arxiv.org/pdf/1104.4468

**Locator:** Theorem 1.1, pp. 2–3; state-generation formulation, §2; threshold direct product Theorem 5.5, p. 16.

Theorem 1.1 gives exponentially small joint success when many instances are computed with insufficient total query complexity. The work also covers state generation and XOR/threshold variants. It is substantive joint-success prior art.

Its resource and conclusion differ: a global query budget and constant-factor direct-product estimates are not exact multiplicativity at individually specified local action budgets. Arbitrary algorithmic workspace is already allowed, so large bath dimension alone does not distinguish the parity result. The theorem does not directly specialize to Q, F, private refreshes, or finite-controller R without an additional reduction establishing those structures.

## 4. Aharonov–Kitaev–Preskill: correlated fault-path sums

D. Aharonov, A. Kitaev, and J. Preskill, *Fault-Tolerant Quantum Computation with Long-Range Correlated Noise*, Physical Review Letters **96**, 050504 (2006).

Primary source: https://preskill.caltech.edu/pubs/preskill-2006-long-range.pdf

**Locator:** Hamiltonian/noise definitions, Eqs. (1)–(6), pp. 050504-1–2; short-range fault-path bound Eq. (9), p. 050504-2; long-range effective noise strength Eq. (24), p. 050504-4.

Equation (9) bounds the norm of the **sum** of all fault paths having faults at every specified location, with unrestricted faults elsewhere: ‖E(I_r)‖ ≤ ε^r. The bath Hamiltonian is unrestricted. Long-range pair interactions yield a different effective noise-strength estimate.

This already controls coherent shared-bath correlations through dimension-independent norm estimates. However, it is a fault-amplitude/support certificate, not a sharp nonselective endpoint-effect product ∏Q_i; squaring or summing it does not automatically recover that expression. Its physical support condition also differs from a parity selection rule. An own-odd/other-even term may depend on all other parity labels while preserving them, and need not have the local physical support used in the short-range argument.

## 5. Facchi–Pascazio: nonselective histories and Zeno limits

P. Facchi and S. Pascazio, *Quantum Zeno subspaces and dynamical superselection rules*, arXiv:quant-ph/0207030 (2002).

Primary source: https://arxiv.org/pdf/quant-ph/0207030

**Locator:** §4.2, pp. 7–9; nonselective dynamics Eqs. (27)–(31); limiting results Eqs. (32)–(37). The endpoint-repopulation versus selected-survival distinction is discussed on p. 9 immediately before §5.

The finite-N nonselective expression sums measurement histories. The authors explicitly distinguish leaving and repopulating a sector from surviving every selected measurement. Their no-leakage conclusion is a frequent-measurement limit.

This matches the measurement semantics and prevents an incorrect identification of endpoint probability with one selected history. It does not provide the finite asynchronous coordinatewise sharp product under the stated bounded odd interactions. Its Hilbert-space treatment is not merely a fixed-bath-dimension toy model; that would be an inappropriate distinction.

## 6. Pechen et al.: exact measurement-driven two-level transfer

A. Pechen, N. Il’in, F. Shuang, and H. Rabitz, *Quantum control by von Neumann measurements*, Physical Review A **74**, 052102 (2006), arXiv:quant-ph/0606187.

Primary source: https://arxiv.org/pdf/quant-ph/0606187

**Locator:** §III, pp. 7–10 of the linked manuscript; Bloch-vector product Eq. (5), p. 8; optimum Eq. (6) and optimal observables Eq. (7), p. 9.

This computes exact optimal objectives for two-level systems controlled by a fixed number of nonselective measurements, optimizing the measured observables. The solution is a Bloch-vector product with an explicit cosine-power optimum.

Its control variables differ from a fixed parity channel between two norm-action-limited interaction gaps. The two-level optimization is not a supremum over persistent baths and sink dimensions and does not directly yield F. In the partial-refresh equality construction, c=1 is the simple two-level interference case; an interior optimizer c<1 uses another sink direction. Ancillary dimension is therefore an essential comparison condition, not a cosmetic implementation choice.

## Imperfect channels and finite-window controllers

The six-paper inspection does not establish historical priority for the exact partial-dephasing value F. A decisive comparison must retain all of the following: the full joint channel D_eta ⊗ identity on persistent bath/reference degrees of freedom; inaccessible discarded environment; a fixed node; separate before/after action limits; and optimization over arbitrary finite ancillary dimension. A reduced coherence-decay parameter alone does not specify this contract.

For R, the projective-angle perturbation estimate is standard geometric comparison. The specific application also needs the private-controller reduction: deleting concurrent own-odd interaction must expose the stipulated dephasing channel without informing the prover of the sampled phase. All concurrent odd action remains charged. A generic finite-pulse or Zeno-control result does not by itself certify that information boundary.

Fixed schedules and private random variables are separate assumptions. Schedules/envelopes must be exogenous; local refresh environments or controller samples must factor as specified. Conditioning on an external clock is legitimate only if the conditional control contract retains the needed independence. No unconditional product of averaged factors is implied.

Generic screening additionally surfaced switchable-Markovian-noise state-transfer and continuous partial-measurement papers, but these were not expanded into further full-paper reviews and are not used to support an exclusion claim. The relevant leads are https://arxiv.org/abs/1605.06473 and https://arxiv.org/abs/2006.13970. Their stated noise/control models differ; any closer comparison would require a separate bounded investigation.

## Exact unresolved priority gate

A decisive earlier source must establish either the same finite-action endpoint bound under matching assumptions, or a general theorem with an explicit specialization supplying:

1. The private-copy parity-preserving interface, including preservation under every unrestricted prover strategy.
2. Simulation of arbitrary admissible own-odd interactions without increasing any individual gap action.
3. Arbitrary finite shared bath/reference, inaccessible local measurement records and noise environments, and fixed asynchronous schedules.
4. For F, the piecewise two-gap optimum with ancillary/sink assistance and the stipulated full-joint partial-dephasing channel.
5. For R, private sample-independent controls while concurrent odd interaction remains active and fully charged.

The defensible attribution is therefore: established causal product theorem; established simulation and geometric ingredients; supplied parity-specific reduction and singleton computations. Historical priority of that precise reduction remains unresolved by this six-paper check.
