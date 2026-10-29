# Event-updated memory programs a balanced transport current

30 October 2026. Root construction. Finite-system theorem; no hydrodynamic,
mixing, apparatus-feasibility or priority claim is imported into it.

## 1. Actual network and operation

Assume all stated processes are nonexplosive. Let G be a finite graph on n sites, with an orientation of each selected edge
e=(x,y), positive selected conductances c_e, and occupancies eta_x in {0,1}
at a fixed particle number M. Put delta_e=eta_x-eta_y, a_e=delta_e^2.
The selected directed conductances are balanced at each vertex:

    sum_(e leaves x) c_e = sum_(e enters x) c_e.                 (1)

Consequently, for every occupancy configuration,

    sum_selected c_e delta_e = 0.                             (2)

Introduce one physical bit u in {-1,+1}. A selected active transition swaps
eta_x,eta_y AND flips u, with actual rate

    r_e(eta,u)=c_e(1+alpha u delta_e),  0<=alpha<=1.            (3)

Inactive edges do not generate events. Native event counting never includes
null swap attempts. Each transition records the current increment delta_e.
Other transitions leave u unchanged. They may contain arbitrary hidden
kinetics, position dependence and memory, provided their actual stationary law
is a warranted common law nu on the visible/hidden state and they are reversible
with respect to that law separately for every fixed u. For the explicit formulas
below nu has uniform canonical occupancy marginal. The simplest instance has
no other transitions and nu is uniform over occupancies with M particles.

For a nontrivial hidden state z, selected swaps must preserve the common law:
nu(eta,z)=nu(eta^e,z), and (3) must be the actual selected rate, independent of z.
A frozen arbitrary z with conditional uniform canonical eta is included. A
hidden variable that changes selected rates is NOT covered merely by calling it
unobserved. One can add a separately justified averaging supplier, but that is
not a premise silently granted by this theorem.

The joint equilibrium law is mu=nu times a fair bit. Equation (3) obeys detailed
balance because simultaneous reversal sends (u,delta_e) to (-u,-delta_e), leaving
u delta_e and c_e unchanged. The other transitions preserve mu by hypothesis.
Irreducibility is unnecessary. The bit may be retained and read; the theorem
does not require hiding it from an observer.

The physical supplier in (3) is an event-coupled selective gate. It requires
neither evaluation of a global configuration parity nor an external clock that
flips the bit between events. It DOES require atomic transition/bit updating
and coupling of every selected port to that same bit. A delayed measurement and
broadcast implementation is a different process until its error is controlled.

## 2. Exact corrected-current theorem

Let J_t be the sum of delta_e over selected events. Define

    A_c(eta)=sum_selected c_e a_e,
    d_e=delta_e-alpha u  on selected active transitions,
    M_t=sum_selected_events d_e.                              (4)

Using (2) and delta_e^2=1 on active events,

    sum_selected r_e d_e
      =(1-alpha^2) sum_selected c_e delta_e = 0,
    sum_selected r_e d_e^2=(1-alpha^2) A_c.                    (5)

Hence M is an exact square-integrable martingale and

    <M>_t=(1-alpha^2) int_0^t A_c(eta_v) dv.                  (6)

Every selected transition changes u by -2u, and no other transition changes it.
This gives the pathwise identity

    J_t=M_t+(alpha/2)(u_0-u_t).                              (7)

No cancellation of independent hypothetical futures, no microscopic copy and
no unrecorded random selector occurs. The correction is an actual endpoint of
the same internal degree of freedom.

At alpha=1, every positive-rate event has delta_e=u, so d_e=0. Thus

    J_t=(u_0-u_t)/2,  |J_t|<=1                              (8)

on every path, under every initial law and at every time. This exact constraint
survives arbitrary changes of positive rates that retain the allowed event
set and the atomic bit update. Such changes need not preserve equilibrium,
mixing or a specified density evolution. Those are distinct properties.

## 3. Equilibrium variance without a mixing assumption

Start at the actual law mu. Stationarity gives

    E M_t^2=(1-alpha^2) E_mu[A_c] t.                        (9)

The endpoint in (7) is bounded by alpha. Cauchy--Schwarz therefore proves

    lim_(t->infinity) Var_mu(J_t)/t
       =(1-alpha^2) E_mu[A_c].                             (10)

There is no requirement that hidden memory mix, nor a spectral gap requirement
for (10). This is an asymptotic second-moment statement, not an automatic CLT.
A martingale CLT additionally needs stabilization of its activity bracket.

At uniform canonical occupancy,

    E_mu[A_c]=[2 M(n-M)/(n(n-1))] sum_selected c_e.          (11)

Thus all unknown reversible kinetics on unselected channels can change
correlations and relaxation while leaving (10)--(11) unchanged. The known
selected conductances and their balance are essential information.

The actual number of bit updates is the selected jump count. Its stationary
mean rate is E_mu[A_c]. Memory capacity is one bit, while its operation count
grows linearly in physical time and in the number of active selected ports.
No work, energy, sensing latency or communication cost is inferred from a bit
count alone.

## 4. A supplied circulating force and exact stationary response

For a physical load h, suppose the same selected operation additionally has
the actual rates

    r_e^h=c_e(1+alpha u delta_e) exp(h delta_e).              (12)

The log ratio of reverse selected rates is 2h delta_e; h is half the dimensionless
edge affinity. Unselected transitions remain unchanged and reversible at each u.
Supplying (12) is an additional force interface, not an acquisition theorem.

Define

    w_h(u)=1-alpha u tanh h,
    mu_h(deta,dz,u)=nu(deta,dz) w_h(u)/2.                  (13)

For finite h this law is positive, normalized, and has exactly the same
visible/hidden marginal nu. To verify invariance, sum incoming and outgoing
selected rates at each state. Balance (2) gives outgoing coefficient

    A_c [cosh h+alpha u sinh h] w_h(u),

and incoming coefficient

    A_c [cosh h-alpha u sinh h] w_h(-u).

They agree exactly. Each unselected reversible channel separately preserves
(13). No detailed balance under the load, no mixing, and no uniqueness of (13)
are assumed.

The instantaneous selected current drift is

    A_c [sinh h+alpha u cosh h].                            (14)

Under the actually initialized law mu_h, u is independent of eta,z and has
mean -alpha tanh h. Thus the exact stationary mean current is

    E_(mu_h) J_t/t=E_mu[A_c](1-alpha^2) sinh h.              (15)

This equality holds for every positive t. The derivative at h=0 is exactly the
equilibrium variance coefficient (10). With the full affinity 2h the corresponding
factor is one half. Noise suppression is not obtained at unchanged response to
this force. The controller's changed constitutive law respects the equilibrium
fluctuation-response relation.

The state law (13) is an initialization premise for the stated exact stationary
formula. In a reducible model, merely waiting need not select it from an
arbitrary recorded start. For weak fields h=E/N the total variation distance
between mu_h and mu_0 is alpha |tanh(E/N)|/2, but this o(1) comparison does not
transfer exponentially rare probability laws at speed N.

## 5. Exact two-state spectral cell for the current

Let k be a current-counting parameter, and let L_(h,k) be the tilted generator:
multiply selected off-diagonal terms by exp(k delta_e), retaining the actual
escape rates from (12). On positive functions v depending only on u,

    L_(h,k) v(eta,u)=A_c(eta) [B_(h,k) v](u),              (16)

where

    [B v](u)=[cosh(h+k)+alpha u sinh(h+k)]v(-u)
              -[cosh h+alpha u sinh h]v(u).               (17)

Its Perron eigenvalue is

    b_alpha(h,k)=-cosh h
       +sqrt[alpha^2 cosh^2 h+(1-alpha^2)cosh^2(h+k)].     (18)

The associated positive vector v exists for all finite h,k and 0<=alpha<=1.
At alpha=1 the eigenvalue is zero. For any such eigenvector,

    exp[k J_t-int_0^t b_alpha(h,k) A_c(eta_v)dv]
           v(u_t)/v(u_0)                                 (19)

is an exact mean-one exponential martingale from every initial state. This
follows from the jump compensator and (16), not from treating A_c as a constant.
The other channels act trivially on v(u). Bounded selected rates on a finite
network ensure the needed exponential integrability.

The cell obeys b_alpha(h,k)=b_alpha(h,-2h-k), and

    b_alpha(h,k)=(1-alpha^2)(h k+k^2/2)
                       +O((|h|+|k|)^4)                  (20)

near zero. Equation (19) is a joint current/activity identity. It is NOT an
exact scalar-current SCGF unless the random activity has been controlled at
the relevant exponential scale. Negative b can favor low-activity trajectories;
equilibrium activity concentration alone does not settle that large-deviation
problem. This matters for weakly driven current tails and possible dynamical
transitions.

## 6. Several programmed flows

The construction extends to a finite set of labeled transition channels a.
Each channel has its own balanced oriented conductances c_e^a, bit u_a and
coupling alpha_a. A channel-a event swaps its endpoints and flips only u_a,
at rate c_e^a(1+alpha_a u_a delta_e^a). Channels may use the same physical edge,
but their event identities and separate bit updates must actually be supplied.
Other channels preserve the reference law separately at fixed bit vector.

Under nu times fair independent bits, each corrected current M_a is a martingale
with bracket (1-alpha_a^2) int A_a. Distinct channels do not jump simultaneously,
so <M_a,M_b>=0 for a!=b. Their bounded endpoint corrections imply

    lim_(t->infinity) t^-1 Cov(J_a(t),J_b(t))
      =1_(a=b)(1-alpha_a^2) E_nu[A_a].                    (21)

Independent force parameters h_a give stationary law
nu product_a [1-alpha_a u_a tanh h_a]/2 and exactly diagonal stationary response
E A_a (1-alpha_a^2)sinh h_a. A linear combination of recorded channel currents
has the covariance obtained by ordinary matrix congruence. That last step is
a readout transformation, not a physical cross-coupling operation.

## 7. What is and is not enabled

This construction supplies exact, selectable current suppression on balanced
flow channels using bounded internal memory. It avoids identifying arbitrary
unselected reversible kinetics. It does not grant unknown selected rates,
selection of an unobserved native channel, global communication, instantaneous
actuation, a stationary preparation, or physical load access.

On the even-length periodic exclusion ring, (3) is exactly the earlier parity model in
coordinates u=sigma p(eta), with zero external sign-clock rate. The event-memory
architecture makes explicit a different supplier and removes an externally
running clock premise. Full spatial transport action and unchanged macroscopic
density relaxation require the separate receiving construction. This finite
network theorem alone is not a declaration of either property.

Antithetic sampling, finite internal-state transport, lifted chains,
cycle-current gauge methods and local/long-range dipole-conserving pairs are
close mechanisms. Generic memory, negative temporal correlation and current
correction are not claimed as inventions. The exact balanced-flow interface,
its conditional kinetics scope and emergent-law consequence require comparison
at their actual premises; historical priority remains open.
