# A stronger equally informed local-CPTP comparator

28 October 2026. **Proof candidate, separate from the frozen raw-sign/localization manuscript.** No new source samples. This addendum improves the inverse-contrast dependence of fine candidate acquisition by letting a conventional learner optimize the actual empirical two-axis calibration risk over all local CPTP decoders. It uses the SAME physical states and comparison tournament, not a more informed source oracle.

Import the model, known physical locality, coarse overlap localization, fresh-bank schedule, comparison measurements, and finite encoder design of `ordinary_local_mixed_gauge_decoder_tournament_20261028.md`, frozen SHA `b1102426bfb3af58483e0d84fedde59e9317a6c0bfaac0a9e59a761f4976a9be`. In particular on each true patch the exact local logical decoder D_* exists, its pullbacks are B_j, and for every physical D

    (kappa/2)ell0(D)<=r(D)=g(D)−g_*<=ell0(D),
    ell(D E_x)−ell_star(x)<=4ell0(D).                       (1)

Neither g_* nor D_* is supplied to the learner. The matrices G_alpha may be noncommuting/rank deficient; no eigenvalue floor or noise flag is added.

## 1. A physically feasible empirical decoder, not an arbitrary sign pair

For each fine candidate patch I, obtain the four density estimates tau_(j,s), j=X,Z,s=±, from the actual fresh Bures banks. Define the known linear objective

    ghat(D)=1/2−(1/8)sum_(j,s) s Tr[sigma_j D(tau_(j,s))]. (2)

Minimize it over ALL CPTP maps from the d=2^w local patch to one qubit, to additive optimization tolerance zeta. This is a known-coefficient SDP on the unnormalized Choi matrix J, with

    J>=0,  Tr_output J=I_d.

The strictly feasible center J0=I_(2d)/2 has minimum eigenvalue1/2, trace d and known affine constraints. This is not the hard global weighted/rational active-design problem: the encoder and state estimates are fixed, and the objective is linear in one local decoder. Each candidate is frozen after its own solve.

Use a finite solver with an EXACTLY feasible returned physical channel. One elementary feasibility repair is as follows. Choose a strictly positive rational delta. Suppose the rational Hermitian approximate solution Jtilde obeys lambda_min(Jtilde)>=−delta and ||Tr_output Jtilde−I||_infinity<=delta. Set

    Jhat=Jtilde+(I_2/2) tensor (I_d−Tr_output Jtilde),
    Jphys=(Jhat+4delta J0)/(1+4delta).                      (3)

Then Tr_output Jhat=I, lambda_min(Jhat)>=−3delta/2, and Jphys is strictly PSD and exactly TP. The identity ordering follows the output-first Choi convention. These claims can be certified by exact rational arithmetic. Indeed ||Jhat−Jtilde||_1<=d delta, ||Jhat||_1<=d+6d delta, and ||Jphys−Jhat||_1<=8d delta; hence total repair is at most9d delta. The objective coefficient norm is at most1/2, so its increase is at most(9/2)d delta. Choose the solver's objective tolerance and delta=O(zeta/d) sufficiently smaller than zeta, e.g. objective slack zeta/4 and delta<=zeta/(128d), so the repaired channel is within zeta of the true optimum. A known-center mixing argument supplies polynomial-bit Slater margins for approximate optimization; the correction does not depend on the unknown optimal decoder's smallest Choi eigenvalue. The known-interior solver and prescribed precision must have a deterministic polynomial cap and the stated certificates for EVERY normalized density-estimate input, including statistical bad histories; data failure does not invalidate its Slater center. A fallback replacement remains physical, but any failure to deliver the promised numerical certificate must be covered by the implementation guarantee, not an invented additional probability allowance. Never declare a nonpositive fitted Choi matrix physical.

Jphys has the learner-generated certified lower bound Jphys>=[delta/(2(1+4delta))]I; this is NOT a source eigenvalue-floor assumption. Exact rational PSD Jphys has a finite algebraic Gram/Kraus factorization. Its TP identity supplies an exact-reference Stinespring isometry with environment dimension at most2d, embedded in a known unitary of dimension at most4d. Thus at most two additional local reset qubits suffice, with all unused registers traced out. Generic synthesis costs O(poly(w)4^w) gates before precision overhead, followed by the whole-process compilation-error allocation already required by the main theorem. No exact floating eigenvector or free arbitrary-CPTP hardware primitive is assumed. The old two-reflection decoder is a simpler competing control architecture, not falsely declared to implement this more general optimum.

## 2. Localized Bures ERM bound

Only analyze the fixed true patch I_*; other candidates remain physical but may be arbitrarily bad. Let D be its empirical optimizer, A_j=D†sigma_j, and H_j=A_j−B_j. These H_j are observable differences, NOT the gauge contrast matrices with the same letter in the source model. Define a_(j,s)=Tr r_(j,s) H_j^2. Assume each of the four root-fidelity deficits is at most m.

The received Uhlmann inequality, valid pointwise for every Hermitian H_j even when chosen from the same estimated states, gives

    |Tr H_j(r_(j,s)−tau_(j,s))|
              <=2sqrt(2m a_(j,s))+4m.                     (4)

Empirical optimality against the feasible true decoder D_* implies

    r(D)<=zeta+(1/8)sum_(j,s)
                         |Tr H_j(r_(j,s)−tau_(j,s))|.      (5)

For Hermitian contractions A_j and exact reflections B_j,

    sum_(j,s)a_(j,s)=2sum_(j=X,Z)Tr rho(A_j−B_j)^2
                         <=16ell0(D)<=32r(D)/kappa.        (6)

Cauchy–Schwarz over the four states then gives the FAST excess-risk inequality

    r<=zeta+4sqrt(m r/kappa)+2m.

Young's inequality 4sqrt(mr/kappa)<=r/2+8m/kappa yields

    r(D)<=20m/kappa+2zeta.                                (7)

No raw calibration noise floor appears, and no inverse gauge weight occurs. Unlike independent raw-sign composition, this learner optimizes the actual jointly constrained calibration objective; that is the source of the better contrast dependence. This is an ordinary local channel-adapted SDP with an explicit finite state-acquisition ledger, and is available to the strongest equally informed conventional learner.

## 3. Substitute into the already physical tournament

Choose zeta<=m and

    m=kappa^2 epsilon/32768.                              (8)

Then at least one fine candidate has

    r_min<=22m/kappa<kappa epsilon/640.                    (9)

This is exactly the input required by the frozen main theorem's balanced tournament; every candidate's true pullbacks A_X,A_Z are now computed from its actual Choi/Kraus controls rather than from the raw-sign formula. All physical spectral-difference laws, variance bounds, finite backward diagonalization, disjoint SAME-output measurement option, and union-patch control costs remain unchanged for arbitrary physical CPTP candidates.

Use the coarse source cap2qN0 and localized candidate count R_max=min(n−w+1,2w−1) from the main theorem. Replace its fine per-bank cap by

    N1_ERM=ceil[(80*4^w/m)log(48*4^w*R_max/beta_A)].        (10)

Keep its tournament Npair, encoder N_count and total complete source cap

    2qN0+4q1N1_ERM+(R_max−1)Npair+N_count+1.               (11)

For R_max=1, the comparison term is zero. The +1 counts one final payload. The same beta_0+beta_A+beta_Q+beta_C<=epsilon/8 and whole-process implementation budget nu<=epsilon/8 suffice. Exact finite SDP arithmetic/optimization errors are already included in zeta; stochastic source or circuit failures may not be silently reassigned to it.

The preferred fine source rate becomes O_tilde(w4^w/(kappa^2 epsilon)), rather than the raw-sign construction's O_tilde(w4^w/(kappa^3 epsilon)). The coarse logarithmic-n cost and tournament O_tilde(w/(kappa^2 epsilon)) remain, as does the ordinary encoder O_tilde(1/(gamma epsilon)) term. Collective cross-copy memory and all receiver controls are still paid. The actual statistical conclusion remains averaged loss<=(1+gamma)ell_star+epsilon for ONE recovered logical qubit, conditional on the structural family contract.

This is a refinement, not a generic unflagged-source solution, not a count-acquired experiment, and not a separation from conventional subsystem identification. The simpler expand-once width-(3w−2) construction is still a legitimate competing architecture. A separate independent review is required before treating this addendum as received.
