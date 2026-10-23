# Strong-distortion upper: the logarithmic transport exponent

Contributor: `/root/cycle9_upper`, 22 October 2026 UTC.
Bounded assignment: challenge and prove the new upper interface; no lower
construction or historical-priority claim is made in this note.

## Sources actually read and status

The exact owned predecessor is
`Astra_Amplification_Cycle8_PRO3_20261022.zip`. I read Sections 3–5 and
the two-state lower in Section 5 of its `ASYMMETRY_BUDGET_THEOREM.md`,
SHA256
`eba1595d9efec9c7dc8ac5c97257a9f0bf741f1f7931105114dc58faeae9e6c1`.
I also read `INFORMATION_AND_COST_CONTRACT.md`, SHA256
`42bf08bf07856c5e0f385a6f888ffe5102db54d510c297f6528b9e1f7064f9ae`.
Those exact originals were not changed. The load-bearing inherited facts
are the distorted finite energy bound (10)–(16), the full-return
certificate (18), and the binary KL inequalities (21).

The argument below finds no defect in the proposed strict-exponent upper.
In fact its endpoint can be justified directly from the *finite* envelope:
the positive part need not vanish exactly, because its accumulated excess
is small. This does not substitute an endpoint into a theorem requiring a
strict inequality. Its finite hypotheses are checked below.

## 1. Model and result

Use the unchanged native model: finite labelled positive probability
vectors pi,q, one population `D(pi||q)<=K`, fixed K>0, fixed
`0<alpha<1`, beta=1-alpha, proposal initialization q, and a fixed
target-independent row-stochastic reciprocal-support Q. At horizon n,
the public deterministic policy is `0<eta_n<1`, finite `kappa_n>=0`,
finite `A_n>=0`, with the actual reciprocal proposal bound at most A_n.
The local first screen is

\[
 S_{xy}=(q_y/q_x)^{\eta_n}(Q_{yx}/Q_{xy})^{\kappa_n},
\]

and the second factor completes the true target Hastings ratio. Its
actual rejection diagonal is retained. Write

\[
 C=(I+\alpha G+\beta L)/2,\qquad
 \mathscr R_n=\sup\|qC^n-\pi\|_{\rm TV},
\]

with the same admitted class and half-l1 convention as the predecessor.
Put

\[
 \ell=\log n,\quad L=\log\ell,\quad
 D_n=|\kappa_n-\eta_n|A_n,\quad
 v_n=\frac{\eta_n\ell}{1+D_n},
\]
\[
 r_0=\frac{\alpha e^{-K}}\beta,
 \qquad\gamma_* =\log(1+r_0)>0.
\]

**Upper proposition.** Suppose

\[
 D_n\longrightarrow\infty,\qquad
 \frac{v_n}{\log\log n}\longrightarrow\lambda\in(0,\infty).
                                                               \tag{U1}
\]

Then, uniformly over all admitted finite instances at each n,

\[
 \boxed{\mathscr R_n\le
 \frac K{\ell-4\log\ell-1}+O_{K,\alpha}(\ell^{-2})
 +\exp\!\left\{-\gamma_*\frac{\eta_n\ell}{D_n}+o(1)\right\}.}
                                                               \tag{U2}
\]

The scalar o(1) depends on the public policy sequence, K and alpha;
it is uniform in support size, atom probabilities, Q, and the target.
In particular,

\[
 \boxed{\liminf_{n\to\infty}
 \frac{-\log\mathscr R_n}{\log\log n}
 \ge\min\{1,\lambda\gamma_*\}.}                            \tag{U3}
\]

If `lambda gamma_*>1`, the inherited policy-independent two-state lower
also gives the stronger amplitude conclusion

\[
 (\log n)\mathscr R_n\longrightarrow K.                      \tag{U4}
\]

There is no new critical-amplitude assertion when `lambda gamma_*=1`.
The lower needed to make (U3) an equality is a separate native transport
obligation, retained by the principal researcher.

## 2. Proof exponent and the exact finite scalar branch

Set

\[
 \theta_n=\gamma_*\eta_n/D_n,\quad
 p_n=(1-\theta_n)^{-1},\quad w=1.
                                                               \tag{U5}
\]

By (U1),

\[
 \theta_n\ell
 =\gamma_*v_n(1+D_n^{-1})
 =(\gamma_*\lambda+o(1))L.
                                                               \tag{U6}
\]

Thus theta_n=O(L/ell)->0. Also theta_n/eta_n=gamma_*/D_n->0,
so eventually `0<theta_n<=eta_n` and `theta_n<=1/2`, exactly as
required by the inherited finite energy argument. No positive lower bound
on eta_n is used, and eta_n is allowed to approach one.

Suppress n temporarily. The inherited parameters are

\[
 \tau=p(1-\theta/\eta)
      =\frac{1-\gamma_*/D}{1-\gamma_*\eta/D},\qquad
 U=e^{D\theta p/\eta}=e^{\gamma_*p}.
                                                               \tag{U7}
\]

For all sufficiently large n, `0<tau<1`; in particular

\[
 1-\tau=\frac{\gamma_*(1-\eta)}{D(1-\gamma_*\eta/D)}>0,
 \qquad \tau\to1.
\]

Consequently `U tau -> exp(gamma_*)>1`, so the second branch of the
*exact* finite maximum applies eventually:

\[
 H_1(D)=\sup_{0<z\le1}(Uz^\tau-z)
       =U-1=e^{\gamma_*p}-1.                                 \tag{U8}
\]

This identity uses the accepted outflow subtraction in the predecessor.
Dropping that subtraction would replace `U-1` by a different quantity
and would not prove this constant.

## 3. Endpoint excess is paid, rather than discarded

For the predecessor's low-weight set
`A_0={pi/q<h}`, write b=q(A_0). Choose h=ell^-2 and put

\[
 \Delta_h=\frac{H_2(h)+Kh}{1-h}.
\]

Its binary KL inequality gives

\[
 -\log(1-b)\le K+\Delta_h,\qquad
 1-b\ge e^{-K}e^{-\Delta_h},\qquad
 \Delta_h=O_K(L/\ell^2).                                    \tag{U9}
\]

Since `beta(exp(gamma_*)-1)=alpha exp(-K)`, (U8)–(U9) imply

\[
\begin{split}
 [\beta H_1(D)-\alpha(1-b)]_+
 &\le \beta(e^{\gamma_*p}-e^{\gamma_*})
       +\alpha e^{-K}(1-e^{-\Delta_h})\\
 &\le C_{K,\alpha}(\theta+\Delta_h).
\end{split}                                                 \tag{U10}
\]

Here `p-1=theta/(1-theta)<=2theta`, and the exponential is bounded
on the eventually compact range `1<=p<=2`. The constants do not depend
on the finite instance. In contrast to a proof with a fixed exponent
strictly below gamma_*, the positive part in (U10) need not be zero.
The endpoint conclusion will pay it over every first-hit iteration.

The inherited multiplier is

\[
 \Gamma(e)=\frac12+\frac{2^{p-1}}2
 \left\{1+[\beta H_1(D)-\alpha(1-b)]_++\alpha e\right\}.
\]

It follows, for `0<=e<=1`, that

\[
 0\le\log\Gamma(e)
 \le C_{K,\alpha}(\theta+\Delta_h+e).                        \tag{U11}
\]

This includes the lazy identity and the true local/global rejection
diagonals. It is not inferred from an off-diagonal comparison.

## 4. Complete full-return error bound

Use the predecessor's proof cutoffs, which do not change the sampler:

\[
 R=n/\ell^4,\quad d_{\rm test}=\ell^{-2},\quad
 N=\left\lceil\frac{8}{\alpha e^{-K}}L\right\rceil,
 \quad M_0=e^{2K+1},
\]
\[
 J_0=\frac2{\alpha(2(n-N)+1)},\quad
 a=\pi(\pi/q>R),\quad
 \rho=1-\alpha(1-b)/2,
\]
\[
 \bar e=\min\left\{1-b,\frac aR+
 \frac{(N+1)(M_0/h+1)J_0}{d_{\rm test}^2}\right\}.
                                                               \tag{U12}
\]

All finite-certificate hypotheses hold eventually, with `N<n/2` and
`R>e`. The inherited bounds give

\[
 a\le\frac K{\ell-4L-1},\qquad
 \bar e\le E_n:=C_{K,\alpha}(L+1)\ell^6/n,
                                                               \tag{U13}
\]
\[
 \sqrt{(M_0+R)J_0}+d_{\rm test}+\bar e+b\rho^N
                  =O_{K,\alpha}(\ell^{-2}).                 \tag{U14}
\]

For the last bound it suffices that `1-b>=e^-K/2`, which follows
uniformly from (U9), and then `b rho^N<=ell^-2`.

The complete full-return certificate is

\[
 \|qC^n-\pi\|_{\rm TV}\le
 a+O_{K,\alpha}(\ell^{-2})
 +b^{1-\theta}\bar e^\theta\Gamma(\bar e)^{N(1-\theta)}.
                                                               \tag{U15}
\]

If b or bar e is zero, the final term is zero and needs no logarithm.
Otherwise `b^(1-theta)<=1`, and (U11)–(U13) give

\[
\begin{split}
 \log\{b^{1-\theta}\bar e^\theta
                   \Gamma(\bar e)^{N(1-\theta)}\}
 &\le-\theta\ell
 +\theta\{6L+\log(L+1)+\log C_{K,\alpha}\}\\
 &\quad+C_{K,\alpha}N(\theta+\Delta_h+E_n)\\
 &=-\gamma_*\eta_n\ell/D_n+o(1).
\end{split}                                                  \tag{U16}
\]

Every remainder here is uniform over instances: `theta L=O(L^2/ell)`,
`N theta=O(L^2/ell)`, `N Delta_h=O(L^2/ell^2)`, and `N E_n->0`.
In particular the *accumulated* multiplier is `1+o(1)` in this
specific regime. Merely proving `Gamma->1` would not have sufficed.
Combining (U13), (U15), and (U16) proves (U2).

The inherited decomposition used to obtain (U15) follows each first hit
by the original full C for its remaining deterministic time. Thus (U2)
bounds the actual full-chain law, including every post-hit return. No
absorbed process has been substituted for a sampler, and no random
attempt count has been substituted for the actual horizon n.

## 5. Exponent and the ordinary-amplitude corollary

By (U1), `eta_n ell/D_n=(lambda+o(1))L`. Hence (U2) is

\[
 \mathscr R_n\le\ell^{-1+o(1)}
                   +\ell^{-\lambda\gamma_*+o(1)},
\]

which proves (U3). The accepted policy-independent two-state family with
Q=I gives `liminf ell R_n>=K`. When `lambda gamma_*>1`, the last
term in (U2) is o(1/ell), and (U4) follows.

This proof uses the two consequences of *one* KL budget on each instance.
It does not claim simultaneous attainment of both worst-case bounds, and
it does not add independent KL allocations. A logarithmic exponent is
compatible with taking the worse of different lower families. A critical
amplitude would require the sharper joint allocation and an attainable
transport construction at its prefactor scale; that is not established
by (U2).

## 6. Same-v comparison: what this obligation establishes

The principal's proposed matched comparison has public `v_n=L` and
`eta_n=L/ell`, `kappa_n=eta_n`, hence D_n=0. The strong-distortion
comparison has `eta_n=1/2`, `kappa_n=0`,
`A_n=ell/L-2` for all sufficiently large n, hence

\[
 D_n=\ell/(2L)-1\to\infty,\qquad v_n=L
\]

*exactly*. The same public A_n may also be supplied to the matched
policy: its mismatch is zero, and its class contains all symmetric
lower constructions while the accepted reciprocal matched upper applies
to the enlarged class.

At `K=1,alpha=1/2`, this note supplies upper logarithmic exponent
`gamma_*=log(1+exp(-1))` for the second policy. A matching native lower
is necessary before asserting a same-v separation. The matched exponent
c_* is inherited, rather than reproved here. For `r0 in (0,1)`,
`F(c_*)=r0<=c_*` and `log(1+r0)<r0`, so `gamma_*<c_*`.
Thus the claimed separation would follow once the new lower matches.

This comparison varies eta as well as mismatch, even if the public A_n
is identical. It does not prove that A_n and mismatch separately affect
the exponent when eta_n and D_n are held fixed. Indeed the upper just
proved is uniform in both separate factors throughout (U1).

## 7. Resources and boundaries

This is an analytical contribution. No numerical jobs, large native
graphs, finite matrix powers, public disclosure, hardware, spending, or
external outreach were used. The source-read and file-write operations
are small local operations, not measurements of discovery cost. Token,
inference, energy, monetary, and total research costs are unknown.

The proof retains exact-real arithmetic and all predecessor information
and cost premises. It does not establish finite-precision stability,
historical originality, external mathematical acceptance, or an
implementation speedup. Ordinary IMH retains its stronger general
amplitude K comparator. The result here is an upper theorem and a
load-bearing review of that part only, not independent acceptance of a
lower that had not yet been delivered when this note was written.

## 8. Strengthened upper over the whole strongly distorted convergent regime

After the principal asked whether the proof really needs a finite positive
limit of v/L, the accumulated error was checked again. It does not need
that hypothesis for a relative logarithmic estimate.

**General upper proposition.** Suppose only `D_n->infinity` in addition
to the native policy conditions. For sufficiently large n, let
`w_n=eta_n ell/D_n=v_n(1+1/D_n)`. There are constants depending only
on K and alpha such that

\[
 \boxed{\mathscr R_n\le
 \frac K{\ell-4L-1}+\frac{C}{\ell^2}
 +\exp\left\{-\gamma_*w_n
       \left(1-C\frac{L+1}{\ell}\right)+\varepsilon_n\right\},}
                                                               \tag{U17}
\]

where the scalar `epsilon_n->0` is uniform over policies once the
finite-envelope branch conditions hold, and uniform over all finite
instances. Those branch conditions hold along every sequence D_n->infinity.
One may take `epsilon_n=C N(Delta_h+E_n)`, with the explicit cutoffs
above, enlarging C to absorb harmless fixed logarithms.

To prove this, retain theta=gamma_* eta_n/D_n. Then theta<=gamma_*/D_n
tends to zero, so (U7)–(U11) still hold. The finite certificate and all
cutoff bounds (U12)–(U15) do not depend on v. The right side of (U16)
is at most

\[
 -\theta\ell+C\theta(L+1)+C N\theta
                  +C N(\Delta_h+E_n)
 \le-\gamma_*w_n\left(1-C\frac{L+1}{\ell}\right)
                  +C N(\Delta_h+E_n).
\]

Here N=O(L+1) and `N(Delta_h+E_n)->0` with constants independent
of the policy. This proves (U17). In this generality Gamma^N need not
tend to one; the multiplier is retained and compared with theta ell.
When v=O(L), the paid term `theta(L+1)=O(L^2/ell)` does tend to
zero, recovering (U2) with additive o(1) without requiring `v/L->lambda`.

In particular, if also `v_n->infinity`, then

\[
 \boxed{\liminf_{n\to\infty}
 \frac{-\log\mathscr R_n}
      {\min\{\log\log n,\gamma_*v_n\}}\ge1.}               \tag{U18}
\]

Indeed both L and gamma_* v tend to infinity, w/v->1, and (U17)
is the sum of a term `exp[-L+O(1)]` and a term
`exp[-gamma_*v(1+o(1))+o(1)]`. Taking logarithms of a sum loses at
most log 2; dividing by the minimum, which diverges, proves (U18).
This argument remains valid when v/L oscillates or approaches zero.

For `liminf gamma_*v_n/L>1`, (U17) also gives the amplitude K
conclusion by the inherited two-state lower. At equality, no amplitude
is asserted. The matching transport lower only needs to handle the
bounded-v/L region where transport could dominate the ordinary tail;
the Q=I family already bounds the logarithmic exponent by one elsewhere.
The principal must still supply and check that lower before promoting
(U18) to a sharp general rate law.
