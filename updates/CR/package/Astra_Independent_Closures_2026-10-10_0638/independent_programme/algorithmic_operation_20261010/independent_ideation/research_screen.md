# Independent computational-operation screen

Date: 2026-10-10 UTC.

## Outcome

No genuinely new foundational operation was established in this pass. Two mechanisms were developed far enough to expose their exact algorithms and costs; both collide with established work. The most important finding is that a plausible exact counterfactual algebra is isomorphic to an explicit table of counterfactual worlds. Its algebraic presentation does not itself reduce work. This is a rejection report, not a novelty claim.

## Four bottlenecks considered

1. **Coordinated repair of a shared computation.** Given a circuit, its input, allowed modifications, and a desired output, find the least costly collection of modifications that changes the output while satisfying protected outputs. Single local changes interact after reconvergent fanout, so an ordinary derivative or independent repair score is insufficient. An unrestricted solution contains weighted satisfiability. Bounded-separator dynamic programming and compiled decision diagrams are useful, but are established methods rather than a new operation.
2. **Exact multi-world computation.** Evaluate actual output and finite counterfactual outputs jointly, retaining the same edit identity through every reconvergent path. This led to the explicit algebra below. The one-edit instance is already deductive fault simulation; sharing across configuration worlds is variability-aware execution.
3. **Exact historical revision.** Remove or change a past state transition without replaying all subsequent transitions. Invertible updates admit cancellation conjugated by the suffix, but constructing the suffix action is the actual cost. A closed family of clipped affine transitions gives an efficient concrete algorithm below. General retroactivity and self-adjusting computation are established, and generic efficient retroactivity has strong conditional lower bounds.
4. **Future-query preservation under irreversible forgetting.** Retain a compact summary while allowing a future, not-yet-selected query to depend on discarded information. For an unrestricted query family, exact recovery of every coordinate query forces retention of the original information. Restricting to a query family leads to familiar sufficient summaries, knowledge compilation, or streaming lower-bound questions. No new primitive was found that escapes the information constraint.

## Candidate A: exact budgeted intervention algebra

### Native input and output

- A finite acyclic circuit with rational arithmetic and/or Boolean gates.
- A baseline input and m separately identified edits, initially taken to be alternative values for distinct input positions.
- A nonempty downward-closed admissible family F of edit subsets. A standard choice is every subset of size at most k.
- Output: the exact circuit value y(T) for each T in F, or its mixed finite-difference coefficients.

Internal gate replacement is also possible: replace a gate result g by (1-e_i)g + e_i r_i, where r_i is the replacement result. Mutually exclusive alternatives at one gate can be imposed by excluding their joint edit set from F. Boolean SELECT is represented by p*a+(1-p)*b. Arbitrary comparison gates require pointwise evaluation, not an unsupported symbolic extension.

### The proposed algebra

Let D = |F|. Work over a coefficient ring R, such as the rationals. Take basis elements e_S for S in F, with e_empty = 1 and multiplication

    e_A * e_B = e_(A union B), if A union B is in F;
                  0, otherwise.

Extend addition and multiplication bilinearly. Thus e_i squared equals e_i, rather than zero. Edit identity is preserved when its causal effect reconverges with itself. A multiplication involving too many distinct edits vanishes, but repeated appearances of the same edit do not falsely increase the edit count.

The lifted input at edited position i is baseline_i + (replacement_i - baseline_i)*e_i. Run the original circuit with these lifted values. For Boolean circuits over Q, use AND(a,b)=ab, NOT(a)=1-a, OR(a,b)=a+b-ab, and XOR(a,b)=a+b-2ab.

### Correctness

For each admissible world T define evaluation phi_T(e_S)=1 if S is a subset of T, and 0 otherwise. This is a ring homomorphism. If A union B is inadmissible, no admissible T contains that union, by downward closure, so the zero case also respects multiplication. Every lifted input evaluates to its correctly edited or baseline value. Induction over circuit gates gives phi_T(y_lifted)=y(T).

If y_lifted = sum_S c_S e_S, then

    y(T) = sum_(S subset T) c_S,
    c_S = sum_(T subset S) (-1)^(|S|-|T|) y(T).

These are the subset zeta transform and its Mobius inverse.

### Why the apparent breakthrough disappears

Order F by increasing set size. The matrix with entry 1[S subset T] is triangular with diagonal one. Therefore the map y_lifted -> (y(T): T in F) is an isomorphism from this algebra to the direct product R^F with coordinatewise multiplication.

This is exactly a change of basis of an explicit table of worlds. It is not a new method to evaluate exponentially many worlds in polynomial work. Every possible table can be represented, so a universal fixed-size lossless representation cannot exist without exploiting additional circuit or output structure. A compact symbolic expression can still defer evaluation, but that is not the same as cheaply obtaining its answers.

### Honest costs

For all subsets of size at most k,

    D = sum_(j=0..k) binomial(m,j).

In the world-value basis, each scalar circuit gate costs O(D), for total O(sD) ring operations for a circuit of s gates; memory is O(LD) for L simultaneously live values. This is ordinary batched evaluation. In coefficient form, naive support-union multiplication costs sum_(j<=k) binomial(m,j)*3^j operations. Conversion to values, pointwise multiplication, and conversion back can be performed in O(kD) ring operations with downward-closed zeta-transform edges precomputed. Rational bit complexity and growth of intermediate values must be accounted for separately; these bounds count ring operations only.

For Boolean outputs, one can pack worlds into machine words, but the resulting O(sD/w) bitset-style speedup is ordinary bit-parallel simulation, not exponential compression. Sparse effects and equality of values may give large instance-specific savings, but those require their own explicit complexity measure and are already central ideas in fault simulation and variability-aware execution.

### Prior art collision, located after specifying the mechanism

- **Deductive fault simulation:** fault identities that change each gate are propagated through gates, including reconvergent fanout. A single true-value simulation carries the effects of all single faults. University source: https://ece-research.unm.edu/jimp/vlsi_test/slides/html/fault_simulation1.html
- **Boolean differences with reconvergence:** *Fault-cover investigations of fan-out reconvergent circuits using boolean differences*, Computers & Electrical Engineering 9(2), 1982, pp. 63-79. The paper explicitly targets avoiding expensive higher-order Boolean differences around reconvergent paths. https://doi.org/10.1016/0045-7906(82)90012-X
- **Variability-aware execution:** *Exploring Variability-Aware Execution*, ICSE 2014, shares equal data and execution across configurations, splitting when values or control flow differ and merging equal results. Author-hosted paper: https://www.cs.cmu.edu/~ckaestne/pdf/icse14_varex.pdf
- **Generalized derivatives:** Mario Alvarez-Picallo and C.-H. Luke Ong, *Change Actions: Models of Generalised Differentiation*, 2019, includes finite differences, Boolean derivatives, and compositional change semantics. https://link.springer.com/chapter/10.1007/978-3-030-17127-8_3
- **Provenance circuits:** circuits and polynomial quotients already represent combinations of causes and support choices. *Circuits for Datalog Provenance*, author-hosted PDF: https://www.cs.tau.ac.il/~milo/projects/bpq/papers/icdt14b.pdf

The exact truncated algebra above was derived in this pass. These sources are sufficient to reject a broad claim that exact causal-effect lifting or shared-world execution is a new foundational capability. They do not certify that this precise notation appears in an earlier paper, and this report does not assert that stronger bibliographic claim.

## Candidate B: exact retroactive saturation dynamics

### Native input

A scalar initial state x0 and a sequence of transitions

    f_i(x) = clip(a_i*x+b_i, L_i, U_i), L_i <= U_i.

Updates insert, delete, or replace a historical transition; a query asks for the final or a prefix state. All coefficients can be rational.

### Constant-size composition

For f(x)=clip(a*x+b,L,U) and g(x)=clip(c*x+d,P,Q), set h=g composed with f.

If c >= 0,

    h(x) = clip(c*a*x+c*b+d,
                clip(c*L+d,P,Q),
                clip(c*U+d,P,Q)).

If c < 0, swap L and U when forming the two new bounds. The result is again a clipped affine map. When the two new bounds coincide the map is constant; this remains a valid representation.

This formula follows because a monotone affine map carries a clipped interval to a clipped interval (reversing endpoints when decreasing), and clipping the result again clips the endpoints as well. Function composition is associative, so a balanced binary composition tree stores each segment in O(1) rationals.

### Costs and operational significance

Build in O(n) scalar operations; a replacement requires O(log n) recompositions; a balanced sequence tree also supports insertion/deletion in O(log n) amortized operations. Final state needs one application of the root map. Prefix queries need O(log n) recompositions. Exact rational bit length is not constant and must be included in a bit-complexity claim.

This gives exact nonlinear historical edits for capacity-limited scalar recurrences without replaying n events. Nevertheless, the essential closure operation is established clamp composition, and the data-structure idea is ordinary monoid aggregation.

### Prior art collision

- A direct author-written implementation and derivation of shifted-clamp composition inside segment trees appears in the Tokyo Institute of Science student programming article *Static Top Tree derived by algebraic manipulation*: https://trap.jp/post/2861/ . This is primary implementation evidence for the shifted-clamp special case, not a citation for every signed-affine extension above.
- Max-plus recurrences and queue networks, including finite buffers, are a longstanding modeling framework: N. K. Krivulin, *Max-plus algebra models of queueing networks*, originally WODES 1996, later arXiv posting: https://arxiv.org/abs/1212.0578 .
- Demaine, Iacono, Langerman, *Retroactive Data Structures*, SODA 2004: https://erikdemaine.org/papers/Retroactive_SODA2004/ .
- Chung, Demaine, Hendrickson, Lynch, *Lower Bounds on Retroactive Data Structures*, ISAAC 2022, shows conditional nearly maximal overhead for general partial retroactivity: https://erikdemaine.org/papers/RetroactiveSeparation_ISAAC2022/paper.pdf .

## Additional relevant fences

- Self-adjusting computation already tracks dependencies and reuses executions after changes. Acar et al., *An Experimental Analysis of Self-Adjusting Computation*, 2009: https://www.cs.cmu.edu/~guyb/papers/ABBHT09.pdf . A new selective-replay proposal must be compared against this rather than against full from-scratch replay alone.
- Knowledge-compilation representations trade succinctness against supported efficient queries and transformations. Darwiche and Marquis, *A Knowledge Compilation Map*: https://arxiv.org/abs/1106.1819 . A new representation of possible futures needs a concrete supported query and proved succinctness/cost advantage, not merely a compact unevaluated circuit.

## What would change the outcome

A useful next result would have to identify a native class of interacting, reconvergent programs for which exact intervention answers can be computed using a provably smaller parameter than explicit world count, without receiving a precompiled decision diagram, convenient oracle, or specialized factorization as free input. It must include the cost of discovering the exploitable structure and compare against fault simulation, variability-aware execution, knowledge compilation, and self-adjusting computation. This is an open target from this pass, not a mechanism already solved.
