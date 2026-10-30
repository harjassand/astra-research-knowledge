# Binding derivations for the matching native register
30 October 2026. Independent reviewer `producer-workspace/review_matching_native_register`.

These details are part of the acceptance, not new physical resources.

## 1. Disjoint signed union
Let J(F) be the groups with more than K faulty locations. For a nonempty group subset A, the accepted disjoint sieve gives the actual map

    D_A = sum_{F: A subset J(F)} E_F,   ||D_A||_diamond <= product_{j in A} b_j.

The complete bad map is exactly sum_{A nonempty} (-1)^{|A|+1} D_A. Consequently its norm is at most product_j(1+b_j)-1, and hence (1+b_p)^G-1. This includes fault sets with arbitrarily many bad groups without treating signed coefficients as probabilities. Use x<=1, K=floor(pN/g), and enlarge N0 for rounding. If K+1 exceeds a group's size its b_j is zero; do not apply a negative-power sieve formula to that group. With M<=c_loc N and fixed p>0, sufficiently small fixed x makes b_p exponentially small by the binomial entropy bound. The bath/system model is the finite bounded centered-HP, interval-wise CP-divisible model of the accepted cavity theorem, also during the windows; no infinite-bath extension is implied.

## 2. Full good-map factorization and positive repair
All banks remain system factors. Expand a good fault coefficient only on its finitely supported system legs; arbitrary cross-group bath coefficients remain unbounded in number but no norm is taken on this expansion. Each matched pair has at most gK post-ideal faulty sites. The accepted live-prefix calculation applies to every ket and bra coefficient with the same DATA-independent BUSY masks. Its two-sided KL identities on the common product error module imply the *same joint logical matching unitary* in every coefficient. Taking linear sums preserves this identity. Mere support in the code subspace would not suffice: an undetected logical Pauli is the counterexample.

For the norm repair, write C for compression to the output chart, J for its isometric embedding, and H=Ad_U tensor A_good. Then G=JH, ||Phi-G||<=epsilon_p, and ||C Phi-H||<=epsilon_p. The map R_U(Psi)(X)=Tr_L[(Ad_U^dagger tensor Id)Psi(I_L/d_L tensor X)] is a complete contraction on superoperators, maps CP/TNI maps to CP/TNI maps, and R_U(H)=A_good. Thus

    ||Phi-J(Ad_U tensor R_U(C Phi))|| <= epsilon_p+epsilon_p.

This triangle inequality compares directly against G; it does NOT pass through Phi versus its projection and requires no gentle square root. The common cut is I_L tensor P_aux, so the repaired output has the same auxiliary support. The repair is an analytical comparison, not an implemented depolarization. All restrictions are to the admitted product logical/error chart; they do not extend the initial-bath contract.

## 3. Joint native killed drift
Let P=product_i P_i, and extend F_i by identity on every other bank and bath. The source supplies [F_i,P_i]=0, so [F_i,P]=0. For finite bounded total GKLS dynamics the adjoint killed generator satisfies, on P,

    L_P^*(P F_i P) = P L^*(F_i) P
                         - sum_a P J_a^dagger (I-P) F_i (I-P) J_a P.

The subtracted expression is positive; Hamiltonian cross terms vanish by the commutation. This identity uses a representation of the TOTAL physical generator only for its sign, not to assign a local Kraus norm budget. The native centered local HP system-leg decomposition is used for quantitative estimates. Terms with no system support in bank i annihilate F_i; touching terms have total norm O(eta N), independently of B. The original fixed-cone relative proof therefore supplies rho N, not rho BN. Use the accepted centered perturbation convention throughout (or explicitly receive a centered decomposition with its adjusted fixed noise constant).

Apply the bank-i proof map T_i on the whole positive killed state. It preserves P_i by the accepted branchwise invariance argument, acts trivially on other banks, and preserves their cuts. Scalar spectral Jensen applies to its subnormalized output regardless of correlations. This reproduces the stated logarithmic moment law with the same per-bank warm exponent and stationary floor. No other logical bank has been classified as an unprotected bath.

## 4. First exits cost B, not B squared
An actual bounded system leg changes only a fixed number of canonical syndrome/history variables per touched bank. On P, the per-bank confinement margin excludes radius exits; an exit in bank i must originate in

    R_i = P 1_{E_i >= e_cut N-K_edge}.

The F_i lower bound and warm logarithmic moment give Tr(R_i rho_P)<=C exp(-gamma N), uniformly in time throughout one fixed dwell. Expand each local HP map on its finite SYSTEM legs, as in the actual global proof, before applying cross-block Cauchy--Schwarz. A term with support S can have an outgoing block only at a bank touched by S; all untouched cuts commute through it. Its boundary contribution is bounded by a fixed constant times its complete norm times sum_{i touched} sqrt(Tr(R_i rho_P)). The same accounting covers complete-loss and Hamiltonian pieces via the accepted local boundary construction. Summing incidences gives O(N) per bank and thus O(BN), not a global O(BN) norm times another B-union estimate. Duhamel through the contractive full and killed propagators gives

    ||Phi_dwell-Phi_killed||_diamond <= B C N(1+t_d) exp(-c_mem N).

Exponent c_mem includes the boundary square root. Constants and fixed polynomial prefactors can be conservatively adjusted, but never scale with B. On every retained canonical system leg the source/target representatives and that leg have weight below distance in EACH touched bank. Each such bank's logical action is identity; tensoring gives joint logical identity. This proves the killed map's joint factorization, not merely its marginal fidelity.

## 5. BUSY transfer and endpoint cut
The full-Hilbert bank-i BUSY witness obeys its original drift on the whole register with the same incidence reasoning. At the fixed dwell endpoint the full-state bad-BUSY union has mass at most B exp(-c_B N). Transfer this single bounded union projector to the joint killed state with ONE epsilon_mem comparison. Energy tails on the killed state sum to B exp(-c_E N). Commuting canonical energy and BUSY labels therefore give

    p_cut <= B(exp(-c_E N)+exp(-c_B N))+epsilon_mem.

The actual BUSY witness need not commute the forest or the native cut; no killed BUSY drift is invoked. Only the BUSY count and energy cut need the accepted joint chart commutation. Gentle compression costs at most 2 sqrt(p_cut), uniformly with reference and for subnormalized inputs. Projection is logical-independent, so the killed exact identity factor is retained.

## 6. Fixed cycle and final normalization
Use the jointly chosen small-first-edge family and strict inequalities in the accepted local lemma, not arbitrary pre-existing hardware parameters. All supports, thresholds, tau and dwell are fixed independently of N,B,R. Account for a required initial cooldown from a warm factory source and for whichever final endpoint is requested. The fixed product bare-DATA decoder is applicable at pulse and cooled endpoints via the accepted bounded BUSY forest footprint; it remains ideal analysis/readout.

The manuscript MR5 bounds the actual channel versus a CP/TNI exact-logical comparison. Its normalized logical output requires the binding root normalization addendum: if this bound is E_total, actual trace preservation implies a comparison trace deficit <=E_total. The final diamond error is <=min(2,2E_total). Do not claim MR5 alone is the normalized error. Initial source error is included exactly once before this final comparison.

The polynomial N factor in memory error and square-root union tails are absorbed by sufficiently large constants in N=O(log(BR/epsilon)), for B,R>=1 and nontrivial epsilon. This is an asymptotic existence bound, not a practical threshold/latency estimate. A bounded-degree bank graph need not be geometrically local; only its actual installed edges are supplied. SWAP uses three paid CNOT rounds. No addressability of individual logical coordinates within a bank follows.
