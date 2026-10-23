# Independent challenge of the all-qutrit corrected-depth obstruction

Reviewer: `/root/coherent_stability`  
Date: 22 October 2026 (Brisbane)  
Status: **internal mathematical acceptance of the exact algebra, spectral-Schur bridge, boundary term and normal-state consequences stated here.** The root retains the main construction and its separate exponential-tilt proof. This note does not certify that latter proof merely from its proposed conclusion.

## Claim being checked

For the actual fixed two-seed Fock bath and `V=alpha U+i beta I`, with `0<=beta<=1/4`, let `rho` be a fixed qutrit port density used independently at every call. The root proposes that the spectral window

\[
 \frac16 I<\rho<\frac12 I
 \tag{1}
\]

implies a bounded correction to depth whose exact one-step increment is uniformly positive. The condition `H_2(rho)>3/2` implies (1), so the result applies to every fixed iid port density of entropy strictly above the completed capacity floor.

This is an iid reduced-bath theorem. It is not a quantum capacity converse, and it cannot be applied to a code merely because individual port marginals have high entropy: those inputs may be correlated across time and with the evolving bath.

## 1. Basis change is a representation change only

Write the port density in zero/color blocks as

\[
 \rho=\begin{pmatrix}q&\gamma^*\\\gamma&A\end{pmatrix},
 \qquad A>0.
\]

Diagonalize the two-dimensional color block, and adjust the phases of its two eigenvectors so that the transformed vector is `gamma_j=-i g_j`, with `g_j>=0`. The color block remains diagonal, `A=diag(a1,a2)`, with `a1+a2=1-q`.

If the new color basis vectors are `|j'>=sum_a W_aj|a>`, the creation operators in the same expression for `U` become `S'_j=sum_a W_aj S_a`. They obey all the same Cuntz--Toeplitz relations:

\[
 S_i'^*S_j'=\delta_{ij}I,\qquad\sum_jS'_jS_j'^*=I-P_0,
 \qquad RS'_j=S_j'^*R=0.
\]

The endomorphism `C(Z)=sum_j S_j Z S_j*`, all depth projections, and the vacuum exchange are unchanged. No port operation, bath preparation or bath access is being inserted. The actual `tau_pi` is unchanged as well. Primes are dropped below.

## 2. The resolvent and the crossed color denominator

Let `p=1-q` and `r=q/p`. By (1), `q<1/2`, so `r<1`. Define

\[
 S_g=g_1S_1+g_2S_2,\qquad
 f_1=\frac{g_1}{a_2},\quad f_2=\frac{g_2}{a_1},\qquad
 S_f=f_1S_1+f_2S_2,
\]

and the norm-convergent bounded operator

\[
 B_f=\sum_{k=0}^\infty r^k\mathcal C^k(S_f),
 \qquad\|B_f\|\le\frac{\|f\|_2}{1-r}.
 \tag{2}
\]

The crossed denominator is essential. For the diagonal part of the bath channel, at level `k=0`,

\[
 \sum_j a_j S_j^*S_fS_j=S_{Af};
\]

at every `k>=1`,

\[
 \sum_j a_j S_j^*\mathcal C^k(S_f)S_j
 =p\mathcal C^{k-1}(S_f).
\]

Thus `(I-T_0*)B_f=S_{(pI-A)f}=S_g`, because `pI-A=diag(a2,a1)`. Replacing `a_(3-j)` by `a_j` would fail for unequal colors.

## 3. Independent derivation of the full corrector identity

The exact reduced channel has the same form as in the special-family note,

\[
 \Phi(\tau)=\beta^2\tau+\alpha^2T(\tau)-i\alpha\beta[h,\tau],
 \qquad h=qR+i(S_g^*-S_g),
\]

now with `a sum S_a tau S_a*` replaced by `sum a_j S_j tau S_j*` and the corresponding `g_j` root terms. Put `D_g=S_g^*-S_g`. Direct multiplication gives

\[
 \boxed{(I-\Phi^*)B_f
 =\alpha^2S_g+i\alpha\beta qS_fR
   -i\alpha^2(g\cdot f)R
   +\alpha\beta[D_g,B_f].}
 \tag{3}
\]

Checks of the delicate terms:

- The real root-coherence source is zero because `g dot f` is real and `R` is self-adjoint; it must be kept until this real-part step.
- The `qR` Hamiltonian contributes the `S_f R` term because `RB_f=0` and `B_fR=S_fR`.
- All higher insertion levels vanish on the two vacuum vertices, so no additional root term is hidden in the infinite sum.
- The series in (2) converges in norm, permitting the bounded channel and commutators to act term by term.

## 4. A uniform commutator bound

The exact insertion identities are

\[
 S_g^*B_f=(g\cdot f)I+rB_fS_g^*,
 \qquad B_fS_g=S_fS_g+rS_gB_f.
\]

They imply

\[
 [D_g,B_f]=(g\cdot f)I+S_fS_g
              -(1-r)(B_fS_g^*+S_gB_f).
 \tag{4}
\]

Because `||S_g||=||g||_2`, `||S_f||=||f||_2` and `(1-r)||B_f||<=||f||_2`,

\[
 \boxed{\|[D_g,B_f]\|\le4\|g\|_2\|f\|_2.}
 \tag{5}
\]

This bound has no `1/(1-r)` divergence. Taking a naive norm estimate before applying the insertion identities would lose exactly the useful cancellation.

## 5. Corrected drift, including the exceptional-root cost

Define

\[
 X=\operatorname{Re}B_f,\qquad
 H=L-\frac{2\beta}{\alpha}X,
 \qquad Y_f=\frac i2(RS_f^*-S_fR).
\]

Using the exact depth drift and the real part of (3), the `Re S_g` terms cancel and give

\[
 \Phi^*H-H
 =\alpha^2(1-2q)I+\alpha^2qP_0
       -2\beta^2qY_f
       +2\beta^2\operatorname{Re}[D_g,B_f].
 \tag{6}
\]

For `J=S_fR`, `J*J=||f||_2^2 P0`. Completion of the square between the vacuum and `J`-image components yields

\[
 \alpha^2qP_0-2\beta^2qY_f
 \ge-\frac{\beta^4q\|f\|_2^2}{\alpha^2}I.
 \tag{7}
\]

Together with (5), this proves the proposed bound

\[
 \boxed{\Phi^*H-H\ge\nu I,\quad
 \nu=\alpha^2(1-2q)-8\beta^2\|g\|_2\|f\|_2
          -\frac{\beta^4q\|f\|_2^2}{\alpha^2}.}
 \tag{8}
\]

This review independently confirms the coefficient of the root correction. It is not legitimate to erase the root exchange and use only the bulk cancellation.

## 6. The spectral-Schur bridge

Under (1), compression to the color subspace gives `a_j>1/6` and `a_j<1/2`, hence `||f||_2<=6||g||_2`. Let `delta=1/2-q>0`. Positivity of the entire block matrix

\[
 \frac12 I-\rho
 =\begin{pmatrix}\delta&-\gamma^*\\-\gamma&D\end{pmatrix},
 \qquad D=\frac12I-A,
\]

gives by the Schur complement

\[
 \delta>\gamma^*D^{-1}\gamma\ge3\|g\|_2^2,
 \tag{9}
\]

because `0<D<(1/3)I`. The last inequality is strict when `g` is nonzero; the weak form suffices, and when `g=0` we still have `delta>0`.

Substituting `q<1/2`, `||f||<=6||g||` and `||g||^2<delta/3` into (8) gives

\[
 \nu\ge\delta\left(2\alpha^2-16\beta^2
                         -\frac{6\beta^4}{\alpha^2}\right).
 \tag{10}
\]

Writing `x=beta^2`, the bracket is `2-18x-6x^2/(1-x)`, decreasing on `0<=x<=1/16`. At `x=1/16` it equals `17/20`. In particular,

\[
 \boxed{\nu\ge\frac45\delta>0\qquad(0\le\beta\le1/4).}
 \tag{11}
\]

The conservative `4/5` coefficient is enough for the theorem. At `beta=0`, some intermediate strict inequalities become equalities; (10) is correctly stated with `>=`, and (11) remains valid.

## 7. Why strict input entropy above 3/2 supplies the spectral window

Let `m` be an extreme eigenvalue of a three-dimensional density. At fixed `m`, concavity of entropy bounds the other two eigenvalues by taking them equal, giving

\[
 H_2(\rho)\le h_2(m)+(1-m).
\]

If the largest eigenvalue were at least `1/2`, the right side would be at most `3/2`: its derivative is `log2((1-m)/m)-1<0` for `m>=1/2`. Thus `H_2(rho)>3/2` forces `rho<(1/2)I`.

If the smallest eigenvalue were at most `1/6`, maximizing the same expression on `0<=m<=1/6` gives

\[
 H_2(\rho)\le h_2(1/6)+5/6<3/2.
\]

For the strict last inequality, exponentiating after multiplying by `6 ln2` reduces it to the exact integer inequality

\[
 6\left(\frac{12}{5}\right)^5<512,
 \qquad 1{,}492{,}992<1{,}600{,}000.
\]

Therefore `H_2(rho)>3/2` implies both strict inequalities in (1). No numerical entropy approximation or noncommutative Pinsker inequality is needed for this bridge.

The spectral window is itself the reusable sufficient hypothesis. The proof should not assert that it is equivalent to `H_2(rho)>3/2`.

## 8. Normal-state consequences and precise limitations

The corrected drift is bounded. Taking `H_M=min(L,M)-(2beta/alpha)X`, the inherited capped-depth increment bound gives uniformly bounded increments converging strongly to (6). Against any hypothetical normal invariant density, each capped increment has expectation zero; normality permits the limit, contradicting (11). This covers invariant densities of infinite depth expectation.

The channel has at most nine bounded Kraus operators and consequently preserves compact operators in the dual. The Cesaro means of any normal orbit have approximate invariance in trace norm, with error at most `2/N`. Their weak-star cluster points as trace-class operators acting on compact operators are invariant positive trace-class operators of trace at most one. There is no nonzero such point, because it could be normalized to an invariant density. Hence all Cesaro means converge weak-star to zero, and their mass on each finite-rank projection tends to zero. In particular, no normal orbit is uniformly tight.

These conclusions agree with the complete proofs in `coherent_stability.md`, Sections 7 and 8, with the new `H` and `nu` substituted. They are weaker than the root's targeted pointwise exponential escape. No-normal-invariant-state alone is insufficient to refute a communication code: the already successful critical input can spread sublinearly without a normal limiting bath. A ballistic/quantitative estimate is needed for the proposed coordinate-compression obstruction.

Even a ballistic escape theorem for every iid high-entropy input is still not a converse for all correlated communication codes, nor does it prove that extensive depth necessarily means uncorrectable information. Those distinctions remain essential.

## 9. Scope of independent work and costs

I independently recomputed the color-basis transformation, diagonal and coherent contributions to `Phi*B_f`, the crossed denominator, the commutator cancellation, and the exceptional-root completion of squares. I then checked both spectral extrema and the Schur-complement argument. The all-qutrit construction and spectral-Schur proposal originated with the root; this review is an independent check of the load-bearing steps, not a claim of independent historical discovery.

No additional numerical replay was required for this general-family proof. No external source, purchase, hardware credit or outreach was used. Total inference time, token use and discovery cost are not independently metered. Internal acceptance is not external certification, publication priority or an efficient physical implementation.
