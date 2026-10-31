# Independent review: monotone noncommuting Gaussian capacity

## Verdict and exact source binding

PASS as a conditional mathematical capacity theorem, with the mass/symmetry convention below. This is not acceptance of a parser, an executable integration backend, or a global diffusion construction from slab data.

Entire source read and hash verified:
- `MATRIX_MONOTONE_CAPACITY_CANDIDATE.md`, SHA-256 `b82715562387da5e0b8549baf24c2d0187d3ca7f191342451b90c3b1fb92b1e9`.
- Conditional-transport dependency `../acquired_entropic_capacity_20261031/PROOF.md`, SHA-256 `9de2b84db7b432a346605b0b0f04b8737ea8424c47346c2fbb58b2684af4f291`. I read its entire body for this review, but this receipt accepts the transport/capacity receiving argument used here, not a fresh code audit of that scalar package.

No source files were modified. Ordinary Gaussian transport and Dirichlet/Thomson principles are credited; historical priority of the resulting integrated inequality is not determined here.

## 1. Gaussian current: noncommutation is handled correctly

For C=beta^{-1} A^{-1}, differentiation gives C'=-beta^{-1} A^{-1}A'A^{-1}. The symmetric Sylvester solution SC+CS=C' exists uniquely since C is positive. At a single evaluation point, diagonalizing A gives

    S_ij=-A'_ij/(lambda_i+lambda_j).

There is no differentiation of eigenvectors and no common eigenbasis assumption. The linear current S z transports the centered Gaussian: its covariance derivative is SC+CS, exactly C'. Its kinetic cost is

    K=Tr(S C S)
     =(1/(2 beta)) sum_ij |A'_ij|^2 /
                         [lambda_i lambda_j(lambda_i+lambda_j)].

The factor 1/2 follows by pairing the i,j terms, including diagonal terms. In particular the one-dimensional expression is (A')^2/(4 beta A^3).

Let B=-A^{-1/2}A'A^{-1/2}. Loewner decrease, not entrywise decrease, implies B>=0. The lower spectral bound then gives

    K <= Tr(B^2)/(4 beta a)
      <= ||B|| Tr(B)/(4 beta a).

The last inequality is a spectral inequality for the single positive matrix B; it does not require B to commute with A.

## 2. Integrated inequality and endpoint sign

The derivative assumption gives ||A'(y)||<=Ly on [0,b], hence ||B||<=Ly/a. With W=sqrt(det A), Jacobi's identity is

    W'/W=Tr(A^{-1}A')/2=-Tr(B)/2.

Thus W decreases and

    K W <= (L/(2 beta a^2)) y(-W').

Integration by parts yields precisely

    integral_0^b K W <= (L/(2 beta a^2))
                              (integral_0^b W - b W(b)).

The discarded boundary term is nonpositive. Evenness of A on the slab implies evenness of K and W, so the two-sided resistance bound is

    R0 <= R1 <= (1+L/(2 beta a^2)) R0.

There is no explicit fiber-dimension factor. This does NOT assert uniformity when the acquired a tends to zero or L grows with dimension. L=0 and zero transport give the exact reduced capacity, as expected.

Loewner monotonicity is substantive. For example a rotating precision R(theta) diag(1,2) R(theta)^T has constant determinant but strictly positive Gaussian transport cost wherever theta' is nonzero. Its B has zero trace and is indefinite. Choosing theta=y^2 even retains A'(0)=0. Thus a determinant-only argument without the positivity premise would fail.

## 3. Capacity receiving and a symmetry qualification

For an admissible full-space test function h, conditional differentiation and fiber integration by parts give

    (E_rho h)'=E_rho[h_y+w.grad_z h].

Conditional Cauchy--Schwarz bounds its square by (1+K) times the conditional full gradient energy. The one-dimensional minimum therefore gives the lower capacity 1/[beta integral (1+K)/p]. Restricting to h(y) gives the upper capacity 1/[beta integral 1/p]. Full-fiber basin boundaries preserve the required constant boundary data under averaging. Gaussian integration and ordinary Dirichlet-domain approximation supply the stated smooth-to-energy-domain passage.

Writing p=q/Z, the normalization cancels in cap/mass. The candidate's MA=integral_b^infinity q is correct for the LEFT basin only if the full marginal is even, not merely if its restriction to [-b,b] is even. I read the source's unqualified 'A(y) is even' as global evenness for this formula. If only slab symmetry is intended, replace MA by integral_{-infinity}^{-b} q; all slab estimates and the factor remain unchanged. The actual global marginal must be the stated q/Z, with no omitted longitudinal energy.

With this convention, the displayed sandwich follows. Capacity/mass is equilibrium conductance in the specified Dirichlet normalization. It is not a Markovian reduction of y_t, an arbitrary-initial-state exit law, or a universal mean passage time. The conservative reversible full diffusion and finite nonzero basin mass remain explicit premises; a local precision estimate alone does not prove them.

## 4. Polynomial noncommuting illustration

For v=(1-y^2)^2 and A=I+v H1+v^2 H2 with H1 positive definite and H2 positive semidefinite, A'=v'(H1+2vH2)<=0 for 0<y<=1/2. A'(0)=0. On this interval v>=9/16, so both a=1 and the proposed sharper bound are valid.

The derivative bounds |v''|<=4 and

    (v^2)''=8(1-y^2)^2(7y^2-1),  |(v^2)''|<=8

are correct. The triangle inequality gives L=4||H1||+8||H2||. For distinct positive v1,v2,

    [A(v1),A(v2)]=v1 v2 (v2-v1)[H1,H2],

so the proposed unequal-diagonal/rank-one two-dimensional blocks genuinely need not commute. Bounded block norms keep the loss bound fixed as blocks are repeated. This alone is not a complete global-rate asymptotic or an acquisition algorithm.

The homogeneous quadratic Hessian P+H1+H2 has the stated unique pivot kernel when the fiber is positive. Recovering all higher coefficients and verifying the entire polynomial are still required. No acceptance is extended to the separately developing parser, unknown/noisy coefficients, or an uncharged coordinate/metric oracle.

## 5. Independent checks and stopping scope

In addition to the symbolic derivation above, I solved the symmetric Sylvester equation exactly over rationals for A=I+v diag(1,3)+v^2 [[1,1],[1,1]], at eleven rational points y=0,1/20,...,1/2. All 33 cost/nonnegativity/trace-sign checks passed. These finite checks are diagnostics, not the proof of the continuum theorem.

No blocking algebraic defect was found. The symmetry convention is the only receiving clarification needed. The global process, determinant/quadrature implementation, exact raw-input recognition, numerical budgets, and strongest historical matching remain separate obligations, as the candidate itself states.
