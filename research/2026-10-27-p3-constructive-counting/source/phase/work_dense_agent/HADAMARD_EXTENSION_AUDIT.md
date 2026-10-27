# Independent audit: arbitrary Hadamard/diagonal alternation

27 October 2026. Audited Corollary 6.1 (`cor:hadamard`) in
`deliverables/Astra_P3_Constructive_Phase_Representations.tex` and the
implementation `work_root/hadamard_phase_compiler.py`.

## Finding

The corollary is valid, conditional on the local phase-product theorem
and its governing manuscript. No normalization, path multiplicity,
locality, or original-qubit complexity gap was found. The restriction
`h_H <= C n` is essential to the claimed parameter transfer.

## Path representation

Start every wire at the constant zero. A diagonal gate changes no wire
value and contributes its phase on the current wire values. Each Hadamard
introduces exactly one fresh Boolean path variable v, replacing the old
wire value u, with kernel

    <v|H|u> = 2^(-1/2) (-1)^(u v).

The complete expression therefore has exactly h_H introduced variables
before boundary reduction, at most m+h_H phase terms, and locality at
most max(k,2). The Hadamard sign is a permitted phase because -1 is the
q/2-th power of a primitive q=2^b-th root. Constant old values only reduce
the sign to a unary phase or the constant one. Diagonal operations,
regardless of their number or alternation with Hadamards, create no path
variables.

For a requested amplitude, final wire values are pinned to the requested
computational string. Every remaining path assignment specifies one
computational history, and conversely. The amplitude is exactly

    2^(-h_H/2) times the reduced phase sum.

## Marginals and multiplicity

Multiplying an amplitude path expression by its conjugate creates two
independent copies of the path variables and changes the sign of every
phase exponent in the second copy. Pin the measured final wires in both
copies. Summing unmeasured output values imposes equality of the two final
bits on each unmeasured wire.

There is no extra factor of two from an unmeasured output: each pair of
paths with matching endpoints determines that output bit uniquely. A
constant final wire contributes one allowed endpoint, not two. Union-find
elimination of equality constraints replaces each consistent equivalence
class by one free bit, unless it is pinned to a constant. Assignments of
these free class bits are in bijection with the original satisfying
assignments of the equality system. Contradictory zero/one pins give zero.
Thus boundary elimination introduces no multiplicity, and the probability
is exactly

    2^(-h_H) times the reduced double-path phase sum.

The number of free bits is at most 2h_H. Identifying or pinning arguments
of a local truth table never increases its scope. There are at most
2(m+h_H) phase terms, including Hadamard signs. Duplicate variable
arguments can be collapsed by table substitution; no extra Boolean
constraints or trace variables are needed.

## Precision, description, and cost

Let N_* = n+2h_H. Under h_H<=C n, N_*=Theta(n), including the degenerate
case h_H=0. If boundary elimination leaves r free bits, pad with N_*-r
unused bits. This multiplies the phase sum by exactly 2^(N_*-r).

Each padded assignment contributes one root of unity, so every standard
cyclotomic coordinate is an integer in [-2^N_*,2^N_*]. Precision N_*+2
therefore recovers the signed padded sum uniquely. Divide by the known
padding multiplicity only after reconstruction. This avoids a premature
precision loss. The remaining normalization has O(h_H) bit description.
For an odd Hadamard count, retaining the factor 2^(-h_H/2) symbolically or
adjoining sqrt(2) enlarges the fixed number field by only a constant degree.

The number of phase factors after padding and reduction is
O(m+h_H), and

    log(2+(m+h_H)/N_*) = o(log N_*).

The phase-product theorem consequently gives poly(L+n) 2^o(n) bit time
and polynomial space. Constructing the raw path expression, handling
boundary equalities and pins, substituting bounded-size tables, and
normalizing the exact output all have polynomial description cost. No
geometry, graph-width, or assumed contraction order is used.

## Executed-implementation coverage

The root's checker compares unnormalized path numerators with an
independent exact state-vector evaluation. Its amplitude comparisons use
the same recorded Hadamard count on both sides; its marginal comparisons
sum products of state-vector numerators with their conjugates. These
match exactly the normalizations above. The current executed results are
24 circuit fixtures, 144 amplitude checks, 264 marginal checks, two
inconsistent-boundary checks, and two constant-wire/no-Hadamard truth-table
checks. All assertions passed in the recorded result file.

The implementation now handles both monomial-controlled phases and
arbitrary local phase tables. For a table it computes the Boolean Mobius
transform of the phase exponents over Z/qZ, using subtraction only. This
produces an exact multilinear exponent polynomial on Boolean inputs,
without dividing in a nonfield coefficient ring. Substituting current
wire constants and collapsing repeated Boolean arguments is correct; in
particular the empty monomial retains a nonzero global phase even when
all initial wires are zero. The independent state-vector evaluator reads
the table entries directly, without using this Mobius expansion, so the
comparison tests the representation conversion as well as the boundary
identities. Twelve fixtures use each gate format.

The executed table compiler can expand one gate to at most 2^k monomial
phases. Its factor count is therefore O_k(m+h_H), rather than exactly
m+h_H in that representation. The mathematical corollary may retain one
local-table factor per gate, as written. Either version has the same
density hypothesis and asymptotic bound because k is fixed, and the
explicit table/expansion costs are paid in the description. The
asymptotic replacement counter and a fast sampler were not executed.

The path expansion itself is established machinery, as the main report
states. The additional computational bound comes from applying the new
phase-product counter while charging only O(n) Hadamard path bits. It
does not permit an uncharged conversion of arbitrary gates into this
gate set, nor a claim for unrestricted Hadamard count.
