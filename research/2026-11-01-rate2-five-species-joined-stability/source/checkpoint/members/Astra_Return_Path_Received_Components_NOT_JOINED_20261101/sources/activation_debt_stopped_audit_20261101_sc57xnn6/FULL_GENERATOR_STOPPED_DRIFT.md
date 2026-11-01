# Full finite-jump certificate for the cubic activation-debt coordinate

**Result.** For the exact five-species rate-2 tree, the proposed cubic remaining-work coordinate does admit a full-generator negative drift on a fixed charging region. This is a stopped-domain result, **not** a global Foster theorem or a recurrence proof. No averaged/frozen fast fiber is used.

Take

\[
a=1/100,\quad q=2,\quad r=101/100,\quad K=1,\quad \epsilon=20,\quad t_0=100.
\]

For an integer state \(x=(A,B,C,D,E)\), set

\[
c=A+C,\quad d=A+D,\quad Z=B-A+E,\quad H=aZ-E,
\]

and let \(t=\tau(x)\) be the positive solution, when \(H>0\), of

\[
qP(c,d,t)=H,\qquad
P(c,d,t)=cdt+\frac{c+d}{2}t^2+\frac{t^3}{3}.
\]

Set \(\tau=0\) when \(H\le0\). Write \(N=A+B+C+D+E\),

\[
p=\frac{A^2}{B+1},\qquad h=1+\epsilon p,\qquad V=r^N e^t h.
\]

Then the **whole exact finite-jump generator** satisfies

\[
\boxed{\quad LV(x)\le-\tfrac12 V(x)\quad\text{whenever }\tau(x)\ge100.\quad}
\]

The estimate is uniform in arbitrarily unbalanced \(C,D\), and includes every port, \(2A\), reverse-arm, grouped \(AE\), and neutral-pair jump.

## 1. Exact generator and structural estimates

All propensities use falling-factorial conventions. The transitions, rates, and changes of the debt coordinates are:

| Reaction | Rate | \(\Delta c\) | \(\Delta d\) | \(\Delta H\) | \(\Delta N\) |
|---|---:|---:|---:|---:|---:|
| \(0\to A\) | 1 | 1 | 1 | \(-a\) | 1 |
| \(A\to0\) | \(A\) | -1 | -1 | \(a\) | -1 |
| \(2A\to AC\) | \(A(A-1)\) | 0 | -1 | \(a\) | 0 |
| \(AC\to2A\) | \(AC\) | 0 | 1 | \(-a\) | 0 |
| \(2A\to AD\) | \(A(A-1)\) | -1 | 0 | \(a\) | 0 |
| \(AD\to2A\) | \(AD\) | 1 | 0 | \(-a\) | 0 |
| \(2A\to AE\) | \(A(A-1)\) | -1 | -1 | \(2a-1\) | 0 |
| \(AE\to2A\) | \(AE\) | 1 | 1 | \(1-2a\) | 0 |
| \(AE\to CD\) | \(AE\) | 0 | 0 | 1 | 0 |
| \(CD\to AE\) | \(2CD\) | 0 | 0 | -1 | 0 |
| \(CD\to AB\) | \(CD\) | 0 | 0 | 0 | 0 |
| \(AB\to CD\) | \(AB\) | 0 | 0 | 0 | 0 |

Put

\[
\mu=\frac{a}{q(1-a)}=\frac1{198},\qquad
\nu=\frac a{1-a}=\frac1{99}.
\]

On \(t\ge100\), \(H=qP\ge qt^3/3\), \(qcdt\le H\le aZ\), and \(B=A+Z-E>(1-a)Z\). Consequently

\[
\frac{cd}{B+1}\le\frac\mu t,\quad
p\le\frac\mu t,\quad
\frac1{B+1}\le\frac{3\mu}{t^3},\quad
\frac E{B+1}\le\nu,\quad
1\le h\le\frac{991}{990}<\frac{101}{100}.                 \tag{1}
\]

No bound on \(C/D\) occurs. Also \(A(C+D)\le2cd\). Every legal one-step neighbor still has \(H>0\), since \(H\ge2\cdot100^3/3>1\) and every \(H\)-jump has absolute size at most 1. Thus the generator below uses the actual root at every neighbor; no artificial stopping/reset is inserted into an individual jump.

## 2. Finite-jump facts

The identity

\[
P(c+1,d+1,t-1)=P(c,d,t)-P(c,d,1)                         \tag{2}
\]

is useful. Its shifted counterpart gives

\[
P(c-1,d-1,t+1)=P(c,d,t)+P(c-1,d-1,1).
\]

Because \(qP(c-1,d-1,1)\ge q/3>a\) whenever \(A\ge1\), death increases \(t\) by less than 1. By coordinate monotonicity, each legal forward \(2A\) reaction likewise increases \(t\) by at most 1. Immigration and the reverse \(AC,AD\) arms strictly decrease \(t\). The \(CD\to AE\) reaction decreases \(t\); the two neutral \(AB\leftrightarrow CD\) jumps leave it exactly unchanged.

### The two \(AE\) channels must remain grouped

For \(AE\to CD\), write the new root as \(t+\delta\). For \(AE\to2A\), write it as \(t-s\). With \(D_t=(c+t)(d+t)\), monotonicity of \(P_t\) gives

\[
0<\delta\le\frac1{qD_t}\le\frac1{2t^2},\qquad 0<s<1,
\]

and the mean-value theorem gives

\[
s\ge
\frac{qt(c+d+t+1)-(1-2a)}{q(c+t+1)(d+t+1)}.
\]

Hence, already for \(t\ge2\),

\[
\frac{s}{\delta}
\ge[2t(t+1)-1]\Big(\frac t{t+1}\Big)^2
\ge\frac{44}{9}>4.                                   \tag{3}
\]

Using \(e<3\), \(s<1\), and \(\delta\le1/8\),

\[
1-e^{-s}\ge s/e>s/3\ge4\delta/3,
\qquad e^\delta-1\le\delta/(1-\delta)\le8\delta/7.
\]

Therefore

\[
e^{-s}+e^\delta-2\le0.                                \tag{4}
\]

The corresponding weighted changes of \(p\) satisfy

\[
e^{-s}\frac{2A+1}{B+1}
+e^\delta\frac{-2A+1}{B+1}
\le\frac2{B+1},                                       \tag{5}
\]

because a legal \(AE\) reaction has \(A\ge1\). This is the precise finite-jump grouping; it is not a cancellation only at first derivative order.

## 3. States with \(A\ge1\): the exact fast correction pays

For any reaction \(j\), put \(z_j=(\log r)\Delta N_j+\Delta t_j\). The exact identity

\[
\frac{LV}{r^Ne^t}
=h\sum_j\lambda_j(e^{z_j}-1)
+\epsilon\sum_j\lambda_j e^{z_j}(p_j-p)                \tag{6}
\]

separates the base multiplier and its phase correction.

By the finite-jump facts and (4), every positive base contribution is bounded by the port immigration, death, and the three forward \(2A\) channels. Thus the first sum in (6), including \(h\), is at most

\[
h\{(r-1)+(e-1)A+3(e-1)A(A-1)\}
\le h\{1/100+3(e-1)\}A^2<7A^2.                       \tag{7}
\]

For the correction, \(AB\to CD\) has the exact contribution

\[
\epsilon AB\left[\frac{(A-1)^2}{B}-\frac{A^2}{B+1}\right]
=-\epsilon A(2A-1)+\epsilon\frac{A^3}{B+1}.            \tag{8}
\]

All port-death and forward-\(2A\) correction terms are nonpositive. The remaining positive terms are bounded as follows:

* Immigration: \(\epsilon r(2A+1)/(B+1)\).
* Reverse \(AC,AD\) arms together: \(2\epsilon\mu(2A+1)/t\).
* \(CD\to AE\): \(q\epsilon\mu(2A+1)/t\).
* \(CD\to AB\): \(\epsilon\mu(2A+1)/t\), using its actual denominator \(B+2\).
* The grouped \(AE\) pair: \(2\epsilon AE/(B+1)\le2\epsilon\nu A\), by (5).
* The positive remainder in (8): \(\epsilon\mu A/t\).

Since \(2A+1\le3A\), the entire correction is at most

\[
-\epsilon A^2+
\epsilon\left[\frac{16\mu}{t}+2\nu+
\frac{9r\mu}{t^3}\right]A.
\]

At \(t\ge100\), the square bracket is less than \(1/40\). With \(\epsilon=20\), the correction is therefore at most \(-\frac{39}{2}A^2\). Combining with (7),

\[
LV/(r^Ne^t)<-\tfrac{25}{2}A^2\le-\tfrac12h.           \tag{9}
\]

## 4. States with \(A=0\): immigration and charging jointly pay

Here \(c=C,d=D,h=1\). Only immigration and the two \(CD\) exits have positive rates. The immigration decrease \(s_b=t-t_b\) obeys

\[
s_b\ge
\frac{t(c+d+t+1)}{(c+t+1)(d+t+1)}
\ge\rho\beta,
\]

where

\[
\beta=\frac{t(c+d+t)}{D_t}=1-\frac{cd}{D_t}\in[0,1],
\qquad \rho=\left(\frac t{t+1}\right)^2.
\]

The \(CD\to AE\) decrease \(s_c\) obeys \(s_c\ge1/(qD_t)\). Using \(e^{-u}-1\le-u+u^2/2\), its base contribution is at most

\[
qcd(e^{-s_c}-1)
\le-\eta(1-\beta),\qquad
\eta=1-\frac1{2qt^2}.
\]

The complete base contribution is thus at most

\[
r e^{-\rho\beta}-1-\eta(1-\beta).                    \tag{10}
\]

This is a convex function of \(\beta\), so its maximum is attained at an endpoint. For \(t\ge100\), the endpoint values satisfy

\[
r-1-\eta<-3/5,\qquad r e^{-\rho}-1<-3/5.
\]

For a purely rational check of the second inequality, use \(\rho>49/50\) and
\(e^{49/50}>1+49/50+(49/50)^2/2+(49/50)^3/6>101/40\).

The exact phase correction of these three jumps is bounded by

\[
\epsilon\left[\frac r{B+1}+
\frac{(q+1)cd}{B+1}\right]
\le20\mu\left[\frac{3r}{t^3}+\frac3t\right]<1/100.     \tag{11}
\]

Thus \(LV/V<-59/100<-1/2\). Equations (9) and (11) prove the stated theorem.

## 5. Legitimate stopped consequence, and the missing interface

The actual chain is nonexplosive because \(N(s)\le N(0)+I(s)\), with \(I\) a unit-rate Poisson immigration count. Globally,

\[
\tau\le(3aN/q)^{1/3},\qquad
V\le r^N\exp[(3aN/q)^{1/3}](1+20N^2).
\]

Poisson domination therefore supplies the finite-horizon integrability needed to remove localization in stopped Dynkin. Let

\[
\sigma=\inf\{s\ge0:\tau(X_s)<100\}.
\]

For an initial state with \(\tau\ge100\),

\[
\mathbb E_x\left[e^{(T\wedge\sigma)/2}
V(X_{T\wedge\sigma})\right]\le V(x),\qquad T\ge0.       \tag{12}
\]

In particular \(\mathbb E_xe^{\sigma/2}\le V(x)\), so this actual charging episode exits in finite time almost surely. Equation (12) also controls the total-count/exponential-debt cost of its exit, without resetting the chain.

**What is not proved:** no drift is supplied on \(\tau<100\); bounded remaining work does not automatically give \(A\)-occupation service; no activated-region profile is glued to this one; repeated returns across the interface are not paid. Therefore (12) must not be promoted to a global stability or exponential-stationary-moment claim. The next mathematical obligation is a compatible receiving potential on the bounded-debt/activated side, with both directions of actual interface jumps accounted for.

## Verification artifact

`verify_exact_generator.py` independently evaluates the complete reaction list with high-precision arithmetic, using integer test states constructed to have an exact prescribed initial root. It stresses balanced and extremely unbalanced \(C,D\), large \(A\), large \(E/B\), port jumps, and every reaction term. Its numerical results supplement, but do not replace, the inequalities above.
