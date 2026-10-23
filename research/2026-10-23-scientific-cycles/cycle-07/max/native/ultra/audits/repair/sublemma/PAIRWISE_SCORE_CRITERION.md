# Exact score criterion for pairwise queue repair

Status: internal analytic sublemma, independently checked within this run.
This is an obstruction under the explicit channel hypotheses below. It is not
a resolution of joint cross-pair repair, approximate repair, or the parent
research objective. No numerical search or external novelty claim is used.

## 1. Definitions and channel scope

Let \(D\ge2\) be an integer and
\[
 |\Phi_D\rangle=D^{-1/2}\sum_{i=1}^{D}|i\rangle_A|i\rangle_B,\qquad
 \Phi=|\Phi_D\rangle\langle\Phi_D|,\qquad
 \nu=(I_A/D)\otimes(I_B/D),\qquad q=D^{-2}.
\]
All effective pair channels have input and output
\(\mathbb C^D\otimes\mathbb C^D\), with the displayed Bell projector as target.

A SEP channel here means a CPTP map with product Kraus operators
\(A_s\otimes B_s\). This includes LOCC and its finite-dimensional closure.
It does not mean merely a channel that maps separable states to separable
states. Internal local ancillas and discarding are allowed when the resulting
effective pair map has the stated dimensions and is SEP.
There is no uncharged initial shared entangled ancilla or other nonlocal
resource. Any extra resource must be included and charged in the parent
bookkeeping; an effective channel using it need not be SEP. The channel
class used here permits local discard and preparation. Whether these are
free in a stricter physical model is a separate resource-accounting question.

## 2. Known exact Bell-fixing rigidity

This is a special case of Gheorghiu and Griffiths, *Entanglement transformations
using separable operations*, Phys. Rev. A 76,032310(2007), Theorem 1,
[arXiv:0705.0369](https://arxiv.org/abs/0705.0369). It is retained below as a
self-contained check, not claimed as a new rigidity theorem. The actual mixed
queue-score induction in Section 4 is a distinct receiving consequence.

If a SEP channel \(\Lambda\) satisfies
\(\operatorname{Tr}[\Phi\Lambda(\Phi)]=1\), then
\[
 \Lambda(X)=\sum_s p_s
 (U_s\otimes\overline U_s)X(U_s\otimes\overline U_s)^\dagger,
 \qquad p_s\ge0,\quad\sum_s p_s=1.
\]
In particular,
\[
 \Lambda(\Phi)=\Phi,\qquad \Lambda(\nu)=\nu.
\]
Thus such a channel cannot remove any entropy from the private product noise.

Proof. Unit Bell overlap makes the output exactly the pure state \(\Phi\).
For each product Kraus operator, positivity and output purity imply
\[
 (A_s\otimes B_s)|\Phi_D\rangle=c_s|\Phi_D\rangle,\qquad
 A_sB_s^T=c_sI,\qquad \sum_s|c_s|^2=1.
\]
For \(c_s\ne0\), \(A_s\) is invertible and, putting
\(P_s=A_s^\dagger A_s\),
\[
 \|A_s\|_F^2\|B_s\|_F^2
 =|c_s|^2\operatorname{Tr}(P_s)\operatorname{Tr}(P_s^{-1})
 \ge D^2|c_s|^2.
\]
Equality holds exactly when \(P_s\) is scalar. Trace preservation gives
\[
 \sum_s\|A_s\|_F^2\|B_s\|_F^2
 =\operatorname{Tr}I_{D^2}
 =D^2=D^2\sum_s|c_s|^2.
\]
Every nonnegative deficit is therefore zero. A \(c_s=0\) term has zero
product-Kraus norm and vanishes. Every remaining term has
\[
 A_s=\sqrt{a_s}U_s,\qquad
 B_s=(c_s/\sqrt{a_s})\overline U_s,
\]
so its product Kraus operator is
\(c_s(U_s\otimes\overline U_s)\), proving the formula.

For an uncorrelated product channel
\(\Lambda=\mathcal E_A\otimes\mathcal E_B\), this specializes to one matched
local-unitary channel. Indeed, its independent Kraus pairs must all have
the displayed form; fixing any nonzero Kraus operator on one side makes
all operators on the other side proportional, and conversely. Hence in
this narrower case every input spectrum is unchanged.

As a direct corollary, a SEP channel whose Bell score never decreases on
any input already obeys this rigidity: apply the condition to \(\Phi\).

## 3. A sharp criterion for one isotropic input

Define
\[
 a=\operatorname{Tr}[\Phi\Lambda(\Phi)],\qquad
 b=\operatorname{Tr}[\Phi\Lambda(\nu)].
\]
Every SEP channel satisfies
\[
 a+Db\le1+\frac1D,\qquad
 b-q\le\frac{1-a}{D}.                                      \tag{1}
\]

For completeness, the state
\[
 \chi=\frac{\Phi+D\nu}{D+1}
      =\frac{I+D\Phi}{D(D+1)}
\]
is separable. One explicit finite decomposition is obtained as follows.
Let \(Z=\sum_i|ii\rangle\langle ii|\), and let
\[
 |v_\theta\rangle=D^{-1/2}\sum_i e^{i\theta_i}|i\rangle,
 \qquad \theta_i\in\{0,\pi/2,\pi,3\pi/2\}
\]
with the phases independent and uniform. The average of the product
projectors
\(|v_\theta\rangle\langle v_\theta|\otimes
 |\overline v_\theta\rangle\langle\overline v_\theta|\)
is \((I+D\Phi-Z)/D^2\). Mixing this with the product-state ensemble
\(Z/D\), with weights \(D/(D+1)\) and \(1/(D+1)\), gives \(\chi\).
Every separable state \(\sigma\) has
\(\operatorname{Tr}(\Phi\sigma)\le1/D\), by Cauchy--Schwarz on pure product
vectors and convexity. Applying this fact to \(\Lambda(\chi)\) proves (1).

Now let \(\alpha,\beta\ge0\). They may be unnormalized weights; no division
by \(\alpha+\beta\) is needed. The Bell-score change on
\(\alpha\Phi+\beta\nu\) is
\[
 \Delta=\alpha(a-1)+\beta(b-q)
 \le-(\alpha-\beta/D)(1-a).                               \tag{2}
\]
Consequently, if
\[
 \alpha>\beta/D\quad\hbox{and}\quad\Delta\ge0,              \tag{3}
\]
then \(a=1\), and the rigidity in Section 2 forces
\(\Lambda(\Phi)=\Phi\) and \(\Lambda(\nu)=\nu\).

The strict threshold is sharp. The local product reset
\(R(X)=\operatorname{Tr}(X)|00\rangle\langle00|\)
has \(a=b=1/D\) and saturates (2):
\[
 \Delta_R=(1-1/D)(\beta/D-\alpha).
\]
At \(\alpha=\beta/D\), it preserves the score while changing noise entropy;
at \(\alpha<\beta/D\), it increases the score. Thus unknown branch position
alone is not a blanket entropy obstruction.

## 4. Actual uniform queue under fixed pairwise processing

Let \(1\le L\le N\), and define the exact uniform queue
\[
 \omega_N=\frac1L\sum_{k=1}^{L}
      \Phi^{\otimes k}\otimes\nu^{\otimes(N-k)},\qquad
 P_j=\Phi^{\otimes j}\otimes I^{\otimes(N-j)}.
\]
Suppose the processor is a fixed, input-independent product of individually
CPTP SEP pair channels,
\[
 T=\bigotimes_{i=1}^{N}\Lambda_i,
\]
and its actual averaged prefix scores satisfy
\[
 \operatorname{Tr}[P_jT(\omega_N)]
 \ge\operatorname{Tr}[P_j\omega_N]\qquad(1\le j\le L).       \tag{4}
\]
Then every uncertain position \(1\le j\le L\) obeys
\[
 \Lambda_j(\Phi)=\Phi,\qquad \Lambda_j(\nu)=\nu.
\]
The first \(L\) pairs of the queue are unchanged. A known suffix \(j>L\)
can be reset; the theorem does not constrain it.

Proof by induction. At \(j=1\), the first pair is certainly \(\Phi\), and
(4) forces \(a_1=1\). Section 2 therefore fixes both \(\Phi\) and \(\nu\)
at this position.

For \(2\le j\le L\), assume the preceding pair channels fix both states.
The contribution of branches \(k\ge j\) to the \(j\)-th prefix score is
then weighted Bell input, while branches \(k<j\) contribute weighted noise
input. Their exact unnormalized weights are
\[
 \alpha_j=\frac{L-j+1}{L},\qquad
 \beta_j=\frac1L\sum_{k=1}^{j-1}q^{j-1-k}
        =\frac1L\sum_{h=0}^{j-2}q^h.                      \tag{5}
\]
Thus the before/after prefix scores are respectively
\(\alpha_j+\beta_jq\) and \(\alpha_ja_j+\beta_jb_j\).
These are not probabilities conditioned by dividing through by the
previous-prefix score; equation (2) applies directly to their weights.
Moreover,
\[
 L(\alpha_j-\beta_j/D)
 \ge1-\frac1D\sum_{h=0}^{\infty}D^{-2h}
 =1-\frac{D}{D^2-1}>0 \qquad(D\ge2).                     \tag{6}
\]
Equations (2), (4), and (6) force \(a_j=1\), completing the induction.

The same conclusion holds for a convex mixture
\[
 T=\sum_t p_t\bigotimes_i\Lambda_{i,t},
\]
with each factor individually CPTP SEP. At \(j=1\), each component has
nonpositive score change, so every positive-weight component must have
zero change and \(a_{1,t}=1\). Inductively, all earlier factors in every
positive-weight component fix \(\Phi,\nu\). Equations (2) and (6) then
make every component's \(j\)-th change nonpositive. A nonnegative average
forces every positive-weight component to have \(a_{j,t}=1\). Continuous
shared-random mixtures give the same statement almost surely.

### Classical branch records

Retaining the classical outcomes of the uncertain-pair operations does not
permit learning which of their inputs was Bell or private noise. In the
original product-Kraus refinement of any such SEP pair channel, Section 2
forces every nonzero branch to have
\[
 K_s=c_s(U_s\otimes\overline U_s),\qquad
 K_s^\dagger K_s=|c_s|^2I.
\]
Its branch probability is therefore input-independent. Conditioned on the
full branch label, its normalized operation is a matched local unitary,
which fixes both \(\Phi\) and \(\nu\). For a product over uncertain positions,
the complete branch record has input-independent weight, and the conditional
uncertain-prefix queue remains exactly its original state. The same holds
after conditioning on the shared-random mixture component. Coarsening or
forgetting classical labels cannot reveal a hidden queue branch.

In particular, let
\[
 q_{\rm readout}(\sigma_{AB})
 =\inf_{\{M_y\}_A}\sum_y p_yS(\sigma_{B|y}).
\]
For the uncertain-prefix state, giving the complete shared classical record
to Alice and Bob leaves this optimized quantity unchanged: every conditioned
state is the same queue, and Bob's classical record is known after Alice
includes that record in her outcome. A matched local-unitary rotation would
give the same conclusion by local-unitary invariance. Less available
classical information cannot improve on the optimum with the complete
record. Thus these classical outcomes do not provide a lower-readout-entropy
repair of the uncertain prefix.

This paragraph concerns classical records of the stated instruments. It
does not treat retained coherent quantum flags, enlarged output dimensions,
or extra quantum resources; those require a separate argument with all such
systems included in the resource and entropy bookkeeping.

For \(r\) independent output tasks, the argument applies to each task
when the processor is a product over pair positions and tasks, or a
shared-random mixture of such products. Joint operations coupling pairs
or tasks are not included.

For a nonuniform prior \(p_k\), the same induction is available whenever
the successive strict inequalities hold, using
\[
 \alpha_j=\sum_{k\ge j}p_k,\qquad
 \beta_j=\sum_{k<j}p_kq^{j-1-k}.
\]
Those inequalities can fail, so the uniform-prior conclusion must not
be transferred without checking them.

## 5. Consequences and unresolved scope

For \(N=L+1\), the terminal pair is deterministically \(\nu\), independent
of the uncertain prefix. Resetting it locally to a pure product is allowed,
leaves scores \(j\le L\) unchanged, and increases its Bell overlap from
\(D^{-2}\) to \(D^{-1}\). This removes \(2\log D\) of joint von Neumann
entropy from that known terminal factor. The argument above blocks
extending that reset to an uncertain position within the stated pairwise
model while preserving every actual prefix score.

If the processor is an arbitrary joint cross-pair LOCC channel, an adaptive
sequence of cross-pair instruments, a processor coupling output tasks, or a
state-dependent approximate repair, the queue induction above does not
apply. These questions remain open here. Approximate preservation also
requires a quantitative robustness analysis; the exact equality proof
must not be cited as such a bound.

The full-space SEP rigidity of Section 2 separately applies to joint
channels only when they exactly fix a maximally entangled state across
their entire unchanged input/output space. Fixing only a prefix does not
meet that hypothesis, because resetting an unconstrained suffix is possible.
