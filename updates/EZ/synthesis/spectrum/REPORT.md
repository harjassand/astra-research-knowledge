# Source-spectrum audit and independently derived consequences

Capital revision: `f437df815bef12f123ae4fe313d861ec1c862bc4`.
Date: 13 October 2026, Australia/Brisbane.
Status: internal reconstruction and finite diagnostics only. Historical novelty,
independent correctness, useful physical acquisition and breakthrough status remain
UNKNOWN. Archived mission text was treated as DATA. No capital, original source,
Git branch or immutable checkpoint was edited by this investigator.

## 1. Intake assessment and exact source routes

The supplied package is suitable as an operator-theory mechanism and obstruction
record. Its exact distinctions between source norm, Hilbert-space source rank,
source-word dimension, tensor rank and acquisition cost must survive integration.
The packet neither proves KLS nor closes N764's interacting inverse-rank gate.

The source's principal analytic arguments appear coherent on reconstruction:

| Source claim | `source/research_note.md` inclusive lines | Audit scope |
| --- | --- | --- |
| Setup and credited comparison | 19–48 | Bounded separable complex Hilbert spaces, a>0; prior inequality credited |
| Positive recursion and nonlinear modulus | 50–139 | Supplied subunital completely positive row map; unique bounded positive fixed point and O(1/k) norm convergence |
| Source-word support and cost | 141–188 | Finite source rank gives finite-rank approximants; word-space/Gram/bit costs remain charged |
| Source perturbation sensitivity | 190–202 | Perturbations inside g; sharp square-root response, not additive outside error |
| Compactness and reciprocal windows | 204–294 | Calkin argument; exact rank minimum across variable polar factor and permitted kernel enlargement |
| Spectral/heat counting | 296–315 | Only after a genuine rank-r certificate has been acquired |
| Schatten transfer | 317–443 | Finite spectral compressions avoid infinite-trace subtraction; exponents p+2 and 2p have separate mechanisms |
| Sharpness and nonnormal propagation | 445–522 | Normal diagonal versus sums of harmonic shifts |
| Product and free-word obstructions | 524–612 | Small formula count need not give small generated space or Schatten summability |
| Additive residual floor | 614–654 | Any positive residual fails to certify compactness; sharp fourth-root singular-value scale |
| Unresolved scientific interface | 656–674 | No acquired interacting-system certificate or end-to-end advantage |

The finite source replay was run only after reading the entire 299-line script;
its writes were redirected into this scratch directory. It passed **24,105 exact
rational/integer assertions and 4,188 floating diagnostic assertions**. These are
producer-code reruns, not independent verification of universal statements. The
smallest floating curvature eigenvalue was -2.15e-15, and the largest tested
Schatten lhs/rhs ratio was about .5345. No interval or physical certification was
performed. Exact source hashes are in `EVIDENCE_INVENTORY.json`.

No decisive mathematical error was found in the source's stated scopes. Its
phrase “explicit acquisition” must retain its actual contract: given the
propagators/source and computable source-word inner products, the recursion
constructs approximants. It does not acquire those input interfaces from a target
Hamiltonian, Jacobian, PDE or experimental medium.

## 2. Stronger construction: simultaneous minimum rank and minimum source budget

This improves the packet's padded forward-shift realisation. It is a consequence
of classical converse interlacing, not a claimed new inverse-eigenvalue primitive.
The source already supplies the trace lower bound implicitly at p=2; the new
point is simultaneous attainment with its exact minimum source rank and, for a
finite spectrum, without enlarging the target dimension.

### Proposition 1 — finite-dimensional joint optimum

Let a>0 and a^-1>lambda_1>=...>=lambda_n>0. Set

\[
 r=\sup_{x>0}\#\{j:x\le\lambda_j^{-1}<x+a\},\qquad
 S=\sum_{j=1}^n[f_a(\lambda_j)-\lambda_j].
\]

There exist n by n T and an n by r source B with these singular-square values,

\[
 T^*T=g_a(TT^*+BB^*),\qquad \operatorname{rank}B=r,
 \qquad \|B\|_{S_2}^2=S.
\tag{J1}
\]

Every admissible T and B with the same positive singular-square list, even on an
enlarged finite Hilbert space, satisfy rank B>=r and ||B||_(S_2)^2>=S. Thus both
minima are attained together. “Source budget” here means a mathematical
Hilbert–Schmidt quantity, not physical energy, electrical power or acquisition
cost.

**Proof.** Write A=diag(lambda_j), D=f_a(A). The rank lower bound is the packet's
min–max/interlacing argument, source lines 269–277. Taking traces in
D<=TT*+BB* gives

\[
 \operatorname{Tr}BB^*\ge \operatorname{Tr}D-\operatorname{Tr}A=S.
\tag{J2}
\]

Partition the indices into r chains j=s,s+r,s+2r,..., for 1<=s<=r. On one chain
write c_1>c_2>...>c_m for its lambda values and d_j=f_a(c_j). Reciprocal-window
spacing gives

\[
 d_1>c_1\ge d_2>c_2\ge...\ge d_m>c_m>0.
\tag{J3}
\]

The chain values are strictly decreasing because a>0. Define nonnegative
residues

\[
 w_j=\frac{\prod_{k=1}^m(d_j-c_k)}
            {\prod_{k\ne j}(d_j-d_k)},\qquad v_j=\sqrt{w_j}.
\tag{J4}
\]

The numerator and denominator have the same sign under (J3); an endpoint
coincidence may make w_j=0. The determinant lemma, or polynomial interpolation
at every distinct d_j, proves

\[
 \det[zI-(\operatorname{diag}d-vv^*)]=\prod_k(z-c_k).
\tag{J5}
\]

For completeness, multiply
`1+sum_j w_j/(z-d_j)` by `prod_j(z-d_j)`: its value at d_j is
`w_j prod_(k!=j)(d_j-d_k)=prod_k(d_j-c_k)`, and both sides are monic of degree m.
Their difference has degree at most m-1 and m distinct zeros. Hence they agree.

Therefore C_s=diag(d)-vv* is positive and has spectrum c. Its rank-one positive
correction has trace ||v||^2=sum(d-c)>0, so it has rank exactly one. Take block
sums over the r chains: C=D-P has the prescribed lambda spectrum, P>=0 has rank
r, and Tr P=S. A unitary U with C=UAU* exists by the spectral theorem. Put
T=UA^(1/2) and factor P=BB*. Then f_a(T*T)=TT*+BB*, proving (J1). The source's
order-inversion equivalence, lines 206–223, finishes the proof. QED.

### Degeneracies and zero singular values

Repeated positive lambda values are allowed in Proposition 1. The window count
places any repeated level in distinct residue chains: lambda_(j+r)<=g_a(lambda_j)
<lambda_j. Hence each individual chain has distinct d_j, and the residue
formula never divides by zero. Equalities c_j=d_(j+1) are allowed; they merely
produce zero residues at some coordinates. Every nonempty chain still has
positive total trace and rank-one correction.

If an original N-dimensional space has n positive singular-square values and
N-n prescribed zeros, perform the construction on the n-dimensional support and
extend A,C,T,P by the zero block. Exact curvature equality, rank r and budget S
are preserved in the original N-dimensional space, including its kernel size.
For n=0 take T=0, B=0, r=0 and S=0. The countable extension below still permits
kernel enlargement; it does not assert arbitrary prescribed infinite kernel
multiplicity can be retained.

### Example

For a=1 and lambda=(1/2,1/3,1/4), r=1. The padded shift uses source squared norm
1, whereas the exact equality realisation uses 3/4. Its correction is
P=(3/4)e_1e_1*, D=diag(1,1/2,1/3), and C=diag(1/4,1/2,1/3), isospectral to A.
This is a finite-rank structural improvement, not a scientific speedup.

### Countable extension, with permitted kernel enlargement

If the positive list tends to zero and r<infinity, the same simultaneous optimum
holds with S=sum_j(f_a(lambda_j)-lambda_j)<infinity, allowing arbitrary kernel
enlargement as in the original theorem. This is an existence result; the argument
does not provide an effective rate for constructing the limiting source.

To see finiteness, sum each chain's gaps using
f_a(c_(j+1))<=c_j: every chain contributes at most f_a(c_1). For truncations at n,
construct P_n by the finite proposition and extend by zero. Then
0<=P_n<=D_n<=D=f_a(A), D is compact, rank P_n<=r and Tr P_n=S_n. The order interval
[0,D] is norm precompact: if Q_N cuts the leading N basis vectors, then

\[
 \|(I-Q_N)P_n\|\le\sqrt{\|D\|\,\|(I-Q_N)D(I-Q_N)\|},
\]

uniformly in n. Finite-dimensional compression and this vanishing tail give a
norm-convergent subsequence P_n->P. Thus P>=0 has rank at most r,
C=D-P is positive, and norm eigenvalue continuity implies C has exactly the same
positive eigenvalue list as A. Moreover
|Tr(P_n-P)|<=2r||P_n-P||, so Tr P=S. Add a common infinite zero summand to A and C
if necessary so their kernels agree, then use a unitary as in the finite proof.
The rank lower bound forces rank P=r. Finally, Ky Fan gives for every admissible
source

\[
 \sum_{j=1}^N[f_a(\lambda_j)-\lambda_j]\le\operatorname{Tr}BB^*;
\]

letting N grow proves optimality, without subtracting divergent traces.

### Cost and boundary

The finite rational residue calculation uses O(sum_s m_s^2)<=O(n^2) arithmetic
operations before the polar unitary is acquired. Products, small gaps, proximity
to a^-1, algebraic square roots, basis output and eigenvector conditioning are
charged. A conventional dense implementation of the polar unitary costs ordinary
dense spectral linear algebra and may produce n^2 entries. The input already
contains the singular spectrum. The construction changes the target's polar
factor, generally destroying locality, tensor form and original dynamics.

For a fixed pre-existing finite T, the optimal source is instead
BB*=(f_a(T*T)-TT*)_+: its rank is the positive inertia and its minimum
Hilbert–Schmidt squared norm is Tr(f_a(T*T)-TT*)_+. The simultaneous construction
above is over the variable polar factor, not a free repair of a supplied physical
operator. It must not be used as an algorithm for acquiring the spectrum it takes
as input.

## 3. Quantifying the extra nonnormality information needed for stronger summability

### Proposition 3 — a supplied commutator majorant removes the propagation loss

Under the original single-operator comparison let A=T*T, C=TT* and P=BB*. Suppose
an acquired positive operator Q satisfies C-A<=Q. Then

\[
 aA^2\preceq f_a(A)-A\preceq P+Q.
\tag{C1}
\]

For any p>0, if B belongs to S_p and Q^(1/2) belongs to S_p, then T belongs to
S_(2p). More explicitly, for 0<p<=2,

\[
 \|T\|_{S_{2p}}^{2p}\le a^{-p/2}
 [\|B\|_{S_p}^{p}+\|Q^{1/2}\|_{S_p}^{p}],
\tag{C2}
\]

whereas for p>=2,

\[
 \|T\|_{S_{2p}}^{4}\le a^{-1}
 [\|B\|_{S_p}^{2}+\|Q^{1/2}\|_{S_p}^{2}].
\tag{C3}
\]

**Proof.** Equation (C1) follows from f_a(A)<=C+P and
f_a(A)-A=aA^2(I-aA)^-1>=aA^2. Since P+Q is compact under the hypotheses, spectral
min-max implies `Tr A^p<=a^(-p/2)Tr(P+Q)^(p/2)`. For p<=2 use the trace
subadditivity already proved in the source, lines 355–404; for p>=2 use the
S_(p/2) triangle inequality. Finite compression followed by a monotone limit
avoids infinite-trace subtraction. QED.

For p<2 the exponent 2p improves the source's unconditional p+2, but only after
the additional commutator summability has actually been acquired. Normality
gives Q=0. More generally the positive commutator part `(TT*-T*T)_+` is a legal
choice; calculating or certifying it can itself require expensive operator
information. A small commutator norm alone gives no Schatten budget in unbounded
dimension, and a selected chemical adjoint identity is not a normality theorem.

The harmonic shift in source lines 463–495 gives an exact falsifier for dropping
this extra hypothesis. Here C-A has diagonal
`(-lambda_0,lambda_0-lambda_1,lambda_1-lambda_2,...)`, and

\[
 Q=\operatorname{diag}(0,\lambda_0-\lambda_1,
 \lambda_1-\lambda_2,...) ,\qquad
 \lambda_{k-1}-\lambda_k=a\lambda_{k-1}\lambda_k\asymp k^{-2}.
\]

Thus Q^(1/2) belongs to S_p exactly when p>1, and T belongs to S_(2p) exactly
when p>1. The rank-one B belongs to every S_p, so at p<=1 the stronger conclusion
fails precisely alongside the missing defect summability. This is not a new
physical acquisition mechanism or a replacement for N764's TT-rank gate.

## 4. A decisive negative synthesis with N764: two source words can need exponential tensor rank

The source packet's source-word dimension D_k and N764's tensor-train bond ranks
are different invariants. The following exact family refutes a generic deduction
from small D_k to a small tensor representation, even when the propagator is
specified by a short circuit and the source is a product vector. It does not
refute N764's particular physical approximation target or prove computational
hardness for all other representations.

### Proposition 2 — rank-two fixed point with exponential tensor rank

For m>=1 let d=2^m, and let
H=C^2_clock tensor C^d_L tensor C^d_R. Across the cut (clock,L)|R define

\[
 s=|0\rangle|0^m\rangle|0^m\rangle,\qquad
 e=|1\rangle d^{-1/2}\sum_{x=0}^{d-1}|x\rangle|x\rangle.
\]

Choose a unitary U taking |0^m0^m> to the displayed Bell-pair state. It is given by
m Hadamard gates on L followed by m paired CNOTs (O(m^2) elementary local gates
suffice after routing on a one-dimensional nearest-neighbour line). Set

\[
 V=|1\rangle\langle0|\otimes U,\quad Bz=zs,\quad a=1.
\]

Then VV*<=I, Vs=e, Ve=0, and the source-generated space stabilises at
W_2=span{s,e}, of dimension two. Yet the unique positive fixed point is

\[
 X_*=\tfrac12|s\rangle\langle s|+\tfrac13|e\rangle\langle e|,
\tag{T1}
\]

of ordinary matrix rank two and operator Schmidt rank d^2=4^m across the stated
cut. It is obtained exactly in two source-recursion iterations.

**Proof.** The two projectors are orthogonal and Phi(X*)=(1/2)|e><e|. Applying
g_1 to P+(1/2)|e><e| gives (T1). Expand the entangled projector as

\[
 |e\rangle\langle e|=d^{-1}\sum_{x,y}|1,x\rangle\langle1,y|
                                   \otimes |x\rangle\langle y|.
\]

These d^2 right matrix units are Hilbert–Schmidt orthonormal. Their left
coefficients are mutually orthogonal; the coefficient for the right E_00 is the
orthogonal sum of `(1/2)|0,0><0,0|` and `(1/(3d))|1,0><1,0|`. Thus the complete
operator Schmidt singular list is

\[
 \sqrt{\tfrac14+\tfrac1{9d^2}},\quad
 \underbrace{\tfrac1{3d},...,\tfrac1{3d}}_{d^2-1}.
\tag{T2}
\]

This proves the exact rank claim. More strongly, any approximation of operator
Schmidt rank 1<=R<=d^2 has Hilbert–Schmidt error at least

\[
 \frac13\sqrt{1-\frac{R}{d^2}}.
\tag{T3}
\]

This is the singular-value tail of the exact realignment matrix. Error at most
1/6 therefore requires R>=3d^2/4. The generated vector e itself has vector Schmidt
rank d and optimal rank-R squared error 1-R/d. QED.

For m=20, the abstract word-space and ordinary fixed-point rank are both two,
but the operator Schmidt rank is 1,099,511,627,776, and error <=1/6 requires rank
at least 824,633,720,832. These large integers follow from the analytic family;
no such dense matrix was allocated in the checks.

### Capital interface and precise rejected transfer

Read N764's current dossier, branch view and checkpoint, plus its original proof
`updates/EW/package/frontier_separable/recovered/astra_frontier_separable_completion/research_note.md`:

- Lines 426–457 give a contraction on the balanced interacting inverse with
  explicit inner-error allowance; cheap outer iteration does not bound inner cost.
- Lines 469–475 charge tensor rounding and actual conservation repair.
- Lines 483–499 define the open target: acquired response fields and near-minimum
  Hodge corrections with controlled TT ranks, poles, bits and full discovery cost.

**Composition state: REFUTED TRANSFER**, for the generic assertion “small source
rank and small source-word dimension suffice for small TT ranks.” Proposition 2
is an executed exact counterexample family. **INCOMPATIBLE ASSUMPTIONS** for
claiming that the new source recursion has already certified N764's actual
interacting response: no such curvature comparison/propagation algebra has been
constructed for that response, and the physical weighted norm and input format
have not been converted. No N764 historical gate is closed or invalidated.

A small word-space basis can be efficient in a circuit representation while
expensive in TT form. This is a reason to keep an explicit representation and
inner-product/application contract, not a reason to declare the underlying task
hard or easy. The example's Bell correlations are highly structured.

## 5. Residual-to-decision certificate: adversarial check of root's new consequence

For the exact supplied recursion F, positive bounded Y, eta=||Y-F(Y)|| and
X* its fixed point, let delta=||Y-X*||. The source modulus gives

\[
 \delta\le\eta+g_a(\delta),\qquad
 \delta\le r_a(\eta)=\frac{\eta+\sqrt{\eta^2+4\eta/a}}2.
\tag{R1}
\]

The signs distinguish an outside residual from the inside-source perturbation
at source lines 190–202. Equation (R1) is sharp with P=0, Phi=identity and Y=rI,
where eta=ar^2/(1+ar). A certified upper enclosure for eta can safely replace eta.

For selfadjoint trace-class task Q,
`|Tr Q(Y-X*)|<=||Q||_1 r_a(eta)`. A difference between two task predictions with
residual radii r1,r2 is certified if its measured margin exceeds
`||Q||_1(r1+r2)` plus all task/readout/model errors. At small target norm error
rho, the necessary worst-case residual scale is
eta<=a rho^2/(1+a rho), not merely eta=O(rho). Checking the operator-norm residual
of an implicit infinite operator remains an acquisition/certification task.

For an unspecified positive subsolution A, the source gives A<=X*, not A=X*.
Only a one-sided consequence follows for positive Q:
`Tr QA<=Tr QY+||Q||_1 r_a(eta)`. Taking A=0 versus A=X* refutes two-sided recovery
of an arbitrary subsolution from a fixed-point residual. For indefinite Q there
is no direct order implication. These bounds do not certify compactness under a
nonzero residual.

The source and N771 both support task-specific rather than global certificates,
but their objects differ. N771's `updates/EY/SYNTHESIS.md:95–118` has the exact
chemical projected correction `b^T(lambda-ell)=xi^T R_N b`, with residual,
response direction and calibration charged. It does not supply a subunital
curvature recursion for R_N or an operator-norm residual bound. **CANDIDATE
CONNECTION** only: a model-specific acquired positive majorant could potentially
bound this selected correction. The missing lemma is a construction from the
native chemical Jacobian and measured data with the required weighted norms and
cost. No chemistry theorem is imported or improved by analogy alone.

## 6. Primary-source audit and prior-art boundary

Primary sources were accessed live on 13 October 2026. These checks establish
locators and specific overlap; they are not historical-priority clearance.

1. [Balasubramanian–Kasiviswanathan, arXiv:2610.07728v2](https://arxiv.org/html/2610.07728v2#S7.SS1),
   Section 7.1, Lemma 7.1, equation (7.1), does contain the same bounded-operator
   comparison with R,L in place of T,B. The source's attribution is correct.
   Their full claimed KLS theorem is not assumed or independently validated here.
2. [Leite–Tomei, arXiv:2108.06285v2](https://arxiv.org/pdf/2108.06285v2),
   page 1, Theorem 1.1, explicitly states the converse to rank-one eigenvalue
   interlacing. This is established machinery behind Proposition 1, not a new
   mathematical primitive of this integration.
3. [Kar–Sinopoli–Moura, arXiv:0903.2890v2](https://arxiv.org/html/0903.2890),
   Section II-A, equations (8)–(11), provides the standard Kalman covariance
   Riccati setting. In one channel, put Z=VXV*+P and observe
   `g_a(Z)=Z-Z(Z+a^-1 I)^-1 Z`. This is the posterior covariance update with full
   observation and observation covariance a^-1 I. The prediction recursion for Z
   is `Z_next=V g_a(Z)V*+P`, matching the standard form. Thus the source's operation
   has classical Riccati ancestry; its exact global O(1/k) singular/degenerate
   modulus needs a separate comparison and is not dismissed by this identity.
4. [Townsend–Wilber, arXiv:1712.05864v2](https://arxiv.org/html/1712.05864v2),
   Sections 1–3, treats source singular-value decay in linear Sylvester equations,
   with constructive ADI/Smith schemes. This establishes relevant source-spectrum
   prior art, not equivalence with the nonlinear inequality.
5. [Bourin–Uchiyama, math/0702475](https://arxiv.org/abs/math/0702475) gives a
   broader matrix subadditivity result; the needed trace inequality is proved in
   the packet independently. [Arveson, funct-an/9705007v2](https://arxiv.org/abs/funct-an/9705007v2)
   and [math/9808100](https://arxiv.org/abs/math/9808100) confirm standard
   multivariable-shift/Hilbert-module context. No new shift object is claimed.
6. [Lemm–Lucia, arXiv:2409.09685v2](https://arxiv.org/abs/2409.09685v2) confirms the
   rejected inverse-square frustration-free finite-size novelty route. The source's
   noncommutative identity-testing citation [arXiv:2209.04797](https://arxiv.org/abs/2209.04797)
   was located; it is not a commutative derandomisation theorem.

## 7. Verification, strongest surviving consequence and next decisive gate

`source_replay_results.json` contains the producer replay. `synthesis_checks.py`
is a new implementation, using definition-first exhaustive windows, exact
rational secular polynomial identities and direct small Bell circuit/realignment
matrices. Its **6,908 checks** passed: 375 spectra, 1,123 exact chain residue and
characteristic-polynomial instances (including the displayed example), 41 small
floating polar reconstructions, three finite Bell families, and 64 exact tensor
error/rank thresholds, plus 48 noncommuting commutator instances and 336
Schatten-transfer diagnostics. Floating polar residuals were at most 2.23e-16. The count
mixes exact and floating checks and does not claim universal proof verification.
The written proofs, not finite tests, support the stated universal propositions.

The strongest positive mathematical consequence here is the joint optimum:
minimum source rank and minimum Hilbert–Schmidt source budget can be attained
simultaneously, with exact curvature equality in the original finite dimension.
The strongest operational obstruction is distinct: even a rank-two, exactly
two-step fixed point with only two source words can require exponential tensor
rank at fixed Hilbert–Schmidt accuracy. The residual-to-task certificate is valid
for the fixed point with its precise quadratic residual budget.

No civilisation-enabling or independently validated breakthrough follows. The
next consequential gate is to **construct from an original scientifically
important input** a verified recursion/majorant whose source words have an
accessible representation, certified Gram/apply costs and a useful task margin,
and compare total acquisition, arithmetic, bits and certification against the
strongest specialised method. For N764 this must control its actual weighted
response/Hodge fields, not abstract source rank. For the joint-optimum theorem,
external proof review and an application where the spectrum is independently
available and polar redesign is physically/legal computationally useful would be
needed before capability claims.
