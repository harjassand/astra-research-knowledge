# Independent whole challenge: exact mixed cq retention

## Verdict

The general mathematical theorem and its corrected literal coefficient
certificate are ACCEPTED at the declared supplied-state scope. I whole-read
root_cq_retention/PROOF.md Sections1--6 and reconstructed the argument
independently, including the full unequal-reference modular gauge. I then
read the corrected Section5 and new Section7 in the final version with SHA
`4ae07075968d2f076f8ebb67621c5db87c55d12d9eba1aca0445417af93a0420`.
No substantive counterexample or missing mathematical premise was found.
One literal all-complex Choi representation correction was requested and
has been fixed. The main entropy theorem and its Kraus congruence were
already sound before that correction.

For n>=2 finite preparations, define `P_i=ker(sum_(j!=i)tau_j)` inside
`S=supp(sum_i tau_i)` and `r=min_i Tr(tau_i P_i)`. For EVERY finite quantum
reference and EVERY admitted cq pair with finite defined differences,

`D_out-D_ref >= r(D_in-D_ref)`.

The factor is sharp already on scalar/equal-reference pairs; the reverse
coefficient is1/r for r>0 and infinite for r=0. No reference-size promise,
classical-output equivalence or physical simultaneous recovery map is
assumed. A singleton input alphabet is excluded from the sharp conditional
ratio claim because both conditional quantities then vanish identically.

## Load-bearing reconstruction

1. Mixed-projector extraction is correct even when the private projectors
   overlap and do not commute with their own states. E_i=P_i/r_i kills
   tau_j from BOTH sides for i!=j, so every off-diagonal matrix entry of
   T L_tau_j T* and T R_tau_j T* vanishes. The surviving entry is1/r_j,
   using P_j^2=P_j. No positivity/trace-preservation of T is required.
2. The inverse-form inequality is ordinary Hilbert-space projection. It
   applies to arbitrary complex u_i and two independent positive weight
   families. On actual faithful modular blocks the output W is positive
   on HS(S tensor R); the common unused output kernel must be removed.
3. At each modular parameter, z=(sum Q_i)^-1 sum H_i and
   u_i=H_i-Q_i z center the tangent. The input subtraction is exactly the
   square-completion term. On output W(I tensor z)=sum tau_i tensor Q_i z,
   and the cross term vanishes by sum u_i=0 and Tr tau_i=1. The output
   subtraction is therefore the SAME marginal term. Intermediate z,u_i
   need not be Hermitian; the complex quadratic-form inequality allows
   this. This is what genuinely closes unequal-reference J.
4. Integration of the modular inverse forms gives the BKM Hessians;
   Bregman line integration gives the claimed Umegaki differences.
   Common faithful regularization converges term-by-term for each finite
   D by joint convexity and lower semicontinuity. Undefined
   infinity-minus-infinity has not been assigned a value.
5. Classical endpoint sharpness is valid for mixed noncommuting outputs.
   All small eigenvalues of `(1-e)B+e tau_i` lie between fixed positive
   multiples of e, their projector is P_i+O(e), and the remaining spectrum
   stays separated from zero. Its logarithm is `(log e)P_i+O(1)` in norm.
   The constants are channel-dependent; no uniform endpoint rate is
   claimed. If r_i=0, the output entropy remains bounded while the input
   entropy diverges. This also pays the infinite reverse-factor case.

The full independent derivation is in INDEPENDENT_DERIVATION.md. C's
BKM_BRIDGE.md and PURE_FRAME_REVERSE.md were also whole-read at the
recorded intake versions; the former's sufficient two-family implication
matches this reconstruction. Necessity of the unrestricted two-family
condition for arbitrary CQ comparisons is NOT established or needed.

## Literal certificate repair

Let the e-by-f arrow Z implement Phi(A)=Z* A Z/c. Under source-first
Choi indices `C_(a,p),(b,q)=[Phi(E_ab)]_(p,q)`, the rank-one matrix is

`vec(conjugate Z)vec(conjugate Z)*/c`.

ZZ*/c has the wrong dimension if Z means this arrow matrix. Also omitting
the conjugate is incorrect on complex inputs, although the retained real
0,+ control would not reveal that. The correct congruence has exact U
off-diagonals, top `diag(Q_i/(c r_i))` and bottom c. The nonnegative
source-effect fills close the target exactly. Thus this is a repair of
the literal coefficient output, not an obstruction to the main theorem.

I sent the correction to both producers. The final root Section5 explicitly
uses the corrected complex convention; its certificate display is now
accepted. C also reports its general wording amended with no change to
the real-pair execution. A generic
symbolic complex-index consumer, check_complex_choi.py, independently
checked all16 polynomial entries and confirmed that the unconjugated
vector is not generally correct. It took0.018858s after imports, about
0.564s process time. This is an algebraic consumer, not a new channel,
source, solver run or theorem substitute.

## A constructive strengthening acquired during review

FINITE_WITNESS.md supplies an explicit rational endpoint witness for any
claimed c below1/r. Rational pseudoinverse-trace floors a,b give, for
e<=ab/8,

`D(tau_i||(1-e)B+e tau_i)<=r_i log(1/e)+log(8/(ab))`.

An integer h with2^h>=8/(ab), and
`k=max(h,floor(c h/(1-c r_i))+1)`, produce e=2^-k and a literal rational
scalar input pair with `D_in>c D_out`. This removes an asymptotic or
matrix-log oracle from finite witness existence. It does not erase rare
prior costs: an ordinary explicit rational denominator needs k+1 bits,
which may be large. The construction was proved analytically, not
executed as a new source case. Root's new Section7 independently obtains
the same conservative matrix floor from the simpler decomposition
`B_e=e(tau_i+B)+(1-2e)B`; that proof also checks and has no hidden
alignment assumption.

## Acquisition and decision boundary

Exact rational kernel projectors and weights have polynomial bit cost in
the explicit rational matrix input. No rational orthonormal support basis
is required: a full-space rational projector is available from a kernel
basis, and `A^+=(A+P_ker A)^-1-P_ker A`. The explicit Choi identity can
remain on the original HS coordinates even when its source center is
singular; it does not need a free-Farkas Slater theorem. Physical BKM
inverses restrict analytically to S.

Exact support admission is substantive. Every arbitrarily small full-rank
contamination gives r=0 for n>=2. The finite inverse coefficient is not
robust under unrestricted channel uncertainty. When finite, its geometry
implies n<=d and rank(tau_i)<=d-n+1. Product-source factors multiply over
the full product alphabet; a one-copy constant is not unchanged by reuse.

The strongest ordinary comparator is unambiguous discrimination on the
SAME states, not an uninformed classifier. Its private-kernel criterion
and POVM SDP are established, and already give a finite heralded inverse
when every r_i>0. The proposed operation earns the exact Umegaki constant
without pretending its HS extraction is one physical POVM. For0,+ it
gives2, versus the optimum uniform heralding bound2+sqrt(2). Details and
current primary source boundaries are in PRIMARY_AND_DECISION.md.

Historical priority remains UNKNOWN. No practical information-acquisition,
channel-calibration, state-preparation, capacity or physical advantage is
certified. No new quantum/dynamical simulation was run. This is a complete
internal analytical challenge at the declared all-finite-reference
mathematical scope; those honest boundaries do not diminish that verdict.
The retained 27-order real-pair certificate is C's separate execution;
this review does not claim to have replayed it or executed a new mixed
source. A generic exact complex-index identity was the only computation
executed for this challenge.
