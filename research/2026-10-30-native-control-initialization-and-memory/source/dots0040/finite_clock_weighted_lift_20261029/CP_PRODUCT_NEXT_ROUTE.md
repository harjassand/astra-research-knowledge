# Local CP-product resummation route — NOT YET PROVED

The linear positive credit gives a real clean drift but fails under arbitrarily weak local noise for large animals. A concrete alternative avoids disconnected expansions.

1. Start with the exact clock-only Poisson solution from CLEAN_LINEAR_LIFT.md. Exponential weighted coefficient contraction should permit a fixed-radius truncation B_h satisfying 0<=B_h<=t M I and
L_clock* B_h=-t kappa(n_h-p_h I)+E_h,
||E_h||<=t delta, delta<<kappa p_min.
One must prove a bound on the generator applied to the tail, not merely its operator norm; the integrated weighted-support norm is the relevant input. A scalar shift imposes positivity. For isolated clocks a negative-semidefinite choice needs only O(t(g/kappa)^2) ready-sector shift, while the excited-sector coefficient is O(t).

2. With tM<1, define a LOCAL unital CP supermap on the full clock/data observable algebra:
T_h(O)=sqrt(I-B_h) O sqrt(I-B_h)+sum_s K_hs^* sqrt(B_h) O sqrt(B_h) K_hs.
Clock-only B_h commutes with K_hs. On data-only V this gives T_h(V)=V-B_h d_h. This is positive without a first-order additive lower-bound estimate.

3. Color the enlarged supports (radius fixed independently of volume), and compose these maps in a fixed bounded number of disjoint layers, T=product T_h. Apply T separately to every animal, F_A=T(f_A). Positivity is exact. Each local map has an identity branch bounded below by 1-tM, so the crude global lower loss is exp(-C t|A|), independent of theta. A bounded-depth causal-cone argument should yield a uniform single-local-error relative condition number, rather than a condition number growing with |A|; this must be checked explicitly for the noncommuting CP maps.

4. Crucial algebra: analyze
L* T V=T L* V+[L*,T]V.
For genuinely disjoint enlarged supports [L_j*,T_h]=0 EXACTLY, including their reset/data actions. Thus a commutator expansion is linked/local; expanding L* of a first-order sum hides this and creates apparent disconnected |A|^2 terms. Fixed circuit depth makes support enlargement bounded.

5. The missing estimate is a SIGNED, weighted local commutator bound. The desired leading Poisson term supplies -t kappa p_h d_h while imperfect cancellation of -kappa n_h d_h leaves service slack. Local overlaps must be bounded by that slack or by a small multiple of sum d_h. Mere operator norm bounds O(t kappa) are insufficient, since the favorable strict rate is O(t g^2/kappa). In particular n_j d_h cannot automatically be charged to n_j d_j: hub j may be inactive on the data yet its excited clock blocks h. The exact Poisson solution accounts for this at linear order, but the CP-product commutator may reintroduce such terms. This is the actual unresolved proof obligation.

Even a successful clean CP-product argument still needs a full-Hilbert physical extension accounting for complementary Kraus labels and illegal occupancies, or a combined positive defect/barrier construction. Neither issue is solved by mean defect damping alone.
