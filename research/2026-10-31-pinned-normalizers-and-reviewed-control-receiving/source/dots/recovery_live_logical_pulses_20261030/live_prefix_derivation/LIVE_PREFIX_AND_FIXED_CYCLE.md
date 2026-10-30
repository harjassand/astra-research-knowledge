# Live native prefixes through selected transversal CNOT: deterministic constants and closed cycle
30 October 2026. Construction agent derivation. This is not a review receipt. Extends the root candidate only at its live-prefix and relaxation seams; root supplies the joint-register CP-cavity matching construction.

## 1. Actual imported structure, not clean-controller initialization
Read directly: `producer-workspace/GLOBAL_EXPONENTIAL_COMPILER.md` §§2,4–7; `producer-workspace/DIRECT_SINGLETON_DERIVATION_V1.md`; `producer-workspace/WHOLE_RECEIPT.md` §§3–5 and its actual-source receipt. The first document's originally proposed inequalities are imported only as subsequently accepted by the governing global-memory receipt, not on their original candidate status.

Native energy is E=U+R sum B_h. In the common canonical basin, U>=h r, where r is the SUM of minimum X- and Z-sector weights. A physical Pauli on m DATA sites contributes at most 2m to this convention. Actual history-bad B_h is subordinate to the stronger BUSY_h. The actual forest preserves BUSY masks/count; on a fixed coherent mask its nonidentity factors have DATA support in the union of full footprints of its BUSY owners. Let f bound one full owner DATA footprint. These facts apply on malformed histories: they do not require a completed controller or a DATA-independent activity witness.

Let a=c_act bound the number of full readiness predicates whose controller/tag support can meet one physical site. The strong-ready predicate is DATA-independent. Let c_U>0 bound raw Tanner energy per canonical CSS weight; all constant baseline terms are zero relative to the target code. All constants refer to the unchanged actual native machine.

## 2. Deterministic live-prefix receiving lemma
Start a matching edge with each bank in the coherent common logical-error span r<=r_in and M_BUSY<=m_in. Retain arbitrary coefficients on apparatus/bath/reference. Freeze every native generator during the pulse; intended pulse acts only on DATA components of resource sites. Its exact unitary is transversal CNOT. Let the *good* pulse coefficient have faults on at most ell physical resource sites in the whole matched pair, after propagation through the remaining intended disjoint gates. Thus ell already counts the two-site gate-block enlargement; do not charge it a second time. A CP-cavity bad-location coefficient can be converted to this form with ell<=g k for g-site blocks (g=2 for CNOT, idle sites may be padded).

For EACH output bank:

    b_out_count = m_in + a ell,
    r_out_count = 2 r_in + 6 f m_in + 2(1+f a) ell,
    E_out_count = c_U r_out_count + R b_out_count.          (1)

Proof by coefficient spans, not expectation. The initial forest in each bank adds at most 2f m_in CSS weight. In a transversal CNOT, the output CSS weight on either one bank is at most the SUM of the two input CSS weights. This follows separately from x_c'=x_c, x_t'=x_t+x_c, z_c'=z_c+z_t, z_t'=z_t over F_2; cancellations only lower support. Hence before new faults the bare output weight per bank is <=2r_in+4f m_in. Faults add <=2ell. Intended DATA-only gates preserve every readiness predicate; faults can affect at most a ell additional owners. The final inverse of the SAME native forest adds <=2f(m_in+a ell). Summing gives (1), and history energy follows from B<=BUSY and U<=c_U r. No physical forest inverse is performed.

Every statement holds coefficientwise on its own owner/fault support; coherent sums remain in the same bounded common span. One must not take the union of all masks. Controller operations in the forest preserve the masks. An idle bank satisfies the same bounds conservatively. The new logical target is the actual global matching of transversal encoded CNOTs, acting on all corresponding logical coordinates. Canonical re-expression has no unintended logical action when the bounds lie strictly within the common KL radius.

## 3. Positive warm source, with no expectation-to-support leap
Set r_in=eN/h, m_in=bN and ell=pN. Define

    d = 2e/h + 6fb + 2(1+fa)p,
    b_+ = b+ap,
    E_+ = c_U d + R b_+,
    w_E = g+s E_+,       w_B = 2C_B delta_B b_+.

Require d<r0 and E_+<e_cut. The exact common-error-span projector onto the intended logical module, r<=dN, BUSY<=b_+N, E<=E_+N is applied only virtually to the ACTUAL positive output. The CP-cavity good coefficients lie in it; the signed bad-map norm bounds its actual leakage, followed by a gentle bound. It is not legitimate to treat the signed good map itself as a positive state. Both projector and witness must be conjugated by the SAME canonical forest.

The virtual projection alone does NOT imply exact intended logical factorization: a small bad-map component may already lie inside the code as a wrong logical operator. Retain that error explicitly. In the fixed coherent KL chart, conjugate away the intended logical unitary and write the projected actual CP/TNI map as Psi, with signed good reference Id_L tensor A_good and complete-norm discrepancy <=zeta (including pulse bad-map and gentle-projection costs). Define the CP/TNI auxiliary map

    A_pos(X)=Tr_L Psi((I_L/d_L) tensor X).

The finite logical input embedding and output trace are complete contractions, so ||A_pos-A_good||_diamond<=zeta and

    ||Psi-Id_L tensor A_pos||_diamond<=2zeta.

Restore the intended logical unitary. This supplies a genuine positive factorized restart map, not a claimed positivity of the signed good expansion. The auxiliary output remains in the SAME allowed radius/history/BUSY label support because the projected actual output was supported there and the KL syndrome-label cut is logical-independent. This is an analytical complete-norm replacement, not a physical depolarization or trace operation. If only a fixed auxiliary input is in use, the same construction gives its positive auxiliary state. Joint-register use must use the full register KL chart, not marginal bank charts.

The true spectral envelope F<=exp(gN)exp(sE) then gives P F P<=exp(w_E N)P; similarly G_BUSY<=exp(2C_B delta_B M_BUSY) gives the warm BUSY moment exp(w_B N). No Jensen upper bound from mean E is used. The witness G_BUSY need not commute with the forest; only its count does.

## 4. Exact energy and BUSY relaxation
The accepted positive pullback has F=T(V_G), V_G=G exp(sE), [G,E]=0, 0<=log G<=gN, and

    L*F <= -lambda_E T(E V_G) + rho_E N F.

For a positive subnormalized killed state rho, sigma=T_*(rho) is positive and has mass<=1. With x=Tr(V_G sigma), scalar spectral Jensen gives Tr(V_G log(V_G) sigma)>=x log(x/Tr sigma)>=x log x. Hence

    a_E=lambda_E/s,   nu_E=g+s rho_E/lambda_E,
    log Tr(F rho_t)/N <= nu_E+(w_E-nu_E) exp(-a_E t).       (2)

This is entropy relaxation of a moment, not trace mixing. Lower F>=exp(-q_t N)exp(s' E) gives the killed energy-cut tail at E>eN:

    exp(-[s'e-q_t-nu_E-(w_E-nu_E)e^(-a_E t)]N).            (3)

Separately the original unpinched full-Hilbert singleton BUSY witness obeys

    exp(2c_B delta_B M)<=G_B<=exp(2C_B delta_B M),
    L*G_B<=-lambda_B G_B log G_B+rho_B N G_B,
    rho_B=C delta_B epsilon^2+C_noise eta.

Its proof permits fixed sufficiently small analytical delta_B independently of the global proof's delta=d epsilon^2. Scalar Jensen with subnormalized mass yields

    nu_B=rho_B/lambda_B,
    log Tr(G_B rho_full,t)/N<=nu_B+(w_B-nu_B)e^(-lambda_B t). (4)

Thus the full-state BUSY tail at M>bN is exp(-[2c_B delta_B b-nu_B-(w_B-nu_B)e^(-lambda_Bt)]N). Transfer it to the same positive killed state through full-versus-killed complete norm error, then jointly cut the commuting canonical energy/BUSY labels. Do not infer a G_BUSY drift for the killed dynamics unless its required basin commutants are separately proved. The gentle errors are exponential, with exponent halved as usual.

## 5. Explicit strict feasible budget and fixed dwell
Fix fast hardware, code, s,R,s',e_cut,r0,h,c_U,f,a. Take

    A_e=2c_U/h,
    A_b=6c_U f+R,
    A_p=2c_U(1+fa)+Ra,
    alpha=min(s'e_cut/(4s), c_U r0/2),
    e=alpha/[3(A_e+1)], b=alpha/[3(A_b+1)], p=alpha/[3(A_p+1)].

Then E_+=A_e e+A_b b+A_p p<alpha, d<=E_+/c_U<r0/2, and s E_+<s'e_cut/4. These choices are conservative and strictly positive.

Use the accepted simultaneous small-parameter family: choose global proof ratios to make s rho_E/lambda_E sufficiently small, then epsilon sufficiently small to make g,q_t small AND the BUSY epsilon^2 floor small, then choose eta below all positive energy/BUSY/pulse thresholds. In particular enforce

    g+q_t < s'e/4,
    s rho_E/lambda_E < s'e/4,
    nu_B < c_B delta_B b,
    g+q_t < s'e_cut/4.

The energy source rho_E includes noise; select eta after positive lambda_E is fixed. Thus nu_E+q_t<s'e/2 and max(w_E,nu_E)+q_t<s'e_cut/2 (since e<e_cut). Warm burn-in is inside the SAME memory barrier with a fixed coefficient gap. The pulse strength condition must also make the CP-cavity bad-group tail at ell=pN exponential. None of these constants depends on N, bank count or command length.

Let T_E=s'e-q_t and T_B=2c_B delta_B b, with positive gaps. Choose

    tau_E = (1/a_E) log max(1, 2 max(0,w_E-nu_E)/(T_E-nu_E)),
    tau_B = (1/lambda_B) log max(1, 2 max(0,w_B-nu_B)/(T_B-nu_B)),
    tau_cool = max(tau_E,tau_B).

Equations (3),(4) then have gaps at least gamma_E=(T_E-nu_E)/2 and gamma_B=(T_B-nu_B)/2. Floors below thresholds, warm barrier, postgate support and pulse tail are ALL strict simultaneous conditions. A fixed cycle is tau_gate+tau_cool (plus any separately proved paid ramps); abrupt bounded scheduled switches produce no state impulse and need no ramp term. No reset, re-encoding, fresh apparatus, frame program or outcome-dependent dwell is used.

## 6. Composition boundary and failures excluded
This note alone does not justify treating other logical banks as arbitrary bath. For the joint register use the root's full-matching CP-cavity fault expansion, all native generators OFF in the pulse, disjoint matching-pair/idle groups, and per-bank joint killed cooling cut. Per-bank moments commute other banks' basin cuts, so conditional positivity removes outgoing gains and preserves each energy inequality; the errors sum over bank-time. Never use a global BN-radius code ball: the tensor-product bank code has distance only O(N).

One pulse's support inequality does not alone permit repetition: without (2)–(4), repeated r->2r would exhaust the basin. Nor does a small expected E certify the warm support. Neither signed low-order Dyson maps nor marginal bank fidelities certify a positive joint logical channel. These are counterexamples to the corresponding shortcuts, not failures of the explicit closed cycle above.

## 7. Direct structural and rate-source checks (additional evidence)
The actual `producer-workspace/FULL_HILBERT_FOREST_GAUGE.md` §§1–3 constructs F_h as a clock/lock block diagonal unitary V_t(m), identity in A,Q,R(A),R(Q), nontrivial only on private W_h and resources actually tagged o_h. Different owners' factors commute because owned resource blocks are orthogonal. This proves the mask support needed in §2 directly. At A0 the forest is identity, hence preserves W0 there; all other nonidentity clock sectors are already BUSY. It fixes tags and clock labels. Therefore it preserves each strong-ready predicate, including malformed sectors, rather than only its total count. All strong-ready A0/W0/no-own-tag configurations are history-good; hence B_h<=BUSY_h. The unified generator's later complete A_i aborts do not alter this static forest.

The actual `producer-workspace/GLOBAL_EXPONENTIAL_CONTROLLER_INTERFACE_CANDIDATE.md` §6 provides the quantitative simultaneous family used above:

    t=c epsilon^2, delta=d epsilon^2, d=r c,
    lambda_E=min(a_U c epsilon^4,a_B/R),
    rho_0/lambda_E <= C_s(c+d)^2/(c a_U)+O(epsilon^2).

Fix r for activity reservations, then reduce c: the displayed leading ratio is C_s c(1+r)^2/a_U and tends to zero. Next epsilon makes q_t=O(c epsilon^2), g=O(d epsilon^2) and the higher-order remainder small; independently it reduces the singleton BUSY floor. Noise contributes C_noise eta to rho_E and rho_B; choose eta only after these positive fixed rates and margins have been fixed. This proves the proposed hierarchy does not try to independently vary incompatible hardware rates. It can yield extremely long fixed cooldown, since lambda_E is small; no practical latency bound is claimed.
