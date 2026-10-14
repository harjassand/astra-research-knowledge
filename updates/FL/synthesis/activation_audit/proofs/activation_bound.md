# Independent derivation: regenerative molecular activation ledger

## 1. Contract and notation

This proof treats one **addressed, successfully prepared** molecule per attempt. It is a conditional cycle model, not a molecular-dynamics model.

- $E>0$: recoverable excitation energy present immediately after preparation, in J/molecule or eV/molecule.
- $\eta\in(0,1]$: source-work-to-that-excitation efficiency at a declared input boundary. Input work per prepared molecule is $E/\eta$. This is an energy efficiency, not the fraction of a bulk gas population in a high-$J$ state.
- $\lambda_r>0$: constant desired-product hazard, in s$^{-1}$.
- $\lambda_\ell\ge0$: constant nonproductive, activation-destroying hazard, in s$^{-1}$.
- $K=\lambda_r+\lambda_\ell$, $a=\lambda_r/K$, with $a=1$ if $\lambda_\ell=0$.
- $t\ge0$: reaction window before the unload step, in s; the work/product ratio below is defined for $t>0$.
- $s=e^{-Kt}$: probability the excitation remains addressable at the end of that window.
- $p$: probability of desired product in that window.
- $r\in[0,1]$: fraction of the excitation on a molecule still addressable at time $t$ that is converted into usable work by the subsequent unload operation.
- $h\ge0$: additional unrecovered control work per addressed attempt, at the same work boundary as $E/\eta$.

The model makes four restrictions that are essential to the result: product and loss are mutually exclusive terminal outcomes during the hold; a loss destroys all still-recoverable excitation; no work is recovered from either terminal branch; and unloading acts only on the survivors after the reaction window. A product event yields one counted product. Loading, $r$, $h$, and both hazards are fixed across attempts. These assumptions are not asserted to describe the real CO\(_2\) experiment.

## 2. Constant-hazard probabilities

Until the first terminal event, survival to time \(u\) is \(e^{-Ku}\). Therefore

\[
 p=\Pr(\text{product by }t)
 =\int_0^t\lambda_r e^{-Ku}\,du
 =\frac{\lambda_r}{K}(1-e^{-Kt})=a(1-s).
\]

Similarly, \(\Pr(\text{loss by }t)=(1-a)(1-s)\), and \(\Pr(\text{still addressable at }t)=s\). The three probabilities sum to one.

Expected supplied work per attempt is \(E/\eta+h\). Expected returned work is \(rEs\): only the survivor fraction \(s\) still carries excitation, and the unload extracts fraction \(r\) of that amount. Thus the ensemble work divided by counted products is

\[
 w(t)=\frac{E/\eta-rEs+h}{a(1-s)}.
\]

The ratio is exact for a large independent batch in the linear expected-work/product account, and also for repeated identical renewal attempts when every nonproductive attempt resets to the same input state and returned work is credited once. Without such a reset/accounting contract it is not an assertion about a particular evolving reactor.

Since \(r\le1\), \(\eta\le1\), and \(h\ge0\),

\[
 E/\eta-rEs+h
 = (E/\eta)(1-s)+Es(1/\eta-r)+h
 \ge (E/\eta)(1-s).
\]

Dividing by \(p=a(1-s)\) gives

\[
 \boxed{w(t)\ge\frac{E}{\eta a}
 =\frac{E}{\eta}\left(1+\frac{\lambda_\ell}{\lambda_r}\right).}
\]

For \(\eta=1\), the exact excess is visible in the decomposition

\[
 w(t)=\frac{E}{a}\left(1+\frac{(1-r)s}{1-s}\right)
       +\frac{h}{a(1-s)}.
\]

This shows the tradeoff precisely: recovery lowers work only on molecules that remain addressable; it cannot refund a loss branch under the model. If \(r=1\), \(h=0\), and \(\eta=1\), the bound is attained at every finite \(t>0\). If recovery is imperfect or \(h>0\), the work/product ratio decreases as \(t\) grows. Indeed, with \(C=E/\eta+h\),

\[
 \frac{dw}{ds}=\frac{C-rE}{a(1-s)^2}\ge0,
 \qquad \frac{ds}{dt}=-Ks<0.
\]

Under this model the energy-only optimum is therefore the limiting hold \(t\to\infty\), not a finite unload time. It gives \(p\to a\), returns no work from the vanishing survivor fraction, and reaches \(w\to E/(\eta a)+h/a\). A finite hold can be optimal for throughput, finite residence-time, selectivity, or equipment objectives, but those objectives add constraints/costs. For example, with cycle time \(t+t_d\), constant rates, and no other timing constraints, maximizing product rate means maximizing \((1-e^{-Kt})/(t+t_d)\), whose positive stationary point satisfies \(e^{Kt}=1+K(t+t_d)\) when \(t_d>0\). That is a different objective from minimizing energy per product.

In the loss-free, zero-overhead special case $a=1,h=0$, the expression simplifies to $w/E=r+(1-r)/p$. Thus at $p=10^{-6}$ and $r=0.99$, $w/E=10000.99$ (approximately $10^4$). This is the recovery/survival tradeoff: the unrecovered fraction is paid once for each rare productive event, not just once per prepared molecule.

If both competing hazards are binary-collision rates with the same density factor, $\lambda_r=nk_r$ and $\lambda_\ell=nk_\ell$, then $a=k_r/(k_r+k_\ell)$ is independent of $n$. Increasing density can raise throughput, but does not improve this idealized energy/product floor. A density-dependent state distribution, three-body channel, or changed reaction pathway violates that factorization and requires new rates.

## 3. Loading efficiency and addressed population

If \(E\) is molecular excitation and \(\eta\) is the fraction of supplied work that reaches it, then the floor is \(E/(\eta a)\), not \(E/a\). Charging a real laser, optical train, or wall-plug interface may make \(\eta\) much smaller; the input boundary must be stated to avoid charging those losses twice.

Let \(f_{\rm addr}\) be the fraction of feed molecules actually addressed in a target state. If only addressed molecules can make the counted product, the ideal batch has product yield per feed molecule \(f_{\rm addr}p\) and activation input per feed molecule \(f_{\rm addr}E/\eta\). Their ratio cancels \(f_{\rm addr}\) only if unaddressed material incurs no additional work and contributes no counted products. A fixed beam/handling cost per bulk feed instead contributes in proportion to \(1/(f_{\rm addr}p)\). The fraction of the ensemble occupying a state is therefore a throughput/yield parameter, not a license to call the state energy an ensemble mean.

## 4. General renewal accounting with partial losses and product recovery

The rate-ratio expression is not a universal law for chemical activation. For an i.i.d. renewal attempt, let \(q\in(0,1]\) be the probability of a desired product, \(c_r\) the conditional expected **net** work cost given a productive outcome, and \(c_\ell\) the conditional expected net work cost given a nonproductive outcome. These costs are computed after crediting every physically returned work packet exactly once and include the common preparation/control charges allocated to that outcome. If each nonproductive outcome resets the same renewal state, then the expected number of failures before one product is

\[
\mathbb E N_\ell=\sum_{k\ge1}\Pr(N_\ell\ge k)
 =\sum_{k\ge1}(1-q)^k=\frac{1-q}{q}.
\]

Consequently

\[
 \boxed{\mathbb E[W\mid\text{one product}]
       =c_r+\frac{1-q}{q}c_\ell.}
\]

If the only two terminal hazards are constant, \((1-q)/q=\lambda_\ell/\lambda_r\). This identity also permits partial loss and post-reaction product-state recovery: those change \(c_\ell\), \(c_r\), or both. It is ordinary renewal accounting, not a new physical principle.

Exact countermodels with \(E=1\), \(q=1/10\), and unit preparation charge per attempt illustrate why the loss/recovery assumptions matter:

1. Full activation loss on failures and no product recovery: \(c_r=c_\ell=1\), so \(w=10\).
2. A failure returns \(9/10\) of the activation but a product returns none: \(c_r=1,c_\ell=1/10\), so \(w=1+9/10=19/10\).
3. Both the failure and product branches return \(9/10\) as usable work: \(c_r=c_\ell=1/10\), so \(w=1\).

These are algebraic witnesses showing that the \(E/a\) floor depends on assuming every failed or product channel yields zero recoverable work. They do **not** establish a chemistry, that returned energy can be stored/reused at the declared boundary, or that changing product recovery leaves branching probabilities and throughput unchanged. If later chemistry can reverse a product or revoke its value, the state/reward horizon must be enlarged as in the N783 capital contract.

## 5. Adaptive hazard policies: a valid extension and a failure of averaging

Let the preterminal molecular state be controlled by any predictable policy using its full observed history. Suppose the process is nonexplosive, has exactly one terminal event (desired product or nonproductive loss) almost surely, and the cause-specific hazards under every legal action/state/history satisfy the **uniform pathwise** inequality

\[
 \lambda_\ell(t\mid\mathcal H_t)\ge\kappa\lambda_r(t\mid\mathcal H_t)
 \quad\text{for one acquired }\kappa\ge0.
\]

The counting-process compensator identity gives

\[
 \Pr(\text{loss})-\kappa\Pr(\text{product})
 =\mathbb E\int_0^\tau(\lambda_\ell-\kappa\lambda_r)\,dt\ge0.
\]

Because the terminal probabilities sum to one, \(q=\Pr(\text{product})\le1/(1+\kappa)\). For repeated renewal attempts with uniform nonnegative net cost floors \(c_r\ge\epsilon_r\ge0\) and \(c_\ell\ge\epsilon_\ell\ge0\), this yields

\[
 \mathbb E[W\text{ per product}]\ge\epsilon_r+\kappa\epsilon_\ell.
\]

This is a conditional extension of the same compensator/renewal ideas used in controlled Markov analyses; it establishes no physical actuator. If no positive uniform \(\kappa\) is known, or if a policy can change the reaction/loss ratio, there is no policy-independent floor of this form. A control that only multiplies **both** hazards by the same positive clock factor preserves their ratio and eventual branching probability; it changes time, not endpoint selection. N777's acquired-committor theorem is more general for finite-state networks, requiring \(L^u q=0\) for every legal generator and almost-sure absorption. N777's finite-horizon caveat also matters: censoring changes observed conditional yields even when eventual committors agree.

Do not replace a heterogeneous or adaptively controlled population by the ratio of unweighted mean rates. A finite exact mixture countermodel is:

- type A, weight \(1/10\): \((\lambda_r,\lambda_\ell)=(100,0)\), hence \(q_A=1\);
- type B, weight \(9/10\): \((\lambda_r,\lambda_\ell)=(1,9)\), hence \(q_B=1/10\).

The true mixture yield is \(q=(1/10)(1)+(9/10)(1/10)=19/100\), so unit-cost renewal work is \(100/19\). The unweighted mean hazards are \((109/10,81/10)\), whose fictitious single-hazard yield is \(109/190\) and work/product is \(190/109\), a severe underestimate. The mixture has no single constant cause-specific hazard pair; its surviving risk set changes type composition over time. State- or history-conditioned hazard accounting is required.

For action control, a separate exact finite example has action A rates \((\lambda_r,\lambda_\ell)=(1,9)\), and action B rates \((9,1)\), with unit load and full failure loss. A gives \(q=1/10,w=10\); B gives \(q=9/10,w=10/9\). The fixed-action constant-hazard theorem is correct for each action, but an average over available legal actions is not the guarantee for the policy that selects B. Any proposed adaptive advantage must include the acquired action-conditioned rates, their work costs, information available to the controller, and the strongest equally informed comparator.

## 6. Unloading under a torque bound and competing loss

Use the explicitly ideal planar rigid-rotor Hamiltonian

\[
 H=\frac{L^2}{2I}-U_0(t)\cos^2(\theta-\phi(t)),
 \qquad 0\le U_0(t)\le U_{\max}.
\]

Hamilton's equation gives \(|\dot L|=|U_0\sin 2(\theta-\phi)|\le U_{\max}\). Therefore reducing initial momentum \(L_0>0\) to zero takes at least

\[
 t_d\ge L_0/U_{\max},\qquad L_0=\sqrt{2IE_0}.
\]

Now assume an independent catastrophic loss event has constant hazard \(\lambda_\ell\) during unloading, and each infinitesimal amount of rotor energy extracted before that event is retained as work. Under a monotone trajectory (L(t)\), the work removed is \(-dE\) with \(E=L^2/(2I)\); the expected retained work is

\[
 \int_0^{t_d} e^{-\lambda_\ell t}(-\dot E(t))dt.
\]

For a given decrement $dL<0$, $-dE=(L/I)(-dL)$ is fixed. The torque bound implies the earliest feasible time at fractional momentum reduction ($u=1-L/L_0$) is $t(u)=uL_0/U_{\max}$. Since survival $e^{-\lambda_\ell t}$ decreases with time, all decrements should be made as early as possible: maximum deceleration from the start is the energy-recovery optimum under this model. Deliberately slowing or waiting only discounts each still-unextracted increment. A control waveform, capture constraint, thermal damage cost, or reactivity during unload can alter this optimization and is outside the model.

With maximum constant deceleration, \(t_d=L_0/U_{\max}\), \(L(t)=L_0(1-t/t_d)\), and \(E(t)=E_0(1-t/t_d)^2\). For \(z=\lambda_\ell t_d\),

\[
 r_{\max}(z)=\frac{\mathbb E W_{\rm return}}{E_0}
 =2\int_0^1(1-u)e^{-zu}du
 =\begin{cases}\frac{2(z-1+e^{-z})}{z^2},&z>0,\\1,&z=0.\end{cases}
\]

The integral is the key accounting step: it gives credit for work extracted **before** a later loss. Equating recovery to whole-pulse survival $e^{-z}$ would undercount. The small-$z$ expansion is \(1-z/3+z^2/12-z^3/60+O(z^4)\). Moreover \(r'_{\max}(z)=-2\int_0^1u(1-u)e^{-zu}du<0\). Numerically, 99% recovery requires \(z\le0.03022704459947\), or, with the torque floor, \(\lambda_\ell L_0/U_{\max}\le0.03022704459947\). Here \(U_{\max}\) is an energy/torque in J, \(L_0\) is angular momentum in J·s, and the quotient is seconds.

This ideal-model \(r_{\max}\) can be inserted for $r$ in the work/product equation only if reaction is closed during unloading and the only unloading hazard is the specified loss. If product formation continues while unloading, use both cause-specific hazards and an outcome-dependent energy ledger over that interval; multiplying by the hold-phase \(a\) without changing the contract is invalid. Loss of coherence also need not equal loss of extractable population energy.

## 7. CO-unit conversion and comparison boundary

With \(M_{\rm CO}=28.010\) g/mol as a nominal molar mass,

\[
1\;\mathrm{eV/molecule}
 =\frac{(1.602176634\times10^{-19}\,\mathrm{J/eV})
 (6.02214076\times10^{23}\,\mathrm{molecule/mol})}
 {(3.6\times10^6\,\mathrm{J/kWh})(0.028010\,\mathrm{kg/mol})}
 =0.9568540\;\mathrm{kWh/kg\ CO}.
\]

Thus the conditional one-product-per-6.14-eV-addressed-molecule floor is \(6.14\times0.9568540=5.87508\) kWh/kg CO. This uses the high-energy tail state as the energy **per addressed product attempt**; it does not infer the ensemble-average rotational energy or the mean cost over all inlet CO\(_2\). It assumes one CO per productive attempt and gives no credit for product-state work recovery, useful cascades, or thermal/chemical work returned across the selected boundary.

Primary process comparisons have different evidence and boundaries:

1. The 2023 ISPT upscaling report specifies an Air Liquide model case for CO \(\ge96\) mol% at 13 barg, with the SOEC at 750 °C, 50% single-pass conversion, and an assumed process design. Its Table 6 reports 3.2 kWh/kg CO from 2.7 stack DC + 0.2 feed heat + 0.1 air heat + 0.2 compression. Table 12 adds 0.1 kWh/kg for an explicit 97%-efficient AC/DC conversion and reports 3.3 total. The study's 3.2 is a modeled use-case electricity figure, not an independently demonstrated full operating plant; excess-heat/integration and upstream CO\(_2\) feed preparation remain boundary conditions. The 5.875 ideal molecular floor is 1.836 times 3.2 (or 1.780 times 3.3), before activation/control losses.
2. A 2022 Topsoe presentation reports a long-duration dry-CO\(_2\) electrolysis **stack** result: 14,000 h, 30,000 Nm³ (35.5 t) CO, 3.44 kWh/Nm³, and Faradaic efficiency \(99\pm1\)% (vendor-reported). It is not a full-plant energy result.
3. Topsoe's eCOs plant FAQ separately states 6–8 kWh/Nm³ for total plant consumption and about 3–3.5 kWh/Nm³ for the stack, with standard 99 vol% product purity. These are vendor ranges, not the measured stack trial's system boundary. A mass conversion depends on the document's normal-volume convention. Using the 35.5 t / 30,000 Nm³ conversion printed in the vendor presentation gives 1.1833 kg/Nm³ and an illustrative full-plant range of 5.07–6.76 kWh/kg. Using the common 0 °C, 1 atm ideal-gas convention instead gives about 1.249 kg/Nm³ and 4.80–6.41 kWh/kg. Under either explicit conversion the 5.875 kWh/kg activation floor falls **inside** the vendor's broad plant range. It is not rigorously above every complete-plant benchmark.

The most defensible conclusion is narrower: this high-J one-CO cycle is worse than the matched-condition ISPT modeled electricity case even at its ideal activation floor, and it has no demonstrated route to the missing energy margin. The numerical comparison does not prove that every regenerative activation chemistry loses to every full-plant CO process; the modelled ISPT case and vendor full-plant range differ in boundary, pressure/purity, integration, and evidence tier. Neither comparison establishes actual chemical conversion by the optical-centrifuge route.
