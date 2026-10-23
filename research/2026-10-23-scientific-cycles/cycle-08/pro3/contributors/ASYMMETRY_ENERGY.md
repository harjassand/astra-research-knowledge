# Finite reciprocal energy with a mismatched proposal exponent

Contributor: `/root/asymmetry_energy`. Scientific date: 22 October 2026.
Status: bounded independent finite-energy challenge and proof submitted to
the principal. Principal acceptance, a sharp minimax law, and lower-bound
attainment are not asserted here.

The exact predecessor read for this contribution is
`cycle7_pro3/research/RECIPROCAL_PROPOSAL_THEOREM.md`, especially its
Lemmas 2 and 3. No older proof audit or external work was performed.

## 1. Scope and notation

Retain the predecessor's finite positive native class: fixed `K>0`,
`0<alpha<1`, `beta=1-alpha`, positive probability vectors `pi,q` with
`D(pi||q)<=K`, initialization `q`, and a fixed target-independent
row-stochastic proposal `Q` with reciprocal off-diagonal support. All
kernels and parameters remain fixed within a run. Actual rejection
diagonals, the independence-MH kernel `G`, and the lazy random mixture

\[
 C=(I+\alpha G+\beta L)/2
\]

are retained. No support-size, proposal-degree, or minimum-atom bound is
imposed. Every required reverse proposal probability remains a genuine
evaluable quantity with its native cost.

For a positive off-diagonal proposal edge write

\[
 R_{xy}=Q_{yx}/Q_{xy},\qquad
 r_{xy}=q_yR_{xy}/q_x,\qquad
 t_{xy}=\pi_yR_{xy}/\pi_x.
\]

The changed first screen and accepted probability are

\[
 S_{xy}=(q_y/q_x)^\eta R_{xy}^{\kappa}
       =r_{xy}^{\eta}e^{\xi_{xy}},\qquad
 \xi_{xy}=(\kappa-\eta)\log R_{xy},
\]
\[
 a_{xy}=\min(1,S_{xy})\min(1,t_{xy}/S_{xy}),\quad
 L_{xy}=Q_{xy}a_{xy},\quad
 L_{xx}=1-\sum_{y\ne x}Q_{xy}a_{xy}.
\]

Let

\[
 A(Q)=\max_{x\ne y:Q_{xy}>0}|\log R_{xy}|\le A,
 \qquad \delta=\kappa-\eta,\qquad D=|\delta|A.
\]

For a proposal with no positive off-diagonal entries use `A(Q)=0`.
The argument uses `|xi_xy|<=D`, but this is derived from the genuine
proposal-ratio constraint. It does not redefine the class as one with
independently selectable edge perturbations.

Because `S_yx=1/S_xy` and `t_yx=1/t_xy`,

\[
 \frac{a_{xy}}{a_{yx}}
 =\frac{\min(1,S_{xy})}{\min(1,S_{xy}^{-1})}
  \frac{\min(1,t_{xy}/S_{xy})}{\min(1,S_{xy}/t_{xy})}
 =t_{xy}.
\]

Consequently `L`, `G`, and `C` have exactly the reversibility properties
used in the predecessor's full-return certificate. Laziness keeps the
spectrum of `C` in `[0,1]`.

## 2. Exact scalar envelope for the proposed local proof

Fix

\[
 0<\eta<1,\quad 0<\theta\le\eta,\quad \theta\le1/2,
 \quad p=(1-\theta)^{-1},\quad w\ge1,
\]
\[
 \tau=p(1-\theta/\eta)\in[0,1),\qquad
 U=w\exp(D\theta p/\eta)\ge1.
\]

Define

\[
 H_w(D)=\sup_{0<z\le1}(Uz^\tau-z).                 \tag{A1}
\]

**Scalar claim.** Whenever `r>0`, `|xi|<=D`, and
`0<=a<=min(1,r^eta exp(xi))`,

\[
 w a^p r^{-\theta p}-a\le H_w(D).                 \tag{A2}
\]

**Proof.** At fixed `r,xi`, the expression on the left is convex in `a`.
Its maximum over the permitted interval occurs at zero or at the upper
endpoint. Zero is harmless because `H_w(D)>=U-1>=0`.

If `r^eta exp(xi)<=1`, put `z=r^eta exp(xi)`. At the nonzero endpoint,

\[
 wa^pr^{-\theta p}-a
 =w e^{\xi\theta p/\eta}z^{p(1-\theta/\eta)}-z
 \le Uz^\tau-z\le H_w(D).
\]

If `r^eta exp(xi)>=1`, the nonzero endpoint is `a=1`. The screen
inequality gives `r>=exp(-xi/eta)`, so

\[
 wr^{-\theta p}-1\le w e^{\xi\theta p/\eta}-1
 \le U-1\le H_w(D).
\]

This is precisely the `z=1` endpoint already contained in (A1). Thus the
screened and unscreened regimes require no additional constant. QED.

### Explicit maximizing regimes

If `tau=0`,

\[
 H_w(D)=U=w e^{D\theta p/\eta}.                    \tag{A3}
\]

The supremum is approached as `z` decreases to zero and is not attained
on `0<z<=1`. No expression `0^0` is needed. At `theta=eta`, when this
choice is admitted by `theta<=1/2`, (A3) becomes `w exp(Dp)`.

If `0<tau<1`, differentiation gives the complete formula

\[
 H_w(D)=
 \begin{cases}
 U(1-\tau)(U\tau)^{\tau/(1-\tau)},&U\tau\le1,\\
 U-1,&U\tau\ge1.
 \end{cases}                                                   \tag{A4}
\]

For `U tau<1`, the unique maximizer is
`z_*=(U tau)^(1/(1-tau))` in `(0,1)`. For `U tau>1`, it is `z=1`.
At `U tau=1` both formulas give `U-1`, and the maximizer is again `z=1`.
Equivalently the interior regime is

\[
 D<\frac{\eta}{\theta p}\log\frac1{w\tau},
\]

when its right side is positive; otherwise the endpoint regime applies
for every `D>=0`. In particular `H_w(D)>=w-1>=0`. At `D=0`, (A3)-(A4)
reduce exactly to the predecessor's scalar formulas.

These are exact extrema of the relaxed scalar expression in (A1), not
claims about the norm of an entire proposal matrix or a mixing lower.

## 3. Full local energy, including actual rejection subtraction

Let the sets `A_0,E` be disjoint, put `S_0=A_0 union E`, and construct
`L^E` exactly as in predecessor Lemma 2: retain actual `L` entries from
rows `A_0` into `S_0`, kill the remaining outgoing mass, and make `E`
absorbing. Never renormalize a killed row. Use `A_0` here to distinguish
the proof set from the numerical proposal-asymmetry bound `A`.

Put

\[
 \mathsf D=\operatorname{diag}(q_x^\theta)_{x\in S_0},\qquad
 T=\mathsf D L^E\mathsf D^{-1},\qquad
 \mathcal E_w(v)=\sum_{A_0}|v_x|^p+w\sum_E|v_x|^p,
 \qquad \omega_x=1\ (x\in A_0),\quad \omega_x=w\ (x\in E).
\]

**Finite local lemma.** Every row vector `v` satisfies

\[
 \boxed{\mathcal E_w(vT)\le 2^{p-1}
       \left[(1+H_w(D))\sum_{A_0}|v_x|^p
                         +w\sum_E|v_x|^p\right].}             \tag{A5}
\]

**Proof.** At output `y`, use reverse-proposal Jensen coefficients
`B_xy=Q_yx` for retained off-diagonal edges from `A_0`; on the diagonal
use the actual `L_xx` for `x in A_0`, and one for `x in E`; set the
remaining entries to zero. Reciprocal support makes zero coefficients
harmless. The column coefficient total is bounded by two because the
off-diagonal coefficients come from the outgoing row of `Q` at `y`.
Thus

\[
 |(vT)_y|^p\le2^{p-1}\sum_{x:B_{xy}>0}
                   |v_x|^p T_{xy}^p/B_{xy}^{p-1}.
\]

Since `p-1=theta p`, the off-diagonal powered coefficient is still

\[
 \frac{T_{xy}^p}{B_{xy}^{p-1}}
 =Q_{xy}a_{xy}^p r_{xy}^{-\theta p}.             \tag{A6}
\]

Changing the first screen has not changed the algebraic ratio in (A6).
The diagonal powered coefficient is exactly `L_xx`, or one on `E`.
For an input `x in A_0`, multiply by the output weights, sum, and use
the actual diagonal to obtain

\[
 \begin{split}
 L_{xx}+\sum_{y\in S_0,y\ne x}\omega_yQ_{xy}a_{xy}^p
                   r_{xy}^{-\theta p}
 &\le1+\sum_{y\in S_0,y\ne x}Q_{xy}
            (w a_{xy}^p r_{xy}^{-\theta p}-a_{xy})\\
 &\le1+H_w(D).
 \end{split}                                                    \tag{A7}
\]

Accepted outflow into the killed complement was subtracted before its
nonpositive contribution was dropped. The second line uses (A2),
`H_w(D)>=0`, and `sum_{y!=x}Q_xy<=1`. For input `x in E`, its sole
entry is its absorbing diagonal, with weighted coefficient `w`.
This proves (A5) with finite nonnegative sums only. QED.

## 4. Absorption multiplier and unchanged original-chain certificate

Now take the actual proof set
`A_0={pi/q<h}`, `B_0=A_0^c`, `b=q(A_0)`, `E subset B_0`, and `e=q(E)`.
The killed global step and the initial transformed energy are unchanged.
Combining its predecessor bound with (A5) gives the valid multiplier

\[
 \Gamma_{\theta,w,D}(e)=\frac12+\frac{2^{p-1}}2
 \left(1+[\beta H_w(D)-\alpha(1-b)]_++\alpha we\right).         \tag{A8}
\]

Consequently the exact first-`B_0`-hit measure obeys

\[
 \Pr_q(X_0\in A_0,\tau_{B_0}\le N,X_{\tau_{B_0}}\in E)
 \le(b/w)^{1-\theta}e^\theta
                \Gamma_{\theta,w,D}(e)^{N(1-\theta)}.         \tag{A9}
\]

This includes all possible first-hit times in a single absorbing proof
counter. Empty `A_0` or `E` gives zero directly. The sampler is the
original chain throughout.

Every other premise of predecessor Lemma 3 has been retained: reversibility,
positive spectrum, the IMH Dirichlet lower bound, actual killed global
mass, initialization, and the population KL budget. Therefore its finite
certificate is valid with precisely the replacement
`Gamma_{theta,w} -> Gamma_{theta,w,D}`. Explicitly let

\[
 M=e^{2K+1},\quad a=\pi(\pi/q>R),\quad
 J=\frac{2}{\alpha(2(n-N)+1)},\quad
 \rho=1-\alpha(1-b)/2,
\]
\[
 \bar e=\min\left\{1-b,\frac aR+
        \frac{(N+1)(M/h+1)J}{d_{\rm test}^2}\right\}.
\]

For the admitted finite parameters,

\[
 \begin{split}
 \|qC^n-\pi\|_{TV}\le{}&a+\sqrt{(M+R)J}+d_{\rm test}
       +\bar e+b\rho^N\\
 &+(b/w)^{1-\theta}\bar e^\theta
               \Gamma_{\theta,w,D}(\bar e)^{N(1-\theta)}.
 \end{split}                                                    \tag{A10}
\]

The same original-chain continuation after each first hit, including
every later return, is the one in predecessor (18). No generic kernel
perturbation estimate, comparison to a different sampler, or telescoping
error of size `n times a one-step discrepancy` is used.

## 5. A support-uniform upper bound, uniform also in moving eta

This section allows every deterministic sequence `0<eta_n<1`, real
finite `kappa_n`, and finite `A_n>=0`. Each parameter is fixed during its
own run. It proves an upper bound, not its sharpness. Put

\[
 r_0=\alpha e^{-K}/\beta,\qquad
 \epsilon=\min\{1/4,r_0/8\}>0,\qquad c=\epsilon/4.
\]

Put `D_n=|kappa_n-eta_n|A_n` and
`v_n=eta_n log n/(1+D_n)`. For sufficiently large `n`, set `ell=log n`
and use

\[
 \theta_n=\frac{\eta_n\epsilon}{2(1+D_n)},\quad w=1,
 \quad h=\ell^{-2},\quad R=n/\ell^4,\quad d_{\rm test}=\ell^{-2},
\]
\[
 N=\left\lceil\frac{8}{\alpha e^{-K}}\log\ell\right\rceil.
                                                               \tag{A11}
\]

These proof parameters do not alter the actual sampler. They obey all
finite parameter restrictions eventually. In particular
`0<theta_n<=eta_n/8<1/2`. There is no positive lower bound on `eta_n`.

### Uniform scalar margin

Write

\[
 \lambda=D_n\theta_n p/\eta_n,\qquad
 c_{\rm eff}=1-\tau=\theta_n p(1-\eta_n)/\eta_n.
\]

Since `p<=2`, both `lambda<=epsilon` and `c_eff<=epsilon` hold.
Using `0<z<=1` and the predecessor's elementary
`sup(z^(1-c)-z)=F(c)<=c`,

\[
 H_1(D_n)\le e^\lambda-1+F(c_{\rm eff})
 \le e^\epsilon-1+\epsilon\le3\epsilon\le3r_0/8.             \tag{A12}
\]

The same-instance binary KL bound gives

\[
 -\log(1-b)\le k_h=\frac{K+H_2(h)}{1-h}
                 =K+O_K(\ell^{-2}\log\ell).
\]

Thus `1-b>=e^(-K)/2` eventually, uniformly over the class, and

\[
 \Delta_n=[\beta H_1(D_n)-\alpha(1-b)]_+=0.       \tag{A13}
\]

The strict margin in (A12) avoids any need to balance an accumulated
positive-part error against `N`.

### KL tail, tests, and residual

The predecessor's binary tail bound is

\[
 a\le\frac K{\log R-1}
     =\frac K{\ell-4\log\ell-1}.                 \tag{A14}
\]

Because `N=O_{K,alpha}(log ell)` and `J=O_alpha(1/n)`, there is a constant
`C_0=C_0(K,alpha)` such that, eventually and uniformly,

\[
 \bar e\le e_n:=C_0\ell^6\log\ell/n,\qquad
 \sqrt{(M+R)J}+d_{\rm test}+\bar e=O_{K,\alpha}(\ell^{-2}).
                                                               \tag{A15}
\]

An upper bound on `bar e` suffices; no lower bound on `q(E)` or minimum
atom is being assumed. Also

\[
 b\rho^N\le\exp(-\alpha e^{-K}N/4)\le\ell^{-2}.             \tag{A16}
\]

Thus the proof horizon grows enough to remove the initial bad-set
residual while its union of `N+1` tests costs only the factor `log ell`
already present in (A15).

### The accumulated multiplier is controlled, not silently discarded

From (A8), (A13), `p-1=theta_n p`, and `b<=1`,

\[
 \Gamma_{\theta_n,1,D_n}(\bar e)^{N(1-\theta_n)}
 \le\exp\{N\theta_n\log2+\alpha N\bar e\}.                   \tag{A17}
\]

Therefore the last term of (A10) is at most

\[
 \begin{split}
 e_n^{\theta_n}\exp\{N\theta_n\log2+\alpha N e_n\}
 =\exp\big\{&-\theta_n\ell+
 \theta_n(\log C_0+6\log\ell+\log\log\ell+N\log2)\\
 &+\alpha N e_n\big\}.
 \end{split}                                                    \tag{A18}
\]

The parenthesized positive term is `O_{K,alpha}(log ell)=o(ell)`;
`N e_n` tends to zero. Hence, for all sufficiently large `n`, uniformly
in every nonnegative `D_n`, (A18) is bounded by

\[
 2\exp(-\theta_n\ell/2)
 =2\exp(-c v_n).                                              \tag{A19}
\]

For fixed positive `eta` and bounded `D_n`, `N theta_n` diverges, so it would be
incorrect to state that the accumulated multiplier tends to one.
Its logarithm is smaller than the main decay exponent by the factor
`O(log ell/ell)`, which is the estimate actually used.

### Uniform conclusion

There are constants `C<infinity` and `n_0`, depending only on `K,alpha`,
such that for `n>=n_0`,

\[
 \boxed{
 \sup_{\substack{\text{native finite class}\\A(Q)\le A_n}}
 \|qC^n-\pi\|_{TV}
 \le \frac K{\ell-4\log\ell-1}
       +\frac C{\ell^2}
       +2\exp\left[-\frac{c\eta_n\ell}
                              {1+|\kappa_n-\eta_n|A_n}\right].}
                                                               \tag{A20}
\]

The right side may be capped at one. Constants do not depend on support
size, proposal degree, minimum atom, the particular instance, `eta_n`,
`kappa_n`, or `A_n`. This
bound explicitly includes the proof horizon, multiplier, cutoff `h`,
test union, KL tail, and original-chain returns.

Therefore `v_n -> infinity` implies uniform convergence. The stronger
condition `v_n/log log n -> infinity` makes the exponential in (A20)
smaller than any fixed negative power of `log n`, and yields

\[
 \limsup_{n\to\infty}(\log n)
 \sup_{A(Q)\le A_n}\|qC^n-\pi\|_{TV}\le K.                   \tag{A21}
\]

For fixed `0<eta<1` and real `kappa`, `A_n=o(log n)` implies
`v_n -> infinity`; hence this includes the requested fixed-policy
convergence implication. If `kappa_n=eta_n`, `D_n=0` irrespective of
proposal asymmetry, and the sufficient convergence condition becomes
`eta_n log n -> infinity`. For fixed `eta`, the stronger condition
`D_n=o(log n/log log n)` implies (A21).

Only convergence, not (A21), follows from `D_n=o(log n)` alone with fixed
`eta`. For example `D_n=log n/sqrt(log log n)` makes the displayed
transport bound decay more slowly than `1/log n`. With moving `eta_n`,
`D_n=o(log n)` alone need not even make `v_n` diverge. These are exact
limits of the stated implication, not claims of corresponding lower
behavior. The upper proof accommodates negative `kappa_n`; it does not
assert that any lower or sharp law under a nonnegative-exponent contract
extends to negative exponents.

## 6. Challenge to any sharpness inference from H_w(D)

The finite conjecture survives the algebraic challenge. The following
additional inferences do not follow from it.

1. **The sign of delta is erased only in this upper envelope.** Achieving
   `xi=D` requires `R_xy=exp(A)` if `delta>0`, and `R_xy=exp(-A)` if
   `delta<0`. These are different orientations of the native proposal
   budget. If `delta>0`, the individual forward probability obeys
   `Q_xy<=exp(-A)`; if `delta<0`, the individual reverse probability
   obeys `Q_yx<=exp(-A)`. Row normalization and reciprocity are genuine
   simultaneous constraints.

2. **The maximizing q ratio is coupled to that orientation.** At an
   endpoint with `S_xy=z<=1` and `xi=D`,

   \[
   q_y/q_x=z^{1/\eta}R_{xy}^{-\kappa/\eta}.
   \]

   Thus the total probability mass of all sources or destinations must
   be checked after choosing degrees, edge probabilities, and actual
   per-vertex atoms. A scalar `r` or a level-total mass ratio cannot be
   substituted for this native per-edge constraint.

3. **Row saturation and Jensen saturation are separate.** The proof uses
   the scalar maximum on every retained edge, the upper row budget one,
   the reverse-column Jensen budget two, the larger output weight `w`,
   and a positive-part relaxation in the mixture. Those extrema need
   not occur on a common full finite instance. Unbounded degree can
   help some local budget constructions, but is not a proof of full-law
   attainment.

4. **The second acceptance stage and population KL budget remain.** The
   envelope uses only `a<=min(1,S)`. Achieving this endpoint requires the
   appropriate target ratio on every relevant edge; an admissible lower
   must then check one population KL budget, positive native atom
   values, exact lumping if used, and original-chain returns.

5. **The coarse constants in (A20) have no sharpness claim.** Their role
   is to give a support-uniform convergence implication under
   sublogarithmic asymmetry. A sharp law or a necessary threshold at
   logarithmic asymmetry requires an independent admitted lower and
   possibly a less lossy upper argument.

These points explain why the result is a proved finite extension plus a
uniform convergence guarantee, rather than a claimed sharp theorem for
all exponent pairs or asymmetry-growth regimes.
