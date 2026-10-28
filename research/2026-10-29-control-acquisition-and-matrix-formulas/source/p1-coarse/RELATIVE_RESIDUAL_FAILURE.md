# Small relative defects do not control long switched programs

28 October 2026. A proposed escape from the contraction-margin dependence
fails in three real dimensions, for positive self-adjoint contractions, an
actual reachable-word dictionary and exact Galerkin maps.

## The failed sufficient condition

The inequalities E_i <= kappa^2 (I-T_i)*W(I-T_i), with kappa tending to zero,
do not imply an all-word output error tending to zero. Positivity, exact
source geometry, Galerkin orthogonality and absence of exact common fixed
vectors do not repair the implication.

Let 0<e<=1/4, d=e^2, s=1+d^2+e^2, b=(1,0,0), and

    u_+=(d,1,e), u_-=(-d,1,-e), A_i=I-u_i u_i*/s.

Both A_i are orthogonal projections. The two-word dictionary {b,A_+b}
spans S=span{b,h}, h=(0,1,e). In convenient coordinates V=[b,h],
W=diag(1,1+e^2), and h=((1+e^2)/d)b-(s/d)A_+b. Thus no inaccessible
hidden coordinate is supplied. The coordinate change is poorly scaled as
e shrinks, but this counterexample grants exact data.

For the exact Galerkin maps T_i=W^-1 V*A_iV and E_i=(A_iV-VT_i)*(A_iV-VT_i),

    E_+=0,
    E_-=kappa^2 (I-T_-)*W(I-T_-),
    kappa^2=4e^2/[(1+e^2)d^2+(1-e^2)^2] -> 0.

The squared norms of the S and S-perpendicular components of u_- are,
respectively, d^2+(1-e^2)^2/(1+e^2) and 4e^2/(1+e^2). Their ratio proves
the displayed identity, as both sides are the same rank-one form times
these respective squared norms.

## Arbitrarily large output failure

Both true operations fix k=(e,0,-d). Orthogonal invariance and contractivity
give, for every word, f(w)>=(e^2-d^2)/(e^2+d^2)=(1-e^2)/(1+e^2).
The reduced cycle C=T_-T_+ has rank one, C^2=lambda C, and

    lambda=1-chi, chi=4d^2/[(1+e^2)s^2].

For H=ceil(10/chi)+1 cycles its scalar output has absolute value at most
lambda^(H-1)<=exp(-10)<1/20000. The signed correction is zero because
these maps are exactly Galerkin.

Remove every exact conservation law by setting A'_i=(1-a)A_i and
T'_i=(1-a)T_i, where a=e^10. Now each true operator has norm 1-a<1.
The relative inequalities survive because I-T'_i=aI+(1-a)(I-T_i), whose
extra square and cross terms are positive in the W metric. Meanwhile

    f'(w)>=(1-2Ha)(1-e^2)/(1+e^2)

for the same 2H-operation word. Since H=O(e^-4), this tends to one.
The reduced output remains below 1/20000. Replacing the fixed threshold
10 by a larger constant makes the ultimate discrepancy arbitrarily close
to one.

## Executable proof receipts

`core/relative_residual_obstruction.py` uses exact rational identities and
elementary analytic power bounds. It does not physically execute the long
words. `results/RELATIVE_RESIDUAL_OBSTRUCTION.json` preserves all fixtures.

| e | kappa squared | Primitive word length | Proved gap lower bound |
|---|---:|---:|---:|
| 1/4 | 0.283108 | 1,550 | 0.880999 |
| 1/8 | 0.0644834 | 21,468 | 0.969161 |
| 1/16 | 0.0157475 | 331,548 | 0.992168 |
| 1/32 | 0.00391389 | 5,258,268 | 0.997999 |
| 1/64 | 0.000977039 | 83,947,548 | 0.999462 |

This rejects the proposed sufficient condition, not finite-rank realization,
the proved uniform bound with a margin, or a larger dictionary containing
all three dimensions. The missing slow direction is a joint property of
the operations. A gap-free replacement must retain a joint relation,
restrict its time/accuracy claim, or pay for source information that makes
the direction observable. Merely making each residual relative is not
enough. No broad priority claim about stability theory is made.
