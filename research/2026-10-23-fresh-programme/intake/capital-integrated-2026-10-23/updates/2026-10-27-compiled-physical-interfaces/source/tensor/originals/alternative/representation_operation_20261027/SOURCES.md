# Primary sources, comparator and attribution

The bounded prior search supports the scope distinctions here. It does not
establish historical priority or absence of an equivalent prior algorithm.
Primary works are credited for their established ingredients; the completed
operation is not presented as a new free-fermion tractability class.

| Primary source | Relevant operation and boundary |
|---|---|
| Cai and Lu, *Holographic algorithms: From art to science*, JCSS 77 (2011), [DOI](https://doi.org/10.1016/j.jcss.2010.06.005), [ECCC TR06-145](https://eccc.weizmann.ac.il/report/2006/145/download) | Basis recognition is an existing computational operation. Section 3.2/Theorem 3.1 treats a common basis; bounded-arity nonsymmetric common-basis recognition must also receive a strong comparison. A comparison with only a supplied-gauge FKT evaluator would be too weak. |
| Morton, *Pfaffian Circuits*, [arXiv:1101.0129](https://arxiv.org/html/1101.0129) | Heterogeneous Pfaffian contraction is established. Theorem 6.4 realizes individual ternary tensors under free basis change; the following compatibility obligation across a circuit remains essential. Individual ternary realizability does not by itself acquire compatible network bases. |
| Margulies and Morton, *Polynomial-time solvable #CSP problems via algebraic models and Pfaffian circuits*, [arXiv:1311.4066](https://arxiv.org/html/1311.4066), [DOI](https://doi.org/10.1016/j.jsc.2015.06.008) | Heterogeneous gauge discovery using linked polynomial ideals/Groebner methods is a real raw-input competitor. Its reported computations on different systems are not a matched timing baseline for this construction. |
| Chertkov, Chernyak and Teodorescu, *Belief propagation and loop series on planar graphs*, [arXiv:0802.3950](https://arxiv.org/html/0802.3950) | Section 3 already describes gauge-generated tractable planar models and BP/triple-vanishing equations. Gauge replacement and loop/Pfaffian evaluation are not new here. |
| Chernyak and Chertkov, *Planar Graphical Models Which Are Easy*, [arXiv:0902.0320v5](https://arxiv.org/html/0902.0320v5) | The Wick/free-fermion orbit under arbitrary paired inverse local gauges is established. The inspected statements do not supply the identical complete raw-rational generic bit pipeline, but that observation is not a priority proof. |
| De Lathauwer, De Moor and Vandewalle (2004), [DOI](https://doi.org/10.1137/S089547980139786X); De Lathauwer (2006), [DOI](https://doi.org/10.1137/040608830) | Simultaneous diagonalization/pencil methods for CP decomposition are longstanding. The constant-size pencil step is reused, not claimed as a new tensor factorization theorem. |
| Rosser and Schoenfeld (1962), [DOI](https://doi.org/10.1215/ijm/1255631807) | Standard nth-prime bounds justify that polynomially many small-prime candidates have polynomial numeric sizes. Trial division and deterministic root/nonresidue setup are then charged in the expanded input bit length. |

A current software comparator inspected during the attack was
[holant-tools theory documentation](https://raw.githubusercontent.com/pcoz/holant-tools/main/docs/holant-tools-theory.md).
Its documented recognition interface uses one common basis and nonsymmetric
bounded-arity tensors. Its implementation notes include parity-branch
enumeration but refer to a polynomial paper algorithm; no advantage is claimed
by choosing that weaker implementation as the baseline. The documentation is
not used as a proof of this construction. No holant-tools timing comparison was
performed.

## Same-input ordinary comparison

The ordinary alternative receives the same exact coefficients, supplied
embedding, complete prior theory, any generated-case decomposition and all
retained work. It may use heterogeneous polynomial-ideal recognition,
common-basis recognition where applicable, tensor/pencil methods and the same
Fisher/FKT/CRT primitives. It need not expand a characteristic-zero compositum;
it can reuse the local criterion and finite-field proof as soon as available.
Consequently avoiding that compositum is a completed operation, not an
established advantage over the strongest equally informed ordinary solver.
No practical or acquisition-cost comparison was measured on an independently
useful workload.

## Independent contributions within this run

The parent `/root` proposed the rational determinant-quadratic reduction
`q_(w,e)` which removes neighboring fields from each local balance test,
checked odd-component cancellation, supplied the simple Fisher normalization
and reference matching sign, and derived/checked the original-bit insertion
projection including the scalar-prefactor derivative. These are substantive
mathematical contributions, not just fixture review.

The independent ordinary-comparator worker `/root/hidden_representation_comparator`
supplied the parity-involution necessity proof, the Frobenius/component-scale
lemma proving Fp2 suffices for edge square roots, deterministic bit accounting,
and an explicit standard Fisher/orientation/Pfaffian backend. The evaluator
pattern in `fisher.py` is adapted from that backend with credit; it adds port-ID
and disconnected-component integration rather than claiming a new FKT method.
Its source at review was SHA256
`6190ab081e28e6a6620c72fff3406749d49012541c814beae185c5b117bae21f`.

This worker developed the raw-input compiler contract and integration: exact
local CP recovery/receipts, split-etale admission, common-Fp2 checked
symmetrization and root-sign solve, port embedding, original-basis insertion
transport, separate partition/pin CRT, zero-partition behavior, original-input
height and executable interface. These contributions form one jointly checked
construction; priority is not assigned by who first implemented a fixture.

The parent completed an independent whole-math and whole-code review, exact
original-edge enumeration, separate insertion checks, and independent rational
parallel-edge/disconnected fixtures. Its actual scoped acceptance and five
source hashes are frozen in `review/`. No default external audit is pending at
that accepted internal scope; novelty, useful-workload advantage and physical
application remain separate, unestablished claims.

## Bounded Astra lookup

The current task-first Astra interface was selectively read at commit
`98c726d67f8da34f2893203fa9ae23960d7fd35c`.
Connected repository searches for Pfaffian/Ising returned no relevant packet,
and the current retrieval interface was read to check the lookup contract.
This is only a bounded retrieval fact: it does not prove corpus absence or
novelty. No accepted Astra theorem is silently transferred into this operation,
and no protected or frozen producer folder was edited.
