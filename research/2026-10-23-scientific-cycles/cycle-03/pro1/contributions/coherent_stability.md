# Corrected-depth obstruction for the entire high-entropy coherent iid family

Contributor: `/root/coherent_stability`  
Date: 22 October 2026 (Brisbane)  
Status: independently derived corrector algebra and boundary estimate; full analytic entropy extension and normal-state/Cesaro consequences. The root owns the main corrected-depth/tilted-escape construction. This note is a distinct challenge and family extension, not another audit of the inherited capacity floor.

## 1. Exact contract and result

Let the bath be the supplied two-seed binary Fock space. The creation isometries satisfy

\[
 S_i^*S_j=\delta_{ij}I,\qquad \sum_iS_iS_i^*=I-P_0,
 \qquad R^*=R,\quad R^2=P_0,
\]

where `R` swaps the two vacuum vertices and vanishes elsewhere. Let `L` be word depth. Keep the supplied

\[
 U=\begin{pmatrix}R&S_1&S_2\\S_1^*&0&0\\S_2^*&0&0\end{pmatrix},
 \qquad V=\alpha U+i\beta I,\quad \alpha=\sqrt{1-\beta^2}>0.
\]

For this note take the fixed iid port density

\[
 \rho=\begin{pmatrix}q&ig&0\\-ig&a&0\\0&0&a\end{pmatrix},
 \qquad a=(1-q)/2,\quad g\in\mathbb R,
\]

with positivity assumed. Let `Phi` be the exact reduced bath channel. No bath reset or finite reflecting approximation is made.

**Family obstruction.** If `H_2(rho)>3/2` and `0<=beta<=1/3`, there is a bounded self-adjoint `X` and a real finite `c` such that the bounded depth increment of `H=L-cX` obeys

\[
 \Phi^*H-H\ge\nu I,\qquad \nu>\frac45\left(\frac12-q\right)>0.
\]

Consequently this bath channel has no normal invariant density. No orbit of a normal initial density is uniformly tight. In fact, for every finite-rank bath projection `P` and every normal initial density `tau`,

\[
 \lim_{N\to\infty}\frac1N\sum_{n=0}^{N-1}\operatorname{Tr}\bigl(P\Phi^n(\tau)\bigr)=0.
\]

This is an iid-input stability obstruction, **not** a capacity converse. It does not exclude arbitrary correlated input code families, other environment compression, or recovery with an extensive environment. The root's separate exponential-tilt argument can supply a stronger pointwise escape statement when its hypotheses are checked.

The concrete seed in the continuation belongs to this high-entropy family at `beta=1/512`. Its actual initializer remains `tau_pi`. The normal-state conclusions above do not require replacing that initializer by an analytic invariant state.

## 2. Exact reduced channel and phase sign

Write

\[
 h=qR+ig(S_1^*-S_1).
\]

Direct expansion of the supplied unitary gives

\[
 \Phi(\tau)=\beta^2\tau+\alpha^2T(\tau)-i\alpha\beta[h,\tau],
\]

where

\[
 T(\tau)=qR\tau R+q\sum_aS_a^*\tau S_a
       +a\sum_aS_a\tau S_a^*
       +igR\tau S_1^*-igS_1\tau R.
\]

Thus `Phi*(Z)=beta^2 Z+alpha^2 T*(Z)+i alpha beta[h,Z]`. In particular the Hamiltonian contribution to `Phi*(S1)` is

\[
 -i\alpha\beta qS_1R-\alpha\beta g(I-S_1S_1^*).
\]

From the diagonal actual `tau_pi`, the first generated real `S1` coherence is negative for `g>0`. The sign is opposite to the positive real coherence that would cancel the positive diagonal drift. This first-step observation alone is not the theorem; the corrected-depth calculation below controls the accumulated dynamics.

## 3. A bounded Poisson corrector

Since high entropy will force `q<1/2`, put

\[
 r=\frac{q}{1-q}<1,\qquad
 \mathcal C(Z)=\sum_aS_aZS_a^*,\qquad F_k=\mathcal C^k(S_1),
\]

and define

\[
 B=\sum_{k=0}^{\infty}r^kF_k,
 \qquad X=\operatorname{Re}B.
\]

The series converges in operator norm, with `||B||<=1/(1-r)`. Each `F_k` inserts color 1 after the first `k` letters of a word, and annihilates words shorter than `k`. Both seed sectors are present. The relations

\[
 \mathcal C(F_k)=F_{k+1},\qquad
 \sum_aS_a^*F_kS_a=2F_{k-1}\quad(k\ge1),\qquad
 \sum_aS_a^*F_0S_a=F_0
\]

are exact. Also `RF_k=F_kR=0` for `k>=1`, and `RS1=S1*R=0`.

For the real parts, the `ig` root terms in `T*` cancel: at `F0` they give `igR`, whose real part is zero, and for `k>=1` they vanish. The diagonal part of the reduced channel therefore satisfies

\[
 (\beta^2I+\alpha^2T_{g=0}^*)X-X=-\alpha^2 a\operatorname{Re}S_1.
\]

To see the telescoping coefficient exactly, the coefficient of `F0` in `(I-T_0*)B` is `1-a-(1-q)r=a`; the coefficient of every `F_k`, `k>=1`, is

\[
 r^k-qr^{k-1}-(1-q)r^{k+1}=0.
\]

Define the self-adjoint boundary operator

\[
 Y=\frac{i}{2}(RS_1^*-S_1R)
\]

and the self-adjoint commutator

\[
 A=[S_1^*-S_1,X].
\]

The full exact identity is

\[
 \boxed{\Phi^*X-X=-\alpha^2a\operatorname{Re}S_1
                +\alpha\beta qY-\alpha\beta gA.}
\]

The root exchange cannot be dropped: it is exactly the `Y` term.

## 4. A uniform commutator bound despite a large corrector

The norm of `B` grows as `q` approaches `1/2`, so the naive commutator bound would lose the result. Instead use the exact insertion identities

\[
 S_1^*B=I+rBS_1^*,\qquad BS_1=S_1^2+rS_1B.
\]

They yield

\[
 A=I+\frac{S_1^2+S_1^{*2}}2
 -\frac{1-r}{2}
 \bigl(BS_1^*+S_1B^*+S_1B+B^*S_1^*\bigr).
\]

As `(1-r)||B||<=1`, it follows that

\[
 \boxed{\|A\|\le4.}
\]

This bound is independent of the distance to criticality. It is the useful cancellation in the corrector, rather than an unjustified iteration of a one-step contraction of `S1`.

## 5. Boundary completion and positive corrected drift

The exact depth increment is

\[
 \Phi^*L-L=\alpha^2(1-2q)I+\alpha^2qP_0
                -2\alpha\beta g\operatorname{Re}S_1.
\]

Set

\[
 c=\frac{2\beta g}{\alpha a},\qquad H=L-cX.
\]

The unbounded domain is `Dom L`; `X` is bounded. The `Re S1` terms cancel exactly:

\[
 \Phi^*H-H=\alpha^2(1-2q)I+\alpha^2qP_0
              -\frac{2\beta^2gq}{a}Y
              +\frac{2\beta^2g^2}{a}A.
\]

For the boundary estimate let `J=S1R`. Then `J*J=P0` and `JJ*=S1P0S1*`. For any vector, completing the square between its vacuum component and its `J`-image component gives

\[
 \alpha^2qP_0-\frac{2\beta^2gq}{a}Y
 \ge-\frac{\beta^4g^2q}{\alpha^2a^2}JJ^*
 \ge-\frac{\beta^4g^2q}{\alpha^2a^2}I.
\]

For `q=0` the entire boundary expression is zero, so the same final inequality is valid by direct interpretation. Combining it with `||A||<=4` proves

\[
 \boxed{\Phi^*H-H\ge\nu I,\quad
 \nu=\alpha^2(1-2q)-\frac{8\beta^2g^2}{a}
      -\frac{\beta^4g^2q}{\alpha^2a^2}.}
\]

This independently confirms the root's coefficient, including the `beta^4` boundary term. For the selected seed, `||cX||<=8/(3 alpha)`. In the full family the bound is finite for each fixed input but need not be uniform as `q` tends to `1/2`.

## 6. An elementary entropy inequality makes the drift positive throughout the high-entropy family

Pinching the zero/color coherence gives

\[
 H_2(\rho)\le h_2(q)+1-q.
\]

The right side is at most `3/2` for `q>=1/2`. Thus `H_2(rho)>3/2` implies `q<1/2`. Put `delta=1/2-q>0` and `b=q+a=(1+q)/2<=3/4`.

Here one can prove the needed coherence-entropy penalty directly, without importing a separate quantum Pinsker theorem. Let `x=g^2`, `t=sqrt((q-a)^2+4x)`, and

\[
 \lambda_\pm(x)=\frac{b\pm t}{2}.
\]

The natural-log entropy loss from pinching is

\[
 G(x)=\lambda_+(x)\ln\lambda_+(x)+\lambda_-(x)\ln\lambda_-(x)
                -q\ln q-a\ln a.
\]

It has `G(0)=0`, and, in the interior of the positivity interval,

\[
 G'(x)=\frac1t\ln\frac{b+t}{b-t}\ge\frac2b,
\]

because `ln((1+u)/(1-u))>=2u` for `0<=u<1`. Degenerate endpoints follow by continuity. Integrating gives

\[
 H_2(\operatorname{diag}\rho)-H_2(\rho)
 =\frac{G(g^2)}{\ln2}\ge\frac{2g^2}{b\ln2}
 \ge\frac{8g^2}{3\ln2}.
\]

Since `h2(q)<=1`, strict high entropy requires

\[
 \boxed{g^2<\frac{3\ln2}{8}\,\delta.}
\]

Using `a>=1/4`, `q/a^2<=8`, and `1-2q=2delta` in the drift bound yields

\[
 \nu>\delta\left(2\alpha^2-12\beta^2\ln2
                      -\frac{3\beta^4\ln2}{\alpha^2}\right).
\]

For `beta<=1/3`, the bracket is at least

\[
 \frac{16}{9}-\frac{11}{8}\ln2>\frac45.
\]

For example, the elementary bound `ln2<7/10` makes the last expression larger than `587/720>4/5`. This proves the stated uniform positive coefficient. The interval `beta<=1/3` is a convenient conservative range, not an optimized endpoint claim.

## 7. No normal invariant density, including infinite-depth states

Let `L_M=min(L,M)`. The one-step differences `Phi*L_M-L_M` are uniformly bounded and converge strongly to the bounded depth increment, as in the actual inherited drift proof. Since `X` is bounded, the same is true for `H_M=L_M-cX` and the corrected increment.

If a normal density `sigma` were invariant, every bounded `H_M` would satisfy

\[
 \operatorname{Tr}\sigma(\Phi^*H_M-H_M)=0.
\]

Uniform boundedness and strong convergence allow passage to the limit against normal trace-class `sigma`, giving

\[
 0=\operatorname{Tr}\sigma(\Phi^*H-H)\ge\nu>0,
\]

a contradiction. No finite entropy or finite mean depth of `sigma` was assumed. The argument never subtracts two infinite expectations.

For an initial state with finite mean depth, ordinary telescoping also gives

\[
 \operatorname{Tr}(\Phi^n(\tau)L)
 \ge\operatorname{Tr}(\tau L)+n\nu-2|c|\|X\|.
\]

That mean-growth estimate alone would not prove escape or lack of tightness; the invariant-state argument below supplies the stronger normal-state conclusion.

## 8. No uniformly tight orbit and Cesaro escape from finite projections

The finite qutrit input/output and finite-rank port state give a Kraus representation of `Phi` with at most nine bounded operators. Consequently `Phi*` maps compact bath operators to compact bath operators. This fact is specific enough to avoid a hidden compactness-continuity assumption.

Let

\[
 \sigma_N=\frac1N\sum_{n=0}^{N-1}\Phi^n(\tau).
\]

Then `||Phi(sigma_N)-sigma_N||_1<=2/N`. Regard trace-class operators as the Banach dual of compact operators. The positive unit ball is compact in this weak-star topology; on the separable bath, bounded sequences have weak-star convergent subsequences. Any cluster point `sigma` is a positive trace-class operator of trace at most one. Compact-preservation by `Phi*` makes `Phi` weak-star continuous for this topology, so the `2/N` identity implies `Phi(sigma)=sigma`.

If `sigma` were nonzero, normalizing its trace would produce a normal invariant density, which was excluded above. Thus zero is the only cluster point. It follows that `sigma_N` converges weak-star to zero. Pairing with any finite-rank `P` proves

\[
 \frac1N\sum_{n=0}^{N-1}\operatorname{Tr}(P\Phi^n(\tau))\longrightarrow0.
\]

Uniform tightness of the orbit would supply some finite-rank `P` whose mass is, say, at least `1/2` at every time, contradicting this limit. The conclusion applies to every normal initializer, including the actual `tau_pi`.

This is Cesaro escape. Pointwise escape, an exponential low-depth estimate, or a coding upper bound requires additional arguments and is not inferred from this compactness proof.

## 9. An explored stronger commutator route that is not used

The exact commutator `A` above appeared positive in small exact-principal-section numerical probes. I did not obtain an all-length proof of `A>=0`, so the theorem uses only the proven `||A||<=4`. The computations were finite principal sections of the infinite algebra with a two-level guard, not a reflecting bath or a stationary-state simulation. They cannot establish global operator positivity. The exploratory script and output are separate; this unproved strengthening is unnecessary for the entropy-family obstruction.

## 10. Observed resources and receiving use

The substantive contribution is analytic: insertion-operator identities, the cancellation giving a uniform commutator bound, boundary completion of squares, an elementary entropy-loss estimate, and trace-class compactness consequences. No primary-literature theorem beyond standard operator/functional calculus is needed for these derivations. Historical priority is not assessed by this note.

One exploratory Python principal-section calculation was observed at 0.404209657 seconds command wall time by the execution tool. It used NumPy/SciPy, depths 3 through 6, and r values 0.2, 0.7 and 0.99. Its CPU/RSS and total inference/search/reading/discovery cost were not independently measured. No purchase, remote job, new hardware credit, disclosure or outreach was used.

Receiving use: combine the exact `nu` estimate with the root's separately proved tilted-escape lemma if its hypotheses hold. This upgrades the seed-specific obstruction to the entire stated fixed iid family. Keep the capacity question open; do not infer a converse from the failure of this sufficient bath-compression mechanism.
