# A paid weak-coupling deformation, and what it does not buy

The accepted source supports an arbitrarily small **average** coupling to a full-rank product state by a new, explicit, classically flagged dilation. It does not support arbitrary direct depolarization of its original baseline with the original signed witness intact. The flagged dilation has an exactly computable positive margin, but its rare hard branch is not weakly coupled in relative operator norm. In the square-root encoder it produces a lazy identity step, not a reset. It therefore does not close the lead's ordinary-capacity rate inequality.

All statements below retain the existence-only finite hard witness dimension. In particular, neither the deformation nor its constants acquire or bound that dimension.

## The actual N675 object

Use the notation of N675 Sections 12.1–12.3, printed/PDF pp. 22–23, equations (66)–(71). The physical input has dimension n=a+q0, where a=2MK, L is the compiler node count, and q0=ceil(L/a). Put q=max(a,q0). The game-computable parameters are

    gamma=1/4,
    e=min(1/2, gamma/(8 max(1,Bdeg))),
    Bdeg >= sum_w |w| |c_w|,
    lambda>0, delta_s>0.

For a finite perfect maximally entangled strategy of unknown local dimension ell, the actual source takes

    Re=(1-e)R0+e (I_a/a) tensor I_ell,
    Se=(1-e)S0+e (I_a/a) tensor I_ell,
    Reff=Re directsum Se,
    Tlow=e I_q0 tensor I_(2ell)/(2q0),
    Rtop=Reff-e I_a tensor I_(2ell)/(2a),
    Theta0=diag(Rtop,Tlow),
    rho=Theta0/(2ell), H=X/sqrt(ell).

Here X has physical top-to-bottom cross blocks, with word-coordinate matrices in the upper-right block of the old reference C^ell directsum C^ell. They are constructed from the root vec(I_ell)/sqrt(ell), and their operator norms are at most sqrt(2)/sqrt(ell). Thus, writing D_old=2ell,

    rho_R=I_(D_old)/D_old,
    l I/D_old <= rho <= u I/D_old,
    l=e/(2q), u=a,
    ||H|| <= 4L/D_old,
    -h rho <= H <= h rho, h=8Lq/e,
    Tr H=0.

For the source and target measurement channels E,F, respectively,

    g_(F rho)(F H)-g_(E rho)(E H) >= d0,
    d0=delta_G=4 delta_s^2 gamma/lambda>0.

Every source output block is between alpha_eff I/D_old and I/D_old for a game-computable positive rational effect lower bound alpha_eff; hence kappa=1/alpha_eff is dimension independent. This is the accepted source's normalization, with no unknown factor D_old removed by assumption.

Let Z_old be +1 on the first old-reference copy and -1 on the second. The actual object satisfies

    [Z_old,rho]=0,  Z_old H Z_old=-H.

This parity is retained by every flagged deformation below. It is not removed by making its weight small.

## The entropy constant can be paid before dilution

N675 Lemma 13.1, pp. 24–25, equations (72)–(74), gives the following explicit constants from h,kappa,d0:

    m=max(6,ceil(288 kappa^2 h^4/d0^2)), N=2m+1, r=N+1,
    lambda_j=1+j/m^3, j=0,...,2m,
    c_j=(-lambda_j)^m / product_(k!=j)(lambda_k-lambda_j),
    Lambda0=sum_j |c_j|,
    qstar=h kappa Lambda0,
    jstar=5^(-(4m+2))/N,
    eta=min(1/4,jstar d0/(16 qstar^2)),
    t0=min(1/(2qstar),3 jstar d0/(256 qstar^3)),
    epsilon0=jstar d0 t0^2/16>0.

On the filter centre and N leaves,

    W=diag(1,lambda_0,...,lambda_(2m)), Z=Tr W,
    v=N^(-1/2) sum_j e_(j+1), w=sum_j c_j e_(j+1),
    tau=vv*, L_F=e0 w*+w e0*,
    sigma=(1-eta)tau+eta I_r/r,
    alpha=rho tensor sigma,
    beta=(rho tensor W+t0 H tensor L_F)/Z.

These are faithful states, beta>=alpha/(2Z), and their F-minus-E relative-entropy defect is at least epsilon0. The filter is finite and computable from game constants; it does not make the old hard reference finite dimension computable. All these entropy formulas use the source's logarithm convention. If a numerical bound is wanted in bits, a conservative rational lower bound is the same displayed positive epsilon0, since 1/ln(2)>1.

The physical doubling used in N1677 is Xi=diag(rho,rho)/2 and Htilde=[[0,H],[H,0]]/2. It preserves the SLD signal and the relative bound h. This exact formula is in the complete N1677 visible response, lines 130–201; it is also the doubling retained by N1680 Section 3. For a genuine receiver/environment pair, use its accepted, computed transported Fisher/entropy constants rather than silently identifying them with the measurement-pair constants above.

N1680 Section 3 (complete available visible response, lines 1406–1673) identifies the discrete obstruction and gives the repair: move T0=Q_old F into the physical input, and use the actual channel

    Ctilde=C tensor E_(2r,1/2).

The new physical factor has computable dimension 2r. The unknown remaining reference has D=ell and marginal I_D/D. Since Tr L_F=0, the erased-T0 branches have identical alpha and beta. The actual, exact repair factors are

    Delta_D(Ctilde,R0)=Delta_D(C,T0 R0)/2,
    Delta_chi(Ctilde,R0)=Delta_chi(C,T0 R0)/2

for every binary prior in the second identity. The old enlarged physical marginals need not agree. If the pre-repair complementary construction has its N1680 computable entropy margin delta>0, the repaired margin is delta/2; it is not delta, and it does not establish an ordinary capacity rate.

## Explicit flagged dilution

This construction applies either to (rho,H,E,F) before the filter, or to the repaired physical receiver/environment construction and its entropy pair. Let A be the physical input at that stage, dim A=n, let the remaining reference have unknown dimension D, and suppose

    omega_R=pi_D=I_D/D,
    l I/D <= omega_AR <= u I/D,
    -h omega <= H <= h omega.

The actual source above has such computable l,u. The filter, doubling and repair also retain them, with changed computable constants; no spectral bound depending on a numerically supplied D is needed.

Choose any rational 0<s<1 and tau_A=I_n/n. Introduce a physical classical flag J of dimension two and define the ordinary states and tangent

    omega_s = s |0><0|_J tensor omega_AR
              +(1-s)|1><1|_J tensor tau_A tensor pi_D,
    H_s = s |0><0|_J tensor H.

There are no off-diagonal flag blocks. The state is full rank for every s>0. Its reference marginal remains pi_D, and

    l_s I/D <= omega_s <= u_s I/D,
    l_s=min(s l,(1-s)/n)>0,
    u_s=max(s u,(1-s)/n),
    -h omega_s <= H_s <= h omega_s,
    ||H_s||=s ||H||.

The full-rank product comparator is

    sigma_s=(omega_s)_(JA) tensor pi_D.

Because omega_A and omega_AR obey the same scaled lower/upper bounds,

    D ||omega_s-sigma_s||_op
        =s D ||omega_AR-omega_A tensor pi_D||_op
        <=s(u-l),
    ||omega_s-sigma_s||_1
        =s ||omega_AR-omega_A tensor pi_D||_1 <=2s.

Thus given any rational tolerance zeta>0, taking a rational s<=min(1/2,zeta/(1+u-l)) gives an explicit D-scaled operator-norm error below zeta, independently of unknown D. The trace-norm estimate is even independent of n and the spectral constants. Also I(JA:R)_(omega_s)=s I(A:R)_omega, if this alternative coupling measure is useful.

The full-rank product comparator degenerates as s tends to zero: its hard flag has probability s. This is **not** a deformation into a fixed uniformly faithful product neighbourhood. The following cancellation shows exactly where its hard content remains:

    ||sigma_s^(-1/2)(omega_s-sigma_s)sigma_s^(-1/2)||_op
      =||(omega_A tensor pi_D)^(-1/2)
          (omega_AR-omega_A tensor pi_D)
          (omega_A tensor pi_D)^(-1/2)||_op.

It is independent of s. In particular this method does not produce arbitrarily weak relative coupling or a bounded s-independent condition number. Its l_s can shrink linearly in s. A bound derived only from the new spectral extremes, u_s/l_s, can grow as 1/s. The actual blockwise domination is better: omega_s<=max(1,u/l) sigma_s, with the same old correlation bound for all s. That bound does not approach one; the hard-branch relative correlation is unchanged. Neither estimate supplies cyclic entanglement recovery or a forgetting theorem.

### The physical channels, rather than an assumed preserved witness

For a measurement pair P,Q, define P_s,Q_s to measure the input flag, apply P or Q in flag zero, and produce the same fixed output in flag one. Both outputs include the measured flag. In POVM notation their hard effects are |0><0| tensor P_i or |0><0| tensor Q_i, and their common filler effect is |1><1| tensor I_A. This is an explicit rational CPTP pair. Its effects need not be strictly positive on the enlarged physical input, so it is an extension of the accepted source object rather than an assertion that it retains that particular POVM-format restriction.

If using N1680's genuine physical channel Ctilde, wrap it as the direct-sum channel C_s which uses Ctilde on flag zero and a common self-complementary dephasing channel D_A on flag one. An actual Stinespring isometry is

    |0>_J |psi>_A -> |0>_(J_B)|0>_(J_E) V_Ctilde |psi>,
    |1>_J |a>_A   -> |1>_(J_B)|1>_(J_E)|a>_B|a>_E.

The branch spaces are orthogonal direct sums. This is computable with rational Kraus matrices from the original rational Kraus description. No quantum reference wire has been transmitted. Flag coherences vanish in both actual complementary outputs, and the filler channel is exactly self-complementary. Both receiver and environment have the physical branch record. Thus the no-case complete environmental order is preserved: apply it to each conditional hard input block; the filler defect vanishes and the same classical branch-weight contribution cancels. Subnormalized relative entropy obeys D(p rho||q sigma)=p D(rho||sigma)+p log(p/q), so this proof also handles unequal branch probabilities in arbitrary tested state pairs.

SLD homogeneity is g_(s A)(s K)=s g_A(K). Consequently the exact signed Fisher difference of (omega_s,H_s) under this wrapper is s times its original value. In particular the N675 measurement margin becomes s delta_G, with h unchanged. For that measurement pair the enlarged output condition number is bounded explicitly by

    kappa_s=max(s,1-s)/min(s alpha_eff,1-s).

Every hard outcome has eigenvalues in [s alpha_eff/D,s/D] and the filler output is (1-s)I/D, proving the bound. If it is preferable to perform entropy conversion after dilution, Lemma 13.1 can be rerun with d0_s=s delta_G and kappa_s. That produces much worse constants unnecessarily.

Instead dilute the already constructed entropy pair, using a single common faithful product filler chi=tau_A tensor pi_D:

    alpha_s=s|0><0| tensor alpha+(1-s)|1><1| tensor chi,
    beta_s =s|0><0| tensor beta +(1-s)|1><1| tensor chi.

Here A includes every already-paid physical factor; after the N1680 repair both alpha_R and beta_R equal pi_D. Direct-sum relative entropy gives exactly

    Delta_D(alpha_s,beta_s)=s Delta_D(alpha,beta),
    Delta_chi(same binary prior)=s Delta_chi(original binary prior).

The source measurement entropy margin is therefore s epsilon0. The margin of N1680's repaired actual complementary channel is at least s delta/2. There is one attenuation power s and the already-required repair factor 1/2. No logarithmic branch penalty is lost: the two letters have the same branch weights. The domination beta>=alpha/K survives with the same K>=1 since the filler states agree. Each diluted letter is O(s) close to its own physical-marginal product state by the preceding estimates. This is an exact finite-dimensional algebraic construction for every supplied witness, not an algorithm for acquiring the hard witness.

## Why neither direct depolarization nor memory forgetting follows

For the original fixed N675 POVMs, direct mixing of the Choi baseline toward its product baseline scales each centered source letter T by 1-e at the fixed marginal. Equation (68) only guarantees

    <z,F(T_e)z> <= -gamma+e Bdeg,

with e chosen small in (66). It does not preserve negativity as e tends to one. Replacing F(T) by a rescaled polynomial F(T/s) would require a new soundness argument on all actual normalized Jordan-domain instances: T/s is not generally in that domain. Thus this rescaling is not a legitimate inherited no-case proof. The accepted theorem and its fixed e remain intact; the missing arbitrary-depolarization assertion is simply not a supplied premise.

More decisively, small average correlation is not a reset in the actual N1680 square-root memory interface. Its Kraus matrices are

    K_af=sqrt(D) [sqrt(omega_AR)]_af.

For omega_AR=tau_A tensor pi_D,

    K_af=[sqrt(tau_A)]_af I_D,
    M_product(X)=sum_af K_af X K_af*=X.

This identity holds for every memory operator X, not merely for its stationary marginal. A product baseline leaves all hidden memory intact. For the flagged omega_s, the square root has the same physical flag blocks, so the resulting memory channel is exactly

    M_s=(1-s) id+s M_omega.

Every eigenvalue lambda of M_omega becomes 1-s+s lambda. If the original has a nontrivial invariant memory operator, it remains invariant. Even if a spectral gap exists, this construction introduces no computable dimension-independent lower bound for it. It usually slows relaxation. This interface does not turn O(s) trace-norm coupling into O(s) memory persistence.

Finally, flagging retains [Z_old,omega_s]=0 and Z_old H_s Z_old=-H_s. In the unrepaired encoder, the one-insertion emitted derivative remains the trace of an odd memory operator and hence vanishes. The flag cannot cure that N1680 parity obstruction. The explicit paid Q_old F erasure repair can cure the identified observable-signal loss, but it still does not imply the missing uniform entropy-rate/history inequality or an ordinary capacity lower bound.

## Source locations and finite check

Originals were read in place, without recovering held attachments:

- N675: `updates/DG/package/channel_order_undecidability/channel_order_undecidability.pdf`, via its supplied `EXTRACTED_TEXT.txt`; pp. 16–17, eqs. (51)–(54), for the physical cross tangent/effective baseline; pp. 22–23, eqs. (66)–(71), for the normalized actual witness and constants; pp. 24–25, eqs. (72)–(74) and Lemma 13.1, for the effective entropy filter. Text lines 1327–1419 and 1422–1541 contain the main formulas reproduced here.
- N1680 complete available visible response: `research/2026-11-03-p1-ordinary-capacity-resource-interface/source/p1/COMPLETE_VISIBLE_RESPONSE.txt`, Section 3, lines 1239–1419 for normalized bounds/filter and old-reference structure, lines 1420–1676 for parity and paid half-erasure repair; Section 4, lines 1798–1923 for the square-root memory encoder. The text extraction loses some square-root glyphs, but the stated two Kraus-normalization identities determine the intended square-root formula, and it is the square-root encoder explicitly named in Section 3.
- N1677 complete available visible response: `research/2026-11-03-p1-symmetric-assistance-return/source/p1/COMPLETE_VISIBLE_RESPONSE.txt`, lines 130–201, for the explicit physical doubling retained by N1680.

`check_flagged_dilution.py` is a finite numerical diagnostic of the new algebra, using a noncommuting 2-by-2 reference example and unsharp rational Pauli measurements. It checks Fisher and entropy scaling, both norm identities, relative-norm non-attenuation, full rank, and the exact lazy-memory-channel identity at s=1/2,1/8,1/1024. It passed with maximum absolute error 4.45e-16; actual output is in `check_results.json`. It is not a hard-game witness acquisition, a test of N675's accepted reduction, or a capacity calculation. The equalities above have their direct-sum/homogeneity proofs independently of the diagnostic.
