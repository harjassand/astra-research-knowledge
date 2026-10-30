# Exact two-weight repair for the CP-dressed basin comparison

2026-10-30. Independent addition to the scoped geometric-blocker audit. This fills a missing comparison, not the original compiler's dirty-sector gap.

## Problem

A clean inequality for T(V) bounds its expectation, while the existing safe syndrome basin and local exit-source barrier are defined using V. Since every correction decreases V, the CP dressing generally gives T(V)<=V. A volume-uniform bound T(V)>=cV does not follow and is not assumed below.

## 1. A per-animal no-jump lower bound

Each circuit gate is exp(tZ_h), where the Lindblad jumps are J_hs=sqrt(B_h)K_hs and sum_s K_hs†K_hs=I. Clock and data factors commute, so

    sum_s J_hs†J_hs=B_h.

The no-jump CP summand of this gate has Kraus Q_h=exp(-t B_h/2), acting ONLY on clocks. All remaining quantum-jump summands are CP. This is an exact finite-time unraveling of the mathematical CP gate, not a claim about an observed physical reset record.

Fix animal A. Only the bounded-depth causal cone of the physical support of f_A contributes to T(f_A); all other unital circuit factors cancel exactly. Since each check has bounded weight and depth/support sizes are fixed, that cone contains at most C_gate |A| gates. Let Bmax bound ||B_h|| uniformly.

Choose the no-jump summand for every gate in this cone. The resulting ordered Kraus product Q is clock-only, even though its factors need not commute. Positivity of all other summands gives

    T(f_A) >= Q† f_A Q = f_A Q†Q.

The minimum singular value is multiplicative from below:

    Q†Q >= exp[-t sum_cone ||B_h||] I
          >= exp[-C_gate Bmax t |A|] I.

Thus EXACTLY

    T(f_A) >= exp[-C_dress t |A|] f_A.               (1)

No global circuit gate count, global inverse condition number, or false operator inequality for a general noncommuting O is used. The commutation f_A Q=Q f_A holds because f_A is data-only and Q is clock-only.

## 2. Two nearby tuned animal weights

Choose a common theta and two tuned exponents a_+>a_0, both strictly inside the permitted parameter region of the weighted SSF proof. Let

    f_A^+=exp(a_+|A|)theta^{holes(A)},
    f_A^0=exp(a_0|A|)theta^{holes(A)}.

Construct B_h and T and prove the clean/noise inequalities using V_+=sum_A f_A^+ and W_+=sum_A |A|f_A^+. All constants can depend on this fixed choice. Then choose t small enough that

    C_dress t <= a_+-a_0.

Equation (1) yields termwise

    T(f_A^+) >= f_A^0,
    T(V_+) >= V_0.                                 (2)

There is parameter room: in the notation a=(1-u)log(1/theta), the monotonicity, completion and boundary conditions require u to lie in a nonempty open interval (0,u_max). Choose 0<u_+<u_0<u_max; then choose theta sufficiently small for both and finally t sufficiently small. All previous finite-clock t restrictions are upper bounds and are compatible with this additional one.

## 3. Basin invariance and killed comparison

Define the analytical data basin using V_0:

    P={sectorwise minimum representatives component-safe, V_0<M},

where M lies below the local canonical-edge threshold derived for V_0. Both parameter choices obey the full-animal per-move monotonicity. Each Phi_h therefore preserves this basin: V_0 cannot increase, and the local edge lemma prevents a component-unsafe target. Clock-only factors do not change P. Thus every Schrödinger CP gate and T preserve P.

On P, the clean drift proved with V_+ pushes through T, and the Stinespring perturbation lemma gives

    L* T(V_+) <= -c T(W_+)+bN

after sufficiently small generic perturbations, in the model where that clean drift is established. Since W_+>=V_+, positivity gives T(W_+)>=T(V_+). The killed process therefore has a uniform O(N) moment of T(V_+), and (2) controls its V_0 moment by the same bound.

Because T preserves P in the Schrödinger picture and is CP, T(V_+) is block diagonal with respect to P when V_+ is: in a Stinespring/Kraus representation, all Kraus maps preserve P, but THIS ALONE DOES NOT IN GENERAL imply the off-diagonal P-Q block of T(V_+) vanishes. Therefore the generic killed-observable comparison needs an additional check before simply deleting outgoing gains.

For this particular circuit, a stronger property is available for the DATA-syndrome P: each K_hs has a single fixed syndrome-shift character within its measured block, while every no-jump clock factor is data-syndrome diagonal. Expanding the CP semigroup into jump histories, each Kraus history maps any given input syndrome to one definite output syndrome (or zero). However two different input syndromes can in principle merge to the same output. The initial local syndrome measurements in K_hs distinguish them if their trajectories first merge by a correction; without an intervening measurement, clock-only no-jump pieces preserve their difference. Hence T maps syndrome-diagonal observables to syndrome-diagonal observables. This also follows directly from stabilizer-conjugation covariance: every K_hs=F_hs Pi_hs has fixed stabilizer character, B_h is clock-only, so Z_h and T commute with every stabilizer conjugation. A syndrome-diagonal observable is the fixed algebra of those conjugations. Consequently [P,T(V_+)]=0 EXACTLY.

This covariance is the needed stronger fact. It justifies Hamiltonian compression and deletion of positive outgoing jump gains for the dressed observable, exactly as in the original killed-basin proof. Mere basin preservation would not suffice.

Exit-source syndrome blocks obey V_0>=theta^(k_max)M. Thus by (2) their killed mass is O(N/M). All compressed local physical operators have identity canonical logical action by the V_0 edge lemma. Duhamel full-minus-killed and normalization then yield the same polynomial-times-t/sqrt(M) logical bound.

At exact encoded initialization every Phi_h acts identically on the zero-syndrome subspace, so T(V_+) there equals V_+(vacuum) times clock identity. This is O(N), uniformly over a fixed initial clock/bath state independent of the logical input. Require N>=N0 so V_0(vacuum)<M; use the trivial diamond bound for smaller sizes.

## Scope

This closes the dressed-observable/data-basin comparison for the FULL-TENSOR DIRECT fresh-K model, assuming its audited clean drift and the original canonical boundary lemma. In the clean-range-only old compiler, noise can leave the clock/workspace range from vacuum without a high syndrome barrier. No choice of these two weights fixes that separate physical-sector problem.
