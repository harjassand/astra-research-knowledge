# Root reconstruction and branching extension

23 October 2026. Internal mathematics; historical novelty and physical utility UNKNOWN.
Pinned corpus e606bfc587c76bdcae8b8fa3ec33e721efa2fbac. This note reconstructs
w49 PROOF_V4.txt, SHA256 ccd777dd4daea424e19d6b8fd4e8c6842fb7f0614aa0fb325cc1744fe532da11.

## Independent reconstruction of the load-bearing steps

The actual unitary is V=sqrt(1-b)U+i sqrt(b)I, with the original central
root edge retained. For each initial radial shell H, charge conservation
gives final depth l=H+q-o, and charge covariance gives output-pinched Choi
matrix sum_(q,o) J_Hqo. Positive pinching costs exactly N+1.

I checked the potentially dangerous purifier and normalization factors:
the input in the Choi marginal is the unnormalized P_q, not P_q/dim P_q;
the initial purifier has dimension r_H=2^(H+1); and for its positive
complement Omega, Omega <= r_H Tr_F(Omega) tensor I_F. This costs r_H,
which cancels the 1/r_H in the shell diagonal comparison. It cannot be
silently omitted. The complement and Choi blocks share nonzero spectra.

For t>=1 the weighted bath CP map M_t=sum t^(qi+qo) Koi(.)Koi* has
M_t^N(sigma_H)=sum t^(q+o) omega_Hqo. On radial diagonal operators the
root interference vanishes. More robustly, the bounded positive operator
psi=2^(-L/2) obeys directly
M_t(psi)=g_b(t)psi+(1-b)(1-sqrt(2)t)P_root <= g_b(t)psi,
where g_b(t)=2sqrt(2)(1-b)t+b(1+2t^2). This also makes it unnecessary
to claim diagonal individual charge marginals. Positivity and
sigma_H <= psi/[r_H psi(H)] give the claimed bound after compressing
to the exact final depth l.

Consequently J_Hqo <= g^N t^(-q-o)2^(-(q-o)/2) I_Aq tensor I_Bo.
Because q-o>=-H, this is <=g^N(t sqrt(2))^H t^(-2o) times that
identity. Summing orthogonal q sectors introduces no multiplicity. The
actual shell law p_H=(2/3)3^(-H) gives exactly
sum p_H(t sqrt(2))^H=2/(3-t sqrt(2)). At t=sqrt(2), normalizing the
output weight B_t gives a product state diag(1/2,1/4,1/4)^tensor N,
and the global CP replacer coefficient is 2(N+1)(8+2b)^N.

The Bell bound is valid for a CPTP encoder: the untouched logical
reference stays I/K, and its product with any decoded normalized output
has Bell overlap 1/K^2. No physical-input purification assumption is
needed in this step. For entropy bounds one may instead purify the
physical input. Operator log monotonicity gives I(R:B)<=log C_N;
Ic<=min(Sinput,log C_N-Sinput), and purity gives actual complementary
leakage I(R:E F0)>=max(0,2Sinput-log C_N).

The normal-state extension is pointwise, not uniform. For fixed M,
P_<=M tau P_<=M <=3*6^M tau_pi, even with coherences. Fidelity is a
bounded positive initializer-linear functional. First N tends to
infinity at fixed M, then M tends to infinity. This covers each fixed
normal independent initializer, but not an adversarial horizon-dependent
initializer or initial input-bath correlations.

Verdict: I found no blocking defect in v4. This is an internal
reconstruction in addition to the separate fresh reviews, not formal or
external certification. The inherited positive lower still needs its
own proof reconstruction before asserting matching Theta(b).

## Root extension: arbitrary integer branching d>=1

Replace the two tree isometries by d prefix isometries, retain two
vacuum seeds joined by R, and use d+1 charge ports, q=diag(0,1,...,1).
Then U=[[R,S_1,...,S_d],[S_1*,0,...],...] is still a self-adjoint
involution: R^2+sum S_j S_j*=I and S_i* S_j=delta_ij I. The bath
is the (d+1)-regular tree. This changes the device; it is a proved
algebraic transfer candidate, not a claim about the original physical
apparatus.

Use psi=d^(-L/2), shell size r_H=2d^H. The weighted map obeys

g_(d,b)(t)=2sqrt(d)(1-b)t+b(1+d t^2),
M_t(psi)=g psi+(1-b)(1-sqrt(d)t)P_root <=g psi

for t>=1/sqrt(d). Its charge-block bound is
s_Hqo <=g^N t^(-q-o)d^(-(q-o)/2).
For any lambda>t sqrt(d), the faithful auxiliary normal state with
shell weights (1-1/lambda)lambda^(-H) yields CP coefficient

C_N=(N+1)(lambda-1)/(lambda-t sqrt(d))*h_(d,b)(t)^N,
h_(d,b)(t)=g_(d,b)(t)(1+d/t^2).

The original source state need not equal this auxiliary state: the same
finite-support domination argument transfers the rate ceiling to every
fixed normal independent initializer. Thus the generalized device has
unassisted no-feedback capacity bounded by

Q_d(b) <= (1/2)log_2 min_(1<=t<=sqrt(d)) h_(d,b)(t).

For d=1 the interval degenerates and the upper is 1 qubit/call. For
d>1, expand
h=2sqrt(d)(1-b)(t+d/t)+b(1+d^2+d t^2+d/t^2).
It is strictly convex for t>0, with derivative nonpositive at 1 and
nonnegative at sqrt(d), so this interval contains the global minimizer.
At b=0 the ceiling is 1+(1/2)log_2 d. At b=1 it is log_2(d+1),
as required for the identity port channel. No matching generalized lower
or efficient encoding claim is made.

The explicit t=sqrt(d) bound is
Q_d <=(1/2)log_2[4d+2(d-1)^2 b].
For the original d=2, optimization gives
t_*(b)=sqrt(2)-(3sqrt(2)/4)b+O(b^2),
min h=8+2b-(9/4)b^2+O(b^3), and hence
Q_2 <=3/2+b/(8 ln2)-5b^2/(32 ln2)+O(b^3).
This fourth-order correction in beta is not an exact-capacity claim.

The transfer follows the audited argument; it still requires a fresh
reader before consequential use. Choi/pinching/CP max-information tools
are established. The proposed new content is their evaluation for the
specified family of recurrent tree devices, subject to priority review.
