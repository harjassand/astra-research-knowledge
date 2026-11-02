# A zero-gain receiver fusion: high exit, double-low activation, joint drainage and the mixed-sign large-residual region

**Result and limitation.** This note proves a new *joint* actual stopped law for a single globally proper receiver on an explicitly described noncompact union of four regimes, including a newly proved full-generator mixed-sign large-residual region. It does **not** establish positive recurrence for the unrestricted six-species process. Its essential new step is that the source-resolved joint cleanup/drain from `POSITIVE_UNPAIRED_JOINT_CLEANUP.md` can be tuned to give an **arbitrarily prescribed linear-in-population surplus in Sol's high-region quadratic receiver**. That surplus absorbs the entire actual low-low-corner Green correction, including at both input and output. A count-charged switching lemma then composes arbitrarily many crossings with coefficient one.

## 1. Exact setting, source scopes and units

The six species and ten mass-action channels are exactly the ones in the principal's problem. Write `M=A+B+C+D+E+F`, `r1=B-C`, `r2=E-F`, `q=C+F`, `B0=alpha0+beta0`, and `q_nc` for the sum of all eight *block* propensities. The full process is taken to be nonexplosive as explicitly accepted by the programme. Every actual core event is retained.

We use the high potential from `PROPER_HIGH_ANCHOR_RECEIVER.md` and `JOINT_AXIS_FOUR_EVENT_THEOREM.md`:

    t1=min(B,C), t2=min(E,F),
    O=(t1 mod 2)+(t2 mod 2), J=floor(t1/2)+floor(t2/2),
    Psi=3(r1)_+ + 3(r2)_+ + a_w(-r1)_+ + a_w(-r2)_+ + 2O+J,
    h1=|r1|+3t1/2+(t1 mod2)/2, h2=|r2|+3t2/2+(t2 mod2)/2,
    g1=(A-h1)_+, g2=(D-h2)_+,
    U=eta1*g1^2+eta2*g2^2 + C*(Psi+c0)^2.

Here `a_w,C,c0,eta1,eta2` are fixed positive raw constants satisfying those *earned* high-region theorems; choose the `eta` ratio required by the exact four-event axis theorem. `Psi` is preserved by **both core directions** at every physical endpoint, and each block event changes it by at most `b0=a_w+1` in absolute value. Sol's high-region synthesis supplies a **single finite scale** `s>=1` and a finite `N>=6` for which `V=sU` has the complete actual high-exit contract

    E_x[tau_H+J_nc(tau_H)+V(X_tau_H)] <= V(x),
    H={A>=N,D>=N},  x in H.                                        (H)

Here `tau_H` is the actual first exit from H; the nonempty-hidden generator and joint-axis four-event operation are both included. The source notes `HIGH_REGION_ELIMINATION.md` and `COMMON_RECEIVER_BY_ACTUAL_EXIT_VALUE.md` earn (H) without assuming a low-boundary drift. Note that `V` is globally defined, nonnegative, quadratically proper. **No new receiver is imposed on the high output.**

The other source is the exact original `POSITIVE_UNPAIRED_JOINT_CLEANUP.md`, supplied November 3, 2026. The arguments below use its pathwise finite cleanup count `N_H`, its complete physical service/interruption estimates (including active core), its good-deletion lower bound `E D>=c K/3` for sufficiently large n, and the physical/noncore residence upper bound `E(sigma+J_nc)<=C_H+C K(q+1)`. We retune its scalar `K,eps,n0`; we do not infer an inequality by multiplying its old `Z^2` inequality.

## 2. A tunable **V-native** stopped-return law

**Theorem 1 (arbitrary linear surplus).** Fix any finite integers `H>=1,L>=1` and any finite `Gamma>0`. For the full ten-rate generator, there are `eps>0` and `n0<infty`, depending on the rates,H,L,Gamma, such that every physical input with

    A,D<=H;  n=min(r1,r2)>=n0;  max(r1,r2)<=L*n;  q<=eps*n        (P)

admits Sol's *actual, unmodified* cleanup followed by guarded delayed drainage, with genuine stopping time `sigma`, and

    E_x[sigma+J_nc(sigma)+V(X_sigma)]
          <= V(x)-Gamma*(1+M(x)),                              (P1)
    M(X_sigma)<=2(1+M(x))  on EVERY realization.                (P2)

One can replace the factor 2 in (P2) by `1+delta` at the expense of shrinking eps and enlarging n0. Uniformity is within each fixed H,L,Gamma, not across unbounded heads or ratios.

**Proof.** Keep Sol's *same physical policy*: service is run at the actual core/terminal rates until the first terminal or competing growth; cleanup has at most `N_H` continuing noncore events before either successful `A=D=0` or a failure; after success, run at most `ceil(K(q+1))` full activation attempts, stopping at the first interruption or at `D=floor(n/4)` good deletions. All source competitions, actual endpoints, all core jumps and genuine residence are present in the source construction.

In particular the entire run has anchor head at most `H'=H+N_H+5` independent of n. The residual differences change only by source 0 (+1) and source 1 (-1) in each port; source 2, terminal and core preserve them. Neutral completed words `0,1,2,3` leave the complete physical state unchanged, whereas good words `0,1,1,3` change the selected unpaired B (or E) by precisely -1, leaving its positive minority unchanged. Thus for all n large, on the *whole physical path*,

    r1,r2>=n/2>H',  hence g1=g2=0,
    V(X_t)=s*C*(Psi(X_t)+c0)^2.                              (P3)

Every core jump leaves Psi exactly fixed. Cleanup and a possible single final interruption involve at most `N_H+5` noncore events; thus there is a pathwise error `xi` with

    Psi(X_sigma)=Psi(x)+xi-3D,
    |xi|<=b_H=(N_H+5)*(a_w+1),  0<=D<=floor(n/4).             (P4)

In particular `xi` is independent of the number of neutral attempts, and independent of K and n; the ordinary good-deletion drift is exactly **3 units of the high-region workload**, not merely one unit of the old Z.

Put `P=Psi(x)+c0`. For positive r's, `P>=6n` and `P<=6L*n+eps*n/2+O(1)`, while `M(x)<= (2L+2eps)*n+2H`. After n is enlarged (depending on b_H), `3D<=P/4` and direct expansion gives

    (P+xi-3D)^2-P^2 <= 3*b_H*P-5*P*D.                   (P5)

(Use `9D^2<=3PD/8`, `6b_H D<=PD/8` and `b_H^2<=b_H P`.) The source's true good-probability and interruption estimates give for a suitable numerical constant c>0, uniformly in the cone,

    E D>=c*K/3,
    E(sigma+J_nc(sigma))<=C_H+C*K*(q+1).                 (P6)

First choose K so large that the negative term `5 s C P cK/3` absorbs the required `Gamma*(1+M(x))`, the fixed `3b_H*s C P` cleanup error and one more positive multiple of P. Then choose eps **after K** so that `C K eps*n` is smaller than this residual linear margin and the true failure/guard probabilities remain within the source's bounds. Finally enlarge n0 to pay the constant `C_H+C K`, all finite-head errors and the guard. This gives (P1), with all choices finite and raw-rate-dependent.

The cleanup changes `q=C+F` by at most the explicit head-dependent constant `b_q=2(N_H+1)` (core transfers preserve q; each noncore event changes q by at most 2). There are at most `N_H+1+4ceil(K(q_initial+b_q+1))` noncore events in this stopped word. A noncore event changes M by at most 7; core preserves M. Hence pathwise

    M_out<=M_in+7[N_H+1+4ceil(K(q_initial+b_q+1))].

Because `M_in>=2n`, eps can be made sufficiently small after K and n0 enlarged to make the last addition at most M_in. This proves (P2). The source's physical moments guarantee all expectations and stopping laws are genuine. QED.

**Why this is more than rescaling Sol's existing stopped inequality.** Neither a generic quadratic comparison nor multiplication of `E[Z_out^2+cost]<=Z_in^2` proves (P1). It is the exact zero anchor term (P3), exact core invariance, exact -3 good effect and the ability to make the mean *number* of good deletions as large as any prescribed finite K that earn the new receiving value.

## 3. Attach an actual low-low corner corrector while keeping V on its exit

Let `C0={A<=2,D<=2}`. Let `tau0` be its first actual exit. No terminal reaction is enabled until tau0, each block event raises precisely one anchor by 1, and core fixes both anchors and the total population. Thus

    J_nc(tau0)<=5, E tau0<=5/B0,
    |Psi(X_tau0)-Psi(x)|<=5(a_w+1).

The process before tau0 visits a finite physical state set for each input; nonexplosion is accepted. For x in C0 define its **actual** finite Green value

    F0(x)=E_x[tau0+J_nc(tau0)+V(X_tau0)].                (C1)

Then `L F0=-1-q_nc` everywhere on C0, in the *raw* generator, and

    |F0(x)-V(x)|<=K0*(1+M(x))                           (C2)

for a finite raw constant K0 (with fixed V). Indeed at both the input and output the anchors are at most 3, so all `g_i^2` contributions to U are bounded; the squared-Psi variation is at most `10(a_w+1)(Psi+c0)+25(a_w+1)^2` times `sC`. The physical and count rewards are at most `5/B0+5`. This proves (C2) with no stationarity or core-activity moment assumption. F0 is nonnegative, quadratically bounded and proper, because M_out>=M_in-35 pathwise and V_out dominates a positive quadratic in M_out.

Define ONE global receiver

    Vhat(x)= F0(x),  x in C0;
             V(x),   x not in C0.                       (C3)

It is globally proper and quadratically bounded. All raw exits from C0 receive exactly V, and therefore Vhat, at their genuine physical landing. Since N>=6, all first exits from H still have both anchors >=N-3>=3: they **cannot** land in C0. Therefore (H) is valid verbatim with Vhat at high inputs and outputs. No high source has been deleted and no high-return seam correction is imposed.

For a positive-unpaired input satisfying (P), choose Gamma>=3 K0 and shrink eps (if needed) so the pathwise (P2) holds. Using (C2) twice, once at the input and once at the actual output, yields

    E_x[sigma+J_nc(sigma)+Vhat(X_sigma)]
      <= V(x)-Gamma*(1+M_in)+2K0*(1+M_in)
      <= Vhat(x).                                       (C4)

Thus the complete overlap between the original corner potential, the high return and the positive-unpaired operation is received at coefficient one **without assuming an unknown boundary law or treating two quadratic potentials as equal**.

## 4. An unrestricted-minority and mixed-sign **raw** Foster region

The source-resolved high workload permits a stronger direct operation than the positive-unpaired drain when both anchors are at least 3. **Neither the absolute cold inventories nor the anchor ratio nor the signs of the two residual differences need be restricted.** Only the *magnitudes* of the unpaired differences must dominate their corresponding anchors by a fixed finite margin.

Put `f(t)=2*(t mod2)+floor(t/2)` and `w=a_w>=4`. On port i, let `a>=3`, `r=B-C`, `t=min(B,C)`, and `lambda_j` its four actual source hazards. For `|r|>=2`, the following are **exact integer increments**, not asymptotic approximations:

| Sign of r | source 0 | source 1 | source 2 | source 3 |
|---|---:|---:|---:|---:|
| `r>0` | +3 | -1 if t even; -4 if odd | +2 if t even; -1 if odd | -1 when enabled |
| `r<0` | `-w+2` if t even; `-w-1` if odd | +w | +2 if t even; -1 if odd | -1 when enabled |

A disabled source has zero hazard. The core transfers two units of *both* hidden counts per port, so both signed r_i are preserved, each t_i changes by an even number and `sum_i f(t_i)` is **exactly invariant**. Thus `L_core Psi=0` with all real core rates retained.

**Theorem 2 (all-rate, all-minority mixed-sign Foster sector).** For each port there is an explicit finite raw integer `R_i`, such that on the entire physical region

    Rmix={A,D>=3,
          |B-C|>=max(A+2,R_1),
          |E-F|>=max(D+2,R_2)}                             (M1)

one has

    L Psi <= -q_nc/4,   L Vhat=L V<=-1-q_nc.              (M2)

There is **no** bound on `C+F`, no requirement that r_1,r_2 have the same sign or comparable magnitudes, and no bound on A/D. Every feasible source and both core directions are included.

**Proof with finite choices.** Write the port's fixed positive rates as `kappa0,...,kappa3`. Increase `R_i` until all of the following are satisfied for `r>=R_i`:

    3*kappa1*r >= 16*kappa0,
    12*kappa3*(r+1)*(r+2) >= 16*kappa0,
    kappa2/[kappa3*(r+1)] <= 1/8,
    2*(kappa2/kappa1)*(r+1) >= 8*w,
    w*kappa1/[2*kappa3*(r+1)*(r+2)] <= 1/8.               (M3)

Such a finite R_i exists for **every** positive rate list. The third bound holds for either sign whenever t>=2, by exact falling-factorial division:

    lambda2/lambda3 = (kappa2/kappa3)/[(a-2)(B-1)(C-1)]
                    <= (kappa2/kappa3)/(r+1).

For `r>0`, at t=0 or odd t>=1 all enabled non-source0 channels have workload increments at most -1; source1 at t=0 has `lambda1>=16*kappa0`. For even t>=2, source3 has `lambda3>=16*kappa0` by (M3), and `lambda2<=lambda3/8`; the source1 increment is -1. Thus

    L_i Psi <= 3*kappa0-lambda1+2lambda2-lambda3
            <= -lambda1-(9/16)lambda3 <= -q_i/4.

At odd t>=1 the same `-q_i/4` inequality follows from the negative source1/source2 increments and the first bound in (M3).

For `r<0`, t=0 enables only source0 with increment `-w+2<=-2`. At t=1, source2 has increment -1 and

    lambda2/lambda1 = (kappa2/kappa1)*(a-1)*C
                    >= 2*(kappa2/kappa1)*(r+1)>=8*w;

therefore the positive `+w` source1 is paid by source2. For t>=2 the two exact ratios and (M3) give `lambda2<=lambda3/8` and `w*lambda1<=lambda3/8`; the source0 contribution is already negative. The terminal then pays **both** positive possibilities with a uniform `-q_i/4` margin. Sum the two ports, and use exact core invariance, to obtain the first inequality in (M2).

Now ensure, by enlarging R_i if necessary, that `P=Psi+c0` on Rmix satisfies

    P>=4*(a_w+1)^2,      s*C*P/4 >= 1+1/B0.           (M4)

At every input in Rmix, each `g_i=0`, because `h_i>=|r_i|>=a_i+2`. This also holds at **every one-jump physical neighbor**, including a source1 which reduces a positive r by one, and a source0 which reduces the magnitude of a negative r by one: both raise the anchor by one, consuming at most the two-unit margin. Source2 and terminal are easier, and core preserves r and anchors. Moreover, after any single jump the *other* anchor stays >=3, so that neighbor cannot lie in the double-low corner C0. Hence `Vhat=V=s C P^2` at the state and all its one-jump neighbors; there are no uncharged `g_i` or `F0` switching terms.

Using the true **two-sign** bound `|Delta Psi|<=b0=a_w+1` for all enabled sources (negative-r source1 has increment `+a_w`, so a bound of 4 would be false), the raw generator gives

    L Vhat=s*C*[2P*(L Psi)+sum_sources lambda_r*(Delta Psi_r)^2]
          <=s*C*(-P/2+b0^2)*q_nc
          <=-(s*C*P/4)*q_nc <=-1-q_nc,

as required. The inequalities are uniform over all actual core fibers and all absolute inventory scales. QED.

**Actual exit kernel.** The set Rmix is invariant under **each core jump** (it depends only on anchors and the two residual differences). Stop at its first physical exit. Localization of the last pointwise inequality gives

    E_x[tau_mix+J_nc(tau_mix)+Vhat(X_tau_mix)]<=Vhat(x).

Since the noncore hazard is always at least B0, tau_mix is finite a.s., and its first exit includes at least one counted block reaction. All genuine endpoints are paid. This adds one fully compatible, all-rate **mixed-sign, arbitrarily large minority** operation to the previously stitched high/corner/drain menu.

## 5. General actual-stop fusion lemma and its application

**Lemma (count-charged policy fusion, no uniform head).** Let a nonexplosive countable-state CTMC have an integer-valued nondecreasing count N(t). Let Vhat>=0 be proper. Suppose a countable family of regions D_i has an actual stopping rule tau_i for every x in D_i such that

    E_x[tau_i+N(tau_i)-N(0)+Vhat(X_tau_i)]<=Vhat(x),

and the stop always includes at least one counted event. Give each input in `G=union D_i` the first eligible policy in a fixed enumeration. Reapply the chosen policy at its genuine endpoint whenever that endpoint is in G. Stop at the **first episode endpoint** outside G. Then that combined stopping time T is a.s. finite and

    E_x[T+N(T)-N(0)+Vhat(X_T)]<=Vhat(x), x in G.        (F1)

**Proof.** Iterate the conditional inequalities through m policies and add their genuine costs. The nonnegative supermartingale bound gives `E sum_{k<m} costs<=Vhat(x)` for all m. Since each continuing policy includes at least one counted event, the expected total number of attempted policies is at most Vhat(x) and therefore finite. Hence the algorithm exits after finitely many episodes a.s. The full CTMC is nonexplosive, and the genuine stopping times and cost sums are finite. Fatou gives (F1). The result does not say that T is the *first physical exit* from G; a verified episode may temporarily visit its complement, and all this motion and its final landing are retained.

Apply the lemma with: (i) the entire high region H, with Sol's actual high-return rule; (ii) the **entire** double-low corner C0, with the actual `tau0`; (iii) the full mixed-sign, unrestricted-minority region Rmix from Theorem 2, using its actual first-exit stop; and (iv) for every finite integer pair `(H,L)`, the positive-unpaired inputs (P), with Gamma=3K0+1 and the corresponding retuned eps(H,L),n0(H,L). All regions use the SAME Vhat from (C3), and every episode pays genuine noncore count and physical residence. The countable union yields the **single globally composable coefficient-one stopped operation** (F1) on its noncompact domain, even through arbitrary repeats of the high/corner/positive-region operations. This is not a claim that the domain is all of N^6.

## 6. Exact count-gauge time pricing (independent structural simplification)

Write `ell=3(A+D)-4(C+F)`. Every source0 changes ell by +3; each source1/2/3 by -1; core changes ell by zero. Thus pathwise

    J_nc(t)=4 N_0(t)+ell(x)-ell(X_t),
    q_nc+L ell=4B0.

For integrable true stops with integrable landing, source0's constant-rate clock gives

    E_x[tau+J_nc(tau)+Vhat(X_tau)]<=Vhat(x)
      iff
    E_x[(1+4B0)tau+(Vhat-ell)(X_tau)]<=(Vhat-ell)(x).

Because ell is only linear, subtracting it preserves properness of the quadratic Vhat (after adding an irrelevant sufficiently large constant). This identity is useful for expressing policy fusion using only physical time and a shifted receiver; it does not supply inward sign on any missing domain.

## 7. The real unresolved geometric interface

The global fusion domain above is *not* all physical states. It still excludes most mixed/negative unpaired differences, separated scales, high-vs-low anchors with an arbitrary active peer, and the complete intermediate unready population regimes. N1671's terminal/core service receiver W is still valid at its own earned scope but it is **not** automatically fused into Vhat: the two leading quadratic angular geometries differ in some directions by order M^2, not O(M).

Two simple rays at A=D=0 demonstrate the obstruction. For B=C=E=F=n, `Psi=n+O(1)` while `S=4n`, so `U~C n^2`, `W~16R n^2`. For B=E=n,C=F=0, `Psi=6n` while `S=2n`, so `U~36C n^2`, `W~4R n^2`. Thus the U/W leading ratios are C/(16R) and 9C/R, a factor of 144 apart. No single scalar normalization can make `U-W=O(M)` on both rays. This is why (C2) works for the finite-phase corner corrector but not for a general terminal/core service replacement.

The completed construction is therefore a new actual **zero-gain fusion** of four proved regimes and a reusable count-charged switching lemma, **not** a full six-species positive recurrence theorem. A genuinely new angular/activation operation or normalizable stationary-measure construction remains necessary to cover the complement.

## Sources and reproducibility

- Sol, `PROPER_HIGH_ANCHOR_RECEIVER.md`, `JOINT_AXIS_FOUR_EVENT_THEOREM.md`, `HIGH_REGION_ELIMINATION.md`, frozen commit `487bfb76526a4218c71990cd32dda8e0a52478c7`, and its high-region accepted physical-count contract.
- Sol, `GLOBAL_SERVICE_RECEIVER.md`, commit `23d0ada35f0340d1460403d23503620e3686c2d0`: compatible source-sensitive service physics, but not assumed a Vhat receiver.
- Sol, `COMMON_BACKGROUND_SOURCE_RENEWAL.md`, commit `c53cdb1c534aef14de99e44532cc69d3935576a7`: actual common background source transport and polynomial renewal; not needed as a black-box global boundary sign.
- Supplied `POSITIVE_UNPAIRED_JOINT_CLEANUP.md` (original joint cleanup/delayed drain proof): bounded core-live cleanup, first interruption and good deletion estimates used above.
- Anderson, Cappelletti, Kim (2020), multistep embedded-chain stochastic recurrence arguments, arXiv:1904.08967; Laurence and Robert (2023), physical-time stopped Foster criterion, arXiv:2310.01949. Neither ordinary theorem establishes recurrence for this generator.
- `verify_u_native_stitch.py`: exhaustive finite integer stoichiometric checks.
- `verify_mixed_sign_workload_region.py`: mixed-sign generator fixtures with exact rational drift and one-jump receiver checks (not the proof of uniform-in-population rate inequalities).
