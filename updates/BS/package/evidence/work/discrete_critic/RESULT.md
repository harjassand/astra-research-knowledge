# Independent discrete-time audit and finite observable separation

Status: internally derived proof with exact finite algebra and exhaustive word-range replay. No external certification, priority claim, practical acquisition claim, or historic breakthrough. The construction changes the source continuous-time process; neither discrete model below is asserted to be a sampled version of the original CTMC.

## Result

The supplied rational ten-state generator Q defines two stationary ten-state, six-label chains P_e=I+eQ, e=1 and e=1/2. Each observed law is exactly time-reversal invariant and every reflected word-probability kernel has one common nonnegative ten-atom factorization. Nevertheless a single explicitly defined statistic W_e of five consecutive observed letters has nonnegative expectation for EVERY stationary reversible hidden Markov chain with deterministic emissions, regardless of hidden dimension, but strictly negative expectation for P_e.

The e=1/2 variant additionally has positive observable spectrum in [0,1]. Consequently every scalar observable autocorrelation is a positive mixture of powers lambda^n with lambda in [0,1], and its sequence is completely monotone. This stronger blind-spot variant avoids the negative observable eigenvalue of the faster e=1 variant.

| e | universal circle coefficient | universal square-root residual coefficient | exact witness target expectation (decimal display) | certified W range | sufficient independent windows, each error <=.025 |
|---|---:|---:|---:|---:|---:|
| 1 | 836/75 | 503 | -0.002972777578630545 | [-7,000,000, 16,000,000] | 503,210,463,733,650,416,172 |
| 1/2 | 664/75 | 796 | -0.001486388789315273 | [-29,000,000, 81,000,000] | 46,040,428,061,831,153,388,823 |

The sample counts are rigorous sufficient upper bounds for the specified test, not lower bounds on the acquisition problem and not demonstrated experiments. They remain wholly impractical.

## Source and finite verification

The source is work/hidden_equilibrium/certificate.txt; its SHA-256 is recorded in every exact report. We did not assume its analytic argument valid. seed_verify.py independently reconstructed the generator and checked 82 finite rational identities/inequalities using fractions.Fraction: row and column sums, nonnegative off-diagonal entries, P_1 nonnegativity, uniform stationarity, QH=HL, M=H^T H/10, ML=L^T M, rank H=8, circle points, CCW facets, flow formulas, monotonicity, negative pairing, geometry constants and interpolation bounds. All pass. No finite-algebra flaw was found.

The exact source row vectors are xi_i=(1,v_ix,v_iy,0^5) for five internal states, and xi_(5+k)=(0,0,0,e_k) for markers. The emissions are 0 internally and k+1 on marker k. Let eta=1/10, l_k(x)=a0_k+n_k dot x be the supplied inward facet functions. Put a=e eta (a0_k)_k and N=e eta (n_k^T)_k, a 5-by-2 matrix.

## Observable definitions and complete executable construction

Let C=(N^T N)^(-1)N^T, an exact rational left inverse. Using observed letters at times 0 and 1, define

- I0=1_{Y0=0}, psi_k=1_{Y0=0,Y1=k+1};
- (F_x,F_y)^T=C(psi-a I0);
- F=(I0,F_x,F_y,1_{Y0=1},...,1_{Y0=5});
- D=psi-a I0-N(F_x,F_y)^T;
- K=(I+eL)^T and G=U_1F-KF.

All-marker least squares reduces the finite-word range relative to every two-marker inverse that was tested. This is an implementation improvement within the same proved inequality; it is not a claim of global optimality. F uses two letters and G uses three. Reverse the time labels to obtain F^-,D^-,G^-; use forward labels for the plus versions. All following statistics depend on exactly the five observed letters at -2,-1,0,1,2:

p0=E I0;
s2=E[F_x^- F_x^+ + F_y^- F_y^+];
Rh=E[D^- dot D^+];
Rt=E[G^- dot G^+].

For each source point shift the supplied planar field by c=(4/5,0), writing ztilde_i=z_i-c and t_i=ztilde_i dot v_i. Define

Z_i=(-5t_i/6,ztilde_ix,ztilde_iy,(t_i/6)1^5), and Z_marker=0.

Let b_i=Z_i dot (I-K)xi_i. The unique rational quadratic

q(x,y)=q0+q1 x+q2 y+q3 x^2+q4 xy

satisfying q(v_i)=b_i is obtained by solving the nonsingular five-by-five moment matrix. Exact coefficients for e=1 are in SEED_CHECK.json and EXACT_WITNESS.json; the e=1/2 coefficients are exactly half. Define the observed linear statistic

Sq=E[q0 I0 + q1(F_x^-+F_x^+)/2 + q2(F_y^-+F_y^+)/2
       +q3 F_x^- F_x^+ +q4(F_x^- F_y^++F_y^- F_x^+)/2].

For e=1 set circle=836/75, Ch=503. For e=1/2 set circle=664/75, Ch=796. In both cases set

alpha=3e/1000, beta=e/125000,
Lambda=Ch^2/(4alpha), Mu=9/(25 beta),
W=Sq_integrand +circle*(I0-s2_integrand)
  +alpha*(I0+s2_integrand)+beta*I0+Lambda*Rh_integrand+Mu*Rt_integrand.

This is a fully specified rational statistic; no hidden variable enters its evaluation. Explicit penalty coefficients are:

- e=1: Lambda=63252250/3, Mu=45000;
- e=1/2: Lambda=316808000/3, Mu=90000.

## Analytic proof of the universal inequality

Consider any stationary reversible hidden chain with deterministic emissions. Conditional past/future independence and reversibility identify every reflected product with the corresponding product of conditional forward expectations. Write xi(X0)=E[F^+|X0]. At an internal output xi=(1,x,y,0^5), while a marker output gives its exact marker vector. Consequently s2=E[I0|x|^2], Rh=E|r|^2 and Rt=E|r_t|^2, where r=E[D|X0] and r_t=E[xi(X1)|X0]-Kxi(X0). These are nonnegative without a dimension or transition-rate assumption.

Conditional marker probabilities are nonnegative. On output 0 they equal a+Nx+r. Therefore ||l(x)_-|| <= ||r||/(e eta). Projection to the pentagon P=conv{v_i}, y=proj_P(x), obeys

|x-y| <= (11/5)||l(x)_-|| <= (22/e)||r||.

The Hoffman constant 11/5 follows from projection KKT. At a projected edge only its normal is needed; at a vertex the adjacent normal matrix N_edge is invertible. The exact checks (11/5)^2 N_edge N_edge^T-I >=0 and reciprocal single-normal bounds establish the claim. Thus D2=E[I0|x-y|^2] <= (22/e)^2 Rh.

The exact geometric estimate

min_i |y-v_i| <= (16/5)(1-|y|^2), y in P,

is stronger than the source's constant 8. Partition P into the Voronoi cells of its vertices. On cell i the function |y-v_i|+(16/5)|y|^2-16/5 is convex, hence bounded above by its maximum at the finitely many cell vertices. Enumerating these rational vertices gives maximum squared ratio exactly 8585/841 < (16/5)^2. geometry_check.py and the independent seed verifier both replay this calculation.

Round y to a nearest vertex v_i and use Z_i, with zero field on markers. All pairwise monotonicity pairings of the rounded feature points are nonnegative. Planar shifting preserves internal differences; internal-marker pairings are zero. Rowwise projection off Omega=(1,0,0,1^5) also preserves all pairings because Omega dot xi=1 on every feature point. The exact bounds are

max|Z_i| <6/5,
max_{i,j}|ztilde_i-ztilde_j| <41/20 (including marker planar field 0),
max|[Z_i(I-K)]_{xy}| <8e/15,
|q_linear| <e/5, and ||q_quadratic_matrix|| <7e/20.

The stationary two-time hidden feature coupling is symmetric. Expanding xi as its rounded feature plus planar error and using monotonicity gives

E Z_round(X0) dot [xi(X0)-xi(X1)] >= -(41/20)E[I0|x-v_i|].

The regression residual contributes at most (6/5)sqrt(p0 Rt). Comparing q(x) with q(v_i)=Z_i dot(I-K)xi_i, and splitting the change through y, yields

Sq >= -A_e E[I0 d] -(7e/20)E[I0|x|d]
      -B_e E[I0|y-v_i|] -(6/5)sqrt(p0 Rt),

where d=|x-y|, A_e=41/20+8e/15+e/5+7e/20,
and B_e=41/20+8e/15+e/5+7e/10.

Set circle=(16/5)B_e. Since 1-|y|^2 <= 1-|x|^2+2|x|d, Cauchy-Schwarz gives

Sq+circle*(p0-s2)
 >= -(22/e)*sqrt(A_e^2+(7e/20+2circle)^2)*sqrt((p0+s2)Rh)
    -(6/5)sqrt(p0 Rt).

For e=1 the first coefficient is sqrt(5690442329/22500)<503. For e=1/2 it is sqrt(7110532693/11250)<796. Thus the two universal nonlinear inequalities follow. Applying a sqrt(uv) <= alpha*u +a^2*v/(4alpha) separately to each residual proves E W>=0 for every competitor. This proof uses only bounded conditional functions and stationary reversibility, so even unrestricted measurable-state stationary reversible chains cannot evade it when regular conditional expectations exist.

## Exact target separation and all-word blind spots

The exact replay verifies E[F|hidden state]=H, E[D|hidden state]=0. QH=HL gives E[G|hidden state]=0. On the target, p0=s2=1/2 and Rh=Rt=0; reflected products equal the source feature inner products by the argument below. The negative source pairing is

g=0.005976777578630545... = -farkas_drift_pairing/2 >0.

The field shift leaves its stationary expectation unchanged. Hence Sq=-eg and

E_target W=-eg+alpha+beta/2.

For e=1 this is less than -29/10000; for e=1/2 it is less than -29/20000. All signs and target identities are exact Fraction checks.

To independently reconstruct the blind-spot argument, let H0=range(H) inside L2(uniform pi). Emission multiplications preserve H0 and, being orthogonal projections, commute with its orthogonal projection Pi. P_e preserves H0 and is self-adjoint there because ML=L^T M. Therefore Pi P_e^*=(P_e|H0)Pi. Induction over the backward conditional-word recursion yields Pi h_F^back=h_F^forward. Every forward conditional-word vector belongs to H0 and is genuinely nonnegative. Conditional past/future independence then gives

P(F reflected past,G future)=<h_F^forward,h_G^forward>_pi
                          =(1/10)sum_i h_F^forward(i)h_G^forward(i).

This supplies a common ten-atom nonnegative factorization for all reflected words, including the boundary. On H0 all transition powers and output projections are self-adjoint, so reversing their order inside the stationary scalar product gives exact observed time-reversal invariance.

For e=1/2 write P_e=(I+R)/2 with R=I+Q a stochastic matrix. Its restriction to H0 is self-adjoint; R's spectrum has modulus at most one, so the restricted P_e spectrum is in [0,1]. The spectral theorem proves the completely monotone scalar-correlation claim. For e=1 an observable eigenvalue is approximately -0.46261: that variant still defeats all reflected CP/reversal tests against reversible DISCRETE chains, but ordinary nonnegative-spectrum tests can exclude a sampled reversible CTMC. Keep this distinction explicit.

A bounded five-word statistic with a strict gap also excludes the target five-word marginal from the total-variation closure of all reversible hidden output laws. No infinitesimal argument, generator convergence, hidden-state compactness or source rigidity theorem is needed for this finite separation.

## Reproducibility, acquisition and limits

Run from package root:

python3 work/discrete_critic/seed_verify.py
python3 work/discrete_critic/exact_witness.py
python3 work/discrete_critic/exact_witness.py --half

The exact word script enumerates all 6^5=7776 words, including words absent from the target. Its observed runtime was approximately 0.27 seconds per variant on the local environment; this is a machine-specific measurement, not an asymptotic theorem. The script uses only the standard library. The exploratory all-pairs enumeration uses NumPy. Source coefficients are exact rational inputs; finite precision approximations should be bounded before claiming the exact test guarantee.

For range width B and certified target gap d, reject equilibrium when the average of N independent W values is below -d/2. Hoeffding bounds both equilibrium false rejection and target missed detection by exp(-Nd^2/(2B^2)). The displayed sufficient counts use N=ceil(8B^2/d^2) and ln40<4. They require independent stationary five-letter windows: five observed symbols per window, four transitions of span, plus preparation of an independent stationary run. They DO NOT establish an equally valid finite guarantee from one correlated trajectory under arbitrary unknown mixing. They also do not charge a zero cost for stationary preparation.

The frozen e=1 witness has floating target variance about 3.822743391865e12. A separate floating optimization of Young parameters gives range 2.22021006e7, variance 3.84609469e12 and a Hoeffding planning count 4.0838e20; these optimized numbers are not the exact certified frozen witness. ENUMERATION.json labels them. Exactness of the rational algebra is evidence for this construction, not proof of novelty or experimental feasibility.

The source mechanism supplies a model-specific universal rejection statistic. It does not learn the model or discover this statistic from unknown observations at the stated sampling cost. The acquisition barrier remains central: reduce the robust separation's range-to-gap ratio by many orders of magnitude, or develop a valid adaptive/nonlinear inference procedure with proved materially better sample complexity under explicit preparation/mixing conditions. No claim is made that the current enormous Hoeffding count is necessary.

Artifacts: RESULT.md; seed_verify.py; SEED_CHECK.json; geometry_check.py; GEOMETRY_CHECK.json; exact_witness.py; EXACT_WITNESS.json; EXACT_WITNESS_HALF.json; enumerate_witness.py; ENUMERATION.json; enumerated_ls.npz; shift_search.py. No external publication or repository mutation occurred. All assigned checks are complete.

## Independently audited variance-sensitive acquisition improvement

Root subsequently supplied work/root/DISCRETE_VARIANCE_NOTE.txt and the standard-library replay work/root/discrete_variance_certificate.py. I independently reviewed the proof, checked the primary [Maurer–Pontil paper, Theorems 3, 4 and 10](https://www.learningtheory.org/colt2009/papers/012.pdf), and replayed the certificate. No flaw was found.

For the half-step target, entrywise upward dyadic rounding of every transition probability to denominator 2^40, an integer five-letter forward recursion, and upward integer rounding of exact W(w)^2 certify E_target W^2 <= V=27,034,341,276,573. The test rejects if the empirical mean plus the Maurer–Pontil empirical-Bernstein radius is negative, using unbiased sample variance. Type-I error is at most .025 for every iid equilibrium null; target power is at least .975 for n > max(160V/Delta^2,80R/Delta,2), Delta=29/20000, R=110,000,000. The certified sufficient count is

n=2,057,310,156,600,085,612,368 independent stationary windows.

The target variance is used only to prove power; null validity uses observed sample variance. This improves the sufficient half-step count to approximately 2.06e21 windows, still impractical. The source-note width 140,000,000 is also conservative and gives the same count; the current machine-readable certificate uses the tighter width 110,000,000. Iid stationary preparation remains an explicit requirement.
