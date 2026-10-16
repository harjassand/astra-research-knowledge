# Exact reverse-RLD radius for classical-input quantum-output channels

## Statement for faithful quantum outputs

Let a classical-input quantum-output channel prepare density matrices sigma_i>0 on C^d for input i=1,...,m. The sigma_i need not commute. Consider the complete conditional RLD/Petz-chi-square excess coefficient: arbitrary finite reference dimension, faithful baseline blocks R_i summing to I, Hermitian tangents H_i, and subtraction of the untouched reference contribution. Input pairs may have unequal reference marginals.

Its exact value is

C = min_{U=U*} max_i Tr[(sigma_i-U)sigma_i^-1(sigma_i-U)]
  = 1-min_{p in Delta_m} Tr[(sum_i p_i sigma_i^-1)^-1]
  = 1-1/K,

where

K=min_{omega>=0, Tr omega=1} max_i Tr[omega sigma_i^-1 omega].

Thus the proposed reverse quantum chi-square radius is correct for faithful outputs, even when they do not commute. The same constant is sharp for the operator-valued reference defect. Reference dimension at most min(m,d^2)-1 suffices in the supremum for a nonconstant channel; the physical lower witness needs no additional coherent flag. Constant channels have coefficient zero.

This theorem does not include singular outputs without a separate support convention and proof. It is a mathematical derivation, not a literature-priority claim.

## 1. The physical conditional defect

Let A=sum_i sigma_i tensor R_i and J=sum_i sigma_i tensor H_i, K=sum_i H_i. Put Z_i=H_i-R_i K, so sum Z_i=0. The output centered matrix is

Z=sum_i sigma_i tensor Z_i=J-A(I_d tensor K).

Since Tr_output A=I and Tr_output J=K, expansion gives

Tr_output[J A^-1 J]-K^2=Tr_output[Z* A^-1 Z].

The input conditional defect is sum_i Z_i*R_i^-1 Z_i. Therefore an inequality between these two positive operator-valued forms proves the physical upper bound. Reference congruence handles baseline blocks summing to arbitrary W>0 without changing dimension.

## 2. Noncommutative weighted Cauchy gives the upper bound

For positive A_i and arbitrary B_i, matrix weighted Cauchy says

(sum B_i)*(sum A_i)^-1(sum B_i)<=sum B_i*A_i^-1 B_i.

Apply it with

A_i=sigma_i tensor R_i,
B_i=(sigma_i-U) tensor Z_i.

Since sum Z_i=0, sum B_i=Z. Partial trace over the quantum output gives

Tr_output[Z*A^-1 Z]
<=sum_i f_i(U) Z_i*R_i^-1 Z_i,
f_i(U)=Tr[(sigma_i-U)*sigma_i^-1(sigma_i-U)].

For Hermitian U, this is the stated f_i. Therefore C<=min_U max_i f_i(U). No commuting inverses, entrywise harmonic means, or tensor inverse elimination is used. In particular the inverse of sum_i sigma_i tensor R_i is handled directly by weighted Cauchy.

## 3. Minimax and radius identification

For Hermitian U,

f_i(U)=1-2Tr U+Tr[U sigma_i^-1 U].

These are uniformly coercive strictly convex quadratics. Epigraph KKT duality or finite-dimensional convex minimax yields

min_U max_i f_i(U)=max_p min_U sum_i p_i f_i(U).

Let M_p=sum_i p_i sigma_i^-1>0. The inner objective is 1-2Tr U+Tr U M_p U. Its stationarity equation is M_p U+U M_p=2I; the unique solution is U=M_p^-1. The resulting value is 1-Tr M_p^-1, proving the harmonic formula.

For the density-constrained radius, minimax on the compact convex density set gives

K=max_p min_{omega density} Tr omega M_p omega.

The unique inner optimum is omega=M_p^-1/Tr M_p^-1, with value 1/Tr M_p^-1. Positivity is automatic. Hence K=1/min_p Tr M_p^-1 and C=1-1/K.

The unrestricted quadratic center U is not a density matrix. Confusing it with omega changes the minimax problem; the normalized radius relation includes optimization of its scale.

## 4. Weighted-simplex vector lower witness

First choose p_i>0 for all i and m>=2. Let s=(sqrt(p_i)), P=I-ss*, and H=s^perp of dimension m-1. Put v_i=P e_i,

R_i^0=v_i v_i* on H,
z_i=sqrt(p_i) v_i.

Then sum R_i^0=I_H, sum z_i=0, and the supported inverse input energy is E=sum z_i*(R_i^0)^+z_i=sum p_i=1.

On C^m tensor C^d, let D=direct_sum_i sigma_i. Decompose the classical factor into span{s} plus H. The compressed lower-right block of D is

A_H=(P tensor I_d)D(P tensor I_d)|_(H tensor C^d)
   =sum_i R_i^0 tensor sigma_i.

The off-diagonal block W:C^d -> H tensor C^d is

W=(P tensor I_d)D(s tensor I_d)=sum_i z_i tensor sigma_i.

All sigma_i are faithful, so A_H>0. The Schur-complement identity gives

W* A_H^-1 W
=sum_i p_i sigma_i-(sum_i p_i sigma_i^-1)^-1.

Taking trace yields output vector energy

N=1-Tr M_p^-1.

Thus the vector lower ratio equals the dual value for every positive p. Faithful regularization R_i(delta)=(R_i^0+delta I)/(1+m delta) preserves sum I, and all supported input energies converge while the output inverse is continuous. Positive priors are dense and the harmonic expression is continuous, proving sharpness at any maximizing prior.

## 5. Same-dimension Hermitian physical realization

Choose real h_i not all equal and set H_i=h_i R_i^0, K=sum H_i. Then Z_i=H_i-R_i^0 K has range in span(v_i), and sum Z_i=0. Since [v_1,...,v_m] has kernel exactly span{s}, there is one common row w* such that

Z_i=z_i w* for every i,
w*=s*diag(h)P.

Its squared norm is the p-weighted variance of h, hence positive. The output centered matrix is, up to tensor-factor ordering,

sum_i sigma_i tensor Z_i=W(I_d tensor w*).

Cyclicity of trace therefore gives the output physical defect ||w||^2 Tr W*A_H^-1W, while the input physical defect is ||w||^2 E. Their ratio is exactly the vector lower value.

Subtracting the same scalar from all h_i leaves Z_i unchanged and can make Tr K=0. Keep these H_i fixed during faithful baseline regularization. They are supported on the original input blocks, giving convergent input costs; the quantum output baseline is already positive definite and its costs are continuous. Divide all blocks by m-1 and choose a sufficiently small nonzero tangent perturbation. This produces faithful normalized physical state pairs, with the exact quadratic Petz-Q2 identity.

If a maximizing prior has support k<m and the coefficient is positive, restrict to that support first and use reference dimension k-1, then add inactive inputs by faithful regularization. No extra coherent flag is needed. These are sufficient reference dimensions, not claims of minimality.

### Improved sufficient reference dimension

View M_p in the real vector space of Hermitian d-by-d matrices, of dimension d^2. The dual minimizes F(M)=Tr M^-1 over the convex hull of sigma_i^-1. Its gradient at an optimum M_* is the nonzero Hermitian matrix -M_*^-2. First-order optimality places M_* in the exposed minimizing face for this gradient. If the hull has full dimension, that face has affine dimension at most d^2-1; if the hull has smaller dimension, its affine dimension is already at most d^2-1. Caratheodory therefore represents M_* using at most d^2 vertices. The same coefficient has an optimal prior on at most min(m,d^2) inputs, so the physical frame witness requires at most min(m,d^2)-1 reference dimensions. This is a sufficient bound, not a minimality assertion.

## 6. Small semidefinite upper certificates

Using column vectorization, define B_i=I_d tensor sigma_i and u_i=vec(sigma_i-U). Then f_i(U)=u_i*B_i^-1u_i. Consequently the minimax has an SDP description with Hermitian U and scalar c:

minimize c subject to [[c B_i,u_i],[u_i*,1]]>=0 for every i.

Each block has size d^2+1. There are d^2+1 real optimization variables. Rational-complex outputs and trial U produce exact rational-complex certificate matrices. Numerical optimization alone is not an exact certificate; matching dual priors give rigorous lower bounds.

## 7. Exact rational noncommuting qubit benchmark

Let X,Y,Z be the Pauli matrices and take three prepared states

sigma_X=(I+(3/5)X)/2,
sigma_Y=(I+(3/5)Y)/2,
sigma_Z=(I+(3/5)Z)/2.

They have eigenvalues 4/5 and 1/5 and do not commute. Use the dual prior p=(1/3,1/3,1/3). Then

M=sum p_i sigma_i^-1
 =[[5/2,(-5+5i)/8],[(-5-5i)/8,15/4]],
U=M^-1=[[24,4-4i],[4+4i,16]]/55,
Tr U=8/11.

Exact arithmetic gives f_X(U)=f_Y(U)=f_Z(U)=3/11. The primal and dual certificates therefore match:

C=3/11,
K=11/8,
omega=U/Tr U=[[3/5,(1-i)/10],[(1+i)/10,2/5]].

The weighted-simplex physical lower witness uses a qubit reference. This benchmark establishes the theorem on genuinely noncommuting quantum outputs; it is not a relabeled classical stochastic channel. No claim about its ordinary scalar-reference coefficient is needed here.

## Physical meaning

The coefficient is the minimum erasure reveal probability required to dominate this classical-input quantum-output channel in complete conditional standard-Petz/RLD comparison. Quantum output noncommutativity does not obstruct the radius formula: weighted matrix Cauchy supplies the upper certificate, and a block Schur complement supplies a matching noncommutative lower construction. The information in the untouched reference is subtracted; this is not the ordinary tensor-with-identity SDPI coefficient, which can be one.

## Additional symmetric rational benchmark

Choose four qubit Bloch vectors (b,b,b), (b,-b,-b), (-b,b,-b), (-b,-b,b), with 0<b<1/sqrt(3), and sigma_i=(I+v_i dot Pauli)/2. All have squared Bloch length 3b^2 and sum v_i=0. Uniform p gives M=2I/(1-3b^2), and U=(1-3b^2)I/2. Each primal cost equals 3b^2, so C=3b^2 exactly. At b=1/4 all state entries and certificates are rational-complex and C=3/16. The general construction provides a three-dimensional reference witness; this does not assert that three dimensions are necessary.

## Resource and interpretation boundary

The task assumes a specified classical input alphabet and the ability to prepare the listed quantum output states, with an untouched finite quantum reference. It compares standard-Petz/RLD quadratic distinguishability after subtracting reference information. Realizing the sharpness witness requires controlled, generally noncommuting conditional reference blocks and sufficiently small faithful state perturbations; it does not require entangled classical-reference input states. The erasure source is a classical reveal-or-erase measurement. The threshold does not state that the quantum-output channel can be simulated from erasure by a physical postprocessing channel. The reverse quantum radius itself is an established type of information-radius objective; the identification with this complete conditional coefficient requires the proof above and has not been claimed historically new.

## Tensor-product consequence

For two faithful prepared-state families with independent input alphabets, their product family obeys K_product=K_1 K_2, hence

1-C_product=(1-C_1)(1-C_2).

For the upper bound on K, take product density centers: Tr[(omega_1 tensor omega_2)(sigma_i tensor tau_j)^-1(omega_1 tensor omega_2)] factors, giving K_product<=K_1 K_2. For the lower bound, use product optimal dual priors; the corresponding inverse harmonic matrix is M_p^-1 tensor N_q^-1, whose trace factors. The harmonic dual therefore gives K_product>=K_1 K_2. This is standard radius-additivity structure and is not claimed as a new additivity theorem.

## Executable exact check

Run the package verification runner, or execute checks/verify_cq_exact.py by its full path. SymPy verifies the rational-complex primal and dual certificates, the tetrahedral benchmark, and the exact 4-by-4 inverse frame identity for the three-Pauli benchmark. It also checks same-reference-dimension Hermitian input defect 2/3 and output defect 2/11, giving ratio 3/11. The verification runner prints the exact certificate results. The frame baseline is supported; the theorem's faithful regularization justifies the physical supremum.
