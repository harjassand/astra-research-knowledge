# Exact passive systems with identical frozen laws and different sequences

Constructed and checked 28 October 2026. This is an exact mathematical
counterexample, with rational actuator matrices. It is not a physical-device
execution. The Clifford algebra is standard; historical novelty of this
counterexample is unestablished.

## Matrices and scalar interface

Let X,Y,Z be the ordinary 2-by-2 Pauli matrices and define complex Hermitian
4-by-4 matrices

\[
g_1=X\otimes I,\quad g_2=Y\otimes I,\quad
g_3=Z\otimes X,\quad g_4=Z\otimes Y,\quad g_5=Z\otimes Z.
\]

Realify them by R(C)=[[Re C,-Im C],[Im C,Re C]] and set Gamma_i=R(g_i).
These are real symmetric signed-permutation 8-by-8 matrices. Direct
multiplication gives

\[
\Gamma_i^2=I,\quad \Gamma_i\Gamma_j=-\Gamma_j\Gamma_i\ (i\ne j),
\quad\Gamma_1\Gamma_2\Gamma_3\Gamma_4\Gamma_5=-I.
\]

Every product of a nonempty proper subset has trace zero: for an even-sized
subset, conjugate by a generator inside it; for an odd-sized proper subset,
conjugate by a generator outside it. In either case conjugation negates the
product while preserving its trace. The included integer checker verifies
these identities and saves all matrix entries.

Source 1 actuators are A_i=(4I+3Gamma_i)/8. Source 2 keeps the first four
and replaces Gamma_5 by -Gamma_5. Every actuator is real symmetric positive
definite and has eigenvalues 1/8 and 7/8.

For a single linear scalar port, take hidden space R^8 tensor R^8,
b=vec(I_8)/sqrt(8), and actuators A_i tensor I_8 (with the consistent
vectorization convention). Then

\[
f(w)=\langle b,A_wb\rangle=\operatorname{tr}(A_w)/8.
\]

This is a 64-coordinate reciprocal contraction system with unit reset and
one scalar terminal receiver. No quantum interpretation is required.

## Equality of every frozen law

For every real u,

\[
(\sum_i u_i\Gamma_i)^2=\|u\|_2^2I,
\qquad\operatorname{tr}(\sum_i u_i\Gamma_i)=0.
\]

Therefore every constant mixture sum_i u_i A_i in both sources has exactly
the same two eigenvalues, each of multiplicity four. Every analytic scalar
port function of that mixture agrees, including fixed-mixture powers,
semigroups and legal resolvents. This is not limited to testing each actuator
separately.

It also holds for frozen continuous relaxation generators. Set

\[
H_i=-\log A_i=aI-c\Gamma_i,\quad
a=\tfrac12\log(64/7),\quad c=\tfrac12\log7.
\]

Here a>c>0 and exp(-H_i)=A_i. For u_i>=0,
H(u)=a(sum_i u_i)I-c sum_i u_i Gamma_i is positive definite when u is nonzero.
Writing d=s+a sum_i u_i gives, on the resolvent domain,

\[
\langle b,(sI+H(u))^{-1}b\rangle
=\frac{d}{d^2-c^2\|u\|_2^2}.
\]

Both sources have the same expression. Their frozen-time response is also
identical: exp(-a t sum_i u_i) cosh(c t ||u||_2).

## Embedding in the predecessor's static family

Lift H_i to the 64-coordinate scalar-port realization. Put B_i=H_i^(1/2) and
g_i=B_i^T b. The handoff's permitted finite-rank source family then contains

\[
J(u)=c_0+\min_y[\|y\|^2+\sum_i u_i\|B_i^T(b+y)\|^2]
=c_0+1-\langle b,(I+H(u))^{-1}b\rangle.
\]

The entire J(u) agrees between sources on every dose simplex, with equal
finite rank and norm bounds. This uses full finite actuator rank, not the
rank-one suite of the predecessor. The predecessor's static results retain
their actual scope. The relative noncommutative orientations needed for
sequential operation are absent from that entire static law.

## Exact five-operation separation

Expand A_5 A_4 A_3 A_2 A_1 into Clifford monomials. Only the empty and full
five-generator terms survive the normalized trace. Thus

\[
f_1(12345)=\frac{1-(3/4)^5}{32}=\frac{781}{32768},
\qquad f_2(12345)=\frac{1+(3/4)^5}{32}=\frac{1267}{32768}.
\]

The exact separation is 243/16384. Every word of length at most four agrees:
after reducing repeated generators and anticommutations, a nonzero trace
which changes under the fifth-generator sign flip needs all five generators.
The checker also exhaustively compares all 781 such shorter words.

Consequently the entire frozen scalar law cannot determine arbitrary
switched operation. One suitable five-operation experiment distinguishes
these sources if the scalar error intervals are narrow enough.

## What mixed Gram acquisition adds

Use the actual word dictionary consisting of the empty word, five singles,
and ten ordered pairs ij with i<j. Its size is 16. Its source vectors span
the reachable Clifford module. The exact dictionary Gram G is nonsingular
and identical between sources because every entry uses a word of length
at most four. The shifted Grams M_i=V^*A_iV do differ: they contain words of
length five. Thirty entries across the five M_i distinguish the sources.

For both sources and every actuator, the second shifted Gram
N_i=V^*A_i^2V satisfies

\[
N_i-M_iG^{-1}M_i=0.
\]

The checker verifies these ten matrix identities by exact Fraction arithmetic.
This is an invariant reachable representation in this fixture. G alone does
not acquire it; the shifted mixed-word readings supply essential information.

## Charged operational interpretation

Each scalar word query means a prepared/reset state b, the commanded sequence
of contractions, and one signed calibrated terminal reading. The abstract
matrix construction does not supply a laboratory preparation, actuator,
timing contract or scalar precision. Every queried word incurs its full
operation length, preparation and reset cost; repeated histories and shared
entries need an explicit reuse policy. Distinguishing the two specified
sources requires a five-operation execution and terminal precision adequate
for their separation. General acquisition of G,M_i,N_i costs many such
experiments; no query count is a physical-time or energy bound.

The exact synthetic scalar-interface implementation actually constructs all
three matrix families through a cached query(word) interface. For each of the
two sources it charges 1036 scalar readings/prepared histories and 4995
actuator applications, with maximum query length six. The dictionary and the
measurement plan are supplied in this demonstration. They are not discovered
automatically. Twenty-six later length-five-through-seventeen predictions
agree exactly with checker-only source evaluations; no additional learner
source queries were used. All are in ideal exact arithmetic and do not
validate a finite-precision physical instrument.

The exact calculations establish the scientific counterexample and the
finite dictionary's algebra. They do not establish the real-world cost of
acquisition, a working device, or an advantage over equally informed model
reduction/realization methods.

Files: check_clifford.py and CLIFFORD_RESULTS.json. The separate interpolation
branch's RESULTS.json is not evidence for this construction.
