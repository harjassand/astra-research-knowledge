# Independent whole challenge: arbitrary-alphabet information-budget design

30 October2026. Producer c_independent_opening/ was READ ONLY. This review
adds no source case, solver call, channel tuning, reference-state query or
actual random sample. N1038/free-Umegaki are retained as accepted inputs at
their actual scopes; their historical candidate labels are not reopened.

**ACCEPTED at the stated arbitrary-alphabet mathematical, rational receiver
and conditional exact-ticket-law scopes. No substantive correctness issue
or producer correction is outstanding.** The producer supplied its stable
22-file snapshot before this decision. Governing PROOF SHA is
`9321a42a4fc3f23daa823db12f8419fec1ce07c08d15778b1c83155965498400`;
FROZEN.json SHA is
`e691c68385a519cd6831f43ac4614b305b6607b9186b262678cd5b365c42a94b`.
All manifest entries and the replayed input bytes match that snapshot.
This is no historical-priority, physical-privacy or practical-advantage claim.

## 1. Exact input and inherited entropy interface

The new problem is a one-use design at a SHARED classical input boundary.
L is strictly positive, square n-by-n and invertible. K has m output symbols,
is column stochastic and has a specified positive entry floor kappa<1/m.
The budget is a fixed rational0<c<1, and utility is an explicit rational
linear function. The program does not learn L, acquire raw X, calibrate an
unknown physical channel or produce a model from data. Applying K needs
raw classical X and private randomness independent of the reference.

The accepted inherited theorem identifies the all-reference conditional
Umegaki comparison with the universal free inverse quadratic forms on
positive effects Q_i summing toI and zero-sum vectors u_i. Its finite-
difference/support convention is retained. Neither fixed-reference SDPI
nor a scalar/commuting-effects relaxation is silently substituted. Taking
the product comparison state rho_X tensor rho_R does give the stated
I(R:K(X))<=c I(R:L(X)) corollary, including arbitrary finite quantum R.
It does not give differential privacy, guessing dominance or every-loss
Blackwell order.

## 2. General covariance reduction really is dimension independent

For noncommuting positive output effects W_y summing toI, direct ordered
multiplication of diag(W_1^-1,...,W_q^-1)+11^T tensor W_m^-1 with
diag(W_1,...,W_q)-w w^* givesI. In the offdiagonal terms the ONLY reduction
is sum_(y<m)W_y=I-W_m; no pair of effects is commuted. Thus the arbitrary-m
inverse identity is sound.

For L, R=P_n L^-1 satisfies sum_y L_yi r_y=e_i. The r_y affinely span
R^(n-1): if a.r_y is constant, multiply a^T P_n L^-1=b1^T byL to find
a^T P_n=b1^T; its last component forces b=0,a=0. Strictly positive L
columns therefore make every covariance H_i positive definite. The same
constant-row gauge cancellation used in the accepted three-symbol proof
gives H_L=sum_i(H_i+e_i e_i^T) tensor Q_i-qq^*.

K need not be invertible or square. With D=P_m K B_n, J_K=D^T M_K D;
the comparison follows from the equal nonzero singular values of
M_K^(1/2)D J_L^(-1/2) and its adjoint. Hence the rectangular/singular-D
equivalence (4) is valid. Here M_K is the positive inverse-action pencil
BEFORE inversion, not its covariance. The entry floor keeps all required
output inverses bounded even on the closed effect simplex.

Expanding x_i=D e_i+x_n gives V=sum x_i x_i^T tensor Q_i-XX^*>=0. This is
an operator variance, with an explicit positive decomposition; it is not
a scalar covariance assumption. The coefficient identity (5), including
the negative(c-1)V at subunit budgets, is correct. Its completion around
a scalar common center z yields (6) exactly with the proper product order.

## 3. Necessity of ONE common center for arbitrary output dimension

I independently reconstructed the nontrivial necessity step. For an
arbitrary normalized q-component reference vector w, assemble its columns
into U and let E_i=U^*Q_iU, G=sum E_i and d=sum E_i x_i. The squared norm
of X^*w is bounded below by d^*G^+d by orthogonal projection onto ran U.
Conversely any E_i>=0 with Tr G=1 realizes equality in dimension rankG<=q
by U=G^(1/2) and Q_i=G^(-1/2)E_iG^(-1/2) on its support. The block PSD
condition imposes exactly s>=d^*G^+d, including the singular range condition.
Thus the finite convex program (7) is an EXACT universal minimum, not a
relaxation obtained from a guessed reference rank.

Complex conjugation averaging of E_i,G,d preserves its affine PSD block
and real objective, so real symmetric E_i suffice. E_i=I/(nq) and a
strictly larger s give primal Slater. E_i live in a compact trace-one set,
s>=0 andt>0, so the objective has a finite optimum. Ordinary SDP duality
therefore provides dual attainment. With dual block[[Z,b],[b^T,t]], its
Schur condition is Z>=bb^T/t. The coefficient constraints are
A_i-mu I-Z-bx_i^T-x_i b^T>=0; selecting the smallest allowed Z and b=-tz
gives precisely B_i(c,z)>=mu I. This verifies the sign and the common-
center necessity, not only sufficiency.

Consequently the new free witness rank q=m-1 is justified at the level
needed here. Passing through the inherited faithful active/vacuum entropy
realization may require one more reference dimension, m, and arbitrarily
poor conditioning. No favorable physical preparation or witness precision
is inferred. The c>=1 vertex criterion and c=0 constant-release endpoint
also check, though the executed design uses strictly subunit c.

## 4. Exact JOINT unknown-K lift, compactness and paid weak optimization

The two rank-one penalties and D H_i D^T in (9) are exactly the Schur
complement of (10), since its three lower blocks are H_i^-1,c,t>0. All
offdiagonal columns are affine in the UNKNOWN K and a=t z. Thus the full
universal budget-feasible set is a spectrahedral shadow at the stated
square-reference interface. The lifted order is q+p+2=m+n and there are
n blocks. No bilinear unknown-center/channel term remains hidden.

The center box is harmless: positivity gives
t(z_j-x_ij)^2<=c x_ij(1-x_ij)<=c/4, so |a_j|<=t+sqrt(ct)/2<=5/4<2.
With K stochastic/floored, the boxed variables are compact. An optimum
exists, but it need not be rational.

The constant K0=1/m,a0=t x0 is STRICT in the affine stochastic coordinates:
the Schur complement is c[diag(x0)-x0x0^T]>=c/m^2 I. This is a substantive
Slater point. SLATER_RADIUS.md supplies a literal rational interior radius,
not just an existential conditioning argument:

`mu0=(1/4)min{c/m^2,t,1/max_i Tr(H_i)}`,

`rin=min{1/2,(1/m-kappa)/(2m),mu0/[8(m+n)]}`.

The proof uses a block-triangular congruence with inverse norm<2 and the
explicit perturbation Lipschitz bound4(m+n). The outer variable radius is
also rational/polynomial. Exact L inversion and determinant bounds give
polynomial bit lengths for H_i,H_i^-1. Hence log(Rout/rin) is polynomial in
the rational input length, even if the numerical condition is poor.

I directly read [de Klerk--Vallentin1507.03549v2, Theorem1.1](https://arxiv.org/html/1507.03549).
Its known rational center and relative inner/outer radii give the ordinary
Turing polynomial additive-accuracy SDP contract, with log(1/epsilon)
dependence. The block/affine conversion here has polynomial rational size.
This supports the CLAIMED weak-SDP operation; it does not prove that every
fixed-precision floating solver has that runtime. Rational blending with
the interior point and sufficiently fine rounding preserve constraints
at a paid utility loss. The actual finite repair loops may fail and are
not a universal precision controller; their successful proposal is checked
separately. This is not exact rational optimality or a unit-cost SDP oracle.

## 5. Exact global receiver and integer operational law

For PSD Y_i, every feasible point has C:K>=C:K-sum Tr(Y_i M_i). The latter
is affine on the full ambient variables. Its exact minimum over the larger
floored-column-simplex and center box is (11), including the negative
2sum|b_h| term. Stationarity residuals need not vanish. A poor dual proposal
still supplies a valid lower bound; rational PSD/LDL, not solver status,
is the qualification. A feasible rational K supplies the upper bound.

I read all295 lines of acquire_design.py and all208 lines of
receive_design.py. The producer checks the small Schur B_i; the standalone
consumer rebuilds full lifted19-by-19 blocks and derives affine coefficients
by literal finite differences. Neither step assumes a favorable eigenvalue
roundoff sign. Column sums, floors, center box, dual PSD and both exact
cost endpoints are retained. A solver's optimal label is only a proposal.

The integer sampler has an exact finite contract. For each input the LCM
of rational denominators yields positive integer counts summing toN. A
fresh uniform k-bit word, k=ceil(log2 N), is retained iff it is<N; its
conditional distribution is uniform onN tickets. The half-open cumulative
intervals return output probabilities exactly K. bisect_right at an END
correctly selects the next interval. The actual supplied table hasN=7*2^62,
k=65, acceptance7/8 and expected fair-bit cost520/7, not a hard bit cap.
The endpoint checks do not claim to establish independent randomness.
Private fresh ideal bits are a declared primitive; no samples were acquired.

The information guarantee concerns applying that one-use channel to raw X,
with randomness independent of R. Access only to an L record does not
implement an arbitrary feasible K: that would be a degrader restriction.
The proof explicitly keeps this input/operation distinction.

## 6. Strong ordinary comparator and the retained loss

The erasure/replacer family K=cPL+(1-c)r1^T is a valid sufficient family by
joint convexity/DPI (or by keeping then forgetting the independent erasure
flag). Its source-aware linear optimization is an ordinary LP. The full
same-floor family receives the same raw symbols,L,c,C and floor; its exact
primal and nonnegative-floor-multiplier lower bound check. The relaxed
no-floor optimum is also retained and is SMALLER than the new design cost.
Thus the actual example does not beat the relaxed family, let alone all
ordinary algorithms. The stronger source-aware common-center/convex/free-SOS
route is allowed to use the new mathematics and match this exact SDP.

[Helton--Klep--McCullough1102.4859v3](https://arxiv.org/pdf/1102.4859) directly
supplies degree-controlled weighted SOS certificates for free positivity on
monic LMI domains. I read primary Theorem1.1/Remark1.2 and its setup. It is a
strong ordinary antecedent, not an automatically substituted proof of this
specific joint unknown-K lift or a claim that the earlier three-symbol
result was unknown. N1038 supplies the accepted covariance/common-center
mechanism. This packet is its proved arbitrary-alphabet DESIGN extension;
historical priority and practical advantage are unestablished.

## 7. One-use versus persistent release, and final operational scope

Root supplied a useful repetition guard, which I independently reconstruct
analytically. For L=BSC(1/4), K=.5L+.5uniform=BSC(3/8), the one-use all-
reference budget hasc=.5. Repeating the SAME hidden uniform bit129 times,
with its classical copy inR, permits majority error underK below1/32:
the Chernoff bound is(15/16)^(129/2)<1/32. Binary conditional entropy is
then at mosth2(1/32)<ln2/4, while I(R:L^129)<=ln2. Hence the unchanged
strict factor.5 cannot hold for these correlated repeated inputs.
This is a scope guard, not a counterexample to the stated one-use theorem
and not a new numerical test. Persistent privacy or repeated-budget
composition requires its own channel/model analysis.

The operation is exact software design for an explicit rational channel
model, not empirical channel identification, cryptographic security,
rectangular/rank-deficient reference extension, a coherent-input quantum
channel theorem, hardware performance or all-loss utility dominance.
The all-reference entropy contract is a meaningful new exposed operation
at its precise interface; the broader civilisation mission is not thereby
declared achieved.

## 8. Independent SAME-input arithmetic receipt

replay_certificate.py uses only stdlib/Fraction and imports NONE of the
producer, conic/LP solvers or symbolic packages. It recomputes the12 H_i,
their exact mean/covariance identities,12 common-center Schur certificates,
12 dual PSD checks, the exact global interval, both ordinary intervals and
all168 integer-ticket endpoints from the literal saved source/certificate.
It also acquires mu0=1/392 and rin=1/59584 for this input. It writes ONLY
the review directory and checks producer bytes unchanged during the run.

Observed cost:0.152715333s after stdlib imports, peak RSS23412736 bytes on
Darwin, zero solver calls, zero random samples and zero reference queries.
This is an independent exact certificate/operational replay, not an
independent optimization or all-alphabet numerical experiment. Exact cost
gap is1507948144221822533/722120855195452534947840, about2.0882213e-6.
The displayed same-floor and relaxed comparison signs reproduce.

The final source also retains the initial unjustified expected-improvement
assertion, its failed source/proposal and its NOT_SERIALIZED runtime. The
corrected acquisition's0.705536458s after imports excludes its final output
serialization; its scientific imports cost1.074671334s. Those are not the
complete two-attempt research time. The producer standalone receiver's
0.641891125s includes its own exact intake and ticket catalogue write, not
our independent replay. No timing ratio or full-cycle speedup is accepted.

The analytical all-size reconstruction above, full code intake, stable source
binding and actual rational receiver checks support the stated acceptance.
No tuning, new model or solver rerun is requested.
