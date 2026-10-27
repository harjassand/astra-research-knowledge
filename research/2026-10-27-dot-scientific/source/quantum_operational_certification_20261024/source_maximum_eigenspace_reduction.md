# A source-compatible maximum-eigenspace principle would settle the full target

2026-10-25. Exact sufficient reduction; the maximum-eigenspace premise remains OPEN. This note does not assert the premise or the unrestricted entropy theorem.

## The proposed weak principle

For every faithful effect 0<A<=I with ||A||=1, let P be its eigenprojection at eigenvalue1, B=E(A), and C=(A+3B)/4. The sufficient assertion is only

Tr P[log B-2log C]>=0.                                  (M)

This is weaker than a Loewner compression inequality and different from the false weighted certificate Tr A[log A+log B-2log C]>=0. It uses the true source relation B=E(A), not merely equal trace, cap and majorization.

## Why the endpoint p=1/4 suffices for every regularization

For 0<p<=1/4 put C_p=pA+(1-p)B. Because A,B<=I, the scalar function

f(p)=-Tr P log C_p

is nonnegative and convex on [0,1). Its supported endpoint value at1 is0 since A is identity on P. To justify the endpoint, C_p>=pA+(1-p)lambda_min(B)I, while C_p<=I, so the compressed logarithm tends to zero. A nonnegative convex function vanishing at the right endpoint is nonincreasing. Hence Tr P log C_p is nondecreasing in p. Thus (M) at1/4 implies the same nonnegative trace at every smaller p.

## Full-target receiving proof

Assume a strict counterexample to WH3 exists. As in wh3_global_reduction_to_strict_log_exclusion.md, choose N_t=(1-t)E+tN, t<1 sufficiently close to1, and a negative global minimizer A on its actual finite reference support. The regularized output is faithful, and opening any input kernel decreases the entropy defect, so A is faithful. Its gradient is

G=log A+log B-2N_t(log N_tA)=lambda I,
lambda=Delta_t(A)/Tr A<0.

Scale A to ||A||=1; the gradient is unchanged because the scalar logarithms cancel. Let P be its maximal eigenprojection. Operator Jensen gives

N_t(log N_t A)<=log(N_t^2A)
=log(pA+(1-p)B), p=t^2/4<1/4.

Since P log A P=0,

lambda Tr P=Tr PG
>=Tr P[log B-2log(pA+(1-p)B)]>=0

by (M) and the preceding monotonicity. This contradicts lambda<0. Therefore (M), if proved, implies the full arbitrary-spectrum WH3 entropy inequality in every finite reference dimension.

## Exact obstruction to forgetting the source interface

Let

A=diag(1,1/1000,2/5),
U=[[4/5,3/5,0],[0,0,1],[-3/5,4/5,0]],
X=UAU*, B=(A+8X)/9.

Both matrices are faithful with equal trace. B is majorized by A since it is a convex combination of unitary copies of A. Moreover

0<=9B-A=8X<=8I.

Nevertheless the exact rational atanh-series certificate top_eigenvector_index_only_obstruction.py proves

e1*[log B-2log((A+3B)/4)]e1 < -1/200.

The script proves I/16<B,C<I by exact Sylvester minors and evaluates60 terms of the matrix atanh series over rationals. With rho=15/17 the total three-log tail bound is less than5.93e-8, while the rational center is below-.00651956. No rounded-eigenvalue sign is used.

This B is NOT asserted to equal the physical conditional expectation of A. Thus the example rejects a generic proof from the two index bounds and majorization alone; it does not reject (M), the WH3 target, or the all-two-level theorem.

## Current status

The source-compatible premise (M) remains unproved. A bounded source-compatible diagnostic did not find a negative maximal-eigenvector trace; that observation is not part of the argument. The existing shifted-projector transport verifies the affine-projector special class, but an arbitrary spectral tail changes the acquired Schur interface and cannot simply be replaced by a scalar multiple of the identity. Any next proof must obtain that interface or retain the channel's actual Jensen gap through a weaker gradient formulation.
