# Coarse survival: a useful tail form, an obstruction, and switched decay

28 October 2026. New exploratory results only. This note does not reopen the
accepted boundary or energy theorems, and does not audit the new coarse
cover's execution or statistical ledger.

## Setting

Work in a real \(L^2\) space with its ordinary positive cone. Each \(A_i\)
is positivity preserving, selfadjoint, and a contraction. There is a common
positive unit preparation/readout vector \(v\) satisfying

\[
 A_i v\le v.
\]

For symmetric substochastic matrices with uniform preparation this is the
normalized all-ones vector. More generally, a common reversible reference
probability gives \(v=\sqrt{\pi}\) in symmetric coordinates. Alive/absorbed
readout after a word then has probability \(f(w)=\langle v,A_wv\rangle\).
Preparation/readout selfduality by itself does not imply the order bound.
All comparisons below require the same physical preparation and genuinely
nonintrusive coarse observation.

## 1. A finite positive event controls the killing-vector inverse tail

For one primitive \(A\), put \(h=(I-A)v\ge0\), and \(f(n)=\langle v,A^n v\rangle\).
Define the extended inverse form by its nonnegative series, not by a
pseudoinverse that discards endpoint components:

\[
 Q_h=\sum_{k=0}^{\infty}\|A^k h\|^2.
\]

For every finite \(K\ge0\),

\[
 \boxed{\quad
 \sum_{k=K}^{\infty}\|A^k h\|^2
 \le f(2K)-f(2K+1).
 \quad}                                                     \tag{1}
\]

Indeed, every \(\langle h,A^n h\rangle\) is nonnegative. The even terms are
therefore bounded by the entire tail:

\[
\begin{aligned}
\sum_{k=K}^{\infty}\|A^k h\|^2
&=\sum_{k=K}^{\infty}\langle h,A^{2k}h\rangle\\
&\le\sum_{n=2K}^{\infty}\langle h,A^n h\rangle\\
&=\langle h,A^{2K}v\rangle
 =f(2K)-f(2K+1).
\end{aligned}
\]

For completeness, \(A^n v\) decreases pointwise and is dominated by \(v\),
so it converges strongly to a fixed vector \(z\). The telescoping sum on
the second line is
\(\langle h,A^{2K}v-z\rangle\); selfadjointness gives
\(\langle h,z\rangle=\langle v,(I-A)z\rangle=0\).
This also establishes \(Q_h<\infty\) and the actual square-root range
condition for \(h\), even when the global inverse is unbounded.

The right side of (1) is the probability of absorption at step \(2K+1\)
under repeated \(A\), measured from a fresh preparation. It can be acquired
as a positive event using alive/absorbed observations alone. A fixed-budget
binomial upper confidence endpoint therefore gives a finite confidence
bound on the entire tail; no exact boundary label or global strict gap is
used. The prefix is

\[
\sum_{k<K}\|A^k h\|^2
 =\sum_{k<K}\big[f(2k)-2f(2k+1)+f(2k+2)\big].
\]

Equivalently, this prefix is the difference between the probabilities of
odd and even absorption times up to \(2K\). Its signed estimation error
must still be paid. The finite tail event and its confidence endpoint are
not free instrument precision. Each trial requires a genuine preparation
and at most \(2K+1\) primitive calls, with earlier stopping after absorption.

The lemma is useful for killing vectors, or vectors with a warranted
pointwise domination by such a vector. It does not automatically apply to
the centered fitted residual \((A-t)v\). The latter includes a component
proportional to \(v\), whose local inverse form may be infinite.

## 2. No nontrivial finite-confidence upper estimator for generic centered forms

Here is an obstruction stronger than failure of a particular polynomial
tail bound. Fix a preparation law \(\pi_j=2^{-j}\), \(j\ge1\), and
\(v_j=\sqrt{\pi_j}\). Consider diagonal, symmetric, substochastic operations.
For the good source \(A_0=aI\), \(0<a<1\), every reset lifetime is geometric.
For a bad source \(A_{j,\lambda}\), replace only diagonal entry \(j\) by
\(\lambda\in(a,1)\). Every source in this pair is strictly contractive and
absorbs almost surely; no immortal state is required.

Every finite scalar word changes in expectation by at most \(\pi_j\),
uniformly over its length:

\[
 f_{j,\lambda}(k)=(1-\pi_j)a^k+\pi_j\lambda^k,
 \qquad |f_{j,\lambda}(k)-a^k|\le\pi_j.
\]

More strongly, any adaptive experiment using at most \(N\) preparations can
be coupled to have an identical entire coarse transcript with probability
at least \(1-N\pi_j\). Couple the internal randomness and all non-\(j\)
trajectories. Until a reset happens to select state \(j\), every observation,
adaptive word choice, stopping decision, and output agrees. Word lengths
may be arbitrarily long and adaptively chosen.

Yet

\[
 Q_t(A_{j,\lambda})
 = (1-\pi_j)\frac{(a-t)^2}{1-a^2}
   +\pi_j\frac{(\lambda-t)^2}{1-\lambda^2}
\]

can be arbitrarily large for every fitted \(t\) bounded below one.

**Finite-confidence consequence.** Suppose a procedure claims a uniformly
sound upper certificate \(U\ge Q_t\), with false-certificate probability at
most \(\delta\), over this source class. It cannot, on \(A_0\), stop after a
finite transcript and output both \(U<\infty\) and \(t<1\) with probability
strictly greater than \(\delta\).

To prove this, a finite union exhaustion supplies an event \(E\) of
probability greater than \(\delta\), on which at most \(N\) preparations
occur, \(U\le M\), and \(t\le1-\kappa\), for fixed finite \(N,M\) and
\(\kappa>0\). Choose \(j\) so that the coupling transfers \(E\) to the bad
source with probability still greater than \(\delta\). Then choose
\(\lambda\ge1-\kappa/2\), sufficiently close to one that

\[
 \frac{\pi_j\kappa^2}{4(1-\lambda^2)}>M.
\]

Every transferred output on \(E\) is false, a contradiction. The argument
does not require a bounded expected stopping time. It requires only that
the claimed successful outputs have finite transcripts. Unknown finite
uniform mixtures with increasing hidden size give the same obstruction
when that size is not supplied to the learner.

This is a limitation of the inverse form, not an impossibility theorem for
uniform scalar prediction. The predictor \(a^k\) is already within
\(\pi_j\) of the bad source at every horizon. If every primitive has the
same rare-block construction, the same statement holds for every switched
word. The observable task is continuous in rare preparation mass while the
inverse residual form is not.

## 3. The proposed all-switching lemma is valid, with a sharper scalar bound

For any \(x\) with \(|x|\le c v\), selfadjoint spectral calculus gives

\[
\|x\|^2-\|A_i^m x\|^2
\le m\big(\|x\|^2-\|A_i x\|^2\big),\qquad m\ge1.
\]

This uses \(1-\lambda^{2m}\le m(1-\lambda^2)\), valid throughout
\([-1,1]\); positive semidefiniteness of the operator is not required.
Positivity additionally gives
\[
 |A_i^m x|\le c A_i^m v,\qquad
 \|A_i^m x\|^2\le c^2 f_i(2m).
\]

Thus the scalar survival measurement supplies the functional inequality

\[
 \boxed{\quad
 \|x\|^2\le m\,\langle x,(I-A_i^2)x\rangle
              + f_i(2m)\left\|x/v\right\|_\infty^2 .
 \quad}                                                     \tag{2}
\]

The gauge \(\|x/v\|_\infty\) is nonexpansive under every primitive. Every
reachable word state starting at \(v\) has gauge at most one. If
\(f_i(2m)\le s\le1\) for every primitive, then arbitrary switching gives

\[
 \|A_wv\|^2\le z_H,\qquad
 z_H=s+(1-1/m)^H(1-s),\qquad H=|w|.
\]

For the scalar response, split the word into lengths \(a\) and \(b\).
Selfadjointness turns the transpose of one half into the reversed physical
word. Both resulting vectors are reachable, so

\[
 f(w)\le\sqrt{z_a z_b}.
\]

In particular,

\[
 \boxed{\quad
 |w|=2h \ \Longrightarrow\
 f(w)\le s+(1-1/m)^h(1-s).
 \quad}                                                     \tag{3}
\]

For odd lengths use \(a=\lfloor H/2\rfloor\), \(b=\lceil H/2\rceil\).
The limiting scalar floor is \(s\), improving the unsplit \(\sqrt{s}\)
floor. Balanced splitting minimizes this product within this envelope
because \(\log z_h\) is convex. Endpoint cases \(s=0,1\) and \(m=1\) follow
directly or by continuity.

A finite collection of measured pairs \((m_j,s_j)\), common to all
primitives, gives the stronger scalar recursion

\[
 u_0=1,\qquad
 u_{h+1}=\min\!\left\{u_h,\ 
       \min_j\left[(1-1/m_j)u_h+s_j/m_j\right]\right\}.
\]

Every map in this minimum is increasing, so \(u_h\) bounds the reachable
norm squares by induction. The same two-sided bound uses
\(\sqrt{u_a u_b}\). This is a profile refinement, not a new acquisition
implementation.

### Established functional-inequality context

Inequality (2) is a killed, noncentered weak-Poincaré/weak-Hardy inequality
with bounded-function gauge. Weak Poincaré inequalities and their conversion
to \(L^2\) decay are established machinery. Röckner and Wang (2001) establish
the semigroup relationship; Andrieu, Lee, Power, and Wang, arXiv:2312.11689,
Definition 3 and Theorem 8, formulate the discrete-chain gauge inequality
and energy-decay mechanism using \(P^*P\). Those sources concern invariant
Markov chains and centered functions; the killed-source result above is
proved directly rather than imported without checking those hypotheses.

Primary sources:

- [Röckner and Wang, JFA 185 (2001), 564–603](https://doi.org/10.1006/jfan.2001.3776).
- [Andrieu, Lee, Power, and Wang, arXiv:2312.11689](https://arxiv.org/pdf/2312.11689).

The new operational question is the finite observable certificate common
to an entire switched language. The weak functional inequality itself
should not be presented as a newly invented general principle. This
targeted comparison does not establish novelty priority for the complete
construction.

## 4. Both structural assumptions are load-bearing

**Selfduality without the common order vector is insufficient.** Let

\[
 v=e_1,\quad
 A_0=\begin{pmatrix}1/2&1/4\\1/4&1/2\end{pmatrix},\quad
 A_1=\operatorname{diag}(1/2,1).
\]

Both are symmetric positive contractions, and each pure response tends to
zero. But \(A_0v\not\le v\), and

\[
 \langle v,A_0 A_1^H A_0v\rangle
 =\frac1{16}+\frac14\,2^{-H}\longrightarrow\frac1{16}.
\]

Thus pure decay alone does not imply switched decay for an arbitrary
selfdual input-output pair.

**The common order vector without selfadjointness is insufficient.** Let
\[
 A=\begin{pmatrix}0&1\\0&0\end{pmatrix},\qquad B=A^*,
 \qquad v=2^{-1/2}(1,1).
\]
These are nonnegative doubly substochastic contractions, and \(Av,Bv\le v\).
Both pure powers vanish at step two, while the response of \((AB)^h\)
equals \(1/2\) for every \(h\ge1\). The spectral step in (2) cannot be
extended to arbitrary nonsymmetric operations.

Primitive lifetime-CDF estimation, including DKW control, only concerns
repetitions of one action. Equations (2)–(3), with both structural premises,
are what transfer those data to every switched word.

## 5. The new countable-block example has infinite inverse residual forms

Consider the root construction's fast block of weight \(1023/1024\) and
slow blocks with

\[
 p_n=2^{-n-1}/1024,\qquad e_n=2^{-n-4},\qquad
 A_{i,n}=(1-e_n)I+e_n C_i,
\]
\[
 C_0=\frac1{16}\begin{pmatrix}10&2\\2&2\end{pmatrix},
 \qquad
 C_1=\frac1{16}\begin{pmatrix}8&1\\1&2\end{pmatrix}.
\]

Preparation is uniform inside each block, with the stated block weights.
Both \(C_i\) are symmetric, positive definite, and strictly substochastic.
Their row sums are bounded below one. Consequently the direct sum preserves
the common order interval, has norm exactly one, and has no nonzero fixed
live vector. Every slow block has positive preparation probability.

The expected lifetime within slow block \(n\) is

\[
 \frac{1}{e_n}\left\langle u,(I-C_i)^{-1}u\right\rangle,
 \qquad u=2^{-1/2}(1,1).
\]

The bracket equals \(12/5\) for \(C_0\) and \(64/37\) for \(C_1\). Since
\(p_n/e_n=1/128\), each successive slow block contributes the same positive
amount to the unconditional mean, so that mean is infinite. Nevertheless,
every individual block eventually absorbs, and dominated convergence gives
\(f_i(k)\to0\). Equations (2)–(3) therefore supply arbitrary switched-word
tail bounds without a finite mean lifetime or strict global gap.

The separation is stronger than failure to estimate a finite quantity.
For every scalar \(t<1\),

\[
 \|(I-A_i^2)^{-1/2}(A_i-t)v\|^2=\infty.
\]

On sufficiently slow blocks, every eigenvalue is at least
\(1-(1-t)/2\), so the residual magnitude is at least \((1-t)/2\) times the
preparation norm. Also

\[
 I-A_{i,n}^2\le 2e_n I.
\]

Each such block contributes at least
\[
 \frac{p_n(1-t)^2}{8e_n}=\frac{(1-t)^2}{1024}
\]
to the form. Summing proves divergence.

This extends to every finite word-feature compression with a strictly
stable computational \(T_i\). For word features of fixed finite lengths,
the block feature matrix has expansion
\[
 V_n=\sqrt{p_n}\,[u\,\mathbf1^T+O(e_n)].
\]
Therefore
\[
 (A_{i,n}V_n-V_nT_i)x
 =\sqrt{p_n}\,[u\,\mathbf1^T(I-T_i)x+O(e_n)].
\]
Since \(I-T_i\) is invertible, some \(x\) has a nonzero leading coefficient.
The inverse form then again has a positive lower contribution from every
sufficiently slow block. The same argument applies to finite linear
combinations of word features retaining \(v\), replacing \(\mathbf1^T\)
by their nonzero limiting row.

This statement is restricted to finite word features and strictly stable
computational models. It is not a theorem against all reduced
representations. It explains why a coarse survival cover can succeed on
this example while that class of inverse-form certificates cannot even
have finite premises.

## Exact check scope

The companion coarse_survival_checks.py verifies a small negative-spectrum
killing-vector example, the two structural counterexamples, a noncommuting
common-order pair, rare-mode form blow-up, and the exact block constants.
It does not sample physical trials or test the root's acquisition ledger.
