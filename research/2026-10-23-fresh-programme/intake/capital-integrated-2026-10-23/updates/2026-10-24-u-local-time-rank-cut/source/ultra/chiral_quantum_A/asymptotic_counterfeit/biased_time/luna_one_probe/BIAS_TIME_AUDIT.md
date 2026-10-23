# Reversible biased-majority amplification: bounded audit

## Verdict

The probability recursion, its fixed-​p asymptotics, the every-site mismatch formula, and the stretched-exponential-in-time upper bound are correct under the opening's iid Bernoulli(p) input and stated local gate schedule. The exponent is

\[
\alpha=\frac{\ln 2}{\ln 3}\approx 0.6309,
\qquad e_{\rm site}\le C_p\exp[-c_p(JT/\hbar)^\alpha]
\]

for constants depending on fixed \(p\in(0,1/2)\). This is a construction-specific upper bound, not an optimal exponent or a comparison against every reversible compression schedule. Its costs include a fresh biased source and a growing, one-use device; the time exponent does not price those resources away.

## Recursion and asymptotic rate

If each child majority is wrong independently with probability \(\epsilon\), the parent majority is wrong when at least two children are wrong. Hence

\[
\epsilon'={3\choose2}\epsilon^2(1-\epsilon)+\epsilon^3
=3\epsilon^2-2\epsilon^3=:\phi(\epsilon).
\]

For \(0<\epsilon<1/2\),
\[
\epsilon-\phi(\epsilon)=\epsilon(1-\epsilon)(1-2\epsilon)>0,
\]
so the sequence decreases to the only fixed point below its initial value, zero. Also, on \(0<\epsilon\le1/2\),
\[
2\epsilon^2\le\phi(\epsilon)\le3\epsilon^2.
\]
The lower inequality iterates from \(\epsilon_0=p\) to
\[
\epsilon_k\ge\tfrac12(2p)^{2^k}.
\]
For the upper bound choose a finite \(j_0=j_0(p)\) with \(3\epsilon_{j_0}<1\). Setting \(u_j=3\epsilon_j\), the upper inequality gives \(u_{j+1}\le u_j^2\), and therefore
\[
\epsilon_k\le\tfrac13\exp\{-[-\ln(3\epsilon_{j_0})]2^{k-j_0}\},\qquad k\ge j_0.
\]
Together these imply
\[
-\ln\epsilon_k=\Theta_p(2^k)=\Theta_p(L^{\ln2/\ln3}),\qquad L=3^k.
\]
The constants are not uniform as \(p\uparrow1/2\) or \(p\downarrow0\); the claim is for each fixed \(p\in(0,1/2)\).

## Record errors and time conversion

The two inverse strings at fixed full recursive syndrome are complements. Thus a block is either reproduced relative to its reference shift or all its bits flip. Independent source blocks have independent root-majority labels, so the probability that adjacent labels differ is exactly
\[
e_{\rm site}=2\epsilon_k(1-\epsilon_k).
\]
This is the joint per-site mismatch probability for every tested site, not only a block average. For a specified one-bit input label \(b\), with source mass \(p_b\in\{p,1-p\}\),
\[
\Pr[\text{mismatch}\mid X_i=b]
\le \frac{e_{\rm site}}{p_b}
\le \frac{e_{\rm site}}p.
\]
The joint mass of that label and a mismatch is at most \(e_{\rm site}\). These are single-site-label guarantees; they do not give a useful uniform conditional bound for an entire length-\(L\) input word, whose least probability is exponentially small.

Let \(d_k=7(3^k-1)+8k\) be the stated depth bound and \(\tau=\pi\hbar/J\) the gate-time bound. For available time \(T\), take the largest admissible \(k\) with \(d_k\le JT/(\pi\hbar)\). Since \(d_k=7L+O(\log L)\) and \(d_{k+1}=21L+O(\log L)\), this largest fitting \(L=3^k\) is \(\Theta(JT/\hbar)\) at large time. Consequently \(2^k=L^\alpha=\Theta((JT/\hbar)^\alpha)\); the recursion upper bound yields the claimed \(e_{\rm site}\le C_p\exp[-c_p(JT/\hbar)^\alpha]\). The bound is valid for the largest code in this family; it does not assert that this code is the best use of time among all admissible controls.

Conditional on the opening's routing recurrence and its conjectured \(L-1\) coarse-shift swaps, the all-gate arithmetic is consistent: \(G_P(1)=0\), \(G_P(L)=3G_P(L/3)+2(L-3)+10\), giving \(G_P=2Lk+2(L-1)\); two encoders plus those swaps give \(G_\Omega=4Lk+5(L-1)\). This count is \(\Theta(Lk)\). Summed pulse action is at most \(\pi\hbar G_\Omega\) for pulses of duration \(\pi\hbar/J\) and strength at most \(J\); it is \(\Theta(\hbar Lk)\) only if the pulses attain that strength up to constants. This sum over pulses is distinct from parallel depth/time \(\Theta(L\hbar/J)\); the opening's exact physical synthesis of the gate alphabet remains a separate implementation check.

## Resource boundary

The operation consumes a fresh iid biased block of \(L\) bits. Its entropy is \(Lh_2(p)\) bits, with a source bias of \(L[1-h_2(p)]\) bits relative to a uniform block; preparing or maintaining that source is outside the gate-time bound. All \(L-1\) recursive syndrome bits remain in the data. There is no pure work tape, reset, selective discard, or feedback, and the footprint and interaction radius grow as \(O(L)\). After the permutation the data generally carry correlations, so a second independent trial requires a new valid source block; this is a single-use-per-fresh-block statement, not a stationary repeated-cycle or full-record/channel guarantee. This resource dependence also explains why the result does not contradict a uniform-source \(\Theta(1/T)\) bound.

## Gibbs-source net-work check

Take the tested bits to have \(H_0=\Delta\sum_i n_i\), \(n_i=|1\rangle\langle1|\), and prepare the source as the Gibbs product with
\[
p=(1+e^{\beta\Delta})^{-1},\qquad \Delta=\beta^{-1}\ln\frac{1-p}{p}>0.
\]
On a finite periodic device with at least two blocks and size compatible with the block shift, the encoding, coarse countershift and decoding compose to a basis permutation \(U\). For a cyclic operation returning the endpoint Hamiltonian to \(H_0\), Gibbs passivity gives work-on-system \(W=\operatorname{Tr}[H_0(U\tau U^\dagger-\tau)]\ge0\). The reference shift preserves total excitation, and for each computational-basis input/output pair,
\[
\sum_i(n_i^{\rm out}-n_i^{\rm ref})\le \#\{i:n_i^{\rm out}\ne n_i^{\rm ref}\}.
\]
Averaging and using the exact every-site error therefore gives
\[
0\le W/N\le\Delta e_{\rm site}.
\]
For an operationally explicit cycle, prepare under \(H_0\), quench the onsite term off during the fixed local-gate programme, then restore it. The quench/restoration are included in this endpoint net work; any peak borrowed energy, switch/controller cost, or source preparation remains unpriced. Equivalently, onsite cancellation can be included in the driven generators if that is the declared control model. The stated time conversion counts the gate layers; finite-duration switching must be added if not idealized or folded into those layers. The endpoint inequality is not a bound on total control work/action, clock cost, refrigeration, or source/reset cost.

Under the additional contract of independently programmable onsite fields with per-site norm at most \(\Delta\) (or \(\Delta/2\) after subtracting a scalar), use ramps \(H_i(t)=f(t)\Delta n_i\) over exactly \(\tau=\pi\hbar/J\) before and after the pair-gate window, with \(f:1\to0\) and then \(0\to1\). These add \(2\tau\) to the schedule, so the finite-time condition is \(T\ge\tau(d_k+2)\). Each ramp commutes with \(H_0\) and supplies only onsite diagonal phases; these leave computational-basis record probabilities and the Gibbs endpoint-work calculation unchanged. The exact unitary gains onsite layers, which preserve its support radius and index. This completes switching time only under that onsite-field contract; slew-rate, controller, and dissipative costs are still unpriced.
