# Adversarial audit of the baseline covariance chemistry certificate

**Disposition:** The proposed inequalities are mathematically correct for a strictly positive deterministic mass-action state when **every hidden reversible pair is individually balanced at the baseline**, (Q) is the consistently normalized full-species infinitesimal jump covariance of those pairs, and the stated exponent bound (M) holds for every hidden complex. The useful zero criterion is exact under those assumptions. Baseline stationarity, baseline covariance, and even separately observed total forward/backward jump rates do **not** establish the individual-balance premise. It is therefore a conditional certificate for a trusted equilibrium hidden class, not a model-free way to dismiss unknown side reactions in a driven manufacturing reactor. Novelty and practical advantage are unknown.

## Algebra and exact quantifiers

Write (s_r=\beta_r-\alpha_r), (a_r^+(c)=a_r^-(c)=w_r>0), and (c'=c\odot e^h). Define

\[
\theta_r(h)=\int_0^1\exp\big((1-t)\alpha_r\cdot h+t\beta_r\cdot h\big)\,dt.
\]

Then (e^{-M}\leq\theta_r\leq e^M) and (F_H(c')=-\sum_r w_r\theta_r s_r(s_r\cdot h)). Consequently, with (Q=2\sum_r w_rs_rs_r^\top),

\[
|z\cdot F_H(c')|\leq\frac{e^M}{2}\sqrt{(z^\top Qz)(h^\top Qh)},\qquad
\frac{e^{-M}}2 h^\top Qh\leq-h\cdot F_H(c')\leq\frac{e^M}2 h^\top Qh.
\]

The factor (1/2) is right. Since all (w_r>0), (Q_h=0\) iff (s_r\cdot h=0\) for **each** hidden pair. Under individual baseline balance, this makes each pair balanced at (c'), hence (F_H(c')=0). Conversely, if (Q_h>0), (-h\cdot F_H(c')>0), so (F_H(c')\neq0). The zero equivalence does not need (M); the nonzero magnitude bounds do.

## Baseline-indistinguishable counterexample when individual balance is unacquired

At (c=(A,B)=(1,1)), consider two open, reversible, mass-action pairs:

| Pair | Forward rate | Reverse rate | (s) |
|---|---:|---:|---|
| (\varnothing\rightleftharpoons A) | (2) | (A) | ((1,0)) |
| (B\rightleftharpoons A+B) | (B) | (2AB) | ((1,0)) |

The individual currents at baseline are (+1,-1); the *aggregate* forward and reverse event rates are both (3). Thus the complete observed species drift is zero and the baseline jump covariance is (Q=6e_Ae_A^\top). Take (h=(0,\log2)), hence (c'=(1,2)) and (Q_h=0). The first current remains (+1), the second becomes (-2), and (F_H(c')=-e_A), directly violating a zero-flux conclusion if aggregate stationarity were substituted for pairwise balance. The stated exponent premise even holds with (M=\log2); only individual baseline balance fails.

An individually balanced comparator with the *same two reaction complexes* and forward/reverse rates (3/2,3/2) for each pair has the **same** aggregate (+A,-A) rates (3,3), drift zero, and (Q=6e_Ae_A^\top) at baseline. After (B\to2), its drift remains zero. Hence an arbitrarily accurate observation of the full baseline species jump process at that one state cannot distinguish the two mechanisms if reaction identity is hidden. [Exact rational replay](chemistry_counterexample.py) also finds a sign failure: at (A=11/10,B=1/4), the cancelling-current network has (F_A=3/5), so (-h\cdot F_H=-(3/5)\log(11/10)<0) while (Q_h>0). The advertised dissipative lower bound cannot be extended to merely stationary hidden networks.

For context, [Feinberg's primary conditions for detailed balancing](https://doi.org/10.1016/0009-2509(89)85124-3) explicitly require rate-constant structure beyond stationarity; [Müller and Joshi's primary graph-theoretic paper](https://doi.org/10.1007/s11538-020-00792-1) distinguishes detailed from complex balance and gives stationary non-detailed-balanced examples. I inspected Feinberg's abstract and the Müller–Joshi abstract, introduction, and example passages; the concrete counterexample above is my own.

## Salvage with a paid nonequilibrium-current budget

If individual balance is unavailable, write (w_r=(a_r^++a_r^-)/2), (j_r=a_r^+-a_r^-), and (\bar e_r=(e^{\alpha_r\cdot h}+e^{\beta_r\cdot h})/2). The exact identity is

\[
F_H(c')=-\sum_r w_r\theta_r s_r(s_r\cdot h)+\sum_r j_r s_r\bar e_r.
\]

If the hidden aggregate is stationary at (c), so (\sum_r j_rs_r=0), the extra term is (\sum_r j_rs_r(\bar e_r-1)). Therefore one can add the explicit uncertainty term

\[
|z\cdot F_H(c')|\leq\frac{e^M}{2}\sqrt{Q_zQ_h}+(e^M-1)\sum_r|j_r(z\cdot s_r)|.
\]

This valid extension exposes the acquisition burden: (Q) alone does not bound the last term tightly when invisible currents cancel. A verified bound on absolute hidden pair currents or perturbation responses must be purchased. In the counterexample (Q_h=0) but the residual term is nonzero.

## Physical acquisition, strongest comparator, and decisive test

- **Channel premise:** A production reactor often has chemostatted reagents, fuels, catalysts and byproducts. Its net stationary composition does not certify detailed balance of unknown side reactions. Pair-resolved forward/reverse rates or a justified closed-equilibrium class plus a complete thermodynamic mechanism are needed. An apparently reversible arrow is insufficient.
- **Full covariance:** (Q=2\sum wss^\top) is a conditional, infinitesimal covariance in molecule-count units when (w) is events/time. If (c) denotes concentration and (w) concentration flux, observed concentration covariance rate is (Q/V) for volume (V); normalization must be explicit. Finite-frame imaging adds detector noise, missed fast events, transport and changing state. Projected observables (y=Px) provide (PQP^\top), not generally (Q_h) or (Q_z). Known channels must be separated to get hidden (Q). Total (Q\succeq Q_{\rm hidden}) gives conservative **upper** bounds for absolute flux and dissipation under detailed balance, but not the stated lower dissipation bound; its zero test is stronger than hidden balance and is not equivalent to it.
- **Exponent premise:** (M\geq\max_r\{|\alpha_r\cdot h|,|\beta_r\cdot h|\}) requires a bound on every hidden reactant/product complex, or a direct upper bound on their activity changes. Even under pairwise detailed balance, a hidden (nB\rightleftharpoons A+nB) pair at (c=(1,1)) has the same baseline (Q=2e_Ae_A^\top) for every (n) when both rates equal one, but after (A,B\to2A,2B) its flux is (-2^n e_A). Unknown spectator order makes a fixed (M) unavailable. At low copy number, stochastic propensities use falling factorials and the exact exponential shift needs replacement or a large-volume limit.
- **Precision and cost:** Finite data cannot prove (Q_h=0) exactly. If a single event type with known projected jump (d=s\cdot h\) has zero observed events over time (T), an ideal 95% upper event-rate bound is about (3/T), giving (Q_h\lesssim3d^2/T) for that type; unobserved channels and detector efficiency worsen it. Acquiring (Q) at a held baseline requires preparation, state feedback, calibration, event bandwidth, repeated trajectories and volume normalization. The full-resource comparator is direct measurement of target-composition drift/product flux and conventional network identification with the same access, if the target can be safely prepared. The certificate wins only if baseline covariance and trusted equilibrium/support bounds are materially cheaper or safer at the needed accuracy.

The decisive empirical test is twofold: first, demonstrate the baseline-indistinguishable pair of mechanisms above or an equivalent hidden-current chemical system, perturb (B), and observe the divergent (A) drift; second, on a proposed *actual* detailed-balanced side-network class, independently validate pair balance and bound (M), measure the **full normalized** covariance at baseline, then blindly compare predicted target-drift envelopes with measured target drift after subtracting known channels. No such laboratory validation was performed. [Gillespie's primary chemical-Langevin paper](https://doi.org/10.1063/1.481811) was inspected at the abstract level for the well-stirred, reaction-channel noise premise; the covariance formula and acquisition critique above are direct derivations, not source-reported measurements.
