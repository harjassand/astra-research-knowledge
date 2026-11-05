# Finite-record weighted evaluation of the acquired local trial

This corollary uses the selected thermal construction as a premise. It removes the optional marking coin when the subsequent physical policy does not use the arm. It is ordinary change of measure and Rao-Blackwellization, with an explicit finite-record implementation and reuse ledger.

## 1. Input contract and target

Write `P` for the momentum at the trigger, `Z` for the remaining physical state, `R` for the old retained classical reference and `T` for the actual private trigger time. The ideal local replacement law is

\[
Q(d p,dz,dr,dt)=G_\sigma(dp)\,\mu(dz,dr,dt).
\]

The hidden/old-reference/clock law `mu` need not be an equilibrium law, and its hidden dimension need not be known. The completed thermal preparation and its priced meter backaction provide a comparison between the actual run and the ideal run through the later outcome. Let its joint total variation error be at most `delta` for `(P,Z,R,T,Y)`. Clock failure can either be a common declared failure branch or be included in `delta`. This corollary does not replace the preparation, clock or backaction proofs.

The ideal future is a single common stochastic channel

\[
K_{r,t}(dy\mid p,z),\qquad |Y|\leq1.
\]

It may include the finite meter window and arbitrary subsequent nonlinear dynamics, observations and control using `R,T`. It must not inspect the new weight cache, the raw momentum-meter record, an optional marking coin, or a copy/side channel of these data. In particular, it must not select a later force using the cached weight. Independent controller randomness is permitted. This restriction is an actual information-routing condition on the apparatus, not an independence claim about the cache: the cache is deliberately correlated with momentum.

Choose a known `L_s`-Lipschitz function `s: R -> [-1,1]` with `E_G s(P)=0`. Define

\[
q_\pm(dp)=G_\sigma(dp)[1\pm s(p)].
\]

For the sinusoidal example, `s(p)=sin(p/sigma)` and `L_s=1/sigma`. The clipped-linear function in the accompanying challenge note is another valid choice. The average trial contrast is

\[
\tau=\int\mu(dz,dr,dt)
\left[\int q_+(dp)K_{r,t}(dy\mid p,z)y
-\int q_-(dp)K_{r,t}(dy\mid p,z)y\right].
\]

The same `mu` occurs in both terms. This definition does not substitute a stationary hidden ensemble, recreate an identical hidden configuration, or assert independence between successive specimens or successive runs.

## 2. Ideal weighted-score identity

Direct substitution gives

\[
\boxed{\tau=2\mathbb E_Q[s(P)Y].}
\]

If an optional arm `A in {-1,+1}` is generated with `Pr(A=a|P)=(1+a s(P))/2`, and the future does not inspect that arm or its coin, then

\[
\mathbb E[2AY\mid P,Z,R,T,Y]=2s(P)Y.
\]

Consequently

\[
\boxed{
\operatorname{Var}(2AY)-\operatorname{Var}(2s(P)Y)
=4\mathbb E[(1-s(P)^2)Y^2]\geq0.
}
\]

No independence between `P` and the future outcome is assumed. The only required conditional independence here is that the unused marking coin does not influence the common future. If the arm chooses a later physical action, that assumption is false and the actual two-arm instrument, with its corresponding target, must be retained.

## 3. Finite implementation

Use the actual finite momentum meter from the thermal construction and let its output be `P_hat`. Permit arbitrary correlation between its error and the subsequent trajectory. It is enough to have the paid mean-error contract

\[
\mathbb E_{\rm actual}|\widehat P-P|\leq e_p.
\]

Alternatively, a good-event error bound plus an overflow probability can be converted directly into the bounded marking-error contract below; unbounded momentum errors on an overflow branch need not be assigned a fictitious finite mean.

Compute an approximation to `s(P_hat)` with uniform error at most `e_calc`, clip it to `[-1,1]`, and round to the nearest grid point in

\[
\mathcal W_K=\{-1,-1+1/K,\ldots,1\}.
\]

Store only the resulting weight `W` in a private cache. It uses at most

\[
b_W=\left\lceil\log_2(2K+1)\right\rceil
\]

bits, apart from the separately priced finite raw-meter and arithmetic workspace. Then

\[
\mathbb E|W-s(P)|
\leq L_s e_p+e_{\rm calc}+\frac1{2K}=:e_W.
\]

A more general meter contract `E|s(P_hat)-s(P)|<=e_s` replaces `L_s e_p` by `e_s`. If this contract holds only outside an event of probability `eta`, add `2 eta`, because both markings are bounded by one. This avoids using total variation alone to infer an unbounded momentum moment.

Operate the common future policy without access to the cache. At the outcome time obtain a finite `Y_hat in [-1,1]` with

\[
\mathbb E|\widehat Y-Y|\leq e_Y.
\]

Compute `2 W Y_hat`, and optionally round it to the nearest point of

\[
\mathcal C_M=\{-2,-2+4/M,\ldots,2\}.
\]

Call this retained score `C`. It uses at most `ceil(log_2(M+1))` bits and the final rounding error is at most `2/M`. The multiplication and comparisons use finite integer/rational arithmetic; their implementation errors, if any, are included in this final rounding allowance or stated separately.

After this computation erase or permanently isolate the weight cache, raw momentum readings, raw outcome readings and scratch registers. Retain only `C` and whatever other finite output registers the programme explicitly chooses. Erasing the cache means it is not available to subsequent plant dynamics, controllers or future choices. A copy in a log, meter buffer or reachable bath is still a record and must be accounted for.

## 4. Finite-error guarantee

Since `|Y|<=1` and `|W|<=1`,

\[
\left|\mathbb E_{\rm actual} C
-2\mathbb E_{\rm actual}[s(P)Y]\right|
\leq2e_W+2e_Y+\frac2M.
\]

This uses only the triangle inequality, so meter errors may be correlated with the hidden state and with the future outcome. The integrand `2s(P)Y` ranges from `-2` to `2`. The stated joint TV error therefore gives

\[
\boxed{
\left|\mathbb E_{\rm actual}C-\tau\right|
\leq4\delta+2L_s e_p+2e_{\rm calc}
+\frac1K+2e_Y+\frac2M.
}
\]

Use `2e_s` in place of `2L_s e_p` under the bounded marking-error alternative. If the outcome itself is quantized with grid spacing `1/L`, its rounding contribution is at most `e_Y=1/(2L)` in addition to its physical metrology error.

Thus finite precision is explicit. For an allocated additional bias `epsilon`, choosing `K,M=O(1/epsilon)` requires `O(log(1/epsilon))` weight/output bits, while `e_p=O(epsilon/L_s)`, `e_calc=O(epsilon)` and `e_Y=O(epsilon)` are actual meter/computation contracts. The theorem does not make acquisition of that accuracy free. The root programme separately supplies repeated-run statistics and exposure costs; no independent-run claim is used here.

## 5. The next-round entropy ledger counts the retained record

Let `S'` denote the plant state after the common future and outcome interaction. Write `R_old` for all pre-existing records and controller variables that remain accessible to the next round. Suppose the already paid physical evolution, action and metrology have established

\[
D(\rho_{S'R_{\rm old}}\Vert\pi_{S'}\rho_{R_{\rm old}})
\leq D_{\rm base}.
\]

Let `C_all` be the complete *actually retained* new finite output: for example the quantized score, a quantized timestamp, failure flags and a finite outcome label if that label is kept. Appending that output gives the exact identity

\[
D(\rho_{S'R_{\rm old}C_{\rm all}}
\Vert\pi_{S'}\rho_{R_{\rm old}C_{\rm all}})
=D(\rho_{S'R_{\rm old}}\Vert\pi_{S'}\rho_{R_{\rm old}})
+I(S':C_{\rm all}\mid R_{\rm old}).
\]

Therefore

\[
\boxed{D_{\rm next}\leq
D_{\rm base}+H(C_{\rm all}\mid R_{\rm old})
\leq D_{\rm base}+\log|\mathcal C_{\rm all}|.}
\]

If only `C in C_M` is retained, the added term is at most `log(M+1)` nats. If a campaign keeps only an updated finite accumulator, apply the same identity to that actual accumulator and its retained auxiliary flags, not to an imagined archive of erased samples. Which variables count as `R_old` must match the real controller implementation.

The temporary weight and raw readings do not contribute an additional entropy term **after they have actually been removed from the next round's accessible reference**. This conclusion does not say that they were independent of the plant, or that their acquisition and reset were free. It follows because the final joint state is the marginal on `S',R_old,C_all`. The physical reset/isolation must not secretly act back on `S'`; any such action belongs in `D_base` and the physical-error budget.

For a finite imperfect reset, include the accessible residual register `B_res`. If it has at most `d_res` states and is blank with probability at least `1-eta_reset`, its extra entropy cost is bounded by

\[
H(B_{\rm res})\leq h_2(\eta_{\rm reset})
+\eta_{\rm reset}\log(d_{\rm res}-1)
\]

for the usual small-error range `eta_reset<=1-1/d_res`; a trivial `log d_res` bound always remains available. This term, or an actually retained reset-failure flag and its associated branch, prevents a finite reset error from being mistaken for exact deletion. Exact analog timestamps or analog meter pointers that remain accessible cannot be charged as a finite-bit output without an additional argument.

## 6. Physical costs and scope

The finite implementation retains the private weight for the complete future-outcome duration. It pays its memory protection, initialized workspace, momentum and outcome metrology, clock, arithmetic and the energy/time of reset or isolation. A reset protocol on `b_temp` temporary bits has its actual duration, error and work bill; no universal finite-cost perfect erase is asserted here. Keeping a fresh isolated cartridge instead pays its growing occupied storage. The retained score requires its own storage/protection and is part of the next-round information ledger.

This corollary avoids an unnecessary coin for evaluating a common future response. It does not create the physically arm-routed channel, speed up rare-event production, or turn the hidden state into an independent fresh specimen. Its advantage over the arm score is an exact variance reduction under the stated information-routing contract. The physical achievement being reused is the preceding acquisition of local independence from hidden state and old references.
