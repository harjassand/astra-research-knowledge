# Event-promotion action profile

## 1. Question and contract

Can a proposal distribution make a rare event common by a certified, low-cost transport of a baseline law? The first candidate was a one-scale Wasserstein boundary-shell inequality. The empirical action profile is already contained in established distributionally robust chance constraints, and Blanchet–Murthy's general transport dual already covers closed events on Polish spaces, including path-dependent first-passage probabilities. So the action curve is retained as an accounting coordinate, and the investigation changes representation again: certify event acceptance and conditional-law fidelity as separate quantities.

Let \((\mathsf X,d)\) be a Polish metric space, let \(P\) be a Borel probability with finite first moment, and let \(A\subseteq\mathsf X\) be a nonempty Borel event. Write

\[
g_A(x)=d(x,A)=\inf_{y\in A}d(x,y),\qquad Z=g_A(X),\quad X\sim P.
\]

For a requested acceptance level \(\beta\in[0,1]\), define the action profile

\[
J_{P,A}(\beta)
=\inf_{\substack{\nu\le P\\\nu(\mathsf X)=\beta}}
  \int g_A(x)\,\nu(dx).
\tag{1}
\]

Here \(\nu\le P\) means that \(\nu\) is a sub-probability measure dominated by \(P\). It selects \(\beta\) units of baseline mass to move. Since \(g_A=0\) on \(A\), pre-existing event mass costs zero. The output contract is the minimum infimal expected displacement needed to obtain a law with event probability at least \(\beta\).

For a general acquired action cost \(c(x,y)\ge0\), replace \(d\) by \(c\) and assume \(c(x,x)=0\). Assume \(g_A(x)=\inf_{y\in A}c(x,y)\) is measurable and, for every \(\eta>0\), there is a measurable transport kernel into \(A\) whose expected cost from each input \(x\) is at most \(g_A(x)+\eta\). This is the acquired approximate-realization certificate. The metric case has it for Borel \(A\) on a Polish space, using a universally measurable approximate selector. If the application restricts which transitions or path edits are allowed, the selector must obey those restrictions; otherwise (1) is only a relaxation.

The mean cost in (1) is the declared resource. It can encode spatial displacement, path-edit action, or another per-state intervention cost. It does not include the cost of acquiring \(P\), evaluating \(g_A\), finding the mass threshold, evaluating the transport map, or drawing random bits. Those are separate ledger entries.

## 2. Exact action theorem

Define the lower quantile of \(Z\) by

\[
F_Z^{-1}(u)=\inf\{t\ge0:P(Z\le t)\ge u\},\quad 0<u<1.
\]

**Theorem 1 (event-promotion action law).** Under the interface above, for every \(\beta\in[0,1]\),

\[
J_{P,A}(\beta)
=\int_0^\beta F_Z^{-1}(u)\,du
=\int_0^\infty\bigl(\beta-P(Z\le t)\bigr)_+\,dt
=\sup_{\lambda\ge0}\left\{\lambda\beta-\mathbb E_P[(\lambda-Z)_+]\right\}.
\tag{2}
\]

Moreover,

\[
J_{P,A}(\beta)
=\inf_{Q:\,Q(A)\ge\beta}
  \inf_{\pi\in\Pi(P,Q)}\int d(x,y)\,\pi(dx,dy),
\tag{3}
\]

and the same statement holds with the acquired cost \(c\) in place of \(d\). The infimum need not be attained if nearest points or the action selector are not attained; for every \(\eta>0\), the interface constructs a law with event probability at least \(\beta\) and cost at most \(J_{P,A}(\beta)+\eta\).

**Proof.** First minimize (1). Among all submeasures of mass \(\beta\), the cheapest one contains the \(\beta\) mass with smallest values of \(Z\); at a quantile atom, take just the required fraction. The quantile integral follows. For the layer-cake form, write \(F(t)=P(Z\le t)\). Any selected submeasure \(\nu\) of mass \(\beta\) has

\[
\int Z\,d\nu=\int_0^\infty \nu(Z>t)\,dt
\ge \int_0^\infty (\beta-F(t))_+\,dt.
\]

The lower-quantile selection makes equality hold: below its cutoff it selects all available mass, above the cutoff it selects none, and at the cutoff it takes the needed tie fraction.

For the hinge dual, for every \(\lambda\ge0\) and every \(z\ge0\),

\[
z\ge \lambda-(\lambda-z)_+.
\]

Thus every selected \(\nu\) gives \(\int Z\,d\nu\ge\lambda\beta-\mathbb E_P[(\lambda-Z)_+]\). Taking the supremum gives a lower bound on (1). At a lower-quantile cutoff \(\lambda\), select all points with \(Z<\lambda\) and the required fraction at \(Z=\lambda\). The inequality is then equality, proving the dual representation; limits of cutoffs handle endpoint cases.

For (3), let \(\pi\) couple \(P\) to any \(Q\) with \(Q(A)\ge\beta\). Its incoming crossing mass is \(m_{in}=\pi(A^c\times A)\), and outgoing crossing mass is \(m_{out}=\pi(A\times A^c)\). Marginal balance gives

\[
m_{in}-m_{out}=Q(A)-P(A)\ge\beta-P(A).
\]

Consequently \(m_{in}\ge(\beta-P(A))_+\). On every incoming pair, \(d(x,y)\ge d(x,A)=Z(x)\). The first marginal of these pairs is a submeasure of \(P|_{A^c}\). If \(P(A)\ge\beta\), choose a mass-\(\beta\) submeasure of \(P|_A\), which has zero cost-to-event. If \(P(A)<\beta\), add all of \(P|_A\) to a mass-\((\beta-P(A))\) restriction of the incoming first marginal. In either case the result is a submeasure of \(P\) with mass \(\beta\) and no greater cost than \(\pi\); hence \(J_{P,A}(\beta)\le\int d\,d\pi\).

For the reverse direction, take the lower-quantile submeasure in (1). Leave unselected states fixed. Keep selected states already in \(A\) fixed, and send selected states outside \(A\) into \(A\) using the acquired selector, paying at most \(g_A(x)+\eta\) per selected unit of mass. Every baseline point already in \(A\) remains there; the selected outside mass is added to it. The resulting law has event probability at least \(\beta\) and total action at most \(J_{P,A}(\beta)+\beta\eta\). Since \(\eta\) is arbitrary, the infima agree. For a general cost \(c\), the lower-bound step uses \(c(x,y)\ge g_A(x)\), and the upper-bound step uses the acquired cost selector. \(\square\)

## 3. Operational readings

An implementing kernel selects all states whose cost-to-event is below a threshold \(\lambda\), selects the required fraction of the mass tied at \(\lambda\), transports the selected outside states into \(A\), and leaves the rest fixed. If the baseline is already in \(A\) with probability at least \(\beta\), the identity kernel suffices. The threshold, tie probability, and destination selector are part of the acquired certificate.

The profile is nondecreasing and convex. Its marginal cost, at every continuity point of the quantile, is

\[
J'_{P,A}(\beta)=F_Z^{-1}(\beta).
\]

So the next unit of event mass costs the distance to the event of the next cheapest baseline states. The inverse profile gives the largest event frequency compatible with a transport-action budget, up to the infimum/attainment distinction in Theorem 1.

For an empirical baseline \(P=N^{-1}\sum_{i=1}^N\delta_{x_i}\), sort \(z_i=d(x_i,A)\) increasingly. Then \(J(k/N)=N^{-1}\sum_{i=1}^k z_{(i)}\); for a nonintegral \(N\beta\), use the same full sum plus the required fraction of the next atom. The induced transport moves the selected atoms to closest points in \(A\), with a fractional final atom. This is exactly the geometric mechanism used by the established Wasserstein chance-constraint result reviewed in Section 6.

For an exact sampler implementing the transport, one needs a sampler for \(P\), event membership, the quantile threshold and its tie rule, and an acquired transport map into \(A\). Per output, the expected cost is at least the baseline sample cost plus the evaluation and map costs. If the threshold and map were acquired once at total cost \(C_{acq}\), after \(m\) outputs their amortized cost is \(C_{acq}/m\). The theorem's transport action is an additional resource, and cannot be silently equated with run time or physical feasibility.

## 4. A concrete rare-tail calculation

Let \(X\sim N(0,1)\), \(A=[R,\infty)\), \(R>0\), and \(p=\bar\Phi(R)\). Under Euclidean cost,

\[
Z=(R-X)_+,
\qquad F_Z^{-1}(u)=
\begin{cases}
0,&0<u\le p,\\
R+\Phi^{-1}(u),&p<u<1.
\end{cases}
\]

Therefore, for \(p\le\beta<1\),

\[
J_{P,A}(\beta)
=R(\beta-p)+\phi(R)-\phi(\Phi^{-1}(\beta)).
\tag{4}
\]

Indeed, the cheapest \(\beta-p\) mass outside the event lies just below the normal quantile \(\Phi^{-1}(\beta)\), and the optimal endpoint transport moves it to \(R\). If \(p\to0\) with fixed \(\beta\in(0,1)\), then

\[
J_{P,A}(\beta)=\beta R-\phi(\Phi^{-1}(\beta))+o(1),
\qquad R\sim\sqrt{2\log(1/p)}.
\]

Thus promoting a Gaussian tail to a fixed acceptance level has action of order \(\sqrt{\log(1/p)}\) under Euclidean endpoint cost, even though the original tail probability is exponentially small in \(R^2\). This says how much endpoint displacement is required; it does not provide the target conditional law or a dynamically valid rare-event path.

## 5. Sampling fidelity is a separate coordinate

Suppose \(Q(A)=q>0\), \(P|_A\ll Q|_A\), and \(L=dP/dQ\) on \(A\). The ordinary importance-sampling variable \(Y=1_A(X)L(X)\), with \(X\sim Q\), is unbiased for \(p=P(A)\). Write

\[
m=\mathbb E_Q[L\mid A]=p/q,
\qquad
\kappa_A(Q)=\frac{\mathbb E_Q[L^2\mid A]}{m^2}.
\]

Then the exact relative variance of one importance sample is

\[
\frac{\operatorname{Var}_Q(Y)}{p^2}=\frac{\kappa_A(Q)}{q}-1.
\tag{5}
\]

This follows by expanding \(\mathbb E_QY=q m=p\) and \(\mathbb E_QY^2=q\mathbb E_Q[L^2\mid A]\). With \(n\) independent proposals the relative variance divides by \(n\). Equation (5) makes the missing certificate explicit: large acceptance \(q\) helps only when the conditional likelihood-ratio second moment \(\kappa_A(Q)\) is also controlled. The action profile contains no such information.

Let \(P_A=P(\cdot\mid A)\) and \(Q_A=Q(\cdot\mid A)\). Since \(dP_A/dQ_A=(q/p)L\) on \(A\),

\[
\kappa_A(Q)=1+\chi^2(P_A\|Q_A).
\tag{6}
\]

Thus Equation (5) becomes

\[
\frac{\operatorname{Var}_Q(Y)}{p^2}
=\frac{1+\chi^2(P_A\|Q_A)}{q}-1.
\tag{7}
\]

Also, under \(\|P_A-Q_A\|_{TV}=\frac12\int|dP_A/dQ_A-1|\,dQ_A\), Cauchy–Schwarz gives \(\|P_A-Q_A\|_{TV}\le\frac12\sqrt{\chi^2(P_A\|Q_A)}\). The pair \((J_{P,A}(q),\chi^2(P_A\|Q_A))\) therefore reports two distinct quantities: action to raise acceptance and fidelity of the accepted law.

An importance-sampling certificate can therefore take the form \(Q(A)\ge\beta\), \(\chi^2(P_A\|Q_A)\le D\), and \(P_A\ll Q_A\), with an exact evaluator for \(dP/dQ\) on \(A\). It yields one-sample relative variance at most \((1+D)/\beta-1\). For \(n\) independent proposals, Chebyshev's inequality gives relative error at most \(\varepsilon\) with failure probability at most \(\alpha\) whenever

\[
n\ge\frac{(1+D)/\beta-1}{\alpha\varepsilon^2}.
\]

If each proposal, event check, and likelihood-ratio evaluation costs \(c_Q,c_A,c_L\), respectively, the charged runtime is \(n(c_Q+c_A+c_L)+C_{\mathrm{acq}}\), where \(C_{\mathrm{acq}}\) is the cost of acquiring and checking the certificates. If only unnormalized densities are available, the normalized likelihood ratio is a separate requirement and may contain the unknown event mass itself.

### Failure test: cheap event promotion, bad conditional proposal

Take \(\mathsf X=\{a_0,a_1,b\}\) with distances \(d(a_0,a_1)=1\), \(d(a_0,b)=\epsilon\), and \(d(a_1,b)=1\), where \(0<\epsilon<1\). Let \(A=\{a_0,a_1\}\), and

\[
P(a_0)=P(a_1)=p/2,\qquad P(b)=1-p.
\]

For any fixed target acceptance \(\beta>p\), form \(Q\) by moving mass \(\beta-p\) from \(b\) to \(a_0\), leaving every other point fixed. Then \(Q(A)=\beta\), and this transport attains the action profile

\[
W_1(P,Q)=J_{P,A}(\beta)=(\beta-p)\epsilon.
\]

Yet the target conditional law is uniform on \(a_0,a_1\), while

\[
Q(a_1\mid A)=\frac{p}{2\beta},\qquad
L(a_1)=1,\qquad
L(a_0)=\frac{p/2}{\beta-p/2}.
\]

The target remains absolutely continuous with respect to the proposal on \(A\), but direct substitution in (5) gives

\[
\kappa_A(Q)=\frac{\beta}{4(\beta-p/2)}+\frac{\beta}{2p},
\qquad
\frac{\operatorname{Var}_Q(Y)}{p^2}
=\frac{1}{4(\beta-p/2)}+\frac{1}{2p}-1.
\]

For fixed \(\beta\) and \(p\to0\), the acceptance stays constant and the action tends to zero as \(\epsilon\to0\), while relative variance remains \(\Theta(1/p)\). This defeats any claim that event promotion alone certifies an efficient rare-event estimator. A likelihood-ratio second-moment certificate, support check, or direct conditional-law certificate is an additional acquired input.

### Stronger failure test: fidelity can diverge at fixed event probability

Fix \(0<p<\beta<1\). On \(\mathsf X=\{a_0,a_1,b\}\), set \(d(a_0,a_1)=\delta\), \(d(a_0,b)=\epsilon\), and \(d(a_1,b)=\delta+\epsilon\), with \(\delta,\epsilon>0\). This is the line metric for points \(a_1=-\delta\), \(a_0=0\), \(b=\epsilon\). Let \(A=\{a_0,a_1\}\) and \(P(a_0)=P(a_1)=p/2\), \(P(b)=1-p\).

For \(0<\eta<p/2\), define \(Q_\eta\) by moving \(\beta-p\) mass from \(b\) to \(a_0\), and \(p/2-\eta\) mass from \(a_1\) to \(a_0\). Then \(Q_\eta(A)=\beta\), \(Q_\eta(a_0)=\beta-\eta\), and \(Q_\eta(a_1)=\eta\). The displayed coupling has cost

\[
W_1(P,Q_\eta)\le(\beta-p)\epsilon+(p/2-\eta)\delta.
\]

On \(A\), the likelihood ratios are \(L_\eta(a_0)=p/[2(\beta-\eta)]\) and \(L_\eta(a_1)=p/(2\eta)\). Direct calculation gives

\[
1+\chi^2(P_A\|Q_{\eta,A})
=\kappa_A(Q_\eta)
=\frac{\beta}{4}\left(\frac{1}{\beta-\eta}+\frac{1}{\eta}\right),
\qquad
\frac{\operatorname{Var}_{Q_\eta}(Y)}{p^2}
=\frac14\left(\frac{1}{\beta-\eta}+\frac{1}{\eta}\right)-1.
\]

For fixed \(p,\beta\), choose \(\delta=\epsilon=\eta^2\) and let \(\eta\downarrow0\). Acceptance remains \(\beta\), the explicit transport cost tends to zero, and conditional chi-squared divergence and relative variance diverge like \(1/\eta\). Thus no finite conditional-fidelity bound follows from transport action and acceptance alone, even when \(p\) is fixed.

### Failure test: absolute Wasserstein error is not relative rare-event accuracy

On the line, let \(P=(1-p)\delta_0+p\delta_1\), \(Q=\delta_0\), and \(A=\{1\}\). Then \(W_1(P,Q)=p\to0\), but \(P(A)=p\) and \(Q(A)=0\). A small absolute transport distance therefore gives no relative event-probability guarantee as \(p\to0\). The action profile detects the issue: lowering the event mass by \(p\) costs \(p\,d(1,A^c)=p\).

## 6. Prior-art gate and final status

Chen, Kuhn, and Wiesemann (2022), Theorem 2, show for an empirical baseline that the exact minimum cost to move an \(\varepsilon\)-fraction of the samples to the unsafe set is the sum of the \(\varepsilon N\) smallest distances, with the fractional convention for a noninteger count. Their Theorem 1 gives the corresponding worst-case distribution by moving the nearest samples first and fractionally moving the last sample. They explicitly state that this reproduces closed-form characterizations by Blanchet–Murthy (2019) and Gao–Kleywegt (2016). This is the same empirical action curve as (1)–(3), after switching the event/complement convention.

The full-law action profile is a reparameterization of the event-probability dual in Blanchet–Murthy, not a new general-law theorem. The proof above is an independent derivation from the definitions; the underlying argument is fractional selection plus optimal transport. The conditional chi-squared variance identity is also standard. No independent search of all mathematical literature was performed, so no priority claim is warranted. The useful result for this task is the no-go separator: an event-acceptance/action certificate and a conditional-fidelity certificate are distinct inputs.

The path-space form is valid only if the chosen metric/action and selector represent allowed physical interventions. If the transport map makes trajectories that violate the source dynamics, (3) is an endpoint relaxation. If computing \(g_A\), its quantile, or the event-conditioned likelihood ratio requires the original hard simulation, the certificate has not removed that cost.
