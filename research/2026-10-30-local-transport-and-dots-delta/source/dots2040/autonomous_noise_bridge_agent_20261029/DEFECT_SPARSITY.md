# Uniform equal-time defect sparsity under general local Markovian perturbations
Date: 2026-10-29. This is a leakage/clock-defect result, not a data fault-path threshold.

## Clean identities (root construction, independently verified)
On the entire physical space, define Q_x=I−P0_x,
R_x=Q_x−V_xV_x†,
E_xy=Q_xQ_y for edges x~y.

R_x is a positive projector: V_x†V_x=I on the ground ancilla sector. It projects onto excited states outside the intended Stinespring image. For guarded H,

[H,R_x]=0,
L_clean*(R_x)=−κ_x R_x,
[H,E_xy]=0,
L_clean*(E_xy)=−(κ_x+κ_y)E_xy.

R_x annihilates V_x,V_x† on both sides. A conflicting y Hamiltonian is guarded by P0_x and also annihilates R_x on both sides; nonconflicting terms have disjoint support. For the reset, L_xs†R_xL_xs=0, while {Q_x,R_x}=2R_x. All other reset terms commute. The edge identities follow similarly.

For any collection S of R_x with pairwise disjoint physical supports, P_S=Π_{x∈S}R_x is a projector and

L_clean*(P_S)=−(Σ_{x∈S}κ_x)P_S.

Products of edge defects similarly decay at κ times the number of distinct occupied ancillas, not twice the edge count when vertices repeat.

## Noise assumptions
Add Σ_β N_β(t), each a local trace-preserving Lindblad generator or Hamiltonian generator, acting on a fixed bounded region. Write ν_β(t)=||N_β*(t)||_{∞→∞}; a commutator generator has ν≤2||h|| and a single dissipator D[L] has ν≤2||L||². These finite bounds include thermal raising jumps. Assume:

1. every perturbation region touches at most b members of the chosen pairwise-disjoint defect-support family;
2. λ=sup_{x,t} Σ_{β: supp N_β intersects supp R_x} ν_β(t) is finite;
3. κ_x≥κ_min>0.

These are local assumptions independent of system size. Let q=(λ/κ_min)^(1/b)≤1.

## Theorem
If the initial state has no R defects (more generally, Tr(P_Sρ_0)≤q^|S| for every finite S in the separated family), then for every time t and every finite S,

Tr(P_Sρ_t)≤q^|S|.

Thus measurements of separated commuting defect projectors give an equal-time q-bounded random set, uniformly in volume and runtime, despite arbitrary local nonunitary Markovian perturbations and retained finite-κ ancillas.

## Proof
Let T_β(S) be the members of S touched by perturbation β. By locality, if T_β is empty its contribution vanishes. Otherwise,

N_β*(P_S)=P_{S\T_β} N_β*(P_{T_β}).

The two factors have disjoint supports. N_β* preserves Hermiticity and ||P_{T_β}||≤1, so

N_β*(P_S)≤ν_β P_{S\T_β}

in operator order. Therefore m_S(t)=Tr(P_Sρ_t) satisfies

m'_S≤−|S|κ_min m_S+Σ_{β:T_β≠empty}ν_β m_{S\T_β}.

Induct on r=|S|, with m_empty=1. At a first potential crossing m_S=q^r, all lower-order moments are bounded by q to their cardinality. At most b factors are removed by each perturbation, and Σ_{β:T_β≠empty}ν_β≤rλ. Thus the source is at most rλ q^{max(r−b,0)}. For r≥b this equals rκ_min q^r; for r<b it is no greater than rκ_min q^r because q^b≤q^r. Hence the derivative cannot cross upward. Equivalently the scalar comparison formula proves the invariant bound without relying on differentiability of a first-crossing time. Time-dependent locally bounded coefficients follow by integration/approximation.

## Why this is not the missing compiler theorem
R defects measure departure from the local Stinespring encoding, not errors within encoded data. Their decay does not undo a data error already emitted. The theorem provides equal-time spatial sparsity, not a distribution of all spacetime data faults or coherent fault amplitudes. Temporal defect correlations persist for O(1/κ), and adjacent defects need clustering rather than multiplication. Moreover the baseline Hamiltonian remains bounded-support many-body, not two-body. These distinctions must be retained in any threshold claim.
