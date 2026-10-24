# A quantum lower bound on acoustic frequency coverage

This strengthens ACOUSTIC_RANGE_THEOREM.md while preserving it unchanged. That theorem's classical fluctuation floor also holds quantum mechanically. Retaining the full quantum covariance yields a stronger bound when the range cap includes zero-point motion. The bound concerns the UPPER END of a frequency interval carried by acoustic channels; it does not create a gap at zero frequency.

## 1. Full quantum theorem

Use exactly the connected positive scalar periodic graph, counted intercell stiffness K_aff, total mass M, all-node local relative rms cap d and ideal intrinsic channel count of ACOUSTIC_RANGE_THEOREM.md. Intercell links may have arbitrary finite nonzero integer shifts and may connect different cell coordinates. Let

a=max_q sqrt(lambda_min D(q)),
Omega_aff=2sqrt(K_aff/M),
theta=k_B T/hbar.

Put

c= hbar/(864M d^2),

and let rho_T>0 be the unique solution of

rho_T tanh[rho_T/(2theta)]=c.

Then EVERY admitted quantum Gibbs network satisfies

a>=b_Q(T):=min{Omega_aff/4,rho_T},
J>=integral_0^(b_Q(T)) g_theta(omega)domega,
(J_Q-J)/J_Q<=Tail[b_Q(T)/(2theta)].

Here J_Q=pi^2theta/3 and Tail is the explicit Bose tail in ACOUSTIC_RANGE_THEOREM.md. These statements remain uniform when the finite graph, node number and spring values are changed separately at every T, as long as the displayed resources and range cap are respected.

For nearest-cell cross-node links the constants improve to

c=hbar/(384M d^2),
b_Q=min{Omega_aff/(2sqrt(2)),rho_T}.

For same-coordinate nearest-cell rails they improve further to

c=hbar/(64M d^2),
b_Q=min{Omega_aff/(2sqrt(2)),rho_T}.

The root is unambiguous because u tanh[u/(2theta)] increases strictly from0 to infinity. In particular

rho_T>=c,
rho_T>=sqrt(2theta c).

At fixed positive c, rho_T tends to c as T tends to0. Therefore a temperature-independent lower bound on acoustic COVERAGE is

a>=b_0:=min{Omega_aff/4,hbar/(864M d^2)}>0

in the general class. The nearest-cell variants use their corresponding constants.

## 2. Proof from the actual covariance

The preceding theorem constructs a positive within-cell quadratic observable F. Its modal value is at least1/12 on a set of wave numbers of normalized measure at least1/3 whenever a<=Omega_aff/4. The local range cap bounds its Gibbs expectation by

V_F<=12M d^2.

For a mass-normalized mode of frequency omega, the actual quantum position covariance coefficient is

c_T(omega)=hbar/(2omega)coth[omega/(2theta)].

It is strictly decreasing for omega>0: differentiating gives a sum of two negative terms. Every chosen lowest mode has omega_min(q)<=a, so c_T(omega_min(q))>=c_T(a). Retaining that mode on the same wave-number set gives

V_F>=c_T(a)/36
    =hbar/(72a)coth[a/(2theta)].

Thus, whenever a<=Omega_aff/4,

12M d^2>=hbar/(72a)coth[a/(2theta)],
a tanh[a/(2theta)]>=hbar/(864M d^2)=c,
a>=rho_T.

Otherwise a exceeds the first threshold already. The continuity/time-reversal channel argument supplies J>=integral_0^a g_theta, so the conductance statements follow. The nearest-cell factor1/16 and rail factor1/8 in the earlier proof give the384 and64 denominators in exactly the same way.

No state-independent relation between a static susceptibility and an arbitrarily prepared displacement is invoked. The proof uses the harmonic Gibbs mode covariance. A squeezed or driven state can have a different covariance.

## 3. Classical and quantum range must not be conflated

The elementary bound coth x>=1/x recovers the earlier thermal estimates. In the general class it gives

rho_T^2>=k_B T/(432M d^2).

That bound is sufficient for the preceding exp[-constant/sqrt(T)] tail. It is valid for the classical Gibbs state too. The additional coth x>=1 gives

rho_T>=hbar/(864M d^2),

and it is this zero-point contribution that supplies the stronger quantum low-temperature result.

If d bounds TOTAL quantum equilibrium relative rms displacement, then at fixed M,d and K_aff bounded away from zero,

(J_Q-J)/J_Q
 <=Tail[b_0/(2theta)]
 =O(T^(-2) exp[-hbar b_0/(k_B T)]).

If d instead bounds only a thermal excess after subtracting a T-dependent ground-state covariance, this last result is not asserted. The cap in the theorem is on the actual coordinate range including its zero-point motion. In a classical model hbar is not inserted as an extra physical cost; only the earlier thermal version applies.

This is protection against suppression below the acoustic quantum, not an assertion that every retuned multichannel design has J/J_Q tending to1. Soft additional channels may increase J.

## 4. Consequence and an attaining resource order

Let a family retain Omega_aff/theta tending to infinity, and suppose its ideal intrinsic conductance has a nonzero limiting fractional deficit below J_Q. The Bose-tail bound then forces rho_T/theta to remain bounded along a subsequence. Since rho_T>=c, necessarily

M T d^2 does not tend to0.

Equivalently the dimensionless localization resource

eta=hbar^2/(M d^2 k_B T)

cannot diverge while retaining a fixed fractional deficit. More explicitly, the conditional cutoff equation in dimensionless variables is

z tanh z=eta/1728, z=rho_T/(2theta).

This makes the quantum/thermal crossover of the bound explicit without a temperature sweep.

QUANTUM_COST_ATTAINABILITY.md supplies an actual positive two-mass family with M proportional to1/T, a fixed total quantum relative-rms cap and nonzero limiting deficit. Its spring, masses, full bands and actual Gibbs variance were derived. Thus the NECESSARY mass/range/temperature order is attained inside the broader graph class by a conventional one-pendant network. No optimal constants or complete bounded-range Pareto frontier are inferred.

At fixed mass the same family has quantum variance proportional to1/T, which is consistent with this theorem. Adding graph complexity or more intercell links cannot avoid the all-node range cost established above.

The effective-stiffness/range distinction remains: fixed K_eff and a uniform interaction-shift bound L0 imply K_aff>=K_eff/L0^2. One may then use Omega_aff>=2sqrt(K_eff/M)/L0. If interaction reach is unbounded, this replacement is not justified by that relation alone; the long skip-link example in the preceding theorem keeps all channel multiplicities and illustrates the limitation.

## Scope

The thermal quantum, Gibbs oscillator covariance and passive network operations are established physics. The new internal result here is a uniform quantitative resource bound across the admitted graphs and retunings. Historical priority is UNKNOWN. This is still intrinsic scalar harmonic transport with a Gibbs reference-state displacement constraint. It supplies no finite-contact device advantage, material specimen, active refrigerator or fabricated thermal barrier. All earlier proofs and corrections remain unchanged.
