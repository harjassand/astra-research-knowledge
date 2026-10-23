# Calibration contract — frozen opening

**Status:** independent opening recorded before reading other new-worker files. The completed PCA/acquired-precision unit remains frozen. This is a finite-sample source-calibration contract only; no target CPTP benchmark is run here.

## Supplied interface and promises

There is one fixed single-Pauli Markovian noise channel with unknown unit axis \(n\sim -n\), known rate \(\gamma>0\), and trusted controls/readout. During source calibration the signal is off. For a predeclared waiting time \(\tau>0\), the Bloch map is

\[
M=qI+(1-q)nn^T,\qquad q=e^{-2\gamma\tau},\quad \lambda=1-q>0.
\]

The class, \(\gamma\), \(\tau\), trusted Pauli preparations and measurements, and stationarity/i.i.d. reset promises are supplied. The learner receives no \(n\), exact \(M\), latent simulation seed, or target truth. Axis sign is immaterial: the learned object is the one-dimensional projector \(nn^T\).

## Nine-setting count interface

For each \(j\in\{x,y,z\}\), prepare \(|+j\rangle\), wait \(\tau\), then measure \(\sigma_i\) for each \(i\in\{x,y,z\}\). Each of the nine setting pairs \((i,j)\) is repeated \(k\) times and yields only binary outcomes \(Y_{ij\ell}\in\{-1,+1\}\), with expectation \(M_{ij}\). The input record is the nine pairs of counts \((N^+_{ij},N^-_{ij})\), not an exact Bloch matrix. The empirical entry is \(\widehat M_{ij}=(N^+_{ij}-N^-_{ij})/k\).

Use cumulative checkpoints \(k_j=k_0 2^{j-1}\), \(j=1,2,\ldots\), with fixed settings and all old shots retained. At checkpoint \(j\), allocate

\[
\alpha_j=\alpha_{\rm src}\,\frac{6}{\pi^2j^2},\qquad \sum_{j\ge1}\alpha_j=\alpha_{\rm src}.
\]

The evaluator's random seeds and latent channel parameters remain evaluator-only. They are not part of the nine-count learner input.

## Simultaneous angle certificate and gates

Set

\[
u_j=\sqrt{\frac{2\ln(18/\alpha_j)}{k_j}},\quad
\widehat S_j=\frac{\widehat M+\widehat M^T}{2}-qI,\quad
\widehat\lambda_j=\lambda_{\max}(\widehat S_j).
\]

For a single setting, Hoeffding's inequality for \(k_j\) Bernoulli \(\pm1\) observations gives
\(\Pr(|\widehat M_{ij}-M_{ij}|>u_j)\le 2e^{-k_ju_j^2/2}\). A union bound over the nine settings gives failure probability at most \(\alpha_j\). Symmetrization does not enlarge the entrywise error, and the 3-by-3 Frobenius bound gives

\[
\|\widehat S_j-(1-q)nn^T\|_{\rm op}\le 3u_j.
\]

Let \(\widehat e_j\) be a unit top eigenvector of \(\widehat S_j\). If \(\widehat\lambda_j>3u_j\), the residual identity

\[
(1-nn^T)\widehat S_j\widehat e_j
=(1-nn^T)(\widehat S_j-(1-q)nn^T)\widehat e_j
\]

proves the data-dependent certificate

\[
\sin^2\angle(\widehat e_j,n)=1-(\widehat e_j^Tn)^2
\le (3u_j/\widehat\lambda_j)^2.
\]

The **coverage gate** opens only when \(\widehat\lambda_j>3u_j\); otherwise report UNRESOLVED and acquire the next checkpoint. A requested precision \(s_\star\in(0,1)\) gate opens when the coverage gate is open and \((3u_j/\widehat\lambda_j)^2\le s_\star^2\). The simultaneous statement is valid under optional stopping because the \(\alpha_j\) sum over every checkpoint the policy may inspect.

For a source-budget design check using the known gap \(\lambda=1-q\), the sufficient condition

\[
k_j\ge 18\ln(18/\alpha_j)\left(\frac{1+s_\star}{\lambda s_\star}\right)^2
\]

ensures \(3u_j\le\lambda s_\star/(1+s_\star)\). On the simultaneous event, Weyl gives \(\widehat\lambda_j\ge\lambda-3u_j\), so the observed gate certifies \(\sin\angle\le s_\star\). This is a conservative planned sample-size condition; the gate itself uses observed counts and \(\widehat\lambda_j\), not the unknown axis. If \(\gamma=0\) or \(\tau=0\), then \(\lambda=0\) and this calibration cannot identify the axis.

## Charged source operations

At cumulative count \(k_j\), the ledger records exactly \(9k_j\) preparations, \(9k_j\) source waits of duration \(\tau\) (total source waiting time \(9k_j\tau\)), and \(9k_j\) Pauli readouts. At each doubling, newly acquired work is \(9(k_j-k_{j-1})\) shots; earlier shots are neither discarded nor charged again. Failed coverage or requested-precision checks remain in the cumulative ledger. No physical energy price is assumed. The log stores the nine binary count pairs, checkpoint index, \(k_j\), \(\tau\), and gate result; the estimator consumes no seeds or exact channel matrix.

The later code/experiment may demonstrate that finite noisy counts can open this source gate on a synthetic fixture, but it will not run or claim the target logical-cycle operation until its separate CPTP audit is complete. No novelty, downstream advantage, or total practical-cost claim is made here.
