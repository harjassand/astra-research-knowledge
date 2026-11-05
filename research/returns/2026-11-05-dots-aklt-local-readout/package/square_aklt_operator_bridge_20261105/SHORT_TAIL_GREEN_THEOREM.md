# A certified short-loop / all-length-tail Green comparison

## Result

Split routed loops into 60 D4/translation types of length at most 12, and the tail of all lengths at least 14. The exact all-loop certificate permits the following stronger block comparison at the same positive tilt μ=log(1000001/1000000):

- Tail-to-tail length-weighted norm is less than 0.330151.
- A rational type-weighted norm of the FULL raw ancestor kernel is less than 0.907806.
- The nonlinear short-type Schur comparison has norm less than 0.857586; its weighted Green bound is at most 500000/71207, about 7.022.
- A separate inhomogeneous source-one Green supersolution bounds the expected number of true candidate cylinders in all time-zero root ancestor clans by 0.466967N for an N-vertex finite box. Summing separate root clans overcounts their union, so this also bounds the union.
- The past-depth tail is bounded by 1.733198N exp(−0.046097t).

These bounds include all loop lengths. They do not include null sampler proposals or work per oracle call, and do not yet retain boundary height or path-source geometry. They are not a quantum-gap estimate.

The improved full-kernel norm uses weights a(γ)=L(γ)v_type for short loops and a(γ)=L(γ) for long loops. It is NOT legitimate to substitute 0.907806 for the earlier unmodified-length q while leaving all earlier length-normalization constants unchanged.

## 1. Tail moments

All moments below use the tilted target activity w(η)exp(μL(η)). Subtract the EXACT short-loop moments from the certified total upper caps:

  S_tail <0.241735230502,
  T_tail <0.506702142772,
  M4_tail <0.028452299271.

This subtraction is rigorous: true_tail=true_total−exact_short≤total_upper−exact_short. It does not require the positive majorant's short coefficients to equal the true coefficients. Any extra short artifacts make the result looser, not invalid.

The exact short moments are

  S_short=0.282208679309736...,
  T_short=1.183480010064811...,
  M4_short=0.018078717009343....

Define

  A_s=S_tail/5+T_tail/2,
  A_t=S_tail/2+7T_tail/20,
  d=A_s+M4_tail.

The total moment caps were rounded upward to rational decimals from the independent interval certificate before subtraction. All subsequent arithmetic is exact rational.

For a long root, the identical simple-loop target is absorbed by its at least four turning visits. The needed inequality is only

  A_s−A_t ≥ (3·14/4)x^14,

where x=exp(μ)/3, because L≥14 and Lx^L decreases thereafter. This is checked exactly. Thus d<0.330151 bounds raw tail-to-tail influence, including self-exclusion.

## 2. The finite short kernel

For short root type i and target type j, enumerate all distinct D4 orientations of j and every translation touching i. Define the exact unnormalized coefficient

  C_ij = w_j Σ_placements[1−δ(i,j_placement)].

The identical placed loop is INCLUDED. This is the raw ancestor coefficient, not the sharper heat-bath coefficient. Every coefficient is recomputed as an exact rational count of hard overlaps and soft contacts, and saved in raw_short_matrix_exact.json.

The normalized tilted short matrix is

  B_ij = (L_j/L_i) exp(μL_j) C_ij.

The full 60-type finite raw matrix has numerical spectral radius about 0.542813 before the extra length tilt. Smaller previously reported heat-bath radii must not be used for this proposal-ancestor comparison.

## 3. Short-to-tail rows

For a short root of length L_i, count its routed straight and turning visits n_s(i),n_t(i), including both visits to a degree-four vertex. Its local tail charge is

  [n_s(i)A_s+n_t(i)A_t]/L_i.

For a simple root, union-bounding the possible degree-four attachment gives coverage M4_tail. For a nonsimple root, choose any one of its degree-four vertices; every covering target must have degree four there, so the coverage contribution is only M4_tail/L_i. There is no identical-loop term because the target is long.

Call the resulting exact rational upper row b_i. Its range is approximately [0.30058439,0.32898884].

## 4. Long-to-short rows

Coverage is impossible: a target with at most 12 edges cannot contain the edge set of a root with at least 14 edges.

For each short target type j, compute its full-plane degree-two straight and turning local moments s_j,t_j. If o_j is its number of distinct D4 orientations and n2s(j),n2t(j) its numbers of degree-two straight/turn vertices, then

  s_j=L_j w_j exp(μL_j)o_j n2s(j),
  t_j=L_j w_j exp(μL_j)o_j n2t(j).

For arbitrary nonnegative type caps u_j, the long-root row is bounded by the larger of

  A^s·u,  A^t·u,

where A^s_j=s_j/5+t_j/2 and A^t_j=s_j/2+7t_j/20. The sums of these vectors are approximately 0.648181741 and 0.555322344.

It is important to retain the maximum of these two linear forms. Choosing whichever branch dominates one numerical Perron vector does NOT make that branch an entrywise upper kernel for all other sources.

## 5. Positive nonlinear comparison and Schur elimination

For u=(u_S,u_T)≥0 define

  F_S(u)=B u_S+b u_T,
  F_T(u)=max(A^s·u_S,A^t·u_S)+d u_T.

If a function on actual placed loops is bounded by L(γ) u_type, applying the full tilted raw kernel is bounded by L(γ)F(u)_type. This holds in every finite region and under arbitrary activity suppression.

The code selects positive type weights numerically, rounds them to rational numbers, then checks EVERY comparison inequality with exact fractions. It verifies

  F(v) <0.907806v.

The short factors lie between 0.711122124 and 0.937475399, and the tail factor is one. The minimum actual loop weight a(γ)=L(γ)v_type is 937475399/250000000, attained by the plaquette type.

For sources supported on the short block, eliminate the tail exactly in the comparison:

  S(u)=B u+[b/(1−d)]max(A^s·u,A^t·u).

A separate rational positive vector v^S verifies

  S(v^S)<0.857586v^S.

Hence the monotone Schur Green comparison has weighted norm at most 1/(1−0.857586)=500000/71207. With a nonzero tail source g_T, first add b g_T/(1−d) to the short source, then recover the tail cap [g_T+max(A^s·u,A^t·u)]/(1−d).

This is a nonlinear monotone comparison theorem. It is not a claim that an arbitrarily chosen single 61×61 matrix dominates all spatial sources.

## 6. Source-one resource certificate

To count all ancestors of a fixed root, including that root, solve the normalized source-one comparison with source components

  g_i=1/L_i for short types,  g_T=1/14.

A positive rational vector u is checked directly to satisfy u≥g+F(u). It therefore bounds the actual raw Green function for counting ancestors by L(γ) u_type. This is an inhomogeneous supersolution, not just a spectral-radius claim.

For short type j, the full-plane time-zero root intensity times root length per lattice vertex is

  r_j=o_j L_j w_j exp(μL_j).

The total tilted root-length density is bounded by

  R=6(G_s+G_t)+(18/5)(2G_s²+G_t²)<0.299599123984.

The tail density is at most R−Σ_short r_j. Therefore

  E[sum of root-clan sizes]/N
  ≤ Σ_short r_j u_j+[R−Σ_short r_j]u_T
  <0.466967.

All root clans may overlap; summing them only increases the union count. The count refers to true loop cylinders after the physical loop-birth thinning, not to all automaton attempts, rejected walks, or global clock proposals.

For physical-time depth, let q_A=0.907806 and θ=(1−q_A)/2=0.046097. An ancestor edge's time-gap exponential moment contributes 1/(1−θ), and the root's stationary age contributes another such factor. Marked path counting and the minimum a-weight give

  P(any required birth time is earlier than−t)
  ≤ [R/(a_min θ)] N exp(−θt)
  <1.733198N exp(−0.046097t).

The time unit is the mean-one candidate lifetime used in the loss-network construction.

## 7. Reproduction and remaining use

Run certify_short_tail.py from the shared workspace root. It recomputes or reads the exact finite raw matrix, builds all rational tail bounds, checks both homogeneous norm certificates, and verifies the source-one inhomogeneous inequalities. Artifacts:

- raw_short_matrix_exact.json
- short_tail_exact_certificate.json
- short_tail_source_resource_certificate.json
- certify_short_tail.py

The target for the quantum boundary problem is still more demanding: retain path-source positions and boundary height in the Green kernels, and fit their full marked-tree sum into the residual long-path operator budget. The present type-only improvement does not establish that inequality.

## Independent conceptual audit

A separate reading checked the tail subtraction, impossible long-to-short coverage, fixed degree-four-site short-to-tail bound, preservation of the max of two tail geometries, visit-count root density, type-weight normalization, and root-age/time-tail factor. No conceptual or multiplicity error was found. The exact rational numerical checks remain reproducible in the supplied script.
