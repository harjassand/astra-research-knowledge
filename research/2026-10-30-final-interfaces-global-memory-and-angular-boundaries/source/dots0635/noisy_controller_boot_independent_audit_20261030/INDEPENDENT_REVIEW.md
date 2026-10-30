# Independent audit: finite-time noisy controller boot

2026-10-30. **SCOPED PASS for the explicitly controlled boot operation, with the Duhamel and positive-factor handoff made precise below.** This is a new initialization interface, separate from the accepted native storage theorem. It assumes already encoded DATA, a fixed logical-independent controller/monitor/bath input, actual finite-rate onsite reset generators during a fixed boot interval, and a declared one-time switch to storage. It is not an encoded-DATA factory, autonomous self-starting theorem, or physical switch implementation.

Frozen source: `FINITE_TIME_BOOT.md`, SHA-256 `f72463e2a71cfbe2fc90956a1a498af04fece19e1a822cee239992ffaa96a6bb`. Root confirmed these bytes frozen. The actual native forest source and accepted storage source are preserved alongside it. No source was edited.

Two potentially invalid readings are explicitly excluded:

1. A dissipative reset propagator is not inverted to form an interaction picture. Use forward Duhamel variation-of-constants, with nominal CP propagators between perturbation insertions.
2. The low-order signed Dyson truncation is not called CP. It is only a common-span comparison. Section 6 below replaces its signed ancillary coefficient by a genuine positive ancillary state obtained from the actual projected channel.

I found no remaining obstruction under these qualifications. In particular sparse syndrome/history labels alone are not used to infer the absence of a logical error.

## 1. The actual nominal boot and backwards test

For each reset register block i, let Reset_i be the onsite channel preparing its declared ready clock/workspace or tag state while retaining DATA and monitor registers. Its actual generator is kappa_i(Reset_i-Id), with kappa_i>=kappa>0. Complete basis-resolved reset Kraus operators implement it at finite rate. Choose the primitive P_i to be the complement of the ready projector for that same reset block, tensor identity on DATA and monitors. Then

    L_boot,0^* P_i = -kappa_i P_i.

The distinct blocks' resets commute, and they annihilate all DATA syndrome/energy occupancy projectors Q_v. Label-only monitor terms also annihilate these diagonal tests; monitor purity is neither required nor asserted. Bath-only evolution acts as identity on these system tests.

For a set S of primitive P/Q labels the proposed F_s satisfies exactly

    (partial_s + L_boot,0^*) F_s = 0.

Each selected factor lies between uI and I. For a joint local noise term, split off selected labels whose physical supports it does not meet. Those factors commute its joint Kraus/Hamiltonian coefficients and pass through its adjoint. At most a fixed m<=qk selected factors remain, with product between u^m I and I. The local cb norm gives a relative order estimate by a constant depending on u and the fixed local label geometry. Summing the actual incident norm budget over supports meeting S gives

    N_s^* F_s <= C eta |S| F_s.

Here C also includes the fixed support size of an individual label. No independent Poisson support process is introduced. The estimate is stable under the retained bath and an arbitrary reference.

Differentiation along the actual positive joint evolution and scalar Gronwall therefore give

    Tr F_T rho_T <= exp(C eta T |S|) Tr F_0 rho_0.

All DATA factors at time zero act as u on encoded DATA. Every initial controller factor is at most u+(1-u)exp(-kappa T), even with arbitrary controller/bath correlations. Hence the joint inclusion bound is

    Tr [product_(ell in S) P_or_Q,ell] rho_T
       <= p_boot^|S|,
    p_boot=exp(C eta T)[u+(1-u)exp(-kappa T)].

It is uniform over logical/reference inputs and the fixed controller/bath state. Choose u, then T, then eta. C can become very large as u decreases, but all choices are fixed, finite and independent of N. No quantitative practical threshold is claimed.

## 2. Actual native forest readiness invariance

I checked the actual `FULL_HILBERT_FOREST_GAUGE.md`, not merely the boot note's declaration. Each F_h is a direct sum over its clock phase and resource tags. It is identity in every A and Q phase and acts only on h's workspace and DATA resources actually tagged o_h. Other owners' factors do not act on h's private workspace. Therefore

    [F, |A0,W0><A0,W0|_h]=0,
    [F, |free><free|_r]=0.

Thus F and F^dagger preserve every primitive readiness P_i. This remains true on malformed masks and arbitrary workspace inputs. Monitor states do not enter these readiness projectors.

The actual history B_h is a function of clock/own-lock consistency and W_h=0. It commutes every primitive readiness projector as well. This additional commutation is useful at the projection handoff below. It would not follow for an arbitrary DATA-dependent notion of readiness or an arbitrary encoding frame.

For each DATA occupancy label Q_v, let C_v be the OR of the non-ready hub/register labels that can activate a forest factor affecting its bounded physical support. When C_v=0 those factors are identity, and all remaining factors commute Q_v. C_v commutes the frame, so

    F Q_v F^dagger <= R_v=C_v+(I-C_v)Q_v,
    F R_v F^dagger=R_v.

A history B_h is bounded by the OR of primitive non-ready blocks in its finite history footprint: if all those blocks are ready, B_h vanishes. The same domination holds after frame conjugation. All these OR witnesses commute each other. They commute the frame-transformed output labels because they are frame-invariant and commute the untransformed raw-syndrome/history algebra. Consequently products, not just marginals, are bounded.

Every output label has at most b primitive witnesses and every primitive label witnesses at most k' output labels. For m output labels, expand their OR events in at most b^m assignments; each assignment uses at least m/k' distinct primitive labels. This proves

    p_out <= b p_boot^(1/k').

Repeated analytical flag tokens are included in k'; they are not treated as independent physical registers.

This receipt verifies the native forest frame. Another simple/encoding frame is covered only if the same preservation and bounded witness properties are separately established.

## 3. Uniform O(N) raw moment in the storage frame

On the framed output the raw syndrome/history occupancy projectors commute. Expanding their joint generating function gives, for every animal A,

    E f_A <= [exp(a)(theta+(1-theta)p_out)]^|A|.

The storage graph is fixed and has bounded animal entropy. Choose p_out small enough for the already selected upper raw exponent V_high; its expectation is then O(N), uniformly over the logical/reference input and the arbitrary fixed controller/bath input. The accepted native observable satisfies F_storage<=V_high, so it inherits this moment. No false inequality G_A<=I is used.

This is only a moment statement. A nontrivial logical Pauli can leave every syndrome and controller label zero, so it is not a logical-correctness argument.

## 4. Correct Duhamel expansion and a common DATA span

Let G_0(t,s) be the nominal boot CP propagator including controller resets and retained bath-only evolution. It acts trivially on DATA and has diamond norm one. Expand the actual evolution by iterating forward variation-of-constants:

    G_0(T,t_r) N_(t_r) G_0(t_r,t_(r-1)) ...
                   N_(t_1) G_0(t_1,0),
    0<t_1<...<t_r<T.

No G_0 inverse appears. The sum of joint local perturbation norms is at most C_phys N eta. The order-r norm is therefore at most (C_phys N eta T)^r/r!, and the discarded tail at r>=r_* obeys the source's bound

    epsilon_D <= exp(C_phys N eta T)
                  [e C_phys N eta T/r_*]^r_*.

For r_*=floor(zeta N) with a fixed positive zeta and eta T sufficiently small, this is exponentially small in N.

Each local insertion has a finite DATA Pauli left/right expansion supported on at most q DATA sites, with arbitrary retained controller/bath coefficient maps. If a grouped site contains several DATA factors, replace q by the fixed corresponding DATA support bound. The nominal propagators do not enlarge DATA support. Hence the entire signed order-<r_* truncation is in the common left/right Pauli span of weight at most q r_*. There is no sum of absolute Pauli coefficients in the estimate; the discarded tail was bounded before making this span observation.

The initial controller/monitor/bath state must be fixed independently of the logical input. Otherwise the coefficient maps of this span can already contain logical information, and the factorization below would not follow.

## 5. Low controller excitation, frame support and basin projection

Let M_ctrl<=a_ctrl N count primitive controller reset blocks, and let C be the projector onto at most alpha N non-ready blocks. The joint inclusion bound implies

    epsilon_C = sup_input Tr (I-C) rho_boot
       <= binom(M_ctrl,ceil(alpha N)) p_boot^ceil(alpha N)
       <= exp(-c_C N)

for p_boot sufficiently small. The actual boot map is CP, so uniform gentle compression gives a diamond error at most 2 sqrt(epsilon_C) when replacing it by C rho C. This holds with arbitrary reference. C is an analytical projection, not an inserted physical measurement.

The native frame preserves every P_i, hence C. On each joint P-mask with at most alpha N occupied blocks, at most alpha N hubs can activate nonidentity forest factors. Their union of DATA footprints has size at most r_frame alpha N. Coherent superpositions of mask locations do not change the common span: the mask projectors are controller-only coefficients, while each mask's DATA Pauli terms have that bounded weight. There is no assumption of a classical mask distribution.

Applying the frame to the compressed low-order Duhamel map therefore gives one common DATA error span of weight

    w_* = q r_* + r_frame alpha N.

Choose zeta and alpha so 2w_* is below both relevant code distances and w_* is below both linear Tanner component cutoffs. Every Pauli in this span has a canonical minimum representative of weight at most w_*, hence component-safe. Its product with that representative is a stabilizer, since it has zero syndrome and weight below distance. Thus its canonical logical action is identity. This argument is for the linear-cutoff family, not a sqrt(N)-cutoff family with finite-density controller excitation.

Let P_comp be component safety. The signed framed/compressed low-order map has support entirely in P_comp. Its actual positive counterpart differs by at most epsilon_D in diamond norm; therefore its component-unsafe probability is at most epsilon_D. This conclusion uses positivity of the actual channel, not positivity of the signed truncation.

Let P be the accepted raw-potential/component basin. The raw upper moment gives high-potential probability at most C N/M. Projection onto P therefore has gentle error at most

    2 sqrt(epsilon_D + C N/M).

There is no moment loss hidden in these analytical projections. In the native frame, C commutes every raw syndrome label and every B_h, hence V_high; P is in the same raw diagonal algebra. Consequently compression by C and P cannot increase the V_high expectation. The final positive projected channel A retains the O(N) F_storage moment and has support in P.

## 6. Positive ancillary replacement: no signed CP assertion

Pass to the fixed canonical logical/syndrome/controller gauge on P. The projected signed low-order map has the form

    B_signed(rho_L)=rho_L tensor tau_signed,

with tau_signed Hermitian but not necessarily positive. The actual projected map A is CP and trace-nonincreasing, and

    ||A-B_signed||_diamond <= epsilon_D.

Choose any fixed normalized logical state omega_L and define

    sigma = Tr_L A(omega_L).

Then sigma>=0 and Tr sigma<=1. Contractivity of evaluation and partial trace gives

    ||sigma-tau_signed||_1 <= epsilon_D.

The genuine CP/TNI product map B_pos(rho_L)=rho_L tensor sigma consequently satisfies

    ||A-B_pos||_diamond <= 2 epsilon_D.

This elementary replacement closes the signed-truncation handoff without asserting that the truncation is CP or that its scalar logical coefficient is a probability. Since sigma is obtained from the actual projected channel, it has support in P and the same O(N) upper F moment. Its trace deficit is bounded by the exponentially small projection failures. One may retain the TNI form or normalize sigma and charge that deficit separately.

The argument works uniformly with an arbitrary reference. Logical/reference coherence is preserved by the common error span; the fixed omega is used only to extract a positive ancillary comparison state.

## 7. Entering the already accepted storage proof

The native storage drift/killed-basin proof needs an initial logical-identity factor, support in its raw basin and an O(N) F moment. It does not intrinsically require a physically perfect controller reset once those properties have been earned. The positive product comparison from Section 6 supplies them, allowing arbitrary correlations inside its fixed syndrome/controller/monitor/bath state.

The killed canonical generator acts as identity on the logical factor under the imported local-edge theorem. Its positive moment evolution and boundary estimate therefore apply to this new initial ancillary state exactly as before. CP/TNI evolution cannot increase the diamond error made at boot. Combining the two gentle errors, the Duhamel tail and the storage boundary error yields, after shrinking the fixed threshold and exponent,

    logical error <= C N^(3/2) (1+u_storage) exp(-cN).

The assertion is for sufficiently large N, including the accepted storage N>=N0 and the fixed rounding/cutoff conditions above. The finite boot time T and all rate/noise choices remain independent of N. A noncircular choice is: first fix the accepted storage apparatus/potential and linear code margins; choose alpha and zeta for the common correctable span; determine the p_boot target from both the controller tail and raw moment; choose u and T; finally choose eta below the storage threshold, backwards-test bound and Duhamel-tail threshold. Storage time is u_storage; it is not the backwards-test parameter u.

## 8. Operational boundary and conclusion

The proof is a valid finite-time noisy-controller initialization interface for the actual native forest construction. It does not require exact finite-time reset, bath refresh, a stochastic Pauli-noise model, measurement of masks, or positivity of a signed Dyson truncation.

It does require:

* DATA already encoded, with arbitrary logical/reference input;
* a fixed logical-independent initial controller/monitor/bath state;
* a controlled boot mode with DATA payload dynamics held off and the stated onsite reset generators on;
* the regularity and bounded joint local perturbation budget needed for the actual CP propagators and Duhamel expansion;
* an explicit one-time switch, instantaneous in this note. A finite-duration or faulty switching implementation is not supplied and must be separately included in the dynamics;
* the same linear-cutoff code and fixed-graph storage interfaces as the accepted native theorem.

Accordingly this acceptance must not be folded retroactively into the unchanged autonomous-storage apparatus as a self-starting capability, nor relabeled as noisy encoded-DATA preparation or noisy physical retrieval.

## 9. Independent finite diagnostics

`check_boot_interfaces.py` checks the backwards equation in an eight-dimensional DATA/controller/retained-bath model with initially Bell-correlated controller/bath, then evolves the actual reset-plus-coherent-noise generator. The backwards residual is below 4.1e-17 and the joint label bound holds. A separate nonmonomial controlled forest fixture gives zero readiness commutator and the OR covering/invariance relations to 4.5e-16. Finally a [[4,2,2]] stabilizer example has exactly zero syndrome moments but trace-distance-two logical change, explicitly testing the necessity of the common-span argument. These are algebra/interface regressions, not a simulation or proof of the full native Tanner memory.
