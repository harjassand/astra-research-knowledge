# Directed positive realization from a consequence-sufficient excursion record

Independent ordinary mathematical review of root's construction, with exact rational full-generator controls. This review is separate from the earlier statistical review in this directory. No native acquisition was repeated and no random source was called.

**Finding.** The construction is sound with the explicit qualifications below. For any exact native record from a finite irreducible continuous-time Markov chain, a positive chain with at most

\[
 m+\lceil1/\epsilon\rceil t+1,
 \qquad t=\#\{(i,j):M_{ij}>0\}\le m^2,
\]

states preserves the endpoint flows, all endpoint-marked first residence moments, port weights, port holding rates, both reduced population loads, and total mass. It increases only the scalar residual residence contribution, from \(c\) to \(\widehat c\in[c,(1+\epsilon)c]\). It therefore gives a simultaneous one-sided relative guarantee for the declared equilibrium mean family, while preserving boundary-started means exactly. The dependence on \(1/\epsilon\) has the correct worst-case order within this record-preserving positive-CTMC class. The state bound is not a bound on preparation effort, numerical bit complexity, rates, or physical construction.

An additional exact corollary follows: the same construction realizes the entire record exactly with an instance-dependent phase count determined by an aggregate conditional-variance margin. That count cannot be bounded by the number of ports alone.

## 1. Native record and nonsymmetric identities

Let \(Q\) be the generator of a nontrivial finite irreducible CTMC, and let \(w>0\) be any common-scale stationary weight vector. Write

\[
 L=-\operatorname{diag}(w)Q,
 \qquad L\mathbf1=0,
 \quad \mathbf1^TL=0.
\]

The retained set \(B\) contains \(m\ge1\) ports; \(I\) is its complement. A native trial starts with an actual departure from port \(i\), ends on its first return to any port \(J\), and records the intervening interior time \(\sigma\). A direct jump to another port has \(\sigma=0\). A self-return is possible only through positive interior time. The holding time at the departure port is excluded from \(\sigma\).

Put

\[
 \lambda_i=-Q_{ii},\quad s_i=w_i\lambda_i,
 \quad P_{ij}=\Pr_i(J=j),
\]

\[
 F_{ij}=s_iP_{ij},\qquad
 M_{ij}=s_i\mathbb E_i[\sigma\mathbf1_{\{J=j\}}],
 \qquad c=\frac12\sum_i s_i\mathbb E_i\sigma^2.
\]

These are exact mathematical inputs to the realization theorem. Neither positivity nor a finite number of coefficients acquires their values experimentally.

For a direct check of the identities, define

\[
 A=-Q_{II},\quad D_I=\operatorname{diag}(w_I),\quad
 G=L_{II}=D_IA,\quad C_{BI}=-L_{BI}.
\]

Let \(C_{BB}\) be the matrix of native direct boundary-to-boundary flows, with zero diagonal. Absorption formulas give

\[
 F=C_{BB}+C_{BI}A^{-1}Q_{IB},
 \qquad M=C_{BI}A^{-2}Q_{IB}.                 \tag{1}
\]

Stationarity on the interior is

\[
 \mathbf1^TC_{BI}=w_I^TA.
\]

Since \(A\mathbf1=Q_{IB}\mathbf1\), equation (1) yields

\[
 M\mathbf1=C_{BI}A^{-1}\mathbf1,
 \quad \mathbf1^TM=w_I^TA^{-1}Q_{IB},
 \quad c=w_I^TA^{-1}\mathbf1=w_I^TG^{-1}w_I. \tag{2}
\]

The last identity also follows by summing the native second-moment formula \(2C_{BI}A^{-2}\mathbf1\). Consequently the reduced record is

\[
 S=\operatorname{diag}(s)-F,
 \quad b_R=w_B+M\mathbf1,
 \quad b_L=w_B+M^T\mathbf1.                  \tag{3}
\]

Both row and column sums of \(F\) equal \(s\). Thus \(S\) is an Eulerian directed Laplacian, and

\[
 \mathbf1^Tb_R=\mathbf1^Tb_L=\mathbf1^Tw.
\]

No detailed-balance equality is used. In general \(b_R\ne b_L\).

For a nonempty port target \(A_B\subseteq B\), let \(R_B=B\setminus A_B\). The full killed Poisson equation reduces to

\[
 h_{R_B}=S_{R_BR_B}^{-1}b_{R,R_B}.          \tag{4}
\]

Its mean under the stationary weights conditioned outside the target is

\[
 T_{A_B}=\frac{c+b_{L,R_B}^T
              S_{R_BR_B}^{-1}b_{R,R_B}}
              {\mathbf1^Tw-\sum_{a\in A_B}w_a}.         \tag{5}
\]

When every port is targeted, the inverse term is empty and the numerator is simply \(c\). A query conditioned on an empty live set is undefined and is omitted. The trivial one-state chain without departures can be handled separately without an excursion record.

## 2. Channel-by-channel positive construction

For each channel with \(F_{ij}>0\) and \(M_{ij}>0\), set

\[
 \mu_{ij}=M_{ij}/F_{ij},
 \qquad
 a=\frac12\sum_{M_{ij}>0}\frac{M_{ij}^2}{F_{ij}}.
\]

Conditional Jensen gives \(a\le c\), even when a conditional channel has an atom at zero from a direct transition. Let

\[
 k=\lceil1/\epsilon\rceil,
 \qquad q_{k,ij}=\mu_{ij}^2(1+1/k),
 \qquad c_0=(1+1/k)a.                     \tag{6}
\]

Initially replace the channel by \(k\) directed serial exponential phases, each with mean \(\mu_{ij}/k\). This is an Erlang law with mean \(\mu_{ij}\) and second moment \(q_{k,ij}\).

If \(c_0>c\), keep these phases. Then

\[
 c<\widehat c=c_0\le(1+1/k)c\le(1+\epsilon)c.
\]

If \(c_0\le c\) and \(c>0\), choose any positive-duration channel, say \((i_*,j_*)\), and increase only its conditional second moment to

\[
 q_*=q_{k,i_*j_*}+\frac{2(c-c_0)}{F_{i_*j_*}}.           \tag{7}
\]

Then \(\widehat c=c\). If \(c=0\), every \(M_{ij}=0\); retain only direct transitions and do not choose a channel.

### Realizing every required conditional second moment

Fix \(\mu>0\) and \(q\ge q_k=\mu^2(1+1/k)\).

If \(q=q_k\), use the Erlang law. For \(q_k<q<2\mu^2\), necessarily \(k>1\); mix an Erlang law of mean \(\mu\) and an exponential law of the same mean, putting probability

\[
 \alpha=\frac{q-q_k}{2\mu^2-q_k}
\]

on the exponential. Both component means equal \(\mu\), so the first moment remains exact and the second moment is the desired convex combination. There are \(k+1\) states. At \(q=2\mu^2\), use only one exponential state.

For \(q>2\mu^2\), use two exponential branches with means

\[
 \mu_f=\mu/2,
 \qquad\mu_s=q/\mu-\mu,
 \qquad p_s=\frac{\mu^2}{2q-3\mu^2}.
\]

These numbers are positive, with \(0<p_s<1\), and direct substitution gives

\[
 (1-p_s)\mu_f+p_s\mu_s=\mu,
\]

\[
 2[(1-p_s)\mu_f^2+p_s\mu_s^2]=q.            \tag{8}
\]

For \(k=1\), the interval \((q_k,2\mu^2)\) is empty; the mixture formula with a zero denominator is never evaluated. Zero-probability branches are deleted.

### Converting those duration laws to one stationary CTMC

Give each branch stationary flow equal to its channel flow times its mixture probability. Every phase on the branch receives stationary mass equal to that branch flow times its own holding mean. Connect port \(i\) to the first phase, the serial phases to one another, and the last phase to port \(j\), with the assigned constant branch flow. Dividing each outgoing flow by its state's assigned mass defines its positive transition rate.

Keep all port weights \(w_B\). A zero-duration channel \(M_{ij}=0\) is a direct edge carrying flow \(F_{ij}\). Such an edge requires \(i\ne j\). A genuine native CTMC record automatically has

\[
 F_{ii}>0\quad\Longrightarrow\quad M_{ii}>0,             \tag{9}
\]

because an actual departure cannot return to the same state in zero time. A purported record violating (9) must be rejected; a generator diagonal is not a legal self-jump. Positive-duration self-return channels are fully supported.

Every phase has equal incoming and outgoing flow. Equal row and column marginals of \(F\) give stationarity at every port. The port return graph of an irreducible source is strongly connected, so the constructed chain is irreducible after deleting zero-probability branches. Its native port departure flow remains \(s_i\), and hence its native holding rate remains exactly

\[
 \widehat\lambda_i=s_i/w_i=\lambda_i.
\]

Each channel has hidden stationary mass \(F_{ij}\mu_{ij}=M_{ij}\). Thus the construction preserves \(F,M,w_B\), both loads in (3), \(S\), and total mass. Equations (6)-(8) prove the claimed interval for \(\widehat c\).

The baseline uses \(kt\) hidden states. Only one channel may need extra states, and its replacement uses at most \(k+1\), including the two-state hyperexponential when \(k=1\). Therefore the total is at most \(m+kt+1\). The bound can be reduced in degenerate cases but no reduction is needed for the theorem.

## 3. What the simultaneous guarantee covers

For a passive exterior, stationary weights and flows must be calibrated in the same scale as the original source. After eliminating any external hidden nodes, a live-system numerator has the form

\[
 N=c+c_{\mathrm{ext}}+
   (b_L+\ell)^T(S+R)^{-1}(b_R+r),             \tag{10}
\]

where external residence \(c_{\mathrm{ext}}\ge0\), the loads \(\ell,r\ge0\), and the grounded M-matrix inverse is entrywise nonnegative. The positive denominator is unchanged. The construction modifies only \(c\), so

\[
 0\le\widehat N-N=\widehat c-c\le\epsilon c\le\epsilon N.
\]

Consequently every declared mean in this family satisfies

\[
 T\le\widehat T\le(1+\epsilon)T.             \tag{11}
\]

Equation (5) is the target-only case. Equations (4) and (10) show that boundary-started mean fields are exact, including in the same external contexts. The guarantee does not depend on a spectral gap, a minimum target probability, or an upper bound on the mean.

For fixed native killing hazards \(\kappa_i\) at ports, the grounded flow contribution is \(\operatorname{diag}(w_B\kappa)\). Preserving \(w_B\) is therefore essential. It is retained here. An arbitrary intervention that changes the source's invariant weights is outside this passive-interface theorem; it cannot be silently reinterpreted as a calibrated attachment.

The theorem concerns these mean observables. It does not approximate all hitting-time distributions, correlations, path laws, or an arbitrary entrance distribution inside the eliminated states. Different phase realizations can disagree sharply on those objects.

## 4. Separator regions require separately retained residence residuals

Suppose each hidden excursion remains in its departure module and returns to a port in that module; cross-module jumps are direct boundary jumps. For any positive-duration channel, its endpoints therefore belong to the same declared module. Let \(c_u\) be the second-moment residual in module \(u\).

Apply (6)-(8) separately in every module, producing

\[
 c_u\le\widehat c_u\le(1+\epsilon)c_u.
\]

The resulting state bound is \(m+kt+g\), where \(g\) is the number of modules with positive residence residual. More precisely,

\[
 t\le\sum_u |B_u|^2.
\]

For a target made of complete modules, remove the target modules' hidden population, their \(c_u\), and their associated load contributions. Keep the globally grounded boundary operator, including killing by cross-module direct jumps. The live numerator has the same positive form, with \(c\) replaced by the sum of live \(c_u\); (11) follows. Boundary-started means remain exact because the retained first-moment channels still have their correct module assignment.

**Matching only the global \(c\) is insufficient.** The exact control includes two modules with residuals \(3/5\) and \(3\). At \(\epsilon=1/3\), a construction that matches their sum exactly but places the residual adjustment in the wrong module has a whole-module target mean ratio approximately \(1.555555555554398\), exceeding \(4/3\). For the other target it underestimates by a factor approximately \(0.888888888889\). The modulewise construction satisfies its bounds in both cases. These numbers are evaluations of exact rational quantities in the receipt, not statistical results.

## 5. Additional exact corollary: the variance margin controls phase cost

For a valid finite CTMC with any positive-duration channel, its conditional residence law has positive variance. This remains true if it also has an atom at zero. Therefore Jensen is strict in the sum:

\[
 a<c.
\]

Choose

\[
 k_{\mathrm{exact}}=
 \max\left\{1,\left\lceil\frac{a}{c-a}\right\rceil\right\}.       \tag{12}
\]

Then \((1+1/k_{\mathrm{exact}})a\le c\), so the second branch of the construction applies and matches \(c\) exactly. Hence every exact finite source record has an exact positive realization with at most

\[
 m+k_{\mathrm{exact}}t+1
\]

states. For \(a=c=0\), direct edges suffice. The regionwise version uses each \(a_u/(c_u-a_u)\) separately.

This does not contradict the exact two-port lower bound: the quantity \(c-a\) can approach zero. For a conditional Erlang-\(n\) law of mean one, \(a=1/2\), \(c-a=1/(2n)\), and equation (12) returns \(k_{\mathrm{exact}}=n\). It identifies the missing conditioning parameter in an exact phase count.

## 6. Worst-case order of the accuracy cost

The classical phase-type bound is

\[
 \mathbb E\tau^2\ge(1+1/k)(\mathbb E\tau)^2
\]

for a proper absorption law with at most \(k\) transient states. This is the Aldous-Shepp theorem; the root file `REVERSIBILITY_AND_REALIZATION.md` also supplies a self-contained martingale proof at the precise scope needed here. It allows loops, branching, and an arbitrary initial transient-state distribution.

For the two-port directed cycle with \(n\) hidden Erlang phases, retain

\[
 F_{01}=F_{10}=1,\quad M_{01}=1,\quad M_{10}=0,
 \quad w_B=(1,1),\quad c_n=(1+1/n)/2.
\]

Any positive CTMC preserving these \(F,M,w_B\) must have a positive-duration channel of mean one. A possible direct zero-time contribution does not evade the bound. If the conditional probability of entering hidden states is \(p\le1\), applying the phase-type inequality after entry gives a second moment at least \((1+1/k)/p\ge1+1/k\). Thus any such realization satisfying \(\widehat c\le(1+\epsilon)c_n\) must obey

\[
 k\ge\frac{1}{\epsilon+(1+\epsilon)/n}.       \tag{13}
\]

Taking arbitrarily large \(n\) proves the worst-case \(\Omega(1/\epsilon)\) order. This establishes the accuracy dependence at fixed two-port size, not optimal dependence on \(m\). It is a lower bound for record-preserving positive Markov realizations, not a bound for formulas, semi-Markov laws, arbitrary simultaneous perturbations of the record, or runtime for answering the mean queries.

Primary source: D. Aldous and L. Shepp, *The least variable phase type distribution is Erlang* (1987), DOI [10.1080/15326348708807067](https://doi.org/10.1080/15326348708807067), [primary repository](https://escholarship.org/uc/item/7w51x4rb). Erlang and hyperexponential moment matching are conventional ingredients. This review does not establish historical priority for the combined mean-interface construction.

## 7. Marked first-moment acquisition and its unperformed obligation

Suppose a legal reset-and-departure interface provides independent native trials and a separately warranted tail envelope

\[
 \Pr_i(\sigma>t)\le C e^{-\gamma t}.
\]

Fix a censor horizon \(H\). Record \(J\) and \(\sigma\) for returns by \(H\), and a pending flag otherwise. For every endpoint use

\[
 Y_{ij}=\sigma\mathbf1_{\{\sigma\le H,J=j\}},
 \qquad 0\le Y_{ij}\le H.
\]

The unobserved endpoint-marked contribution is bounded by

\[
\begin{aligned}
0&\le\mathbb E_i[\sigma\mathbf1_{\{J=j\}}]-\mathbb E_iY_{ij}\\
 &\le\mathbb E_i[\sigma\mathbf1_{\{\sigma>H\}}]\\
 &=H\Pr_i(\sigma>H)+\int_H^\infty\Pr_i(\sigma>t)\,dt\\
 &\le Ce^{-\gamma H}(H+1/\gamma).             \tag{14}
\end{aligned}
\]

The \(H\) term is necessary for this unknown-endpoint estimator. The smaller residual \(Ce^{-\gamma H}/\gamma\) applies to the unmarked truncated-duration estimator \(\min(\sigma,H)\), whose boundary-horizon part is observed even for a pending trial. It is not a valid replacement in (14).

For concentration one may use the bounded range and

\[
 \operatorname{Var}(Y_{ij})\le\mathbb E\sigma^2\le2C/\gamma^2.
\]

A duration timestamp error bounded by \(a_t\) contributes at most \(a_t\) to each trial's first-moment error. Endpoint identity, horizon classification, resetting, independence, and the tail envelope are distinct acquisition requirements. Multiply a simultaneous conditional-moment interval by a valid flux interval to obtain an interval for \(M_{ij}\).

For a nonreversible source, \(s\) is a stationary left vector of \(P\). Detailed-balance path ratios are generally invalid. An anchored stationary solve with verified uncertainty, or an appropriate positive Markov-chain-tree calculation, can recover its calibration from sufficient endpoint information, but its conditioning and preparation cost must be charged. If \(s\) is directly supplied, its source and calibration remain explicit premises. Fixed holding-rate estimates alone do not supply \(s\).

**No nonreversible finite-count acquisition certificate was executed here.** The existing frozen numerical assays and the earlier statistical review remain reversible. Their raw endpoint/duration format is compatible with computing marked moments, but this does not retroactively establish a nonreversible stationary-flux certificate or a source tail warranty. The present construction begins with an exact supplied record; (14) specifies one component of a future acquisition argument.

## 8. Exact controls, costs, and comparison

The executable `check_nonreversible_approximate_realization.py` constructs full positive source and fitted generators independently, using `fractions.Fraction`. It then eliminates the full interior and solves full killed systems. The associated receipt is `NONREVERSIBLE_APPROXIMATE_REALIZATION_CHECKS.json`.

The completed run checked:

- Twenty-eight source/accuracy combinations, including directed channels, hidden self-returns, direct transitions, zero interior mass, \(k=1\), and all four phase-construction branches.
- Exact preservation of \(F,M,w_B,s,S,b_L,b_R\), total mass, and positive stationarity in every fitted generator.
- Eighty-eight full-generator equilibrium port-target means and the exact boundary mean fields.
- Eighty-four passive exterior means, including external population and residence, with the exact numerator change \(\widehat c-c\).
- Two complete-module target queries, plus the explicit global-\(c\)-only failure described above.
- Six instance-dependent exact constructions from equation (12), and fifteen exact checks of the lower-bound algebra (13).

All mathematical controls use rational arithmetic. Decimal displays and wall-clock timing are merely reporting conveniences. The run made zero RNG calls and zero acquisition-source calls. These finite controls catch implementation and orientation errors; the preceding ordinary proof supplies the general theorem. This is independent review of the root proposal, not a claim that a second external referee or proof assistant has verified it.

Given an exact record, preparing channel parameters takes \(O(m^2)\) scalar operations plus construction of at most \(O(m^2/\epsilon)\) phases. Exact arithmetic bit complexity depends on record precision and parameter magnitudes. Very large required second moments can create tiny mixture probabilities or slow phases; nearly deterministic durations require many fast phases as \(\epsilon\) decreases. The state count does not make those costs disappear. Simulating the fitted chain incurs its native jump and residence costs.

The strongest equally informed conventional mean solver uses the same \(m\)-port nonsymmetric Schur system directly and needs no phase expansion. It will normally be the preferable route for these mean queries. It can also adopt the present phase construction whenever a positive Markov model is required. The substantive output of this construction is therefore a uniform **positive realization theorem for the declared consequence interface**, and a separation between exact and fixed-relative-accuracy phase cost, rather than a faster matrix solver or a demonstrated acquisition advantage.
