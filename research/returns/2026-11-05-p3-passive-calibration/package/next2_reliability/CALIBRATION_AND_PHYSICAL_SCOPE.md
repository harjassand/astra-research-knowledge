# Invariant-law uncertainty, acquisition, and physical execution

This note supplies the uncertainty and physical-access companion to PROOF.md. The earlier common-invariant operator/CDF theorem and conditional-TV implementation theorem remain accepted results of the preceding run. The changing-invariant-law result below is a new derivation, written in full. None of these statements establishes a physical model from a quiet passive trace.

## 1. A continuous-time CDF theorem when the invariant law is uncertain

Let \(L_0,L_1\) be positive definite killed conductance Laplacians on the same safe set \(A\). Thus each is symmetric, has nonpositive off-diagonal entries and nonnegative row sums. Let \(M_0,M_1\) be positive diagonal matrices of invariant masses restricted to \(A\). The killed generators are \(G_i=M_i^{-1}L_i\); put \(a_i=1^TM_i1\). The corresponding equilibrium-safe CDF is
\[
F_i(t)=\frac{H(L_i,M_i,t)}{a_i},\qquad
H(L,M,t)=1^TM(I-e^{-tM^{-1}L})1.
\]
Assume
\[
e^{-\eta}L_0\preceq L_1\preceq e^\eta L_0,\qquad
e^{-\Delta}M_0\preceq M_1\preceq e^\Delta M_0.
\]
Then, simultaneously for every \(t>0\),
\[
e^{-(\eta+2\Delta)}F_0(t)
\le F_1(t)\le
e^{\eta+2\Delta}F_0(t).                                 \tag{1}
\]
There is no inverse probability, deadline, or lifetime factor. The initial law is the equilibrium-safe law belonging to each model; this is not an arbitrary-start theorem.

### Proof of the missing mass comparison

Fix \(L\) and vary positive diagonal \(M_s\). Write
\[
G_s=M_s^{-1}L,\qquad u_r=e^{-rG_s}1.
\]
Since \(G_s\) is a killed Markov generator, \(0\le u_r(x)\le1\), and
\[
G_su_r=-\partial_r u_r\ge0
\]
coordinatewise. The last claim follows from
\(G_su_r=e^{-rG_s}G_s1\), positivity of the killed semigroup, and nonnegative killing vector \(G_s1\).

Differentiate \(H\) by Duhamel's formula and use \(M_s\)-self-adjointness. The coefficient of the diagonal derivative \(\dot M_s(x)\) is
\[
b_x(t)=1-u_t(x)
-\int_0^t u_{t-r}(x)(G_su_r)(x)\,dr.
\]
Because \(0\le u_{t-r}(x)\le1\),
\[
0\le b_x(t)\le1-u_t(x);
\]
the unweighted integral of \(G_su_r(x)\) equals \(1-u_t(x)\). Therefore \(H(L,M,t)\) is coordinatewise increasing in the diagonal masses \(M(x)\).

For a scalar \(c>0\),
\[
H(L,cM,t)=cH(L,M,t/c).
\]
The function \(t\mapsto H(L,M,t)\) is increasing and concave and vanishes at zero, by its positive spectral mixture. Consequently
\[
\min\{1,c\}H(L,M,t)
\le H(L,cM,t)
\le\max\{1,c\}H(L,M,t).
\]
Sandwich \(M_1\) between \(e^{-\Delta}M_0\) and \(e^\Delta M_0\), and use coordinatewise monotonicity. This proves
\[
e^{-\Delta}H(L,M_0,t)
\le H(L,M_1,t)
\le e^\Delta H(L,M_0,t).                               \tag{2}
\]

At fixed \(M_0\), the completed geometric-path theorem applied to
\(M_0^{-1/2}L_iM_0^{-1/2}\) gives a further factor \(e^{\pm\eta}\) for changing \(L\). The intermediate positive-operator path need not be Markov. Finally \(a_1/a_0\in[e^{-\Delta},e^\Delta]\). Combining these three comparisons proves (1).

## 2. Discrete endpoint version with changing masses

For a clocked model let \(P_i=I-M_i^{-1}L_i\) be nonnegative substochastic killed kernels, positive semidefinite in their respective mass inner products. Linear interpolation of both \(M\) and \(L\) retains these properties: \(M_s-L_s\) is a convex combination of positive semidefinite entrywise nonnegative matrices.

Let \(u_j=P_s^j1\). Differentiating unnormalized discrete heat content gives a conductance contribution and a mass contribution. The mass coefficient is
\[
b_x(n)=1-u_n(x)
-\sum_{j=0}^{n-1}u_{n-1-j}(x)\,[u_j(x)-u_{j+1}(x)].
\]
It lies in \([0,1-u_n(x)]\). If
\[
|\dot L_s|\preceq A_L(s)L_s,\qquad
|\dot M_s|\preceq A_M(s)M_s,
\]
the same discrete energy identity as in the completed common-law proof gives
\[
|\partial_s H_s(n)|\le[A_L(s)+A_M(s)]H_s(n).
\]
For symmetric endpoint log bands of radii \(\eta,\Delta\), linear interpolation has integrated relative derivative bound
\[
B(z)=2\log\frac{1+e^z}{2}
\]
for the corresponding radius \(z\). To check this, maximize
\((q-1)/(1+s(q-1))\) over \(q\in[e^{-z},e^z]\); the positive and negative magnitudes cross at \(s=1/2\), and their integrals give \(B(z)\).

After dividing by safe mass, the discrete CDFs thus obey the explicit log-radius
\[
\eta_{\rm disc}=B(\eta)+B(\Delta)+\Delta.               \tag{3}
\]
This is slightly weaker than (1). The simpler common-invariant theorem remains sharper when \(\Delta=0\): its exact log-radius is \(\eta\), rather than \(B(\eta)\).

## 3. Instantiating the bands with acquired local kinetics

Use the accepted P2 bounded-port model rather than assuming a complete transition model. Its governing source is the fixed revision cited at the end of this note. The declared blocks, fresh-memory behavior, reversibility/reciprocity, product equilibrium and operating backbone remain physical premises.

Suppose fitted local dimensionless energies have simultaneous errors
\[
|h_i-\widehat h_i|\le e_i,\qquad \Delta=\sum_i e_i.
\]
For Bernoulli Gibbs weights, both \(\log q_i\) and \(\log(1-q_i)\) are 1-Lipschitz in \(h_i\), so
\[
e^{-\Delta}\le\pi_{\rm true}(x)/\pi_{\rm fit}(x)\le e^\Delta
\]
for every full configuration, including normalization. Let refresh coefficients have log error at most \(b\).

Prepared local collision trials or native at-risk dwell experiments give absolute bands for all admitted transitions, including positive upper bands on observed-zero transitions. In the fitted invariant law, their simultaneous error satisfies
\[
|\mathcal E_{\rm aux}-\mathcal E_{\rm fit}|
\le\rho\mathcal E_{\rm backbone},
\qquad
\rho=\max_i\frac{2\sum_{\alpha\ni i}r_\alpha}{\gamma_i},
\]
\[
r_\alpha\le(2^{|S_\alpha|}-1)d_\alpha.
\]
For clarity, the auxiliary model is made reversible by an EXPLICIT conductance definition; actual reverse rates are not reused under the wrong invariant law. For each unordered local pair \(\{u,v\}\), choose \(u\) so \(\pi_{{\rm fit},S}(u)\le\pi_{{\rm fit},S}(v)\), and let \(r(u,v)\) be the true rate in that one measured direction. Define
\[
c_{\rm aux,S}(u,v)=\pi_{{\rm fit},S}(u)\,r(u,v),\qquad
c_{\rm fit,S}(u,v)=\pi_{{\rm fit},S}(u)\,\widehat r(u,v).
\]
The reverse auxiliary and fitted rates are defined by dividing these SAME symmetric conductances by \(\pi_{{\rm fit},S}(v)\); diagonals are the negative row sums. For a full configuration, multiply by the fitted outside product mass. The auxiliary backbone is EXACTLY the fitted backbone. Thus both auxiliary and fitted forms are reversible for the fitted law by construction.

If the measured directional rate error is at most \(d_\alpha\), the induced reverse error is at most \(d_\alpha\pi_{\rm fit,S}(u)/\pi_{\rm fit,S}(v)\le d_\alpha\). The local error generator therefore has maximum exit at most \((2^{|S_\alpha|}-1)d_\alpha\), yielding exactly the displayed \(\rho\), without an extra symmetrization factor. The true conductance divided by the auxiliary conductance is \(\pi_{\rm true}(u,z)/\pi_{\rm fit}(u,z)\) at the chosen full source, which lies in \(e^{\pm\Delta}\). This one-direction construction is the oriented-pair acquisition operation in the accepted P2 source.

Both auxiliary and fitted forms contain the same fitted backbone. Their mutual comparison therefore gives
\[
(1+\rho)^{-1}L_{\rm fit}
\preceq L_{\rm aux}\preceq(1+\rho)L_{\rm fit},
\]
without requiring a positive fitted value for every true transition.

The accepted product-energy and refresh envelopes compare true and auxiliary conductances by \(e^{\pm(\Delta+b)}\). Hence the total form log-radius can be taken as
\[
\eta=\Delta+b+\log(1+\rho).                            \tag{4}
\]
For a genuine continuous-time model, (1) yields the all-deadline CDF log-radius
\[
3\Delta+b+\log(1+\rho).                               \tag{5}
\]
For actual fixed-tick endpoint dynamics use (3)-(4) and the discrete computational theorem instead. The fitted endpoint kernel must also satisfy its stochastic row caps and positive-semidefinite contraction premise; these require the declared null-tick margin or explicit feasible fitting constraints. Reconstructed rates alone do not supply that condition. A collision kernel divided by its service time is not automatically a continuous-time first-failure model.

If the physical initial distribution is instead the fitted equilibrium-safe law, then
\[
e^{-2\Delta}\le\nu_{\rm fit}(x)/\nu_{\rm true}(x)\le e^{2\Delta}
\]
on \(A\). Since every failure-event probability is a positive linear functional of its initial distribution, an additional log-radius \(2\Delta\) covers that deliberate change of start. In particular the continuous log-radius becomes \(5\Delta+b+\log(1+\rho)\). This is a multiplicative density argument, not an absolute-TV error divided by a tiny probability.

## 4. What the local observations cost

For bounded-register collision ports, the accepted fixed-shot experiment prepares every local input, removes preparation fields during the actual port operation, executes one native collision, and reads its result. With absolute probability accuracy \(h\), its shot count is
\[
O(J\,2^k h^{-2}\log(J4^k/\delta_{\rm acq})).
\]
All reset, ancillary preparation, input verification, isolation, readout and service duration are paid. Attempt-weight error and systematic contamination enlarge the local bands. If each bit belongs to at most \(D\) ports and the operating refresh floor is \(\gamma_{\min}\), a sufficient common rate/probability radius is of order
\[
d=O\!\left(\frac{\rho\gamma_{\min}}{D(2^k-1)}\right)
\]
in the same clock units. This is a value dependence on the actual backbone, not a bit-length dependence.

For a declared native exponential-rate port, the accepted at-risk experiment uses fixed cumulative dwell exposure at a prepared state, counts the exits, and resets after every exit. With exit-rate upper bound \(\overline r\), absolute rate radius \(d\), and confidence logarithm \(z\), a sufficient exposure per input state is
\[
\max\{8\overline r z/d^2,\;4z/(3d)\}.
\]
Reset counts, reset work and detector limitations are additional costs. This continuous-time model is a premise of that experiment; finite-duration collisions are not silently treated as instantaneous jumps.

### Unknown equilibrium weights are not calibrated for free

If energy errors are supplied by a real independently priced energy measurement, use that measurement's noise, repetitions and systematic-error budget. There is no generic promise that every unknown energy is directly observable at constant cost.

An elementary alternative is to sample fresh native local equilibrium bits. Suppose a certified \(\beta_i>0\) satisfies \(\min(q_i,1-q_i)\ge\beta_i\), and independent samples cost \(T_i\) each including preparation/mixing. Multiplicative Bernoulli concentration gives simultaneous log-weight radius \(e_i\) using
\[
O\!\left(\frac{\log(m/\delta_{\rm weight})}{\beta_i e_i^2}\right)
\]
samples of bit \(i\). The total physical exposure is this count times \(T_i\), summed over \(i\), with sensor bias and correlations explicitly added. Without a supplied lower floor, staged confidence sequences can learn the scale, but their actual exposure still depends on the rare local probability.

Thus the result removes inverse GLOBAL first-failure probability from computation, not inverse rare local-rate or rare local-weight calibration costs. When local probabilities are bounded and global rarity comes from redundancy, the calibration costs can remain polynomial. When a single exponentially rare local mechanism dominates, passive local calibration can remain exponentially expensive.

## 5. Finite implementation and initialization

The completed conditional-TV theorem applies to an actual clocked implementation even if small factory errors break reversibility:
\[
\left|\frac{F_{\rm actual}(n)}{F_{\rm ideal}(n)}-1\right|
\le\frac{d_{\rm init}+v_{\rm step}}{g_{\rm ideal}p_{\rm ideal}},
\qquad n\ge1.
\]
The per-step bound must hold conditional on every admitted history. Marginal error rates, average equilibrium errors and silence about omitted mechanisms do not establish it.

Under the mass/form bands, a certified true gap and failure-mass floor follow from
\[
g_{\rm true}\ge e^{-(\eta+\Delta)}g_{\rm fit},
\qquad p_{\rm true}\ge e^{-\Delta}p_{L,\rm fit}.
\]
The gap inequality follows by comparing Dirichlet forms and using
\(\operatorname{Var}_{\pi_{\rm true}}f\le e^\Delta
\operatorname{Var}_{\pi_{\rm fit}}f\).

Choose per-step and initial absolute errors of order
\(\zeta g_{\rm true}p_{\rm true}\). In the accepted strong verified-factory model, conditional readout error below \(1/2\), independent repeated checks, nonbackaction, a write-success floor and protected storage can make the number of checks logarithmic in the inverse target error. Those are supplied physical capabilities, not a theorem about arbitrary sensors. Fixed caps, null outcomes and padded service time must be included in the actual endpoint kernel and clock.

The displayed implementation bound uses the true equilibrium-safe reference start. If instead the ideal prepared law is \(\nu_{\rm fit}\), with density ratio to \(\nu_{\rm true}\) bounded by \(\kappa=e^{2\Delta}\), use the conservative bound
\[
\frac{\kappa d_{\rm init}+\kappa^2v_{\rm step}}{g_{\rm true}p_{\rm true}}.
\]
Indeed the truncated lifetime under \(\nu_{\rm fit}\) is at most \(\kappa\) times its equilibrium-safe value, whereas its failure CDF is at least \(\kappa^{-1}\) times that value. The same argument applies to the continuous intensity term. The extra density comparison is not silently absorbed into a spectral-mixture identity for the wrong start.

For a genuine continuous-time implementation at the true equilibrium-safe start, a conditional discrepancy intensity \(v\) gives
\[
|F_{\rm actual}(t)-F_{\rm ideal}(t)|
\le v\int_0^tS(s)\,ds
\le \frac{v}{\gamma p}F_{\rm ideal}(t)
\]
with exact initialization. A finite unrestricted initial TV error may place an atom in \(B\); it therefore cannot give relative accuracy uniformly as \(t\downarrow0\).

For a declared minimum deadline \(t_0>0\), it suffices to choose
\[
d_{\rm init}\le
\zeta_{\rm init}\bigl(1-e^{-\gamma p t_0}\bigr),
\]
because \(F(t)\ge1-e^{-\gamma pt}\). Exact safe initialization or a multiplicative density guarantee can instead support every positive time. The distinction is part of the operational result.

For endpoint-clock predictions, the guaranteed parameter is the number of completed ticks. An uncertain physical tick duration requires an interval over the corresponding possible tick counts; near an individual tick boundary a relative wall-time guarantee need not survive. Clock counters, timestamp precision and padded execution are therefore not omitted.

## 6. A consequential family with all rarity costs visible

Take a complete \(n\)-vertex graph, constant independent edge-failure probability \(0<q\le1/4\), and bounded-degree collections of bounded-size reciprocal interaction ports. Keep an independent refresh backbone active. Product equilibrium does not require independent transition dynamics.

A particular isolated-vertex event gives \(p\ge q^{n-1}\). A union over the fewer than \(2^{n-1}\) nontrivial cuts gives
\[
p\le(2q)^{n-1},
\]
because every nontrivial cut has at least \(n-1\) edges. Thus global failure is exponentially rare in \(n\), while the local equilibrium probabilities stay bounded. A constant per-component continuous refresh rate and polynomially bounded total local attempt rate give inverse-polynomial \(g\) after computational uniformization.

In this declared class, the static oracle, local calibration, finite safe preparation and the whole-CDF computation all have polynomial resource bounds in system size and inverse accuracy; no experiment waits for an ordinary global failure. The cost polynomials can be large, and this is not a demonstrated engineering advantage. The exact small-state solvers used for diagnostics are better for those small examples.

## 7. Finite rational uncertainty factors

The uncertainty transfer need not evaluate logarithms or exponentials on unbounded-precision physical estimates. Let a rational \(C_\pi\ge1\) enclose every invariant-mass ratio and let rational \(C_\gamma\ge1\) enclose each refresh-coefficient ratio. For Bernoulli confidence bands \([q_{i,L},q_{i,U}]\) and fitted \(q_i\), such a factor is the product over \(i\) of the largest of
\[
\frac{q_{i,U}}{q_i},\quad\frac{q_i}{q_{i,L}},\quad
\frac{1-q_{i,L}}{1-q_i},\quad
\frac{1-q_i}{1-q_{i,U}}.
\]
Positive band endpoints are obtained on the stipulated local calibration event; no zero lower endpoint is treated as finite relative knowledge.

Put \(C_L=C_\pi C_\gamma(1+\rho)\). The continuous equilibrium-safe CDF factor is exactly the rational quantity
\[
C_{\rm CDF}=C_L C_\pi^2.
\]
For fitted rather than true equilibrium-safe initialization, multiply this by \(C_\pi^2\). The discrete joint-mass factor from (3) is
\[
C_{\rm CDF,disc}
=\left(\frac{1+C_L}{2}\right)^2
 \left(\frac{1+C_\pi}{2}\right)^2 C_\pi.
\]
Use the sharper common-law factor \(C_L\) when \(C_\pi=1\). A certified general gap/failure product floor is
\[
g_{\rm true}p_{\rm true}
\ge \frac{g_{\rm fit}p_{L,\rm fit}}{C_LC_\pi^2}.
\]
All interval multiplication and physical-error targets can therefore be implemented with finite rational arithmetic.

## 8. Composition into one physical confidence interval

Run the computational certificate at a smaller internal accuracy, and allocate separate failure probabilities to local-rate, equilibrium-weight, timing/backbone and computation bands. On their joint finite event, multiply the fitted interval endpoints by the proved CDF sensitivity factors, and then by the conditional-TV implementation factors. Endpoint ratios multiply; for example, a continuous equilibrium-safe form/mass log-radius \(E\) and implementation relative radius \(\zeta<1\) enlarge a computational ratio \(r\) to at most
\[
r\,e^{2E}\frac{1+\zeta}{1-\zeta}.
\]
Choose the displayed quantities so this is at most the requested \(1+\epsilon\). For example, for \(0<\epsilon\le1\), a computational ratio at most \(1+\epsilon/8\), total CDF log-radius \(E\le\epsilon/64\), and implementation radius \(\zeta\le\epsilon/64\) suffice, with ample slack. Their logarithmic total is at most
\[
\epsilon/8+\epsilon/32+\frac{2\epsilon/64}{1-1/64}
<0.19\epsilon<\epsilon\log2.
\]
The rational factors above can certify these allocations by conservative rational comparisons. The operation is a finite reviewable allocation, not an unspecified appeal to small errors.

### Governing accepted source

The acquisition/physical premises are supplied by the fixed P2 revision, not newly experimentally verified here:

https://github.com/harjassand/astra-research-knowledge/tree/324acb589443002bf8d529cc15e160129c5e36d2/research/returns/2026-11-05-p2-unknown-local-ports

The common-law sensitivity and finite conditional-TV proofs remain preserved in ../preserved_deferred_calibration/independent_routes/reliability/COMPLETED_RESULTS.txt. The old computational extension was explicitly unfinished; PROOF.md in the present directory supplies its new completed closure.
