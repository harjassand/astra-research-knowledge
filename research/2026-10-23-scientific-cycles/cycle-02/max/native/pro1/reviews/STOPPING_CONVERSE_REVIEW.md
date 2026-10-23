# Independent challenge: expected-use stopping converse

Reviewer: `/root/stopping_converse`  
Date: 21 October 2026  
Status: qualified internal mathematical acceptance of the new operation below. This is neither external certification nor historical-priority assessment.

## Scope and source dependence

This review concerns the newly proposed variable-length/expected-use extension. It does not repeat the old unassisted capacity audit. I read the exact tree/Dyck/rank portion of `RECURRENT_RESERVOIRS.tex`, the frozen feedback candidate, and its `ACCEPTED_SCOPE.txt` corrections. The inherited premise is the complete-block Kraus-operator-rank certificate and its unnormalized classical-transcript preservation:

\[
M_n=\left\lfloor(2\sqrt2)^n\right\rfloor\le 2^{cn},\qquad c=3/2.
\]

For a vertex-diagonal initializer, every fixed-\(n\) feedback branch has a Kraus representation with individual operator rank at most \(M_n\). For a density supported on a finite set \(F\) of \(r\) vertex coordinates, the corresponding bound is \(rM_n\). This is not a claim about the number of Kraus operators. The corrections concerning measurable controls, normal instruments, CP densities, and finite vertex-coordinate projections are essential and are retained here.

## Operational assumptions that must be explicit

The same tree device and one fixed normal initializer are used for every logical dimension. The logical input and arbitrary reference are initially independent of the bath and laboratories. Alice and Bob have local ancillary systems, no preshared entanglement, and only noiseless **backward classical** communication in addition to the counted forward qutrit calls. Instruments are normal and their controls measurable, for example with standard Borel outcomes. Integrated instruments, not individual CP Radon--Nikodym densities, obey normalization.

The integer \(N\ge0\) is a receiver-controlled stopping time for the causal transcript. On termination Bob has a decoded \(K\)-dimensional system. The complete, all-branch decoded operation is a trace-preserving channel \(\Lambda_K\). Require termination almost surely on every logical input. The number of forward calls is the cost; no branch is discarded from either fidelity or cost. There is no free Alice-controlled timing, silence, omitted-slot, or forward classical side channel. A receiver stop message may tell Alice that no further call is needed.

Define

\[
\bar n_K=\sup_\rho\mathbb E_\rho N,
\qquad n_K^\circ=\mathbb E_{I/K}N\le\bar n_K,
\qquad F_e=\langle\Phi_K|(\mathrm{id}\otimes\Lambda_K)(\Phi_K)|\Phi_K\rangle.
\]

The proof works with the weaker maximally-mixed-input mean \(n_K^\circ\), and therefore also with the worst-input mean. At a fixed finite \(K\), finiteness of the former implies finiteness of all input means because \(\rho\le K(I/K)\); this does not give a useful uniform-in-\(K\) factor, so the two cost definitions should still be named separately.

This is a change in the communication-cost contract, not a rephrasing of fixed length. A random protocol is still deterministic in the quantum-information sense used here: its unconditioned decoded map is CPTP. A successful-branch fidelity alone would be a different, excluded contract.

## 1. Bounded stopping prefixes inherit the rank certificate

Fix \(L\ge0\). Collect every transcript that stops by call \(L\), retaining its unnormalized decoded branch. These branches define a CP trace-nonincreasing subchannel \(\Lambda_{\le L}\).

One rigorous way to apply the fixed-horizon lemma is mathematical padding. Whenever a branch has already stopped, keep its decoded output in Bob's private register, feed fixed dummy inputs for the remaining calls up to \(L\), and ignore the extra outputs. The extra calls act on the bath/dummy ports and cannot change the stored decoded marginal, even when that marginal is correlated with the bath: a nonselective trace-preserving operation on the complementary systems leaves its reduced state invariant. The flag saying that the original protocol stopped by \(L\) is retained. Selecting that flag at the end recovers precisely \(\Lambda_{\le L}\).

The padded construction is only a proof device. Its extra calls are **not** charged to the real stopping protocol, and no assertion is made that its final bath equals the real final bath.

For every complete transcript in this selected subchannel, the fixed-horizon rearrangement supplies a different encoder \(E_t\), the same device block channel, and a matching decoder branch \(D_t\). Every resulting Kraus operator has rank at most \(M_L\) for a diagonal bath, or at most \(rM_L\) for a bath supported on \(r\) vertex coordinates. Positively integrating measurable branches preserves the finite-dimensional Schmidt-number cone. A continuous-outcome CP density is not individually assumed trace-nonincreasing.

If \(\omega_{\le L}\) is the subnormalized reference/decoded state on input \(\Phi_K\), then

\[
\langle\Phi_K|\omega_{\le L}|\Phi_K\rangle
\le \min\{1,M_L/K\}\operatorname{Tr}\omega_{\le L}
\le M_L/K
\]

for a diagonal bath. The rank-overlap inequality applies directly to each unnormalized pure component and then to the sum; there is no transcript-count factor and no normalization of the selected event.

The stopped-after-\(L\) contribution is positive and its overlap with \(\Phi_K\) is at most its trace \(\Pr_{I/K}(N>L)\). Consequently

\[
\boxed{F_e\le M_L/K+\Pr_{I/K}(N>L).}
\]

Using \(N\ge L+1\) on that event gives

\[
\boxed{n_K^\circ\ge (L+1)[F_e-M_L/K]_+.}
\]

This does not use any finite maximum stopping time. Almost-sure termination gives a well-defined all-branch channel; the event \(N\le L\) itself is bounded and needs no limiting commutation of unbounded expectations.

For a diagonal bath there is also the optional finer representation

\[
F_e\le\sum_{n\ge0}p_n\min\{1,M_n/K\},\qquad
p_n=\Pr_{I/K}(N=n),
\]

obtained by applying the unnormalized branch bound separately at each actual stopping length. It is not necessary for the leading asymptotic theorem. In particular, Jensen cannot be used to replace the right side with \(2^{c\mathbb E N}/K\): the relevant exponential is convex.

## 2. The arbitrary normal coherent initializer requires only one trace-distance error

Let \(P_F=\sum_{v\in F}|v\rangle\langle v|\), \(r=|F|\), \(q=\operatorname{Tr}(P_F\tau)>0\), and

\[
\tau_F=P_F\tau P_F/q,\qquad
\Delta_F=\tfrac12\|\tau-\tau_F\|_1\le\sqrt{1-q}.
\]

The final inequality follows by projecting and normalizing a purification and tracing its purifying subsystem. Arbitrary rank-\(r\) projections do not justify the sum-of-\(r\)-vertex-operators bound and must not replace \(P_F\).

Run only the original protocol's prefix up to call \(L\), with a failure flag for branches still running. After a successful stop, measure the projector \(\Phi_K\) on the stored reference/decoded output. The event

> original protocol stops by \(L\), and the maximally-entangled-state test accepts

is a single effect, with values in \([0,1]\), on the initial bath when all other initial systems and the protocol are fixed. Therefore its probabilities under \(\tau\) and \(\tau_F\) differ by at most \(\Delta_F\). The early-stop probability itself need not be compared, and neither expectation \(\mathbb E_{\tau_F}N\) nor almost-sure termination under \(\tau_F\) is needed.

The rank argument under \(\tau_F\) bounds this event probability by \(rM_L/K\). The still-running contribution under the actual initializer \(\tau\) is bounded by its actual probability. Thus

\[
\boxed{F_e(\tau)\le rM_L/K+\sqrt{1-q}
       +\Pr_{\tau,I/K}(N>L),}
\]

and

\[
\boxed{n_K^\circ(\tau)\ge
(L+1)[F_e(\tau)-\sqrt{1-q}-rM_L/K]_+.}
\]

The coefficient of the trace-distance error is one, with half-trace convention. Bounding two separate event probabilities would unnecessarily introduce a second error term. More seriously, transporting an unbounded expected stopping cost by trace distance would be invalid; the bounded-prefix proof avoids that operation completely.

## 3. Consequence: sharp leading expected cost

Set \(x=\log_2K\) and fix a finite vertex set \(F\) before taking any limit. For sufficiently large \(K\), choose

\[
L_K=\left\lfloor\frac{x-\log_2r-\sqrt{x}}{c}\right\rfloor.
\]

Then \(rM_{L_K}/K\le2^{-\sqrt{x}}\), and \((L_K+1)/x\to1/c\). Every sequence of protocols with \(\liminf F_e\ge f\) satisfies

\[
\liminf_{K\to\infty}\frac{n_K^\circ}{\log_2K}
\ge \frac{[f-\sqrt{1-q}]_+}{c}.
\]

Normality allows an increasing sequence of finite vertex sets with \(q\to1\). Take this cutoff limit **after** the \(K\) limit. Hence

\[
\boxed{\liminf\frac{n_K^\circ}{\log_2K}\ge f/c.}
\]

The same inequality holds with \(\bar n_K\). The bound is uniform over protocols for each fixed \(K,F\), so it also applies to infima of costs over admissible protocols, including infima not attained.

For achievability, let \(m(K)\) be the least \(m\) with \(C_m2^m\ge K\), and use any \(K\)-dimensional subspace of the exact Dyck code. Its length \(n_K=2m(K)\) obeys

\[
n_K/\log_2K\to1/c
\]

by the inherited elementary Catalan bounds. Bob sends one independent classical coin outcome to Alice before any forward call. With probability \(p\), run the exact Dyck code; with probability \(1-p\), make no forward call and have Bob output \(I_K/K\). This gives the complete channel

\[
\Lambda_K=p\,\mathrm{id}_K+(1-p)\,\mathcal D_K,
\qquad \mathcal D_K(X)=\operatorname{Tr}(X)I_K/K.
\]

Its entanglement fidelity and every input's expected cost are

\[
F_e=p+(1-p)/K^2,\qquad \mathbb E_\rho N=p n_K.
\]

For fixed \(f\in(0,1]\), take \(p=(f-K^{-2})/(1-K^{-2})\) for sufficiently large \(K\). Every branch is counted and the output map is deterministic/CPTP. The infimum expected cost \(C_\tau(K,f)\), using either mean convention, therefore satisfies

\[
\boxed{\lim_{K\to\infty}\frac{C_\tau(K,f)}{\log_2K}=
\frac f c=\frac{2f}{3}.}
\]

If a contract requires at least one call, replace the zero-call abort by a fixed two-call push/pop loop, adding only \(O(1)\) cost. The exact Dyck code returns the bath, including correlations with any inert purification, at its endpoint. The zero-call abort does too. Thus this achievability already obeys exact terminal bath return, although the converse does not require return. It does not imply return after every internal use.

## 4. Strong-converse distinction

Reliable transmission means \(F_e\to1\), and the expected-use capacity is still \(c=3/2\). But an expected-use-only contract has no above-capacity strong converse of the fixed-length kind. At any fixed target rate \(R>c\), choose \(p=c/R\). The lottery has

\[
\frac{\log_2K}{\mathbb E N}\to R,
\qquad F_e\to c/R>0.
\]

The converse proves that this positive limiting fidelity is optimal: if the expected rate tends to \(R\), then \(\limsup F_e\le\min\{1,c/R\}\). This is not an increase in reliable capacity and not successful-branch credit. It identifies the exact loss of the strong-converse property under a change from maximum length to expected cost.

## 5. Optional strengthening: uniform complete error

For the complete half-diamond error

\[
\delta_K=\tfrac12\|\Lambda_K-\mathrm{id}_K\|_\diamond,
\]

the maximally-entangled input and its acceptance effect imply \(F_e\ge1-\delta_K\). Therefore a requirement \(\delta_K\le\delta\), fixed \(0\le\delta<1\), gives a lower cost coefficient \((1-\delta)/c\).

The above lottery achieves this coefficient with a direct, self-contained diamond-norm calculation. The depolarizing channel is the average of all \(K^2\) discrete Weyl conjugations. Write

\[
\mathcal D_K=K^{-2}\mathrm{id}_K+(1-K^{-2})\mathcal W_K,
\]

where \(\mathcal W_K\) averages the nonidentity Weyls. Channel distance gives
\(\tfrac12\|\mathrm{id}-\mathcal W_K\|_\diamond\le1\). On \(\Phi_K\), the nonidentity Weyls produce Bell states orthogonal to \(\Phi_K\), attaining equality. Hence

\[
\tfrac12\|\mathrm{id}_K-\mathcal D_K\|_\diamond=1-K^{-2},
\qquad
\delta_K=(1-p)(1-K^{-2})=1-F_e.
\]

Choose \(p=1-\delta/(1-K^{-2})\) for sufficiently large \(K\). It follows that the minimal expected cost under a uniform complete-error bound has leading coefficient

\[
\boxed{\lim_{K\to\infty}\frac{C^{\diamond}_\tau(K,\delta)}{\log_2K}
=\frac{1-\delta}{c}=\frac{2(1-\delta)}3.}
\]

If error is specified as the **full** diamond norm \(e\in[0,2)\), the coefficient is \((1-e/2)/c\). This extension covers arbitrary reference entanglement uniformly and states the full/half conversion explicitly. It is not a statement about bath-return error.

## Gaps searched for, failures excluded, and remaining limitations

- Remote steering does not defeat fixed unnormalized branch factorization; normalizing a branch would.
- The protocol's physical completeness is only used after summing branches; a finite or countable transcript-count factor is never inserted.
- Dummy padding changes the bath but not the already decoded output. Claiming preservation of the padded bath would be false and is unnecessary.
- No comparison of unbounded expectations for nearby bath states is used. Such a comparison is generally invalid.
- The bath cutoff is a finite vertex-coordinate cutoff and is fixed before the large-\(K\) limit. No common exponential or finite-size rate follows for arbitrary normal coherent tails.
- Receiver-controlled stopping excludes a free forward timing channel. This must be in the operation's definition.
- The sharp formulas are leading asymptotic expected-cost statements, not exact finite-\(K\) optima and not efficient circuit constructions.
- Expected-use reliable capacity and absence of a strong converse are different conclusions. The lottery establishes the latter while preserving the former.
- No historical novelty is asserted. The stopping argument is a direct consequence of the supplied block-rank invariant and standard bounded-event/first-moment reasoning; its importance is the changed operational cost/error boundary.

## Review activity and resource record

This review used targeted reads and a symbolic mathematical challenge. It did not rerun the old capacity diagnostics or perform a finite-tree simulation. No numerical experiment is offered as proof. No external person, purchased service, hardware platform, or independently owned programme was used. The inference/tool resource cost is not independently metered.
