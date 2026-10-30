# Parameterized transfer of the acquired local certificate

30 October 2026. WORKING transfer proof, NOT independently reviewed. This is an interface-level construction explaining what the raw-graph acquisition would buy. It is not part of either accepted frozen bundle. No general weak-reversibility or novelty claim.

## Exact proposed input

Keep the connector `0 -> A+B -> mA+qB -> 0`, a0>=2, m=a0+2, q>m. Replace the two-type fast conversion module by a finite irreducible graph on residual types X_1=a,X_2,...,X_k, with reactions X_i+D->X_j+D, only the linear birth a+D->2a, positive 2a->a+D seed, optional 2a->2D seed, and positive 2D->a+D. Fixed positive clearing at 2a is the connector clearing under the common physical factor (A)_a0(B)_q. All rate parameters and graph size are fixed. The offset is physical A=a+a0.

The preceding graph notes acquire local kernels but not this full connector theorem. The candidate conclusion here is classwise positive recurrence and every prescribed total-count exponential invariant moment, via the same two-direction construction as the frozen four-species bundle. The purpose is to isolate dependence on numerical decay exponents, rather than append unrelated reactions and repeat the specialized resolvent.

Let N=A+sum_{i>1}X_i+D. The exact phase coordinates H,r,Z and active-section convention are unchanged, replacing C by sum_{i>1}X_i. Every fast move conserves N,B. For n=N-a0 large, a positive-D input is active exactly when A>=a0: if D>=2 the reverse channel is enabled, while D=1 and some type present enables a conversion/birth. Exceptions have bounded n. At D=0 only the same a-seed/clear marks remain. Thus the dormant reference connector and its actual marked seed outputs have precisely the old A,B law; frozen other-type counts are merely carried through as residual metadata.

## 1. Local certificate in abstract exponent form

For every member of the finite exponent list needed in the phase processor, use acquired constants C_s and positive exponents. Choose one eta>0 smaller than all relevant uniform T,U, and terminal f_m-reset exponents, and if necessary smaller than 1. Let epsilon_n denote a fixed sum of positive powers n^(-eta) and n^(-delta/2), delta=1/(2L+1).

The available positive-D first-stage bounds are:

* profile transport C_s f_s;
* time and activation spending m and m-1 powers, respectively;
* `(b)_q T + (b)_q U + E f_m(A_out) <= C n^(-eta)`;
* dormant entrance in incoming f_s profile <=C_s n^(-delta/2) f_s;
* on x>=K(n)=log^2(2+n), same-stage T/U<=C/x, V_m/[(b)_q U]<=C/x^2, and V_(m-1)/[(b)_q U]<=C/x.

The last reward case is proved in GRAPH_GENERAL_DORMANT_REWARD_COROLLARY, not assumed from the p=m case. Finite small shells retain their actual values. Fast phases conserve n, so fixed residual powers can be carried pointwise during each local stage; variable residual powers across dormant/connector phases still require the actual polynomial-weight Green.

## 2. Full local first-connector continuation

A positive-D stage ends at the first connector or dormant entrance. At a dormant entrance apply the existing actual D=0 Green, stopped at connector or seed, with its A,B output retained. The weighted return-to-seed operator is bounded on each f_s, whereas the preceding positive-D-to-D=0 operator is O(n^(-delta/2)) in the same profile. Their product is smaller than 1/2 above a raised residual threshold. Positive iteration constructs the full first-connector law, not an assumed stationary law.

This retains profile grades and uniform positive-power resets, possibly reducing eta. For good input, dormant continuation time and occupation are at most constants times V_m/(b)_q and V_(m-1)/(b)_q after the same small-kernel inversion. Thus T_full/U_full<=C/x, and later dormant occupation is O(U_full/x). This is the qualification margin needed in Section 5.

The fixed-b local iteration here is stopped before the first connector; B cannot change inside it. It is distinct from the unbounded-B dormant section Green used in the full phase processor. Confusing these two stopping conventions would invalidate this step.

## 3. Phase processor: exponents change, geometry does not

Take the finite requested set of s (and their needed 2s). Choose lambda so ordinary clearing profile factors satisfy C_s exp(-lambda)<1/8. Then raise r0 so high-activation and dormant-error norms are small: high activation has unweighted mass O(n^(-eta)) and f_(2s) transport, hence f_s norm O(n^(-eta/2)); dormant return contributes O(n^(-delta/2)). Their fixed exp(lambda B-jump) factors are absorbed at this second choice.

Ordinary high clearing decreases B by q. Low activation plus ordinary clearing decreases B by one. Noncompulsory low immigration increments a finite degree counter and spends one inverse power. The B=0 launch either returns immediately or consumes a counted race. At each fixed counter the continuing norm is below 1/2; the finite triangular counter matrix therefore has a positive Green. The actual high seed B remains weighted by exp(lambda B), never replaced by a bounded phase.

Designated exits remain small in the tilted exit measure: high immigration costs O(n^(-eta)); high activation O(n^(-eta/2)); clearing output has f_m reset O(n^(-eta)), paying low-race/inactive exits; dormant error has its acquired power. Bounded physical approaches from inactive inputs have bounded overshoots and are then composed with these exit measures. A second positive Neumann series constructs the actual arbitrary-phase return/threshold repair with bound

    C exp(lambda B_in) (1+r)^j exp(theta r)

for each fixed requested real j and profile. The same polynomial-weight proof as the frozen Green is required here: decreasing output r cannot be replaced by its input. No numerical equality eta=1 is used in either inversion.

## 4. Complete signed source

The degree geometry is unchanged because fast moves preserve N,B. Positive terminal residual requires degree at least m. Applying the acquired grades along the finite-degree processor and stopping at the actual first completed degree gives the same complete dormant source O(w f_m).

More sharply, split a section cycle at its first connector. All three first connector outputs are r-neutral and have fixed B. From clearing output, positive continuation costs f_m; `(A)_m f_m(A-m)` is bounded. From activation output B=2q-1, positive continuation needs one further degree and costs f_1; `A f_1(A+m-1)<=1`. Immigration has mass iT. The graded repair is already earned, so

    E[(w_next-w)_+] <= C w T,
    P[w_next f_m(A_next)] <= C w T.

These identities are structural compensator statements, independent of the old 1/n reset exponent. Therefore the bad positive-D source is O(w r^(-eta)), not O(w/r).

## 5. Genuine negative event on the logarithmic good set

Take good section inputs A>K(r), K(r)=log^2(2+r). An activation has mass proportional to U. The local occupation reward bounds price later dormant low-A activation mass by O(U/K), so all but that amount is qualified. An initial high-A dormant part is qualified directly.

After a qualified activation at B=2q-1, prescribe ordinary clearing to q-1, then low activation/clearing pairs down through q-2,...,1, followed by low activation to active B=q. It reduces r exactly by h=q-m and has no earlier section return. At a positive-D clearing, terminal f_m reset bounds the chance A_out<K/4 by

    C K^m r^(-eta) -> 0.

Direct high-A dormant clearings lose only a bounded number of A particles; low-race failures are O(1/K). The finite word succeeds with probability 1-o(1) uniformly on qualified outputs. Thus a genuine negative event has probability at least cU. Combined with the independently priced full positive part,

    Pw-w <= -c_theta w U + C w T.

The full T/U ratio tends to zero on this good set. No failed continuation is declared nonpositive.

## 6. Non-small dormant row and altered bad scales

Use

    g0=w f_m(A),      g+=w (1+r)^(-eta).

The actual pure dormant bad-to-bad kernel is not small; precondition it by its previously earned Green. A seed-mediated dormant return is small by the acquired weighted return power. For the other blocks, on A<=K(r), inverse-profile/reset estimates give the same two-type majorant with small parameter

    e(r0)=sup_{r>=r0} C K(r)^m (1+r)^(-eta) -> 0.

Specifically B0->B+ has norm at most e, B+->B0 bounded, B+->B+ at most e. The real polynomial residual-weight extension uses j=-eta and the logarithmic factor must be kept at actual outputs. It can be bounded by arbitrarily small positive residual powers: for any rho in (0,eta), K(r)^m<=C_rho(1+r)^rho. Use this bound inside the ACTUAL weighted kernel, not a pointwise output-to-input replacement. This yields e<=C r0^(-(eta-rho)) after the finite preconditioning constants are fixed.

Positive 2x2 iteration constructs H0<=Cg0,H+<=Cg+ and its actual bad-set kernel equation. On the bad positive-D set g+<=C K^m r^(-eta) w f_m=o(w f_m); globally H<=C w f_m. The unrestricted inverse-m identity therefore gives good leakage PH<=CwT=o(wU). The negative good margin survives.

## 7. Physical costs and complementary direction

At B=q, n=r+O(1). The first holding interval gives U>=c(1+r)^(-m); bad dormant f_m>=c(1+r)^(-m), and the bad positive-D scale is r^(-eta) with eta<1. Repeating the fixed polynomial-weight construction at order at least m therefore pays physical cycle cost. This produces the r-directed stopped value with exterior leakage C exp(lambda B), not a bounded leakage.

The complementary Z=B-N-h I_active trial uses only: conservation of N by fast moves; the active predicate described above; uniformly vanishing positive-D first-connector T,U; a positive chance of genuine dormant clear versus seed; and finite-N paths. All are retained. Large-N trials use whole actual first-connector episodes. Finite-N activation/clearing pairs reduce N by one; unexpected neutral events abort. At most m prescribed immigrations give down probability c Z^(-(m-1)), up probability C Z^(-(q-1)), and bounded conditional trial duration. Conditional renewal gives up-exit probability O(Z^(-(q-m))) and mean O(Z^(m-1)). There is no need for eta=1 in this fixed large-N threshold choice.

The Z stopped value's exterior leakage remains C AB. Since r=N-alpha B+O(1), Z=B-N+O(1), alpha=(m-1)/(q-1)<1, choose theta_Z after lambda so theta_Z(1-alpha)>lambda. This absorbs the true r-potential leakage on its threshold strip; exp(theta r) absorbs AB on the other strip. First holding lower bounds make the sum normlike.

Fast reactions conserve total N+B. Connector clearing dominates AB in the high corner and AB is linear on complementary strips, giving independent nonexplosion. Localized stopped-value Foster then yields the candidate recurrence/moment conclusion. Every allowed transition lies in an executable reaction-cycle return because the connector and this exact fast graph are weakly reversible; communicating components are therefore closed.

## Review boundary

This note is a substantive transfer construction, not an accepted extension. In particular Section 6's logarithmic-output bookkeeping and Section 7's parameterized Z trials deserve whole-interface challenge. The scientific claim worth testing is the finite raw-graph acquisition plus this exponent-robust interface, not arbitrary weakly reversible recurrence or novelty of Foster theory. The two original whole-review receipts do not cover this file.
