# Full-algebra quotient certificate without an invariant section

28 October 2026. Separate derivation of the root's surjective-extension proposal. This is not yet received and is deliberately excluded from the frozen 14:17 science list until review. It reuses the received count/inverse/Choi-norm argument, but changes the algebraic interface. No novelty or universal lifting claim is made.

## 1. Candidate and data interfaces

Keep the acquired `r`-dimensional observable representation, in normalized preparation coordinates:

    C_z=H^(-1)H_z,    initial=e_1,    trace=m=1^T.

The same exact rank promise, finite legal experiment library, independent whole-process starts and simultaneous count event are required. Let full virtual Hermitian space have dimension `D=d²`, an orthonormal Hermitian basis and trace row `tau`.

A candidate supplies real matrices `P:R^D -> R^r`, `L:R^r -> R^D`, and a virtual initial density `rho_0`, satisfying

    P L=I_r,       tau=m P,
    rho_0>=0,      P rho_0=e_1.                        (S1)

Here a density is identified with its coefficient vector. Trace normalization follows from (S1). Crucially **rho_0 need not equal L e_1**, and neither `L` nor `P` is assumed CP. The right inverse is a charged linear algebra object, not a physical preparation channel.

Fit observable maps `Ctilde_z` and full maps `Wtilde_z` satisfying

    P Wtilde_z=Ctilde_z P,
    m sum_o Ctilde_(a,o)=m,
    tau sum_o Wtilde_(a,o)=tau,
    J(Wtilde_z)>=0.                                    (S2)

The kernel of `P` is invariant, but no invariant right-inverse image is required. For fixed `P`, constraints (S2) and fitted count residual objectives are linear/semidefinite in the maps; variable `P` search is nonconvex. Verifying `PL=I`, trace compatibility, initial positivity, full Choi constraints and all residuals is compulsory.

## 2. Certified exact extension

Use the received interval inversion to obtain `|C_z-Ctilde_z|<=E_z`, explicitly

    U=Hhat^(-1),  A=|U|D_H,  ||A||_infinity<1,
    M=(I-A)^(-1)|U|,
    E_z=M[D_z+D_H|Ctilde_z|+|Hhat Ctilde_z-Hhat_z|].

Define an existential exact full-space map

    W_z=Wtilde_z+L(C_z-Ctilde_z)P.                     (S3)

This map is used for the proof; the learner only implements the fit. Since `PL=I`,

    P W_z=C_z P.                                      (S4)

Since `tau L=m PL=m` and both observable trace identities hold,

    tau sum_o(W_z-Wtilde_z)=m sum_o(C_z-Ctilde_z)P=0.  (S5)

Thus full trace preservation is retained, not merely trace preservation on a selected subspace. The entrywise correction radius is

    F_z=|L|E_z|P|,       kappa_z>=||F_z||_F.            (S6)

Require a verified full Choi margin `J(Wtilde_z)>=m_z I` with `m_z>=kappa_z`. The Choi/Frobenius isometry then proves `W_z` CP on the entire matrix algebra. Equations (S4) and (S1) imply exact word probabilities:

    tau W_(z_H)...W_(z_1)rho_0
      =m C_(z_H)...C_(z_1)e_1.

This proves a finite virtual HQMM realization from ordinary data and explicit witnesses. No physical environment identification occurs. The same native half-diamond bound `(d/2) max_a sum_o kappa_(a,o)`, common-CP mixing coefficient `max_z kappa_z/m_z`, controller hybrid, clocked and adaptive reuse bounds apply exactly as in the received full-rank note.

For terminal probabilities `g_b`, fit rows `gtilde_b` whose full-space effects have coefficient rows `btilde_b=gtilde_b P`, are PSD, and sum to `tau`. Define the true full effect row `b_b=g_b P`. Then its perturbation row is `(g_b-gtilde_b)P`; the count/repair error multiplied by `|P|` gives an operator-norm radius. Subtract this radius before certifying each effect and charge the terminal measurement error. No post-terminal operation is needed. The rank promise must include all terminal effects.

## 3. A genuinely non-splitting full-space example

This is exact algebra, not new acquisition. Use the unnormalized qubit Pauli basis `(I,X,Y,Z)` and a unital channel with coefficient matrix

    W = [[1,0,0,0],
         [0,a,0,b],
         [0,0,a,0],
         [0,0,0,a]],       a=b=1/4.

Its Choi matrix equals the depolarizing-a Choi matrix plus `(b/2) Z^T tensor X`. The former has smallest eigenvalue `(1-a)/2=3/8`, and the latter has operator norm `b/2=1/8`. Hence `J(W)>=I/4`: the full channel has a strict CP interior margin.

Let `P0` retain just the `I,Z` coefficients. Then `P0 W=diag(1,a) P0`. Nevertheless **there is no invariant right inverse** of this quotient for this map. A section's Z-column must be `Z+uX+vY`; applying W gives `a(Z+uX+vY)+bX`, which cannot equal `a(Z+uX+vY)` because `b!=0`. Thus this provider does not secretly impose the preceding addendum's invariant-section condition.

Start at `rho_0=(I+Z/2)/2`. Add unsharp Z-test-and-reset branches

    X -> Tr[((I +/- Z/2)/2)X] rho_0.

Each branch has Choi minimum `1/16` and factors through `P0`; its sum is a TP reset. The core preparations `rho_0,W(rho_0)` and tests trace/positive-Z have determinant `-3/32`, so the process has observable rank two. Converting to preparation coordinates, put

    Q=[[1/2,1/2],[1/4,1/16]],
    P=Q^(-1)P0,       L=P0^T Q.

Then `PL=I`, `(1,1)P=(2,0,0,0)`, and `P rho_0=e_1`, satisfying (S1). Exact full CP maps satisfy (S2). The sampled-gauge theorem is not needed for this algebraic feasibility check.

This example separates **extension witnesses for the same full-space model**, not stochastic process classes: its two-dimensional observable law has other realizations, possibly injective/classical ones. It does not prove that all processes require this new certificate or that it reduces learning cost.

## 4. Remaining boundary and conventional comparison

This construction certifies a quotient of the **whole full matrix algebra**, with an explicitly fitted full CP instrument and a full-space initial density. It does not assume that CP on an abstract quotient implies a CP lift. Rather, it fits the lift and proves that an uncertainty correction remains CP.

An arbitrary physical realization may have a proper reachable subspace `W` and then a quotient `W/K`; it need not supply a map from all of `Herm(d)` satisfying the required kernel-invariance, trace compatibility and full CP fitting constraints. No theorem here converts every such reachable-subspace quotient into the full-algebra interface, bounds a suitable d, or efficiently finds P. Strict Choi interiors, inverse-core costs, `|L|E|P|` amplification, initial-state feasibility and finite-library/reset restrictions remain.

This is directly within the CP-realization/lifting setting of Monras–Winter (TQC 2014), particularly Sections 4–6 and their distinction between a CP quotient and a CP lift. Their general quotient-operator-system framework already motivates this question; calling the right inverse a “predictive lifting” is not novelty. The bounded result is an explicit finite-confidence sufficient witness for a full-algebra quotient subclass. [Primary paper](https://drops.dagstuhl.de/storage/00lipics/lipics-vol027-tqc2014/LIPIcs.TQC.2014.99/LIPIcs.TQC.2014.99.pdf).
