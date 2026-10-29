# Positive clock initialization with a growing penalty

29 October 2026. Root construction; independent review PENDING. This changes
the old fixed-coupling recipe. Novelty and practical advantage UNKNOWN.

## 1. Input and intended result

Use the source-qualified recursive code, fixed odd subdivision, literal
unique decoder histories, prefix gauge, and clock normal form in
`c_syndrome_initializer/`, `b_conventional/two_body_phase/`, and
`b_conventional/clock_stability/`. There are m clocks, N=O(n) binary history
variables, and fixed clock dimension L. Choose beta=4 ln B0 sufficiently
large but fixed. Constants below can be enormous.

In formal syndrome sector s,

    H_s(lambda)=Naux+lambda V_s,
    E_s=b(lambda)-2lambda^L sum_c s_c+R_s(lambda),
    Delta(lambda)=1/(4lambda^L).

The simple clock ground gap is >=1/2. The paid sectorwise normal form is

    W_s H_s W_s*=E_s+K_s, K_s=Naux+D_s,
    D_s=sum_B Q_B T_B(s) Q_B,
    sup_j sum_(B contains j)||T_B|| <= Cmart lambda.

Q_B complements the local product vacuum. Fix lambda_0 with Cmart lambda_0
<=1/2 and the further gates below. Claim for review: a positive ideal quantum
operation initializes the FULL simulator Gibbs state to trace error epsilon
in expected polynomial(N,1/epsilon) cost, with

    Delta_N=O(Delta_0+log(m/epsilon)/beta).

For arbitrary unknown logical input it initializes the corrected thermal
encoder. Fixed couplings, physical thermalization, noisy preparation, charged
error protection, and native performance are NOT claimed.

## 2. Total thermal excitation weight

Q_B<=sum_(j in B)Q_j implies -aNaux<=D_s<=aNaux, with a=Cmart lambda<=1/2.
Thus K_s>=Naux/2. Eigenvalue min--max, followed by the scalar exponential,
gives Tr exp(-tK_s)<=[1+(L-1)e^(-t/2)]^m. No operator monotonicity is used.
The vacuum is the unique zero eigenvector, hence

    p_exc(s)<=exp[m(L-1)e^(-t/2)]-1.                  (1)

Replacing conditional clock Gibbs states by ground projections costs
<=2 sup_s p_exc in trace norm. This pays the density of states; a gap alone
would not justify an N e^-t bound. Take

    t=beta Delta >=2 ln[32m(L-1)/epsilon].

Choose the largest DYADIC lambda_N<=lambda_0 satisfying this. Its Delta is
within a factor 2^L of the maximum of Delta_0 and that logarithmic threshold.
Its bit length is O(1+log log(m/epsilon)), with fixed input constants.
The surviving syndrome law is exp(-beta Delta E_s), NOT the nominal law.

## 3. Acquire the corrected classical energy

Retain independent amplitudes on all gauged hopping labels. Their overlap
graph has fixed degree. A connected set A of distinct hopping labels has a
connected declared clock support B_A of <=q|A| cells. Identify each cell
with its top-check-history vertex, and add the clock-interaction edges to
the history primal graph. The enlarged G has fixed degree d; every symbol
in A is in B_A.

Let E_C(s) be the simple ground energy retaining only hops C subset A. Set

    eta_A(s)=sum_(C subset A)(-1)^(|A|-|C|) E_C(s).

Disconnected increments vanish by factorization. Möbius inversion recovers
the full energy from connected A. Fourier expand each increment in <=q|A|
formal signs. Remove scalar coefficients and the actual order-L leading
amplitude monomials. The remaining scaled real coefficients are r_b, parity
monomials S_Xb, with connected declared supports B_b=B_A. No quotient by
check relations is required. Several bonds can share the same support.

The frozen marked-amplitude KT estimate is coefficient-l1, with density
<=3J rho on |lambda|=rho. Remainders start at order L+1; order k has support
<=qk. Therefore, for fixed 0<h<1 and lambda h^(-q)<=rho/2,

    sup_i sum_(b: i in B_b)|r_b|h^(-|B_b|)<=C_h lambda,
    C_h=(3J/(2rho^L))h^[-q(L+1)].                     (2)

Unmerged hop supports and subtraction of the actual leading monomials are
essential. A bound only on sign incidence would not pay this statement.
Grouping connected increments or equal parities can only reduce l1.

Retaining |A|<=K omits only amplitude orders >=K+1. A loose global scaled
energy error is

    e_K <=(3mJ rho/(4lambda^L))
                 (lambda/rho)^(K+1)/(1-lambda/rho).    (3)

Choose K>=L so 2beta e_K<=epsilon/16. Then
K=O(log(m/epsilon)+log(1/lambda)), with fixed constants.

There are m C^K connected hopping sets. Subsets/sign assignments cost
exp(O(K)); each clock matrix has dimension <=L^(qK). Dyadic lambda gives
rational Hermitian entries (use a real embedding). Rational-inertia bisection
encloses its simple ground eigenvalue using explicit norm bounds and the
uniform gap. Work is polynomial in matrix size and precision. Alternating
subset/Fourier sums cost O(K) extra bits. Total coefficient acquisition is
polynomial(m,1/epsilon), with an enormous fixed exponent. No global clock
diagonalization or coefficient oracle is assumed.

## 4. Positive bond identity

For r_b!=0,

    exp[-beta r_b(S_X-1)]
       =c_b[1+v_b 1{S_X=-sign(r_b)}],
    v_b=exp(2beta|r_b|)-1,
    c_b=1 if r_b>0, else exp(-2beta|r_b|).            (4)

Constants c_b cancel from normalization. Optional active bonds have weight
v_b and the displayed favorable parity constraint. Bonds compatible with
the all-zero history retain their background contribution.

For finite computation use downward nonnegative RATIONAL v_b. If an r_b
interval straddles zero, omit that bond and charge its possible magnitude;
otherwise certify its sign. Refine all intervals until omitted/rounded
log-factor error totals <=epsilon/32. There are polynomially many terms,
so polynomial extra bits suffice. Downward rounding preserves the gates.
Nominal weights B0^(-4E_top) are rational; no transcendental coin is assumed.

An augmented configuration is an accepted history T (its 1 sites), plus
active bonds satisfying their constraints. Its covered set is T union all
active declared supports. Components in G form a positive hard-core gas.
Restricting to one component preserves every original factor: it sees
nonzero input from at most one component, and its zero input is accepted.
Compatible components concatenate. All energy/bond factors are internal.
This exactly represents the truncated, rounded corrected syndrome law.

## 5. Activity bound including overlapping bond multiplicity

There is ONE aggregated activity w_U for each connected covered set U. Set
x=B0^-1. The paid history bound |T|<=4E_top(T) bounds its weight by x^|T|.
If sup_i sum_(b: i in B_b)v_b h^(-|B_b|)<=delta_h, then coverage implies
|T|+sum_active |B_b|>=|U|. After inserting powers of h and dropping coverage,

    w_U<=h^|U|(1+x/h)^|U|
                    product_(b: B_b subset U)[1+v_b h^(-|B_b|)]
       <=[(h+x)exp(delta_h)]^|U|.                    (5)

Thus many overlapping bond choices are paid, rather than falsely counting
colored supports by a single exponential. From (2), if C_h lambda<=1/(4beta)
then v_b<=4beta|r_b|. Require lambda<=1/(16beta C_h), giving delta_h<=1/4.

Set A=4max(1,d), R=16A^2, h=1/(256A^3), and choose x<=h. Equation (5) and
exp(1/4)<2 imply w_U<=a^|U| with a=1/(64A^3)=1/(4AR). Also require
lambda<=rho h^q/2 and the old normal-form/thermal gates. B0 and lambda_0
are chosen jointly once. Decreasing lambda_N preserves all gates.

## 6. Computable activities and internal histories

For W subset U calculate

    Z_W=sum_(accepted T subset W) B0^(-4E_top(T))
                   product_(b: B_b subset W)[1+v_b 1{favorable(T)}].

Predicates have zero input outside T. Exact coverage inclusion--exclusion is

    w_U=sum_(W subset U)(-1)^|U-W| Z_W.                (6)

Connected U means one covered component. Work is O(3^|U|) times a polynomial
in the global rational bond list. Exact arithmetic pays cancellation, while
the positive configuration definition ensures nonnegativity. Fixing T in
the same formula gives its nonnegative weight conditional on U. Enumerating
T,W and using a rational categorical coin samples the internal history.
No enumeration of all bond subsets, decoration oracle, or normalizer is used.

Use the ordinary reconstructed vertex polymer chain. At root v draw Kp with
Pr(Kp>=s)=R^-s, capped at N. Enumerate connected U containing v, |U|<=Kp,
and output U with conditional probability w_U R^|U|, else empty. The sum
is <=(aR)/(1-AaR)<=1/(3A); each unconditional proposal is exactly w_U.
With probability 1/2 remove the polymer at a uniform root, otherwise add
the proposal if compatible. Detailed balance holds.

The incompatible birth mass for a discrepancy gamma is bounded by

    sum_(U incompatible gamma)|U|w_U
       <=|gamma|(d+1)a/(1-Aa)^2 <|gamma|/2.

The one-polymer coupling mixes in O(N log(N/epsilon)) FIXED updates.
Expected enumeration/activity work is bounded by
sum_s poly(s)(3A/R)^s times polynomial global input cost; R>3A pays it.
Final internal-history work can be charged when its polymer is accepted,
with the same proposal tail. This proves expected polynomial cost. A single
total cap at expected work/epsilon, returning zero on timeout, adds <=epsilon
TV and yields polynomial bounded work. Restarting on favorable runtime is
not used. The chain is ordinary Chen et al. 1901.06653v6, reconstructed in
c_syndrome_initializer; (4)--(6) provide the corrected-energy admission.

## 7. Positive quantum operation and total error

Sample the corrected classical history. Use the already paid nominal
stabilizer encoder and recovery Pauli for its top syndrome s. Given this
CLASSICAL s, prepare the clock ground state from the vacuum along
Naux+u lambda_N V_s, 0<=u<=1. The gap stays >=1/2 and
||dH/du||<=lambda_N mJ; the second derivative vanishes. Ordinary finite-
dimensional quantitative adiabatic preparation uses polynomial(m,1/epsilon)
time; fixed-locality Hamiltonian simulation gives polynomial ideal gates.
The phase may depend on s: s is classically mixed, and the path acts as
identity on every unknown logical input. Apply the finite-depth inverse
prefix gauge. This is an actual positive operation, not a diagonal classical
sample asserted to be a noncommuting Gibbs state. No global Gibbs oracle or
exponentially small-overlap postselection is used.

Errors add: energy truncation <=2beta e_K in classical l1; rounding has the
chosen log-density budget; chain TV contributes twice that amount; discarded
clock population costs <=2 sup p_exc; adiabatic and digital errors take the
remaining trace budgets. Split epsilon among these. The trace error is
uniform over unknown logical inputs and a reference. Logical I/2 yields the
full Gibbs state; other inputs yield the frozen logical-module encoder.

The ordinary adiabatic source is Jansen--Ruskai--Seiler,
https://arxiv.org/abs/quant-ph/0603175v3. No new adiabatic principle is claimed.

## 8. Consequences, prior methods, and remaining gates

For epsilon=N^-p, penalty is O(log N) and ideal cost is polynomial. For
exponentially small epsilon only polynomial-in-1/epsilon cost is claimed.
The earlier fixed-coupling dynamic theorem needs a velocity receipt:
a conservative v_N=O(Delta_N) grows logarithmically, losing logarithmic
factors in stretched-exponential exponents. A strictly smaller positive
exponent can plausibly absorb this; a full uniform dynamic-constant
composition is NOT certified by this initializer proof.

Ordinary machinery is retained: polymer dynamics, linked energy increments,
finite-matrix spectral isolation and gapped adiabatic preparation. The primary
Helmuth--Mann https://arxiv.org/html/2201.06533v2 supplies classical quantum
PARTITION approximation in its lattice scope. Eassa et al.
https://arxiv.org/abs/2310.20129 supplies a quasi-distribution for observables.
Neither is silently promoted to a physical full-state preparation oracle.
Fixed-coupling cold sampling, unknown charged errors, noisy preparation,
world novelty and practical performance remain open.
