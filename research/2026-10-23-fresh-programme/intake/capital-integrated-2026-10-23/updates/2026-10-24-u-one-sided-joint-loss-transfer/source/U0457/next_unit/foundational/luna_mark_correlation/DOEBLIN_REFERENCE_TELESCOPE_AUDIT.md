# Doeblin reference telescope for Alice-only selection

## Verdict

The proposed inequality is valid in the finite-matrix model under its stated one-sided selection and product-channel assumptions. In particular, no entropy-of-state subtraction is needed: the telescope follows from finite cq direct-sum relative entropy and Donald identity. The Doeblin contraction also holds with quantum side information $U=(X_{<i},B)$ by exposing an independent mixture flag. I found no exact support or conditional-independence obstruction.

## Source and notation

Let the selected normalized source on $X^mB$ be $\Omega_{X^mB}$, with classical input law $Q_X$ and conditional Bob states $\rho_{x^m}$. The event is Alice-only, Bob's complete instrument has not been applied, and the original free input law is $\mu^{\otimes m}$. Thus the selected $Y^m$ channel remains

\[
P(y^m\mid x^m,E)=\prod_j\mu(y_j\mid x_j),
\]

and $B$ is conditionally independent of $Y^m$ given $X^m,E$. Assume for every $x$ that

\[
\mu(y\mid x)=\delta\nu(y)+(1-\delta)\kappa(y\mid x),
\qquad 0<\delta\le1.
\]

For round $i$, put $H=X_{<i}$, $S=Y_{>i}$, $R=(H,S)$, $U=(H,B)$, and let $q_R$ be the selected conditional law of $X_i$. Write

\[
d_i=\mathbb E_R D(q_R\Vert\mu_X),\qquad
\chi_i=\mathbb E_R I(X_i:B\mid R).
\]

All information quantities here are finite-dimensional relative entropies or cq Holevo quantities, with natural logarithms.

## Exact $F_i$ identity

Define

\[
F_i=\mathbb E_{S=Y_{>i}}
 D\!\left(\Omega_{X_{\le i}B\mid S}
       \middle\Vert \mu_X^{\otimes i}\otimes\phi\right),
\]

where $\phi$ is Bob's original marginal and conditional states are normalized on positive-probability $S$. In particular, $F_0=\mathbb E_{Y^m}D(\Omega_{B\mid Y^m}\Vert\phi)\ge0$, and $F_m=D(\Omega_{X^mB}\Vert\mu_X^{\otimes m}\otimes\phi)$.

Fix $s=Y_{>i}$ and let $U=(X_{<i},B)$. Finite cq direct-sum decomposition followed by Donald identity gives

\[
\begin{aligned}
D(\Omega_{X_iU\mid s}\Vert\mu_X\otimes\mu_X^{\otimes(i-1)}\otimes\phi)
={}&D(P(X_i\mid s)\Vert\mu_X)
 +I(X_i:U\mid s)\\
 &+D(\Omega_{U\mid s}\Vert\mu_X^{\otimes(i-1)}\otimes\phi).
\end{aligned}
\]

The averaged first two terms equal $d_i+\chi_i$. Indeed, the ordinary classical mixture identity gives

\[
\mathbb E_{H\mid s}D(P(X_i\mid H,s)\Vert\mu_X)
=D(P(X_i\mid s)\Vert\mu_X)+I(X_i:H\mid s),
\]

and the chain rule for the cq ensemble gives

\[
I(X_i:U\mid s)=I(X_i:H\mid s)+I(X_i:B\mid H,s).
\]

Thus, after averaging over $s$,

\[
d_i+\chi_i
=\mathbb E_S\!\left[D(P(X_i\mid S)\Vert\mu_X)
                       +I(X_i:U\mid S)\right].
\tag{1}
\]

Now mix the states $\Omega_{U\mid Y_i=y,S=s}$ over $y$. Donald identity says

\[
\mathbb E_{Y_i\mid s}D(\Omega_{U\mid Y_i,s}\Vert\mu_X^{\otimes(i-1)}\otimes\phi)
=I(Y_i:U\mid s)+D(\Omega_{U\mid s}\Vert\mu_X^{\otimes(i-1)}\otimes\phi).
\]

The left side, averaged over $s$, is $F_{i-1}$. Substitution into the preceding decomposition yields the claimed exact identity

\[
\boxed{F_i-F_{i-1}=d_i+\chi_i-I(Y_i:X_{<i}B\mid Y_{>i}).}
\tag{2}
\]

This derivation uses only relative-entropy mixture identities; it never writes $S(\rho)$ and subtracts possibly undefined type-III state entropies.

## Markov property and Doeblin flag

Because $E$ uses only Alice's input and instrument, it changes $Q_X$ and the conditional Bob assemblage but does not alter the channel generating $Y^m$ given $X^m$. Since that channel is a product over rounds, conditional on $S=Y_{>i}$ the cq state has the Markov form

\[
U\;\longleftarrow\; X_i\;\longrightarrow\;Y_i\qquad\text{given }S,
\]

where the $X_i\to Y_i$ channel is still $\mu(y\mid x)$. In particular, the conditional state of $U$ given $X_i,S$ does not depend on $Y_i$.

Realize the Doeblin channel with a fresh independent flag $Z_i$: with probability $\delta$, set $Y_i\sim\nu$ independently of all pre-channel variables; otherwise sample $Y_i\sim\kappa(\cdot\mid X_i)$. The flag is independent of $(X_i,U,S)$. Adding it to the output can only increase mutual information, while

\[
\begin{aligned}
I(Y_i:U\mid S)
&\le I(Y_iZ_i:U\mid S)\\
&= (1-\delta) I(Y_i:U\mid S,Z_i=0)\\
&\le (1-\delta) I(X_i:U\mid S).
\end{aligned}
\]

The last step is data processing through $\kappa$; the $Z_i=1$ branch has zero information. By (1), $\mathbb E_S I(X_i:U\mid S)\le d_i+\chi_i$. Therefore (2) implies

\[
F_i-F_{i-1}\ge\delta(d_i+\chi_i).
\]

Summing, using $F_0\ge0$ and $F_m\le\ln(1/p)$ from the one-sided domination $\Omega_{X^mB}\le(\mu_X^{\otimes m}\otimes\phi)/p$, gives

\[
\boxed{\displaystyle\sum_i(d_i+\chi_i)\le\frac{\ln(1/p)}{\delta}.}
\]

## Boundary and finiteness checks

- The essential condition is Alice-only selection with Bob's premeasurement system retained and Bob's full POVM complete. If selection depends on Bob's input or outcome, $Y_i-X_i-U$ need not hold and $F_i$ need not telescope this way.
- Product conditional channels across rounds are needed for the conditional Markov statement. An arbitrary joint channel $P(Y^m\mid X^m)$ is not covered merely by having the same one-coordinate marginals.
- For positive-probability suffixes, the conditional states in $F_i$ are normalized finite matrices; zero-probability suffixes are omitted. The domination $\Omega_{X^mB}\le(\mu_X^{\otimes m}\otimes\phi)/p$ and finite alphabets give finite endpoint divergence. Each $F_i$ is finite as well: applying the product channel and tracing out $X_{>i}$ gives $\Omega_{X_{\le i}B,S=s}\le \mu_Y^{\otimes(m-i)}(s)(\mu_X^{\otimes i}\otimes\phi)/p$. Dividing by the selected suffix probability $Q_{Y_{>i}}(s)>0$ gives the conditional reference domination with factor $\mu_Y^{\otimes(m-i)}(s)/(p\,Q_{Y_{>i}}(s))\ge1$; the inequality follows by tracing the original domination to $S$, which yields $Q_{Y_{>i}}(s)\le\mu_Y^{\otimes(m-i)}(s)/p$. Thus no $\infty-\infty$ cancellation is used.
- The selected source remains correlated within each $(X_i,Y_i)$ pair according to $\mu$. This argument does not pretend the selected input law is a product base law; the $d_i$ terms explicitly charge the $X_i$-law drift relative to $\mu_X$.
