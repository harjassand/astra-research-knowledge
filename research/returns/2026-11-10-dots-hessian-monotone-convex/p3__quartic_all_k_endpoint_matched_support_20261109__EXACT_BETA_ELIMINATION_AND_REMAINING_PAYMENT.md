# Exact beta-affine elimination and the remaining coupled payment

9 November2026. Author construction for the fixed endpoint-matched translator. The complete all-k support is NOT established.

## 1. Original scaling and exact identity

Use the complete support polynomial scaled by8nm as in MATRIX.json, with n=k+1,m=3k+1,ell=3k-1, k>1/3. Let A=[[alpha,beta],[0,delta]], X=[[x,2kV],[-mV,y]], and T=V^2. The polynomial has the exact form

    Pscaled=(q0+q2 T) beta^2+2V(L0+T L1)beta
                               +R0+T R1+T^2 R2,

where R0,R1,R2,L0,L1 are preserved literally in TRANSVERSE_BLOCKS.json or recovered by the frozen source from MATRIX.json. In particular

    q0=2ell[m(x^2+y^2)-2(k-1)xy]>=0,
    q2=2nm(69k^2+22k+1)>0,
    L1=2kn^2m(81k^2+42k+1),
    R2=k^2n^2m(243k^3+405k^2+129k-1).

For q=q0+q2T>0, completing the actual affine beta square gives

    q Pscaled=q^2[beta+V(L0+TL1)/q]^2
                      +K0+T K1+T^2 K2+T^3 K3,          (1)

    K0=q0R0,
    K1=q2R0+q0R1-L0^2,
    K2=q2R1+q0R2-2L0L1,
    K3=q2R2-L1^2.

The only q=0 case is X=0, which is trivial. Every determinant and affine interaction is retained. This is not an independent minimization of mean blocks.

## 2. Three paid pieces for the whole parameter half-line

K0>=0 for all k>1/3 by the full diagonal pointwise support. The complete proof and exact rational Gram are in quartic_all_k_diagonal_gram_20261109/EXACT_DIAGONAL_GRAM_PAYMENT.md, SHA2563266b6631f45a922f28977e1ca337a87859dc095fbe2f2e2372f34960fed7a95. This block was constructed jointly from the exact invariant extraction and the lead's single fixed Gram, not from parameter samples.

K3 is explicitly positive:

    K3=6k^2 n^3 ell m^2(405k^4+864k^3+354k^2+24k+1)>0.

K2 is a homogeneous quadratic form in(alpha,delta,x,y). Its exact symmetric4x4 matrix is in TRANSVERSE_BLOCKS.json. Its leading principal minors are

    4k^2 n^2 ell m^2(9k+1)(69k^2+22k+1),

    384k^3 n^4 ell^2 m^5(69k^2+22k+1)^2,

    256k^4 n^6 ell^3 m^6(69k^2+22k+1) P7,

    2048k^5 n^9 ell^4 m^7 P13,

where

    P7=263898k^7+451737k^6+231174k^5+56421k^4
                                     +4350k^3+515k^2+34k-1,

    P13=1444456638k^13+9307126233k^12+17226049842k^11
       +14203423386k^10+6139208376k^9+1321705755k^8
       +50568948k^7-34434468k^6-6171906k^5-335793k^4
                         -4646k^3-1078k^2-116k-3.

P7>0 since34k-1>0. For P13 and k>=1/3, all negative terms are bounded in magnitude by56215458k^6. The single positive term1321705755k^8 is at least146856195k^6. Thus its surplus is at least90640737k^6, with every other positive term untouched. All four minors are strictly positive. Hence K2 is positive definite for all k>1/3.

These statements pay the actual blocks, not a separate reserve that may be added to the original support a second time.

## 3. A precise failure of coefficientwise positivity

The one unpaid quartic K1 is NOT nonnegative in isolation. At k1,x0,y1, divide it by its positive factor2n ell m=32. Its exact form is

    64[33alpha^2-48alpha delta+35delta^2
                             +2alpha+22delta+23/4].       (2)

At alpha=-1/2,delta=-2/3, expression(2) is -1216/9. Its unrestricted two-mean minimum is -78512/579, attained at alpha=-299/579,delta=-129/193.

This does NOT refute the full translator: at k1 the complete support was independently proved for every state. It demonstrates exactly why K0,T^2K2,T^3K3 cannot be discarded while pricing T K1. The witness is also only a constant-matrix allocation test, not a compatible periodic negative Jensen field.

The full remaining target is therefore the joint scalar polynomial

    K0+T K1+T^2K2+T^3K3>=0, all T>=0, all alpha,delta,x,y,

with the SAME fixed k-dependent coefficients. For example, a bound on the negative part of K1 against K0,K2,K3 could close it. Neither the stronger condition K1>=0 nor an unpaid independent norm bound is permissible. The exact4x4 original matrix remains available if this coefficient allocation is too strong.

## 4. Construction receipts and scope

construct_transverse_blocks.py SHA256bfcaa46873073424965f913b91c213eeebba470bb4beb33937c13f2244d69f73 completed once in1.172604057 seconds, rc0, external10-second cap. It reads the already frozen original matrix and performs exact elimination.

construct_remaining_quartic.py SHA2563d2f46af0b4cfa4abf4f1b457f5eedd09b227b1a56a19566e5a12d19ce89834c completed once in1.705496953 seconds, rc0, external5-second cap. It extracts the literal remaining two-mean matrix and determinant, not a numerical proposal. All signed forms are preserved in REMAINING_QUARTIC.json. No optimization, field/parameter grid or scientific retry occurred.

The author-derived existential small-positive-r adapted-Hessian interval remains separately valid and does not depend on solving this all-k joint payment. The full J_r problem for arbitrary compatible gradients and all affine means remains open in this work. No novelty claim or user-facing delivery is inferred.
