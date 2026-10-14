# Post-freeze audit of the root observation-channel packet

This comparison was made after the original FJ packet and the first delta
audit were frozen. It does not edit either packet. The root-proposed exact
two-type witness and conservative rational caps were independently checked
against `work/FJ-root/NONLINEAR_OBSERVATION_CHANNEL.md` and
`work/FJ-root/observation_channel.py`.

## Findings

The frontier product argument is correct for a branching exploration when,
conditional on the explored history and the current frontier node's type,
the freshly generated child multiset has the law used in the row inequality

\[
 z\,\mathbb E_x\prod_{c}t(\operatorname{type}(c))\le t(x),
 \qquad z>1,\quad t\ge1.
\]

Define \(W_k=z^{k\wedge N}\prod_{x\in Q_{k\wedge N}}t(x)\), and keep it
constant after the frontier empties. Conditional expectation decreases at a
processing step by the displayed inequality. On \(N>n\), \(W_n\ge z^n\), so
\(\Pr(N>n)\le t(x_0)z^{-n}\). Also \(W_k\to z^N\) on finite trees and
\(W_k\to\infty\) on infinite trees; Fatou gives \(\mathbb E z^N\le t(x_0)\)
and rules out an infinite tree. The condition must be conditional on exploration
history; a marginal row inequality alone does not cover a shared latent
environment that changes the next node's offspring law.

The root's exact two-type witness is valid and sharper than the separately
derived witness in `DELTA_AUDIT.md`. With all children type A,

\[
 G_A(s)=3/8+5s/16+5s^2/16,\qquad
 G_B(s)=1/4+3s/8+3s^2/8.
\]

At \(t_A=11/10\), these equal \(351/320\) and \(893/800\). For
\(t_B=28/25\), \(z=352/351\), the A inequality is equality:
\(zG_A(t_A)=11/10\). For B,

\[
zG_B(t_A)=314336/280800\le28/25,
\]
since \(314336\cdot25=7{,}858{,}400\le7{,}862{,}400
=280800\cdot28\). This certifies an exponential node-count tail from either
root even though type B has mean offspring \(9/8>1\). The earlier witness
\((t_A,t_B,z)=(11/10,9/8,501/500)\) remains valid.

The finite-state PDE in the first delta audit supplies the exact rejection
case for the old scalar criterion. Its mean-progeny matrix is
\(M=\left[\begin{smallmatrix}15/16&0\\9/8&0\end{smallmatrix}\right]\),
with \(M(1,6/5)^\top=(15/16)(1,6/5)^\top\). Thus the weighted
mean-progeny certificate proves contraction and finite expected work. With
\(R=1\), \(\lambda=1\), and \(B_2=1/2\), the old scalar enclosure is
impossible at every radius because
\(\sup_{a\ge0}(\lambda a-B_2a^2)=1/2<R\), and its derivative condition
also fails at the stated envelope: \(\Gamma=2>1\). The root's new \((t,z)\)
witness adds an exponential tail and deterministic truncation certificate; it
does not first establish the mean-progeny construction or a new PDE solution.

## Independent exact source and cap replay

For the incoming periodic PDE case, the source-event mass is \(80/101\),
and the degree-2, 3, 4 probabilities are \(75/404,25/1616,25/51712\).
The remaining zero-offspring mass is nonnegative. The mean offspring is
\(5425/12928<1\), and the offspring PGF (combining the source and zero marks
at degree zero) at \(s=3/2\) is \(1051417/827392\). Therefore
\(z=s/f(s)=1241088/1051417>1\), with \(\mathbb E z^N\le3/2\).

At two query points, \(h_i=1/8\), \(\sigma=1/4\), and \(R^2=1/2\).
For \(\varepsilon=1/20\), split \(\varepsilon_g=\delta=1/40\).
The exact choice \(j=15,m=60\) gives clipping bound
\(10m/2^j=75/4096\le1/40\). Exact rational powers give

\[
K=67,\quad J_{\rm cap}=22,\quad B=mKJ_{\rm cap}r=176880,
\quad n_{\rm cap}=105,
\]

where \((7/8)^K\le\delta/(3m)\),
\(2^{J_{\rm cap}}\ge24mK/\delta\), and
\(z^{n_{\rm cap}}\ge3B(3/2)/\delta\). The resulting hard PDE-node cap
is \(18{,}572{,}400\) per output. The uncapped expected vector-acquisition
bound is \(2e^2m\); using the source's uniform mean \(q=5425/12928\),
the expected PDE-node bound is
\(2e^2m\,r/(1-q)\), about \(3055.61\) nodes per output. The cap is valid
but highly conservative.

The three cap budgets are sound. The proposal failure probability is at most
\((1-e^{-2})^K\le(7/8)^K\); for \(J\sim\mathrm{Poisson}(2)\),
\(\Pr(J>J_{\rm cap})\le\mathbb E[2^J]/2^{J_{\rm cap}}
=e^2/2^{J_{\rm cap}}<8/2^{J_{\rm cap}}\); and the frontier tail is at
most \(t_{\max}z^{-n_{\rm cap}}\) per possible tree. Union bounds cost at
most \(\delta/3\) each. Coupling the capped execution to the ideal factory
until a cap is reached gives final total-variation error at most
\(\varepsilon_g+\delta=1/20\), with a fixed fallback on abort.

The expected-cost argument also survives correlation between a tree's cost
and returned value. Each acquisition request is decided before that fresh
oracle pair is generated; conditional on that past, its expected complete
cost is bounded by \(C_X\). Summing predictable request indicators gives
\(\mathbb E[\mathrm{cost}]\le C_X\mathbb E[N_{\rm acq}]\). A cap abort
mid-acquisition incurs no more than the corresponding full latent tree cost.
This requires a uniform conditional cost bound and fresh iid acquisitions.

## Scope corrections and status

The source PDE's exact rational envelope, offspring probabilities, PGF, and
caps are arithmetically checkable; the root Python run's normal, exponential,
uniform and acceptance calculations are floating point. The recorded 8,000
outputs and FFT comparison are diagnostics only. They do not validate the
continuous-target TV theorem or exact diffusion operations in finite bits.
The finite-state example in the original delta packet has exact resolvent
rows and no continuous Brownian endpoint, but still uses ideal exact random
draws. Acquisition of the full-domain envelope, all coefficient bounds, the
PGF or \((t,z)\) inequalities, tilted endpoint laws, and setup is charged.
For the continuous diffusion source, exact tilted-resolvent sampling and its
cost remain open.

No new-priority claim follows. Positive spatial supersolutions for branching
moments, multitype weighted progeny, Hamilton–Jacobi/stochastic-dominance
controls, importance-sampled branching PDEs, and the N722/FORS positive
Gaussian factory are close prior mechanisms. This composition is a checked
interface and cap theorem under supplied certificates, not a superior
solver, generic closure of N687, or physical validation.
