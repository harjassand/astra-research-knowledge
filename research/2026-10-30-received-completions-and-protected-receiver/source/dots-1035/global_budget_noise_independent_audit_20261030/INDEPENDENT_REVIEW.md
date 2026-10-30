# Independent review: global joint-norm budget and unknown strong local defects
2026-10-30. Reviewer: `challenge_live_busy_energy`.

## Verdict and scope
**Scoped PASS, with the completing global-module and boot arguments below, for the GLOBAL-radius native memory, live BUSY/common-span access, and base finite destructive CSS readout under a pointwise TOTAL joint cb-norm budget.** Per-site smallness is not needed for these global-radius conclusions. The nominal bounded-degree architecture and every stated initialization/control/readout resource remain unchanged.

This is a NEW scoped error-model extension, not a retrospective edit of earlier receipts. It does not extend the old connected-animal/subset/LOCC/source-waiting theorems. A finite independent-module completion lemma is earned here, but applying it to a particular Bell carrier additionally requires that carrier's own disjoint-module witness and physical coupling contract; this receipt does not import an entire recipient/source process.

The root candidate reviewed is copied verbatim in `reviewed_sources/GLOBAL_JOINT_NORM_BUDGET.md`; its hash and all governing dependency hashes are in `DEPENDENCY_SHA256.txt`. The proof below is substantive completion, not acceptance merely because several previous sources used an O(N) sum.

## 1. Precise physical hypothesis and a meaningful defect interpretation
For every time u, suppose the bounded perturbation is a sum of local normal HP adjoints N_Z*(u), supported on at most q physical system sites and the retained shared bath, with

    sum_Z ||N_Z*(u)||_cb <= eta N.                  (1.1)

The system body bound q is fixed; the sites in Z may be distant, unknown and time dependent. The TOTAL actual generator and interval propagators must remain physical/CPTP; signed local decomposition pieces need not themselves be generators. The same existence/normality and CP/TNI killed-compression assumptions as the accepted global memory theorem remain. The nominal system generator still has bounded degree, fixed local dimensions and fixed rates.

Equation (1.1) is an instantaneous worst-case JOINT norm, not a time average, marginal reduced-system norm, state-average power, or calibration estimate. Bath-only nominal evolution is separately CPTP and identity-annihilating. Center bounded local pieces only within the SAME total trace-preserving perturbation: subtracting {N_Z*(I),O}/2 preserves their aggregate exactly when sum_Z N_Z*(I)=0, and costs at most a factor two in the summed norm. No cancellation with an uncontrolled/unbounded bath generator is permitted. Absolute convergence for fixed N follows directly from (1.1).

An unknown set of at most fN bounded-degree defective quantum/controller/detector components is genuinely covered if each component's removal/replacement changes at most c_def bounded-body terms with total joint generator-difference norm at most R. Then

    sum_Z ||N_Z*||_cb <= c_def f R N.

For f<eta_*/(c_def R), the theorem applies uniformly without locating the set. A missing reset can be modeled by cancelling its bounded nominal dissipator; a wrong bounded local interaction can be added as another bounded difference. This is not restricted to weak faults at those sites: R may be much larger than the original per-site threshold, provided f is correspondingly smaller.

This interpretation retains the fixed physical Hilbert space and body size. Undeclared loss levels, infinite rates, unbounded fanout, a faulty global command device, or a failed classical output processor are not automatically represented by (1.1). Final faithful pointer reading, supplied reliable commands and reliable classical postprocessing remain declared resources.

## 2. Global memory: the noise estimate is genuinely termwise
The accepted global observable is

    F=T_B T_t(VG_mem),    V=exp(s[U+R D]),
    D=sum_h B_h,

with fixed-depth local proof maps and a fixed-depth bounded-incidence activity congruence. The accepted inverse maps used in algebraic normalization are local bounded LINEAR maps; inverse positivity is not used.

For one q-site physical noise term, conjugate to the fixed full-Hilbert forest coordinates and through the actual proof circuits. Disjoint circuit pieces cancel, leaving a union of at most C(q) fixed nominal cones. Its local norm is bounded by K(q)||N_Z*||_cb. This constant depends on q, local dimensions and the already fixed proof coefficients, but NOT on the rate of another noise term, the number of noisy terms meeting those sites, or the distance between sites in Z.

Split V into the factors affected by this union and the unaffected commuting factors. Only C(q) bounded local energy/history terms are affected, so the affected positive factor has a fixed upper/lower spectral ratio. The direct relative-norm calculation, followed by positive CP pullback, yields INDIVIDUALLY

    +/- N_Z*F <= C_mem(q)||N_Z*||_cb F.             (2.1)

One may express the bookkeeping explicitly as T^{-1}N_Z*T and then the local activity congruence, prove a relative inequality on VG_mem, and apply positive T. This does not apply an inequality through T^{-1}. Alternatively the accepted local Stinespring argument gives the same bound. The constants are uniform for the declared small-epsilon regime; T_B's fresh survival bounds and T_t's bounded local inverse are fixed before this noise allocation.

Summing (2.1) with (1.1) gives exactly the former C_noise eta N F source. Every nominal drift, dirty-service, useful-clock, DATA-density and finite-controller path estimate is unchanged: it was proved for the fixed NOMINAL apparatus, and actual noise was subsequently handled by (2.1). No noisy local regeneration or per-site-smallness service theorem is being smuggled into that nominal calculation.

The canonical basin/edge proof also needs bounded body size, not small amplitudes. One insertion changes only a bounded number of energy terms and a bounded Pauli weight. The boundary-source height and N0 therefore depend on q but not on its local rate. The full-versus-killed comparison uses the sum of the actual local map norms. That sum is at most

    C_nom N + eta N,

so its polynomial prefactor remains O(N) (up to the already accepted geometric/gentle factors). The positive outgoing-loss comparison uses the FULL physical generator, never the signed perturbation pieces as physical generators. Its CP/TNI existence condition is retained.

Consequently the accepted nonlinear killed moment, exponentially small boundary mass, canonical logical identity and fixed-radius common-span theorem hold under (1.1), with a possibly smaller positive eta threshold. No fixed noise-partner graph or per-site noise estimate is required in these steps.

## 3. Live BUSY: no hidden spatial hierarchy
For the independently accepted constant-singleton observable G_busy,

    L_native*G_busy <=[-a delta_A M_busy+C delta_A epsilon^2 N]G_busy,
    exp(k delta_A M_busy)<=G_busy<=exp(K delta_A M_busy).

The original full-Hilbert witnesses and the actual unified L0 are unchanged. The separately accepted centered-noise refinement is termwise:

    +/- N_Z*G_busy
       <=C_A(q)delta_A ||N_Z*||_cb G_busy.          (3.1)

Its proof is a bounded structural-cone derivative at delta_A=0; it does not count noisy neighbors. Summing (3.1) with (1.1) gives

    L_actual*G_busy <=-lambda_A G_busy logG_busy
                        +C delta_A(epsilon^2+eta)N G_busy.

Thus the full-state BUSY-density tail is uniform at every eligible exogenous/deterministic storage time, with arbitrary retained reference/bath. It is not a noise-dependent stopping-time or simultaneous infinite-time no-excursion statement.

The live-access receipt transfers this FULL-state event to the positive canonical killed channel by its channel-distance estimate, then applies the commuting controller mask projection. It never requires the DATA-dependent activity observable itself to commute the basin. On the good mask, forest-prefix support grows by at most r_D beta_ctrl N. Neither this support statement, the gentle projection nor the fixed correctable-span decoder uses a per-site error probability.

**Counterexample to an excluded transfer:** cancel the nominal reset on fN chosen pointer modules and initialize those modules unfinished. Each such module stays unfinished with probability one, while the total difference norm is O(fN). Therefore a uniform subset law p^{|S|} with p<1 is false even for a singleton hot module. The global count law below is the appropriate replacement, not a claim that every component works.

## 4. General global completion lemma, including its exact conditions
Let i=1,...,m, with m<=nu N, index independent nominal finite modules on disjoint tensor factors (or disjoint complete module factors after fixed grouping). Other nominal terms must act trivially on the module tests. The nominal bath-only factor is separate. Assume

    0<=a B_i<=A_i<=B_i<=I,
    B_i is a projection,
    L_i*A_i<=-r A_i,

with fixed a,r>0. The upper A_i<=B_i implies A_i is supported in B_i and commutes B_i. A finite positive completion witness comparable to B_i can be normalized to this form. The module states need not be independent or uncorrelated with DATA/reference/bath.

For fixed 0<theta<=theta0, put

    H=product_i (I+theta A_i).

Disjoint factors commute. The exact nominal product rule gives

    L_nom*H <=-r H sum_i theta A_i/(I+theta A_i)
             <=-[r/(1+theta)]H logH.               (4.1)

The scalar inequality is valid on 0<=x<=theta:

    x/(1+x)>=log(1+x)/(1+theta).

No noncommuting Jensen or independence assumption appears.

A centered q-body noise piece touches at most k_q module factors. Factor H=H_out H_loc. The untouched system factors pass through the map even with a common bath. Since

    I<=H_loc<=(1+theta)^{k_q}I,
    N_Z*(I)=0,

one has

    ||N_Z*(H_loc)||
      <=||N_Z*||_cb[(1+theta)^{k_q}-1]
      <=C(q,theta0)theta||N_Z*||_cb.

H_loc>=I then yields the relative order bound

    +/-N_Z*H<=C theta||N_Z*||_cb H.

After centering and summing, the actual full-state moment obeys

    L_actual*H<=-lambda_H HlogH+C_H theta eta N H,
    lambda_H=r/(1+theta).

For normalized full evolution, scalar spectral Jensen gives

    log Tr(H rho_T)
      <=e^{-lambda_H T}nu log(1+theta)N
         +(C_H theta eta/lambda_H)N.               (4.2)

This uses the unconditional initial bound H<=(1+theta)^mI, so arbitrary initial module correlations are allowed. Since

    H>=exp[b_theta sum_i B_i],
    b_theta=log(1+theta a)>0,

choose a fixed T and then eta so both terms on the right of (4.2) are at most b_theta beta N/4. It follows that

    Pr(sum_i B_i>=beta N)<=exp[-b_theta beta N/2].  (4.3)

All constants and T are independent of N. No guarantee is made about a specified hot module. Overlapping native retirement witnesses do not satisfy the product premise and are not imported; live BUSY avoids that retirement requirement.

## 5. Finite destructive readout: the replacements are exact
Two direct applications of section 4 replace ALL relevant old pointer subset estimates in the BASE live-access/readout composition.

### 5a. Finite pointer preparation
Use the actual complete onsite reset-to-wait channels from the accepted finite-pointer addendum. Let

    B_i=I-|wait><wait|_i,   A_i=B_i.

Then L_prep*B_i=-kappa_p B_i. Concurrent nominal memory terms act as identity on the pointer factors, so they annihilate H even if DATA and pointer are grouped in one physical site. Noise on that site simply touches a bounded number of factors. Section 4 gives a global low-wrong-pointer tail from arbitrary joint pointer input after fixed T_p.

The existing commuting-label projection, gentle channel comparison and conservative ket/bra union bound remain valid. The initial-pointer contribution to the exceptional DATA set is still 2 beta_0 N; no initial dephasing or mixture is assumed.

### 5b. Final incomplete-detector event
During the declared constant-rate detector hold use

    B_i=|wait><wait|_i,   A_i=B_i.

For the actual J_b=sqrt(kappa)|b><wait| tensor P_b^Z instrument,

    L_det*B_i=-kappa B_i

on the ENTIRE local Hilbert space, not just a wait input. Other nominal DATA/pointer couplings are off, and nominal auxiliary/bath evolution touches neither. Section 4 therefore bounds the actual classical unfinished-count event from arbitrary correlated input. This is precisely the event filtered in the accepted signed-instrument proof; individual pointer correctness is supplied by the exceptional-support argument, not by completion alone.

### 5c. Finite physical access and exceptional support
Use the already accepted first-OFF nominal support background. Remaining physical first-edge waveforms are counted as insertions, not falsely declared noncreating. For total finite access/readout duration L and first-edge ramp duration Delta_first,

    integral sum_Z ||D_Z(u)||_cb du
       <=N[C_1 epsilon Delta_first+C_2 eta L]
       =N a_int.

This uses only (1.1). Forward variation of constants around nominal CPTP segments gives the SAME signed order tail

    epsilon_D<=exp(N a_int)[e a_int/gamma]^{gamma N}

beyond ceil(gamma N) insertions. Each insertion touches at most q sites and activates only a fixed number of owner/pointer footprints, regardless of its amplitude or whether the same hot site recurs. The nominal noncreating-mask support theorem therefore still bounds every retained left/right DATA coefficient.

The global completion event and the low-order signed span are not assumed independent. First compare the real CPTP suffix on the actual and positive good inputs. Only then truncate the good-input evolution. Filter final incomplete pointers as an actual positive classical event. The existing system-leg reduction on exceptional sites and actual-CPTP normalization prove the full logical-Z instrument bound. No signed truncation is called CP.

For the base model the total exceptional density is unchanged:

    w_out=alpha_mem+r_D beta_ctrl+2beta_0
                         +q_comb gamma+beta_inc.

Choose this below both the fixed correctable radius and, if using the efficient X-sector queue, its stricter energy/confinement margin. Final full logical-coordinate extraction still has the previously corrected generic O(N^2) ideal classical cost; neither a linear complete-output claim nor noisy classical computing is added here.

The resulting destructive output error is exponentially small in N, in addition to the inherited storage error. No per-site-smallness step remains in this BASE composition once 5a and 5b replace the old subset tails. Program/recipient/carrier variants require their own additional module and frame contracts; this review does not silently broaden them.

## 6. Controller boot needs a NEW global warm handoff, not the old animal moment
The old boot receipt's subset generating function and O(N) ANIMAL moment do not transfer under (1.1). They are unnecessary for the accepted GLOBAL-radius memory. The following replacement earns a fixed-gap warm contract.

Assume the same controlled boot resource as the old receipt: DATA is already encoded; its input logical/reference may be arbitrary; the initial controller/monitor/bath state is fixed independently of that logical input; payload dynamics is held off; complete finite-rate onsite reset modules are on; and a declared switch to storage is supplied. This does not construct an encoder or a finite/faulty implementation of the boot switch.

Let P_i be the primitive nonready reset-block projectors (hub clock/workspace and lock register blocks). Nominal boot resets have L_i*P_i=-kappa_i P_i. Use A_i=B_i=P_i in section 4. For any selected small alpha_boot>0, choose fixed dwell T_boot and then eta to obtain

    Pr(D_prim>alpha_boot N)<=exp(-c_boot N),
    D_prim=sum_i P_i.                              (6.1)

The actual native forest commutes these primitive projectors. At most alpha_boot N nonready primitive blocks activate at most r_frame alpha_boot N DATA sites, with a conservative fixed r_frame. Every history defect has a bounded OR cover by primitive nonready blocks, so on this projected mask

    D=sum_h B_h <=k_B alpha_boot N.                (6.2)

The accepted proof of these source identities is full-Hilbert and independent of the noise budget.

Expand the boot evolution by FORWARD Dyson around nominal reset/bath propagators, which act trivially on DATA. With r_*=ceil(gamma_boot N), the discarded diamond tail is exponentially small for eta T_boot sufficiently small. Each retained left/right leg has DATA Pauli support at most q_boot gamma_boot N. After the native frame, its common DATA support radius is at most

    w_boot N=(q_boot gamma_boot+r_frame alpha_boot)N+O(1).

There is a fixed local energy upper constant K_U: a weight-w DATA Pauli acting on encoded DATA has U<=K_U w. This follows from bounded energy-term support/incidence, without any active-density lower bound. Thus the framed, low-mask, low-order SIGNED comparison is supported in

    r<=w_boot N,
    E=U+R D <=[K_U w_boot+R k_B alpha_boot]N+O(1)
             =e_w N+O(1).                         (6.3)

Choose alpha_boot,gamma_boot so w_boot is strictly inside the common canonical radius and e_w is strictly below the chosen global energy cap. These are purely upper support bounds, so logical errors with zero syndrome are excluded by the small common DATA span, not by energy alone.

Now project the ACTUAL positive framed/low-mask channel further onto the common radius/energy cap in (6.3). The signed retained comparison already lies there, so its actual outside probability is at most the Dyson norm error. The primitive-mask projection costs the usual uniform gentle error from (6.1). The resulting actual map A is CP/TNI and exponentially close to a signed canonical product map rho_L ->rho_L tensor tau_signed. Use the accepted positive replacement:

    sigma=Tr_L A(omega_L),  sigma>=0,
    ||A-(Id_L tensor sigma)||_diamond<=2epsilon_D.

Its trace deficit is paid by the projection errors; normalize only after charging that deficit. This does not assert positivity of the Dyson truncation.

On the cap E<=e_wN+O(1), the accepted global upper comparison F<=exp(gN)exp(sE) gives

    Tr(F sigma)<=exp[(g+s e_w)N+O(1)].             (6.4)

Choose the boot densities so

    max{g+s e_w,nu_memory}+q_t < s_prime e_cut

by a FIXED positive coefficient gap. This is exactly the global warm-input condition; no old animal O(N) moment is invoked. The positive comparison state has canonical logical identity, basin support, and the required moment. Its exponentially small initial channel error remains small under subsequent physical CPTP evolution.

### Boot to live activity without an exponential-norm mistake
A trace-distance error alone cannot transfer an exponential BUSY moment, because ||G_busy|| grows exponentially. There are two valid routes, neither of which is assumed silently.

First, the positive warm comparison state is supported on the primitive low mask, so M_busy<=k_P alpha_boot N there; its initial BUSY moment is bounded directly. Propagate that positive comparison and transfer only the eventual bounded BUSY EVENT to the actual channel.

Alternatively, use a direct full-state moment at boot. Globally M_busy<=k_P D_prim, and the activity upper bound gives

    G_busy<=exp(K delta_A k_P D_prim).

Choose the boot product parameter so log(1+theta)>=K delta_A k_P (shrink the proof parameter delta_A if useful). For the projection reset modules,

    exp(K delta_A k_P D_prim)<=H_boot.

Equation (4.2) then directly bounds Tr(G_busy rho_boot) on the FULL physical boot output. A sufficiently long fixed dwell makes this coefficient as small as the desired live BUSY barrier; eta is chosen afterward. Subsequent activity contraction is valid for this earned nonzero initial moment. This earns live eligibility without pretending boot gives an exact all-ready state.

## 7. Noncircular simultaneous choices
One consistent order is:

1. Fix code/global-radius and physical Hilbert-space interfaces, the nominal fast apparatus, new aborts, fresh dirty coefficients and fixed later zeta. Fix the declared detector/reset resources and reliable classical/control boundary.
2. Fix analytical s,R, a strict global basin and output margin, DATA proof c,d, and activity delta_A. Restrict to a small epsilon ceiling where the accepted local constants are uniform and g,q_t leave a fixed warm-gap margin.
3. Choose positive boot densities alpha_boot,gamma_boot satisfying (6.3)–(6.4), and output densities alpha_mem,beta_ctrl,beta_0,beta_inc,gamma satisfying the strict correctable output radius. Choose the global-module theta values and all fixed reset/preparation/detection dwells and physical ramp durations. Completion rates are actual fixed nominal module rates; no actual hot module service is assumed.
4. Choose ONE physical epsilon below the ceiling and small enough for the accepted memory, live BUSY barrier, and finite first-edge access integral epsilon Delta_first.
5. Choose ONE positive eta below the global memory/BUSY sources, every global-module moment floor, and the boot/access/readout integrated-Dyson thresholds. All durations are already finite, so such a positive choice exists. Set the unknown defect fraction below eta/(c_def R) if using that concrete interpretation.
6. Enlarge N0 for bounded support, rounding, distance and energy margins.

No physical parameter is retuned differently in different observables. If numerical rates/noise had already been committed, the additional inequalities must be checked at those values; a qualitative old receipt is not numerical certification. The controlled-boot switch remains exactly the declared operation from its source; this review supplies no new switch hardware.

## 8. Hidden-per-site audit summary and limits
The per-site uses found were the old subset laws for boot raw labels, pointer preparation, detector waiting, and some program/carrier readiness assertions. They are NOT preserved. Sections 4–6 replace the ones needed for global boot and BASE finite readout. Native retirement's overlapping witness hierarchy is likewise not generalized; live BUSY removes the need for that dwell.

The global memory/activity drift, local canonical edge identity, physical killing, Duhamel norm tail, finite support propagation, positive common-span replacement, actual classical event filter and deterministic adversarial decoder use only fixed support size plus the total norm budget. These load-bearing steps survive, as proved above.

The ordinary comparator must be equally strong: a distance-d code already corrects arbitrary coherent errors on an unknown support of size less than d/2, and an equally resourced scheduled QEC/readout implementation may exploit the same global error budget and code properties. No new adversarial decoding principle, historical priority, numerical yield, speedup or separation is established. The earned capability here is the complete declared native continuous-memory/global-output construction under this larger allocation class, not a claim that unknown defective qubits are intrinsically beyond standard QEC.

The old stochastic LOCC/ancestor-service theorem, old source waiting assumptions, bare unknown-input encoding, arbitrary warm logical entry, adaptive stopping access, noisy global classical control, and undeclared loss/unbounded faults remain excluded. All previously accepted sources and receipts are untouched.
