# Actual uncapped seeding repair for the A-catalytic extension
Status: personal proof adaptation, not independently reviewed. Uses the local occupation and refined-reset lemmas in this directory, and the finite positive-kernel reset-walk proof in the frozen pure-source bundle only at its abstract kernel scope. No frozen theorem scope is changed.

Write h=q-m, use the exact residual r=N-H(B) from the frozen bundle, and let

    p(r)=C log(2+r)/(1+r)^(m-1), beta(r)=p(r)^(1/m),
    gamma=(m-1)/(2m), 0<alpha h<gamma,
    phi(r)=Gamma(r+1)^alpha.

Increase the killing threshold r0 whenever needed. Since N=r+H(B)>=r, local estimates give normalized fast/clearing mean <=p(r) and clearing-output inverse moment <=Cp(r), uniformly in every ACTIVE high-B input. The competitor probability for activation is o(1) uniformly: the occupation-Holder bound gives O(p(r)^((m-1)/m)) after the B factor, while immigration is O(p(r)). Thus the geometric bound on number of clearing stages still applies. Small-N inactive states are absent in r>r0.

## The extra state type cannot be omitted
For large N, inactive means exactly A=0. At any such state activation and clearing are disabled, as is all fast chemistry. The next event is one actual immigration, with mean waiting time 1/k_I. It produces A=1, N+1, B+1 and an active state. Its r-jump is either0 or+h. This is a genuine waiting interval, not an instantaneous reset.

An arbitrary inactive initial state can therefore be repaired with an initial cost and terminal weight factor at most C r^(alpha h). This factor is allowed ONCE at the initial approach, not silently attached to every downward branch.

## Clearing output kernels pay for repeated inactive seeding
At a fast-stage entrance, the clearing-before-birth subkernel K_D has mass at least1/2 and satisfies

    K_D[(1+A_after)^-m]<=Cp(r)K_D[1].

In particular its inactive-output subkernel has relative mass <=Cp(r). The statement remains valid after final-stage disintegration by pre-clearing B, since whether a clearing is low, neutral or downward is determined BEFORE observing A_after.

Treat an inactive high-B output as a bad branch of mass Cp(r), compose it with its actual seeding wait, then continue at the resulting active input. Its weighted factor is at most Cp(r)r^(alpha h)=o(1). At a low output, retain A=0 inside the actual fresh low law; its compulsory immigration is handled by the same race kernel bound C/(1+A), which is valid also at A=0. No pointwise inverse-moment assertion is made after observing A.

### Downward branches need joint treatment
A downward clearing can leave A=0 and B divisible by q-1. The next immigration then raises r by h and exactly reverses that downward jump. Therefore it is FALSE that every downward branch has weight factor O(r^-alpha h) after arbitrary repair. The valid decomposition is:

- active high-B output: O(r^-alpha h) times the uniform active repair bound;
- inactive high-B output: mass Cp(r), followed by a seed, giving O(p(r)) at the original weight;
- low output: its fresh joint law has the low-law repair bound, including its rare A=0 states, so its expected repaired weight is O(phi(r-h)).

The total downward continuation coefficient is O(r^-alpha h+p(r)), still small. This is why the actual clearing-output kernel, rather than only a mean clearing time, is indispensable.

## Positive-kernel construction
A repair round composes an active fast processor WITH any ensuing fresh low walk, stopping at the active section S={B=q,A>=1}, threshold r<=r0, or a genuine continuation branch. Neutral fast-to-low transitions lie inside a round and have coefficient1. The fresh low law has upward/bad probability O(beta(r)); a low upward wrap enters S directly. Fast bad immigration has mass O(p(r)); a high-B inactive output has mass O(p(r)) and includes one seeding interval. Downward continuations use the decomposition above.

For truncated numbers of rounds, take the supremum of normalized terminal weight and running phi-cost over active fast inputs and fresh low laws (kernel inputs before observing reset output). The continuation norm is bounded by

    C[r0^-alpha h + beta(r0)r0^(alpha h)
                         +p(r0)r0^(alpha h)+p(r0)].

Choose r0 large so this is <1/2. The within-round cost is uniformly Cphi(r): low waiting rates have a positive immigration floor, fast times are bounded by Cp(r), and a seeding wait has constant mean. Positive Neumann iteration then earns finite actual repair cost and expected terminal weight <=Cphi(r) on those input types, uniformly in all hidden populations. Arbitrary low or inactive inputs pay the single initial factor Cr^(alpha h). This is an actual stopped process; no invariant cap or prior finite repair mean is assumed.

The same construction works for Psi(r)=(1+r)^(m-1)phi(r), with its corresponding running cost. Fixed-shift polynomial factors leave every small continuation exponent unchanged.

## Coefficient-one first clearing branch
Start on the active section B=q, and let T,U be occupations up to its first connector event. Let t<=CT be the FIRST clearing-output inverse moment and let p(r) control later reset laws. The refined-first-reset lemma bounds upward/bad low escape by

    E(t,p)=Ct+C sum_(ell=1)^(m-1)t^(ell/m)p^((m+1-ell)/m).

A same-level return has weight exactly phi(r). Safe downward escape, after the JOINT repair just constructed, has expected weight <=Cphi(r-h)+Cp(r)phi(r), which is <=phi(r) for large r. All genuinely bad/up branches cost at most Cr^(alpha h)phi(r). Thus the clearing-first subkernel contributes at most

    P_D phi(r)+C E(t,p)r^(alpha h)phi(r).

The same-level coefficient is exactly P_D, not P_D times an unspecified 1+O(1/r).

Activation-first enters B=2q-1. Its first clearing with no immigration is downward regardless of intervening activations. The joint downward estimate above gives terminal weight

    O(phi(r-h)+p(r)phi(r)+p(r)phi(r+h))=o(phi(r)).

An immigration-first branch is active and costs Cphi(r), with probability k_I T. Actual activation probability is k_T q U. The relative-occupation and refined-reset lemmas give T+E(t,p)<=C e(r)U, where e(r)=Cr^-gamma log(2+r). Consequently

    E phi(r_next)<= [1-cU+C e(r)r^(alpha h)U]phi(r)
                  <= [1-c' r^{-(m-1)}]phi(r).

The last step uses the earned U>=cr^{-(m-1)}; alpha h<gamma controls the relative error. This is pointwise in the full incoming ACTIVE section state. It does not average away composition dependence.

For Psi the same argument pays cphi(r) per cycle. Actual cycle cost is <=Cphi(r), so telescoping the full-state section chain and including initial repair gives the actual threshold value

    W_r(x)=E_x int_0^{tau_{r<=r0}}phi(r(X_s))ds
       <=C(1+r)^(m-1+alpha h)phi(r),
    L W_r=-phi(r) for r>r0.

Only constant-rate immigration enters this threshold from outside, so its exterior positive drift is uniformly bounded. This conclusion is a personal derivation dependent on the explicitly stated local and positive-kernel arguments, not an independently reviewed extension. Complementary Z construction and whole-proof review remain separate obligations.
