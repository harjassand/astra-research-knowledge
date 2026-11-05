# Current forward status and constants (for root)

Full current acquisition contract is written at passive_MEASUREMENT_CONTRACT.md (not merely an interface). It closes raw-force/nonlinear subtraction, finite bins, no-reset offsets, noise, force and slew, and both random-sign and aged-baseline modes.

1. Triangular support 2w, mean delay w, quintic ramp delay h/2: Kstar is positive CM and ||K-Kstar||_1 <= B(h/2+w).
2. Aged baseline test on [H-2w,H], ramp [H,H+h], post test [H+h+t,H+h+t+2w]: old-force bias <= G(h+t+2w)/(e(H-2w)). This is the *mean separation*; it is tighter than using the support endpoints. Requires H>2w and G bounding initial hidden L1 force at the start of this quiet hold.
3. Memory tracking error per test <=2B delta, hence baseline subtraction <=4B delta. Nonlinear subtraction adds at most 2 Omega(delta), where Omega is computable from V' at c, c+A and their +-delta neighbors. Raw f,x meters suffice; no net-force channel.
4. Fine-force quadrature error <=Fmax/n per test with d=w/n. Thus baseline difference costs 2Fmax/n. Force/position calibration bias costs 2 epsilon_f+4 epsilon_x/w. Gaussian meter proxy per test is <=2v_f/(3w)+2v_x/w^3. Baseline difference proxy <=2 v_meter, so uniform nodal random error sqrt(4 v_meter log(2M/alpha)/(R A^2)).
5. Velocity-only feedforward is sound: q=c+u+[u'+V'(c)]/k removes U from D. Need a ramp with u,u',u'',u''' suitably vanishing at splice if q is to remain C2. Quintic u has u''' endpoint jumps, so q'' has finite jumps; bounded acceleration a.e. still holds, but a septic smoothstep gives C2 q with zero endpoint velocity/acceleration. Use u= A[35s^4-84s^5+70s^6-20s^7]. Constants can be safely bounded or computed exactly. Force |f|<=|V'(c)|+U+k delta; q speed<=U+U2/k, acceleration<=U2+U3/k. During every measured hold u'=0, so the bin formulas are unchanged.
6. Initial alignment: prior fixed-q guard contract already works if initial q0 is given, paying force kR0. Root's optional stiffness ramp is valid in y=x-z representation but is an additional actuator operation if only fixed k and moving q were originally allowed. We should present fixed-k centering as default or explicitly add stiffness programmability. Finite fixed-q guard can choose c as unique equilibrium c+V'(c)/k=q0; no assumption c is the V minimum is needed. It gives R0=max(d0,G/(k+mu)), Gprep=G+2B R0, |x-c|<=d0 exp[-(k+mu)t]+Gprep/(k+mu). Subsequent acquisition uses Gprep. No hidden gap is used.

Parent is building the joined fixture; I am not duplicating it. Preparing rigorous full proof and explicit feasibility/resource selection next. No claim of an interval-validated physical ODE is being made.

### Two corrections / exact constants

* In the optional y-coordinate centering formula, the damping is k+mu+b_true, where b_true=nu([0,infinity)). If B is only an upper bound, it cannot replace b_true in a favorable damping term. Safe uniform formula uses k+mu and forcing Gy0+B X. This changes no qualitative conclusion, but matters in the theorem. My fixed-k guard already uses only k+mu.
* Septic smoothstep constants: C1=35/16, C2=84/(5 sqrt(5)), C3=105/2. With k>=1/h, choosing A<=min[Smax*h/(C1+C2), amax*h^2/(C2+C3)] guarantees feedforward q speed/acceleration caps. q travel per complete probe is <=2A+4U/k, not exactly 2A; corresponding absolute actuator-work bound is Fmax(2A+4U/k). Pure moving-center protocol without velocity feedforward has travel exactly 2A.

A 182-mode independent algebraic check (frozen mode plus rates 10^-12..10^12) and exact finite-bin variance checks are in passive_verify_bounds.py and passive_bound_checks.json. Root's nonlinear joined fixture is not duplicated.

### Optional physical sensor response (not needed if allowed meter primitive is the declared bin average)

If a load cell or position meter first applies a known positive normalized causal filter with mean delays tau_f,tau_x, this can be paid without any bath-rate cutoff. For a normalized triangle phi=psi/w, ||phi'||_1=2/w. Hence force filtering adds at most 2 Fmax tau_f/w per residual, by shifting the test function rather than differentiating the unknown force. Position filtering adds at most 2 W_x tau_x/w, where W_x is the certified actual position-speed bound. With velocity feedforward, W_x<=U+k delta+F_V(A+delta)+Gstar (plus actuator error). These are additive deterministic metrology terms, doubled for baseline subtraction and divided by A. Fixed bandwidth creates an explicit accuracy floor; selecting finite faster sensors is a paid resource choice. The original finite-bin-average measurement primitive is already enough for the clean theorem.

### Force-sign convention

For x'+V'(x)+m=f and raw external f, R=weighted(f)-V'(command)-position-difference/w estimates +m. Therefore the positive kernel estimate is (R_post-R_base)/A for a +A ramp. Baseline-minus-post has the opposite sign unless the meter explicitly reports the reaction force -f.

Main full proof now saved as passive_FULL_PROOF.md. It includes fixed-k initial alignment (and finite root residual), programmed velocity feedforward with septic constants, the explicit finite-bin/noise contract, old-force aging, finite sensor-response allowances, ADC range/bit costs, complete resource feasibility, and handoff to the unfiltered passive residual certificate.

### Arbitrary rational nodes: corrected join

Main proof and measurement contract now use M arbitrary rational starts t_i, t_max<=T. Aged source time is guard+R[H+2h+t_max+2w]. Including baseline, conservative counts are 2R(M+1) position boxes and 2nR(M+1) force boxes, plus separate future-initialization measurements. The aged drift numerator is h+t_max+2w. Shared windows retain the same per-node white-noise proxy; no node independence is assumed. Endpoint merging/cumulative-integrator implementation, O(Mn) update/O(M) accumulator bill, finite clock resolution and cumulative-readout precision conversion are explicit. The monotonicity-only kernel handoff now uses 2B Delta with Delta the actual maximum fitting-node gap, rather than 2Bw.

For the root fixture M=96,n=404878, the aged acquisition's conservative requested counts are 194 position boxes and 78,546,332 force boxes, before separate initialization readouts. These counts are theoretical execution resources, not a claim that the emulated fixture materialized all records. All main-contract lattice/Q references are now removed; interpolation uses actual Delta, not w.

The arbitrary-node join has now been independently checked with exact rational polynomial integrals: shared cumulative reduction equals separate force-box sums exactly; the position identity is exact; overlapping nodes have explicitly nonzero noise covariance; all finite-clock signal/variance bounds pass. Files: passive_verify_arbitrary_nodes.py and passive_arbitrary_node_checks.json. This is a small algebraic execution check, not a duplicate source simulation.

### Completed finite release handoff

RELEASE_HANDOFF.md is written. The requested delta_rel and gamma_rel are proved, using one global G to bound both hold-start and release-start hidden y envelopes. The Bdelta_rel term covers the entire hold+release integral; no extra Bdelta is added there. Actual viscous-support force, stiffness/force slew, parameter work/power, support travel/work, finite query approximation, normalized Gamma=1 calibration, and the resulting trajectory bound are included. The optional sensor-delay correction now explicitly uses F_history/global frontend range, rather than F_hold unless support/clearing is certified.
