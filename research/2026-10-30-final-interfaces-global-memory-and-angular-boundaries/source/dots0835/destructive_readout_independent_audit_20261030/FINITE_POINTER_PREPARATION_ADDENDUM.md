# Separate earned extension: finite preparation of readout pointers
2026-10-30. Independent reviewer construction. This is an additional controlled resource/proof, NOT a modification of frozen readout V1's exact-wait premise.

## Result and added physical premise
Exact initial wait pointers can be replaced by finite-time, complete onsite reset-to-wait channels. Assume the finite three-level pointer is grouped locally with its DATA/resource site, or otherwise has fixed bounded incidence. During preparation add actual separately resolved jumps

    R_a=sqrt(kappa_p)|wait><a|,  a in {wait,0,1},

acting only on the pointer. Omitting the self-input a=wait channel also works. The memory/retirement nominal apparatus acts trivially on these new pointer factors. Pointer preparation can run in parallel with actual retirement. Arbitrary local calibration/control errors and DATA-pointer/bath interactions belong to the same bounded-body incident joint-cb budget. The pointer input may be arbitrary and correlated with the retained apparatus/bath, subject to the overall memory theorem's logical-input initialization contract.

This earns a readout input contract without perfect pointer reset. It does not earn final classical pointer reading, classical-bit reliability or reset-command distribution. The pointer register and these complete onsite reset channels are explicitly supplied hardware.

## 1. Full-state wrong-pointer tail
Let D_i=I-|wait><wait| at pointer i. Nominal preparation gives

    L_prep^*D_i=-kappa_p D_i,
    L_prep^* product_(i in S)D_i=-kappa_p |S| product_(i in S)D_i.

All concurrent nominal native terms annihilate these tests. Center the local perturbation adjoints as in the main readout receipt. The same full-state joint-cb subset hierarchy yields, from ANY initial joint pointer state,

    Tr rho(T_p) product_(i in S)D_i <= p_p(T_p)^|S|,
    p_p(T_p)^q=exp(-q kappa_p T_p)
                 +(C eta/kappa_p)(1-exp(-q kappa_p T_p)).

Choose a fixed T_p and then eta so p_p(T_p)<beta_0/(e C_M) with a fixed strict margin. A union bound gives

    Pr(sum_i D_i>beta_0 N)<=exp(-a_0 N).               (1)

The estimate uses the actual full state, not independence, trajectory conditioning or fictitious reset records. It applies to coherent initially wrong labels and arbitrary shared-bath correlations.

## 2. Compatibility with memory and physical retirement
Every preparation channel is DATA identity, preserves clocks/tags/history flags, and acts on a register absent from the forest and proof observables. Thus it commutes the native proof maps, F moment, canonical basin and readiness-label projections. It neither changes the native halted phase argument nor the canonical logical-edge identity. Noise on enlarged grouped sites is charged in the same local incident budget; fixed site dimension/constants may increase.

Consequently the accepted memory/retirement proof still compares the full joint evolution with a positive killed logical-identity channel. Transfer (1) to that positive killed channel using its independently earned full/killed norm error, exactly as for native readiness. Let

    C_0=1_(sum_i D_i<=beta_0 N).

C_0 commutes the forest, memory basin, and coarse native readiness projection. It is used ONLY analytically. Gentle projection costs at most twice the square root of the omitted mass, plus the already inherited trace/norm error. No physical pointer measurement or dephasing is introduced at the preparation/storage boundary.

If preparation and retirement run together, choose their common duration at least max(T_p,T_ret). This remains fixed independently of epsilon and N. Choose epsilon afterward so the finite halt's O(epsilon T) moment cost fits the original margin, and choose eta last to satisfy memory, retirement, preparation and readout thresholds. Enlarging a fixed duration is not a new asymptotic obstruction.

## 3. Readout with a small coherent initial wrong-pointer set
Resolve pointer labels algebraically on the ket and bra of C_0 rho C_0. Each side has at most beta_0 N non-wait positions. Outside the union S_0 of those two sets, pointers are exactly wait on both sides and factor from the other registers. Conservatively,

    |S_0|<=2 beta_0 N.

No assertion of classical mixture is made. Count S_0 as an additional exceptional readout set. In a Dyson term of order r, let S be the actual insertion-site union and I the final retained incomplete-pointer set. Outside S_0 union S union I, nominal readout is the exact completed ideal Z instrument and commutes all remaining insertions. All actions on the exceptional set—including initially completed but incorrect pointers, coherent pointer labels, local effects, arbitrary output bits and retained bath memory—enter the same finite-system-leg output-instrument expansion proved in the main receipt.

Thus the per-leg DATA weight bound used by the main readout proof becomes

    [alpha+2 beta_0+q gamma+beta]N+O(1),                (2)

or, for the base-native finite ramp,

    [alpha_mem+r_R beta_ctrl+2 beta_0
                   +q_comb gamma+beta]N+O(1).

Take this below the ordinary CSS coset-correction radius, or below the stronger X-sector energy/confinement radius for the deterministic queue decoder. The factor two is deliberate and avoids any unsupported initial-pointer dephasing assumption. A sharper per-leg argument might reduce it, but is unnecessary for a positive threshold.

The final wait-label probability bound in the main theorem is valid from arbitrary pointer inputs, so its incomplete-event estimate still holds. The actual output filter is still classical. Only the preparation-boundary analytical projection incurs a gentle square-root cost. The signed Dyson comparison again has the exact logical diagonal form, and actual CPTP normalization proves the same full logical-Z measurement statement. Add the preparation projection/norm error to delta_in in equation (2) of the main receipt.

## Scope and conclusion
For sufficiently small fixed eta and sufficiently long fixed reset/readout intervals, both pointer preparation and destructive measurement are finite-time physical local processes. Their bad masses and Dyson tail are exponential in N. No perfect pointer reset is required. This is a controlled extension of the already specified measurement primitive, retaining arbitrary common bath and controller correlations; it is not a fault-tolerant classical processor or autonomous command-distribution construction.
