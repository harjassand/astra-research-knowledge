# Finite-volume rotor compression from an explicit canonical trial

Scope: a finite-volume implementation with cutoff/range allowed to depend on volume. This is NOT a volume-independent finite-onsite-dimension regulator theorem.

Let H_R be the exactly symmetric finite-range truncation, with proved unique ground energy E_R and gap gamma. Choose the radius also so ||H_R-H_sym||<=delta globally; the interaction tail bound gives this with R=O(log(V/delta)) at fixed paid locality constants. The explicit canonical state Psi=W(|+> tensor Bell) then obeys

 <Psi,H_R Psi>-E_R <=2delta.

The original exact parent need not be solved again. Its vector Psi(phi) is explicitly given by the finite-dimensional Gaussian exponential and has pointwise norm1.

## Fourier approximation despite rounding walls

For each rotor v, varying phi_v while fixing all other angles crosses a finite number J_v of floor/rounding walls. The bound J_v is acquired from the finite local cochain formulas, not assumed from smoothness. Between those walls the actual barycentric texture has bounded derivative: the audited lower spinor norm0.336 controls normalization, and all unnormalized trigonometric derivatives are explicit. The uniformly gapped covariance has a bounded derivative within each chamber. A conservative finite-volume estimate suffices: the Fock norm of a quadratic generator derivative is bounded by a fixed constant times the number D of fast modes times its one-particle norm. Thus the explicit canonical Gaussian exponential has a computable derivative bound L_v (one may pay a factor D); decoration matchings are constant inside their chambers. No derivative across a wall is invoked.

With normalized Haar measure, crossing a wall under angular translation t occurs on measure at most J_v |t|/(2pi). On that event the squared state difference is at most4. Else integrate the within-chamber derivative. Therefore, for sufficiently small |t|,

 integral ||Psi(phi+t e_v)-Psi(phi)||² dphi
 <= A_v |t|+B_v t²,
 A_v=2J_v/pi, B_v=L_v².

A harmless enlargement covers periodic branch cuts and any additional explicitly identified local walls. The key required implementation check is enumeration of those walls; this note is not a substitute for that finite enumeration.

Let Psi_hat(n) denote Hilbert-valued angular Fourier coefficients. Parseval and averaging t over[0,1/K] give

 sum_n 2[1-sin(n_v/K)/(n_v/K)]||Psi_hat(n)||²
 <= A_v/(2K)+B_v/(3K²).

For |n_v|>K the bracketed coefficient is >=c0=2(1-sin1)>0.317. Thus the rectangular Fourier projection P_K onto |n_v|<=K for every rotor obeys

 ||(1-P_K)Psi||² <= (1/c0) sum_v [A_v/(2K)+B_v/(3K²)].

This is a constructive algebraic Fourier-tail bound, not an incorrect Sobolev-H1 claim for a discontinuous rotor state. Normalize chi_K=P_K Psi/||P_K Psi||. If the tail is t_K, then ||chi_K-Psi||<=sqrt(2t_K).

## Minmax gap certificate for compression

Let B>=||H_R|| be a known finite-volume norm bound. Then

 <chi_K,H_R chi_K>-E_R <=2delta+2B sqrt(2t_K) = e.

The compression H_R,K=P_K H_R P_K has lowest eigenvalue at most E_R+e. By the minmax principle its second eigenvalue is at least E_R+gamma. Consequently, if e<gamma, it has a unique ground and gap at least gamma-e. This does not approximate all bounded-reset low-energy states; it uses just one accurate ground trial and the original spectral gap.

Exact symmetry is preserved only if the cutoff projection commutes with the FINAL onsite symmetry representation. For a gauged subgroup one must first earn the actual anomaly-free onsite disentangler and transform both Hamiltonian and trial; a generic bare angular cutoff before that step need not commute with the anomalous controlled symmetry. A supplied abstract disentangler is not silently assumed here. If that finite local circuit has explicit piecewise-smooth coefficients with finitely many walls, the same translation-modulus argument applies to its transformed trial, with paid new J_v,L_v.

The final finite-dimensional matrix entries can be acquired by finite angular integrals of explicit bounded piecewise-smooth kernels, with wall partitions retained. The cutoff size and R may grow strongly with V, D, inverse gap and requested error; no practicality claim follows.

## Actual texture constants (direct code/formula inspection)

In piecewise_texture.py every rounding wall is an edge difference phi_u-phi_v=pi modulo2pi, with u,v vertices of a common coarse tetrahedron. Thus J_v is at most the degree of v in the fixed coarse simplicial1-skeleton; this is directly enumerable from the mesh. No new walls arise from normalization because its denominator has the audited positive lower bound m0. Between walls each barycentric vertex phase is a convex average of selected rotor phases (or one anchor phase). In RADIAN units its derivative coefficient lies in[0,1]. Barycentric spatial weights are nonnegative and sum1, hence ||partial_v q_raw||<=1. Normalization, regarded as the usual real Euclidean radial map, gives ||partial_v q||<=1/m0. A conservative certified choice is m0=cos(3pi/8)/sqrt(2), without needing the sharper bound elsewhere.

For the SU2 matrix this gives ||partial_v U||<=1/m0 and the disjoint onsite mass entries give ||partial_v h||<=M/m0. The imaginary-resolvent formula for the flattened gapped Hamiltonian bounds ||partial_v sign(h)||<=||partial_v h||/g. Summing the quadratic Gaussian generator in D fast modes and differentiating its finite-angle exponential yields, conservatively, L_v<=10 D M/(g m0), with fixed extra factors if the chosen D convention excludes Nambu/copy multiplicities. Counting all doubled Majorana modes in D is safe. The decoration covariance is piecewise constant between the same matching walls. These bounds close J_v,L_v for the ORIGINAL canonical trial. A later onsite disentangler still needs its own explicit regularity audit.
