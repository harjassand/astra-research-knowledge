# Independent scalar review: coherent-history entropy exponents

Reviewer: `/root/stopping_converse`  
Date: 21 October 2026  
Scope: only the scalar history-count and operator-norm-tail exponents supplied by the root construction. The quantum truncation, adaptive transcript, approximate-channel, and coding-converse steps are outside this review.

## Verdict

The proposed entropy estimates and explicit small-perturbation interval are correct. The tail estimate admits a stronger form with **no polynomial prefactor**. The certified rank exponent at \(q=1/100\) is

\[
g_* = 1.581642760903122734639403723143\ldots
<\log_2 3
=1.584962500721156181453738943947\ldots.
\]

For every \(0<\beta\le1/512\), with \(\alpha=\sqrt{1-\beta^2}\), the norm-tail scalar sum is at most

\[
2^{-\gamma n},\qquad
\gamma=\frac9{100}-h_2(1/100)
=0.009206864104088827175133666296\ldots>0.
\]

This verifies the numerical/entropy component of the proposed strict port-rate upper bound on \(0<s\le\arcsin(1/512)\), conditional on the separately reviewed quantum-operator argument. A safely rounded explicit upper rate is **1.581643**, not a downward-rounded 1.58164 presented as an exact upper bound.

## 1. Truncated rank sum

Put \(a=2\sqrt2=2^c\), \(c=3/2\), and

\[
R_n=\sum_{k=0}^{\lfloor qn\rfloor}\binom nk 3^k a^{n-k},
\qquad
g(t)=c+h_2(t)+t\log_2(3/a).
\]

For \(t=k/n\), the usual binomial bound \(\binom nk\le2^{nh_2(t)}\) gives

\[
\binom nk3^ka^{n-k}\le2^{ng(t)}.
\]

It also holds at \(k=0,n\) using \(h_2(0)=h_2(1)=0\). The entropy bound itself follows directly from
\(1\ge\binom nk t^k(1-t)^{n-k}\).

On \(0<t<1/2\),

\[
g'(t)=\log_2\!\left(\frac{3(1-t)}{at}\right)>0,
\]

because \((1-t)/t>1\) and \(3/a>1\). Thus for \(q\in(0,1/2)\), every term in the truncated sum is at most \(2^{ng(q)}\). There are at most \(n+1\) terms, proving

\[
\boxed{R_n\le(n+1)2^{n[c+h_2(q)+q\log_2(3/a)]}.}
\]

The actual monotonicity interval extends to \(t<3/(3+a)>1/2\), but that extension is unnecessary. Floors do not create an error because every included \(k/n\le q\).

## 2. Tail exponent, including the floor

Assume \(\alpha,\beta>0\) and set

\[
T_n=\sum_{k>\lfloor qn\rfloor}\binom nk\alpha^{n-k}\beta^k,
\qquad p=\frac\beta{\alpha+\beta}.
\]

For integer \(k\), \(k>\lfloor qn\rfloor\) is exactly \(k>qn\). For any \(x>1\), multiplying terms by \(x^k\) and bounding the threshold gives

\[
T_n\le x^{-qn}(\alpha+\beta x)^n.
\]

If \(q>p\), the optimizer

\[
x=\frac{\alpha q}{\beta(1-q)}
\]

is strictly greater than one. Substitution yields

\[
\boxed{
T_n\le2^{nf(q)},\qquad
f(q)=h_2(q)+(1-q)\log_2\alpha+q\log_2\beta.
}
\]

Equivalently, \(T_n=(\alpha+\beta)^n\Pr\{\operatorname{Bin}(n,p)>qn\}\) and the displayed bound is the Chernoff inequality. No integer adjustment or polynomial prefactor is required. If \(f(q)<0\), decay is exponential for each fixed perturbation. The endpoint \(\beta=0\) is handled directly: the tail vanishes identically.

## 3. The uniform explicit interval

Now take \(q=1/100\), \(0<\beta\le2^{-9}\), and \(\alpha=\sqrt{1-\beta^2}\). On \(0\le\beta\le1\),

\[
\alpha+\beta\ge1
\]

because \(\sqrt{1-\beta^2}\ge1-\beta\). Therefore

\[
p=\frac\beta{\alpha+\beta}\le\beta\le\frac1{512}<\frac1{100}=q.
\]

Also \(\log_2\alpha\le0\) and \(\log_2\beta\le-9\), so

\[
f(q)\le h_2(1/100)-9/100=-\gamma<0.
\]

This proves the claimed tail decay uniformly over the whole interval without differentiating in \(\beta\) or approximating \(\arcsin\). At its upper endpoint the actual exponent is slightly smaller, approximately \(-0.00920958831447\); the weaker uniform \(-\gamma\) is sufficient and easier to certify exactly.

The rank exponent can be written without radicals as

\[
g_*=(99/100)(3/2)+h_2(1/100)+(1/100)\log_2 3.
\]

Its strict gap to the qutrit port rate is

\[
\log_2 3-g_*
=0.003319739818033446814335220804\ldots>0.
\]

The accompanying executable uses exact rational interval arithmetic to certify

\[
\begin{aligned}
0.08079313589591117&<h_2(1/100)<0.08079313589591118,\\
1.5816427609031227&<g_*<1.5816427609031228,\\
\log_2 3-g_*&>0.0033197398180334,\\
h_2(1/100)-0.09&<-0.0092068641040888.
\end{aligned}
\]

## 4. A shrinking cutoff gives an upper certificate tending to 3/2

For \(\beta\downarrow0\), choose \(q=\sqrt\beta\). Then \(q>\beta\ge p\) for \(0<\beta<1\), while \(q<1/2\) for \(\beta<1/4\). Since \(\beta=q^2\) and \(\log_2\alpha\le0\),

\[
\begin{aligned}
f(q)&\le h_2(q)+2q\log_2q\\
&=q\log_2q-(1-q)\log_2(1-q)\\
&\le q\log_2(e q).
\end{aligned}
\]

The last inequality follows from
\(-(1-q)\ln(1-q)\le q\), obtained by integrating \(1/(1-t)\) over \([0,q]\) or from \(-\ln(1-q)\le q/(1-q)\). Thus the tail exponent is strictly negative whenever \(q<1/e\), in particular for all sufficiently small \(\beta\).

Meanwhile

\[
g(q)-c=h_2(q)+q\log_2(3/a)\longrightarrow0.
\]

One explicit modulus, using \(h_2(q)\le q\log_2(e/q)\), is

\[
g(\sqrt\beta)-c
\le\sqrt\beta\,\log_2\!\left(\frac{3e}{a\sqrt\beta}\right).
\]

A single choice that retains the certified strict gap over \(0<\beta\le1/512\) and also tends to zero is

\[
q(\beta)=\min\{1/100,\sqrt\beta\}.
\]

For \(\beta\ge10^{-4}\), use the uniform fixed-\(q\) proof above; for \(\beta<10^{-4}\), use the square-root argument. Monotonicity of \(g\) gives \(g(q(\beta))\le g_*\), while \(g(q(\beta))\to3/2\).

These are upper-certificate statements. They do **not** prove a matching lower bound or continuity of the actual perturbed quantum capacity. A separate constructive coding argument is required for either conclusion. The large-blocklength limit is taken for each fixed perturbation before sending \(\beta\) to zero; the negative tail exponent shrinks to zero and gives no perturbation-uniform decay rate.

## 5. Exact certificate and observed resources

`history_exponent_certificate.py` uses only Python's standard library. For rational \(1\le x\le2\), put \(z=(x-1)/(x+1)\) and use

\[
\ln x=2\sum_{j=0}^{N-1}\frac{z^{2j+1}}{2j+1}+R_N,
\qquad
0\le R_N\le\frac{2z^{2N+1}}{(2N+1)(1-z^2)}.
\]

The code uses \(N=48\), all sums/remainders as exact `Fraction`s, and elementary radix decompositions for \(\ln2,\ln3,\ln99,\ln100\). Displayed decimals are outward rounded; the decisive assertions compare rational interval endpoints directly with rational decimal separators. Independent coarse integer checks also establish \(1.584<\log_2 3<1.585\).

Recorded result: `exact_rational_checks_passed`. The saved execution in `history_exponent_certificate.json` took approximately 0.00123 seconds and used 8320 KiB peak RSS as reported by the local Linux process. An initial optional `mpmath` calculation failed because that module was unavailable; it was replaced by standard-library Decimal diagnostics and then this exact rational certificate. No package was installed and no external compute service was used.

This finite certificate verifies the scalar constants only. It cannot establish the operator-history expansion, approximate-channel validity, or capacity conclusion; those remain explicit dependencies of the root proof.
