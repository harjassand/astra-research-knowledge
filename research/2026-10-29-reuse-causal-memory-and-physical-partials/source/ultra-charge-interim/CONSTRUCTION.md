# Exact charge-sector Gaussian trajectory construction

29 October 2026. Root constructive extension of A's independently selected
positive Gaussian representation. Internal derivation; novelty and practical
superiority are UNESTABLISHED. This is an actual restricted noisy-system
simulation operation, not a noiseless many-body solver.

Let n=(n_1,...,n_m) be fermionic occupations and let

  H = H_0 + (1/2) n^T U n,
  L_Gamma(rho) = -(1/2) sum_ij Gamma_ij [n_i,[n_j,rho]],

with real symmetric U, real PSD physical Gamma, and number-conserving
quadratic H_0. More generally H_0 preserves diagonal charges C^T n.
The initial Gaussian state and all subsequent states are supported in a
single sector C^T n=q. C has linearly independent columns; Q has orthonormal
columns spanning ker(C^T). Charges must be genuinely preserved, not inferred
from a small mean or approximate conservation law.

For any real s and V, define

  U' = U + diag(s) + C V^T + V C^T.

On this sector, the added Hamiltonian is the quadratic operator
g^T n, g=s/2+Vq. Replace H_0 by H_0-g^T n. No interaction has been erased
outside the stipulated sector. On every sector coherence a,b,
C^T(a-b)=0, so dephasing only depends on Q^T Gamma Q.

Choose D=diag(d)>0 satisfying

  Q^T [Gamma - D - (1/4) U' D^-1 U'] Q >= 0.              (1)

This is sufficient for exact positive Gaussian trajectories of the
interaction-plus-dephasing channel at ANY finite time step. An equivalent
affine block LMI is

 [ Q^T(Gamma-D)Q     (1/2)Q^T U' ] >=0.                 (2)
 [ (1/2)U' Q                  D ]

Thus, for Gamma=gamma Gamma_0, finding a certificate and minimizing gamma
over d,s,V is an SDP, not a many-body state search. Strict d_i>0 is required
for this sampler; numerical optimization needs a positive floor and slack.
We do not claim (1) is necessary for all possible Gaussian decompositions.

## Explicit finite-step instrument and proof

For a step h>0, use reference measure y~N(0,h I) and the positive diagonal
measurement operator

 M_y = exp[sum_i (sqrt(d_i)y_i - h d_i)n_i].

Its squared average is I because n_i^2=n_i, so it is a normalized instrument.
Follow it by the Gaussian phase feedback

 F_y = exp[-i (1/2) n^T U' D^-1/2 y].

For occupations a,b, let delta=a-b and v=a+b. Gaussian integration gives

 E[(F_y M_y)_aa conj((F_y M_y)_bb)]
 = exp[-ih/2(a^T U'a-b^T U'b)
       -h/2 delta^T (D+(1/4)U'D^-1U') delta].            (3)

The real exponent follows by expanding (sqrt(D)v-i D^-1/2 U'delta/2)^2/2
and using a_i^2=a_i, b_i^2=b_i. Symmetry of U' gives
v^T U'delta=a^T U'a-b^T U'b. This proves (3) for every density matrix entry,
at finite h; there is no Euler approximation or signed trajectory weight.

Let S=Gamma-D-U'D^-1U'/4 and R=Q(Q^T S Q)Q^T >=0. Append an independent
Gaussian phase exp(-i n^T z), z~N(0,h R). For all a,b in the sector,
delta^T [D+U'D^-1U'/4+R]delta=delta^T Gamma delta. Together with the quadratic
gauge correction, (3) is exactly the desired finite-step channel.

Each Kraus operator is exp(sum_i complex alpha_i n_i), a fermionic Gaussian
operator. A pure fixed-charge Slater determinant stays a normalized Slater
determinant in each trajectory. A supplied efficiently sampled mixture of
such states is also allowed. This does NOT supply a Gaussian decomposition
for an arbitrary initial correlated state.

The outcome law must be sampled with density ||M_y psi||^2 relative to the
reference Gaussian, not sampled unweighted. Sequentially, y_i is a mixture
of N(0,h) and N(2 sqrt(d_i) h,h), with occupation probability from the CURRENT
conditional Gaussian state. Apply M_{y_i}, normalize, then continue; at the
end apply F_y and the independent R phase. This avoids importance weights.

H_0 generally does not commute with the interaction channel. Alternate its
Gaussian unitary with the exact finite-step channel and pay a product-formula
error (or prove an improved integrator). Finite h in (3) does not make the
FULL noncommuting dynamics exact. Observable estimates pay sampling error,
initialization, matrix updates, numerical conditioning and output costs.

## Exact family and what it changes

For fixed total N, C=1 and P=I-11^T/m. Let W be a symmetric normalized
Sylvester Hadamard matrix, W^2=I, with m a power of four so W is rational.
Take U=W, U'=PWP (a permitted charge gauge), Gamma=P, D=I/2. Then

 P[D+U'D^-1U'/4]P = P/2+(PWP)^2/2 <= P.

Indeed P-(PWP)^2=PW(I-P)WP >=0. The residual R is exactly
PW(I-P)WP/2, rank at most one. Thus the source's singular physical noise
has an explicit positive Gaussian trajectory representation. A full-space
PSD test with Gamma=P and D>0 would fail on the conserved all-ones direction;
that is an artifact of ignoring the fixed sector.

The ordinary edgewise local allocation pays sum_{j!=i}|U_ij|=(m-1)/sqrt(m),
whereas Gamma=P is equivalent to independent rate-one dephasing on the
fixed-total-number sector. The growing sufficient-threshold separation is
against that edgewise condition, NOT a runtime separation against every
equally informed classical algorithm. Dense signed interactions remain
genuinely quartic modulo charge gauges for m>=4: the leading four Walsh
indices obey U_01+U_23-U_03-U_12=-2/sqrt(m), whereas an additive one-body
potential on every two-particle configuration makes that expression zero.
The code checks the complete k=2 channel and additive-potential residual
at m=4,16, but the displayed witness is an all-size algebraic argument.

### Equally informed edgewise comparator: an all-gauges separation

Give the pairwise noise-allocation incumbent the SAME fixed-charge gauge:

 gamma_edge = min_v max_i sum_{j!=i}|W_ij+v_i+v_j|.

Diagonal shifts are already irrelevant to this objective. Even this stronger
incumbent has gamma_edge >=

       (m^2-4m+2)(m-2) / (m^2 sqrt(m)) = Omega(sqrt(m)).    (4)

Proof: let E_ij=H_ij for i!=j, E_ii=0, H=sqrt(m)W. For the Sylvester matrix
H_0j=1, H^2=mI, tr H=0. Its off-diagonal row sums are e_0=m-1 and
e_i=-H_ii (i>0), so sum_i e_i=m and sum_i e_i^2=m(m-1). Put

 a_i = -e_i/(m-2)+m/[2(m-1)(m-2)],
 B0_ij=E_ij+a_i+a_j (i!=j), B0_ii=0,
 M=m^2/[(m-1)(m-2)], B=B0/M.

Every row sum of B is zero. For i,j>0, |B0_ij| is at most
1+(3m-2)/[(m-1)(m-2)]=M. For the first row, cancellation of H_0j=1
with a_0=-(2m-1)/[2(m-1)] leaves either -1/(m-1) or
m/[(m-1)(m-2)], also at most M. Thus |B_ij|<=1.

For any v, multiply each pair residual by B_ij and sum. Gauge terms vanish
because rows sum to zero, and

  (m/2) max_i sum_{j!=i}|W_ij+v_i+v_j|
     >= sum_{i<j}|W_ij+v_i+v_j|
     >= sum_{i<j}W_ij B_ij
      = [m(m-1)/2 + sum_i a_i e_i]/[sqrt(m) M].

Here sum_i a_i e_i=-m(2m-1)/[2(m-1)]. Substitution gives (4).
This is an explicit feasible LP dual for ALL sector gauge choices, not a
comparison against unprocessed coefficients. At m=16 the rational lower
bound is 2.65234375; at m=64 it is 7.2694091796875, versus the global
construction's sufficient rate 1. Numeric LP optima are diagnostic only.

This proves a growing separation between two constructive SUFFICIENT
noise thresholds. It does not prove the optimized pairwise allocation is
the strongest classical simulator, nor prove an impossibility below that
threshold for the prior paper or other Gaussian representations.

## Prior and current boundary

Gonzalez-Garcia, Gorshkov, Cirac, Trivedi, PRL135,190401 (2025),
arXiv:2502.05658v2, establishes convex-Gaussian noisy interacting fermion
simulation; Lemma4 and the many-mode decomposition already pay edgewise
dephasing. Measurement/feedback noise-versus-interaction tradeoffs are
older: Kafri-Taylor-Milburn (2014), Tilloy-Diosi and Gaona-Reyes et al.
arXiv:2007.11980. Those mechanisms are PRIOR, not claimed as new.
This note's candidate contribution is the exact charge quotient plus
gauge-optimized constructive LMI and its finite-time sector sampler.
A's global correlated-noise criterion is the load-bearing unquotiented
primitive. Broader priority, strongest-incumbent runtime, and usefulness
on consequential material/chemical models remain OPEN.

No physical simulator was operated. No noiseless quantum-computation claim,
novel scientific principle claim, or civilisation-level result is warranted.
