# Exact assumption stress tests

These are counterexamples to weakened acquisition contracts. They do not refute the temporal note when its listed assumptions hold.

## Correlated incoming labels

Take (n=2), (p_{\rm low}=1/4), (p_{\rm high}=3/4), so (a=1/2,b=0). Let both entries occur at the same time, so (L_2=0) and the telegraph target is (Q_2=1). At code sign (+1), each atom's heavy marginal is (3/4).

With independent labels, (\mathbb E[X_1X_2]=(1/2)^2=1/4), so the corrected parity mean is (\mathbb E[X_1X_2]/a^2=1), as claimed. With perfectly correlated labels (X_1=X_2), while preserving the same (3/4) heavy marginal for each atom, (\mathbb E[X_1X_2]=1) and the corrected mean is (1/a^2=4). Marginal purity alone does not imply the acquisition identity.

## Missing prehistory

Use the same (n=2) purity settings, but suppose the code starts at time zero. Give every observed product ages (C) and (C+D), with (C>T), so both entries occurred before coding began throughout the observation window. Hold the pre-code feed at (p_{\rm low}=1/4). Independent labels then have mean spin (-1/2), and the nominally corrected parity has expectation
\[
\frac{\mathbb E[X_1X_2]}{a^2}=\frac{1/4}{1/4}=1.
\]
The stationary telegraph target is (e^{-2rD}\to0) as (D\to\infty). No uniform error bound follows from finite observation time unless the relevant prehistory is coded, validly prepared away, or covered by an explicit old-history fraction.

## Unmeasured mixing at the entry boundary

Suppose the commanded symmetric code has nominal contrast (a=1/2), but transport halves the isotope modulation before atoms reach the declared entry boundary. The actual label mean is then (\mathbb E[X\mid\sigma]=a_{\rm actual}\sigma) with (a_{\rm actual}=a/2). For two coincident entry times, (Q_2=1), while use of the nominal correction gives
\[
\mathbb E[X_1X_2]/a^2=a_{\rm actual}^2/a^2=1/4.
\]
An exactly measured boundary waveform and its actual purity contrast are premises of the formula.

## A campaign-level latent history class

Let a shared catalyst state select model E or O with probability (1/2) once per campaign, and let all products in that campaign inherit that one class. Within each class, products can be iid and the isotope code can be independent. Across campaigns, the target is (Q=(Q_E+Q_O)/2), but the campaign estimate tends to (Q_E) or (Q_O) as (T,N\to\infty). Its limiting variance is
\[
\frac{(Q_E-Q_O)^2}{4}
=\frac{(1-e^{-4})^8}{256}
\approx 0.0033692638.
\]
The finite-product term (B_n^2/N) does not cover this dependence. Conditional iid sampling within a fixed stationary mixture does; selecting a mixture component once per campaign requires the added (\operatorname{Var}_\Theta(Q_\Theta)) term.
