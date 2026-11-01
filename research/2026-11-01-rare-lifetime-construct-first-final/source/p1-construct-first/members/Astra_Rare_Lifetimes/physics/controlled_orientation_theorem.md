# Controlled orientation completion: a preserved secondary result

1 November 2026 (Brisbane). This is a modest extension of the accepted passive
construction N1230, not the main proposed breakthrough. Historical priority of
the controlled extension is unestablished. It is a theorem about intrinsic
path-reversal divergence, not a low-heat realization or a bound on protocol work.

## Exact predecessor and failed ordinary inference

Predecessor pin: `harjassand/astra-research-knowledge` at
`51ce47ce39f976517d60e2f87bbe280b651f6056`.

Governing source read in full:
`research/2026-10-29-model-wise-storage-and-acquired-inference/source/p1-physical-information/research/ORIENTATION_MEMORY_AND_SUSTAINED_ENTROPY.md`
(401 lines; packet N1230 gives SHA256
`d69b64d5ed096847dfedb1f0095d5985ccc5519b11f00f887392cef26850208b`).

N1230 already proves passive finite-window approximation by a fixed-clock
4n-state lift with arbitrarily small intrinsic reversal rate. It already proves
the Dobrushin-memory rescue. Re-deriving those is not new progress. The attempted
stronger ordinary consequence was: use adaptive controlled experiments to
identify sustained irreversibility even when passive observation cannot. The
following shows why generic controls alone do not supply the missing physical
reversal/reset information.

## Statement

Let `U` be a finite action set, and let each `Q^u` be an irreducible CTMC
generator on the same n-state visible configuration space X, with stationary
law `pi^u`. The laws `pi^u` need not agree. A fixed finite readout `g:X->Y` is
observed, including exact jump times if desired. An admissible policy chooses
actions predictably from the complete observed history and independent private
randomness. Its controlled chain is well-defined; a finite family has uniformly
bounded escape rates. No action is specified to reset the complete hidden
microscopic state or implement physical reversal.

For any `delta>0`, `eta>0`, and finite horizon T, there is one common
4n-state controlled family `L^u`, one involution Theta, and one fixed escape
clock Lambda such that:

1. Every state under every action has exactly the same escape rate Lambda.
2. Each held action has its own stationary law `rho^u` and intrinsic stationary
   Theta-reversal rate below eta.
3. The readout is even: `g_tilde(Theta z)=g_tilde(z)`.
4. For every adaptive policy, started in `pi^{u0}` versus `rho^{u0}` for any
   initial reference setting u0, the complete observed/control/private-key
   transcript on [0,T] differs in TV by at most delta.

The same construction works for arbitrary initial distributions mu on X if the
lift is initialized with visible marginal mu and the same biased orientation.
Such starts need not be stationary. The held-setting rate claim remains about
`rho^u`, not about the transient or feedback-controlled experiment.

## Construction and exact entropy

Choose `0<epsilon<1/2`, `alpha=1-epsilon`, `d=1-2epsilon`, and kappa>0.
For each u let

`q^{u,*}_{xy}=pi^u_y q^u_{yx}/pi^u_x`.

Use states `(x,s,h)` with `s in {+,-}`, `h in {0,1}`. At s=+ use Q^u on x;
at s=- use Q^{u,*}. Preserve h during visible moves. Flip + to - at rate
`a=kappa epsilon` and - to + at `b=kappa alpha`. Put

`Lambda=max_{u,x}(-q^u_xx)+c0`, `c^u_x=Lambda+q^u_xx`,

for any fixed c0>0 and choose kappa<c0. Toggle h at rates `c^u_x-a` in + and
`c^u_x-b` in -. Thus every total escape rate is Lambda, independent of state,
action, epsilon and kappa.

The stationary law for held u is

`rho^u(x,+,h)=alpha pi^u_x/2`,
`rho^u(x,-,h)=epsilon pi^u_x/2`.

Stationarity follows separately for each orientation's Q/Q* flow, from
`alpha*a=epsilon*b`, and from the symmetric bit toggle. The same involution
`Theta(x,s,h)=(x,-s,h)` works for every action. Set readout g_tilde=g(x).

For a finite generator L and a physical involution Theta, define the intrinsic
rate at its stationary law rho by

`sigma_Theta(L)=sum_z rho_z [sum_{w!=z} l_zw log(l_zw/l_{Theta w,Theta z})
                                     +lambda_{Theta z}-lambda_z]`.

As in the exact N1230 argument, internal Q/Q* logarithms are stationary
gradients and average to zero; the orientation edges are self-reversed; the
common escape rates cancel. Only h toggles remain. Consequently, for every u,

`sigma_u=sum_x pi^u_x d c^u_x log[(c^u_x-kappa epsilon)/(c^u_x-kappa alpha)]`

and

`0<=sigma_u<= kappa d^2/(1-kappa/c0)`.

This bound is uniform in u and in the stationary laws. Preparation divergence
for every held u is still `B=d log(alpha/epsilon)`. The orientation relaxation
rate is kappa. Neither its long relaxation time nor small stationary orientation
population is controlled by Lambda or n.

## Uniform adaptive coupling

Couple target and lifted initial x, and share all private policy randomness.
With probability alpha the lift starts in +. Until the first + to - switch,
all visible transitions have generator Q^{u(t)} and are coupled identically.
Both policies therefore see the same entire record and choose the same next
action. Hidden h toggles are unobserved and do not affect any x or s rate.
The orientation switch intensity a is independent of x, action, h and history.

The probability of coupling failure by T is exactly bounded by

`epsilon+alpha(1-exp(-kappa epsilon T)) <= epsilon+kappa epsilon T`.

It bounds TV of the COMPLETE continuous-time transcript, including controls,
stop decisions, and private random bits, not only a finite set of observables.
Choose epsilon<delta/2 and kappa small enough that
`kappa<c0/2`, `kappa T<=1`, and `2kappa<eta`.

For a target stopping time tau with finite expectation, the same coupling
gives `TV<=epsilon+alpha E[1-exp(-kappa epsilon tau)]
<=epsilon+kappa epsilon E[tau]`. A nonterminating alternative execution can be
recorded as a cemetery outcome. For at most M independently initialized
episodes of total duration T, union coupling costs at most
`M epsilon+kappa epsilon T`. Thus finite adaptive expected budgets cannot
uniformly resolve the hidden orientation.

## What reset operations do and do not change

A specified operation on the VISIBLE x configuration alone can be lifted as
the same operation on x while retaining s and h. Its record and visible effect
are still coupled before the first orientation mismatch. This includes a
visible reset x<-x0. Its thermodynamic cost is not included in sigma_u.

A certified reset of the COMPLETE microscopic state into one even singleton,
a calibrated physical Theta operation, parity-invariant stationary
preparation, or a quantitative hidden mixing bound excludes the completion.
The theorem does not cover those stronger services. Returning to a visible
symbol does not certify such a reset.

## Inferential corollary and limit

Any lower-confidence estimator for a held-setting intrinsic rate that is
uniformly valid over this unrestricted hidden-parity completion class cannot
return a strictly positive bound with power appreciably exceeding its false
positive level from a finite adaptive transcript. For each positive proposed
lower bound, choose eta below it and delta arbitrarily small. The lifted
experiment gives the same data law to within delta while all its held-setting
rates are below eta.

This does not say controls never reveal dissipation. Thermodynamic restrictions
on how actions transform energies, reservoirs and odd external fields may rule
out L^u. It does not bound the entropy of the complete feedback controller or
the work needed to switch actions, prepare rho^u, implement visible resets, or
realize an arbitrary source family physically. No such realization is supplied.

## Finite execution

`active_orientation_check.py` checks two nonidentical three-state generators
with distinct stationary laws, their common 12-state lift, stationarity, exact
clock equality, the entropy formula, and 19,683 adaptive grid transcripts.
At epsilon=1e-4 and kappa=1e-6, the target all-even rates are about 0.693147
and 0.696969. Lifted intrinsic rates are about 9.996004e-7. The adaptive
transcript TV is 1.705769e-5, below the complete continuous-time bound
1.000004e-4. These are ordinary floating calculations, not rigorous enclosures;
the analytic identities supply the theorem.

## Comparison and credit

The construction adopts N1230's exact orientation/clock completion, and that
Astra ingredient must be credited. Its adjoint lifting, slow switching and
parity-boundary ingredients have established antecedents: Kim, Lee and Jeong,
Phys. Rev. Research 4, 023051 (2022), arXiv:2112.04681; Andrieu and Livingstone,
Annals of Statistics 49 (2021), DOI 10.1214/20-AOS2008; Degunther, van der Meer
and Seifert, Phys. Rev. Research 6, 023175 (2024).

The controlled contribution here is one shared lift for all settings (including
different stationary laws), uniform adaptive-transcript coupling, and its
finite-budget inference corollary. A bounded search did not establish priority.
This is a useful obstruction, not a civilization-changing positive capability.
