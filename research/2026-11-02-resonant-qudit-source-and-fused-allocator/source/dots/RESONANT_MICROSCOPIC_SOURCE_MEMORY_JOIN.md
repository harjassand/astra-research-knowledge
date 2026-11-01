# Root join: resonant two-body syndrome service inside autonomous protection

2026-11-01. Draft for independent whole-join review. This replaces only the source implementation of the received six-qubit-GKSL controller. It does not turn the entire classical controller into a two-body Hamiltonian device, nor establish practical superiority.

## 1. Capability and hardware contract

Use the same specified Tanner-witness family and protected component as the prior received construction. Preserve its radius, robustness, ideal encoded-input and ideal terminal-decoder assumptions. All controller and source degrees of freedom are physical and subject to the admitted continuing local noise.

For each weight-w commuting Pauli check, replace the engineered clock-labelled source jump by the explicit resonant apparatus in EXPLICIT_TWO_BODY_QUDIT_SOURCE.md. It is ONE physical qudit of dimension 8w+6, including cache, probe and all ground/excited phase slots. Every ideal source Hamiltonian acts on that apparatus and one data qubit. Every source bath jump acts on the apparatus alone. There is no hidden one-particle subspace, no off-resonant order-w Raman amplitude, and no external runtime timing signal.

The channels include actual finite-impurity preparation, coherence-preserving collective interstage decay, and final readout/cache overwrite at finite rate gamma. Indistinguishable decay across probe values, selective multilevel couplings, stationary pumping/reset reservoirs and phase references are real requirements. Physical errors breaking these requirements are charged after the hardware is selected. An abstract finite-dimensional Hamiltonian/bath model is specified; no atomic species or electromagnetic implementation has been certified.

The remaining Boolean verifier uses its existing fanin-two, at-most-three-site classical GKSL operations, and flag actuation uses its existing conditional local operation. Thus the accepted claim, if reviewed, is a TWO-BODY QUANTUM SOURCE with onsite baths inside that controller. It is not a full two-body/onsite realization of every classical gate. A large w makes the qudit large; this trade must not be hidden by calling it a physical qubit.

## 2. Actual stage completion and cache refresh

For each coherent ground/excited phase with invertible unitary coupling gU and decay gamma, let

  B>=||U-dagger H_env U-H_env||

bound the ACTUAL incident coupling difference. Other-apparatus bath couplings commute with U and may be dilated without charging the entire environment bandwidth. Noncommuting data noise remains separately admitted, not omitted.

The Volterra/Gramian argument proves, for every coherent/entangled initial stage state,

  P(stage completes by t0)>=p0,
  t0=1/(g+B+gamma), p0=gamma g^2/[100(g+B+gamma)^3].

Iteration and a finite number of stages give a uniform conditional exponential survival envelope S(t) for an active cycle. The final onsite readout has exact hazard gamma and is included. Set tau=integral S. These are explicit finite intensive constants, not independent classical clock assumptions.

Let r be the actual idle preparation-pump rate, p the admitted bad preparation/readout branch, and Delta the check-overlap degree. Source activity obeys the full operator bound

  exp(t L_src^*) A_s <= [S(t)+r tau] I.

The last-window construction gives, with T_E=B0+L,

 exp(T_E L_src^*) e_s <= delta_E I,
 e_s=(I-Z_cache,s Sbar_s)/2,
 delta_E=exp[-(rF/8)floor(L/(3F))]+S(B0)+r tau
          +2Delta r integral_(B0)^infinity S(t)dt
          +(2Delta r^2 tau+p r)L.

Here S(F)<=1/[8(Delta+1)], (Delta+1)rF<=1/8 and p<=1/4. This includes arbitrary initial partial probes, reports from earlier-born cycles, and wrong reports AFTER a good report. It is an all-initial-state CP/operator inequality. With z=(Delta+1)r tau+p, suitable B0 and L=O(r^-1 log(1/z)) make delta_E tend to zero. Likewise choose T_A and r so delta_A=S(T_A)+r tau is as small as needed.

The proof-only independent Poisson attempt streams uniformize the invariant activity blocks. They are not a physical controller, independent quantum states, or independent completion clocks. Future neighbor histories are not postselected when applying the stage bound.

## 3. Positive local generator correctors

Apply FINITE_PATCH_CORRECTOR_RECEIPT.md to e_s and A_s (the activity projector is denoted A_s only in this section). For each choose a finite patch radius R, retaining actual source terms without artificial boundary resets. Define

  H_e,s=integral_0^T_E exp(t L_R^*) e_s dt,
  H_A,s=integral_0^T_A exp(t L_R^*) A_s dt.

These satisfy 0<=H_e,s<=T_E I, 0<=H_A,s<=T_A I. Their full-source drift is

  L_src^* H_e,s <=-e_s+q_E I,
  L_src^* H_A,s <=-A_s+q_A I,

where q_E=delta_E+delta_R,E and q_A=delta_A+delta_R,A. For local generator norm bound lambda, term-overlap degree Z and m seed terms, one explicit locality floor is

  delta_R=2 lambda m exp(-mu R)[exp(lambda Z exp(mu)T)-1]/[lambda Z exp(mu)].

This includes BOTH finite-evolution and boundary-generator errors and works on expanders via the path-count proof, not a polynomial-growth locality theorem. Source parameters first make delta_E,delta_A small; finite R then makes each locality floor small. R, local dimension and certificate-computation cost can be enormous, but are independent of n. A numerical approximation adds its actual positivity/commutation/residual error budget; the exact integral defines the theorem without requiring a device to store or compute it.

Every individual ideal source term preserves every dressed stabilizer and logical label. The cache-block-diagonal observable algebra is invariant. Therefore H_e,s and H_A,s commute with all protected component labels and every physical cache Z. Boolean input reading/dephasing leaves them unchanged; they do not depend on Boolean output wires or correction flags. Scalar W conservation alone would not suffice for these statements.

## 4. Exact controller coupling, including cache-write exposure

Let a be the flag actuator rate and g0 a fixed reference source rate. Retain the earlier Boolean consistency E=sum_i w_i e_i, with delta_i=w_i-sum_child w_child>0, cache sensitivities B_s, and wrong-output influence constants R_i,R_s. Let D_W bound a flag move's W change and B_act its E change.

Choose

  epsilon=a/g0, epsilon B_act<=1/2,
  alpha_s=a[(1+D_W)R_s+1],
  gamma_i>=g0[((1+D_W)R_i+w_i)/delta_i].

All source cache changes occur only at the explicit final readout jump, with total rate gamma times its final-phase projector. A conservative all-state bound is

  L_src^*(epsilon E)<=sum_s epsilon B_s gamma A_s,

where now A_s is the source activity projector. This prices ALL cache writes, not just good or bad ones. It is safe for coherent probe states because E is cache/wire diagonal and each completed overwrite changes its value by at most B_s.

Set

  V=W+epsilon E
      +sum_s[alpha_s H_e,s+epsilon B_s gamma H_A,s].

The H_A terms cancel the actual cache-write exposure. Combining the previously received flag/Boolean inequalities with the actual source correctors yields, throughout the old protected component and on arbitrary source states,

  L_ideal^*V <=-(a c0/2)W-a E-a sum_s e_s+b_src n I,

where c0W is the true improving-move lower bound. If the sensor density is at most C_s, alpha_s<=C_alpha a, B_s<=B and gamma/g0<=C_gamma, then

  b_src/a<=C_s[C_alpha q_E+B C_gamma q_A].

Moreover V=W+Z with positive Z and

  Z<=a K_T n I,
  K_T=C_E/g0+C_s C_alpha T_E+C_s B C_gamma T_A.

No maximum over a free unbounded reservoir is used; this particular apparatus is finite-dimensional. No classical source-clock independence or malformed-clock repair is needed because every qudit level is explicitly in the source program. Arbitrary physical jumps between levels remain noise, not ideal valid progress.

## 5. Positive formal parameter region and actual noise

Set c=a c0/2 and C_b=C_s(C_alpha+B C_gamma). Choose source parameters and finite patch radii so q_E,q_A<=q with

  q<=beta c0/(64 C_b).

Then choose actuator rate a and Boolean weight epsilon so

  a K_T<=beta/32,
  a/g0<=1/(4 B_act).

After ALL apparatus rates, dimensions, patch norms and incidences are fixed, require the actual local Hamiltonian/jump perturbation action on V to obey

  L_noise^*V<=u_V n I,
  u_V/a<=beta c0/64.

Absent mechanisms are omitted rather than divided by zero. The full mean inequality is then

  L*V<=-cV+[b_src+u_V+c aK_T]n I,
  [b_src+u_V]/c+aK_T<=3beta/32.

There is a sufficiently small positive intensive perturbation neighborhood for each finite selection, but this is NOT a useful laboratory threshold estimate. Patch-incidence growth can make the bound extremely pessimistic. Noise on pumps, collective decay, level energies, couplings, caches, classical gates and flags is all included; rate-dependent error is evaluated after rates are selected.

## 6. Protected interface and storage consumer

The controlled-prefix dressing has fixed finite-depth support for bounded check weight/degree and finite apparatus dimension. Transport the old good-component projector P through it and the flag frame. Every source corrector commutes all underlying component labels, so [P,V]=[W,V]=0 and V>=W. The bounded-support old-frame Pauli alphabet is explicitly enlarged to cover every actual H, J and full J-dagger-J component, as in the received source-controller theorem. This earns protected factorization and the actual two-step W-shell bandwidth for sufficiently large n.

The exact local noncommuting exponential expansion applies because the finite-patch potentials have finite support/norm/incidence independent of n. Choose a fixed exponent k>0 small enough that its local quadratic remainder divided by c contributes at most beta/8. With the Foster splitting density beta/2, the moment prefactor is at most3. The received killed-subchannel comparison gives

  logical output error <=2 sqrt(3) n(2h_all+3Gamma_all) T_storage
                           exp(k b_W) exp(-k beta n/4).

All actual cut-crossing source/controller/noise terms are counted. Commuting bath-only terms contribute zero. Initial W=0 encoded states have moment bounded by exp(k aK_T n), including arbitrary free apparatus states only in that ENCODED subsystem. No arbitrary unencoded hot attachment is licensed. The terminal consumer remains ideal frame undo plus the received Tanner decoder; noisy encoding/terminal readout need their own admission.

## 7. Early implementation comparison and judgment

An exact finite two-check calculation retains coherent overlapping progress. With g=gamma=1 and pure preparation, r=.001,.01,.05,.1 gives retained wrong-cache probabilities .001059,.010076,.041487,.067902 and report fluxes .000995,.009478,.039133,.064149. The positive two-cell Poisson-price range scales approximately as1/r. These are numerical checks, not the uniform-network proof or a memory threshold. The same-hardware isolated source has zero ideal wrong-cache probability; it is a component reference, not a complete competing two-check schedule.

The resonant source avoids the high-order Raman amplitude. The alternative Raman construction was tested early: naive weight-four overlap has an order-J conditional Stark interaction, and weight-six overlap can exceed J as eta decreases. Reordered paths repair two examples, not arbitrary graphs. Its active same-coupling-graph benchmark also requires explicit timing, switching and reservoir controls. Neither route earns a blanket hardware advantage.

This join would remove the engineered multi-site quantum-source jump premise at the cost of a selective multilevel apparatus and coherent-preserving local reservoir. It does not remove the earlier huge Tanner/Boolean constants, routing burden or the dilution-versus-tracking tradeoff. Higher-rate autonomous control and gauge-based measurement are separate alternatives being tested. Further depth is justified only if these physical costs permit a consequential capability, not merely a longer theorem.
