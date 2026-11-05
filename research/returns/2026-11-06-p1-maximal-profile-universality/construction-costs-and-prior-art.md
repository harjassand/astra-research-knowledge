# Universal construction, full interfaces, prior art and useful failure

The [P1 response](P1_MAXIMAL_PROFILE_UNIVERSALITY_20261106_RETURN.txt) starts from a **supplied channel description and dilation**, not environmental access to an unknown black-box device. For `V: C^a → C^b⊗C^r` dilating `N`, it applies a complementary depolarizing channel `C_p=D_p^c` to the environment: `Ntilde_p=(id_b⊗C_p)∘Ad_V`. The original marginal remains exactly `N`; the complement becomes `D_p∘N^c` with strictly positive Choi matrix for `p>0`. A canonical dilation from `J_N^(1/2)` supplies the separate continuous-embedding statement.

The auxiliary primitive is established work, credited to Leung–Watrous. For nontrivial dimension `d`, its source-reported Gram matrix is `(1−p)|Ω⟩⟨Ω|+(p/d)I`, its exact optimal recovery probability is `p`, and its half-diamond distance to the fixed pure replacer is at most `sqrt(p(1−d^−2))`. At `p=0` the rank structure changes and perfect-profile preservation disappears. The primitive's quadratic recovery cost relative to that distance bound is not an unavoidable universal-extension cost.

The improved extension uses an orthogonal branch flag: `(1−q)Ntilde_p ⊕ q Ad_V`. If the first branch has certified half-diamond error `ζ<ε`, choosing `q=(ε−ζ)/(1−ζ)` gives total error at most `ε` and success at least `q+(1−q)p`. Taking `ζ=ε/2` earns the stated `ε/(2−ε)` bound; smaller `ζ` lets the guarantee approach `ε`. Both branches preserve the exact original marginal and perfect profile. The costs belong to one common construction and parameter choice.

The response reports a general compiler for exact rational-complex Kraus lists or exact rational-complex Choi matrices. Outputs use **weighted rational Kraus terms**, with weights distinguished from amplitudes. Choi input is factored using exact `LDL†` and four rational squares for each positive pivot. The reported finite exhaustive four-square search can be enormous in input bit length; no efficient general factorization or polynomial-time compiler is inferred.

| Resource | Reported contract |
|---|---|
| Source access | Exact matrices or already supplied rational dilation; no inference of discarded-environment access from black-box calls |
| Environment padding | Power-of-two `r<8ab` |
| Rational auxiliary parameters | Integer `m≥r+1`, `c0=(m²−r²+1)/(m²+r²−1)`, `c1=2m/(m²+r²−1)`, `p=r²c1²`; certified half-diamond bound at most `2r/m` |
| Output dimensions | Basic `br²`; improved `b(r²+r)` |
| Dense descriptions | Basic Kraus `O(abr³)` rational entries; basic Choi `(abr²)²` entries |
| Additional tolerance precision | `O(log r+log(1/ε))` coefficient bits, alongside input/factorization costs |
| Recovery and implementation | Paid heralded success and new specimens after failure; physical synthesis/control of the dilation and auxiliary channel required |

The source reports implementations of explicit auxiliary/extension decoders, **without** a generic optimal-SDP solver, ordinary-capacity evaluator or physical realization. It reports exact trace-preservation, all-matrix-unit marginal identity, successful decoder composition, trace-nonincreasing, rank and matching primal/dual certificate checks, covering Kraus/Choi input and genuinely complex rational entries. A reported dimension-12 example has half-diamond bound `1/2` and exhibited success `25091/67081`; a separate auxiliary certificate gives optimum `49/169`. Correlated-reference/two-use numerical discrepancies below `4×10^−12` are convention checks, not proofs of the universal quantifiers. These are source-reported executions; their code/results remain in the held ZIP and were not run or newly verified by Capital.

Prior art is substantive: Hiai–Mosonyi's maximal-divergence equality/multiplicative-domain conditions already distinguish preservation from deterministic reversibility; Oi and Heinosaari–Jivulescu–Reeb–Wolf supply probabilistic reversal/filtering/extension comparators; complementary depolarizing channels are established. Astra N1690 already supplies the nonorthogonal-flag mechanism, its capacity separation and general complete maximal-order evaluator. The proposed addition is the universal extension combined with structural, dimension and optimal recovery-cost theory. No exhaustive world-priority determination is supplied; named original-source comparisons are preserved as reported, without reconstructing unavailable source-ledger links.

The failed route is retained: almost-parallel flags do not uniformly dilute SLD information over all faithful references. With any fixed positive small flag component, ill-conditioned reference states with baseline eigenvalues `s,1−s` can make the encoded SLD quantity tend to the original value `4` as `s→0`. The response gives strictly positive binary-POVM examples. The successful construction instead uses exact maximal-perspective preservation and finite-query diamond control. It claims neither a classification of all Petz-metric orders nor undecidability inside the perfect-profile class.

The earlier joint rounding result retains one common law, fixed-query second moments, edge-length dependence, rational extraction, exact paid original linear optimization and potentially enormous polynomial cost. N752, N675 and N557 retain their scopes. The visible **69m46s** duration is not a complete CPU/memory/spending account. Source reports of no extra workers, physical experiment, outreach, publication or transfer retry are provenance, without new Capital monitoring of the producer. Mathematical explanatory scope does not establish practical scalability, general computational speedup or P versus NP.

[Structure and recovery](structure-and-recovery.md) · [Overview](README.md)
