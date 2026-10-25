# Full WH3 entropy inequality for every affine-projector input

2026-10-25. Analytic receiving theorem. The shifted Schur-log transport pays an unmatched integration interval exactly. It extends the all-projector theorem to arbitrary two-level positive spectra without discarding a Jensen gap or asserting convexity of the entropy deficit.

## Theorem and exact spectral scope

Let N=W_3 tensor id_R and E(X)=I_3/3 tensor Tr_A X. For every orthogonal projection P on the actual finite-dimensional system-reference space and every a,b>=0 with A=aI+bP nonzero,

Delta_N(A):=D(A||EA)-2D(NA||EA)>=0.                       (1)

After normalization this proves the full target for every state with at most two distinct eigenvalues, counting zero, on its actual product support. Flat projectors are included by a=0. No flatness or commutation of the reference marginal is assumed.

A state with two distinct nonzero eigenvalues AND an additional non-product kernel generally has three spectral levels and is not automatically covered. The conclusion is the explicit affine-projector class, not arbitrary spectra.

## 1. Acquired source interface

Write B=E(P). The complete index bound applied to P and I-P gives

P<=9B,  9B-P<=8I.

First use the dense maximal-marginal-rank class constructed in wh3_all_projector_inputs_entropy_theorem.md. In a P/complement decomposition, the exact saturated Schur form is

9B=X_1,
X_r=[[rI+ZZ*, Z sqrt(V)], [sqrt(V) Z*, V]],
H=Z*Z, V>0, H+V<=8I.

The upper identity acts on ran P. The last operator bound is acquired from 9B-P<=8I, not from a trace estimate. Define

D_r(s)=(r+s)(V+sI)+sH,
k_r(s)=[s/(r+s)]D_r(s)^{-1}.

The block inverse formula gives, for every cutoff c>=0,

P log(X_r+cI)P-log(r+c)I
=Z [integral_c^infinity k_r(s) ds] Z*.                 (2)

At c=0 this is the established Schur-log receiver. The shifted identity follows from the same logarithmic resolvent formula after changing variable from s+c to s.

## 2. Shifted compressed logarithm inequality

Put C=(P+3B)/4=X_4/12. We prove for every tau>=0

P log(B+tau I)P-2P log(C+tau I)P+log(1+tau)I>=0.         (3)

For tau>0 set u=9tau and v=12tau=4u/3. The left side of (3), by (2), is

g(u)I+Z [integral_u^infinity k_1(s)ds
               -2 integral_v^infinity k_4(t)dt] Z*,

g(u)=log[(u+1)(u+9)/(u+3)^2].                           (4)

The unshifted positive transport pairs

z=sqrt((s+1)/(s+9)),
t=t(s)=4(3z-1)/(1-z)=s-3+sqrt((s+1)(s+9)),

and gives the exact Loewner comparison of paired integrands and positive measures. Restricting that same comparison to s>=u gives

integral_u^infinity k_1(s)ds
 >=2 integral_(t(u))^infinity k_4(t)dt.                 (5)

Here t(u)>=v. Indeed sqrt((u+1)(u+9))>=3+u/3, since the difference of the squared sides is (8/9)u^2+8u>=0. Thus (5) leaves a genuine negative unmatched interval [v,t(u)], rather than a free deletion of output cost.

## 3. Pay the entire unmatched interval

For every s>0,

D_4(s)>=(s)[(s+4)I+H].

Consequently, by inverse monotonicity,

Z k_4(s) Z*
 <=[1/(s+4)] Z[(s+4)I+H]^{-1}Z*
 <= 8/[(s+4)(s+12)] I.                                (6)

For the last inequality, the nonzero singular values of Z show that the middle expression has eigenvalues h/[(s+4)(s+4+h)], where 0<=h<=8 because H<=8I. The scalar function increases in h. This is a genuine operator bound and does not require [H,V]=0.

The scalar logarithmic margin in (4) pays exactly this interval bound:

16 integral_v^(t(u)) ds/[(s+4)(s+12)]
=2log[((t(u)+4)/(t(u)+12))((v+12)/(v+4))]
=2log[z (u+9)/(u+3)]
=g(u).                                                (7)

In the middle line z=sqrt((u+1)/(u+9)), and (t+4)/(t+12)=z by the defining transport. Combining (4)-(7) proves (3). At tau=0, equation (3) is the preceding unshifted theorem; alternatively take the supported limit already justified in the projector proof.

The interval payment is sharp at the scalar endpoint H=8,V=0. Its role is substantive: the shifted lower integration limits do not match, so the unshifted transport by itself would not prove (3).

## 4. Receive every projection without a marginal-rank assumption

The fixed-rank maximal-marginal-rank approximants P_e from the all-projector theorem converge in norm to any P after adjoining unused reference directions. For tau>0, all operators B_e+tau I and C_e+tau I are uniformly faithful, so ordinary continuous functional calculus proves (3) in the limit; the compressed isometries converge too.

If an enlarged reference was used, the limit is block diagonal between the original reference support and the added spectator directions. The compression onto P lies entirely in the original block. Hence (3) is exactly the desired inequality for the original P and B, not a claim about tracing out a reference or preserving a nonlinear deficit under discarding. For tau=0 the supported logarithm tail bounds in the earlier projector proof apply.

## 5. Integrate a genuine derivative of the physical entropy deficit

By homogeneity it suffices to prove the assertion for A_r=I+rP, r>=0. These inputs are faithful. Since N and E preserve trace and N fixes E,

Delta_N(A_r)=Tr A_r log A_r+Tr E(A_r)log E(A_r)
             -2Tr N(A_r)log N(A_r).

Differentiating the traces, all constant derivative terms cancel, and

Delta_N'(r)=m log(1+r)+Tr B log(I+rB)
            -2Tr NP log(I+rNP),                         (8)

where m=rank P. Self-adjointness of N and operator Jensen for log give

Tr NP log(I+rNP)
=Tr P N(log(I+rNP))
<=Tr P log(I+rN^2P)
=Tr P log(I+rC).

Also Tr B log(I+rB)=Tr P log(I+rB), because log(I+rB) is fixed by E. Therefore (8) is bounded below by

Tr P[log(1+r)I+log(I+rB)-2log(I+rC)].                    (9)

For r>0, equation (9) is nonnegative by (3) with tau=1/r: the scalar log r terms cancel exactly. Thus Delta_N'(r)>=0 for every r>0. Since Delta_N(I)=0, integration proves Delta_N(I+rP)>=0.

No sign was assigned to the Jensen gap beyond its true Loewner positivity. No universal Tr A[log A+log EA-2log(N^2A)]>=0 was assumed; that stronger assertion is independently false for nonflat spectra.

Homogeneity proves (1) for a>0. Taking a down to zero, or invoking the preceding all-projector theorem, handles a=0. Normalization divides the homogeneous deficit by Tr A and preserves its sign.

## Scope and next obstruction

This is a direct entropy theorem for a new nonflat spectral class, not merely a projector derivative diagnostic. It retains arbitrary finite reference dimension, arbitrary projection rank and a possibly nonflat, noncommuting marginal. General states with three or more spectral levels remain open. Layer-cake decompositions, purification, typical projections and reference discarding do not automatically transfer this nonlinear entropy inequality.
