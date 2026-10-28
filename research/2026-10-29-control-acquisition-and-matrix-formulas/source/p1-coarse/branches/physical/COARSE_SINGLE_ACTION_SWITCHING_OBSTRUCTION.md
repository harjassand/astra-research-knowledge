# Exact single-action survival does not determine switching

28 October 2026. A direct finite-dimensional construction under fresh uniform
preparations and coarse live/absorbed observations. All calculations below
are exact. No accepted local proof or predecessor result is re-audited.

## Result

Two live states and two symmetric substochastic operations suffice. There are
two sources with strictly positive, positive-definite live kernels, each a
strict contraction, such that:

1. Every single-operation survival law agrees between the sources, at every
   repetition length.
2. Their two-step mixed survival probabilities differ by **3/32**.
3. The preferred order of the three-step programs **AAB** and **ABA** is
   opposite in the two sources.

Consequently, even exact knowledge of every individual-operation survival
distribution cannot supply a general certificate for switching. Uniform
statistical estimation of those distributions does not resolve the missing
information. The obstruction is relative alignment of hidden coordinates.
This is an elementary conjugacy construction, not a claim of a new general
principle about system identification.

## Observation convention and sources

Let the fresh initial distribution be p=(1/2,1/2)^T, with live readout
1=(1,1)^T. Missing live row mass goes to an irreversible cemetery. For a
chronological word w=i_1...i_h define

\[
s(w)=\mathbf 1^T A_{i_h}\cdots A_{i_1}p
     =u^T A_{i_h}\cdots A_{i_1}u,
\qquad u=\frac1{\sqrt2}(1,1)^T.
\]

The two source families are (A,B_+) and (A,B_-), where

\[
A=\frac1{16}\begin{pmatrix}10&2\\2&2\end{pmatrix},\qquad
B_+=\frac1{16}\begin{pmatrix}8&1\\1&2\end{pmatrix},\qquad
B_-=\frac1{16}\begin{pmatrix}2&1\\1&8\end{pmatrix}.
\]

Their row sums are respectively (3/4,1/4), (9/16,3/16), and
(3/16,9/16). Thus every live state has positive absorption probability.
Symmetry and the row-sum bounds imply operator norms at most 3/4 and 9/16,
strictly below one. All live entries are positive. The first diagonal entries
and determinants are positive:

\[
\det A=\frac1{16},\qquad \det B_+=\det B_-=\frac{15}{256}.
\]

Hence all three live kernels are positive definite as well. The example
does not rely on negative eigenvalues, disconnected live states, infinite
dimension, or inaccessible fixed modes.

## Equality of all single-action observations

Let P exchange the two live states. Then P^2=I, Pu=u and
B_-=PB_+P. For every n>=0,

\[
s_-(B^n)=u^T(PB_+P)^n u
        =u^TPB_+^nPu
        =u^TB_+^nu=s_+(B^n).
\]

The A kernels are identical. This proves equality for every repetition
length, not just for a finite moment dictionary.

For an explicit description of the entire common sequences, Cayley-Hamilton
gives

\[
\begin{aligned}
s_A(0)&=1,&s_A(1)&=\frac12,&
s_A(n+2)&=\frac34s_A(n+1)-\frac1{16}s_A(n),\\
s_B(0)&=1,&s_B(1)&=\frac38,&
s_B(n+2)&=\frac58s_B(n+1)-\frac{15}{256}s_B(n).
\end{aligned}
\]

The complete coarse record during a repeated single action is determined by
its absorption time tau: P(tau>n)=s_i(n). Thus equality of these sequences
also gives equality of full live/absorbed path-record laws, including arbitrary
single-action censor times. Adaptive choices among fresh single-action
experiments cannot distinguish the two sources. Reusing a survivor to apply
a different action would supply a mixed-action experiment and falls outside
the data being compared.

## Mixed survival and an opposite ordering decision

Since the kernels are symmetric, two-step survival is half the inner product
of their live row-sum vectors. Therefore

\[
s_+(AB)=\frac12\left(\frac34\frac9{16}+\frac14\frac3{16}\right)
       =\frac{15}{64},\qquad
s_-(AB)=\frac12\left(\frac34\frac3{16}+\frac14\frac9{16}\right)
       =\frac9{64}.
\]

The difference is 3/32. Any estimate based only on the identical exact
single-action laws has worst-case absolute error at least 3/64 on this pair.
Any interval guaranteed to contain both possible mixed responses must have
width at least 3/32.

Ordinary exact multiplication gives the stronger order-sensitive witness:

| Chronological program | Source + | Source - |
|---|---:|---:|
| AB or BA | 15/64 | 9/64 |
| AAB or BAA | 39/256 | 21/256 |
| ABA | 40/256 | 16/256 |
| AAB minus ABA | **-1/256** | **5/256** |

Thus the single-action observations cannot even determine which of two
programs with the same operation counts has larger survival.

Both families genuinely contain noncommuting operations:

\[
AB_+-B_+A=\frac1{64}\begin{pmatrix}0&-1\\1&0\end{pmatrix},\qquad
AB_--B_-A=\frac5{64}\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
\]

This is not a common hidden-state relabeling of the whole source: the only
nontrivial two-state permutation changes A, whereas A is held fixed.

## Minimality and a genuine exception

**Two live states are minimal.** With one live state, each primitive is a
scalar a_i. Its one-step survival identifies a_i, and every word has survival
equal to the product of its scalar factors. There is no such ambiguity.
At least two operations are necessary, and the mixed witness above uses the
smallest possible length, two.

**Three steps are minimal for order within one source.** For any symmetric
kernels and common preparation/readout vector u,

\[
u^TA_{i_h}\cdots A_{i_1}u
=u^TA_{i_1}\cdots A_{i_h}u.
\]

Every word has the same response as its reversal. In particular AB and BA
cannot differ under this interface, even when A and B do not commute.
AAB and ABA are the first possible pair with equal operation counts that
are not forced equal by reversal, and the displayed construction separates
them with opposite signs across the indistinguishable sources.

**Common constant row sums are an exception in every dimension.** If each
primitive satisfies A_i 1=a_i 1, the uniform direction is a common
eigenvector. Every word then has survival product_i a_i, with factors repeated
according to the word. Individual one-step survival identifies the entire
switched survival response. Our example deliberately violates that shared
closure condition.

## Verification and implication

`coarse_single_action_switching_obstruction.py` verifies conjugacy, strict
row bounds, positivity, positive definiteness, the exact recurrence identities,
mixed responses, noncommutation and the two ordering signs using only Python
`Fraction` arithmetic. It ran successfully. The all-horizon claim follows
from the conjugacy proof, not from finitely checking powers.

The next required information is joint information about the actions on
shared hidden directions. A single mixed probe already distinguishes this
particular pair. The result does not show that a finite mixed-probe family
identifies every coarse hidden source, nor does it restore exact boundary
preparation from a coarse live report.
