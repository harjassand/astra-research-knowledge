# Block operations, reversed adjoints, and conserved components

28 October 2026. Extension of `THEORY.md`; the reviewed primitive code
remains unchanged. A block is an explicitly chosen finite sequence of
native selfadjoint contractions. Its operator B need not be selfadjoint,
but B* is implemented by reversing that sequence. Both are contractions.
Block construction changes experiment lengths; it supplies no free calls.

## 1. General primal and dual defect certificate

Keep dictionary V and b=Vc. For each block choose arbitrary forward and
dual coefficient maps T_i,S_i. Define

    D_i = B_i V - V T_i,       J_i = B_i* V - V S_i,
    F_i = V*D_i = M_i-G T_i,  M_i=V*B_i V,
    E_i = D_i*D_i
        = N_i-M_i* T_i-T_i* M_i+T_i*G T_i,
    K_i = J_i*J_i
        = Q_i-M_i S_i-S_i* M_i*+S_i*G S_i,
    N_i = V*B_i*B_i V,        Q_i=V*B_iB_i*V.          (1)

M_i is generally nonsymmetric. N_i and Q_i are different objects, acquired
with the two different block/reversed-block orders. They must not be
silently identified. All entries are scalar native words, not new state
measurements.

For chronological block word i_1,...,i_h, propagate alpha forward with T,
and beta backward with S. The corrected response is

    ftilde=c*G alpha_h+sum_t beta_t*F_(i_t)alpha_(t-1).

The exact remainder is

    sum_(s<t) <J_(i_t)beta_t,
        B_(i_(t-1))...B_(i_(s+1)) D_(i_s)alpha_(s-1)>.

Proof is the same two telescoping identities as Theorem 1, using B_i* in
the backward recurrence. Therefore the error is bounded by the sum of
products of forward E_i and backward K_i residual norms. This handles
arbitrary maps, including non-Galerkin or singular-dictionary proposals.

If both T_i and S_i contract a computational W>0 by rho<1, and both E_i
and K_i are <=epsilon^2 W, the same uniform bound

    ||c||_W^2 epsilon^2/(1-rho)^2

holds for every block word. No contraction gap on the actual hidden
complement is assumed. It covers the block language; a claim for every
unrestricted primitive word would be stronger and has not been proved.

## 2. Nonsymmetric uncertainty

The primitive implementation's symmetric matrix bound must be modified
for M_i. If |Delta M_jk|<=r_jk, define row sums a_j and column sums b_k.
Weighted Cauchy-Schwarz gives

    |x*Delta M y| <= sqrt(sum_j a_j x_j^2)
                       sqrt(sum_k b_k y_k^2).

If diag(max(a_j,b_j))<=gamma_M W, this is at most
gamma_M ||x||_W ||y||_W. The code certifies that PSD domination exactly.
Residual Grams remain symmetric and retain the row-radius upper matrix.
The uniform measurement term is the same as (7) in `THEORY.md` because
both coefficient trajectories contract by rho.

## 3. A completed example where blocks repair the failed certificate

For qubit projective dephasing, the identity is exactly preserved. On
traceless Bloch vectors, dephasing about a unit axis n acts as P_n=n n^T.
For a reset along z, survival probability is

    p(w)=(1+e_z^T P_w e_z)/2.

Thus subtracting the *known*, physically warranted identity contribution
and rescaling gives the centered scalar echo. This is not a signed-state
preparation and does not infer conservation from a noisy fit. A general
unknown device needs its own warrant for this subtraction.

The fixture uses n_0=(3/5,0,4/5) and n_1=(0,3/5,4/5). Each primitive
projector has norm one. The initial proposal's rho=0.9 common-contraction
check fails, as it should. Two-pulse blocks B_01=P_1P_0 and B_10=P_0P_1
are adjoints and each has norm |n_0 dot n_1|=16/25. A computational rho=0.7
certificate succeeds after acquiring the required forward and dual data.

The executed exact-rational synthetic receiver uses 32 source word
readings plus two standards, 122 native primitive executions, and maximum
query length six. The records include those used in the failed primitive
attempt; they are reused rather than discarded. The certified uniform
centered-amplitude error is 0.000017759383220575353. Thirty-eight finite
checks include 100-block/200-primitive tasks. The all-word conclusion comes
from the proved matrix inequalities, not the finite tests.

The quantum interpretation does not turn a mean reading into one photon
or one trial. With IID survival trials and desired centered-amplitude
radius a, Hoeffding plus a union bound needs

    N >= log(2m/delta)/(2(a/2)^2)

trials per acquired mean. At a=10^-6, m=32 and delta=.01, the illustrative
total is about 5.61e14 trials, before calibration/preparation overhead.
These trials were *not* executed. The synthetic receiver's ADC error was
10^-8; no assertion equates that analog error model with this illustrative
statistical budget. This conservative universal certificate has not shown
a practical quantum advantage.

## 4. What changed and what remains

The block representation addresses a real obstruction: a primitive can
retain a mode that is dissipated by a known sequence. Coarse composition
then changes the appropriate stability parameter. Reversed ordering
supplies the actual adjoint needed by the certificate. Finding or selecting
blocks, their durations, resets and extra echoes remain paid operations.

For finite families of positive contractions in finite dimension, a cycle
containing every primitive is strictly contracting off their common fixed
space; this is related to classical alternating projections. It supplies
no dimension-uniform quantitative gap. Infinite-dimensional sources can
have arbitrarily slow nearly conserved directions. The next missing
operation is acquiring a useful gap and residual at reasonable precision
and duration, or replacing difference-of-moment measurements by an actually
available positive residual detector. Such a detector is a stronger
interface and must be constructed, not assumed.
