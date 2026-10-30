# Finite-time controller boot under bounded continuous noise
2026-10-30. Root construction candidate; not independently reviewed. This supplies an explicit ONE-TIME controlled startup mode, not an autonomous self-start theorem or an encoded-DATA factory.

## 1. Actual operation and input
The DATA arrives encoded, with arbitrary logical/reference state. Controller registers and the retained bath may begin in any joint state FIXED independently of that logical input. During a fixed boot interval [0,T], replace the storage clock/payload dynamics by complete onsite controller-part resets to the declared ready configuration: hub A0/workspace zero and resource tags free. Hold the other storage transitions off. Actual label-only monitors may remain on because their adjoints annihilate the diagonal tests below; alternatively hold them off too. Their states need not be pure or reset. DATA payloads are not reset. Each site reset has rate kappa_i>=kappa>0; the boot channels are actual onsite CPTP reset generators kappa_i(Reset_i-Id), not finite-time perfect preparation.

Keep the same bounded-body joint perturbation class throughout boot, with per-site incident cb-norm sum <=eta and full joint CPTP propagators. Bath-only dynamics may be retained. One-time switch into the storage generator is an explicit control interface; finite switching errors/duration must be charged. This does not assert that the unmodified storage Hamiltonian resets arbitrary DATA/controllers safely by itself.

Let P_i be the projector that clock/workspace/tag part i differs from its ready state, tensor identity on DATA AND monitor factors. These commute. Let Q_v be the commuting DATA syndrome/energy-token occupancy projectors, all zero on encoded DATA. Each physical site meets at most k such P/Q labels, each label has bounded physical support, and noise terms act on at most q sites. N_ctrl=O(N).

## 2. A time-dependent positive test gives sparse joint labels
Fix u in (0,1) and any set S of DATA/controller labels. Define the backwards ideal-reset test

    F_s= product_(v in S_DATA)[u+(1-u)Q_v]
         product_(i in S_ctrl)[u+(1-u)exp(-kappa_i(T-s))P_i].

All factors commute and lie between uI and I. For the nominal boot generator L0,

    partial_s F_s+L0^*F_s=0.

The local relative-factor argument, using the actual incident cb-norm SUM, gives

    N_s^*F_s<=C(u,q,k) eta |S| F_s.

No stochastic support decomposition of continuous noise is assumed. Gronwall along the ACTUAL positive joint evolution yields

    Tr(F_T rho_T)<=exp(C eta T |S|)Tr(F_0 rho_0)
                  <=[exp(C eta T)(u+(1-u)exp(-kappa T))]^|S|.

The DATA factors at time zero equal u on the encoded state; arbitrary controller/bath correlations do not exceed the displayed operator maximum. Since product_(v in S)Q_v <=F_T (with P_i used for controller labels), the joint commuting-label distribution at boot exit obeys a local-stochastic inclusion bound with parameter

    p_boot=exp(C eta T)[u+(1-u)exp(-kappa T)].          (1)

This is a statement about joint label effects, NOT a Pauli-mixture model. It is uniform over logical/reference inputs and initial controller/bath states. Choose u and exp(-kappa T) small, then eta small so p_boot is below any fixed desired threshold. T and all choices are independent of N.

## 3. Moving into the actual storage frame preserves a sparse-label bound
The actual storage forest/simple frame is bounded depth and is identity when local controllers are ready. Its nontrivial factors are controlled by a non-ready hub clock, and it preserves the P_i above (controller readiness projectors must be defined only on clock/workspace/tag parts, never on the DATA payload or a particular monitor state).

For a DATA label v let C_v be the OR of the finitely many controller P_i that can activate a frame factor affecting v. If C_v=0, the frame commutes Q_v. Hence

    F_frame Q_v F_frame^dagger <= R_v=C_v+(I-C_v)Q_v.

R_v is invariant under the frame. All R_v commute with one another and with every frame-transformed label, so their product bounds are valid, not merely separate marginal inequalities. A transformed history defect B_h is similarly bounded by the OR of the finitely many non-ready controller parts in its physical history footprint; no DATA-dependent history is silently measured.

Every output label has at most b primitive P/Q witnesses, and a primitive witness affects at most k' output labels. Expanding these OR events and using (1) gives output-label inclusion strength

    p_out<=b p_boot^(1/k').

For any tuned raw animal potential,

    E f_A <=[exp(a)(theta+(1-theta)p_out)]^|A|.

Thus the raw upper potential V_high has O(N) expectation once p_boot is sufficiently small. Any accepted storage proof observable bounded above by this V_high inherits that initial moment. The native activity-weighted candidate uses such an upper bound rather than falsely asserting G_A<=I.

## 4. Small label moments alone do not exclude an undetected logical error
A separate common-span argument is required. Work in the interaction-picture/Dyson expansion around nominal controller-only resets and bath-only evolution. The latter acts trivially on DATA. The perturbation total diamond norm is at most C_phys N eta. Each order-r term has a finite DATA Pauli left/right expansion supported on at most qr DATA sites; nominal boot evolution never enlarges that DATA support.

For r_* proportional to N, the norm of the omitted Dyson tail is bounded by

    sum_(r>=r_*) (C_phys N eta T)^r/r!
      <=exp(C_phys N eta T)[e C_phys N eta T/r_*]^r_*.

Choosing eta T sufficiently small makes this exp(-cN). A signed low-order truncation need not be CP; only its common operator span and the norm of the discarded tail are used.

Also, (1) gives an exponentially small probability that more than alpha N controller parts are non-ready, by a union bound over subsets. Insert the corresponding analytic low-excitation projector C_ctrl; gentle projection changes the actual channel by exp(-c'N). This is not a physical measurement.

On that low-excitation subspace the storage frame has at most O(alpha N) nontrivial local factors. Its DATA Pauli expansion therefore has support at most r_frame alpha N, regardless of coherent superpositions of the locations. Combining it with the low-order boot expansion gives a COMMON DATA error span of weight at most

    q r_*+r_frame alpha N.

Choose r_*/N and alpha so twice this bound is below code distance and it is below the linear Tanner component cutoff. Every canonical representative is then component-safe and every coefficient has identity logical action in the canonical gauge. No exponential count of Pauli coefficients is used: all coefficients belong to one correctable span.

This section relies on the LINEAR Tanner cutoff. It is not a proof for finite-density boot errors with a sqrt(N) cutoff.

## 5. Entering the storage basin without ideal cleanup
The actual framed boot state has O(N) upper-potential moment. Component/logical safety fails only by the exponentially small norm errors in Section 4. Project analytically onto the accepted raw-potential/component basin P; the high-potential mass is O(N/M), M=exp(cN), and gentle projection costs exp(-c'N).

After the frame and these analytical projections, the low-order common-span map factors as identity on the logical/reference subsystem tensor an ancillary map. That ancillary map need not be positive before the discarded tail is restored. The actual killed storage state is positive and obeys the ordinary moment drift; its difference from the factored truncation is exponentially small and cannot increase under the CP/TNI killed evolution.

Consequently an accepted constant-rate continuous-noise storage theorem with this basin structure extends to this boot operation with a bound of form

    logical error <=C N^(3/2)(1+t)exp(-cN),

after decreasing the fixed noise threshold. No perfect controller reset or bath refresh is inserted at the handoff. Encoded DATA preparation remains a separate resource.

## 6. Open review obligations and operational boundary
- Verify the actual selected frame preserves the chosen controller-part readiness projectors and the finite witness covering used in Section 3; this holds for clock/tag-controlled forest factors but is not true of an arbitrary encoding circuit.
- Use a proper Dyson expansion around the full nominal CP boot propagator, with the retained bath and reference; the support argument expands only finite DATA legs.
- Make the one-time boot/storage mode switch explicit. If it has a non-negligible physical duration, its real generator and noise must be included; it is not supplied by this note's instantaneous switching convention.
- This is not a known-Bell factory, bare unknown-input encoder, autonomous self-starting device, or practical threshold estimate. It is a constructive finite-time noisy-controller initialization interface under declared startup control.
