# Review of the bounded oscillatory quadratic-chain consequence

## Verdict

The proposed family removes the pole and inverse-conditioning loopholes on an explicit invariant domain. Its arbitrary-time evaluation claim is defensible as **polynomial bit complexity for this certified family**, given rational input data, an explicit accuracy criterion, and the acquisition/evaluation representation below. It remains an integrable, deliberately structured subclass, and gives no speed separation from an equally informed conventional recognition/decoder algorithm.

The sole immediate correction: bounded condition number of a hiding matrix L is not enough to preserve the same fixed Euclidean initial ball. L=aI has condition number one but arbitrary scale. Either take L orthogonal, bound both ||L|| and ||L^-1||, or shrink the ball by ||L|| and state the resulting constants. The unhidden family has no such qualification.

## Exact family and all-time bounds

Let n=2m and H_i(u)=u_i+u_(i+1)^2 (i<n), H_n(u)=u_n. Let B have diagonal 2x2 rotation blocks [[0,-j],[j,0]], j=1,...,m, and c=(1,0,1,0,...). The projective field is g(y)=By-(c^T y)y, with homogeneous matrix M=[[0,c^T],[0,B]].

The eigenvalues of B are the distinct nonzero numbers +/-ij. The row c has a nonzero component on each complex eigenspace, so c is cyclic for B. Consequently the denominator row e_0^T is cyclic for M, whose spectrum adds the distinct eigenvalue zero.

Writing R(t)=exp(tB), direct block integration gives

    exp(tM) = [[1,c^T B^-1(R(t)-I)],[0,R(t)]].

Each block of R(t) is an orthogonal rotation. Moreover ||c^T B^-1||_2^2=sum_(j=1)^m 1/j^2<2. Thus for ||y_0||_2<=1/32,

    |den(t)-1| <= 2 sqrt(2)/32 < 1/8,
    den(t) >= 7/8,
    ||y(t)||_2 <= (8/7)/32 = 1/28 < 1/16

for every real t. There are no projective poles on any real-time trajectory in this domain. The estimates hold equally for negative t.

For any target with ||y||_infinity<=1/16, inverse backward substitution

    u_n=y_n,  u_i=y_i-u_(i+1)^2

gives |u_i|<=1/8: the induction uses 1/16+(1/8)^2=5/64<1/8. The Jacobian JH=I+K has only superdiagonal entries 2u_(i+1), so ||K||_infinity<=1/4 and also ||K||_2<=1/4. Therefore both induced norms of (JH)^-1 are <=4/3. This is a uniform local inverse bound on the whole target box, not a generic stability assumption.

The inverse has degree 2^(n-1) but a linear-size recurrence circuit. For F=L^-1 H(Lx), the inverse is L^-1 H^-1(Ly), costing O(n^2) additional gates for a dense explicit L. Orthogonal L preserves the stated Euclidean input ball and 2-norm conditioning. More generally require ||Ly||_2<=1/16 and charge ||L^-1|| ||L|| in the inverse bound.

## Acquiring the quadratic chart without high-degree monomial expansion

The raw input is f=(JF)^-1 g(F), supplied as a low-height rational arithmetic circuit, not as a supplied chart. The canonical q=-div f/(n+1) equals c^T F because det JF is constant and tr B=0. For T=f dot grad+q,

    T1=c^T F,   T(F)=BF,   T^k1=c^T B^(k-1)F  (k>=1).

Thus every cyclic iterate is genuinely quadratic, although the raw degree can grow with n. The first n nonconstant iterates span the chart components. Since F(0)=0 and JF(0)=I, normalizing the acquired chart at zero recovers F exactly, independently of its unknown output basis.

A direct proof-level circuit front end can therefore use the canonical degree<=2 dictionary of O(n^2) monomials. For each current quadratic p, evaluate T(p) through the raw circuit and automatic differentiation at the standard unisolvent quadratic interpolation nodes {0,+e_i,-e_i,e_i+e_j}. Recover its quadratic interpolant and perform rational Krylov elimination. No hidden triangular order or chart is supplied. On this family the interpolation is exact, and closure occurs at rank n+1.

For arbitrary inputs, interpolation alone is not acceptance. Certify every final identity T(phi_i)=sum A_ij phi_j with fresh polynomial identity testing using the raw formal-degree bound. If the raw formal degree is d, these residuals have degree <=d+1. Union-bound the n+1 checks and all adaptive attempts. A true family input never incurs a false negative from these identity checks; false acceptance probability can be bounded by the chosen delta. Exact expansion is an alternative but its cost cannot be omitted.

The normalized F is quadratic, so its complete Jacobian coefficient family has at most n+1 coefficient matrices and can be extracted exactly in polynomial work. The strong-flag certificate and untruncated inverse-DAG construction are then polynomial. This avoids the degree-2^(n-1) inverse truncation search altogether.

This route was initially proof-level. It has since been implemented and independently replayed as described in the added section below; the older general front end still expands raw polynomials.

## Bit complexity and stable arbitrary-time evaluation

The exact acquisition claim must charge rational input coefficient heights and circuit intermediate heights. For the explicit family built from polynomial-height rational L, B, and the length-n Neumann expression for (JF)^-1, arithmetic heights at the interpolation/PIT points are polynomial in n, the input heights, and log(1/delta). A general short circuit does not have this property automatically: even constant gates can encode exponentially large integers by repeated squaring.

The acquired cyclic matrix can be badly conditioned numerically. Do not evaluate an arbitrary floating-point exp(tA) in that basis and infer the all-time result from the hidden representation. Normalize the chart exactly, recover the low-degree transformed generator by exact coefficient algebra, and recognize/certify its rotation form. For this explicit family, the normalized generator is exactly B,c. Alternatively charge the full change-of-basis precision. Exact rational Krylov/basis coefficients have polynomial binary length here (powers j^k have O(n log n) bits, and determinant bounds give polynomial-height inverses), even when their floating-point condition number is large.

For rational t of binary length b, the angles jt have O(b+log n) input bits. Standard certified argument reduction followed by sine/cosine evaluation requires precision polynomial in b+log n+log(1/epsilon); the period must not be approximated at fixed precision when t is huge. The block-rotation formula, uniform denominator separation, and uniform decoder derivative bound then give absolute epsilon original-state values in polynomial bit complexity in n, rational input size, b, and log(1/epsilon). This is a statement about epsilon-approximate output, not exact transcendental output.

The raw initial point should be admitted by checking the acquired F(x_0) ball condition with exact/interval arithmetic. It is not enough merely to assume x_0 is small in arbitrary input coordinates. A certified superset norm bound is acceptable. Under orthogonal hiding, ||F(x_0)||_2<=1/32 suffices directly.

## Honest comparison

This family supplies a real example where enormous polynomial inverse degree does not force poor conditioning, poles, large values, or expensive arbitrary-time approximate output. It therefore strengthens the resource theorem materially. However an ordinary symbolic algorithm using the same divergence, quadratic dictionary, flag, and rotation form achieves the same complexity. No lower bound against that comparator has been proved. The benefit established is acquisition and a certified compact stable decoder on a specified class, not a new general fast-forwarding principle for nonlinear dynamics.

## Added implementation audit: quadratic circuit acquisition

Inspected `quadratic_circuit_acquisition.py` and `UNIFORMLY_CONDITIONED_FAMILY.md`. The implementation now carries out the quadratic interpolation route directly from arithmetic circuits. The quadratic dictionary and interpolation nodes are fixed by n, not supplied hidden chart data. `acquire(c,raw,...)` has no constructor-chart argument. The trial polynomial's gradient, diagonal and mixed quadratic interpolation formulas, rational Krylov elimination, and affine normalization are correct on inspection.

Identity admission evaluates each interpolation residual at three fresh system-random points drawn independently and uniformly from the integer set of size 2^32. For nonconstant raw degree d, residual degree <=d+1 is valid. The per-residual bound ((d+1)/2^32)^3 and union bound across successful steps are sound; there are exactly n+1 residuals on a successful n+1-dimensional run. No modular reduction or floating-point rank decision is used. This remains Monte Carlo admission for arbitrary input circuits.

The supplied test records serialize the raw arithmetic circuit, its roots, the acquired chart, the acquired matrix, and the normalized matrix. `audit/quadratic_circuit_replay.py` imports **no producer code**: it interprets the serialized gates into SymPy sparse polynomials, computes divergence independently, and checks every projective closure identity by exact coefficient arithmetic. It also independently checks the normalized chart and generator for each constructed case.

All **34** global closure component identities passed across n=2,4,8,16. The normalized chart is the quadratic chain, and the normalized matrix is exactly the claimed block-rotation M in every case. Thus these particular saved examples have deterministic replay, despite the generic front end's Monte Carlo admission. Machine-readable results and exact source/output hashes are in `audit/quadratic_circuit_replay.json`.

The raw support counts are 9, 51, 333, and 2361 terms respectively; the n=16 replay took approximately 2.14 seconds and is charged separately. This matters to the comparison: the tested raw family is sparse enough for conventional sparse recognition too. These measurements are not evidence of an empirical circuit-versus-expanded-raw exponential separation. The exponential quantity is the original-state inverse degree; the certified small decoder removes enumeration of that degree.

The reported `acquisition_seconds` measures the front end and excludes strong-decoder construction and exact normalized-generator checks. It must not be described as total end-to-end solving time without separately charging those stages.

Finally, the theorem's uniform perturbation bound should be read as a bound for **initial-state perturbations and numerical evaluation on the exact certified model**. It is not uniform robustness to errors in the vector field or generator: a small frequency error produces phase error proportional to |t|. Exact rational generator recovery and time-dependent guard precision address computational evaluation, not noisy model identification.

The deterministic quadratic replay reviewed these hashes:

    quadratic_circuit_acquisition.py
    8dd23515557d90de4ddd89821dbe05c8cfd4663e3061046422565a3a20b5f68b
    quadratic_circuit_results.json
    f41cda8b2bae5ca5e44cbf08aa46b84ca509412bac4ce2652cf698c7e3d8cb5a
    audit/quadratic_circuit_replay.py
    a51220601b1efe71b6cbf1b4eeae63c193e79f47035f3d1c675a12ad7aae41a2

Additional focused negative controls passed: f=(x^3,0) fails the quadratic residual test; f=(x,y) returns deficient cyclic rank; f=(x-x^2,(2-4x)y) produces a rank-three module but its nonchart is rejected as a singular basepoint. These are stored in `audit/quadratic_negative_controls.json`. The first is a real randomized rejection run, not an unconditional proof that every future PIT draw will detect that residual.

## Supplemental large-time evaluator

Inspected and reran `conditioned_flow_checks.py`. It reads the actual acquired n=16 artifact, normalizes its chart/generator, builds the decoder from the normalized chart, and uses the recovered block frequencies. It does not call the hidden-family constructor. The denominator sign and rotation orientations are correct. The chosen original initial point is admitted by an exact rational check of ||F(x_0)||_2<=1/32.

The five times 0, 1, +/-10^12, and 10^30+1/3 pass the supplemental bounds. At 10^30+1/3, 80-digit versus 160-digit evaluation differs by about 4.05e-54, while 20-digit evaluation differs by about 1.37e-3. This usefully exposes the large-time precision obligation instead of hiding it in a unit-cost trigonometric call.

These are **precision-agreement tests**, not interval-certified error bounds: the 160-digit reference uses the same algorithm and library. The machine field `max_absolute_error` should be interpreted as difference from that reference, not a rigorously enclosed mathematical error. The analytic theorem, not these samples, proves all-real-time boundedness and supplies the complexity route. A production certified evaluator would need explicit interval/error propagation.

The inspected evaluator source hash is

    61abbdf09aed9269e20e78b8b285ef585c67e4cbbb5c1123478b0f830d393631.

**Final theorem verdict:** the bounded, pole-free, uniformly initial-state-conditioned family and its polynomial-cost approximate arbitrary-time evaluation route are accepted with the stated domain, exact-rational-model, input-height, time-bitlength, PIT, and representation qualifications. The current implementation demonstrates acquisition, exact example replay, and supplemental numerical evaluation. It does not yet implement a fully interval-certified arbitrary-time accuracy guarantee and makes no matched superiority claim over conventional symbolic recognition.
