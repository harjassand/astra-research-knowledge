# A finite residual-certified compiler for the learned passive model

## 1. Endpoint and conventions

The compiler takes the **already acquired, finite encoded model**

\[
\widehat K(t)=\sum_{j=1}^m w_j e^{-\lambda_jt},
\qquad w_j>0,\quad\lambda_j\ge0,
\]

the measured encoded bath force \(c\), a known strongly convex potential, a finite force description, a horizon \(T\), and a requested numerical residual allowance \(\varepsilon_{\rm num}>0\). It emits rational knots defining a continuous piecewise-linear path \(y\), with \(y(0)=x_r\), and proves

\[
\boxed{
\|\rho\|_{L^\infty(0,T)}\le\varepsilon_{\rm num},\qquad
\rho=y'+V'(y)+\widehat K*y'-f-c.
}
\tag{1}
\]

The sign of \(c\) matters: backward's measured \(c\) is a positive bath force, so the predictor equation is \(y'+V'(y)+\widehat K*y'=f+c\).

The certificate applies to the emitted rounded path and the exact exponential kernel specified by the encoded rational model. It does not substitute a floating ODE solution for the output or rely on a floating nonlinear solver.

The concrete implementation uses

\[
V'(y)=a y+b y^3,\qquad a>0,\ b\ge0,
\]

with rational coefficients and rational piecewise-affine forcing. All scalar evaluations are exact rational arithmetic. The derivation below extends to other known \(V'\) and bounded piecewise-Lipschitz \(f\) if their finite descriptions include enclosing evaluation algorithms with explicitly charged cost. Strong convexity alone is not a computability assumption.

## 2. Exact exponential update on an emitted linear segment

Let \(t_k\le t\le t_k+h\), and write

\[
y(t_k+s)=y_k+v s,\qquad
v=(Y-y_k)/h,\quad0\le s\le h.
\]

For the exact convolution state

\[
q_j(t)=\int_0^t e^{-\lambda_j(t-u)}y'(u)\,du,
\]

the next endpoint is

\[
q_j^+=a_jq_{j,k}+\psi(\lambda_jh)(Y-y_k),\qquad
a_j=e^{-\lambda_jh},
\tag{2}
\]

where

\[
\psi(z)=\frac{1-e^{-z}}z=\int_0^1 e^{-zu}\,du,\qquad \psi(0)=1.
\]

Thus no numerical quadrature over the full history is required. For \(\lambda_j=0\), use the exact identity

\[
q_j(t)=y(t)-x_r
\tag{3}
\]

rather than allowing roundoff to accumulate in a recurrence.

The endpoint equation for \(Y\) is

\[
G_k(Y)=\frac{Y-y_k}{h}+V'(Y)
+\sum_jw_j\left[a_jq_{j,k}+
\psi(\lambda_jh)(Y-y_k)\right]
-f(t_k+h^-)-c=0.
\tag{4}
\]

For \(Y_2>Y_1\),

\[
G_k(Y_2)-G_k(Y_1)
\ge\left[h^{-1}+\mu+\sum_jw_j\psi(\lambda_jh)\right](Y_2-Y_1).
\tag{5}
\]

The equation has a unique root. If \(V'\) is \(L\)-Lipschitz on the protected interval below, its Lipschitz constant is at most

\[
C_h=h^{-1}+L+B,\qquad B=\sum_jw_j.
\tag{6}
\]

Only two mode-dependent sums are needed during the scalar solve:

\[
H_k=\sum_jw_ja_jq_{j,k},\qquad
P_h=\sum_jw_j\psi(\lambda_jh).
\]

After forming their intervals in \(O(m)\) arithmetic operations, each bisection test costs one scalar potential evaluation and a bounded number of interval operations. The memory-mode loop is not repeated inside bisection.

## 3. A protected interval, independent of step size and hidden source rates

Suppose \(|f|\le F\). Let \(A_0\ge|V'(x_r)-c|\) be a supplied rational bound and choose

\[
R=\frac{F+A_0+\varepsilon_{\rm num}}{\mu},\qquad
I=[x_r-R,x_r+R].
\tag{7}
\]

The small positive margin is convenient for robust endpoint bracketing. Obtain a finite bound \(L\) for the Lipschitz constant of \(V'\) on \(I\).

Let \(u_j=y-q_j\). On every linear segment \(u_j'=\lambda_j(y-u_j)\), with \(u_j(0)=x_r\). If the emitted path remains in \(I\), so do all exact \(u_j\). Hence

\[
|q_j|\le2R.
\tag{8}
\]

The endpoint root lies in \(I\). To see this at the upper boundary \(Y=x_r+R\), note \(Y\ge y_k,u_{j,k}\). Since \(\psi(z)\ge e^{-z}\),

\[
q_j^+=a_j(Y-u_{j,k})
+[\psi(\lambda_jh)-a_j](Y-y_k)\ge0.
\]

Also \(v\ge0\) and \(V'(Y)-c\ge F+\varepsilon_{\rm num}\). Thus \(G_k(Y)>0\). The lower endpoint has the reverse signs. This proves bracketing without an assumption about the approximate stored modal state. Bisection emits only values in \(I\), so the property holds inductively for the actual rounded path.

Take

\[
\tau=\varepsilon_{\rm num}/4.
\]

Whenever the true endpoint residual is at most \(\tau\), (4) and (8) give the slope budget

\[
|v|\le
U:=F+A_0+(L+2B)R+\tau.
\tag{9}
\]

The implementation also records the actual maximum rational slope, usually much smaller than this planning bound.

## 4. A finite step size that guarantees the residual bound

On a force continuity piece let \(L_f\) bound its temporal Lipschitz constant. Set

\[
C=\sum_jw_j\lambda_j<\infty,\qquad
D=(L+B)U+L_f+2RC.
\tag{10}
\]

Every rate in this expression belongs to the learned encoded model, not to the unknown microscopic source.

Because \(q_j'=v-\lambda_jq_j\), its exact derivative is bounded by \(|v|+2R\lambda_j\). Thus throughout a step,

\[
|\rho(t)-\rho(t_k+h^-)|
\le h[(L+B)U+L_f+2RC]=hD.
\tag{11}
\]

Consequently a fixed step size

\[
h\le h_*:=\frac{\varepsilon_{\rm num}}{2D}
\tag{12}
\]

is sufficient, with numerical slack left over after the endpoint solve and finite-state enclosures. If \(D=0\), one step per force piece suffices.

There is no exponential-in-\(T\) Gronwall factor. The rate-dependent cost is explicit through \(C\le B\lambda_{\max}\). A large retained rate can require finer time steps; it is not hidden in a solver oracle.

### A sharper check used by the implementation

Each exact \(q_j\) is monotone on a constant-slope segment:

\[
q_j'(t_k+s)=(v-\lambda_jq_j(t_k))e^{-\lambda_js}.
\]

Therefore

\[
\sup_{\rm step}|\rho|
\le |\rho(t_k+h^-)|
+L|Y-y_k|+L_fh
+\sum_jw_j|q_j(t_k+h)-q_j(t_k)|.
\tag{13}
\]

Outward modal endpoint intervals make the right-hand side rigorously computable. The code accepts a segment only if this complete within-step certificate is at most \(\varepsilon_{\rm num}\). It does not certify only the mesh points.

## 5. Finite coefficient and state precision

Align the mesh with the finitely many force breakpoints. For a force piece of duration \(T_r\), let

\[
k_r=\max\{0,\lceil\log_2(T_r/h_*)\rceil\},\qquad
N_*=\sum_r2^{k_r}.
\tag{14}
\]

This is an explicit upper bound on the number of accepted dyadic segments. In particular \(N_*\le2T/h_*+\#\{\text{force pieces}\}\).

For \(B>0\), choose coefficient and outward state-rounding allowances

\[
\eta_c=\frac{\tau}{256BRN_*},\qquad
\eta_s=\frac{\tau}{64BN_*}.
\tag{15}
\]

Enclose both \(a_j\) and \(\psi(\lambda_jh)\) by rational intervals of width at most \(2\eta_c\), contained in \([0,1]\). Store each modal state in an interval, rounding its endpoints outward by at most \(\eta_s\), then intersect with \([-2R,2R]\). Intersection is sound because of (8). Zero-rate modes use (3) exactly.

If \(W_k\) bounds a stored modal interval's width, direct interval propagation in (2) gives

\[
W_{k+1}\le W_k+8R\eta_c+2\eta_s.
\]

Hence, after at most \(N_*\) accepted steps,

\[
W_k\le \tau/(16B).
\tag{16}
\]

The interval for (4), formed using the two preaggregated sums, has width at most

\[
BW_k+8BR\eta_c
\le \tau/16+\tau/(32N_*)\le3\tau/32.
\tag{17}
\]

This is why interval bisection cannot stall on unresolved signs: an interval straddling zero is already narrow enough to certify a small residual.

For the exact rational polynomial/affine fixture, the algorithm accepts a midpoint once its residual interval is contained in \([-\tau/2,\tau/2]\). Otherwise its sign is resolved and one half of the bracket is discarded. From (6), a safe bound on the number of scalar evaluations is

\[
3+\left\lceil
\log_2\max\{1,8RC_h/\tau\}
\right\rceil.
\tag{18}
\]

For general supplied evaluators, allocate additional potential/force enclosure widths, for example at most \(\tau/32\) each, and use the corresponding slightly enlarged stopping threshold below \(\tau\). Their evaluation cost is part of the compiler cost.

### Stable computation at zero and very small rates

For \(z\le1\), compute \(\psi(z)\) from the alternating series

\[
\psi(z)=\sum_{n=0}^\infty\frac{(-z)^n}{(n+1)!}.
\]

For \(z>1\), use a certified enclosure of \(e^{-z}\) in \((1-e^{-z})/z\); division is then well conditioned. The exponential enclosure itself uses range reduction, consecutive alternating Taylor sums on \([0,1]\), and repeated squaring. If \(z\) exceeds the requested precision in the stated units, \(e^{-z}\le2^{-z}\) supplies a cheap small enclosure.

This avoids division by a tiny rate and treats zero continuously. No inverse hidden spectral gap appears in the precision requirement.

## 6. Adaptive steps still terminate

The implemented adaptive rule begins with the whole current force piece. If the certificate (13) fails, it halves the proposed step without advancing time or modal state. After acceptance, it continues at that size; it may halve further but never increases the size within the piece.

After at most \(k_r\) halvings, the step is at most \(h_*\). The true within-step variation is bounded by \(\varepsilon_{\rm num}/2\). The accepted endpoint solve contributes at most \(\tau\), and endpoint-interval overestimation contributes at most \(2BW_k+B\eta_s\). Equations (15)–(16) put the resulting bound below \(\varepsilon_{\rm num}\). Thus a certified segment must be accepted by that level.

All accepted endpoints lie on the finest planned dyadic mesh, so there are at most \(N_*\) accepted steps. There are at most \(\sum_r k_r\) rejected attempts. Failed attempts do not accumulate state error.

The acceptance test is optional for correctness: running directly on the finest planned mesh is a finite fixed-step algorithm with the same guarantee.

## 7. Work, storage, and bit costs

For one attempted step:

- Forming the two memory sums, updating the \(m\) interval states, and checking the modal variation uses \(O(m)\) arithmetic operations.
- Bisection adds \(O(\log(RC_h/\tau))\) scalar potential evaluations, independent of \(m\). For a fixed-degree polynomial, each has bounded arithmetic operation count.
- Coefficients depend only on the rate and step size. The implemented dyadic rule generates at most \(\#\{\text{pieces}\}+\sum_rk_r\) coefficient banks and discards obsolete banks, retaining only the current one.

It is accurate to call this linear work in the number of modes, with explicit scalar-solve and precision factors. It is not an \(O(m)\) bit-operation claim.

Let \(L_{\rm in}\) be the input encoding length. Coefficient and state fractional precision is

\[
O\!\left(
L_{\rm in}+
\log\frac{BRN_*+BN_*+1}{\varepsilon_{\rm num}}
\right).
\]

Endpoint positions are selected from bisections of the same fixed rational interval \(I\), so their denominators do not compound over time. Modal intervals are rounded outward at fixed precision, preventing accumulated denominator growth. Arithmetic therefore uses finite bit lengths controlled by input precision and the displayed iteration bounds.

Online memory is \(O(m)\) fixed-precision modal intervals, the current position, and scalar working values, plus the supplied force/potential program. Storing the complete emitted path costs one rational knot per accepted step. Arbitrary policy-history storage, if requested, is additional.

## 8. Independent verification from the saved path

The compiler writes rational knots to a file and reloads them. A separate pass reconstructs the exact convolution intervals from those knots, beginning at zero modal memory. It uses fresh exponential and \(\psi\) enclosures with eight additional fractional bits and its own outward state updates. It does not read the compiler's modal states or endpoint-solver residuals.

For every emitted segment it independently checks:

1. The rational endpoints remain in \(I\).
2. The force piece contains the entire segment.
3. The exact finite-kernel endpoint residual is enclosed.
4. Equation (13) bounds the entire segment's residual.
5. The bound is at most the requested numerical allowance.

The result is a certificate for the actual encoded path. No floating diagnostic or sampled residual is used in this verification.

## 9. Joined execution on the actual acquired model

The executed source is

`../bridge/physical_bridge_results.json`

with SHA256

`e15c2b0a2d7f51e909d7f3c7f059edc190ec134dd6d2f1c3948bb55a6027b3aa`.

Only its learned six-mode rational model and declared acquisition/initialization receipts enter the compiler. Microscopic source rates, BDF solutions, and source simulation state do not.

The executable's `main()` is explicitly a fixture adapter: it asserts the source's \(B=T=\mu=1\) normalization and \(F=2/5\), and labels its supplied \(x_r=0\), \(V'(x)=x+3x^3/20\). The JSON is not treated as a description of an arbitrary potential. The general `compile_path` entry point receives its potential, force, and reference coordinate explicitly.

Deployment begins after the source's finite \(10^{-6}\)-duration trap release and drive rise. The adapter requires `initialization.deployment_initial_coordinate_bound`; it never substitutes the preceding hold's tracking allowance. The source supplies the updated post-release force-forecast bound as well. The learned fit, pre-release records, encoded \(c\), and emitted numerical path are unchanged by this interface correction.

The fixture uses

\[
T=1,\quad V'(x)=x+\frac3{20}x^3,\quad
f(t)=\frac7{20},\quad F=\frac25,\quad x_r=0,
\quad\varepsilon_{\rm num}=\frac1{1000}.
\]

The measured bath force is encoded as

\[
c=\frac{54405674475}{1099511627776}.
\]

Its difference from the supplied decimal report is included exactly in the initialization error allowance.

| Quantity | Executed result |
|---|---:|
| Learned positive modes | 6 |
| Planned maximum accepted steps | 16,384 |
| Actual accepted segments | 1,024 |
| Rejected coarser trials | 10 |
| Scalar bisection evaluations | 21,436 |
| Distinct coefficient step sizes | 11 |
| Compiler mode-loop visits for sums, updates, certificates | 18,612 |
| Compiler exponential/\(\psi\) coefficient pairs | 66 |
| Verifier mode-loop visits / coefficient pairs | 12,288 / 6 |
| Compiler coefficient/state fractional bits | 35 / 33 |
| Independent verifier coefficient/state bits | 43 / 41 |
| Largest online modal interval integer payload | 746 bits; verifier 938 bits |
| Largest current coefficient-bank integer payload | 1,664 bits |
| Largest single bisection residual rational payload | 404 bits |
| Verified residual supremum | \(0.000786240803547\) |
| Actual emitted maximum speed | \(0.398790660436\) |
| Saved knots | 1,025 |
| Knot integer payload | 151,074 bits |
| Complete JSON path file | 82,723 bytes |

The latest runtime on this executor was approximately 0.89 seconds for compilation and 0.19 seconds for verification. These are observations about this fixture, not worst-case complexity claims. Integer-payload counts omit container/serialization overhead; the complete path-file byte count includes its JSON encoding.

A separate boundary fixture exercises a zero pole, a \(10^{-12}\) pole, a \(10^6\) pole, a force jump, and both signs of velocity. It is executed by `passive_compiler_boundary_checks.py` and independently verifies the complete residual on every segment. It is separate from the physical-source receipt and does not alter that receipt's certificate.

Outputs:

- `passive_execution_compiler.py`
- `passive_compiler_path.json`
- `passive_compiler_results.json`

The saved path SHA256 is

`77b5254c1cbfdfa09abf4bae0326c6e70823170f65fe2365374d2e9c548b40f8`.

## 10. Direct physical trajectory certificate

The backward comparison uses the actual emitted path, whose reference initial coordinate is exact. Let \(\delta\) bound the actual physical starting-coordinate mismatch, \(\gamma\) bound the old-force forecast error including the rounding of \(c\), and \(\zeta\) be the certified kernel \(L^1\) error. Then

\[
\boxed{
\sup_{0\le t\le T}|x(t)-y(t)|
\le
\max\left\{\delta,\,
\frac{\zeta\|y'\|_\infty+\gamma+\|\rho\|_\infty}{\mu}
\right\}.
}
\tag{19}
\]

The velocity is the numerical path's exact rational maximum slope. An exact-model velocity bound is not silently substituted into this direct residual accounting.

For the joined source, the compiler consumes the exact rational fit certificate plus the stated \(0.006\) smoothing allowance, rounds the supplied **post-release** initialization and coordinate bounds upward, and adds the exact \(c\)-encoding error. The release-aware coordinate allowance is rounded upward to \(1.391625\times10^{-6}\). The supplied force-forecast allowance \(0.001008399318370488\) is rounded upward to \(0.001008399319\), before adding the exact encoding error. The resulting rational certificate has numerical value

\[
\boxed{\sup_{0\le t\le1}|x(t)-y(t)|
\le 0.0102656854708.}
\]

This is conditional on the supplied physical acquisition and initialization event. The compiler does not convert a synthetic physical fixture into a laboratory validation or independently establish its supplied physical premises.

## 11. Feedback and general input representations

The implemented fixture is a prescribed force. It remains valid if that force was chosen after inspecting the acquired model.

The backward \(\mu-\kappa\) comparison applies to separately executed causal feedback policies only under its stated sup-history Lipschitz gain \(\kappa<\mu\), common prehistory, bounded action, and correctly accounted numerical residual. A compiler for such a policy also needs its finite evaluation algorithm and a temporal regularity bound along the candidate piecewise-linear histories. Those costs and any policy-history storage are additional.

If the force endpoint depends on a trial endpoint \(Y\) through a causal policy of gain \(\kappa\), the same endpoint construction remains strongly monotone with lower slope \(h^{-1}+\mu-\kappa\). The supplied temporal modulus replaces \(L_f\) in the residual bound. An arbitrary discontinuous or computationally unspecified policy is outside this digital guarantee.

For general \(V\), the necessary representation condition is likewise explicit: provide finite enclosing evaluation of \(V'\), its strong-monotonicity constant, and a local upper Lipschitz bound on the computable protected interval. The concrete rational-polynomial implementation fully supplies that interface for the executed nonlinear fixture.

