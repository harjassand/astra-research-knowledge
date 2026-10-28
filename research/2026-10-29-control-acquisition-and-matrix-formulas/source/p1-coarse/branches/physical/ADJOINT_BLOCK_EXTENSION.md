# Adjoint blocks, separate dual residuals, and identity centering

28 October 2026. Ordinary proof supporting the root future-word compiler.

## Physical interface

Let A_1,...,A_q be contractions selfadjoint in one physical Hilbert metric.
For a native block with chronological primitive word (j_1,...,j_m), write

    B = A_(j_m) ... A_(j_1).

B need not be selfadjoint. Its adjoint B*=A_(j_1)...A_(j_m) is executable by
reversing the existing primitive order. Both are contractions. This requires
no inverse dissipation and no new primitive operation. It retains the same
reset, matched readout and common physical metric premises as the primitive
construction. Products of individually reciprocal maps in different metrics
do not meet this premise.

Native scalar records may still identify a primitive word with its entire
primitive reversal. A nonsymmetric macro is NOT selfadjoint. One may not
identify a macro word with the reverse list of unchanged macro labels; each
macro must also be replaced by its adjoint, or expanded to native primitives.

## Two-sided algebra for arbitrary finite maps

Work over a real Hilbert space (Hermitian quantum operators with the real
Hilbert-Schmidt product are included). Let V:R^r -> H synthesize a finite
dictionary; no independence or hidden-dimension assumption is made. Let
Vc=b. For each selectable block B_i acquire

    G = V* V,
    M_i = V* B_i V,
    N_i^+ = V* B_i* B_i V,
    N_i^- = V* B_i B_i* V.

These are scalar echoes with the appropriate blocks and their executable
adjoints inserted. G,N_i^+,N_i^- are symmetric; M_i generally is not.

Choose arbitrary coefficient matrices T_i,U_i and put

    E_i = B_i V - V T_i,
    F_i = B_i* V - V U_i,
    D_i = M_i - G T_i,
    R_i = E_i* E_i
        = N_i^+ - M_i* T_i - T_i* M_i + T_i* G T_i,
    S_i = F_i* F_i
        = N_i^- - M_i U_i - U_i* M_i* + U_i* G U_i.

In particular, one cannot replace S_i by R_i without a separate identity.
Measured N_i^+ does not determine N_i^- in general. The relevant native block
words are B_i followed by B_i*, and B_i* followed by B_i, respectively.

For a chronological future block sequence i_1,...,i_h, define

    a_0=c,       a_t=T_(i_t) a_(t-1),
    z_h=c,       z_t=U_(i_(t+1)) z_(t+1),   t=h-1,...,0.

The corrected prediction is

    p = c* G a_h + sum_(t=1)^h z_t* D_(i_t) a_(t-1).

Then the exact remainder equals

    <b, B_(i_h)...B_(i_1)b> - p
      = sum_(1<=t<s<=h)
          <F_(i_s) z_s,
           B_(i_(s-1))...B_(i_(t+1)) E_(i_t) a_(t-1)>.

The empty middle product is the identity. Hence

    |true-p| <= sum_(t<s)
       sqrt(z_s* S_(i_s) z_s) sqrt(a_(t-1)* R_(i_t) a_(t-1)).

### Proof

Primal telescoping, using Vc=b, gives

    true - c*G a_h
      = sum_t <y_t, E_(i_t) a_(t-1)>,
    y_t = B_(i_(t+1))* ... B_(i_h)* b.

Backward telescoping gives

    y_t - Vz_t
      = sum_(s=t+1)^h
          B_(i_(t+1))* ... B_(i_(s-1))* F_(i_s) z_s.

Insert this identity into the first one. The Vz_t part is the signed
correction z_t*D_(i_t)a_(t-1). Move the adjoint middle product to the other
factor to obtain the displayed remainder. Cauchy-Schwarz and contraction of
each true B_i give the bound. Neither inversion of G nor a finite-rank
realization occurs in this proof.

All displayed moment forms are affine in native records once coefficient
maps and the requested word are fixed. The root's exact interval aggregation
therefore applies with these changed forms.

## A common computational metric

Suppose finite rational data certify, for a known W>0 and rho_f,rho_b<1,

    T_i* W T_i <= rho_f^2 W,
    U_i* W U_i <= rho_b^2 W,
    R_i <= eps_f^2 W,
    S_i <= eps_b^2 W.

Then every finite future word has remainder at most

    ||c||_W^2 eps_f eps_b / ((1-rho_f)(1-rho_b)).

Indeed its pair sum is bounded by
||c||_W^2 eps_f eps_b sum_(t<s) rho_f^(t-1) rho_b^(h-s),
and the latter geometric sum is bounded by the displayed denominator.
This does not assert a spectral gap for the true source.

One convenient choice is U_i=W^-1 T_i* W. It has exactly the same induced
W-norm as T_i. A certified T_i contraction then certifies U_i contraction
without a second search. It DOES NOT certify that F_i is small; S_i must
still be acquired and bounded. If W and T_i are rational, so is U_i.

W is a computational coefficient metric. It need not equal the physical
metric represented on the dictionary by G. Confusing these two roles would
wrongly turn a check on a surrogate into a claim about hidden dynamics.

## Non-symmetric moment uncertainty

The symmetric row-radius upper bound used for R_i and S_i remains valid
because they are symmetric residual forms. It cannot be applied directly as
a Loewner bound to M_i, which is generally non-symmetric.

Here is a sufficient finite certificate for the required bilinear error.
If an entrywise enclosure gives |Delta M_jk|<=r_jk, form

    D_row = diag_j sum_k r_jk,
    D_col = diag_k sum_j r_jk.

If D_row<=gamma W and D_col<=gamma W, then

    |y* Delta M x| <= gamma ||y||_W ||x||_W.

Proof: sum r_jk |y_j||x_k| is at most
(y*D_row y+x*D_col x)/2 by 2ab<=a^2+b^2. Apply the same argument to
lambda y and x/lambda, and minimize over positive lambda. This also covers
zero vectors by continuity. Equivalently, use a certified bound on the
symmetric dilation [[0,Delta M],[Delta M*,0]]. Shared raw-word interval
correlations can tighten the result, but ignoring them is conservative.

If the finite error satisfies this gamma_M bound and a corresponding gamma_G
Gram bound, a conservative uniform interval contribution for rho_f=rho_b=rho
is

    ||c||_W^2 [gamma_G + (gamma_M + rho gamma_G)/(1-rho)].

The exact word-dependent coefficient aggregation will usually be sharper.

## Identity centering is an available computation when its baseline is known

For unital trace-preserving channels on a known d-dimensional quantum system,
write b=I/d+b_0 with Tr(b_0)=0. Both identity and the traceless subspace are
invariant; they are Hilbert-Schmidt orthogonal. Thus the survival probability
satisfies

    Tr[b Phi_w(b)] = 1/d + <b_0, Phi_w(b_0)>_HS.

Subtracting the known 1/d from each measured scalar record gives the centered
moments with unchanged measurement radius. No physical preparation of the
nonpositive operator b_0 is needed. This removes the known common identity
mode before fitting finite coefficient maps. It does not remove other common
fixed operators, prove ergodicity or acquire an unknown hidden dimension.
If d or the complete reset/measurement support is unknown, 1/d is not a free
known baseline. Inaccessible memory must still satisfy the source contract.

## Exact alternating-projector example

For nonselective rank-one projective measurements on a qubit, the action on
traceless Hermitian operators is the Euclidean orthogonal projection onto the
measurement Bloch axis. In the x,z plane choose

    n=(0,1), m=(3/5,4/5), P=n n*, Q=m m*.

The blocks B_0=QP and B_1=PQ are executable reversed pairs. Explicitly,

    B_0=[[0,12/25],[0,16/25]],
    B_1=[[0,0],[12/25,16/25]]=B_0*.

Each primitive projection has norm one, while both blocks have norm 4/5.
This is a clean physical instance where grouping existing primitive operations
and subtracting the known identity exposes contraction without changing the
apparatus. For general higher-dimensional projective instruments there may
be a nontrivial common fixed algebra or angles arbitrarily close to zero;
no general strict contraction follows from alternation alone.

The companion exact-rational script checks acquisition identities, the
two-sided remainder, and the computational metric construction with a singular
dictionary. It is a fixture check of the proof and conventions, not evidence
for an operational cost advantage.

## Near-sharpness of the computational-gap uniform denominator

This short construction shows that the squared computational-gap denominator
is substantive even for one positive selfadjoint contraction. Choose
0<rho<1, 0<e^2<rho(1-rho), b=e_1, V=[b], T=[rho], W=[1], and

    A = [[rho, e], [e, 1-e^2/(1-rho)]].

Its eigenvalues are 1 and rho-e^2/(1-rho), both in [0,1]. The exact measured
residual form is R=e^2 and the signed defect is zero. Therefore the root
uniform bound is e^2/(1-rho)^2. But A has an exact conserved mode; its true
scalar response tends to

    lim_(h->infty) <b,A^h b>
      = e^2 / ((1-rho)^2+e^2),

while the finite prediction rho^h tends to zero. The ratio of the actual
limiting error to the certificate is

    (1-rho)^2 / ((1-rho)^2+e^2),

which tends to one as e/(1-rho) tends to zero. Thus the all-length theorem
does not secretly require a true hidden gap, and the denominator cannot
generally be improved in order under only its stated assumptions. A small
residual allows a correspondingly small permanently visible conserved
component; it does not prove that the component is absent.
