# Global exponential energy for linear-radius autonomous quantum memory
2026-10-30. Root construction candidate, NOT independently accepted. This changes representation for the linear Tanner family instead of extending the connected-animal apparatus unnecessarily. The already accepted animal theorem remains intact.

## 1. Consequential target and earned code input
The target is a composable output with exponentially small probability of leaving a FIXED global correctable Pauli radius. This supports an ordinary fixed decoder and subsequent protected operations, rather than an operation-dependent recovery convention.

Use the accepted code-family input: constant rate, distance d>=delta_d N, a nonnegative integer local energy U=U_X+U_Z, bounded local energy terms/read footprints, and for sectorwise minimum representatives with total reduced weight r(E)<r_dec N,

    U(E)>=h r(E),
    number of active local orbit-minimizing hubs >=kappa U(E).

Every selected nonidentity Phi_h decreases U by at least one; it is idempotent and has bounded support. The opposite CSS sector is unchanged. These are the actual reviewed Tanner/GPT properties, not a new global optimization oracle. Fix r0<r_dec and 2r0<delta_d with strict margins.

Use the SAME explicit native controller architecture: fixed multilevel hub/resource sites, two-site Hamiltonians, onsite resolved resets/monitors, irreversible commit, new DATA-free A_i aborts, weak first acquisition epsilon and later fixed zeta. The finite controller lemmas are retained. Only the proof potential changes.

## 2. One global exponential, with actual bad-history energy
Let B_h be the actual commuting forest-frame history defects. Set

    E=U+R sum_h B_h,
    V=exp(sE),  s>0.

Choose a fixed R exceeding the worst bounded DATA-energy increase of an arbitrary terminal/abort instrument. No physical flag copies are added. E is a sum of bounded local commuting terms, although V is a global mathematical observable.

For any normalized local reset on h's bad source, let K bound the range of the affected DATA energy. Factor out unaffected energy/flags. Positivity gives

    reset^*(V0)<=exp(sK)V0,
    Delta_h=V(B_h=1)-V(B_h=0)=(exp(sR)-1)V0,
    reset^*(V0)-V0<=q_R Delta_h,
    q_R=(exp(sK)-1)/(exp(sR)-1).

Take R and s so q_R<1/4. The bound is for the COMPLETE source-normalized instrument, retains nonmonomial partial circuits and reference entanglement, and can use a conservative fixed affected-energy range. The existing deterministic-syndrome clean-image argument removes terminal good/dirty cross blocks.

Also, exactly

    B_h Delta_h=(1-exp(-sR))B_h V.

Thus dirty service is a direct bad-count charge, with no animal completion or entropy multiplicity.

## 3. Local DATA decrements simplify
On a definite raw syndrome,

    d_h=(I-Phi_h^*)V=[1-exp(-s Delta U_h)]V>=0.

If h is active, d_h>=(1-exp(-s))V. Hence in the global safe-radius region,

    sum_h d_h>=kappa(1-exp(-s)) U V.                 (1)

For a correction j, inactive j has zero action. On active j both V and every d_h after j are bounded by a fixed multiple of V before j (indeed V itself decreases). Therefore the bounded overlap estimates used by the clock compiler follow directly, for example |Delta_j d_h|<=C_s d_j and Delta_h d_j<=C_s d_h, with fixed local C_s. Disjoint terms cancel as before. No connected-container hypothesis is needed for (1).

## 4. One global positive controller weight
Use the controller-only, B-pinched activity witnesses and guarded pair/singleton gates already constructed, but select ALL their anchors once. Let Y be their fixed-depth ordered product and G=Y^dagger Y. Then

    I<=G<=exp(gN)I,  g<=C delta(B0+A0 epsilon^2),
    [G,U]=[G,B_h]=0.

Set V_G=GV. Because the same G is used for every term,

    (I-Phi_h^*)V_G=G d_h>=0.

On the clean range the generator product rule separates controller drift from DATA recovery. Each recovery DATA contribution is J_clock^dagger G J_clock times (Phi_h^*V-V), and is NONPOSITIVE individually. There is no need to make individual connected-animal factors decrease. The reviewed activity drift therefore multiplies V directly:

    L_clean^*V_G <=[-a delta A0 epsilon^2 sum P_h
                    -b delta B0 sum_pairs P_hP_j
                    +C delta A0 epsilon^4 N]V_G,

before retaining the useful DATA credit.

The negative ready-opening coefficient also needs no singular-K animal comparison: controller Y and K commute DATA/flag d_h, so Y^dagger K Y d_h>=0 whenever K>=0.

## 5. Exact native useful/dirty transfer, with extensive rather than animal remainder
Retain the analytic guarded useful maps Q_h, the exact C-block terminal cancellation, and the actual weak-initiation block orders. Use T_t=product[Id+t(Q_h-Id)] with t=c epsilon^2. Its local inverse is only a linear algebra tool. Exact finite-depth similarity has local remainder O(t^2).

Retain the correctly ordered dirty CP erasures T_B,h and their full triangular inverse. Recompute the bad resolvents for the actual A_i aborts. Guard every active proof factor near an actual bad flag. On B_h=1, the nearby gates are identity and the remaining GLOBAL cavity G^h commutes h's own map. Healing activates only O(1) gates. Unlike the animal proof, every bad-side relative error is directly bounded by C delta B_h V_G and paid by B_h Delta_h=(1-e^-sR)B_h V. Buffered Q_X<=sum_(h near X)B_h gives the same direct charge. Clean/dirty cross blocks cost O((t+delta)^2)N V_G. The complete inverse/forward activation terms remain included; no inverse positivity is assumed.

All local relative bounds use that a fixed-support operation changes E by at most a fixed constant. Conjugating through the fixed-depth controller circuit keeps local norms bounded, so summing remainders costs N V_G, not an extensive global operator norm exponential in N.

The proposed exact effective drift, to be checked against every reused source identity, is

    L_eff V_G <= -lambda E V_G+rho N V_G,            (2)

where lambda>0 is of order c b_min epsilon^4 times the active-density constant, and

    rho <= C[t^2+t delta+(t+delta)^2
             +delta A0 epsilon^4+t^2 epsilon^4/delta]

after activity budgets are allocated. Strong dirty service pays the R sum B part of E; lower lambda if needed. Set delta=d epsilon^2, choose d/c sufficiently large for busy/collision absorption, then c small so rho/lambda is as small as the desired macroscopic energy margin. Finally epsilon small controls the higher-order terms. This is the load-bearing new controller specialization, not assumed proved merely because the animal version passed.

## 6. Positive pullback and nonlinear scalar moment law
Let T=T_B T_t and F=T(V_G). For physical continuous noise with fixed body size and small per-site incident joint cb-norm sum, the local relative/dilation bound is

    N^*F<=C_noise eta N F.

It needs no fixed noise-partner graph. Absorb this into rho. Positive pullback gives

    L_phys,noisy^* F<=-lambda T(E V_G)+rho N F.       (3)

Because G commutes E, log V_G=sE+log G and 0<=log G<=gN. For any positive subnormalized killed state rho_P, put sigma=T_*(rho_P), x=Tr(F rho_P)=Tr(V_G sigma). Scalar Jensen in the spectral measure of V_G gives

    Tr[V_G log(V_G) sigma]>=x log(x/Tr sigma)>=x log x.

Thus no operator Jensen or commutation of rho_P with V_G is needed, and

    Tr[T(E V_G)rho_P]>=(x log x-gN x)/s.

Equation (3) yields

    d log x/du <=-(lambda/s)log x+(rho+lambda g/s)N,
    log x(u)<=nu N+[log x(0)-nu N]exp(-lambda u/s),
    nu=g+s rho/lambda.                              (4)

The limiting exponential-moment coefficient nu can be made smaller than a prescribed fixed energy barrier by the parameter choices above. This is a macroscopic-energy moment law, not global trace mixing of logical information.

## 7. A simple global code basin and fixed output radius
Use the canonical minimum representatives and define

    P={r(E)<r0 N,  E<e_cut N},

with e_cut<h r0/2. At sufficiently large N, a bounded local Pauli cannot leave the reduced-weight radius from this energy sublevel: the source has r(E)<=U/h<=E/h<r0N/2, and the target minimum weight grows by only a fixed local amount. The source and target representatives and local Pauli have total weight below distance, so their canonical logical action is identity.

Therefore exits must cross the ENERGY cutoff. A fixed local term changes E by at most K_noise, so exit-source energy is >=e_cut N-K_noise. Selected dirty no-jump and useful Id branches give a global lower comparison

    F>=exp(-ell_credit N)V,

where ell_credit can be made small by the mathematical dirty-credit coefficient and t. The upper comparison is F<=exp(gN)V, since both outer maps lower RAW V. Encoded/ready initialization thus has x(0)<=exp(gN).

Choose physical/proof constants so

    nu+ell_credit<s e_cut.

Then (4) bounds killed boundary mass by exp(-cN). The actual O(N) joint-generator norm budget and Duhamel comparison give an exponentially small logical error over exponentially long times. The full process has the usual fixed-bath/encoded-input/ideal-frame qualifications.

Every killed output lies in total reduced weight <=e_cut N/h. Choosing e_cut below the ordinary recovery radius supplies a FIXED globally correctable span, not just a convenient operation-dependent decoder. The same scalar law accommodates an earned warm input with log x(0) below the barrier and contracts its extensive moment coefficient in constant time.

## 8. Noncircular choices and scope
Choose code/payload and fast controller rates; actual bad matrices with new aborts; R,s and target code energy margin; a small dirty proof coefficient so ell_credit is below that margin; later zeta; actual activity supports and isolated useful coefficients; then c,d,epsilon and eta using the finite local bounds. All are fixed independently of N. The final proof must spell out simultaneous constraints, not assume any particular parameter is independently favorable.

This candidate is specialized to a LINEAR global correction radius. It does not replace the animal machinery for sqrt(N)-radius codes or spatial-cluster statements. It does not prepare encoded DATA, implement noisy extraction, prove a practical threshold, or guarantee arbitrary initial logical/bath correlations. Its intended advance is a simpler composable autonomous-correction theory with direct macroscopic error control and no fixed noise topology.
