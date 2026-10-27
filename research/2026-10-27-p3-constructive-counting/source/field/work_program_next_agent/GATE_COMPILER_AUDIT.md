# Exact bounded-degree gate acquisition

The proposed degree-three compiler is sound without a supplied degree promise. Every successful gate stores its exact Boolean ANF, so the downstream field compiler and counter count the original circuit on its original independent inputs. The stronger term-count compiler in the final section supersedes its intermediate-degree restriction. This is a certifying interface built from standard coefficient propagation, not a generic circuit-counting theorem.

## Exact invariant

Use squarefree monomials indexed by subsets of the original `n` inputs. XOR is symmetric difference, NOT toggles the empty mask, and AND takes the parity of all unions of input masks. Perform multilinear reduction and all cancellations before testing the degree cap. Induction in the Boolean ring `F2[x]/(x_i^2-x_i)` proves the accepted-gate invariant. No SAT or gate variables are introduced.

Cancellation before the cap matters: if `a` is a sum of cubic monomials, `a AND a=a` and `a AND NOT(a)=0`, even though individual product pairs may have degree six. Rejecting on the first high pair is incorrect.

The algorithm is intentionally incomplete: an intermediate quartic may eventually cancel to a cubic or constant, yet the compiler rejects at that intermediate. Exact identity preprocessing and dead-gate removal can enlarge the accepted class; neither should be confused with general low-degree certification.

## Description size and a space correction

Assume binary AND/XOR and unary NOT in an acyclic circuit with `S` internal gates. Circuit opcode and reference size is `O((S+n) log(S+n))` bits. Unbounded fan-in must be expanded or its input list separately charged. Put `M_k(n)=sum_{j=0}^k binom(n,j)`.

Each accepted gate stores at most `M_3(n)` masks. Each AND processes at most `M_3(n)^2` pairs, each union having degree at most six. Deterministic sorting/parity reduction gives `O(S M_3(n)^2 poly(n))` bit time; the polynomial absorbs mask and logarithmic costs. Hash-set implementations perform exact algebra but their usual expected lookup cost is not a deterministic worst-case guarantee.

**The direct all-pairs parity-set implementation requires a temporary degree-six space term.** It can retain `M_6(n)` distinct masks before rejection or cancellation. Its safe bound is

    O((S M_3(n) + M_6(n)) n) bits,

plus circuit description, using conservative `n`-bit masks. Counting only storage for accepted gates omits this temporary product.

The smaller `O(S M_3(n) n)` bound is attainable at the same coarse time with a different product implementation. Enumerate every candidate union `U` with at most six elements. For that coefficient enumerate ordered `(A,B)` with `A union B=U` and `|A|,|B|<=3`, querying input-ANF membership. There are at most `3^6` pairs per `U`: each element belongs to the left set, right set, or both. Compute their parity, emit the low-degree coefficient, and reject on a surviving high-degree coefficient. No degree-six array is retained. Since `M_6(n)=O(M_3(n)^2)`, the coarse time stays unchanged; sorted input arrays give deterministic polynomial membership cost.

## What truncation preserves, and what it cannot certify

Let `pi_k` discard squarefree ANF monomials of degree greater than `k`. Then

    pi_k(f+g) = pi_k(f)+pi_k(g),
    pi_k(fg) = pi_k(pi_k(f) pi_k(g)).

The second identity follows because supports multiply by union: a high-degree factor cannot produce a low-degree product. Thus high ANF degrees span an ideal, and gatewise truncation is a quotient-ring homomorphism. It preserves every low-degree coefficient through all subsequent XOR/AND/NOT gates on the same original variables. A discarded high term cannot later become a constant. There is no counterexample with a genuinely constant final function and an incorrectly truncated final constant.

The unsound step is treating the truncated output as a certificate that higher degrees are absent. For

    f=x_1 x_2 x_3 x_4,

degree-three truncation gives zero, though `f` has one satisfying assignment among sixteen. The complement truncates to constant one and gives a false count of sixteen instead of fifteen. Multiplying `f` by `x_1` keeps this undetected high term, but does not convert it to low degree.

For sound incompleteness, compute `g=x_1 x_2 x_3 x_4`, then `NOT(g XOR g)`. Both the full circuit and quotient propagation give constant one. The proposed certifying compiler rejects at `g`. This is the correct distinction between computing low-degree coefficients and certifying the final degree.

Substituting new constants or changing the original variable model after truncation need not commute with this quotient; those are distinct operations requiring their own proof.

## Executed checks

`gate_compiler_audit.py` checks the false-constant count examples, exact degree-six cancellation in cubic idempotence/complement products, rejection despite a constant final output, quotient multiplication identities, and accepted circuit outputs against direct gate evaluation on every input. Results are in `gate_compiler_audit_results.json`. These are interface checks, not a practical-speed comparison.

## Stronger acquired front end: cap term count, not intermediate degree

Fix an explicit budget `M`, for example `M=M_3(n)`. Retain the complete exact ANF at every gate, with monomials of any Boolean degree. After exact union multiplication and parity cancellation, reject a gate only if more than `M` terms survive. Test Boolean degree at most three only at the requested output.

The same induction proves every retained state is exact. Each AND generates at most `M^2` union masks, regardless of their degrees. Sorting these masks and canceling equal runs yields deterministic bit time

    O(|C| + S M^2 n log(M+2)),

where `|C|` is the encoded circuit size. XOR and NOT fit this bound. Conservative storage is `O((SM+M^2)n+|C|)` bits; add `O(n^2)` if all input masks are stored explicitly rather than generated from their input indices. The bound is polynomial in `M`; if `M` is supplied in binary and enormous, it is not automatically polynomial in the description length of `M`. The default `M_3(n)` gives a polynomial front end.

This strictly enlarges the earlier accepted class. A chain computing `g=x_1...x_n` retains a single monomial even though its degree reaches `n`. Then `h=g AND x_1` is the same monomial, `j=g XOR h` is zero, and `NOT(j)` is one. The term-count compiler accepts this entire circuit with `M=1` and acquires the final constant exactly. The intermediate-degree compiler rejects as soon as a fourth distinct input enters the product. Likewise, sparse high-degree states can cancel to a nonconstant cubic output.

The acquisition remains incomplete in a different way: a gate whose true ANF has more than `M` terms is rejected even if its descendants eventually cancel to a constant. This is not an assumed sparsity certificate. The front end computes and checks every accepted state, so a successful run certifies the complete identity on arbitrary input circuits. It does not assert that every circuit yielding a cubic can be recognized within the budget.

The independent executable includes a deterministic sort-and-parity version of this stronger compiler. It checks high-degree cancellation positives, rejection of sparse quartics at the final degree check, and final exact identities on the same random circuits. The downstream centroid and rank-metric representation checks remain necessary, and their runtime must be added to this front-end cost.

## A precise obstruction to complete polynomial-time degree acquisition

The language of arbitrary Boolean circuits whose output has ANF degree at most three is coNP-complete. This is a standard complexity lemma; the following elementary proof audits its applicability here.

Membership in coNP follows from a short witness for degree at least four. Give four distinct input-coordinate indices `I={i_1,i_2,i_3,i_4}` and an assignment `x` such that

    sum_{J subset I} C(x XOR 1_J) = 1 over F2.

The verifier evaluates the circuit only sixteen times. If the degree is at most three, every fourth coordinate difference is zero. Conversely, if an ANF contains a monomial of degree at least four, take four indices in that monomial. Its fourth difference is a nonzero Boolean polynomial: distinct input monomials containing those four indices have distinct remaining supports, so the selected term cannot cancel identically. A nonzero Boolean function equals one somewhere, providing the required assignment. The witness has polynomial length and verification time in the encoded circuit.

For coNP-hardness, reduce CIRCUIT-UNSAT on `C(x)` to the circuit

    G(x,z)=C(x) z_1 z_2 z_3 z_4,

with four fresh independent variables. If `C` is identically zero then `G` is zero and has degree at most three. Otherwise its unique multilinear ANF is nonzero, and multiplying by the four fresh variables adds four to every surviving monomial's degree without cancellation. Thus `G` has degree at least four. The transformation adds only four inputs and four binary AND gates.

A complete deterministic polynomial-time recognizer for this degree condition, or a complete polynomial-time procedure that emits the exact cubic representation whenever one exists and correctly rejects every higher-degree circuit, would therefore imply `P=NP`. This does not rule out restricted acquired representations or incomplete certifying compilers. It does not assert an unconditional lower bound for counting, and it is consistent with the pinned subexponential fixed-width counting theorem.
